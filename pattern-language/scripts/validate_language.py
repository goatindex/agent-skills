#!/usr/bin/env python3
"""Validate a pattern language for structural integrity.

Two delivery shapes are accepted (see references/language-structure.md):

  * a FOLDER of one-file-per-pattern (NNN-name.md) plus index.md — the
    machine-checkable default; links live in typed frontmatter.
  * a single .md DOC carrying the whole language with an embedded
    ```mermaid graph TD``` block — the wiki-hosted shape; the Mermaid block
    is the canonical link source and headers carry identity/scale/confidence.

Standard library only — no third-party imports (portable floor).
Full check descriptions and severities: references/validation.md

Usage: python3 validate_language.py <language-folder | language-doc.md>
Exit: 0 = pass (warnings allowed), 1 = one or more FAILs, 2 = usage/IO error.
"""

import os
import re
import sys

REQUIRED_KEYS = ("number", "name", "confidence", "scale", "links_up", "links_down")
OPTIONAL_KEYS = frozenset({"status", "date", "sympathies", "tensions"})
LINK_KEYS = ("links_up", "links_down", "sympathies", "tensions")
LATERAL_KEYS = ("sympathies", "tensions")
AST = {0: "", 1: "✻", 2: "✻✻"}  # ✻
STARS = "✻★"  # ✻ or ★ — both accepted when reading a single-doc header

# Matches a pattern list-item line in index.md: optional whitespace, digit(s), period, space, link
INDEX_LIST_RE = re.compile(r"^\s*\d+\.\s+\[")


def parse_frontmatter(text, fails, warns, fname):
    """Parse the constrained YAML frontmatter block."""
    m = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        fails.append(f"{fname}: no frontmatter block")
        return None
    fm = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            fails.append(f"{fname}: unparseable frontmatter line: {line!r}")
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.split("#", 1)[0].strip()  # strip inline comments
        if key in LINK_KEYS:
            lm = re.match(r"\[(.*)\]$", val)
            if lm is None:
                fails.append(f"{fname}: {key} must be a list like [1, 2] or []")
                fm[key] = []
                continue
            items = [s.strip() for s in lm.group(1).split(",") if s.strip()]
            try:
                fm[key] = [int(s) for s in items]
            except ValueError:
                fails.append(f"{fname}: {key} contains a non-integer")
                fm[key] = []
        elif key in ("number", "confidence"):
            try:
                fm[key] = int(val)
            except ValueError:
                fails.append(f"{fname}: {key} must be an integer, got {val!r}")
        else:
            fm[key] = val.strip("'\"")

    # Lateral links are optional — default to empty so downstream code is uniform.
    for key in LATERAL_KEYS:
        fm.setdefault(key, [])

    # Warn on unrecognised keys — likely typos (e.g. links_dow:)
    known = set(REQUIRED_KEYS) | OPTIONAL_KEYS
    for k in fm:
        if k not in known:
            warns.append(f"{fname}: unrecognised frontmatter key {k!r} (typo?)")

    missing = [k for k in REQUIRED_KEYS if k not in fm]
    if missing:
        fails.append(f"{fname}: missing frontmatter keys: {', '.join(missing)}")
        return None

    # Check name does not contain '#' (breaks inline-comment stripping)
    if "#" in fm.get("name", ""):
        fails.append(f"{fname}: pattern name must not contain '#': {fm['name']!r}")

    return fm


def first_bold(section_text):
    """True if the first non-empty line starts a **bold** statement."""
    for line in section_text.splitlines():
        line = line.strip()
        if not line:
            continue
        return line.startswith("**")
    return False


def section(body, heading):
    """Return body text of '## <heading>' (with optional colon), or None."""
    m = re.search(
        rf"^##\s+{re.escape(heading)}:?\s*$(.*?)(?=^##\s|\Z)",
        body, re.S | re.M
    )
    return m.group(1) if m else None


def prose_mentions(text, target_num, target_fname):
    """True if text mentions target via filename or anchored link-number '(N)'."""
    if target_fname in text:
        return True
    return bool(re.search(rf"\({target_num}\)", text))


