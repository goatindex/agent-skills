# Pattern form — the anatomy of a single pattern

This is the canonical file format for one pattern. Every pattern in every language produced by this skill follows it. The format has two layers: **frontmatter** (the machine-checkable data layer) and **body** (the Alexandrian prose form). They must agree.

## Frontmatter schema

```yaml
---
number: 12                     # integer, unique within the language
name: Visible Decision Trail   # short noun phrase, evocative, no trailing punctuation
confidence: 1                  # 0 | 1 | 2  (asterisks: none / ✻ / ✻✻)
scale: Committee Practices     # must match a scale group declared in index.md
links_up: [3, 7]               # pattern numbers this one helps complete (lower numbers)
links_down: [15, 18]           # pattern numbers that complete this one (higher numbers)
sympathies: [9]                # optional — patterns that reinforce this one (any scale)
tensions: [14]                 # optional — patterns whose forces pull against this one
---
```

Constraints the validator enforces: all six required keys present; `confidence` ∈ {0,1,2}; links are lists of integers (empty list allowed, `[]`); link targets must exist. Keep frontmatter to exactly these keys plus optional `status:` (`draft` | `reviewed`), `date:`, and the two **lateral-link** keys `sympathies:` / `tensions:`.

**Lateral links.** `links_up`/`links_down` carry the *hierarchy* (the scale gradient). Real languages also discover *lateral* relationships across scales — patterns that **reinforce** each other (a "strong sympathy") and patterns whose resolutions **conflict** (a "known tension" a designer must resolve knowingly). Record these in `sympathies:`/`tensions:` when they are load-bearing; both are **mutual**, so the validator warns if A lists B but B does not list A. They are optional: a young language can leave them empty. Do not overload `links_down` to express them — a tension is not a completion.

## Filename

`NNN-kebab-case-name.md`, zero-padded to three digits: `012-visible-decision-trail.md`. The number in the filename must equal `number:` in frontmatter.

## Body template

```markdown
# 12. Visible Decision Trail ✻

…this pattern helps complete [Standing Mandate (3)](003-standing-mandate.md) and
[Open Committee Floor (7)](007-open-committee-floor.md). When decisions are made
under those patterns, members need a way to see how and why…

## Problem

**Members trust decisions they can trace, but the people making decisions are
too busy to narrate them; when the trail is invisible, trust decays even when
the decisions are good.**

Two or three paragraphs of evidence and reasoning. Why does this tension exist?
What happens when it goes unresolved? What have you observed? Argue from
experience and data, admit uncertainty, keep the voice plain and empirical.

## Therefore

**Publish a short, standing record of each decision — what was decided, by
whom, and the one or two reasons that mattered — in the same place every time,
within a week of the decision. Make writing it part of the deciding, not an
extra job afterwards.**

An optional paragraph or simple diagram (described in words or as a small
Mermaid block) showing the solution's shape, and/or a **resulting context**
paragraph: what the world looks like once the pattern is applied, and which
tensions it newly exposes.

## Known uses

- The 2024 restructure working group — trail kept in the wiki, cited in the
  2025 AGM as why the merger held.
- The library board adopted the same standing record in 2025 after observing
  the working group's.

## Cautions

The record becomes a compliance artifact nobody reads if it is decoupled
from the deciding; retro-writing the trail weeks later destroys its value.

## Links down

…to make the record cheap to produce, use [One-Page Minutes (15)](015-one-page-minutes.md);
to make sure it is read, anchor it in [Member Briefing Rhythm (18)](018-member-briefing-rhythm.md)…
```

## Rules that make it Alexandrian

1. **Header line**: `# <number>. <Name>` followed by the confidence asterisks — `✻✻`, `✻`, or nothing. Must agree with frontmatter.
2. **Context prose** (before `## Problem`): one short paragraph, beginning conventionally with an ellipsis, naming the larger patterns this one completes — as markdown links to their files. Every number in `links_up` appears here; mention no patterns that aren't in `links_up`.
3. **Problem statement**: the first element under `## Problem` is a **single bolded statement** of the tension. The test: does it name forces in conflict? "There is no X" fails the test. "People need A, but circumstance B makes A costly" passes.
4. **Body**: evidence and reasoning in plain prose. Length proportional to confidence — a ✻✻ pattern earns its rating with substantial evidence; a 0-asterisk pattern can be a paragraph of honest hypothesis.
5. **Therefore**: the first element under `## Therefore` is a **single bolded instruction**. Imperative voice. It must be performable ("publish a short standing record…") and under-specified on purpose ("in the same place every time" — but it does not say which place). If you cannot act on it tomorrow, it is too vague; if two teams following it would produce identical artifacts, it is too specific.
6. **Known uses** (optional section, after Therefore): one list item per real, independent instance of *this* pattern working — the PLoP tradition's evidence slot. This is where confidence is *earned*: the validator warns on a ✻✻ pattern with no Known uses section. **A known use is not a citation.** It is a specific occasion on which this exact pattern was applied and observed to resolve its tension — "the 2024 restructure group kept the trail and the merger held," not "good governance literature recommends transparency." Corroboration from an adjacent domain ("MechWarrior 5 tracks faction reputation," "TTRPGs recommend clear party roles") is *supporting evidence* — it belongs in the body prose or the pathfinder's landscape, never as a known use, because it is not an independent instance of the pattern and cannot bear the rule-of-three weight that promotes confidence. If you have no genuine instances, leave the section out and stay at confidence 0 — an empty-but-honest known-uses record beats a padded one.
7. **Cautions** (optional section): the known misapplications and failure modes, stated plainly. Both scrumbook.org ("scaling before high performance scales your dysfunctions") and Group Works ("Cautions & Caveats") carry this slot; a mature pattern knows how it goes wrong.
8. **Links down** (closing prose, always the final section): a paragraph beginning conventionally with an ellipsis, linking to the smaller patterns that complete this one. Every number in `links_down` appears here.
9. **A pattern with empty `links_up` AND empty `links_down` is an orphan** — only acceptable transiently mid-edit; the validator warns.

## Naming patterns

Names carry the language. Prefer concrete, slightly evocative noun phrases that someone could drop into a sentence ("we need a *Quiet Back* here"). Avoid abstractions ("Effective Communication Strategy") and avoid verbs. Two to five words.

## Confidence calibration

Calibrate against **known uses** (the pattern community's "rule of three": one instance is an event, two a coincidence, three a pattern):

- `0` (no asterisk) — a hypothesis worth recording. You believe it; you have not tested it. No known uses required.
- `1` (✻) — real progress on the problem; at least **one** known use, but better formulations surely exist.
- `2` (✻✻) — you would be surprised to see a living solution to this problem that does not contain this pattern in some form. Rare. Demands roughly **three independent known uses** documented in the `## Known uses` section, plus evidence in the body.

When updating an existing pattern, revisit its confidence: ratings should move with evidence, in both directions.
