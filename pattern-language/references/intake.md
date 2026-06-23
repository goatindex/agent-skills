# Intake — creating a new pattern language from scratch

Run this before writing anything. Ask in one or two batches, not one long interrogation; infer what the conversation already answers. Get explicit sign-off on the **scale structure and seed pattern list** before drafting pattern bodies — that is the cheap moment to change course.

## Questions

1. **Domain and purpose.** What is this language about, and what should someone be able to *do* with it? (Design things? Run things? Teach things?)
2. **Audience.** Who reads it — practitioners, newcomers, decision-makers? This sets the voice and how much evidence each pattern needs.
3. **The scale gradient.** What is "large" and what is "small" here? Elicit 3–5 scale levels from whole-system down to smallest repeatable act. If the user can't articulate it, propose one from the domain and iterate.
4. **Seed problems.** What recurring tensions does the user already know? Capture 5–15 raw problem statements in their words. Each candidate must pass the forces test (a tension, not an absence) before becoming a pattern — help reformulate the ones that fail.
5. **Evidence base.** What has actually been tried? This drives confidence ratings; a language born entirely at confidence 0 is fine, but say so honestly in the README.
6. **Existing material.** Documents, retros, runbooks, lore to mine? Mining real material produces better patterns than brainstorming.
7. **Name.** Short, owned by the user.

## From answers to seed language

1. Propose the scale groups with number bands (gaps between bands — see `language-structure.md`).
2. Map each seed problem to a scale, name the candidate pattern (2–5 word noun phrase), assign a number.
3. Sketch the link structure: for each candidate, which larger patterns does it complete; which smaller ones complete it? A seed language should already be a connected network — if a candidate floats free, either find its links or park it.
4. **Present this as a table for approval**: number, name, scale, one-line problem, proposed links, proposed confidence. Iterate here.
5. Only then write pattern bodies per `pattern-form.md`, largest scale first, plus `index.md`.
6. Validate (script or manual checklist) and report.

## Sizing

5–15 patterns is a healthy seed. Resist completeness: a pattern language is grown piecemeal, and shipping a small connected core that the user starts *using* beats a large speculative one. Record parked candidates in the README under "Candidate patterns" so growth has a queue.
