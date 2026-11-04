#!/usr/bin/env python3
"""Lint a Cynefin Compass markdown report.

Use it on reports written by render_report.py, and on hand-written reports
that must follow the same format. Standard library only.

Usage: python3 lint_report.py <report.md>
Exit: 0 = pass, 1 = one or more FAILs, 2 = usage/IO error.
"""

import re
import sys

DOMAINS = ("Clear", "Complicated", "Complex", "Chaotic")
HEADINGS = (
    "## 1. The situation",
    "## 2. Is this one problem or several?",
    "## 3. Domain classification",
    "## 4. The working approach",
    "## 5. What would change the diagnosis",
)
CLASS_LABELS = ("Primary domain", "Evidence", "Second reading", "Boundary risk")
REQUIRED = {
    "Clear": ("Practice",),
    "Complicated": ("Analysis needed", "Experts"),
    "Chaotic": ("Stabilising action", "Sense after"),
}
PROBE_LINES = ("Signal:", "Amplify if:", "Dampen if:", "Time box:", "Safe to fail:")
MAX_PROBES = 3


def split_sections(lines):
    """Return {heading: [lines]} for '## ' headings."""
    sections, cur = {}, None
    for line in lines:
        if line.startswith("## "):
            cur = line.strip()
            sections[cur] = []
        elif cur is not None:
            sections[cur].append(line)
    return sections


def split_pieces(lines):
    """Return {piece_id: [lines]} for '### Piece <id>: ...' headings."""
    pieces, cur = {}, None
    for line in lines:
        m = re.match(r"### Piece ([a-z0-9][a-z0-9-]*):", line)
        if m:
            cur = m.group(1)
            pieces[cur] = []
        elif cur is not None:
            pieces[cur].append(line)
    return pieces


def lint(text):
    fails = []
    lines = text.splitlines()
    if lines and lines[0].startswith("# Cynefin gate:"):
        for label in ("**Decision:**", "**Reason:**"):
            if not any(label in l and len(l.split(label, 1)[1].strip()) > 3 for l in lines):
                fails.append(f"gate report: missing {label}")
        return fails
    if not lines or not lines[0].startswith("# Cynefin assessment:"):
        fails.append("line 1 must start with '# Cynefin assessment:' or '# Cynefin gate:'")

    sections = split_sections(lines)
    last = -1
    for h in HEADINGS:
        if h not in sections:
            fails.append(f"missing heading '{h}'")
            continue
        idx = next(i for i, l in enumerate(lines) if l.strip() == h)
        if idx < last:
            fails.append(f"heading '{h}' is out of order")
        last = idx
        if not any(l.strip() for l in sections[h]):
            fails.append(f"section '{h}' is empty")
    if fails:
        return fails

    classes = split_pieces(sections[HEADINGS[2]])
    approaches = split_pieces(sections[HEADINGS[3]])
    if not classes:
        fails.append("section 3 has no '### Piece <id>: <name>' entries")
    if set(classes) != set(approaches):
        fails.append(
            "pieces in section 3 and section 4 differ: "
            f"{sorted(set(classes) ^ set(approaches))}"
        )

    domains = {}
    for pid, body in classes.items():
        block = "\n".join(body)
        for label in CLASS_LABELS:
            if f"**{label}:**" not in block:
                fails.append(f"piece {pid}: section 3 missing '{label}'")
        m = re.search(r"\*\*Primary domain:\*\*\s*(\w+)", block)
        if not m or m.group(1) not in DOMAINS:
            fails.append(f"piece {pid}: Primary domain must be one of {', '.join(DOMAINS)}")
            continue
        domains[pid] = m.group(1)
        if len(re.findall(r"^\s{2,}- \S", block, re.M)) < 1:
            fails.append(f"piece {pid}: Evidence has no items")
        sr = re.search(r"\*\*Second reading:\*\*\s*(\w+)", block)
        if sr and sr.group(1) == m.group(1):
            fails.append(f"piece {pid}: Second reading repeats the primary domain")

    for pid, body in approaches.items():
        domain = domains.get(pid)
        block = "\n".join(body)
        if domain is None:
            continue
        for label in REQUIRED.get(domain, ()):
            if f"**{label}:**" not in block:
                fails.append(f"piece {pid}: {domain} approach missing '{label}'")
        if domain == "Complex":
            n = len(re.findall(r"^- \*\*Probe \d+:\*\*", block, re.M))
            if n < 1 or n > MAX_PROBES:
                fails.append(f"piece {pid}: Complex needs 1-{MAX_PROBES} probes, found {n}")
            for needle in PROBE_LINES:
                if block.count(needle) < n:
                    fails.append(f"piece {pid}: every probe needs '{needle}'")
        if domain == "Chaotic" and len(re.findall(r"\*\*Stabilising action:\*\*", block)) != 1:
            fails.append(f"piece {pid}: Chaotic needs exactly one stabilising action")

    if not re.search(r"^- ", "\n".join(sections[HEADINGS[4]]), re.M):
        fails.append("section 5 has no bullet items")
    return fails


def main(argv):
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    try:
        with open(argv[1], encoding="utf-8") as fh:
            text = fh.read()
    except OSError as exc:
        print(f"cannot read {argv[1]}: {exc}", file=sys.stderr)
        return 2
    fails = lint(text)
    for line in fails:
        print(f"FAIL {line}")
    print("PASS" if not fails else f"FAIL ({len(fails)} problem(s))")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
