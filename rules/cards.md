# Cards

Cards are the primary language of Tales Untold.

In combat, you don't declare an action and roll — you play a card. The card tells you what you're attempting, how hard it hits, and what happens when it lands or fails. Your hand is your tactical options. Your deck is your character in motion.

What each field on a card means, "Attacker"/"Defender" vs. "Target," and a full worked example: `rules/combat.md`, Reading a Card.

---

## The Die Is the Card's Personality

When you look at a hand of cards, the dice tell you who you are right now.

A hand full of d8s is a brawler who hits hard and moves with purpose.
A d10 is a fourth tier and a Red one — three cards in the game carry it, and each pays for it somewhere else on its own text.
A hand full of d4s is a strategist watching for the moment everything opens up.
A hand full of d6s is someone threading the gap between the two.

Your deck is not just mechanics. It's how your character thinks.

---

## What Each Colour Tends Toward

General conventions, not laws. A card that breaks one for a good reason is fine; a colour that breaks its own convention constantly has stopped meaning anything.

- **Red — self-buffs and raw damage.** The biggest dice live here.
- **Blue — enemy control.** Debuffs, repositioning them, taking their options away.
- **Green — flexibility and support.** Healing, allies, movement, adaptability.

**Some keywords scale by colour rather than by die and range.** Thorns is the clearest: it is retaliation damage, so it belongs to Body, and the number is set by the card's colour — **Green 2, Blue 3, Red 4** — regardless of die or range.

Two cards sit off that on purpose. **BRISTLE** is Green at 3: both its halves do nothing but grant Thorns, and it is Melee-only, so it buys the extra point with the range restriction and with having no second effect — CONFRONT, the other Green melee Thorns card, sits at the base 2 because it spends its defence half on Counter Attack instead. **PAIN IS FUEL** is Red at 2: it re-grants every turn you hold Anchored, and Thorns stacks additively, so a flat 4 there would be a different card.

BRISTLE at 3 lands on Blue's base, which is why it is a d6 and RETORT is a d4: two cards with the same text and the same number have to be separated by die and range or one of them is simply worse. BRISTLE takes the bigger die and the tighter range; RETORT takes the smaller die and the freer one.

The crossovers are deliberate and worth keeping: Red still body-blocks for the party, Blue still helps allies, Green can still focus damage down. A colour with no exceptions is a colour nobody has to think about.

**Effect strength is paid for in the die, and in Range.** Where the same effect appears in more than one colour, the pool prices it: OPEN GUARD, MARKED, and OPENING all apply Vulnerable, at d8/Melee, d6/Ranged, and d4/Both. UNBROKEN, LAST RESORT, and UNTOUCHED are the same trade on Immunity. Read those ladders before setting a new card's die — the pool has already decided what that effect costs.

