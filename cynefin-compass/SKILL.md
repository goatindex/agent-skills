---
name: cynefin-compass
description: Classify a situation with the Cynefin framework (Clear, Complicated, Complex, Chaotic) and turn the result into the next concrete step. Use when the way to proceed is in question - a plan is requested for an unpredictable problem, a team argues about analysis versus experiment, a crisis needs stabilising, or routine work starts to surprise. Skip it for bounded tasks with a known path. Produces a validated JSON assessment and an optional markdown report.
---

# Cynefin Compass

Cynefin is a router. Each domain needs a different way of working.
The costly mistake is the wrong approach for the domain.
The common error is to treat a **Complex** problem as **Complicated**:
a full plan, when small experiments are the right move.

The skill must **change what happens next**. If it does not, skip it.

## Process

Follow these steps in order. Scripts are in `scripts/`. Run them from this skill folder.

1. **Gate.** Decide if naming the domain changes the next step.
   Use `references/classification.md`, section 1.
   - If no: set `gate.changes_approach` to `false`, give the reason, do the task, stop.
2. **Decompose.** List the separate problems in the situation.
   Use `references/classification.md`, section 2.
3. **Classify each piece.** Answer the four questions in order
   (`references/classification.md`, section 3). Write all four answers.
   Check the result against `references/anti-patterns.md`.
4. **Choose the approach.**
   - Clear: apply the known practice. Do not gold-plate.
   - Complicated: name the analysis and the experts.
   - Complex: write 1 to 3 safe-to-fail probes (`references/probes.md`). Do not write a plan.
   - Chaotic: write one stabilising action to take now. Defer analysis.
5. **Write the assessment** as JSON. The contract is `references/assessment-schema.json`.
   Examples: `examples/*.json`.
6. **Validate.** Run:
   `python3 scripts/validate_assessment.py assessment.json`
   - FAIL: fix the assessment, run again. Do not report a result that fails.
   - WARN: read it. Fix it if it is a real weakness.
7. **Render** (full mode, or when the user wants a saved report):
   `python3 scripts/render_report.py assessment.json -o report.md`
   Then run `python3 scripts/lint_report.py report.md`. Fix any FAIL.
8. **Log** (optional, for tuning):
   `python3 scripts/gate_log.py append assessment.json`
   Review with `python3 scripts/gate_log.py summary`.
9. **Report** to the user: the domain per piece, the second reading, and the next step.
   End with the changed next step. Do not explain the framework.

## Modes

| Mode | When | What you do |
|---|---|---|
| **Lite** (default) | One person, a direct question. | Do steps 1 to 4 in a few sentences. If you can write the JSON cheaply, run step 6 too. |
| **Full** | High stakes, contested, or several people must agree. Or the user asks for a report. | Do all steps. For group work, add `references/facilitation.md`. |

Lite replies must still give: the domain, the evidence, a second reading, and the next step.

## Rules

- Give a second reading for every piece. Boundaries are fuzzy. Say what would tip the call.
- Use evidence from this situation. Do not use generic theory.
- Classify the user's own request when it is relevant. If they ask for a plan and the problem
  is Complex, say so first and offer probes.
- A Clear piece needs a `boundary_risk`: Clear and Chaotic touch at a cliff.
- "Confused" is not a result. Decompose the situation until each piece has a domain.
- Do not send the report as the only output. Give the user the next step in plain words.

## Files

| File | Purpose |
|---|---|
| `references/classification.md` | Gate, decomposition, the four questions, boundary tables, transitions, lint rules |
| `references/anti-patterns.md` | Wrong domain and approach pairs, with fixes |
| `references/probes.md` | Probe checklist and examples |
| `references/facilitation.md` | Group sense-making method |
| `references/assessment-schema.json` | Input contract for the scripts |
| `scripts/validate_assessment.py` | Contract and lint check (exit 1 on FAIL) |
| `scripts/render_report.py` | JSON to markdown report |
| `scripts/lint_report.py` | Report format check |
| `scripts/gate_log.py` | JSONL run log and summary |
| `evals/` | Gate and classification cases for regression checks |
