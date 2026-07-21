---
name: pattern-language
description: Create, update, expand, apply, or validate a pattern language in the style of Christopher Alexander — for any domain, not just architecture. Use whenever the user mentions a pattern language, Alexandrian patterns, generative patterns, "turning what works into patterns", codifying recurring solutions to recurring problems, or building a cross-linked library of named practices (organising, governance, game design, teaching, software process, anything). Also use for critique or structural integrity checks of an existing language, and for applying a language to a concrete project (producing a sequence). Do NOT use for UI component libraries, Gang-of-Four coding questions, persuasion proposals (toc-proposal), or PA letterhead docs (pa-document).
---

# Pattern Language

Create, grow, apply, and validate pattern languages in the Alexandrian tradition, agnostic of domain. A pattern language is not a list of tips: it is an **ordered network** of named patterns, descending a declared gradient from largest to smallest, where each pattern resolves a recurring tension and connects upward to the patterns it completes and downward to the patterns that complete it.

## Operations

Determine which operation the user wants, then follow the matching workflow. Read the listed reference file before starting — each is short and load-bearing.

| Operation | When | Read first |
|---|---|---|
| **Create** | New language from scratch | `references/intake.md`, then `references/language-structure.md` |
| **Mine** | Extract candidate patterns from real material (retros, decision logs, literature) — at create time or as a re-entrant pass before Add/Expand | `references/mining.md` |
| **Add / update** | New pattern(s) into an existing language, or revise one | `references/pattern-form.md` |
| **Expand / restructure** | New scale levels, re-sequencing, splitting/merging patterns | `references/language-structure.md` |
| **Apply** | Use the language on a concrete project — the deliverable is a **sequence** | `references/language-structure.md` (§ Sequences) |
| **Validate / critique** | Integrity check or qualitative review | `references/validation.md` |

Read `references/pattern-form.md` before writing or editing any pattern body — it defines the canonical anatomy and file format. For Add / Expand / Apply on an existing language, read its `PATHFINDER.md` first — it is the language's own statement of scope, gradient, and grounding (`references/pathfinder.md` defines it). For all other routing, the table above governs. `references/apl-exemplar.md` holds the factual index of Alexander's original 253 patterns and his conventions — consult it when the user wants fidelity to the original or an example of scale grouping.

## The artifact

A pattern language comes in one of **two delivery shapes**, both first-class and both validatable (see `references/language-structure.md`):

- **Folder** (default) — one markdown file per pattern plus an `index.md` carrying the ordered sequence with connective prose, a `PATHFINDER.md` self-description, and optionally `sequences/` for named sequences. Links live in typed frontmatter, so every structural check runs at full strength and sessions load only the patterns they need. Right at any size — a 5-pattern seed or a 250-pattern corpus — and the shape to prefer whenever a language will be grown over time, machine-checked, or run by lighter models.
- **Single network-doc** — the whole language in one `.md` with an embedded `mermaid graph TD` block (the canonical link source), a generative sequence, and appendices including a `## Pathfinder` section. Best for small-to-medium languages hosted on a wiki page.

Either way, the language carries a **pathfinder** (`references/pathfinder.md`): purpose, scope, declared gradient, landscape and key references, evidence base, and growth queue. It is written at create time from the intake answers and re-read before any later operation — it is what keeps growth grounded and scoped.

Choose by host and size, not by decree; when unsure, default to the folder (it loses no checks). Do not hand-maintain both shapes for one language — keep one canonical and generate the other.

## Core doctrine (applies to every operation)

These are the things that make output Alexandrian rather than a tip list. The full anatomy is in `references/pattern-form.md`; the non-negotiables are:

1. **A pattern is a resolution of forces.** The problem statement must name a genuine tension (two or more forces pulling against each other), not a mere absence ("there is no onboarding doc" is not a problem statement; the tension between X and Y that the missing thing would resolve is).
2. **The solution is an instruction.** It begins in effect with "Therefore:" and tells the reader what to *do* — specific enough to act on, general enough to be done a thousand different ways without ever being the same twice.
3. **Every pattern is embedded.** Context prose at the top links up to larger patterns it helps complete; closing prose links down to smaller patterns that complete it. A pattern with no links is not yet in the language.
4. **Confidence is rated honestly.** Two asterisks (✻✻) = invariant, deeply believed; one (✻) = real progress, will improve; none = a plausible hypothesis. Default new patterns to zero or one asterisk; two must be earned by evidence — the rule of three: roughly three independent **known uses**, documented in the pattern (see `references/pattern-form.md`).
5. **Gradient ordering.** Every language descends one declared, monotone axis — spatial scale, organisational scope, or process order (see `references/language-structure.md` § The gradient). Lower numbers = larger/earlier on the axis. Links up point to lower numbers, links down to higher numbers. The reader should be able to enter at any pattern and walk the network. Beyond the hierarchy, record **lateral links** where they are load-bearing — *sympathies* (patterns that reinforce each other) and *tensions* (patterns whose forces conflict, which a designer must resolve knowingly). Both are mutual and optional; see `references/pattern-form.md`.
6. **Empirical voice.** The body argues from observation and evidence, in plain language, and admits uncertainty. No marketing tone.
7. **The language knows itself.** Every language carries a pathfinder stating its purpose, scope, gradient, landscape, and evidence base. Work that contradicts the pathfinder is either wrong or a deliberate re-scoping — never silent drift.

