# Validation — structural checks and qualitative critique

Two layers. The **structural** layer is what `scripts/validate_language.py` automates; when the script cannot run, perform it by hand from this checklist and tell the user it was a manual pass. The **qualitative** layer is always manual — the script cannot judge whether a problem is a real tension.

## Structural checklist (the script's authoritative check list)

FAIL items block; WARN items are reported but don't block. The script docstring points here rather than duplicating severities. The script auto-detects the **delivery shape** from its argument: a directory → folder shape (the full list below); a single `.md` file → single-doc shape (the subset noted at the end).

- [ ] Every pattern file has frontmatter with all required keys: `number`, `name`, `confidence`, `scale`, `links_up`, `links_down`. (FAIL)
- [ ] `number` unique across the language; filename prefix (3+ digits) matches `number`. (FAIL)
- [ ] `confidence` is 0, 1, or 2. (FAIL)
- [ ] Every `links_up` / `links_down` target exists as a pattern. (FAIL)
- [ ] Header line `# N. Name` matches frontmatter number and name; asterisks match confidence. (FAIL)
- [ ] `## Problem` and `## Therefore` sections present (headings tolerate an optional colon); first element of each is a bolded statement. (FAIL — error message shows headings found nearby)
- [ ] `links_up` point to lower numbers, `links_down` to higher. (WARN — legitimate exceptions exist mid-restructure)
- [ ] Reciprocity: A lists B in `links_down` ⇔ B lists A in `links_up`. (WARN — one per one-way edge, emitted from the asserting side; a one-way edge has exactly one asserter, so pairs are never double-reported)
- [ ] No orphans (empty `links_up` and `links_down`). (WARN — orphanhood is judged on a pattern's *own* frontmatter; a pattern other patterns point at but which declares nothing itself still warns, deliberately: declarations are the pattern's responsibility)
- [ ] Context prose mentions every `links_up` target; Links-down prose mentions every `links_down` target. (WARN — uses anchored filename-or-`(N)` match, not bare substring)
- [ ] `index.md` exists; every pattern appears in exactly one **list-item line** (`N. [Name](file.md)`); prose cross-links in the index are not counted. (FAIL on missing/duplicated list entries)
- [ ] `index.md` group headings match the `scale:` values used in frontmatter. (WARN)
- [ ] Pattern `name` does not contain `#` (breaks inline-comment stripping in the parser). (FAIL)
- [ ] Lateral links: every `sympathies` / `tensions` target exists and is not self-referential. (FAIL on missing/self; WARN — emitted once — when a relation is one-sided, since both are mutual.)
- [ ] `PATHFINDER.md` exists and carries the five core headings (Purpose & audience, Scope, The gradient, Landscape & key references, Evidence & provenance — see `references/pathfinder.md`). (WARN on missing file or heading)
- [ ] A ✻✻ (confidence 2) pattern has a `## Known uses` section. (WARN — rule of three)
- [ ] `sequences/*.md`: every pattern link resolves to an existing pattern (FAIL); step numbers run down the gradient, i.e. ascending (WARN, reported once per sequence); a sequence file with no pattern links at all (WARN).

*Note: two spec rules are not yet enforced by the script — treat them as manual checks:*
- *Index list items are in ascending number order within each group.*
- *Context prose mentions no patterns outside `links_up`.*

### Single-doc shape — the checked subset

When the argument is a single `.md` file, the script reads identity/scale/confidence from `## N. Name ✻` and `# SCALE …` headers and reads **all relations from the embedded `mermaid graph TD` block** (edge grammar in `language-structure.md`). It checks: unique pattern numbers (FAIL on duplicates); every graph edge points at a real pattern (FAIL); each pattern carries a bolded problem statement and a bolded `Therefore:` instruction (FAIL); links_down run largest-to-smallest by number (WARN on reversal); a pattern absent from the graph is an orphan (WARN); sympathy/tension targets exist (FAIL); a `## Pathfinder` appendix section is present (WARN if absent). It does **not** check frontmatter integrity, header/frontmatter agreement, or `index.md` coverage — those are folder-shape concerns. If the doc has no `mermaid` block the link network is unchecked (WARN); convert to the folder shape for a full structural pass.

## Qualitative critique

Apply per pattern, then to the whole. Report findings ranked by severity, with the specific fix — not generalities.

**Per pattern**

