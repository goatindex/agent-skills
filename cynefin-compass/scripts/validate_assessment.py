#!/usr/bin/env python3
"""Validate a Cynefin Compass assessment (JSON).

Checks the contract in references/assessment-schema.json and the lint rules
in references/classification.md ("Lint rules"). Standard library only.

Usage: python3 validate_assessment.py [--json] <assessment.json>
  --json   print one JSON object {"ok", "fails", "warns"} instead of text.
Exit: 0 = pass (warnings allowed), 1 = one or more FAILs, 2 = usage/IO error.
"""

import json
import re
import sys

SCHEMA_VERSION = "1"
DOMAINS = ("clear", "complicated", "complex", "chaotic")
SEQUENCE = {
    "clear": "sense-categorise-respond",
    "complicated": "sense-analyse-respond",
    "complex": "probe-sense-respond",
    "chaotic": "act-sense-respond",
}
PROCEDURE_KEYS = (
    "active_crisis",
    "known_practice_applies",
    "expert_can_determine_before_acting",
    "hindsight_only",
)
MAX_PROBES = 3
MIN_EVIDENCE_WORDS = 6
# Evidence that is only a label. Compared after normalisation.
GENERIC_EVIDENCE = {
    "it is complex", "its complex", "this is complex", "it is complicated",
    "its complicated", "many stakeholders", "it is hard", "it is difficult",
    "unclear", "lots of unknowns", "high stakes", "it is urgent",
    "it is a crisis", "it is routine", "na", "n a", "tbd", "todo",
}
# Phased-plan language on a Complex piece = Complex-as-Complicated.
PLAN_RE = re.compile(
    r"\b(phase\s*\d+|phase (?:one|two|three)|roadmap|gantt|big[- ]bang"
    r"|comprehensive plan|full plan)\b",
    re.I,
)


def words(text):
    return len(re.findall(r"\w+", text))


def norm(text):
    return " ".join(re.findall(r"\w+", text.lower()))


def classify_from_answers(ans):
    """Ordered procedure from references/classification.md. Returns a domain
    name, 'confused' when no question is answered yes, or None when the
    answers are malformed."""
    if not isinstance(ans, dict) or any(
        not isinstance(ans.get(k), bool) for k in PROCEDURE_KEYS
    ):
        return None
    if ans["active_crisis"]:
        return "chaotic"
    if ans["known_practice_applies"]:
        return "clear"
    if ans["expert_can_determine_before_acting"]:
        return "complicated"
    if ans["hindsight_only"]:
        return "complex"
    return "confused"


class Findings:
    def __init__(self):
        self.fails = []
        self.warns = []

    def fail(self, path, msg):
        self.fails.append(f"{path}: {msg}")

    def warn(self, path, msg):
        self.warns.append(f"{path}: {msg}")

    @property
    def ok(self):
        return not self.fails


def need_str(f, obj, key, path, min_words=1):
    val = obj.get(key) if isinstance(obj, dict) else None
    if not isinstance(val, str) or words(val) < min_words:
        f.fail(f"{path}.{key}", f"required text, at least {min_words} word(s)")
        return None
    return val


def need_str_list(f, obj, key, path, min_items=1):
    val = obj.get(key) if isinstance(obj, dict) else None
    if (
        not isinstance(val, list)
        or len(val) < min_items
        or any(not isinstance(x, str) or not x.strip() for x in val)
    ):
        f.fail(f"{path}.{key}", f"required list of text, at least {min_items} item(s)")
        return None
    return val


def check_probe(f, probe, path):
    if not isinstance(probe, dict):
        f.fail(path, "probe must be an object")
        return
    need_str(f, probe, "action", path)
    sf = probe.get("safe_to_fail")
    if not isinstance(sf, dict):
        f.fail(f"{path}.safe_to_fail", "required object")
    else:
        if sf.get("reversible") is not True:
            f.fail(
                f"{path}.safe_to_fail.reversible",
                "must be true. A probe that cannot be undone is not safe to fail. "
                "Redesign it smaller.",
            )
        need_str(f, sf, "bounded_cost", f"{path}.safe_to_fail")
        need_str(f, sf, "why", f"{path}.safe_to_fail", min_words=3)
    for key in ("signal", "amplify_if", "dampen_if", "time_box"):
        need_str(f, probe, key, path)


