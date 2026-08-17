# Invariants

**An invariant is a property that must hold no matter how anything is implemented, visualised, or restructured.** Violate one and something is *broken* — not redesigned.

Two tests separate an invariant from a rule:

1. **Can you violate it and have nothing be wrong?** Evade being 50% is a **rule** — change it to 40% and the game is merely different. Card count being conserved across deck/hand/discard/exile is an **invariant** — break it and there is a bug. Rules are chosen; invariants are consequences.
2. **Can it fail?** An invariant nothing can check is a wish. This file's Confirmed section sat **empty** from its creation until 2026-08-17 while prose candidates accumulated above it, and in that time it caught nothing.

**So this file is an index, not a second source of truth.** Every invariant is named once, with the check that enforces it. Where nothing enforces one, that is stated plainly — an unenforced invariant and an enforced one must not look alike, which is the same disease as a check that doesn't exercise what it claims.

*Moved out of `rules/` on 2026-08-17 (Drew: "pull the invariants out of rules that's the wrong home for it"). These are not rules — a rule tells a player what happens; an invariant tells a builder what must never stop being true. Scope also widened past the simulator, since the repository's most valuable invariants turned out to be structural.*

---

## Enforced

Each of these is asserted by `agent-tools/verify.py` and fails the build when violated.

| Invariant | Enforced by |
|---|---|
| Max HP tracks current stats — always, including bespoke boss HP | `combatsimulations/engine.py`, `Combatant.max_hp` (computed, not stored) |
| Every card has a legal Range, a known tag, and an Attack line | `check_card_format` |
| Deck size equals total stats; per-colour counts equal the individual stats | `check_decks` |
| Max HP equals `(3 × Body) + Soul + Mind` unless explicitly bespoke | `check_stat_blocks` |
| Every card named in a deck resolves to a real card, in the right colour | `check_decks` |
| **A check reads everything it claims to read** | coverage assertions in `check_decks`, `check_stat_blocks` |
| Every card appears in at least one bucket | `check_bucket_lists` |
| Every name listed in a bucket or archetype resolves to a real card | `check_bucket_lists` |
| Every entry folder has one README, one Contents block, and a Contents list matching its files | `check_entry_structure` |
| No heading appears twice within a file | `check_entry_structure` |
| Every backticked path resolves | `check_refs` |
| A restated stat block matches its bestiary source | `check_restated_stat_blocks` |
| Simulator card definitions reconcile against canon | `check_sim` |
| The Oracle's two code mirrors agree with each other and with the pool | `check_oracle_sync` |
| Print artifacts match their sources | `check_print` |
| No measured distances in `quests/` or `bestiary/` | `check_distances` |
| Items use only glossary keywords, never longhand | `check_item_keywords` |

## Not enforced — stated, and known to be unchecked

- **Card count is conserved per combatant across deck, hand, discard, and exile.** Nothing is created or destroyed by ordinary play; the total changes only at two nameable events — a Wound/Exhaust insertion, or a permanent removal (short rest, or Exile returning to deck at combat's end). Any other change is a bug. *Checkable against `combatsimulations/` and worth building; nothing asserts it today.*
- **Content is conserved across a restructure.** A pure move loses no content line and duplicates none. Verified by hand on 2026-08-17's entry-sorting pass (1,591 lines before, 1,591 after) and it should be a standing tool, not a one-off script — every restructure this session that reported "clean" without proving conservation had only proven that nothing it thought to look for went wrong.

---

## How this file earned its current shape

The empty Confirmed section was the evidence. Prose invariants sat here catching nothing while the day's real bugs — nine wrong character HP values, two unparseable deck lines, six cards hidden inside character files, a card claimed shipped that never existed, six of 37 decks silently unvalidated — were all found by assertions that execute.

**The one that proves the point:** the first candidate here read *"derived stats are computed live, never cached."* Stated as an implementation, it was simply **false** — `max_hp` was stored and patched on every stat change. Restated as the property that actually matters — *max HP tracks current stats* — and then tested rather than assumed, it failed **154 of 1,447 random stat changes**: `eff()` floors a stat at 0 and `adjust()` was debiting max HP for points the formula never counted, so a stat driven under-water and back up left max HP wrong, silently self-correcting often enough to never get noticed. Fixed by computing `max_hp` from a fixed baseline instead of patching it, which makes the invariant true by construction rather than by every future mutation site remembering to be careful.

A vague invariant that nobody tests is worth less than no invariant at all, because it reads like coverage.

---

## Mechanic-override reference

Not invariants — a practical index for `combatsimulations/`: every card that overrides a specific mechanic, which one, and for how long. Useful for keeping the simulator's flag-based override system correct; check new content against it when a new card looks like it needs the same kind of override.

| Card/Effect | Mechanic overridden | Lifetime |
|---|---|---|
| Axiom | selection legality (color ban) | next reveal |
| Paradox | RPS resolution (inverts) | the exchange |
| Interrupt | defender may act (cannot-defend) | until your next turn |
| Ledger Weight | card selection (forced re-reveal, attacker-on-defender only) | one reveal |

---

## Related

- `agent-tools/verify.py` — where the enforced invariants actually live
- `agent-tools/design-principles.md` — design standards, which are *not* invariants: violating one makes something worse, not broken
- `rules/card-glossary.md` — keyword rules text, also not invariants
