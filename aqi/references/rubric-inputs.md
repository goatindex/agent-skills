# AQI Input Rubric — "Is this assessable?"

Scale, tier table, and hard rules live in SKILL.md. Gating dimensions: **completeness, consistency**. Score in the order below. Every anchor is tier-relative: "the required artefact set" means the minimum set for the assessed tier (SKILL.md §3).

## Completeness (gating)

| Score | Anchor |
|---|---|
| 4 | Required artefact set for the tier complete; scope of change fully described including edge and failure paths; no material question the documentation cannot answer. |
| 3 | Required artefact set present; remaining gaps peripheral, enumerable, blocking no trust boundary or data flow. |
| 2 | Core artefacts present; gaps bounded and identified, closable by targeted questions without restructuring the submission; no trust boundary entirely undocumented. |
| 1 | Material gaps: at least one trust boundary, data flow, or core component undocumented; assessment would require substantial assumption-making. |
| 0 | Artefact set absent or so sparse the system cannot be reconstructed. |

## Consistency (gating)

| Score | Anchor |
|---|---|
| 4 | No contradictions across technical, logical, or descriptive levels; terminology stable; diagrams, prose, and configurations agree. |
| 3 | Only trivial inconsistencies (naming drift, version-label mismatch) resolvable from context without changing meaning. |
| 2 | Isolated contradictions, each localised and resolvable with a single clarifying question; none touches a security-relevant claim. |
| 1 | Contradiction on at least one security-relevant claim (e.g. prose asserts encryption, diagram shows a plaintext path), or systemic terminology confusion forcing interpretation. |
| 0 | Multiple irreconcilable accounts of what is being built or changed. |

## Currency

| Score | Anchor |
|---|---|
| 4 | All artefacts versioned, dated, attributable; each explicitly reflects the proposed end-state or a marked current-state baseline; nothing stale. |
| 3 | Artefacts current; only minor version/dating hygiene gaps. |
| 2 | Mostly current; some artefacts undated or of uncertain vintage, but content corroborated by other current material. |
| 1 | Key artefacts demonstrably stale (predate known system changes) or of unknown provenance; reliance would mislead. |
| 0 | Documentation describes a system state that no longer exists or never did; provenance unestablished. |

## Conformity (neutral valence — scrutiny signal; non-gating; never in composite)

Low scores are not defects. Conformity ≤ 1 raises the effort tier one step (SKILL.md §3).

| Score | Anchor |
|---|---|
| 4 | Implements recognised reference pattern(s) for the technology class; deviations absent or cited and justified. |
| 3 | Largely pattern-conformant; deviations minor and justified within the submission. |
| 2 | Recognisable patterns present with material deviations left unexplained. |
| 1 | Novel approach where established patterns exist, with no justification for the departure. |
| 0 | No recognisable pattern; unprecedented for the technology class. May be legitimate innovation — maximum scrutiny and effort uplift, never automatic rejection. |

## Clarity (two sub-tests; dimension score = lower of the two)

**Sub-test A — Surface clarity:** can each security-relevant claim be located and restated after a single read? Structural failures drop this score; prose style alone does not.

**Sub-test B — Specificity:** score with the claim-audit protocol in `clarity-specificity-protocol.md` (extract claims → mark security relevance → classify S/P/U against Mechanism/Location/Verification → threshold rules). The operational anchors there are authoritative. The fluent-but-empty pattern (high A, low B) is the generated-slop signature.

## Composite and gate

Composite = weighted mean of completeness, consistency, currency, clarity (conformity excluded), capped at (lowest gating score + 1). Hard rule, gate bands, and caveat handling per SKILL.md §§5–6. The aggregated composite is the **coupling cap input** for the eventual outputs run — persist the JSON.
