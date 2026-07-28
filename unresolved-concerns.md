# Unresolved Concerns

A scannable index of everything currently open that will eventually need a decision or a fix — the things that otherwise sit buried in `memory.md`'s prose (Recently Shipped entries, Standing Reasoning, Pending Propagation) until someone rereads the whole file. **This is an index, not a third home**: each entry is a line or two plus a pointer to where the full trail lives. Add a line when a concern gets flagged; delete the line when it's resolved (`memory.md` keeps the history — this file only ever shows the present).

**What does NOT belong here**: deliberately open questions. This repo keeps quiet doubts and unresolved world-hooks on purpose (`CLAUDE.md`: "the open questions are on purpose") — who bears the Storm Seat, what the Ferryman reads, what's at the Coil's center. Those are design, not debt. This file is for actual debt: flagged issues, known imbalances, deferred decisions that shouldn't be forgotten.

Also not here: **Pending Propagation** (operational staleness — print sheets, sim sync) stays in `memory.md` where the Sync workflow already looks for it. Entries below may point there, but the ledger itself doesn't move.

---

## Mechanics & Balance

- **Gear/gold pacing — a reference frame for how fast a party should accumulate gear and gold, likely a gold-per-session metric.** Distinct from the Bazaar entry below, which is about what's sellable and how pricing works there — this is purely "how much should the party have by session N," with the tier system itself (`rules/equipment.md`) already built and not in question. Drew's own read: pacing is naturally slow anyway — parties start with nothing and might end session 1 with only 2-3 consumables and no equipment at all, so "the first trickle of gear isn't in a rush." Parked, not blocking anything. *Trail: memory.md, the 2026-07-24 entries.*
- **RETALIATE/OVERCOMMIT/SEED's self-deferred Deadly — deliberately left alone in the latest card pass, with a fallback already chosen.** Dice/range tuning (already deferred as lower priority all session) is the first lever; an extra Deadly stack is the named fallback if that's not enough. Queued behind the dice/range pass, not an open question. *Trail: memory.md, the 2026-07-23 11:15 PM entry and the 2026-07-24 correction.*
- **Flapjack Octopus's FREEZE isn't wired into the sim yet — when it is, it'll collide with Briarwatch Jackalope's FREEZE in the name-keyed card registry.** Both cards are deliberately named FREEZE on purpose (Drew's call, 2026-07-28 — same thematic fit, Flapjack's bumped to Scry 2), a real, intentional canon choice this time, not a mistake. The registry conflict is purely a `combatsimulations/content.py` limitation: `build_cards()` returns one flat dict keyed by literal card name, so only one "FREEZE" can be registered at once. Needs a distinct internal registration key for whichever one gets wired in second — printed/canon name can stay identical on both cards either way. *Trail: `cards/briarwatch-jackalope.md`, `cards/flapjack-octopus.md`; memory.md, the 2026-07-28 entries.*

## Canon & World

- **The Underground Bazaar has zero mechanical items** — a real gap, nothing built yet, and Drew's own flag for a genuine future deep-design pass on the location: buying/selling mechanics are meant to be a highlight there, not an afterthought. (How pricing would work — memory/secret/debt economy, not gold — is open design, not debt itself; don't assume standard gold pricing transfers when this gets built.) *Trail: `rules/items.md`, Underground Bazaar section.*

