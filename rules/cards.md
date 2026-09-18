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

**Some keywords scale by colour rather than by die and range.** Thorns is the clearest: it is retaliation damage, so it belongs to Body, and the number is set by the card's colour — **Green 2, Blue 3, Red 4** — regardless of die or range. This is a game-wide rule, not a core-set one: creature signature cards follow the same ladder.

Two cards sit off that on purpose. **BRISTLE** is Green at 3: both its halves do nothing but grant Thorns, and it is Melee-only, so it buys the extra point with the range restriction and with having no second effect — CONFRONT, the other Green melee Thorns card, sits at the base 2 because it spends its defence half on Counter Attack instead. **PAIN IS FUEL** is Red at 2: it re-grants every turn you hold Anchored, and Thorns stacks additively, so a flat 4 there would be a different card.

**The ladder is retired as of 2026-09-17.** Drew called it that morning: a rule described as game-wide, already carrying two named exceptions out of the handful of cards using it, is on its way to not being a rule. By the end of the day it had failed in both directions.

| Colour | Ladder said | What the cards actually do |
|--------|-------------|----------------------------|
| Green | 2 | CONFRONT 2 — and BRISTLE at 3 |
| Blue | 3 | **nothing.** RETORT was Blue's only Thorns card, and it dropped Thorns entirely |
| Red | 4 | RETALIATE 4, SHATTER 3, PAIN IS FUEL 2 |

Red was the colour the ladder anchored and it holds three different values across three cards. Blue has none at all, and BRAMBLE — the card that existed to be Green's rung and did nothing else — was cut on 2026-09-18 once the ladder stopped justifying it — which is the outcome the colour conventions above should have predicted from the start: **Thorns is retaliation damage, so it belongs to Body, and Blue was only ever holding it because a ladder said every colour needed a rung.** Price Thorns per card, on the die and the range, the way everything else is priced.

BRISTLE at 3 was once a strict dominance against RETORT, which read "Gain Thorns 3" at a smaller die and a freer range. RETORT's defence half became Weak on 2026-09-08, and on 2026-09-17 its attack half dropped Thorns for Vulnerable — the card does what Blue does now, taking an enemy's options away rather than mirroring a Green card in another colour. That is the lesson worth keeping: two cards can share a keyword and a number as long as they aren't the same card, and a card that has to be argued into its colour probably belongs in a different one.

The crossovers are deliberate and worth keeping: Red still body-blocks for the party, Blue still helps allies, Green can still focus damage down. A colour with no exceptions is a colour nobody has to think about.

**Effect strength is paid for in the die, and in Range.** Where the same effect appears in more than one colour, the pool prices it: OPEN GUARD, MARKED, and OPENING all apply Vulnerable, at d8/Melee, d6/Ranged, and d4/Both. UNBROKEN, LAST RESORT, and UNTOUCHED are the same trade on Immunity. Read those ladders before setting a new card's die — the pool has already decided what that effect costs.

