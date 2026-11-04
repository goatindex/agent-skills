# Designing safe-to-fail probes

A probe is a small action that you take to learn how the system reacts.
It is not a pilot, and it is not the first phase of a plan.

## Checklist (every probe)

The validator checks the fields marked with `*`.

- [ ] **Action** *: one thing a person can do this week.
- [ ] **Reversible** *: you can undo it quickly. If not, make it smaller.
- [ ] **Bounded cost** *: state the maximum cost in time, money or users.
- [ ] **Why it is safe to fail** *: say what limits the damage.
- [ ] **Signal** *: one thing you will observe. Say where you will see it.
- [ ] **Amplify if** *: the result that makes you do more of it.
- [ ] **Dampen if** *: the result that makes you stop.
- [ ] **Time box** *: when you will look at the signal.
- [ ] **Owner**: one named role.
- [ ] **Contrast**: where possible, run probes that disagree with each other.
  If every probe tests the same theory, you learn less.

Use 1 to 3 probes. More than 3 is a plan.

## Weak and strong probes

| Weak | Strong |
|---|---|
| "Pilot the new process in one region." (large, slow, hard to undo) | "Use the new checklist for 5 releases on one team. Switch back if two releases are late." |
| "Survey users." (no signal, no rule) | "Ask one question at the drop point. Amplify if one theme has over 30% of answers." |
| "Improve culture." (no action) | "Hold a 15-minute retrospective with one team. Amplify if the team asks to repeat it." |

## Examples by context

### Software delivery
- Release behind a feature flag to 5% of users. Signal: error rate and task completion.
- Pair two engineers on the slow area for one week. Signal: cycle time of that area.
- Remove one approval step for low-risk changes for one month. Signal: incidents and lead time.

### Security
- Run a one-hour phishing-report drill with one team. Signal: time to first report.
- Move one low-risk service to short-lived credentials. Signal: failures and support requests.
- Add a warn-only policy rule for two weeks before it blocks anything. Signal: false-positive rate.

### Organisation and change
- Let one team choose its own meeting rhythm for a quarter. Signal: team self-report and output.
- Rotate the facilitator in one forum for four weeks. Signal: who speaks, and decisions made.
- Offer a voluntary drop-in clinic instead of a mandatory training. Signal: attendance and repeat visits.

## After the time box

1. Read the signal.
2. Apply the amplify or dampen rule. Do not argue with a rule you wrote earlier.
3. If the result is stable and repeatable, the piece may now be Complicated. Reclassify.
4. If the result surprised you, stay Complex. Write the next probe.