def check_lateral(patterns, fails, warns, reciprocal):
    """Shared sympathy/tension checks for both delivery shapes.

    `patterns` maps number -> dict carrying a `label` (fname or '#N name'),
    and `sympathies` / `tensions` as iterables of pattern numbers. When
    `reciprocal` is True (folder shape, where each side declares its own list)
    a one-sided relation is a WARN; in single-doc shape the Mermaid edges are
    undirected, so reciprocity is structural and the check is skipped.
    """
    seen = set()
    for n, p in sorted(patterns.items()):
        label = p["label"]
        for kind in LATERAL_KEYS:
            for t in p.get(kind, []):
                if t == n:
                    fails.append(f"{label}: {kind} links to itself ({t})")
                elif t not in patterns:
                    fails.append(f"{label}: {kind} target {t} does not exist")
                elif reciprocal:
                    a, b = sorted((n, t))
                    pair = (kind, a, b)
                    if pair in seen:
                        continue
                    if t not in patterns[n].get(kind, []) or n not in patterns[t].get(kind, []):
                        seen.add(pair)
                        warns.append(
                            f"{label}: {kind} with {patterns[t]['label']} is one-sided "
                            f"(both patterns must list each other)"
                        )


# --------------------------------------------------------------------------- #
# Folder shape — file-per-pattern + index.md                                   #
# --------------------------------------------------------------------------- #

def validate_folder(folder):
    fails, warns = [], []
    patterns = {}   # number -> {fm, fname, body}

    # Accept 3+ digit prefixes so languages beyond 999 patterns are supported
    files = sorted(f for f in os.listdir(folder)
                   if re.match(r"\d{3,}-.*\.md$", f))
    if not files:
        print(f"FAIL: no pattern files (NNN-name.md) found in {folder}")
        return 1

    for fname in files:
        with open(os.path.join(folder, fname), encoding="utf-8-sig") as fh:
            text = fh.read()
        fm = parse_frontmatter(text, fails, warns, fname)
        if fm is None:
            continue
        body = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", text, flags=re.S)
        n = fm["number"]
        prefix = int(re.match(r"(\d+)-", fname).group(1))
        if prefix != n:
            fails.append(f"{fname}: filename prefix {prefix} != number {n}")
        if n in patterns:
            fails.append(f"{fname}: duplicate number {n} (also {patterns[n]['fname']})")
            continue
        if fm["confidence"] not in (0, 1, 2):
            fails.append(f"{fname}: confidence {fm['confidence']} not in 0|1|2")

        # header line: # N. Name [asterisks]
        hm = re.search(r"^#\s+(\d+)\.\s+(.+?)\s*$", body, re.M)
        if not hm:
            fails.append(f"{fname}: missing '# N. Name' header line")
        else:
            hnum = int(hm.group(1))
            rest = hm.group(2)
            expected_ast = AST.get(fm["confidence"], "")
            hname = rest.rstrip("✻ ").strip()
            if hnum != n:
                fails.append(f"{fname}: header number {hnum} != frontmatter {n}")
            if hname != fm["name"]:
                fails.append(f"{fname}: header name {hname!r} != frontmatter {fm['name']!r}")
            got_ast = rest[len(hname):].replace(" ", "")
            if got_ast != expected_ast:
                fails.append(
                    f"{fname}: header asterisks {got_ast!r} != expected "
                    f"{expected_ast!r} for confidence {fm['confidence']}"
                )

        # required sections — tolerate optional colon in heading
        for heading in ("Problem", "Therefore"):
            sec = section(body, heading)
            if sec is None:
                found = re.findall(r"^##\s+.+", body, re.M)
                hint = f" (found: {found})" if found else ""
                fails.append(f"{fname}: missing '## {heading}' section{hint}")
            elif not first_bold(sec):
                fails.append(
                    f"{fname}: '## {heading}' first non-empty line must be **bolded**"
                )

        patterns[n] = {"fm": fm, "fname": fname, "body": body}

    nums = set(patterns)
    for n, p in sorted(patterns.items()):
        fm, fname, body = p["fm"], p["fname"], p["body"]

        for key, direction in (("links_up", -1), ("links_down", 1)):
            for t in fm[key]:
                if t == n:
                    fails.append(f"{fname}: {key} links to itself ({t})")
                elif t not in nums:
                    fails.append(f"{fname}: {key} target {t} does not exist")
                elif direction == -1 and t > n:
                    warns.append(f"{fname}: links_up to higher number {t} (scale-order)")
                elif direction == 1 and t < n:
                    warns.append(f"{fname}: links_down to lower number {t} (scale-order)")

        if not fm["links_up"] and not fm["links_down"]:
            warns.append(f"{fname}: orphan — no links in either direction")

        # Reciprocity — emit only from the lower-numbered pattern to avoid duplicate WARNs
        for t in fm["links_down"]:
            if t in nums and t > n and n not in patterns[t]["fm"]["links_up"]:
                warns.append(
                    f"{fname}: links_down to {patterns[t]['fname']}, "
                    f"but that pattern does not link_up back"
                )
        for t in fm["links_up"]:
            if t in nums and t > n and n not in patterns[t]["fm"]["links_down"]:
                warns.append(
                    f"{fname}: links_up to {patterns[t]['fname']}, "
                    f"but that pattern does not link_down back"
                )

        # Prose-mention checks — use the same regex as section() for the context split
        context_parts = re.split(r"^## Problem:?\s*$", body, maxsplit=1, flags=re.M)
        context = context_parts[0] if len(context_parts) > 1 else ""
        linksec = section(body, "Links down") or ""
        for t in fm["links_up"]:
            if t in nums and not prose_mentions(context, t, patterns[t]["fname"]):
                warns.append(
                    f"{fname}: links_up target {t} not mentioned in context prose"
                )
        for t in fm["links_down"]:
            if t in nums and not prose_mentions(linksec, t, patterns[t]["fname"]):
                warns.append(
                    f"{fname}: links_down target {t} not mentioned in 'Links down' prose"
                )

    # Lateral links (sympathies / tensions) — declared per file, so reciprocal.
    lateral = {
        n: {"label": p["fname"],
            "sympathies": p["fm"].get("sympathies", []),
            "tensions": p["fm"].get("tensions", [])}
        for n, p in patterns.items()
    }
    check_lateral(lateral, fails, warns, reciprocal=True)

    # index.md — count only list-item lines, not prose cross-links
    idx_path = os.path.join(folder, "index.md")
    if not os.path.isfile(idx_path):
        fails.append("index.md missing")
    else:
        with open(idx_path, encoding="utf-8-sig") as fh:
            idx_lines = fh.readlines()
        idx_text = "".join(idx_lines)

        for n, p in sorted(patterns.items()):
            count = sum(
                1 for line in idx_lines
                if INDEX_LIST_RE.match(line)
                and re.search(rf"\({re.escape(p['fname'])}\)", line)
            )
            if count == 0:
                fails.append(
                    f"index.md: pattern {n} ({p['fname']}) not in any list item"
                )
            elif count > 1:
                fails.append(
                    f"index.md: pattern {n} ({p['fname']}) appears in {count} list items (expected 1)"
                )

        headings = set(re.findall(r"^##\s+(.+?)\s*$", idx_text, re.M))
        scales = {p["fm"]["scale"] for p in patterns.values()}
        for s in sorted(scales - headings):
            warns.append(
                f"index.md: scale {s!r} used in frontmatter but no matching '## {s}' heading"
            )

    return report(patterns, fails, warns, rung="folder")


