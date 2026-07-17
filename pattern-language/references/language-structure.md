# Language structure — the network, the folder, the index

A pattern language is more than its patterns: the **ordering is itself content**. Alexander: the sequence of patterns is both a summary of the language and an index to it.

## Two delivery shapes

A language can be delivered in either of two shapes; both are first-class and both are validatable (`scripts/validate_language.py` auto-detects which from the path).

- **Folder** — one file per pattern plus `index.md` (below). Links live in typed frontmatter, so every structural check runs at full strength, and sessions can load only the patterns they need (see SKILL.md § Context discipline). Right at any size — a 5-pattern seed or a 250-pattern corpus. **This is the default.**
- **Single network-doc** — the whole language in one `.md` file with an embedded `mermaid graph TD` block, a generative sequence, and appendices. Choose this for small-to-medium languages hosted on a wiki (GitHub/Obsidian wiki page), where one readable page beats a folder of files. In this shape **the Mermaid block is the canonical link source** — see "Graph view" below for the edge grammar — and pattern identity/scale/confidence are read from `## N. Name ✻` headers and `# SCALE …` band headers. Problem and Therefore are inlined as bold prose rather than `##` subheadings.

Pick by host and size, not by decree. Do not hand-maintain both shapes for the same language; if you need both views, keep one canonical and generate the other. When unsure, default to the folder — it loses no checks.

```
<language-name>/
  PATHFINDER.md                 # the language's self-description — see references/pathfinder.md
  index.md                      # the ordered sequence — canonical
  001-<name>.md                 # one file per pattern
  002-<name>.md
  …
  sequences/                    # optional: named sequences through the language
    <sequence-name>.md
```

No subfolders for patterns — scale grouping lives in `index.md` and in each pattern's `scale:` key, not in the directory tree. This keeps relative links between patterns trivial and the folder portable. (`PATHFINDER.md` supersedes the old optional `README.md`; upgrade an existing README in place.)

## The gradient

Patterns run from the **largest to the smallest** — but "large" and "small" need not mean physical size. The requirement is a **monotone design gradient**: one consistent axis of descent that the designer walks from whole toward part. Valid axes include:

- Spatial/structural scale (APL: towns → buildings → construction)
- Organisational scope (software process: organisation → team → release → change → commit)
- Process/time order (facilitation: intention → context → relationship → flow → closing)
- Campaign structure (game design: setting → arc → session → scene → mechanic)

What matters is that the axis is *declared* (in `PATHFINDER.md` § The gradient) and *consistent* — every band sits unambiguously before or after every other band on the named axis, and a reader entering at the top descends. Thematic **categories with no ordering rationale are not a gradient** (that is the smell qualitative check 6 looks for); ordered categories along a declared axis are fine, as Group Works' event-design ordering shows.

Number patterns so that bands occupy contiguous ranges, and **leave gaps between bands** (e.g. band one starts at 1, band two at 20, band three at 40) so the language can grow without renumbering. Gaps in numbering are normal and healthy; duplicate numbers are fatal.

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

**Clusters (optional, for larger languages).** Within a `## Scale Group`, patterns may be gathered into `### Cluster` sub-headings of roughly 4–10 patterns, each with its own one-sentence connective instruction. This is APL's own index structure — three tiers containing ~36 thematic clusters, each introduced by an imperative ("Within each region work toward…") — and it is where the language's generative voice lives at scale. The validator ignores `###` headings (only `##` headings must match `scale:` values), so clusters are free to add when a group grows past ten patterns.

## Sequences

A reader never uses the whole language at once: they pick a **sequence** — a path through the network for one project, choosing the patterns that apply and compressing them into a single design. When a user asks "apply this language to X", the deliverable is a sequence.

A sequence is **not a bare ordered list**. The strongest published exemplars (e.g. scrumbook.org's *A Scaling Sequence*) carry four elements, and so does ours:

1. **Purpose line** — what walking this sequence produces, for whom.
2. **Entry conditions** — what must already be true before step one ("the starting point is always a single working X"); a sequence entered too early produces cargo cult, not design.
3. **The ordered steps** — largest scale first, each a list item `N. [Pattern Name](../NNN-file.md) — one line on how the pattern lands in this context`, with connective narrative between steps where the hand-off needs explaining.
4. **Cautions** — the known failure modes of running the sequence wrong (skipping a step, entering mid-way, scaling a dysfunction).

Named, reusable sequences are **first-class members of the language**: store them in `sequences/<name>.md` inside the language folder and list them in `PATHFINDER.md` § Sequences. The validator checks that every pattern a sequence links to exists (FAIL) and that steps run down the gradient (WARN). One-off project applications ("apply this to my team") may live outside the language as ordinary documents; promote one to `sequences/` when it proves reusable.

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
