# Unresolved Concerns

A scannable index of everything currently open that will eventually need a decision or a fix — the things that otherwise sit buried in `memory.md`'s prose (Recently Shipped entries, Standing Reasoning, Pending Propagation) until someone rereads the whole file. **This is an index, not a third home**: each entry is a line or two plus a pointer to where the full trail lives. Add a line when a concern gets flagged; delete the line when it's resolved (`memory.md` keeps the history — this file only ever shows the present).

**What does NOT belong here**: deliberately open questions. This repo keeps quiet doubts and unresolved world-hooks on purpose (`CLAUDE.md`: "the open questions are on purpose") — who bears the Storm Seat, what the Ferryman reads, what's at the Coil's center. Those are design, not debt. This file is for actual debt: flagged issues, known imbalances, deferred decisions that shouldn't be forgotten.

Also not here: **Pending Propagation** (operational staleness — print sheets, sim sync) stays in `memory.md` where the Sync workflow already looks for it. Entries below may point there, but the ledger itself doesn't move.

---

## Mechanics & Balance

- **Armour and Thorns don't define what happens when they stack; Resist, Vulnerable, Deadly and Weak all do.** Every one of those four says outright how multiple instances behave ("Stacks: each stack applies to one future damage roll"). `Armour X` and `Thorns X` say nothing, so a creature with an Armour 2 passive that also plays a card granting Armour 1 is genuinely undefined — 2, 3, or highest-wins are all defensible readings. It bit immediately: three Briarbundle cards had to be redesigned mid-build purely to avoid creating the question, which is a workaround, not an answer. **Authority 3 — a glossary change.** Surfaced 2026-08-02 building the Briarbundles. *Trail: memory.md, the Briarbundles entry.*
- **Gear/gold pacing — a reference frame for how fast a party should accumulate gear and gold, likely a gold-per-session metric.** Distinct from the Bazaar entry below, which is about what's sellable and how pricing works there — this is purely "how much should the party have by session N," with the tier system itself (`rules/equipment.md`) already built and not in question. Drew's own read: pacing is naturally slow anyway — parties start with nothing and might end session 1 with only 2-3 consumables and no equipment at all, so "the first trickle of gear isn't in a rush." Parked, not blocking anything. *Trail: memory.md, the 2026-07-24 entries.*
- **RETALIATE/OVERCOMMIT/SEED's self-deferred Deadly — deliberately left alone in the latest card pass, with a fallback already chosen.** Dice/range tuning (already deferred as lower priority all session) is the first lever; an extra Deadly stack is the named fallback if that's not enough. Queued behind the dice/range pass, not an open question. *Trail: memory.md, the 2026-07-23 11:15 PM entry and the 2026-07-24 correction.*

## Canon & World

- **`bestiary/wallows-slime.md` is referenced twice by `quests/the-wallows-descent.md` and has never been written** — both references say "pending" explicitly, so this is acknowledged debt rather than a broken link, but the quest ships a creature the bestiary can't stat. Surfaced by the 2026-08-02 Sync reference sweep. *Trail: `memory.md`, Active Pending Threads — Wallows Slime, which has the creature's behavior already worked out (reaches, envelops, doesn't attack; forcing extraction raises Seat Influence). Only the stat block is missing.*

- **The Underground Bazaar has zero mechanical items** — a real gap, nothing built yet, and Drew's own flag for a genuine future deep-design pass on the location: buying/selling mechanics are meant to be a highlight there, not an afterthought. (How pricing would work — memory/secret/debt economy, not gold — is open design, not debt itself; don't assume standard gold pricing transfers when this gets built.) *Trail: `rules/items.md`, Underground Bazaar section.*

