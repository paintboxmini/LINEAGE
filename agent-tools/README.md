# Agent Tools

Read `CLAUDE.md` and `memory.md` before using any of these. Kept deliberately small — the generator-layer tools that used to live here are archived in `archives/`, not deleted (most of that apparatus was never forced by a real failure, just pre-written for hypothetical ones). Design Principles, Exemplars, and the Alignment Checker were part of that same trim and got restored 2026-07-23, per the trim's own "revisit with fresh eyes after real creative mileage" condition — Drew's call: "pretty sure those were rock solid and should have stayed."

---

| Prompt | Use When |
|--------|----------|
| `repo-orientation.md` | Starting any new task — run this first |
| `compiled-crib.md` | Practical efficiency tool — read INSTEAD of full canon for routine generation; refresh at Sync when canon shifts |
| `red-team.md` | Reviewing any content for issues before it goes to canon |
| `archetypes.md` | Building a new card — a design compass, not canon; never surfaces at the table |
| `design-principles.md` | What makes content well-made — the standard red-team and alignment checks measure against |
| `exemplars.md` | Short curated list of the content that best embodies the principles — extract the principle, don't copy the specifics |
| `alignment-checker.md` | Verifying new content fits its intended context (location/faction identity, tone, system expectations) before committing — includes the Soul Pass, and the finding-the-angle questions for when it fails |
| `player-perspective.md` | Stress-testing content as a first-time player — intent-first reactions, felt danger vs. mechanical danger; refined against the first real GM playthrough |
| `mechanics-perspective.md` | Stress-testing content as a systems designer — action economy, pillar coverage, keyword pricing, table cost. Starter version; refine as it gets used |
| `story-writer-perspective.md` | Stress-testing content as a fiction writer — theme, stakes without the party, motive, restraint, voice. Starter version; refine as it gets used |
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
5. Present to Drew — Authority 1/2 content ships per The Canon Gate (`CLAUDE.md`) and lands in the post-review queue; constitutional (Authority 3) waits for his sign-off
6. Wait for next instruction
