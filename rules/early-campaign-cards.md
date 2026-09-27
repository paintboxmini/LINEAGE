# Early-Campaign Cards

The Oracle content rule in `rules/cards.md` says what a starting deck **may not do**. This is the other half: the specific cards that have been looked at and cleared for a first campaign. A card being legal under the content rule is not the same as a card being right for players who are still learning what the reveal is.

Started 2026-09-17 from the cards already seated, and finished the same day: **every card in the three core colour lists has been screened**, and three were cut outright. *How many cleared and how many went to the middle tier is in `printing/manifest.txt`, which counts the lists rather than remembering a number — the figures written here by hand were wrong by the time anybody checked.* Nothing here is a promise that a cleared card is balanced forever; it is a record that it was read with early play in mind and nothing stopped it.

---

## The screen

Four bars. The first two were derived from three cards Drew pulled on 2026-09-17, then tested against every seated card to check they were real lines and not a rule invented to fit three examples.

**1. It does not touch resolution.** The reveal is the game. A first deck should have players using the Effect, the Defense Effect and the RPS outcome, not editing them.

*Tested, and revised once.* The bar started softer — "one step against an inversion" — which cleared ANTICIPATE for turning a tie into a win while failing PARADOX for flipping the outcome. That line survived exactly as long as the family looked like two cards. Reading the whole pool found six: ANTICIPATE, REBUTTAL, STAND, ADAPT, CALL and PUNISH. The argument that had kept the first two is that a tie advances nobody on its own, and that is true of one card and false of a deck holding four. All six went to the middle tier on 2026-09-17, which cost the seated Oracle 63 two Blue melee cards. **The bar is absolute now, and simpler for it.**

**2. One status per half.** UNRAVEL granted Vulnerable *and* Blind on the same Effect.

*Tested:* with UNRAVEL out, no seated card grants two debuffs in a single half. It really was the only one, so this bar costs nothing to hold.

**3. The Oracle content rule, in full.** Nothing reaching into an enemy's hand, deck or stats; no Sealed; exiling an enemy's played card counts as deck manipulation; and nothing that costs an enemy a whole attack or a whole defence, with OFF BALANCE the one exception. That last one was written against the Staggered keyword until 2026-09-17, when ABANDON turned out to be doing the same thing in plain words. It bars the effect now, so "cannot attack" and "cannot defend" are caught alongside the keyword. See `rules/cards.md`, The Oracle Deck.

**4. Name breadth is part of the card, but it is not a bar by itself.** A name is spent out of combat on an Advantage discard, so a wide name is real power (`rules/cards.md`, The Name Is Half the Card). It is a reason to read a card harder, not a reason to rename it. Renaming five seated cards for breadth was tried on 2026-09-17 and reverted the same day: **when a card does not belong in the early set, take the card out — do not rename it into disguise.** CHANNEL keeps a broad name and a seat, because the card underneath it is fine.

---

## The lists

The lists this screen produces live in `cards/tiers/`, next to the cards themselves:

- **`cards/tiers/beginner.md`** — the 84 that cleared, by colour and range, plus the two watched cards and the two that are eligible but unseated.
- **`cards/tiers/middle.md`** — everything that failed, sorted by which bar it failed. Nothing is cut; a card that fails a bar moves.
- **`cards/tiers/README.md`** — what the tiers are, and what to check when a card moves between them.

---

## Not cleared

The full list, sorted by which bar each card failed, is in `cards/tiers/middle.md`. Twelve cards as of 2026-09-17, eleven of them Blue — not because Blue is the problem colour, but because Blue is the only one read end to end.

Every one of them is a good card. Failing this screen is a statement about when a table should meet it, not about whether the card is worth having.

---

## Open

- **Lifesteal is not a middle-tier keyword, and the ruling that said so was made on the wrong number.** On 2026-09-17 the whole mechanic went to the middle tier on the reading that healing off the damage you deal turns a winning exchange into two. It does not: `rules/card-glossary.md` has always said **half the damage that actually landed, rounded down**, after Resist and every other reduction. Two cards were restating it as the full amount — SKEWER and CONSUME — and the argument was built on their text rather than on the rule. Both now say only *Lifesteal*, which is the convention the glossary asks for. The keyword is beginner-legal by default as of 2026-09-18, and BLEED, SKEWER and CONSUME went back to the bench. PARADOX stayed in the middle tier: it fails bar 1 on its own, for reversing the RPS outcome, and the keyword was never why it was there.

  *Worth keeping as a method note: the ruling was reached by reading the cards, and the cards disagreed with the rules file. `rules/card-glossary.md` opens by saying card text that contradicts it is an error. Reading the glossary first would have cost nothing and saved three cards a tier move.*
