# Language structure — the network, the folder, the index

A pattern language is more than its patterns: the **ordering is itself content**. Alexander: the sequence of patterns is both a summary of the language and an index to it.

## Two delivery shapes

A language can be delivered in either of two shapes; both are first-class and both are validatable (`scripts/validate_language.py` auto-detects which from the path).

- **Folder** — one file per pattern plus `index.md` (below). Links live in typed frontmatter, so every structural check runs at full strength. Choose this for larger languages (roughly 25+ patterns), languages that will be grown and machine-checked over time, or Obsidian/apl-md workflows. **This is the default.**
- **Single network-doc** — the whole language in one `.md` file with an embedded `mermaid graph TD` block, a generative sequence, and appendices. Choose this for small-to-medium languages hosted on a wiki (GitHub/Obsidian wiki page), where one readable page beats a folder of files. In this shape **the Mermaid block is the canonical link source** — see "Graph view" below for the edge grammar — and pattern identity/scale/confidence are read from `## N. Name ✻` headers and `# SCALE …` band headers. Problem and Therefore are inlined as bold prose rather than `##` subheadings.

Pick by host and size, not by decree. Do not hand-maintain both shapes for the same language; if you need both views, keep one canonical and generate the other. When unsure, default to the folder — it loses no checks.

```
<language-name>/
  index.md                      # the ordered sequence — canonical
  001-<name>.md                 # one file per pattern
  002-<name>.md
  …
  README.md                     # optional: provenance, audience, how to use
```

No subfolders for patterns — scale grouping lives in `index.md` and in each pattern's `scale:` key, not in the directory tree. This keeps relative links between patterns trivial and the folder portable.

## Scale ordering

Patterns run from the **largest scale to the smallest**. In APL that was towns → buildings → construction. In any other domain, identify the equivalent gradient first; examples:

- Organising: federation → branch → committee → meeting → conversation
- Game campaign: setting → arc → session → scene → mechanic
- Software process: organisation → team → release → change → commit

Number patterns so that scale bands occupy contiguous ranges, and **leave gaps between bands** (e.g. band one starts at 1, band two at 20, band three at 40) so the language can grow without renumbering. Gaps in numbering are normal and healthy; duplicate numbers are fatal.

## index.md format

The index is structured prose, not a bare list. It declares the scale groups (which the validator cross-checks against each pattern's `scale:`), and each group carries one or two sentences of connective instruction — *what the reader is doing at this scale* — in the spirit of APL's "within each region, work toward…".

```markdown
# <Language Name>

One-paragraph statement of what this language is for and who uses it.

## <Scale Group A>

What you are doing at this scale, as an instruction.

1. [Pattern Name](001-pattern-name.md) ✻✻
2. [Other Pattern](002-other-pattern.md)

## <Scale Group B>

…
```

Every pattern file appears in exactly one list-item line (`N. [Name](file.md)`) in the index, in number order, with its confidence asterisks shown. Prose cross-links within group blurbs are fine and don't count. The group heading text must match the `scale:` values used in frontmatter.

## Sequences

A reader never uses the whole language at once: they pick a **sequence** — a path through the network for one project, choosing the patterns that apply and compressing them into a single design. When a user asks "apply this language to X", the deliverable is a sequence: an ordered subset (largest scale first) with one line each on how the pattern lands in X. Sequences are documents *about* a language; store them outside the language folder or in a `sequences/` sibling.

## Restructuring operations

- **Insert a scale band**: choose a free number range; update `index.md`; new patterns link up into the band above and down into the band below; adjacent patterns gain reciprocal links.
- **Split a pattern**: when one pattern's Therefore contains two instructions, it is two patterns. The original keeps its number and the narrower solution; the new one takes a nearby free number; both inherit and then prune the original's links.
- **Merge**: when two patterns resolve the same tension, keep the better-named one, fold evidence in, retire the other — leave a one-line tombstone file pointing to the survivor if anything external might link to it, otherwise delete and fix inbound links.
- **Renumbering** is a last resort; it breaks external references. Prefer gap allocation. If unavoidable, do it in one commit-like pass and re-run validation.

## Graph view

In the folder shape, build the graph from frontmatter; in the single-doc shape, the graph **is** the link source and everything else is read back from it. Mermaid (plain text, no binary):

```mermaid
graph TD
  subgraph "Scale Group A"
    P1["1. Pattern Name ✻✻"]
    P2["2. Other Pattern"]
  end
  subgraph "Scale Group B"
    P20["20. Smaller Pattern ✻"]
  end
  P1 --> P20          %% hierarchy: links_down (larger scale to smaller)
  P2 --> P20
  P1 -.- P2           %% sympathy: undirected, patterns that reinforce
  P2 x--x P20         %% tension: undirected, forces in conflict
```

**Edge grammar** (the validator parses exactly these in single-doc mode):
- `A --> B` — hierarchy, `links_down` only (drawing both directions doubles every edge);
- `A -.- B` — a **sympathy** (dotted, undirected);
- `A x--x B` — a **tension** (cross-heads, undirected).

Give each node an `[N …]` label so its pattern number is machine-readable. Sympathies and tensions are optional — omit them until they are real. If the user wants an image and Graphviz is *confirmed* available, the same data can be emitted as DOT and rendered — an enhancement, never a dependency.
