---
name: aqi
description: Assessment Quality Index — score the quality of cyber security assessment inputs (submissions, change requests, design documents arriving for security review) and outputs (the security assessment reports themselves) against anchored 0–4/A–F rubrics, producing per-dimension scores, a gated composite, prioritised findings, and rendered assessor and requestor views. Use this skill whenever the user mentions AQI, assessment quality, intake review, assessment readiness, "is this submission ready for assessment", "review/score this security assessment", "evaluate these inputs", gap letters, or wants any structured quality evaluation of security review material — even if they don't name the framework. Also use it when asked whether a security assessment can be trusted, whether a submission is too vague or "AI slop", or whether an assessment approach can be patterned for reuse.
---

# Assessment Quality Index (AQI)

Two-part framework: **inputs mode** asks "is this assessable?" before a security assessment begins; **outputs mode** asks "is this assessment trustworthy and usable?" after. The two are coupled: an assessment's confidence is capped by the quality of its inputs.

Architecture note: the durable core of this skill is the rubrics, schema, and the arithmetic below. `scripts/aggregate.py` is disposable glue (stdlib-only Python). If it cannot run, perform the aggregation manually per §6 — degraded, never broken.

## 1. Mode selection

- Material is a submission / change request / design pack awaiting assessment → **inputs mode**.
- Material is a completed security assessment report → **outputs mode**. Outputs mode **requires** an aggregated inputs run for the underlying submission (coupling rule). If none exists, run inputs mode retrospectively on the assessment's source artefacts first. Only if those artefacts are genuinely unobtainable: record coupling as unevaluated, mark the output composite **provisional**, and say so prominently in every rendered view.

## 2. Workflow (both modes)

1. **Register artefacts.** Every document evaluated gets an `artefact_id` in `subject.artefacts` (name, version, date, owner). Evidence citations point here.
2. **Set the complexity tier** (§3).
3. **Score each dimension** in fixed order, using the anchors in the mode's reference file — read it before scoring:
   - Inputs: `references/rubric-inputs.md` — completeness, consistency, currency, conformity, clarity.
   - Outputs: `references/rubric-outputs.md` — coverage, traceability, consistency, conformity, actionability, clarity.
   - Clarity in both modes: score sub-test B with the claim-audit protocol in `references/clarity-specificity-protocol.md`; dimension score = min(surface clarity, specificity).
   - **Evidence rule: no citation, no score.** Every score cites ≥1 specific artefact location. If a dimension cannot be evidenced, mark it `unscorable` (treated as 0 for gating) — never guess.
4. **Emit findings** as schema objects (`references/findings-schema.json`): `severity_raw`, `effort`, assessor-facing `action`, `evidence_ref`, and (inputs mode) a `requestor_ask` translation following the rules embedded in `assets/gap-letter-template.md`. Asks must be complete standalone specifications — the rubric is never published to requestors.
5. **Aggregate.** Preferred: `python3 scripts/aggregate.py run.json` (outputs mode: add `--input-run inputs-aggregated.json`). The script validates invariants, computes letters, uplift, composite, caps, gate, and sort order. **Never hand-author computed fields.** If Python is unavailable, apply §6 manually and show the working.
6. **Render.** Assessor view always (`assets/assessor-report-template.md`); inputs mode additionally renders the requestor gap letter (`assets/gap-letter-template.md`) honouring its translation rules. Outputs mode reports patternability and the coupling result.
7. **Persist** the aggregated JSON — the inputs run is the coupling input for the later outputs run.

Worked end-to-end fixtures are in `examples/` — consult them for the expected shape before authoring a run object.

## 3. Complexity tier (context modifier — never averaged)

Tier = **highest** applicable driver (max-rule). Record which driver set it.

| Driver | T1 | T2 | T3 | T4 |
|---|---|---|---|---|
| Change depth | Config change | New component | New system | New paradigm for org |
| Trust boundaries | None | Internal zones | Third parties/tenants | Internet-facing / cross-jurisdiction |
| Data sensitivity | Public | Internal | Sensitive/regulated | Highest classification |
| Integration surface | Standalone | Few, known | Many / poorly mapped | Core shared platform |
| Tech novelty (to org) | Operated here | New here | Emerging | Unproven |
| Reversibility | Trivial rollback | Rollback with effort | Complex/costly | Practically irreversible |

