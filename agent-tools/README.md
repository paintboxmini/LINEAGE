# Agent Tools

Read `CLAUDE.md` and `memory.md` before using these. This directory contains the small set of living tools used during design work. Historical harness experiments and retired tooling live in `archives/`.

---

| Prompt | Use When |
|--------|----------|
| `repo-orientation.md` | Starting any new task — run this first |
| `compiled-crib.md` | Practical efficiency tool — read INSTEAD of full canon for routine generation; refresh at Sync when canon shifts |
| `red-team.md` | Reviewing any content for issues before it goes to canon |
| `archetypes.md` | Building a new card — a design compass, not canon; never surfaces at the table |
| `design-principles.md` | What makes content well-made — the standard red-team and alignment checks measure against |
| `alignment-checker.md` | Verifying new content fits its intended context (location/faction identity, tone, system expectations) before committing |
| `player-perspective.md` | Stress-testing content as a first-time player — intent-first reactions, felt danger vs. mechanical danger |
| `mechanics-perspective.md` | Stress-testing content as a systems designer — action economy, pillar coverage, keyword pricing, table cost |
| `story-writer-perspective.md` | Stress-testing content as a fiction writer — theme, stakes without the party, motive, restraint, voice |
| `card-compression.md` | Refactoring a card set like code — find components that don't pull weight, recombine into denser cards; the sim proves equivalence, this pass picks the winner |

---

## Automatic Triggers

| Trigger | Prompt |
|---------|--------|
| Start of any session or new task | `repo-orientation.md` |
| Any card, encounter, or quest content drafted (before presenting) | `red-team.md` |

---

## Workflow

1. Orient (`repo-orientation.md`)
2. Do the work — read the relevant canon, think it through, write it
3. **Clarify before executing** when something is genuinely ambiguous (see `CLAUDE.md`, Translation Principle) — not by default, only when the evidence doesn't pick a side
4. Run `red-team.md` on anything going to canon
5. Apply the current Canon Gate in `CLAUDE.md`
6. Present the finalized result and await the next instruction