# --------------------------------------------------------------------------- #
# Single-doc shape — one .md with an embedded mermaid graph                    #
# --------------------------------------------------------------------------- #

def parse_mermaid(block):
    """Parse a `graph TD` block into typed relations keyed by pattern number.

    Edge conventions (see references/language-structure.md):
      A --> B     links_down  (directed, larger scale to smaller)
      A -.- B     sympathy    (undirected; cross-scale reinforcement)
      A x--x B    tension     (undirected; forces in conflict)

    Node numbers are read from the first integer inside a node label,
    e.g. `P12[12 CARDS THAT TRAVEL]` -> 12.
    Returns (down, symp, tension): down is a set of (a, b) tuples; the two
    lateral relations are sets of frozenset({a, b}) pairs.
    """
    nodemap = {}  # node-id -> number
    for nm in re.finditer(r'(\w+)\s*\[\s*"?\s*(\d+)', block):
        nodemap[nm.group(1)] = int(nm.group(2))

    def num(token):
        token = token.strip()
        lm = re.match(r'(\w+)\s*\[\s*"?\s*(\d+)', token)
        if lm:
            nodemap[lm.group(1)] = int(lm.group(2))
            return int(lm.group(2))
        return nodemap.get(token)

    node = r'(\w+(?:\s*\[[^\]]*\])?)'
    re_tension = re.compile(node + r'\s*x-+\.?-*x\s*' + node)
    re_symp = re.compile(node + r'\s*-\.+-(?!>)\s*' + node)
    re_down = re.compile(node + r'\s*--+>\s*' + node)

    down, symp, tension = set(), set(), set()
    for raw in block.splitlines():
        line = raw.strip()
        if not line or line.startswith("%%"):
            continue
        for rx, bucket, undirected in (
            (re_tension, tension, True),
            (re_symp, symp, True),
            (re_down, down, False),
        ):
            m = rx.search(line)
            if not m:
                continue
            a, b = num(m.group(1)), num(m.group(2))
            if a is None or b is None:
                continue
            bucket.add(frozenset((a, b)) if undirected else (a, b))
            break
    return down, symp, tension


