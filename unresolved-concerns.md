# Unresolved Concerns

A scannable index of everything currently open that will eventually need a decision or a fix — the things that otherwise sit buried in `memory.md`'s prose (Recently Shipped entries, Standing Reasoning, Pending Propagation) until someone rereads the whole file. **This is an index, not a third home**: each entry is a line or two plus a pointer to where the full trail lives. Add a line when a concern gets flagged; delete the line when it's resolved (`memory.md` keeps the history — this file only ever shows the present).

**What does NOT belong here**: deliberately open questions. This repo keeps quiet doubts and unresolved world-hooks on purpose (`CLAUDE.md`: "the open questions are on purpose") — who bears the Storm Seat, what the Ferryman reads, what's at the Coil's center. Those are design, not debt. This file is for actual debt: flagged issues, known imbalances, deferred decisions that shouldn't be forgotten.

Also not here: **Pending Propagation** (operational staleness — print sheets, sim sync) stays in `memory.md` where the Sync workflow already looks for it. Entries below may point there, but the ledger itself doesn't move.

---

## Mechanics & Balance

- **Even-matchup PvP mirrors are still more lethal than the 1-death-per-20-sessions target, though the mechanism fix already landed.** Targeting was reworked (random pick, pile on, drop on collapse) — death-occurred rate dropped from 45–62% to 41–48% in symmetric 3v3 mirrors, real progress, still nowhere near target. Drew's own caveat: mirrors between equal-ish parties were only ever testing the mechanism's direction, not validating the number. Now tested against a real 4-player Oracle-drafted party vs. the Patient Host — see below; the mirror-vs-real-encounter gap is closing, not the death-rate number itself. *Trail: memory.md, Standing Reasoning (the team-targeting rework entry) and the 2026-07-23 test-party entry.*
- ~~Initiative Shift cards may be underpowered~~ — **tested for real, resolved.** A/B ablation on a genuine Oracle-drafted Shift-heavy deck (DELAY/URGENCY/YOU'RE NEXT) in a real 2v2, Shift neutralized vs. intact: 41.5% vs. 47.4% win rate, a real ~6-point swing. Shift is pulling real, measurable weight — not underpowered. *Trail: memory.md, 2026-07-23 test-party entry.*
- **The Initiative Wheel slots/clamp rework is simmering, unresolved** — current wheel rules still govern play; Drew may bring back a replacement whole. Cards stay within Shift ±1–3 until then. *Trail: memory.md Active Pending Threads; `archives/initiative-slots.md`.*
- **The Patient Host: two separate open threads, not one.** (1) Its signature kit (control/Initiative-Shift-flavored) versus its Mind 8/Body 6/Soul 10 stat line is a tuning question independent of whether it wins fights — it does win, decisively (84–91% vs. baseline parties, and now 78% vs. a real 4-player Oracle-drafted party outnumbering its CTR 24 with a combined 36), but that's driven heavily by the raw CTR gap, which doesn't by itself prove the *kit* is tuned right for stats that size. (2) A scaled-party test that would settle it can't be run honestly without an item/gear progression system, which doesn't exist yet. Both parked by Drew ("let the host run his inn in peace. for now"). *Trail: memory.md, Pending Propagation (the parked entry) and the 2026-07-23 test-party entry.*
- **The Greater Stonecoil has no balanced encounter build** — deliberate for now; a party forcing the Deep Stream crossing gets a live GM call or a pause-and-build. Becomes real debt the moment a campaign approaches the Old Flow Channel. *Trail: `quests/hollow-below-briarwatch.md`, Deep Stream Channel; memory.md.*
- **Immunity joined Positive Status Effects (`rules/card-glossary.md`), but the sim's shared status-transfer/strip code (`_transfer_statuses`/`_strip_one_status` in `content.py` — used by WAITING GAME, DRAIN, UNMAKE, LEVEL THE FIELD) still only knows Deadly/Resist/Evade/Protect.** Whether Immunity should be stealable/copyable/strippable by those specific cards is a real design question, not just a mechanical gap — flagged rather than silently wired in. *Trail: this session, 2026-07-23.*

## Canon & World

- **The Underground Bazaar has zero mechanical items** — a real gap, nothing built yet. (How pricing would work there — memory/secret/debt economy, not gold — is open design, not debt itself; don't assume standard gold pricing transfers when this gets built.) *Trail: `rules/items.md`, Underground Bazaar section.*