- **Lifesteal is at zero in both printed sets. Quick is not, and the claim that it was is fixed here** *(2026-09-26)*. Lifesteal is eligible again but unseated: its three cards are Red, Red and Green, so nothing about being legal gets Blue a Lifesteal card. **Quick is on three Oracle 63 cards — FOOTWORK, SLIP THE BLADE and REALIGNMENT** — and zero in the expansion, which is what the earlier note was reaching for and is a much smaller thing than a keyword being absent. *Measured against the seated lists rather than recalled.* Blind, Ward and Vulnerable came back — PARRY, FOCUSED STANCE and PROFILE's rewrite covered them. Filling the Lifesteal gap means a swap or a new card, and it is not obvious it is owed a seat.
- **UNDERSTANDING's name is wider than the card pays for, and it is the only one the 2026-09-27 pass flagged.** Reading all 84 seated names as aims turned up one real mismatch (`rules/cards.md`, Why Green has the broadest names). The card is `Mind + d8. Discard a card; if you do, +1d6.` with **Effect: None** — the biggest attack in Blue, and the whole card on your turn is damage bought with a discard. *Discarding for Advantage is also damage-free value bought with a discard*, so it is the same currency twice, and **Effect: None is the tell**: every other card pays for its name with an Effect line and this one has nothing there to weigh. The fix is the name, not the die — the d8-plus-d6 attack is the interesting part. **Open: what to rename it to.**

- **Seat pressure is real now.** STRIKE took a Red melee seat in the Oracle 63 on 2026-09-17 and PUSH came out for it; PRESSURE and CORNER took the two Blue melee seats the tie-winners vacated. The 12/6/3 ratio fixes the number of seats, so a card cannot take one without something else having a reason to leave. Writing a card costs nothing; seating one costs a seat.

  *And CORNER gave its seat back nine days later.* **On 2026-09-26 it left the player pool altogether**, on a bar none of the four above catches: **a card whose fiction needs a particular kind of place is not a starting card, because the party never picks the place** (`rules/cards.md`, A card that needs terrain belongs to whoever picks it). You cannot corner anybody in a field. It is the Minotaur's card now — a creature that fights in corridors by choice (`bestiary/minotaur.md`). **Blue's melee bench was TAINT, UNNAME and UNRAVEL, all three barred, so the seat genuinely could not be filled from the bench and THINK TWICE was written for it** at the same d8. **Blue melee is where this keeps happening**, and the reason is structural rather than bad luck: Blue's range identity is Ranged, so its melee cards are the ones the colour has least reason to write and the first to run out when anything is cut.

---

## Bugs the screen turned up

Both are fixed. Recorded because the shapes are worth recognising again.

- **PROBE was strictly dominated by PROFILE.** Same colour, same Ranged, identical defence halves, and PROFILE had both the bigger die and the better attack half — there was no state of the game in which you would rather hold PROBE. The shape of the Red/Green BRACE collision (`experimental/archives/cut-cards.md`) without the shared name to make it obvious. Both cards were rebuilt around opponent interaction instead of self-Scry on 2026-09-17: PROBE reads the defender's hand, which moves it to the middle tier, and PROFILE checks its own top card against the colour the other side played. They are not comparable any more.
- **TURN's defence half was unresolvable.** It read `Redirect this attack's damage, in full, to a target of your choice. Only on a clean win — not a tie.` — but a defender who wins cleanly takes no damage at all, so on the only outcome the card allowed there was nothing to redirect. An earlier pass had sanded the redirect off because the card sat in the Oracle pool and the effect was too strong for a starting deck, and what it left behind did not work. The redirect is restored, and the card is middle tier now rather than weakened to fit. **That is the argument for having a middle tier at all:** without somewhere else to put a card, "too strong to start" gets answered by rewriting it until it isn't, and the rewrite is where the bug came from.

---

## Related Documents

- `rules/cards.md` — the Oracle content rule, the colour conventions, and why a name's breadth is part of its power
- `printing/generate-cards.py` — the seated sets themselves, with the dated passes that produced them
- `experimental/card-name-verbs.md` — a naming vocabulary to draw from
