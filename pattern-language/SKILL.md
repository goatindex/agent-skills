---
name: pattern-language
description: Create, update, expand, or validate a pattern language in the style of Christopher Alexander — for any domain, not just architecture. Use whenever the user mentions a pattern language, Alexandrian patterns, generative patterns, "turning what works into patterns", codifying recurring solutions to recurring problems, or building a cross-linked library of named practices (organising, governance, game design, teaching, software process, anything). Also use for critique or structural integrity checks of an existing language. Do NOT use for UI component libraries, Gang-of-Four coding questions, persuasion proposals (toc-proposal), or PA letterhead docs (pa-document).
---

# Pattern Language

Create, grow, and validate pattern languages in the Alexandrian tradition, agnostic of domain. A pattern language is not a list of tips: it is an **ordered network** of named patterns, largest scale to smallest, where each pattern resolves a recurring tension and connects upward to the patterns it completes and downward to the patterns that complete it.

## Operations

Determine which operation the user wants, then follow the matching workflow. Read the listed reference file before starting — each is short and load-bearing.

| Operation | When | Read first |
|---|---|---|
| **Create** | New language from scratch | `references/intake.md`, then `references/language-structure.md` |
| **Add / update** | New pattern(s) into an existing language, or revise one | `references/pattern-form.md` |
| **Expand / restructure** | New scale levels, re-sequencing, splitting/merging patterns | `references/language-structure.md` |
| **Validate / critique** | Integrity check or qualitative review | `references/validation.md` |

Read `references/pattern-form.md` before writing or editing any pattern body — it defines the canonical anatomy and file format. For all other routing, the table above governs. `references/apl-exemplar.md` holds the factual index of Alexander's original 253 patterns and his conventions — consult it when the user wants fidelity to the original or an example of scale grouping.

## The artifact

A pattern language comes in one of **two delivery shapes**, both first-class and both validatable (see `references/language-structure.md`):

- **Folder** (default) — one markdown file per pattern plus an `index.md` carrying the ordered sequence with connective prose. Links live in typed frontmatter, so every structural check runs at full strength. Best for larger languages, languages grown over time, and Obsidian/apl-md workflows.
- **Single network-doc** — the whole language in one `.md` with an embedded `mermaid graph TD` block (the canonical link source), a generative sequence, and appendices. Best for small-to-medium languages hosted on a wiki page.

Choose by host and size, not by decree; when unsure, default to the folder (it loses no checks). Do not hand-maintain both shapes for one language — keep one canonical and generate the other.

## Core doctrine (applies to every operation)

These are the things that make output Alexandrian rather than a tip list. The full anatomy is in `references/pattern-form.md`; the non-negotiables are:

1. **A pattern is a resolution of forces.** The problem statement must name a genuine tension (two or more forces pulling against each other), not a mere absence ("there is no onboarding doc" is not a problem statement; the tension between X and Y that the missing thing would resolve is).
2. **The solution is an instruction.** It begins in effect with "Therefore:" and tells the reader what to *do* — specific enough to act on, general enough to be done a thousand different ways without ever being the same twice.
3. **Every pattern is embedded.** Context prose at the top links up to larger patterns it helps complete; closing prose links down to smaller patterns that complete it. A pattern with no links is not yet in the language.
4. **Confidence is rated honestly.** Two asterisks (✻✻) = invariant, deeply believed; one (✻) = real progress, will improve; none = a plausible hypothesis. Default new patterns to zero or one asterisk; two must be earned by evidence.
5. **Scale ordering.** Lower numbers = larger scale. Links up point to lower numbers, links down to higher numbers. The reader should be able to enter at any pattern and walk the network. Beyond the hierarchy, record **lateral links** where they are load-bearing — *sympathies* (patterns that reinforce each other) and *tensions* (patterns whose forces conflict, which a designer must resolve knowingly). Both are mutual and optional; see `references/pattern-form.md`.
6. **Empirical voice.** The body argues from observation and evidence, in plain language, and admits uncertainty. No marketing tone.

## Workflow notes

**Create**: run the intake in `references/intake.md` (domain, purpose, scales, seed problems), propose the scale structure and a seed pattern list for the user's approval *before* writing pattern bodies, then write patterns largest-scale first. Start small — 5 to 15 patterns is a healthy seed language; the form invites piecemeal growth.

