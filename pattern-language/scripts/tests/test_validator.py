#!/usr/bin/env python3
"""Regression tests for validate_language.py. Standard library only.

Run: python3 scripts/tests/test_validator.py
Exit: 0 = all tests pass, 1 = failures.

The clean fixture is the shipped worked example (examples/garden-crew), so
the example and the validator are tested against each other. Failure-mode
fixtures are generated in a temp dir per test.
"""

import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(os.path.dirname(HERE))
VALIDATOR = os.path.join(SKILL, "scripts", "validate_language.py")
EXAMPLE = os.path.join(SKILL, "examples", "garden-crew")

PATTERN = """---
number: {number}
name: {name}
confidence: {confidence}
scale: {scale}
links_up: {links_up}
links_down: {links_down}
---

# {number}. {name}{stars}

...context: helps complete {up_prose}...

## Problem

**Force A pulls against force B.**

## Therefore

**Do the thing.**
{extra}
## Links down

...completed by {down_prose}...
"""

def write_pattern(folder, number, name, confidence=0, scale="Large",
                  links_up=(), links_down=(), extra="", files=None):
    stars = {0: "", 1: " ✻", 2: " ✻✻"}[confidence]
    kebab = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    fname = f"{number:03d}-{kebab}.md"
    files = files or {}
    up_prose = ", ".join(f"[{files.get(t, t)} ({t})]({files.get(t, t)})"
                         for t in links_up) or "the language"
    down_prose = ", ".join(f"[{files.get(t, t)} ({t})]({files.get(t, t)})"
                           for t in links_down) or "nothing"
    body = PATTERN.format(number=number, name=name, confidence=confidence,
                          scale=scale, links_up=list(links_up),
                          links_down=list(links_down), stars=stars,
                          up_prose=up_prose, down_prose=down_prose,
                          extra=extra)
    with open(os.path.join(folder, fname), "w", encoding="utf-8") as fh:
        fh.write(body)
    return fname

