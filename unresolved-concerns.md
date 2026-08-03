# Unresolved Concerns

A scannable index of everything currently open that will eventually need a decision or a fix — the things that otherwise sit buried in `memory.md`'s prose (Recently Shipped entries, Standing Reasoning, Pending Propagation) until someone rereads the whole file. **This is an index, not a third home**: each entry is a line or two plus a pointer to where the full trail lives. Add a line when a concern gets flagged; delete the line when it's resolved (`memory.md` keeps the history — this file only ever shows the present).

**What does NOT belong here**: deliberately open questions. This repo keeps quiet doubts and unresolved world-hooks on purpose (`CLAUDE.md`: "the open questions are on purpose") — who bears the Storm Seat, what the Ferryman reads, what's at the Coil's center. Those are design, not debt. This file is for actual debt: flagged issues, known imbalances, deferred decisions that shouldn't be forgotten.

Also not here: **Pending Propagation** (operational staleness — print sheets, sim sync) stays in `memory.md` where the Sync workflow already looks for it. Entries below may point there, but the ledger itself doesn't move.

---

## Mechanics & Balance

**`rules/card-glossary.md`'s per-keyword counts need a real mechanical recount.** The header numbers are a stated snapshot. On 2026-08-03 I wrote a recount script while adding seven cards and it disagreed with the header on **16 keywords, in both directions** — including decreases, which adding cards cannot cause. That means my counting rule differs from whatever produced the header, and I could not tell which was right. I updated only the six keywords the seven new cards demonstrably touch (Initiative Shift +2; Weak, Staggered, Resist, Evade, Thorns +1 each) and left the rest alone rather than overwrite live numbers from an unvalidated regex. Someone should settle the counting rule once and recount properly. `verify.py`'s `check_glossary_count` only checks the block total, not the per-keyword numbers. Trail: `memory.md`, the 2026-08-03 Oracle 12/6/3 entry.

**Body-size exemption to the strict distance rule.** Drew ruled 2026-08-03 that `CLAUDE.md`'s ban on measured distances in quest and bestiary content is strict, and sixteen measurements were removed. Three survive on my reading that a creature's own size is a size, not a distance: `bestiary/tollbird.md` and `quests/the-larder-fence.md` ("close to a meter tall"), `bestiary/skeinwing.md` (altitude). Held as hand-listed exemptions in `verify.py`'s `check_distances` so they can't grow quietly. One edit if Drew reads the rule as reaching them. Trail: `memory.md`, the 2026-08-03 contradiction-hunt entry.

**`cards/vescal.md`'s CENSER SWING carries the same vacuous-conditional bug GORE just had.** Range: Melee, Effect: *"If target is Frontline, deal +2 damage."* Melee legality already requires the target to be Frontline, so the condition can never be false — the bonus is unconditional, worded as if it isn't. GORE was fixed 2026-08-03 (Range → Both, die reduced) specifically because this made its condition real again; the identical fix would apply here, but Drew asked about GORE specifically and this wasn't in scope. Trail: `memory.md`, the 2026-08-03 GORE entry.

## Canon & World

**"Immune" used loosely in `rules/items.md`.** A Pell lantern is described as *"immune to the Misdirection Trap."* **Immunity** is a defined keyword meaning one-shot negation of the next attack. Same collision as `bestiary/fogcaller.md`'s, which was fixed; this one was left because it is out-of-combat prose about a navigation hazard, not a stat block. Recorded so it reads as a decision rather than an oversight. Trail: same entry.
