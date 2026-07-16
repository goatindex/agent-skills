# Intake — creating a new pattern language from scratch

Run this before writing anything. Ask in one or two batches, not one long interrogation; infer what the conversation already answers. Get explicit sign-off on the **scale structure and seed pattern list** before drafting pattern bodies — that is the cheap moment to change course.

## Questions

1. **Domain and purpose.** What is this language about, and what should someone be able to *do* with it? (Design things? Run things? Teach things?)
2. **Audience.** Who reads it — practitioners, newcomers, decision-makers? This sets the voice and how much evidence each pattern needs.
3. **The gradient.** What axis orders this language — spatial scale, organisational scope, process/time order? What is "large" and what is "small" on it? Elicit 3–5 bands from whole-system down to smallest repeatable act. If the user can't articulate it, propose one from the domain and iterate. (See `language-structure.md` § The gradient — the axis need not be size, but it must be monotone and declared.)
4. **Seed problems.** What recurring tensions does the user already know? Capture 5–15 raw problem statements in their words. Each candidate must pass the forces test (a tension, not an absence) before becoming a pattern — help reformulate the ones that fail.
5. **Evidence base.** What has actually been tried? This drives confidence ratings; a language born entirely at confidence 0 is fine, but say so honestly in the pathfinder.
6. **Existing material.** Documents, retros, decision logs, runbooks, lore to mine? Mining real material produces better patterns than brainstorming.
7. **Landscape.** What neighbouring pattern languages, source literature, or exemplars already cover parts of this ground? These become the pathfinder's key references — and the check against reinventing a covered pattern.
8. **Name.** Short, owned by the user.

## From answers to seed language

1. Propose the scale groups with number bands (gaps between bands — see `language-structure.md`).
2. Map each seed problem to a scale, name the candidate pattern (2–5 word noun phrase), assign a number.
3. Sketch the link structure: for each candidate, which larger patterns does it complete; which smaller ones complete it? A seed language should already be a connected network — if a candidate floats free, either find its links or park it.
4. **Present this as a table for approval**: number, name, scale, one-line problem, proposed links, proposed confidence. Iterate here.
5. On sign-off, **write `PATHFINDER.md` first** (see `references/pathfinder.md`) — the intake answers map directly onto its sections: purpose/audience (Q1–2), gradient (Q3), evidence/provenance (Q5–6), landscape (Q7), parked candidates into the Growth queue.
6. Then write pattern bodies per `pattern-form.md`, largest scale first, plus `index.md`.
7. Validate (script or manual checklist) and report.

## Sizing

5–15 patterns is a healthy seed. Resist completeness: a pattern language is grown piecemeal, and shipping a small connected core that the user starts *using* beats a large speculative one. Record parked candidates in `PATHFINDER.md` under **Growth queue** so growth has a backlog.