Tier effects: (a) sets the evidentiary bar the anchors demand — minimum artefact set: T1 change record with before/after; T2 + architecture/data-flow diagram and integration list; T3 + threat-model-grade docs, data classification, failure modes; T4 + formal security architecture, dependency analysis, recovery plan; (b) sets expected assessment **effort tier**; (c) **severity uplift**: finding severity rises one band at T3/T4 — keyed off the **intrinsic complexity tier only**; (d) inputs mode: Conformity ≤ 1 raises the **effort tier** one step (max T4) — this drives review depth and the evidentiary bar, and **never inflates finding severity** (novelty already buys scrutiny; charging it again as severity would double-count).

## 4. Scale

0–4 with letters: **4=A Exemplary · 3=B Good · 2=C Adequate (gate pass) · 1=D Poor · 0=F Deficient/Absent.** Composite letter bands: A ≥ 3.5 · B 2.5–3.49 · C 2.0–2.49 · D 1.0–1.99 · F < 1.0.

## 5. Hard rules (apply in both modes)

- Conformity is **neutral valence**: low scores trigger scrutiny and effort uplift, never gate failure; it is **excluded from every composite mean**.
- Gating dimensions — inputs: completeness, consistency; outputs: coverage, traceability. Any gating dimension ≤ 1 → automatic return/rework regardless of composite.
- Output composite ≤ input composite + 1, and the +1 only with **evidenced independent discovery** (assessor-sourced evidence visible in the traceability chain, refs recorded). No evidence → cap is the input composite exactly. A pre-cap mean above the cap is a coupling breach — itself a finding.
- Per-dimension numerics are **suppressed in all requestor-facing output**; requestors see the composite letter and the gate decision only.

## 6. Aggregation arithmetic (manual floor rung)

When the script cannot run, compute in this exact order and show working:

1. Effective score per dimension: stated score, or 0 if unscorable/null.
2. Letters per the §4 map.
3. Effort tier (inputs): conformity ≤ 1 → effort tier = complexity tier +1 step, max T4. Drives review depth only — not severity.
4. Severity: at intrinsic **complexity** tier T3/T4 (not effort tier), uplift each finding one band (low→medium→high→critical).
5. Composite raw mean = weighted mean of dimensions with `in_composite: true` (default weights 1.0; conformity always excluded).
6. Cap = (lowest gating score) + 1. Outputs mode: also cap at the coupling limit per §5. Composite value = min(raw mean, all caps). If the raw mean exceeds the coupling cap, append a coupling breach finding (F000, dimension coupling, high/high) before sorting.
7. Composite letter from §4 bands. Hard-rule flag if any gating score ≤ 1.
8. Gate — inputs: hard rule or value < 2.0 → **return**; 2.0–2.9 → **proceed with caveats** (caveats logged, carried into the assessment's limitations section); ≥ 3.0 → **proceed**. Outputs: hard rule → **rework**; else **proceed**, noting any coupling breach.
9. Patternability (outputs): pattern_conformant requires a cited pattern_ref and conformity ≥ 3; pattern_candidate requires composite ≥ 3.0 **and** traceability ≥ 3; otherwise bespoke.
10. Sort findings: severity descending, then effort ascending, then finding_id.

## 7. Graceful Degradation Ladder

**Gate: Partially.** An AQI score is trusted as a quality verdict and feeds gate decisions. A silently degraded run — vibed arithmetic, unvalidated invariants, an unacknowledged missing coupling input — is false assurance, worse than no score. Degrade openly or not at all.
**Trigger: integrity** — every degraded rung announces itself in the rendered output.

Rungs (announce which ran):
1. **Full** — score per the rubric references; aggregate with `scripts/aggregate.py` (stdlib Python only); render both views. → validated, computed JSON.
2. **Manual aggregation** — Python unavailable: apply the §6 arithmetic by hand, show the working in the assessor report, and state explicitly that aggregation and invariant checks were manual, not automated.
3. **Uncoupled outputs run (last resort)** — the underlying submission artefacts are genuinely unobtainable, so no inputs run can be produced even retrospectively: record coupling as unevaluated and mark the composite **provisional** in every view, prominently.

**Floor (always ships):** the rubric-scored markdown assessor report with cited evidence and shown working. **What never ships:** a score whose degradations are not labelled.

## 8. Quality gates before responding

- Every scored dimension has ≥ 1 evidence citation specific enough to relocate.
- Clarity score equals min of its two sub-scores.
- No computed field was hand-authored; script output (or shown manual working) is the source of truth.
- Requestor view contains no dimension names, no rubric language, no per-dimension scores; every ask is standalone and neutral in register.
- Outputs mode names its inputs run (or carries the prominent **provisional** marking).
- Boundary scores (specificity 3/2 and 2/1) on real artefacts: flag for human review per the calibration protocol's validation status — the protocol is discriminability-tested but not yet field-validated.
