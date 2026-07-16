# Pathfinder — the language's self-description

Every pattern language carries a **pathfinder**: a single document that says what the language is for, what it covers, what axis orders it, what it is grounded in, and where it grows next. The pathfinder is the language's scoping and grounding instrument — an author (human or agent) returning to the language months later reads it *first*, before adding or restructuring anything, and checks proposed work against it. Every strong published language carries some version of this layer (APL's preamble and *The Timeless Way*; scrumbook.org's hub pages; Group Works' template, "what we mean by pattern" page, and pattern-seeds queue); this file makes it canonical rather than optional.

## Where it lives

- **Folder shape**: `PATHFINDER.md` at the language root. Required; the validator WARNs if it is missing or if a core heading is absent.
- **Single-doc shape**: a `## Pathfinder` appendix section carrying the same content with bold sub-headings. The validator WARNs if the section is absent.

The pathfinder replaces the old optional `README.md` (an existing README can be renamed and upgraded in place).

## Sections

Core headings (validator-checked, in this order):

```markdown
# Pathfinder — <Language Name>

## Purpose & audience
## Scope
## The gradient
## Landscape & key references
## Evidence & provenance
```

Optional headings (use when they have content; the validator ignores them):

```markdown
## Conventions
## Growth queue
## Sequences
## Change log
```

What goes in each:

- **Purpose & audience** — one paragraph: what a reader should be able to *do* with this language, and who that reader is. Taken directly from intake questions 1–2.
- **Scope** — what domain territory is inside the language and, just as important, what is explicitly *outside* it (adjacent problems this language declines to cover). This is the line an expanding author checks new candidates against.
- **The gradient** — the axis that orders the language, named and justified: spatial scale, process/time order, organisational scope, or another monotone axis of descent (see `language-structure.md` § The gradient). State the bands and their number ranges. A language that cannot state its gradient here does not have one.
- **Landscape & key references** — the neighbouring works this language is grounded in and differentiated from: other pattern languages in or near the domain, the source literature, and any exemplar whose conventions were borrowed. Two purposes: a new author can judge whether a candidate pattern is already better covered elsewhere, and a reviewer can check the language's claims against its sources.
- **Evidence & provenance** — where the patterns came from: what material was mined (retros, decision logs, interviews, fieldwork), when, and by whom. Note the overall confidence honestly — a language born entirely at confidence 0 is fine, but say so here.
- **Conventions** — anything local: confidence semantics if extended, numbering-band map, naming style, status workflow.
- **Growth queue** — candidate patterns that were parked: name, one-line tension, why parked. This is the language's backlog (Group Works calls these "pattern seeds"); growth starts here, not from a blank page.
- **Sequences** — the named sequences published with the language (see `language-structure.md` § Sequences), one line each on when to use which.
- **Change log** — dated one-liners for structural events: bands added, patterns split/merged/renumbered, validation milestones.

## How it is produced and used

- **Create**: the intake answers (`intake.md`) *are* the pathfinder — write `PATHFINDER.md` immediately after intake sign-off, before any pattern bodies.
- **Add / update / expand**: read the pathfinder first. A candidate pattern that fails the Scope test or cannot be placed on the declared gradient gets parked in the Growth queue or rejected — not shoehorned in.
- **Validate**: the qualitative pass checks the language *against its own pathfinder* — scope drift, gradient violations, unacknowledged sources — not just against generic doctrine.
- **Growth**: when a parked candidate is promoted to a pattern, remove it from the Growth queue and note the promotion in the Change log.

Keep it under two pages. A pathfinder that nobody re-reads is shelfware; brevity is what keeps it load-bearing.