1. **Forces test.** Does the problem statement name a genuine tension? An absence ("no X exists") restated as need is a fail — find the underlying conflict of forces or cut the pattern.
2. **Actionability test.** Could a competent reader act on the Therefore tomorrow without asking what it means? Could two readers act on it and produce usefully *different* implementations? Both must be yes.
3. **Evidence proportionality.** Does the body's evidence justify the confidence rating? ✻✻ with a paragraph of vibes is miscalibrated.
4. **Name test.** Could the name be used in a working sentence by practitioners? Is it concrete?
5. **Single resolution.** One tension, one instruction. Two instructions = split candidate.

**Whole language**

6. **Gradient coherence.** Do the scale groups descend a real, declared, monotone axis (spatial scale, scope, process order — see `language-structure.md` § The gradient), or are they unordered categories? Categories with no ordering rationale are the smell — the reader should descend. Check the groups against the axis declared in `PATHFINDER.md` § The gradient.
7. **Connectivity.** Is the network connected? Clusters with no links between them may be two languages. Density benchmark: APL averages ~14 links per pattern (1,758 edges over 253 patterns); a language averaging under ~2 is under-woven — its patterns are filed, not embedded. (On reciprocity: APL's own network is only ~29% mutually asserted, but that is a defect of hand-maintained prose links, not a target — typed frontmatter makes full reciprocity cheap, so hold new languages to it.)
8. **Coverage honesty.** Are there obvious load-bearing tensions in the domain with no pattern? List them in the pathfinder's Growth queue rather than padding the language.
9. **Voice consistency.** Empirical, plain, no marketing. Flag patterns that read like policy or advertising.
10. **Pathfinder fidelity.** Does the language still match its own `PATHFINDER.md` — scope, gradient, stated evidence base? Scope drift and undeclared gradient changes are HIGH findings; a stale Growth queue or Change log is MED.

## Writers' workshop (peer-critique protocol)

The pattern community's quality mechanism is not solo review but the **writers' workshop** (Richard Gabriel's format, used by every PLoP conference): a structured reading in which the author stays silent while readers work through the pattern. Run it on request, or offer it for any pattern being promoted to ✻ or ✻✻ — it catches what the structural and solo-qualitative passes cannot: whether the pattern *communicates*.

Protocol, per pattern (adapted for one reviewer; with several humans, let each speak in turn):

1. **Author is silent** until step 5. If reviewing in-conversation, treat the pattern file as the author's whole statement — no clarifications sought.
2. **Read back**: summarise the pattern in your own words — the tension, the instruction, who it is for. If the summary is hard to produce, that is itself the primary finding.
3. **What works**: name the strongest elements first (the name, the forces argument, a known use) and *why* they work. Not a courtesy — it tells the author what to protect while revising.
4. **Suggestions for improvement**: findings in severity order, each tied to a specific quality test (forces, actionability, evidence proportionality, name, single resolution) with a concrete rewrite offered. Format each as a labelled review comment (e.g. Conventional Comments: `issue (blocking):`, `suggestion:`, `praise:`) so intent and severity are explicit.
5. **Author responds** — questions of clarification only, then decides; the workshop advises, the author owns the pattern.

Workshop findings feed the same report as the qualitative pass. A pattern that has been workshopped and revised is a reasonable candidate for `status: reviewed`.

## Reporting format

The script prints FAILs first (blockers up top), then WARNs **grouped by category** with each category capped at 10 lines (`--verbose` lifts the cap — real languages can produce hundreds of same-type warnings; APL yields 1,251 reciprocity warns, which ungrouped would bury everything else), then a network-statistics line, then the summary:

```
FAIL  012-standing-mandate.md: links_down target 19 does not exist
WARN  reciprocity: 27
      007-open-floor.md: links_down to 015-one-page-minutes.md, but that pattern does not link_up back
      …
      … 17 more (--verbose lists all)
WARN  prose mentions: 2
      007-open-floor.md: links_up target 3 not mentioned in context prose
      …

Network: 24 patterns (✻✻ 3 / ✻ 12 / — 9); 61 edges; 5.1 links/pattern; 84% reciprocal; 0 orphans

24 patterns checked (folder shape): FAIL (1 fail, 29 warns)
```

Interpret the statistics against the benchmarks in qualitative check 7. When validating manually, mirror this shape and mark the rung:

```
VALIDATION — <language name>
Structural: PASS | FAIL (n fails, m warns) — rung used: script | manual checklist
Qualitative:
  HIGH  004-member-ask.md: problem statement is an absence, not a tension — suggest: "<rewrite>"
  MED   index group 'Practices' is unordered — declare its position on the gradient or split it
```
