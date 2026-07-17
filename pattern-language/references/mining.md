# Mining — from real material to candidate patterns

Mining is how a language becomes *true* rather than merely well-formed. Everything downstream — form, links, validation — can only guarantee structure; whether the patterns describe reality is decided here. The doctrine: **mine, don't invent.** A pattern harvested from what actually happened, with known uses attached, beats a brainstormed one every time — and the modern pattern literature (Iba's mining pipeline, the PLoP known-uses discipline) treats extraction as the core craft, not a preliminary.

Mining runs at two moments:

- **Create** — the first dig, briefed by the intake (below), before any pattern body is written.
- **Re-entrant passes** — every later Add/Expand should begin with a small mining pass over whatever accumulated since the last one (new retros, new decision-log outcomes, new postmortems). Growth is evidence-driven by default; brainstorming is the fallback, not the norm.

## The brief comes from intake

Intake questions 5–7 are the mining brief, and the two source classes they surface do different work:

- **Internal material** (Q5–6: retros, decision logs / ADRs, runbooks, postmortems, meeting notes, lore) generates **candidates** — tensions the org has actually felt, in its own words.
- **Public material** (Q7 landscape: published pattern languages nearby, open-source practice, domain literature) generates **corroboration** — independent known uses. Three instances from inside one org are not fully independent; the rule of three wants at least some daylight between sources. A candidate mined internally and then found alive in two unrelated public sources is a far stronger claim than either alone, and is what justifies ✻✻.

Keep the classes separate in your notes: a candidate that exists *only* in public sources is probably someone else's pattern to cite in the pathfinder's landscape, not yours to write.

## The pipeline

1. **Harvest.** Sweep the material for fragments — moments where something worked, failed, or was fought over. Capture each as one line in the speaker's own words with a source pointer ("we stopped losing new starters when X sat them next to Y — 2024 retro"). Do not generalise yet. A worthwhile dig yields 20–60 fragments; fewer than 10 means the corpus is thin and the language should say so in its pathfinder.
2. **Cluster by tension, not vocabulary.** Group fragments that are pulled by the *same conflict of forces*, even when they use different words; keep apart fragments that share words but not forces (two "onboarding" complaints may be one tension about knowledge transfer and another about workload). This is the judgement-heavy step — surface-vocabulary clustering is the characteristic failure of rushing it.
3. **Forces-test each cluster.** State the tension the cluster keeps circling as "people need A, but B makes A costly." Clusters that only yield an absence ("we have no X") are either reformulated to the underlying conflict or dropped.
4. **Name the candidates.** A 2–5 word evocative noun phrase per surviving cluster (`pattern-form.md` § Naming), plus its strongest fragments as proto-known-uses.
5. **Route.** Candidates that fit the pathfinder's scope and gradient go to the intake seed table (or, on a re-entrant pass, to Add). Candidates that are real but out of scope or premature go to the pathfinder's **Growth queue** with a one-line tension. Nothing harvested is silently discarded.
6. **Write back provenance.** Update `PATHFINDER.md` § Evidence & provenance: which corpora were dug, roughly how many fragments, which clusters became patterns vs queue entries — and **which sources yielded nothing**. The null result stops the next pass re-mining the same seam.

## Re-entrancy

The provenance section is the diff point. Record a resumption marker per corpus ("decision log mined through 2026-06") so a later pass — possibly by a different author or a smaller-context session — mines only the increment and never re-reads the historical corpus. When a Growth-queue candidate is promoted, note it in the pathfinder's Change log; when outcome evidence accumulates for an existing pattern, the mining pass is also the moment to move its confidence (in either direction — see `pattern-form.md` § Confidence calibration).

## Sizing and honesty

Mining does not have to fill the seed table in one dig. Five well-evidenced candidates beat fifteen speculative ones; the Growth queue exists so restraint costs nothing. And if the evidence base is genuinely thin — a young org, a new practice — write the language anyway at confidence 0, but let the pathfinder say plainly that it is a hypothesis awaiting its first season of use.