def check_approach(f, piece, domain, path):
    ap = piece.get("approach")
    apath = f"{path}.approach"
    if not isinstance(ap, dict):
        f.fail(apath, "required object")
        return
    seq = ap.get("sequence")
    if seq != SEQUENCE[domain]:
        f.fail(
            f"{apath}.sequence",
            f"domain '{domain}' needs '{SEQUENCE[domain]}', got {seq!r}",
        )
    summary = need_str(f, ap, "summary", apath, min_words=3)

    if domain == "clear":
        need_str(f, ap, "practice", apath)
        if ap.get("probes"):
            f.fail(f"{apath}.probes", "clear work applies known practice. Do not add probes.")
        if piece.get("boundary_risk") in (None, ""):
            f.fail(
                f"{path}.boundary_risk",
                "required for clear. State how complacency could push this over the cliff to chaotic.",
            )
    elif domain == "complicated":
        need_str(f, ap, "analysis_needed", apath)
        need_str_list(f, ap, "experts", apath)
    elif domain == "complex":
        probes = ap.get("probes")
        if not isinstance(probes, list) or not probes:
            f.fail(f"{apath}.probes", "complex needs 1-3 safe-to-fail probes")
        else:
            if len(probes) > MAX_PROBES:
                f.fail(
                    f"{apath}.probes",
                    f"{len(probes)} probes. Maximum is {MAX_PROBES}. "
                    "More than that is a plan, not probes.",
                )
            for i, probe in enumerate(probes):
                check_probe(f, probe, f"{apath}.probes[{i}]")
        texts = [summary or ""]
        if isinstance(probes, list):
            texts += [
                p.get("action", "") for p in probes
                if isinstance(p, dict) and isinstance(p.get("action"), str)
            ]
        for text in texts:
            m = PLAN_RE.search(text)
            if m:
                f.fail(
                    apath,
                    f"phased-plan wording '{m.group(0)}' on a complex piece "
                    "(Complex-as-Complicated). Replace with probes.",
                )
                break
    elif domain == "chaotic":
        act = ap.get("stabilising_action")
        if not isinstance(act, str) or not act.strip():
            f.fail(
                f"{apath}.stabilising_action",
                "required: ONE action as one text value, taken now",
            )
        elif words(act) > 30:
            f.warn(f"{apath}.stabilising_action", "over 30 words. Is this one action?")
        need_str(f, ap, "sense_after", apath)