**The Attack line can carry more than the die.** Most cards read `Body + d8` and stop there, but the line legitimately holds anything that changes the roll or is paid to make it: a conditional bonus die (RHYTHM BREAK's `+1d6` against someone who moved, TRACE's `+2d6`, UNDERSTANDING's discard-for-`+1d6`), a doubled die (ABANDON's `2d8`), or an HP cost (REPAY's `Pay 3 HP`). OVERCOMMIT puts a whole status there — `Gain Vulnerable` — which stretches the convention furthest.

This matters when reviewing: a card's power is not readable from its Effect lines alone, and a summary that lists only die, range and effects will show ABANDON as a plain d8 and RHYTHM BREAK as a d8 with nothing on offence. Both readings are wrong. Read the Attack line.

---

## The Oracle Deck

The starting Oracle deck is where a player learns what the game is, so it is deliberately narrower than the card pool it draws from. **Nothing in it reaches into an enemy's hand, deck, or stats directly.** Specifically, no Oracle card may:

- reveal or look at an enemy's hand
- force an enemy to discard
- insert status cards into an enemy's hand, deck, or discard
- manipulate an enemy's deck
- reduce an enemy's stats
- apply Sealed
- apply Staggered, with one exception (below)

**Staggered is the one near-total ban.** It costs its target a whole attack or a whole defence, which is a bigger swing than anything else on this list and not something a starting deck should hand out four times over. Red keeps exactly one card that inflicts it — OFF BALANCE — and only on a clean win, so it has to be earned rather than traded for.

Acting on **your own** hand and deck is fine — drawing, discarding to pay a cost, Scry on your own deck. So is control that operates on the board rather than on someone's resources: statuses, positioning, initiative, targeting restrictions, removing buffs an enemy already has. The line is between changing the situation and going through their possessions.

Cards excluded by this rule are still perfectly good cards; they belong in creature decks, character decks, and later Oracle additions. The list lives in `printing/generate-cards.py`'s `SETS`, with the same rule restated above it.

**The deck comes in two sets, 63 cards then 21.** The original prints as `oracle`; the expansion prints separately as `oracle-expansion`, so a review pass over the newer cards doesn't mean re-reading the older ones. They are one deck — the split is for reading, not for play. The expansion holds each colour's range identity at the same ratio (4/2/1 against the first set's 12/6/3), and the content rule above applies to both without exception.

**The expansion was drawn from the core lists, not written fresh.** Anything the deck is short of should be answered from the bench first — the pool holds well over a hundred cards nobody has seated, and a card that already exists has already been priced against its neighbours. Where a bench card was barred by the content rule but was otherwise the right answer, the fix was to rebalance that card rather than invent around it: four were reworked to qualify, which is recorded above the set in `printing/generate-cards.py`. Writing new cards is the last resort, for a gap the pool genuinely cannot fill.

Twenty-one cards written on 2026-09-08 sit in the core lists as bench rather than in either Oracle set — CLEAVE, MAUL, SKEWER, SHOULDER, EXPEND, ANCHOR and HAMMER in Red; DECODE, REDIRECT, UNRAVEL, CORNER, PROBE, DISSECT and INVERT in Blue; HARMONIZE, CHANNEL, PROVOKE, STIR, SHELTER, ENTREAT and CONFRONT in Green. They were drafted as an expansion before the bench-first rule above existed, and they are kept because they are good cards, not because the deck needed them. Three carry shapes the pool had never held: INVERT cancels the other side's Effect for an exchange, CORNER locks both combatants in place rather than charging one with Rooted, and CHANNEL is the only modal card — pick one of three on either half. CONFRONT is the pool's only Green Counter Attack. They are available for creature decks, character decks, and any later Oracle seat.

---

## The Name Is Half the Card

A card's name carries as much weight as its Effect line, because the name is what a player spends outside combat. Discarding a card for Advantage asks the table whether its *name* plausibly supports what you're attempting (`rules/resolution.md`, Advantage & Disadvantage) — so a name is a promise about the kinds of noncombat problems that card can help solve.

Two consequences when writing or reworking a card:

- **A broad name is a stronger card**, whatever its Effect line says, because it applies to more attempts. FOCUS supports nearly anything requiring concentration; CARD TRICK supports card tricks. Breadth is real power, so weigh it the way you weigh a die size — a wide name on top of a strong Effect is a card that does two jobs. That cuts the other way too: a deliberately narrow name is a fair place to pay for an unusually good Effect.
- **Renaming a card changes what it can do out of combat**, not just how it reads. Check that the new name still covers the same ground, and that nothing else already holds it — duplicate names break the print pipeline's by-name lookups, which is exactly how the Red and Green BRACE collided (`experimental/archives/cut-cards.md`).

A working vocabulary to name from, sorted by colour and by mechanic, with names already used by a card struck out of it: `experimental/card-name-verbs.md`.

---

## Card Glossary

Short versions for reading cards. `rules/card-glossary.md` is canonical for keywords like the one below; `rules/combat.md` is canonical for Range and Ongoing Effects.

**Scry X** — Look at the top X cards of a deck (your own unless the card targets another). Place each on top, on the bottom, or into the discard pile, in any order.

---

## Deck Building

**Player decks — the stat-matching heuristic.** A solid default: the number of cards of each color matches the corresponding stat. Mind 4 / Body 2 / Soul 3 → 4 Blue, 2 Red, 3 Green. The deck's color weight mirrors who the character is — and since damage runs off the matching stat, it keeps every card in the deck pulling at full strength. A heuristic, not a law: drafting through the Oracle (see `places/island-in-a-ship.md`) can and should bend it.

**Trading cards.** Cards change hands at the Underground Bazaar and effectively nowhere else (`places/capital/underground-bazaar.md`, Card Trading). Selling is always possible and permanent; buying is rare, is paid for in cards, memories, or secrets rather than coin, and adds to a deck rather than swapping into it. Everywhere else in the world a card is earned — from the Oracle, or from whatever taught it.

**Enemy decks.** Deck size equals the creature's **total stats**, with each color's count equal to the matching stat (signature cards count toward their color). Build 3 themed signature cards, then fill from the core lists (`cards/red-body.md`, `cards/blue-mind.md`, `cards/green-soul.md`) to reach the stat counts, leaning picks toward the creature's temperament. Enemies draw to hand size (Mind, minimum 2) like everyone else.

---

"Allies"/"enemies" in card text never include yourself: `rules/combat.md`, You Are Not Your Own Ally.

