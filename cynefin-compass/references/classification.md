# Classification procedure

Use this file for steps 1 to 3 of the process in SKILL.md: gate, decompose, classify.
The answers go in the `procedure_answers` field of each piece.
`scripts/validate_assessment.py` checks that the domain matches the answers.

## 1. The gate

Ask: **would naming the domain change what we do next?**

| Answer | Action |
|---|---|
| No. The task is bounded and the path is known. | Set `gate.changes_approach` to `false`. State the reason. Do the task. Stop. |
| Yes. The way to proceed is in question. | Set it to `true`. Continue. |

Signs that the gate should be `true`:
- The user asks for a plan, and the outcome depends on how people or markets react.
- The team argues about method (analyse more, or try something).
- Something urgent is happening and the team is about to hold a long analysis.
- Work that was "routine" starts to produce surprises.

Signs that the gate should be `false`:
- One person can do the task with known steps.
- The user asks for a code change, a rename, a format change or a lookup.
- The user only wants a definition of Cynefin. Answer the question. Do not assess.

## 2. Decompose

Most real situations hold more than one problem. Before you classify:

1. List the parts that could be handled by different people or at different times.
2. If you list 2 or more, set `is_single_problem` to `false`. Classify each part.
3. If you cannot classify a part (all four answers are no), the part is **Confused**.
   Break it into smaller parts. Classify those.

Confused is never a final result. The validator rejects it.

## 3. The four questions

Answer in this order. Stop at the first **yes**. The validator uses the same order.

| # | Field in `procedure_answers` | Question | If yes |
|---|---|---|---|
| Q1 | `active_crisis` | Is harm happening now, and is nobody sure what causes it? | **Chaotic** |
| Q2 | `known_practice_applies` | Can a known practice be applied without change? | **Clear** |
| Q3 | `expert_can_determine_before_acting` | Can an expert find cause and effect by analysis, before we act? | **Complicated** |
| Q4 | `hindsight_only` | Can cause and effect be seen only after we act, in hindsight? | **Complex** |
| none | all four are `false` | | **Confused**. Decompose. |

Answer all four fields every time, even after a yes. This makes the answers auditable.

If you choose a domain that the answers do not give, add `override_reason`
(6 words or more). Use it rarely. A frequent override means the questions need work.

## Boundary tables

### Complicated or Complex? (the most common error)

| Test | Complicated | Complex |
|---|---|---|
| Would two good experts reach the same answer? | Yes | No. They disagree, and both can be right. |
| Has a similar case been solved and recorded? | Yes | No, or the result depended on the people involved. |
| Does the system react to our action? | No. It stays still while we analyse. | Yes. People, markets or teams adapt. |
| What does more analysis give? | A better answer | A better guess. Only action gives data. |

If most answers are in the Complex column, **do not write a plan**. Write probes.

### Clear or Complicated?

| Test | Clear | Complicated |
|---|---|---|
| Is there a checklist or runbook that fits? | Yes, and it is current. | It exists but needs expert judgement to apply. |
| Can a new team member do it after training? | Yes | No. It needs years of skill. |

### Complicated, Complex or Chaotic when under pressure?

Time pressure alone does not make a problem Chaotic. Chaotic needs **active harm and no
known cause**. A deadline on a knowable problem is still Complicated.

## Transitions

Domains change. Record the triggers in `reclassify_triggers`.

| Move | Meaning | Typical trigger |
|---|---|---|
| Chaotic → Complex | Stable enough to learn. | Harm has stopped. The cause is not yet known. |
| Complex → Complicated | Patterns have formed. | Probes give a repeatable result that experts can analyse. |
| Complicated → Clear | Knowledge is codified. | A runbook is written and tested. |
| Clear → Chaotic | **The cliff.** | Complacency, or a step that was skipped, causes a sudden failure. |
| Any → Confused | We lose track. | Two kinds of work are mixed together. Split them. |

For every **Clear** piece, `boundary_risk` is required. Say how complacency could push
the work over the cliff.

## Constraints (for Complex pieces)

Probes find out which constraints enable the system and which govern it.
- **Governing constraints** fix behaviour (rules, tools that force one path). They suit Clear and Complicated work.
- **Enabling constraints** shape behaviour without fixing it (norms, guardrails, shared goals). They suit Complex work.
- **No constraints** means Chaotic. Add one stabilising constraint first.

## Lint rules

`scripts/validate_assessment.py` enforces these. FAIL stops the process. WARN is advice.

| Rule | Severity |
|---|---|
| Schema fields present and typed (see `assessment-schema.json`). | FAIL |
| `gate.changes_approach` false means `pieces` is empty. True means 1 or more pieces. | FAIL |
| `is_single_problem` agrees with the number of pieces. | FAIL |
| `procedure_answers` gives the domain, or `override_reason` explains it. | FAIL |
| All four answers `false` (Confused). Decompose. | FAIL |
| `approach.sequence` matches the domain. | FAIL |
| Complex piece has 1 to 3 probes. | FAIL |
| Every probe has `reversible: true`, a cost bound, a signal, amplify and dampen rules, a time box. | FAIL |
| Phased-plan words (`phase 1`, `roadmap`, `gantt`, `big bang`, `comprehensive plan`) on a Complex piece. | FAIL |
| Chaotic piece has one `stabilising_action` (a text value) and `sense_after`. | FAIL |
| Clear piece has `practice`, no probes, and a `boundary_risk`. | FAIL |
| Complicated piece has `analysis_needed` and `experts`. | FAIL |
| Evidence is a generic label (`it is complex`, `many stakeholders`). | FAIL |
| Evidence item has fewer than 6 words. | WARN |
| `second_reading.domain` differs from the primary. Tipping condition has 4 or more words. | FAIL |
| At least one `reclassify_triggers` item. | FAIL |
| `stabilising_action` has more than 30 words. | WARN |