def write_index(folder, entries):
    lines = ["# Test Language\n", "Purpose line.\n"]
    scales = {}
    for number, name, fname, scale, conf in entries:
        scales.setdefault(scale, []).append((number, name, fname, conf))
    for scale, pats in scales.items():
        lines.append(f"\n## {scale}\n\nBlurb.\n")
        for number, name, fname, conf in pats:
            stars = {0: "", 1: " ✻", 2: " ✻✻"}[conf]
            lines.append(f"{number}. [{name}]({fname}){stars}")
    with open(os.path.join(folder, "index.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

def write_pathfinder(folder, drop=None):
    heads = ["Purpose & audience", "Scope", "The gradient",
             "Landscape & key references", "Evidence & provenance"]
    text = "# Pathfinder\n\n" + "\n".join(
        f"## {h}\n\nContent.\n" for h in heads if h != drop)
    with open(os.path.join(folder, "PATHFINDER.md"), "w", encoding="utf-8") as fh:
        fh.write(text)

def run(target, *flags):
    proc = subprocess.run([sys.executable, VALIDATOR, *flags, target],
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace")
    return proc.returncode, proc.stdout

FAILURES = []

def check(label, cond, detail=""):
    status = "ok" if cond else "FAIL"
    print(f"  {status:4} {label}")
    if not cond:
        FAILURES.append(f"{label} {detail}")

def test_clean_example():
    print("clean worked example")
    code, out = run(EXAMPLE)
    check("exit 0", code == 0, out)
    check("0 fails, 0 warns", "(0 fails, 0 warns)" in out, out)
    check("100% reciprocal", "100% reciprocal" in out, out)

def test_up_asserted_one_way_edge_warns():
    # Regression: pre-v0.6 a `t > n` guard silently passed edges asserted
    # only via links_up (558 of APL's 1758 edges).
    print("up-asserted one-way edge warns")
    with tempfile.TemporaryDirectory() as d:
        f1 = write_pattern(d, 1, "Big", scale="Large")
        f2 = write_pattern(d, 20, "Small", scale="Small", links_up=[1],
                           files={1: f1})
        write_index(d, [(1, "Big", f1, "Large", 0), (20, "Small", f2, "Small", 0)])
        write_pathfinder(d)
        code, out = run(d)
        check("reciprocity warn fires", "does not link_down back" in out, out)
        check("still PASS (warn not fail)", code == 0, out)

def test_known_uses_case_insensitive():
    # Regression: '## Known Uses' (Title Case) must satisfy the check.
    print("known-uses check is case-insensitive")
    with tempfile.TemporaryDirectory() as d:
        extra = "\n## Known Uses\n\n- One.\n- Two.\n- Three.\n"
        f1 = write_pattern(d, 1, "Big", confidence=2, extra=extra)
        write_index(d, [(1, "Big", f1, "Large", 2)])
        write_pathfinder(d)
        _, out = run(d)
        check("no known-uses warn", "Known uses" not in out, out)

def test_starred_without_known_uses_warns():
    print("confidence 2 without known uses warns")
    with tempfile.TemporaryDirectory() as d:
        f1 = write_pattern(d, 1, "Big", confidence=2)
        write_index(d, [(1, "Big", f1, "Large", 2)])
        write_pathfinder(d)
        _, out = run(d)
        check("warn fires", "no '## Known uses' section" in out, out)

def test_vague_known_uses_warns():
    # Regression from baseline run 4 (Sonnet x Shadowrun): five patterns
    # promoted to starred confidence on genre convention. Vague-plural known
    # uses on a starred pattern must WARN; specific instances must not.
    print("vague known-uses on starred pattern warns; instances don't")
    vague = ("\n## Known uses\n\n- Recurring convention across genre fiction "
             "and actual play shows.\n")
    specific = ("\n## Known uses\n\n- The 2024 restructure group kept the "
                "trail; the merger held.\n")
    with tempfile.TemporaryDirectory() as d:
        f1 = write_pattern(d, 1, "Big", confidence=1, extra=vague)
        write_index(d, [(1, "Big", f1, "Large", 1)])
        write_pathfinder(d)
        _, out = run(d)
        check("vague warn fires", "read like" in out, out)
    with tempfile.TemporaryDirectory() as d:
        f1 = write_pattern(d, 1, "Big", confidence=1, extra=specific)
        write_index(d, [(1, "Big", f1, "Large", 1)])
        write_pathfinder(d)
        _, out = run(d)
        check("specific instance passes", "read like" not in out, out)

def test_pathfinder_checks():
    print("pathfinder presence and headings")
    with tempfile.TemporaryDirectory() as d:
        f1 = write_pattern(d, 1, "Big")
        write_index(d, [(1, "Big", f1, "Large", 0)])
        _, out = run(d)
        check("missing file warns", "PATHFINDER.md missing" in out, out)
        write_pathfinder(d, drop="Scope")
        _, out = run(d)
        check("missing heading warns", "missing core heading '## Scope'" in out, out)

def test_sequences():
    print("sequence link and order checks")
    with tempfile.TemporaryDirectory() as d:
        f1 = write_pattern(d, 1, "Big", links_down=[20])
        f2 = write_pattern(d, 20, "Small", scale="Small", links_up=[1],
                           files={1: f1})
        # fix reciprocity so only sequence findings appear
        write_index(d, [(1, "Big", f1, "Large", 0), (20, "Small", f2, "Small", 0)])
        write_pathfinder(d)
        os.makedirs(os.path.join(d, "sequences"))
        with open(os.path.join(d, "sequences", "bad.md"), "w",
                  encoding="utf-8") as fh:
            fh.write(f"# Bad\n\n1. [Small](../{f2}) - first\n"
                     f"2. [Big](../{f1}) - order warn\n"
                     f"3. [Ghost](../099-ghost.md) - broken FAIL\n")
        code, out = run(d)
        check("broken link FAILs", code == 1 and "which does not exist" in out, out)
        check("order warn fires", "against the gradient" in out, out)

def test_grouped_reporting_cap():
    print("warn grouping and cap")
    with tempfile.TemporaryDirectory() as d:
        entries = []
        f_first = write_pattern(d, 1, "Pat1", scale="Large")
        entries.append((1, "Pat1", f_first, "Large", 0))
        for i in range(2, 16):  # 14 one-way up-links -> 14 reciprocity warns
            fn = write_pattern(d, i, f"Pat{i}", scale="Large", links_up=[1],
                               files={1: f_first})
            entries.append((i, f"Pat{i}", fn, "Large", 0))
        write_index(d, entries)
        write_pathfinder(d)
        _, out = run(d)
        check("category header with count", re.search(r"WARN\s+reciprocity: 14", out), out)
        check("capped at 10 with more-line", "4 more (--verbose lists all)" in out, out)
        _, out = run(d, "--verbose")
        check("--verbose lifts cap", "more (--verbose lists all)" not in out, out)

def test_single_doc():
    print("single-doc shape")
    doc = """# Tiny

## Pathfinder

Purpose, scope, gradient, landscape, evidence.

# LARGE

## 1. Big ✻

**A pulls against B.** Therefore: **do the thing.**

```mermaid
graph TD
  P1["1. Big"] --> P2["2. Small"]
```

## 2. Small

**C pulls against D.** Therefore: **do the small thing.**
"""
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "tiny.md")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(doc)
        code, out = run(p)
        check("passes clean", code == 0 and "(0 fails, 0 warns)" in out, out)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(doc.replace("## Pathfinder", "## Preamble"))
        _, out = run(p)
        check("missing pathfinder section warns", "no '## Pathfinder' section" in out, out)

def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
    print(f"\n{len(tests)} test groups; {len(FAILURES)} failing checks")
    if FAILURES:
        for f in FAILURES:
            print(f"FAIL: {f[:300]}")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