**The Attack line can carry more than the die.** Most cards read `Body + d8` and stop there, but the line legitimately holds anything that changes the roll or is paid to make it: a conditional bonus die (RHYTHM BREAK's `+1d6` against someone who moved, TRACE's `+2d6`, UNDERSTANDING's discard-for-`+1d6`), a doubled attack (TWIN STRIKE's `(Soul + d4) x 2`), or an HP cost (REPAY's `Pay 3 HP`). OVERCOMMIT puts a whole status there — `Gain Vulnerable` — which stretches the convention furthest.

This matters when reviewing: a card's power is not readable from its Effect lines alone, and a summary that lists only die, range and effects will show TWIN STRIKE as a plain d4 and RHYTHM BREAK as a d8 with nothing on offence. Both readings are wrong. Read the Attack line.

---

## The Oracle Deck

The starting Oracle deck is where a player learns what the game is, so it is deliberately narrower than the card pool it draws from. **Nothing in it reaches into an enemy's hand, deck, or stats directly.** Specifically, no Oracle card may:

- reveal or look at an enemy's hand
- force an enemy to discard
- insert status cards into an enemy's hand, deck, or discard
- manipulate an enemy's deck
- reduce an enemy's stats
- apply Sealed
- cost an enemy a whole attack or a whole defence, however it is worded, with one exception (below)

**Losing a whole attack or a whole defence is the one near-total ban, and it is written against the effect, not the keyword.** That swing is bigger than anything else on this list and not something a starting deck should hand out four times over. Red keeps exactly one card that reaches it — OFF BALANCE, which applies Staggered on a clean win only, so it has to be earned rather than traded for.

**Initiative Shift is not this, and the difference is the whole reason it is a separate mechanic.** A negative shift puts more people in front of you; it does not take your turn away. The turn still arrives, later, and everyone can see exactly when by looking at the wheel. Staggered deletes an instance outright, silently, and there is nothing to read off the table about when it stops mattering. So a card that pushes an enemy back in the order is board control like positioning or targeting, and belongs in a starting deck; a card that costs them the attack itself does not. Carved out deliberately on 2026-09-18 — RETALIATE, DOUBLE DOWN and INTERRUPT are all seated and all push the attacker back, and reading the ban to cover them would have cut three cards for doing the thing initiative is for.

**Staggered is the usual wording, and it is not the only one.** "Cannot defend until your next turn," "the attacker cannot defend next time you attack them," "skip your next attack" — all of it lands in the same place and all of it is barred. This was written against the keyword until 2026-09-17, and ABANDON sat in the gap for eleven days doing exactly what Staggered does with the word left off (`experimental/archives/cut-cards.md`). When you are checking a card against this rule, ask what the target loses, not which word the card used.

Acting on **your own** hand and deck is fine — drawing, discarding to pay a cost, Scry on your own deck. So is control that operates on the board rather than on someone's resources: statuses, positioning, initiative, targeting restrictions, removing buffs an enemy already has. The line is between changing the situation and going through their possessions.

**Exiling an enemy's card is deck manipulation, not board control.** This one is easy to seat by mistake, and was: a card they have played looks like it is already spent, but it is on its way to their discard, and their discard reshuffles into their deck. Exiling it shrinks what they draw from for the rest of the fight. FORGET and FRACTURE both do this and both are barred — FORGET was seated in the expansion for nine days before anyone caught it, and the rewrite that was supposed to make it legal only copied the illegal half onto the other side.

Cards excluded by this rule are still perfectly good cards; they belong in creature decks, character decks, and later Oracle additions. The list lives in `printing/generate-cards.py`'s `SETS`, with the same rule restated above it.

**Legal is not the same as early.** This rule bars what a starting deck may never do; it does not settle whether a legal card is right for players still learning the reveal. The cards cleared for a first campaign, the screen they were cleared against, and the ones that failed it are in `rules/early-campaign-cards.md`.

**The deck comes in two sets, 63 cards then 21.** The original prints as `oracle`; the expansion prints separately as `oracle-expansion`, so a review pass over the newer cards doesn't mean re-reading the older ones. They are one deck — the split is for reading, not for play. The expansion holds each colour's range identity at the same ratio (4/2/1 against the first set's 12/6/3), and the content rule above applies to both without exception.

<!-- print:skip-start -->
**The expansion was drawn from the core lists, not written fresh.** Anything the deck is short of should be answered from the bench first — the pool holds well over a hundred cards nobody has seated, and a card that already exists has already been priced against its neighbours. Where a bench card was barred by the content rule but was otherwise the right answer, the fix was to rebalance that card rather than invent around it: four were reworked for it, which is recorded above the set in `printing/generate-cards.py` — and one of the four, FORGET, turned out not to be qualifiable, because the half it was rewritten to copy broke the rule too. Writing new cards is the last resort, for a gap the pool genuinely cannot fill.
<!-- print:skip-end -->

<!-- print:skip-start -->
Twenty-one cards were written on 2026-09-08 as an expansion, before the bench-first rule above existed, and they were kept because they are good cards, not because the deck needed them. **Nine of the twenty-one are now seated** — PROVOKE moved Green → Red on 2026-09-09 and took a Red slot in the expansion; CHANNEL, CONFRONT and CORNER followed on 2026-09-17; and when seven cards left the Oracle 63 later that same day the replacements came out of this batch too, HAMMER into Red ranged (renamed SHATTER the same day), DISSECT into Blue ranged, and HARMONIZE, STIR and SHELTER into Green. HARMONIZE lasted a day; ALIGN and SEED hold those Green seats now. That is the bench-first rule doing its job: the pool had already priced these against their neighbours, so filling seven seats took no new cards at all.
<!-- print:skip-end -->

<!-- print:skip-start -->
Nine more still sit as bench — CLEAVE, MAUL, SKEWER, SHOULDER, EXPEND and ANCHOR in Red; DECODE and REDIRECT in Blue; ENTREAT in Green — and three failed the early-campaign screen (UNRAVEL, PROBE and INVERT, in `cards/tiers/middle.md`). Of the shapes the batch carried that the pool had never held, INVERT's Effect-cancelling is the one now barred from a starting deck; CORNER's mutual position lock, CHANNEL's three-way choice and CONFRONT's Green Counter Attack are all seated.
<!-- print:skip-end -->

---

## The Name Is Half the Card

A card's name carries as much weight as its Effect line, because the name is what a player spends outside combat. Discarding a card for Advantage asks the table whether its *name* plausibly supports what you're attempting (`rules/resolution.md`, Advantage & Disadvantage) — so a name is a promise about the kinds of noncombat problems that card can help solve.

Two consequences when writing or reworking a card:

- **A broad name is a stronger card**, whatever its Effect line says, because it applies to more attempts. FOCUS supports nearly anything requiring concentration; CARD TRICK supports card tricks. Breadth is real power, so weigh it the way you weigh a die size — a wide name on top of a strong Effect is a card that does two jobs. That cuts the other way too: a deliberately narrow name is a fair place to pay for an unusually good Effect.
- **Renaming a card changes what it can do out of combat**, not just how it reads. Check that the new name still covers the same ground, and that nothing else already holds it — duplicate names break the print pipeline's by-name lookups, which is exactly how the Red and Green BRACE collided (`experimental/archives/cut-cards.md`).

<!-- print:skip-start -->
**Worked example, 2026-09-17.** A card named ALIGN did Scry 2 and checked whether the two matched — nothing about that is alignment, so the word was doing no work where it sat. That card is MATCHED PAIR now, which is what it always was, and ALIGN names a new Green bench card about allies lined up two ways at once, by position and by the initiative order. Freeing a name is worth doing when the name is better than the card wearing it.
<!-- print:skip-end -->

A working vocabulary to name from, sorted by colour and by mechanic, with names already used by a card struck out of it: `experimental/card-name-verbs.md`.

---

## Card Glossary

Short versions for reading cards. `rules/card-glossary.md` is canonical for keywords like the one below; `rules/combat.md` is canonical for Range and Ongoing Effects.

**Scry X** — Look at the top X cards of a deck (your own unless the card targets another). Place each on top, on the bottom, or into the discard pile, in any order.

---

## Deck Building

**Deck size is total stats, for everyone.** Body + Mind + Soul, player and creature alike — 9 for a starting character, and it moves only when a stat does. A player's cards past that maximum sit in their card bank and swap in at advancement (`rules/character-creation.md`, Advancement); a creature simply never has more than its stats allow.

**Player decks — the stat-matching heuristic.** A solid default: the number of cards of each color matches the corresponding stat. Mind 4 / Body 2 / Soul 3 → 4 Blue, 2 Red, 3 Green. The deck's color weight mirrors who the character is — and since damage runs off the matching stat, it keeps every card in the deck pulling at full strength. A heuristic, not a law: drafting through the Oracle (see `rules/character-creation.md`, Advancement) can and should bend it.

**Trading cards.** Cards change hands at the Underground Bazaar and effectively nowhere else (`places/capital/underground-bazaar.md`, The Card Economy). Selling is always possible and permanent; buying is rare, is paid for in cards, memories, or secrets rather than coin, and adds to what you hold rather than swapping into the deck — at the size cap that means the bought card lands in the bank until an advancement makes room for it. Everywhere else in the world a card is earned — from the Oracle, or from whatever taught it.

**Signature cards follow the core set's conventions.** They are written for one stat block, but they are the same object as a core card and are read by the same players: same fields, same keyword vocabulary (numbered where the glossary numbers it), same Thorns ladder, and the same treatment of Range as a real cost. Range especially — a creature whose cards are all Both is a creature that never has to think about position, in a game that spends a third of the Oracle's design space teaching it. Signature cards ran 51% Both until 2026-09-09; they now sit at roughly a third each, leaning Melee because most things that attack you have to reach you first.

**Enemy decks.** Deck size equals the creature's **total stats** — the same number the player rule caps at, except a creature has no bank and no advancement, so its deck is simply built to that size once and stays there (a few bosses are deliberately built under it; `bestiary/hullback.md` and `bestiary/fermata.md` say so on their own entries) — with each color's count equal to the matching stat (signature cards count toward their color). Build 3 themed signature cards, then fill from the core lists (`cards/red-body.md`, `cards/blue-mind.md`, `cards/green-soul.md`) to reach the stat counts, leaning picks toward the creature's temperament. Enemies draw to hand size (Mind, minimum 2) like everyone else.

---

"Allies"/"enemies" in card text never include yourself: `rules/combat.md`, You Are Not Your Own Ally.