def validate_single_doc(path):
    fails, warns = [], []
    with open(path, encoding="utf-8-sig") as fh:
        text = fh.read()
    docname = os.path.basename(path)

    # Split the doc into pattern sections on '## N. Name' headers. A top-level
    # '# ...' heading that is not a pattern is treated as a scale band.
    headers = list(re.finditer(r"^(#{1,2})\s+(.+?)\s*$", text, re.M))
    patterns = {}      # number -> dict
    order = []         # numbers in document order
    current_scale = "(unscaled)"

    pat_re = re.compile(r"^(\d+)\.\s+(.*)$")
    for i, h in enumerate(headers):
        level, title = h.group(1), h.group(2).strip()
        pm = pat_re.match(title)
        if level == "#" and not pm:
            # Scale band heading (skip the doc title — heuristically the first one).
            current_scale = title
            continue
        if not pm:
            continue  # a '##' prose section (How to use, Appendix, …)
        number = int(pm.group(1))
        rest = pm.group(2)
        confidence = sum(rest.count(c) for c in STARS)
        confidence = min(confidence, 2)
        name = re.sub(r"\([^)]*\)", "", rest)            # drop parentheticals
        name = "".join(ch for ch in name if ch not in STARS).strip()
        start = h.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        sec = text[start:end]

        if number in patterns:
            fails.append(f"#{number} {name!r}: duplicate pattern number "
                         f"(also {patterns[number]['name']!r})")
            continue
        patterns[number] = {
            "label": f"#{number} {name}", "name": name,
            "confidence": confidence, "scale": current_scale, "section": sec,
            "links_down": set(), "links_up": set(),
            "sympathies": set(), "tensions": set(),
        }
        order.append(number)

    if not patterns:
        print(f"FAIL: no patterns ('## N. Name') found in {docname}")
        return 1

    # Problem / Therefore presence — single-doc form inlines both as bold prose.
    for n, p in patterns.items():
        sec = p["section"]
        ther = re.search(r"[Tt]herefore\b[:,]?\s*\**", sec)
        before = sec[:ther.start()] if ther else sec
        if not re.search(r"\*\*.+?\*\*", before, re.S):
            fails.append(f"{p['label']}: no bolded problem statement before the Therefore")
        if not ther or not re.search(r"[Tt]herefore\b[:,]?\s*\n?\s*\*\*", sec):
            fails.append(f"{p['label']}: no bolded 'Therefore:' instruction")

    # Links from the canonical Mermaid block.
    mblock = re.search(r"```mermaid(.*?)```", text, re.S)
    if not mblock:
        warns.append(f"{docname}: no ```mermaid``` block — link network unchecked")
    else:
        down, symp, tension = parse_mermaid(mblock.group(1))
        graph_nums = set()
        for a, b in down:
            graph_nums.update((a, b))
            for end in (a, b):
                if end not in patterns:
                    fails.append(f"mermaid: edge references unknown pattern {end}")
            if a in patterns and b in patterns:
                patterns[a]["links_down"].add(b)
                patterns[b]["links_up"].add(a)
                if b < a:
                    warns.append(f"mermaid: {a} --> {b} runs against scale order "
                                 f"(lower number should be the larger scale)")
        for kind, pairs in (("sympathies", symp), ("tensions", tension)):
            for pair in pairs:
                ends = tuple(pair)
                for end in ends:
                    if end not in patterns:
                        fails.append(f"mermaid: {kind} edge references unknown pattern {end}")
                    else:
                        graph_nums.add(end)
                if all(e in patterns for e in ends):
                    a, b = ends if len(ends) == 2 else (ends[0], ends[0])
                    patterns[a][kind].add(b)
                    patterns[b][kind].add(a)
        for n in order:
            if n not in graph_nums:
                warns.append(f"#{n} {patterns[n]['name']}: not present in the mermaid "
                             f"graph (orphan, or missing edge)")

    # Lateral edges are undirected here, so reciprocity is structural.
    check_lateral(patterns, fails, warns, reciprocal=False)

    return report(patterns, fails, warns, rung="single-doc")


# --------------------------------------------------------------------------- #

def report(patterns, fails, warns, rung):
    for w in warns:
        print(f"WARN  {w}")
    for f in fails:
        print(f"FAIL  {f}")
    total = len(patterns)
    status = "PASS" if not fails else "FAIL"
    print(f"\n{total} pattern{'s' if total != 1 else ''} checked ({rung} shape): "
          f"{status} ({len(fails)} fail{'s' if len(fails)!=1 else ''}, "
          f"{len(warns)} warn{'s' if len(warns)!=1 else ''})")
    return 1 if fails else 0


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    target = sys.argv[1]
    if os.path.isdir(target):
        return validate_folder(target)
    if os.path.isfile(target) and target.endswith(".md"):
        return validate_single_doc(target)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
