# AQI Output Rubric — "Is this assessment trustworthy and usable?"

Scale, tier table, and hard rules live in SKILL.md. Gating dimensions: **coverage, traceability**. Outputs mode requires the aggregated inputs run (coupling — SKILL.md §1, §5).

## Coverage (gating)

| Score | Anchor |
|---|---|
| 4 | Every trust boundary, data flow, and in-scope asset addressed; covers the attack surface established by the inputs *and* the assessor's independent analysis; explicit out-of-scope register with rationale. |
| 3 | Full coverage of the input-established surface; omissions peripheral only; scope boundary stated. |
| 2 | Core attack surface covered; gaps identifiable but peripheral; nothing security-critical unaddressed. |
| 1 | Material portions of the surface unexamined (an entire boundary or privileged flow); coverage follows document structure rather than the threat surface. |
| 0 | Assessment addresses something other than the actual change, or leaves the surface largely unexamined. |

## Traceability (gating)

| Score | Anchor |
|---|---|
| 4 | Every finding cites evidence; every control maps to ≥1 finding; every accepted risk cites decision and owner; chain navigable both directions. |
| 3 | Chains present and mostly explicit; occasional implicit links recoverable without guesswork. |
| 2 | Findings generally evidenced; some controls or risk acceptances lack explicit linkage but the mapping can be reconstructed. |
| 1 | Substantial orphan content: controls without findings, findings without evidence, ratings without rationale. |
| 0 | Assertion throughout; no evidence chain; the assessment must be taken on faith. |

## Consistency (internal)

| Score | Anchor |
|---|---|
| 4 | Ratings, findings, controls, and residual-risk position fully coherent; severity scheme applied uniformly. |
| 3 | Coherent, with trivial drift only (one rating arguably mis-banded). |
| 2 | Isolated incoherences that do not alter the overall risk position. |
| 1 | Contradictory positions (critical finding, no control, residual "low"); severity scheme applied unevenly. |
| 0 | Conclusions do not follow from the body; risk position incoherent. |

## Conformity (controls — neutral valence; non-gating; never in composite)

| Score | Anchor |
|---|---|
| 4 | Controls drawn from recognised catalogues or approved internal patterns, with citations. |
| 3 | Mostly catalogue/pattern controls; minor variants justified. |
| 2 | Mix of standard and novel controls; novel elements explained. |
| 1 | Novel controls where standard ones exist, without justification. |
| 0 | Control set unprecedented for the problem class — maximum review scrutiny; excluded from patterning. |

## Actionability

| Score | Anchor |
|---|---|
| 4 | Every mitigation specifies what, where, who, and how verified; acceptance criteria testable. |
| 3 | Mitigations specific and assignable; verification implied rather than stated. |
| 2 | Mitigations concrete enough to implement, but owners or verification missing. |
| 1 | Directional advice only ("harden the API"); the implementer must redesign the control to act on it. |
| 0 | Platitudes; nothing implementable as written. |

## Clarity

Same two-sub-test structure as the input rubric, applied to the assessment's own prose; sub-test B per `clarity-specificity-protocol.md`; score = lower of the two.

## Patternability (categorical flag — not scored)

| Flag | Criteria | Effect |
|---|---|---|
| pattern_conformant | Reuses an approved pattern; pattern_ref cited; conformity ≥ 3 | Future submissions citing the pattern inherit documented scrutiny reduction |
| pattern_candidate | Novel but generalisable; **capped** composite ≥ 3.0 and traceability ≥ 3 | Nominated to the pattern library with applicability conditions |
| bespoke | One-off by design, or below candidate threshold | Marked do-not-reuse |

## Composite, coupling, gate

Composite = weighted mean of coverage, traceability, consistency, actionability, clarity (conformity excluded), capped at (lowest gating score + 1) **and** at the coupling limit: input composite + 1 with evidenced independent discovery (refs required), input composite otherwise. A pre-cap mean above the coupling cap is a breach — log it as a finding. Caveats from the input gate must appear in the assessment's limitations section. Gate per SKILL.md §6. If even excellent independent discovery leaves the cap binding unfairly, the principled remedy is a **re-scored inputs run** with assessor-gathered evidence added to the artefact register — never a manual override of the cap.
