#!/usr/bin/env python3
"""AQI aggregation — deterministic scoring arithmetic. stdlib only (floor-compliant).

Usage: python3 aggregate.py findings.json [--input-run input_findings.json]

Consumes an evaluator-authored canonical findings object (scores + evidence),
computes everything that must never be vibed: letters, severity uplift,
composites, caps, coupling, gate decision, and the prioritised finding order.
Writes the completed object to stdout. Exits non-zero on invariant violations.

Design notes (per skill-architecture doctrine):
- This is disposable glue. The durable core is the rubric + schema. If this
  script cannot run, the same arithmetic is simple enough for the agent to
  perform by instruction — the rules below are the specification.
"""
import json
import sys

LETTERS = {4: "A", 3: "B", 2: "C", 1: "D", 0: "F"}
SEV_ORDER = ["critical", "high", "medium", "low"]
EFF_ORDER = ["low", "medium", "high"]
GATING = {"inputs": {"completeness", "consistency"},
          "outputs": {"coverage", "traceability"}}
REQUIRED_DIMS = {
    "inputs": {"completeness", "consistency", "currency", "conformity", "clarity"},
    "outputs": {"coverage", "traceability", "consistency", "conformity", "actionability", "clarity"},
}


def fail(msg):
    print(f"AQI VALIDATION FAILURE: {msg}", file=sys.stderr)
    sys.exit(1)


def composite_letter(v):
    if v >= 3.5: return "A"
    if v >= 2.5: return "B"
    if v >= 2.0: return "C"
    if v >= 1.0: return "D"
    return "F"


def uplift(sev):
    i = SEV_ORDER.index(sev)
    return SEV_ORDER[max(0, i - 1)]


def effective_score(dim):
    """Unscorable / null score is treated as 0 (no citation, no score)."""
    return dim["score"] if dim.get("score") is not None else 0


def validate_and_normalise(obj):
    mode = obj["mode"]
    dims = {d["id"]: d for d in obj["dimensions"]}

    missing = REQUIRED_DIMS[mode] - set(dims)
    if missing:
        fail(f"mode '{mode}' missing dimensions: {sorted(missing)}")

    for d in obj["dimensions"]:
        # Evidence rule: no citation, no score
        if d.get("score") is not None and not d.get("evidence"):
            fail(f"{d['id']}: non-null score with no evidence")
        if d.get("score") is None and not d.get("unscorable"):
            fail(f"{d['id']}: null score must set unscorable=true")
        # Clarity: dimension score = min(sub-tests)
        if d["id"] == "clarity" and d.get("sub_scores"):
            lo = min(d["sub_scores"]["surface_clarity"], d["sub_scores"]["specificity"])
            if d.get("score") != lo:
                fail(f"clarity: score {d.get('score')} != min(sub_scores) {lo}")
        # Conformity never in composite
        if d["id"] == "conformity" and d.get("in_composite"):
            fail("conformity: in_composite must be false (neutral valence)")
        # Gating flags must match mode
        expected_gating = d["id"] in GATING[mode]
        if d.get("gating") != expected_gating:
            fail(f"{d['id']}: gating must be {expected_gating} in mode '{mode}'")
        d["letter"] = LETTERS[effective_score(d)]
    return dims


def apply_severity_uplift(obj):
    # Severity uplift keys off INTRINSIC complexity only. The conformity-driven
    # effort_tier governs review depth and the evidentiary bar, NOT severity —
    # otherwise novelty would be charged twice (more scrutiny AND inflated
    # severity). A simple system stays a simple system for severity purposes.
    tier = obj["complexity"]["tier"]
    high_tier = tier in ("T3", "T4")
    for f in obj["findings"]:
        f["severity"] = uplift(f["severity_raw"]) if high_tier else f["severity_raw"]
        f["tier_uplifted"] = high_tier and f["severity"] != f["severity_raw"]


def conformity_effort_uplift(obj, dims):
    """Input Conformity <= 1 raises the EFFORT tier one step (max T4).
    Effort tier drives review depth and evidentiary bar — never severity."""
    if obj["mode"] != "inputs":
        return
    tiers = ["T1", "T2", "T3", "T4"]
    base = obj["complexity"]["tier"]
    if effective_score(dims["conformity"]) <= 1:
        obj["complexity"]["effort_tier"] = tiers[min(3, tiers.index(base) + 1)]
    else:
        obj["complexity"]["effort_tier"] = base


