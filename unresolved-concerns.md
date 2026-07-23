# Unresolved Concerns

A scannable index of everything currently open that will eventually need a decision or a fix — the things that otherwise sit buried in `memory.md`'s prose (Recently Shipped entries, Standing Reasoning, Pending Propagation) until someone rereads the whole file. **This is an index, not a third home**: each entry is a line or two plus a pointer to where the full trail lives. Add a line when a concern gets flagged; delete the line when it's resolved (`memory.md` keeps the history — this file only ever shows the present).

**What does NOT belong here**: deliberately open questions. This repo keeps quiet doubts and unresolved world-hooks on purpose (`CLAUDE.md`: "the open questions are on purpose") — who bears the Storm Seat, what the Ferryman reads, what's at the Coil's center. Those are design, not debt. This file is for actual debt: flagged issues, known imbalances, deferred decisions that shouldn't be forgotten.

Also not here: **Pending Propagation** (operational staleness — print sheets, sim sync) stays in `memory.md` where the Sync workflow already looks for it. Entries below may point there, but the ledger itself doesn't move.

---

## Mechanics & Balance

- **DOUBLE DOWN is canon text with zero sim support, on purpose** — Drew's call, pending real playtesting before the nested-second-attack mechanic gets designed at all. Do not wire it up without him. *Trail: memory.md, Pending Propagation.*
- **Even-matchup PvP mirrors are still more lethal than the 1-death-per-20-sessions target, though the mechanism fix already landed.** Targeting was reworked (random pick, pile on, drop on collapse) — death-occurred rate dropped from 45–62% to 41–48% in symmetric 3v3 mirrors, real progress, still nowhere near target. Drew's own caveat: mirrors between equal-ish parties were only ever testing the mechanism's direction, not validating the number. Open until real monster-vs-party encounters (CTR-calibrated deck vs. an actual party with a healer role) exist to test against properly. *Trail: memory.md, Standing Reasoning (the team-targeting rework entry).*
- **Initiative Shift cards may be underpowered** — the live 2v2 ran in the format where Shift matters most (4 combatants) and both sides organically passed on it entirely. Drew's plan: live tests with deliberately pillar-invested decks. *Trail: memory.md, Standing Reasoning (the 4-seats-is-the-peak entry).*
- **The Initiative Wheel slots/clamp rework is simmering, unresolved** — current wheel rules still govern play; Drew may bring back a replacement whole. Cards stay within Shift ±1–3 until then. *Trail: memory.md Active Pending Threads; `archives/initiative-slots.md`.*
- **The Patient Host: two separate open threads, not one.** (1) Its signature kit (control/Initiative-Shift-flavored) versus its Mind 8/Body 6/Soul 10 stat line is a tuning question independent of whether it wins fights — it does win, decisively (84–91% vs. baseline parties), but that's driven heavily by the raw CTR gap (24 vs. 9), which doesn't by itself prove the *kit* is tuned right for stats that size. (2) A scaled-party test that would settle it can't be run honestly without an item/gear progression system, which doesn't exist yet. Both parked by Drew ("let the host run his inn in peace. for now"). *Trail: memory.md, Pending Propagation (the parked entry).*
- **The Greater Stonecoil has no balanced encounter build** — deliberate for now; a party forcing the Deep Stream crossing gets a live GM call or a pause-and-build. Becomes real debt the moment a campaign approaches the Old Flow Channel. *Trail: `quests/hollow-below-briarwatch.md`, Deep Stream Channel; memory.md.*
- **`rules/combat-example.md`'s draw-sequence pedagogy is stale** — its narrative still shows the old random-shuffle Injury behavior, not bottom-insertion. Needs a real rewrite pass, not a word swap. *Trail: memory.md, Pending Propagation.*
- **Immunity joined Positive Status Effects (`rules/card-glossary.md`), but the sim's shared status-transfer/strip code (`_transfer_statuses`/`_strip_one_status` in `content.py` — used by WAITING GAME, DRAIN, UNMAKE, LEVEL THE FIELD) still only knows Deadly/Resist/Evade/Protect.** Whether Immunity should be stealable/copyable/strippable by those specific cards is a real design question, not just a mechanical gap — flagged rather than silently wired in. *Trail: this session, 2026-07-23.*

## Canon & World

- **The Underground Bazaar has zero mechanical items** — a real gap, nothing built yet. (How pricing would work there — memory/secret/debt economy, not gold — is open design, not debt itself; don't assume standard gold pricing transfers when this gets built.) *Trail: `rules/items.md`, Underground Bazaar section.*

## Process

- **The keyword usage counts in `rules/card-glossary.md` are a dated snapshot** (2026-07-18) — self-labeled as such, but cards have moved substantially since (the dice sweep, new Gambler cards, Vulnerable). Recount at next Sync rather than trust. *Trail: the glossary's own header note.*