## Workflow notes

**Create**: run the intake in `references/intake.md` (domain, purpose, gradient, seed problems, landscape); when material exists to mine, run the mining pipeline (`references/mining.md`) so seed problems arrive harvested rather than brainstormed. Propose the scale structure and a seed pattern list for the user's approval *before* writing pattern bodies, then write `PATHFINDER.md` from the intake answers, then patterns largest-scale first. Start small — 5 to 15 patterns is a healthy seed language; the form invites piecemeal growth.

**Mine**: follow the pipeline in `references/mining.md` — harvest fragments, cluster by tension, forces-test, name, route to seed table or Growth queue, and write provenance (including null results and resumption markers) back to the pathfinder. Mining recurs: any Add/Expand on a language with accumulated new material starts with an incremental pass from the pathfinder's last resumption marker.

**Add / update**: read `PATHFINDER.md`, the existing `index.md`, and the patterns adjacent in scale before drafting, so scope, links and numbering land correctly. A candidate outside the pathfinder's scope is parked in its Growth queue, not shoehorned in. New patterns take the next free number within their scale band where possible; renumbering existing patterns is a restructure, not an add.

**Apply**: the deliverable is a **sequence** — an ordered walk through the applicable subset, largest scale first, with a purpose line, entry conditions, one line per step on how the pattern lands in the project, and cautions (`references/language-structure.md` § Sequences). Reusable sequences are saved to `sequences/` and listed in the pathfinder; one-off applications may stay outside the language.

**Validate**: prefer the script (below); fall back to the manual checklist in `references/validation.md`. Always finish a validation with a qualitative pass — the script checks structure, not whether problems are real tensions or solutions are actionable.

**Graph view** (any operation, on request): emit a Mermaid `graph TD` built from each pattern's `links_down` (solid `-->`), grouped by scale with `subgraph` blocks, optionally adding `-.-` sympathy and `x--x` tension edges. Mermaid is plain text and renders in most hosts without binaries. In the single-doc shape this block is canonical, not decorative — the validator reads relations from it. If Graphviz is confirmed present and the user wants an image, a DOT file may be rendered instead — but never depend on it.

## Context discipline & model weight

Correct work never requires the whole language in context:

- **Working set for Add/update/Apply**: this SKILL.md, the one routed reference, `PATHFINDER.md`, `index.md`, and only the *link-adjacent* patterns (the band above and below the insertion point). Never load every pattern file — the index is the network's compressed map. (A reason to prefer the folder shape for long sessions or lighter models: single-doc forces the whole corpus into the window.)
- **Batch–validate–drop**: write one scale band, validate, fix, then drop the bodies from context (files are canonical — see Exit). Largest-first means each new pattern links upward only into work already on disk. The validator is external memory — global consistency (reciprocity, coverage, dangling links) is what a context-limited session drops first.
- **Pathfinder first**: a session loading only `PATHFINDER.md` + `index.md` can act correctly on a language it has never read in full — that is what the pathfinder is compressed for.
- **Mining is incremental**: resume from the pathfinder's provenance markers; never re-read a historical corpus.

Operations differ in how much unfenced judgement they demand, so the minimum model tier differs. The rule: **writing the fences needs a strong model; working inside them doesn't.**

| Operation | Minimum tier | Why |
|---|---|---|
| Validate (script) | light | Mechanical: run, relay grouped output |
| Add / Apply (pathfinder exists) | mid | Scope, form, and links are externally fenced; the validator catches drift |
| Validate (qualitative), Mine | strong preferred | The forces test and tension-clustering are subtle discriminations; light models cluster by vocabulary |
| Create (intake, gradient, naming) | strong | The gradient decision is foundational, made once, and invisible to the validator |

Division of labour: a strong model runs intake, sets the pathfinder, and approves the seed table; a lighter model drafts bodies inside those fences; the script plus a strong-model qualitative pass close the loop.

## Validation script

`scripts/validate_language.py` — Python, **standard library only**. It auto-detects the delivery shape from the path. Run as:

```
python3 scripts/validate_language.py [--verbose] <language-folder | language-doc.md>
```

Full check list and severities: `references/validation.md` (single source). Folder summary: frontmatter integrity; unique numbers; link targets exist; header/frontmatter agreement; bolded Problem/Therefore statements; lateral-link (sympathy/tension) targets exist and are mutual; index list-item coverage (prose cross-links in the index are ignored — only list items count); pathfinder presence and core headings; ✻✻ patterns carry Known uses, and starred known-uses are screened for convention-vs-instance vocabulary; sequence links resolve. Single-doc summary: headers give identity/scale/confidence, the `mermaid` block gives every relation, and the checked subset is the link/orphan/problem-therefore/pathfinder set (frontmatter and index checks do not apply). Exits non-zero on any FAIL. WARNs do not block; they print grouped by category, capped at 10 per category (`--verbose` lifts the cap), followed by a network-statistics line (edges, links/pattern, reciprocity, orphans) interpreted against the benchmarks in `references/validation.md`.

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
*v0.7 (July 2026). Full version history: `references/changelog.md`.*
