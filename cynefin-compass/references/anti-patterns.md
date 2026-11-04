# Misclassification anti-patterns

Each row is a wrong pairing of domain and approach. Check your result against this table
before you write the assessment.

| Pattern | Wrong move | Signal that you are doing it | Fix |
|---|---|---|---|
| **Complex treated as Complicated** (the common one) | Write a full plan or ask for the expert answer. | Words like phase, roadmap, "the right design". Outcome depends on how people react. | Write 1 to 3 probes. The validator fails phased-plan wording. |
| **Chaotic treated as Complicated** | Hold a long analysis during a crisis. | Harm is active and the meeting is about root cause. | Take one stabilising action now. Analyse after. |
| **Clear treated as Complex** | Run experiments on a solved problem. | A runbook exists but the team wants to "explore options". | Apply the practice. Do not gold-plate. |
| **Complicated treated as Clear** | Apply a checklist to a problem that needs expert judgement. | The checklist does not fit, and the team forces it. | Get the right experts. Analyse first. |
| **Clear drifts to Chaotic** | Stop looking because "it always works". | No owner, no check, no review date. | Name the complacency risk in `boundary_risk`. Add a check. |
| **Label without consequence** | Name the domain. Work as before. | The next step is the same as before the assessment. | Use the gate. If the step does not change, skip the skill. |
| **False precision** | State one domain with full certainty. | No second reading. Evidence is generic. | Give a second reading and a tipping condition. Use specific evidence. |
| **Probe that is a pilot** | Call a large, hard-to-undo rollout a "probe". | Cost is large. It cannot be switched off. | Make it smaller until it is reversible and bounded. |
| **Over-triggering** | Run the framework on bounded work. | A rename, a lookup or a format change gets a report. | Set `gate.changes_approach` to false. |