def check_piece(f, piece, path):
    if not isinstance(piece, dict):
        f.fail(path, "piece must be an object")
        return None
    pid = piece.get("id")
    if not isinstance(pid, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", pid):
        f.fail(f"{path}.id", "required, lowercase letters, digits and hyphens")
    need_str(f, piece, "name", path)

    domain = piece.get("domain")
    if domain not in DOMAINS:
        f.fail(
            f"{path}.domain",
            f"must be one of {', '.join(DOMAINS)}. "
            "'confused' is not a final result: decompose the situation.",
        )
        return pid

    # Procedure cross-check (deterministic classification).
    ans = piece.get("procedure_answers")
    expected = classify_from_answers(ans)
    override = piece.get("override_reason")
    if expected is None:
        f.fail(
            f"{path}.procedure_answers",
            f"required object with boolean keys: {', '.join(PROCEDURE_KEYS)}",
        )
    elif expected == "confused":
        f.fail(
            f"{path}.procedure_answers",
            "all four answers are no. This piece is Confused. Decompose it into smaller pieces.",
        )
    elif expected != domain:
        if not isinstance(override, str) or words(override) < 6:
            f.fail(
                f"{path}.domain",
                f"procedure answers give '{expected}', piece says '{domain}'. "
                "Fix the answers or add override_reason (6+ words).",
            )
    elif override:
        f.warn(f"{path}.override_reason", "present but the procedure already agrees. Remove it.")

    # Evidence.
    ev = need_str_list(f, piece, "evidence", path)
    if ev:
        for i, item in enumerate(ev):
            if norm(item) in GENERIC_EVIDENCE:
                f.fail(f"{path}.evidence[{i}]", f"generic label {item!r}. Give a fact of this situation.")
            elif words(item) < MIN_EVIDENCE_WORDS:
                f.warn(f"{path}.evidence[{i}]", f"under {MIN_EVIDENCE_WORDS} words. Is it a specific fact?")

    # Second reading.
    sr = piece.get("second_reading")
    if not isinstance(sr, dict):
        f.fail(f"{path}.second_reading", "required object")
    else:
        if sr.get("domain") not in DOMAINS:
            f.fail(f"{path}.second_reading.domain", f"must be one of {', '.join(DOMAINS)}")
        elif sr.get("domain") == domain:
            f.fail(f"{path}.second_reading.domain", "must differ from the primary domain")
        need_str(f, sr, "tipping_condition", f"{path}.second_reading", min_words=4)

    if "boundary_risk" not in piece:
        f.fail(f"{path}.boundary_risk", "key required (text, or null when none)")
    elif piece["boundary_risk"] is not None and not isinstance(piece["boundary_risk"], str):
        f.fail(f"{path}.boundary_risk", "must be text or null")

    need_str_list(f, piece, "reclassify_triggers", path)
    check_approach(f, piece, domain, path)
    return pid


def validate(doc):
    f = Findings()
    if not isinstance(doc, dict):
        f.fail("$", "assessment must be a JSON object")
        return f
    if doc.get("schema_version") != SCHEMA_VERSION:
        f.fail("schema_version", f"must be {SCHEMA_VERSION!r}")
    if doc.get("mode") not in ("lite", "full"):
        f.fail("mode", "must be 'lite' or 'full'")
    need_str(f, doc, "situation", "$", min_words=3)

    gate = doc.get("gate")
    changes = None
    if not isinstance(gate, dict) or not isinstance(gate.get("changes_approach"), bool):
        f.fail("gate.changes_approach", "required boolean")
    else:
        changes = gate["changes_approach"]
        need_str(f, gate, "reason", "gate", min_words=4)

    pieces = doc.get("pieces")
    if not isinstance(pieces, list):
        f.fail("pieces", "required list")
        return f
    single = doc.get("is_single_problem")
    if not isinstance(single, bool):
        f.fail("is_single_problem", "required boolean")

    if changes is False:
        if pieces:
            f.fail("pieces", "gate.changes_approach is false. The skill is skipped, so pieces must be empty.")
        return f
    if changes is True and not pieces:
        f.fail("pieces", "gate.changes_approach is true. At least one piece is required.")

    if isinstance(single, bool):
        if single and len(pieces) > 1:
            f.fail("is_single_problem", f"true, but {len(pieces)} pieces are listed")
        if not single and len(pieces) < 2:
            f.fail("is_single_problem", "false means decomposed. At least 2 pieces are required.")

    seen = set()
    for i, piece in enumerate(pieces):
        pid = check_piece(f, piece, f"pieces[{i}]")
        if pid:
            if pid in seen:
                f.fail(f"pieces[{i}].id", f"duplicate id {pid!r}")
            seen.add(pid)
    return f


def main(argv):
    args = [a for a in argv[1:] if a != "--json"]
    as_json = "--json" in argv[1:]
    if len(args) != 1:
        print(__doc__, file=sys.stderr)
        return 2
    try:
        with open(args[0], encoding="utf-8") as fh:
            doc = json.load(fh)
    except (OSError, ValueError) as exc:
        print(f"cannot read {args[0]}: {exc}", file=sys.stderr)
        return 2
    f = validate(doc)
    if as_json:
        print(json.dumps({"ok": f.ok, "fails": f.fails, "warns": f.warns}, indent=2))
    else:
        for line in f.fails:
            print(f"FAIL {line}")
        for line in f.warns:
            print(f"WARN {line}")
        print("PASS" if f.ok else f"FAIL ({len(f.fails)} problem(s))")
    return 0 if f.ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