def compute_composite(obj, dims, input_composite=None):
    mode = obj["mode"]
    comp_dims = [d for d in obj["dimensions"] if d.get("in_composite")]
    total_w = sum(d.get("weight", 1.0) for d in comp_dims)
    mean = sum(effective_score(d) * d.get("weight", 1.0) for d in comp_dims) / total_w

    gating_scores = [effective_score(dims[g]) for g in GATING[mode]]
    lowest_gate = min(gating_scores)
    cap = lowest_gate + 1
    value = min(mean, cap)

    coupling = None
    if mode == "outputs" and input_composite is not None:
        c = obj.get("coupling", {})
        evidenced = bool(c.get("independent_discovery_evidenced"))
        if evidenced and not c.get("independent_discovery_refs"):
            fail("coupling: independent_discovery_evidenced=true requires refs")
        ccap = input_composite + (1 if evidenced else 0)
        coupling = {**c, "input_composite": input_composite,
                    "cap": ccap, "breach": mean > ccap}
        value = min(value, ccap)

    obj["composite"] = {
        "raw_weighted_mean": round(mean, 3),
        "lowest_gating_score": lowest_gate,
        "cap": cap,
        "value": round(value, 3),
        "letter": composite_letter(value),
        "hard_rule_triggered": lowest_gate <= 1,
    }
    if coupling is not None:
        obj["coupling"] = coupling
        if coupling["breach"]:
            emit_breach_finding(obj, mean, ccap, input_composite)
    return value, lowest_gate


def emit_breach_finding(obj, mean, ccap, input_composite):
    """A coupling breach IS a finding (doctrine). Make it one in the data, not
    just in prose, so it carries severity/effort and appears in the sorted list.
    Idempotent: never doubles up if the script is re-run."""
    if any(f.get("dimension") == "coupling" for f in obj["findings"]):
        return
    obj["findings"].append({
        "finding_id": "F000",
        "dimension": "coupling",
        "severity_raw": "high",
        "effort": "high",
        "action": (f"Assessment self-quality (pre-cap mean {round(mean, 2)}) exceeds "
                   f"what the inputs support (cap {ccap}, input composite {input_composite}). "
                   "Either evidence independent discovery in the traceability chain, "
                   "re-score the inputs with assessor-gathered evidence added to the "
                   "artefact register, or temper the assessment's confidence."),
        "evidence_ref": {"artefact_id": "composite", "location": "coupling cap"},
        "requestor_ask": None,
    })


def compute_gate(obj, value, lowest_gate):
    reasons = []
    if obj["mode"] == "inputs":
        if lowest_gate <= 1:
            decision = "return"
            reasons.append(f"hard rule: gating dimension at {lowest_gate} (<=1)")
        elif value < 2.0:
            decision = "return"
            reasons.append(f"composite {value:.2f} below 2.0 threshold")
        elif value < 3.0:
            decision = "proceed_with_caveats"
            reasons.append(f"composite {value:.2f} in caveat band 2.0-2.9")
        else:
            decision = "proceed"
            reasons.append(f"composite {value:.2f} >= 3.0")
    else:
        if lowest_gate <= 1:
            decision = "rework"
            reasons.append(f"hard rule: gating dimension at {lowest_gate} (<=1)")
        else:
            decision = "proceed"
            reasons.append(f"composite {value:.2f}; gates clear")
        if obj.get("coupling", {}).get("breach"):
            reasons.append("coupling cap breached: confidence exceeds what inputs support — logged as a finding")
    existing = obj.get("gate", {})
    obj["gate"] = {"decision": decision, "reasons": reasons,
                   "caveats": existing.get("caveats", [])}


def check_patternability(obj, dims, value):
    if obj["mode"] != "outputs" or "patternability" not in obj:
        return
    p = obj["patternability"]
    elig = {
        "composite_gte_3": value >= 3.0,
        "traceability_gte_3": effective_score(dims["traceability"]) >= 3,
        "conformity_gte_3": effective_score(dims["conformity"]) >= 3,
    }
    p["eligibility_check"] = elig
    if p.get("flag") == "pattern_candidate" and not (elig["composite_gte_3"] and elig["traceability_gte_3"]):
        fail("patternability: pattern_candidate requires composite >= 3.0 and traceability >= 3")
    if p.get("flag") == "pattern_conformant":
        if not p.get("pattern_ref"):
            fail("patternability: pattern_conformant requires pattern_ref")
        if not elig["conformity_gte_3"]:
            fail("patternability: pattern_conformant requires conformity >= 3")


def sort_findings(obj):
    obj["findings"].sort(key=lambda f: (SEV_ORDER.index(f["severity"]),
                                        EFF_ORDER.index(f["effort"]),
                                        f["finding_id"]))


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    with open(args[0]) as fh:
        obj = json.load(fh)

    input_composite = None
    if "--input-run" in args:
        with open(args[args.index("--input-run") + 1]) as fh:
            input_run = json.load(fh)
        input_composite = input_run.get("composite", {}).get("value")
        if input_composite is None:
            fail("--input-run object has no computed composite; aggregate it first")
        obj.setdefault("coupling", {})["input_run_ref"] = input_run["subject"]["reference"]

    if obj["mode"] == "outputs" and input_composite is None:
        fail("outputs mode requires --input-run (coupling rule cannot be skipped)")

    dims = validate_and_normalise(obj)
    conformity_effort_uplift(obj, dims)
    value, lowest_gate = compute_composite(obj, dims, input_composite)
    apply_severity_uplift(obj)
    compute_gate(obj, value, lowest_gate)
    check_patternability(obj, dims, value)
    sort_findings(obj)

    json.dump(obj, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
