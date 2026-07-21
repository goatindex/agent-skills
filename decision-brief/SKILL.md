---
name: decision-brief
description: Produce a prioritised decision brief / advisory summary with a recommendations table, per-option narrative tradeoffs, and dive-deeper + open-decisions menus. Use when the user asks for analysis, options, architecture trade-offs, or any "what should I do about X" question and has NOT said build/go/just-do-it.
---

# /decision-brief

Trigger: "decision brief", "advisory", "what are my options", "help me think through",
"recommendations + tradeoffs", or any analysis request where the user hasn't said "build" /
"go" / "just do it".

---

## Output structure

### 1. Framing (one line)
State the question being answered and why it matters now. State any assumptions. No preamble.

### 2. Prioritised recommendations table

| Rank | Option | Verdict | Tradeoff | Decision needed? |
|------|--------|---------|----------|------------------|
| 1 | … | Recommended / Viable / Avoid | upside vs. cost or risk | go (no decision) / decision needed |

- Rank by best fit for the userd stated goal.
- Verdict ∈ **Recommended**, **Viable**, **Avoid**.
- Tradeoff: upside and cost/risk, the most meaningful tensions, separated by " vs. ".
- Decision-needed tag: `go (no decision)` if it can proceed without further input;
  `decision needed` if the user must choose or a condition must be met first.

### 3. Per-option narrative
For each row: one short paragraph — what it is in plain language, why it ranks where it
does, and the explicit tradeoff (what you gain, what you give up or risk).

### 4. Dive deeper menu
Numbered, one line each — follow-on analyses available on request.

### 5. Further investigation / open decisions
Items needing more info or an explicit user decision. Tag each `go (no decision)` or
`decision needed`. Always present, even if short.

---

## Worked example

**Framing:** Which test-runner should the harness use given the disk constraints on C:?

| Rank | Option | Verdict | Tradeoff | Decision needed? |
|------|--------|---------|----------|------------------|
| 1 | pytest, tmp on D: | Recommended | richest fixtures, fast vs. needs TEMP/TMP override | go (no decision) |
| 2 | unittest (stdlib) | Viable | zero install vs. verbose, weak parametrise | go (no decision) |
| 3 | nose2 | Avoid | familiar API vs. effectively unmaintained | decision needed |

**pytest, tmp on D::** `tmp_path` honours TEMP/TMP, so redirecting them to `D:\tmp` keeps
temp writes off the near-full C:. Richest fixtures, fastest parametrised runs. Tradeoff:
env vars must be set first — already handled by the harness disk gotcha.

**unittest:** ships with Python, fine for simple cases. Tradeoff: fixture boilerplate is
heavier; no clean parametrise without `subTest`.

**nose2:** familiar nose syntax. Tradeoff: maintenance-mode project — avoid for new work.

**Dive deeper:** 1. pytest — minimal `conftest.py` enforcing the D: tmp dir · 2. unittest —
equivalent `subTest` pattern.

**Open decisions:** TEMP/TMP already set → `go (no decision)` · pin a min pytest version →
`decision needed`.

---

## Usage notes
- Do NOT jump to implementation unless the user says "build" / "go" / "write the code".
- Keep the table to options that matter; omit noise.
- Match users register: succinct, plain, no filler.
