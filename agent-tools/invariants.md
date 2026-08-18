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
| Non-status cards are conserved across deck/hand/discard/exile | `check_card_conservation` |
| No measured distances in `quests/` or `bestiary/` | `check_distances` |
| Items use only glossary keywords, never longhand | `check_item_keywords` |

## Enforced on demand

Conservation is a property of a *transition*, not of a state, so it cannot live in `verify.py` — it needs a before as well as an after. It is a two-command tool run either side of the move instead.

| Invariant | Enforced by |
|---|---|
| Content is conserved across a restructure — a pure move loses no content line and duplicates none | `agent-tools/conserve.py snapshot` / `check` |

Run `snapshot` over the scope about to change, do the move, run `check`. Lost lines and duplicated lines both fail; newly written navigation is reported but never fails, because a restructure legitimately adds it.

## Not enforced — stated, and known to be unchecked

- **Exile's two combat-end rules are unimplemented in the simulator.** `rules/card-glossary.md` says exiled cards return to their owner's discard when combat ends, and that a status card exiled is *destroyed* instead. `combatsimulations/` models neither — `.exile` is a plain list with no combat-end handling and no status distinction. Harmless today, because within a single combat both readings are identical (out of play either way) and the sim only ever simulates one combat. It would matter the moment anything models a multi-fight sequence.

---

## How this file earned its current shape

The empty Confirmed section was the evidence. Prose invariants sat here catching nothing while the day's real bugs — nine wrong character HP values, two unparseable deck lines, six cards hidden inside character files, a card claimed shipped that never existed, six of 37 decks silently unvalidated — were all found by assertions that execute.

**The one that proves the point:** the first candidate here read *"derived stats are computed live, never cached."* Stated as an implementation, it was simply **false** — `max_hp` was stored and patched on every stat change. Restated as the property that actually matters — *max HP tracks current stats* — and then tested rather than assumed, it failed **154 of 1,447 random stat changes**: `eff()` floors a stat at 0 and `adjust()` was debiting max HP for points the formula never counted, so a stat driven under-water and back up left max HP wrong, silently self-correcting often enough to never get noticed. Fixed by computing `max_hp` from a fixed baseline instead of patching it, which makes the invariant true by construction rather than by every future mutation site remembering to be careful.

A vague invariant that nobody tests is worth less than no invariant at all, because it reads like coverage.

**The second candidate — card conservation — held, and testing it still found something.** Non-status cards proved exactly conserved across 180 duels, so it graduated to `check_card_conservation`. But the run also showed **zero status cards ever reaching exile.**

**The conclusion drawn from that was wrong, and the way it was wrong is worth keeping.** The reading was: the glossary called Exile *"the one way to answer a Wound, an Exhaust, or a curse permanently in the middle of a fight"*, BURN BRIGHT / SHED SKIN / SILENCE THE THREAD exile from your own piles without saying *"of your choice"*, therefore the cards could not perform the use case the glossary described. Drew's ruling (2026-08-18): **"of your choice" is implied when it's not written out.** The phrase appears on eight cards for emphasis, not as the thing that grants the choice — so those cards always could exile a held status card, and the capability was never missing. **A missing phrase was read as a missing capability.** The same paragraph also missed that SHED SKIN's Effect *destroys* a Wound outright, which contradicts "the one way" without involving Exile at all — visible in the card text that was quoted.

The glossary sentence was stale and is gone, but not because the cards failed to support it. It was a definitions file explaining where a mechanic gets used, against its own stated discipline — *"State the rule, plainly, and stop."* The implied-choice default now lives once, in `rules/cards.md` under "Attacker" / "Defender" vs. "Target", where reading conventions belong.

**Lesson, and it generalises past this instance:** an absence in card text is only evidence once you know what the text's defaults are. Before reporting that content cannot do something, check whether the missing words were ever required — `red-team.md` step 3b asks whether fiction claims an effect no rule provides, and the inverse error, claiming a rule provides nothing because a card didn't restate it, is now step 3c.

**And the negative test for this check passed on its first run, wrongly.** The injected fault was gated on `len(self.discard) > 6`, a condition the duels never reached, so nothing was ever leaked and the check reported clean. Tightening the injection to fire unconditionally made it fail correctly, naming three combatants and their exact card counts. **A negative test must confirm it actually triggered the fault, not merely that a fault was written.** That is the fourth instance in one session of a check reading identical whether or not it exercised anything.

**The third candidate — content conservation — is the one the old method could not have caught.** It was verified on 2026-08-17 by counting lines either side of the entry-sorting pass: 1,591 before, 1,591 after. That proves the totals matched. It does not prove the same lines came out the other side, and the difference is not academic. Injecting a deliberately botched move into `bestiary/skeinwing/` — two lines dropped, one block copied, exactly the shape of the reference-rewrite bug that hit three times in one session — produced a corpus with **2,433 content lines before and 2,433 after**, identical, while one line had been lost outright and another silently duplicated. Two faults in opposite directions cancel perfectly in a total. `conserve.py` compares the multiset instead, and named both.

The first injection attempt failed to fire at all: the file chosen was too small, the script raised `IndexError` before writing anything, and the check that followed reported a clean PASS — accurately, because nothing had changed. Retrying against a large enough file, with an assertion that the injection actually landed, is the only reason the finding above exists. **Fifth instance.**

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
