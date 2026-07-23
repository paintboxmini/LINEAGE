# Unresolved Concerns

A scannable index of everything currently open that will eventually need a decision or a fix — the things that otherwise sit buried in `memory.md`'s prose (Recently Shipped entries, Standing Reasoning, Pending Propagation) until someone rereads the whole file. **This is an index, not a third home**: each entry is a line or two plus a pointer to where the full trail lives. Add a line when a concern gets flagged; delete the line when it's resolved (`memory.md` keeps the history — this file only ever shows the present).

**What does NOT belong here**: deliberately open questions. This repo keeps quiet doubts and unresolved world-hooks on purpose (`CLAUDE.md`: "the open questions are on purpose") — who bears the Storm Seat, what the Ferryman reads, what's at the Coil's center. Those are design, not debt. This file is for actual debt: flagged issues, known imbalances, deferred decisions that shouldn't be forgotten.

Also not here: **Pending Propagation** (operational staleness — print sheets, sim sync) stays in `memory.md` where the Sync workflow already looks for it. Entries below may point there, but the ledger itself doesn't move.

---

## Mechanics & Balance

- **Masaharu's Red column has a 1-card deck overcount** (4 total vs. Body 3) — predates this repo's sessions, flagged rather than silently trimmed since the extra card may be a deliberate pick. Drew's call which card goes. *Trail: memory.md, the STEADY HAND entry.*
- **Immunity is deliberately excluded from the Positive Status Effects list** — flagged at creation, never decided. Matters because "remove all Positive Status Effects" cards (LEVEL THE FIELD, WAITING GAME) currently can't touch it. *Trail: memory.md, the BARRIER/LAST RESORT entry.*
- **DOUBLE DOWN is canon text with zero sim support, on purpose** — Drew's call, pending real playtesting before the nested-second-attack mechanic gets designed at all. Do not wire it up without him. *Trail: memory.md, Pending Propagation.*
- **Even-matchup PvP mirrors are far more lethal than the 1-death-per-20-sessions target** (45–62% chance of a death per fight in symmetric 3v3s) — open which lever is wrong: the 25% down-hit rate, or symmetric-mirror testing itself (no healer roles, no monster-side decks). *Trail: memory.md, Standing Reasoning.*
- **Initiative Shift cards may be underpowered** — the live 2v2 ran in the format where Shift matters most (4 combatants) and both sides organically passed on it entirely. Drew's plan: live tests with deliberately pillar-invested decks. *Trail: memory.md, Standing Reasoning (the 4-seats-is-the-peak entry).*
- **The Initiative Wheel slots/clamp rework is simmering, unresolved** — current wheel rules still govern play; Drew may bring back a replacement whole. Cards stay within Shift ±1–3 until then. *Trail: memory.md Active Pending Threads; `archives/initiative-slots.md`.*
- **The Patient Host's kit reads undertuned relative to its Mind 8/Body 6/Soul 10 stat line** — and the scaled-party test that would prove it can't be run honestly until an item/gear progression system exists. Both halves parked by Drew ("let the host run his inn in peace. for now"). *Trail: memory.md, Pending Propagation (the parked entry).*
- **The Greater Stonecoil has no balanced encounter build** — deliberate for now; a party forcing the Deep Stream crossing gets a live GM call or a pause-and-build. Becomes real debt the moment a campaign approaches the Old Flow Channel. *Trail: `quests/hollow-below-briarwatch.md`, Deep Stream Channel; memory.md.*
- **`rules/combat-example.md`'s draw-sequence pedagogy is stale** — its narrative still shows the old random-shuffle Injury behavior, not bottom-insertion. Needs a real rewrite pass, not a word swap. *Trail: memory.md, Pending Propagation.*

## Canon & World

- **Fog Goggles is labeled an Artifact but names no Seat** — `rules/equipment.md` now defines Artifacts as Seat-aligned; the Goggles predate that and don't obviously tie to any Seat. Reconcile next time the Fog Basin gets attention. *Trail: `rules/items.md`, Fog Basin section.*
- **The Underground Bazaar has zero mechanical items** — and its memory/secret/debt economy means standard gold pricing probably shouldn't just be bolted on. Needs its own pricing logic thought through first. *Trail: `rules/items.md`, Underground Bazaar section.*
- **The Carrion Feather's trigger doesn't fire in the Washed Ashore continuity** — its Source line says "upon delivering the party to Briarwatch," which doesn't happen in that opening (Aege leaves the Roadhouse ahead of them). Needs its own moment if it exists there at all. *Trail: `quests/washed-ashore.md`.*
- **Lily, Moth, and Hess & Cob are flagged as next-tier character-file candidates** — each already has real characterization duplicated or split across location files, same pre-split state Kess and Corvel were in. Drew's call whether/when. *Trail: memory.md, the Kess/Corvel entry.*

## Process

- **The keyword usage counts in `rules/card-glossary.md` are a dated snapshot** (2026-07-18) — self-labeled as such, but cards have moved substantially since (the dice sweep, new Gambler cards, Vulnerable). Recount at next Sync rather than trust. *Trail: the glossary's own header note.*
