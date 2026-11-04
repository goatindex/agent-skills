#!/usr/bin/env python3
"""Render a validated Cynefin Compass assessment (JSON) to a markdown report.

Refuses to render when validate_assessment.py reports any FAIL. The output
format is the one lint_report.py checks. Standard library only.

Usage: python3 render_report.py <assessment.json> [-o report.md]
Exit: 0 = rendered, 1 = assessment failed validation, 2 = usage/IO error.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_assessment import SEQUENCE, validate  # noqa: E402

ARROW = {
    "sense-categorise-respond": "sense → categorise → respond",
    "sense-analyse-respond": "sense → analyse → respond",
    "probe-sense-respond": "probe → sense → respond",
    "act-sense-respond": "act → sense → respond",
}


def cap(domain):
    return domain.capitalize()


def title_of(situation):
    """First sentence of the situation, cut at a word boundary."""
    first = situation.strip().splitlines()[0].split(". ")[0].rstrip(".")
    if len(first) > 100:
        first = first[:100].rsplit(" ", 1)[0] + "..."
    return first


def render_skip(doc):
    return (
        "# Cynefin gate: no assessment needed\n\n"
        f"**Situation:** {doc['situation']}\n\n"
        "**Decision:** Skipped. Naming the domain does not change the next step.\n\n"
        f"**Reason:** {doc['gate']['reason']}\n"
    )


def render_classification(piece):
    sr = piece["second_reading"]
    lines = [
        f"### Piece {piece['id']}: {piece['name']}",
        "",
        f"- **Primary domain:** {cap(piece['domain'])}",
        "- **Evidence:**",
    ]
    lines += [f"  - {e}" for e in piece["evidence"]]
    lines.append(f"- **Second reading:** {cap(sr['domain'])}. Tips if: {sr['tipping_condition']}")
    risk = piece["boundary_risk"] or "None identified."
    lines.append(f"- **Boundary risk:** {risk}")
    if piece.get("override_reason"):
        lines.append(f"- **Override of procedure:** {piece['override_reason']}")
    lines.append("")
    return lines


def render_approach(piece):
    ap = piece["approach"]
    domain = piece["domain"]
    lines = [
        f"### Piece {piece['id']}: {piece['name']} ({ARROW[SEQUENCE[domain]]})",
        "",
        ap["summary"],
        "",
    ]
    if domain == "clear":
        lines.append(f"- **Practice:** {ap['practice']}")
    elif domain == "complicated":
        lines.append(f"- **Analysis needed:** {ap['analysis_needed']}")
        lines.append(f"- **Experts:** {', '.join(ap['experts'])}")
    elif domain == "complex":
        for i, probe in enumerate(ap["probes"], 1):
            sf = probe["safe_to_fail"]
            lines += [
                f"- **Probe {i}:** {probe['action']}",
                f"  - Safe to fail: {sf['why']} (cost bound: {sf['bounded_cost']}; reversible)",
                f"  - Signal: {probe['signal']}",
                f"  - Amplify if: {probe['amplify_if']}",
                f"  - Dampen if: {probe['dampen_if']}",
                f"  - Time box: {probe['time_box']}",
            ]
            if probe.get("owner"):
                lines.append(f"  - Owner: {probe['owner']}")
    elif domain == "chaotic":
        lines.append(f"- **Stabilising action:** {ap['stabilising_action']}")
        lines.append(f"- **Sense after:** {ap['sense_after']}")
    lines.append("")
    return lines


def render(doc):
    if not doc["gate"]["changes_approach"]:
        return render_skip(doc)
    pieces = doc["pieces"]
    out = [f"# Cynefin assessment: {title_of(doc['situation'])}", ""]
    out += [f"Mode: {doc['mode']}", ""]
    out += ["## 1. The situation", "", doc["situation"], ""]
    out += ["## 2. Is this one problem or several?", ""]
    if doc["is_single_problem"]:
        out.append("One problem. No decomposition needed.")
    else:
        out.append(f"{len(pieces)} problems in different parts of the situation:")
        out += [f"- {p['id']}: {p['name']}" for p in pieces]
    out.append("")
    out += ["## 3. Domain classification", ""]
    for p in pieces:
        out += render_classification(p)
    out += ["## 4. The working approach", ""]
    for p in pieces:
        out += render_approach(p)
    out += ["## 5. What would change the diagnosis", ""]
    for p in pieces:
        for t in p["reclassify_triggers"]:
            out.append(f"- [{p['id']}] {t}")
    out.append("")
    return "\n".join(out)


def main(argv):
    args = argv[1:]
    out_path = None
    if "-o" in args:
        i = args.index("-o")
        if i + 1 >= len(args):
            print(__doc__, file=sys.stderr)
            return 2
        out_path = args[i + 1]
        del args[i:i + 2]
    if len(args) != 1:
        print(__doc__, file=sys.stderr)
        return 2
    try:
        with open(args[0], encoding="utf-8") as fh:
            doc = json.load(fh)
    except (OSError, ValueError) as exc:
        print(f"cannot read {args[0]}: {exc}", file=sys.stderr)
        return 2
    findings = validate(doc)
    if not findings.ok:
        for line in findings.fails:
            print(f"FAIL {line}", file=sys.stderr)
        print("Not rendered. Fix the assessment first.", file=sys.stderr)
        return 1
    text = render(doc)
    if out_path:
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(text)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
