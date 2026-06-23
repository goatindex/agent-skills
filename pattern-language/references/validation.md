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
- [ ] Reciprocity: A lists B in `links_down` ⇔ B lists A in `links_up`. (WARN — emitted once per broken pair, from the lower-numbered pattern)
- [ ] No orphans (empty `links_up` and `links_down`). (WARN)
- [ ] Context prose mentions every `links_up` target; Links-down prose mentions every `links_down` target. (WARN — uses anchored filename-or-`(N)` match, not bare substring)
- [ ] `index.md` exists; every pattern appears in exactly one **list-item line** (`N. [Name](file.md)`); prose cross-links in the index are not counted. (FAIL on missing/duplicated list entries)
- [ ] `index.md` group headings match the `scale:` values used in frontmatter. (WARN)
- [ ] Pattern `name` does not contain `#` (breaks inline-comment stripping in the parser). (FAIL)
- [ ] Lateral links: every `sympathies` / `tensions` target exists and is not self-referential. (FAIL on missing/self; WARN — emitted once — when a relation is one-sided, since both are mutual.)

*Note: two spec rules are not yet enforced by the script — treat them as manual checks:*
- *Index list items are in ascending number order within each group.*
- *Context prose mentions no patterns outside `links_up`.*

### Single-doc shape — the checked subset

When the argument is a single `.md` file, the script reads identity/scale/confidence from `## N. Name ✻` and `# SCALE …` headers and reads **all relations from the embedded `mermaid graph TD` block** (edge grammar in `language-structure.md`). It checks: unique pattern numbers (FAIL on duplicates); every graph edge points at a real pattern (FAIL); each pattern carries a bolded problem statement and a bolded `Therefore:` instruction (FAIL); links_down run largest-to-smallest by number (WARN on reversal); a pattern absent from the graph is an orphan (WARN); sympathy/tension targets exist (FAIL). It does **not** check frontmatter integrity, header/frontmatter agreement, or `index.md` coverage — those are folder-shape concerns. If the doc has no `mermaid` block the link network is unchecked (WARN); convert to the folder shape for a full structural pass.

## Qualitative critique

Apply per pattern, then to the whole. Report findings ranked by severity, with the specific fix — not generalities.

**Per pattern**

1. **Forces test.** Does the problem statement name a genuine tension? An absence ("no X exists") restated as need is a fail — find the underlying conflict of forces or cut the pattern.
2. **Actionability test.** Could a competent reader act on the Therefore tomorrow without asking what it means? Could two readers act on it and produce usefully *different* implementations? Both must be yes.
3. **Evidence proportionality.** Does the body's evidence justify the confidence rating? ✻✻ with a paragraph of vibes is miscalibrated.
4. **Name test.** Could the name be used in a working sentence by practitioners? Is it concrete?
5. **Single resolution.** One tension, one instruction. Two instructions = split candidate.

**Whole language**

6. **Gradient coherence.** Do the scale groups form a real largest-to-smallest gradient, or are they just categories? Categories are a smell — the reader should descend.
7. **Connectivity.** Is the network connected? Clusters with no links between them may be two languages.
8. **Coverage honesty.** Are there obvious load-bearing tensions in the domain with no pattern? List them as candidate patterns rather than padding the language.
9. **Voice consistency.** Empirical, plain, no marketing. Flag patterns that read like policy or advertising.

## Reporting format

```
VALIDATION — <language name>
Structural: PASS | FAIL (n fails, m warns) — rung used: script | manual checklist
  FAIL  012-standing-mandate.md: links_down target 19 does not exist
  WARN  007-open-floor.md: links_up target 3 not mentioned in context prose
  WARN  007-open-floor.md: links_down to 015-one-page-minutes.md, but that pattern does not link_up back
Qualitative:
  HIGH  004-member-ask.md: problem statement is an absence, not a tension — suggest: "<rewrite>"
  MED   index group 'Practices' is a category, not a scale — consider splitting into …
```