**Add / update**: read the existing `index.md` and the patterns adjacent in scale before drafting, so links and numbering land correctly. New patterns take the next free number within their scale band where possible; renumbering existing patterns is a restructure, not an add.

**Validate**: prefer the script (below); fall back to the manual checklist in `references/validation.md`. Always finish a validation with a qualitative pass — the script checks structure, not whether problems are real tensions or solutions are actionable.

**Graph view** (any operation, on request): emit a Mermaid `graph TD` built from each pattern's `links_down` (solid `-->`), grouped by scale with `subgraph` blocks, optionally adding `-.-` sympathy and `x--x` tension edges. Mermaid is plain text and renders in most hosts without binaries. In the single-doc shape this block is canonical, not decorative — the validator reads relations from it. If Graphviz is confirmed present and the user wants an image, a DOT file may be rendered instead — but never depend on it.

## Validation script

`scripts/validate_language.py` — Python, **standard library only**. It auto-detects the delivery shape from the path. Run as:

```
python3 scripts/validate_language.py <language-folder | language-doc.md>
```

Full check list and severities: `references/validation.md` (single source). Folder summary: frontmatter integrity; unique numbers; link targets exist; header/frontmatter agreement; bolded Problem/Therefore statements; lateral-link (sympathy/tension) targets exist and are mutual; index list-item coverage (prose cross-links in the index are ignored — only list items count). Single-doc summary: headers give identity/scale/confidence, the `mermaid` block gives every relation, and the checked subset is the link/orphan/problem-therefore set (frontmatter and index checks do not apply). Exits non-zero on any FAIL; WARNs (scale ordering, reciprocity, orphans, prose mentions) are reported but do not block.

## Graceful Degradation Ladder

**Gate: Freely.** This skill produces markdown knowledge artifacts; lower-fidelity output is honestly useful and cannot be mistaken for something verified.
**Trigger: none** — reduced output is honestly useful.

Rungs (highest fidelity first; announce which rung ran when more than one could):

1. **Full** — code execution available: write the pattern folder, run `scripts/validate_language.py`, emit Mermaid graph on request. → Validated language.
2. **Reduced** — no code execution: write the same folder/files; validate manually against `references/validation.md` and say so ("validated by manual checklist, not the script"). → Same artifact, hand-checked.
3. **Floor (reduced output)** — no file writing at all: emit the pattern files and index as fenced markdown blocks in conversation, with the manual checklist applied. Always reachable. → Content complete; persistence deferred to the user.

## Copyright boundary

Alexander's book is copyrighted. This skill encodes the *method and form*, and `references/apl-exemplar.md` carries the factual index of pattern names/numbers/groupings. Do not reproduce the book's prose. When users ask for original APL pattern content, summarise briefly in your own words and point them to the book or patternlanguage.cc; write *new* patterns rather than transcribing old ones.

## Exit

When an operation completes: summarise what changed (patterns added/edited, validation result, rung used), present the folder or files, and drop pattern-body working text from the conversation — the files are canonical.

---
*v0.4 (June 2026) — drawn from the Engine 52 worked language. Two delivery shapes are now first-class: the file-per-pattern folder (default) and a single wiki-doc whose embedded `mermaid graph TD` block is the canonical link source. The validator auto-detects shape from its path and gained a single-doc mode (header/scale/confidence + Mermaid relations + problem/therefore presence) and BOM-tolerant reads. Lateral links — `sympathies:` / `tensions:` (mutual; rendered `-.-` and `x--x`) — are now part of the schema and checked in both shapes. Folder checks from v0.3 are unchanged.*
*v0.3 (June 2026) — validator: `#`-in-name check moved to correct field; reciprocity WARNs halved (one per broken pair); context split uses regex matching `section()` so `## Problem:` is handled correctly; unknown frontmatter keys emit WARN (catches typos); misleading `prose_mentions` comment removed. Docs: `language-structure.md` index rule aligned with `validation.md`; reporting-format example updated to match script output. Cluster: complements skill-architecture/skill-creator; no dependencies on other skills.*
