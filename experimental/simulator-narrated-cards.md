# Cards the Simulator Still Narrates

*As of 2026-09-18.* **297 of 319** Effect and Defense Effect halves in the core pool are modelled — 289 compiled into operations the engine runs, 8 read as traits the reveal consults. **22 narrate**: the engine prints the text and leaves it to whoever is playing, which is what every card did before `combat-simulations/effects.py` existed.

**None of them is seated.** All 84 cards in the two printed sets are fully modelled, 166 halves out of 166. What follows is the bench and the middle tier.

A half either compiles completely or narrates. Partial execution is the one outcome worth avoiding — an effect that grants the buff and quietly drops the *and draw 1* produces a wrong fight that reports as a right one.

---

## Wants a person at the table

Rewriting a deck across combats, or becoming another card outright. These are not gaps to close — a simulator that did them would be guessing at a judgement the table should make.

| Card | | Tier | Text |
|---|---|---|---|
| **BECOMING** | Defense | — | Same as Effect. |
| **BECOMING** | Effect | — | Choose a card in your hand. Permanently replace it with a card drawn from the Oracle pool. This card is exiled until the end of combat. After its 3rd use, permanently destroy it instead. |
| **FOLLOW-UP** | Defense | — | Replaced by the copied card's Defense Effect. |
| **FOLLOW-UP** | Effect | — | Replaced by the copied card's Effect. |

## Wants a history the engine does not keep

Both ask about something that happened on an earlier turn. The engine holds the current state of a fight, not its record, so these need a log before they need a reader.

| Card | | Tier | Text |
|---|---|---|---|
| **PUNISH** | Effect | Middle | If the defender was damaged on the turn immediately before yours, this attack deals double damage. |
| **RHYTHM BREAK** | Defense | Bench | If the attacker's initiative shifted at all since their last turn, either direction, gain Resist. |

## Wants status cards moved between piles

Counting Wounds and Exhausts where they sit and moving them somewhere else. Status cards are real cards now, so this is reachable — it is plumbing rather than design.

| Card | | Tier | Text |
|---|---|---|---|
| **PRESS THE WOUND** | Defense | Middle | Heal 2 HP for each status card in your hand and discard pile. Then destroy them. |
| **PRESS THE WOUND** | Effect | Middle | The defender announces how many status cards they have in hand and discard pile. Deal +2 damage for each. |
| **UNBURDEN** | Defense | Middle | Transfer 1 status card from your hand or discard to the attacker |
| **UNBURDEN** | Effect | Middle | Transfer 1 status card from any ally's hand or discard to the defender |

## Wants to read a discard pile

Both look at the top few cards of a pile that is not a deck. Cheap, and the only reason they are still here is that nothing else needed it.

| Card | | Tier | Text |
|---|---|---|---|
| **FRACTURE** | Defense | Middle | If the top 3 cards of your discard are 1 of each color, the attacker must exile the card they played this turn |
| **FRACTURE** | Effect | Middle | If the top 3 cards of your discard are 1 of each color, deal 5 damage to either the enemy Frontline or the enemy Backline (your choice) |
| **TRACE** | Defense | Bench | If the attacker plays the same color as either of the top two cards of their discard pile, remove their Positive Status Effects |

## Per-ally choices and deferred permissions

Each ally decides for themselves, or is given something they may spend on a later turn. The pieces exist; the shapes are all slightly different from each other.

| Card | | Tier | Text |
|---|---|---|---|
| **ENTREAT** | Effect | Bench | Target ally may discard any number of cards, then draw that many. |
| **HARMONIZE** | Effect | Middle | All allies may change position. Each ally who does gains Evade. |
| **HEAVE AND HAUL** | Defense | Middle | All allies may change position freely on their next turn. |
| **HEAVE AND HAUL** | Effect | Middle | Choose a position. All enemies in that position move to the other position. |
| **RENEWAL** | Effect | Middle | All allies may discard 1 card then draw 2, or heal 4 |

## One-offs

Each needs something nothing else in the pool needs.

| Card | | Tier | Text |
|---|---|---|---|
| **CONSUME** | Defense | Bench | Deal Soul + d6 unpreventable damage to the attacker, then Lifesteal off it. You may Exile one card from your own hand to give the attacker Weak and Blind. |
| **TABLE STAKES** | Effect | Middle | Discard 1 random card from your hand. If it was Red, deal 4 unpreventable damage. If it was Blue, target gains Staggered. If it was Green, heal yourself and all allies 3 HP. |
| **TURN** | Defense | Middle | Only on a clean win — not a tie. The attack is not stopped: it resolves against a target of your choice instead of you, at full damage, spending the attacker's statuses on it as it goes. |
| **UNIFY** | Effect | Bench | Until the end of combat, allies next to you in the initiative order heal 2 HP at the start of their turns. Whenever an ally heals this way, you heal 2 HP as well. Ends if you die or leave combat. |

---

## How to regenerate this

`python3 combat-simulations/effects.py -v` lists the current set under **Narrated**, and the counts above come from the same call. This document was generated from the card files rather than typed, so it cannot disagree with them at the moment it was made — but it will go stale the next time a reader pass lands. Check the command before trusting the list.
