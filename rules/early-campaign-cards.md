# Early-Campaign Cards

The Oracle content rule in `rules/cards.md` says what a starting deck **may not do**. This is the other half: the specific cards that have been looked at and cleared for a first campaign. A card being legal under the content rule is not the same as a card being right for players who are still learning what the reveal is.

Started 2026-09-17 from the cards already seated, and finished the same day: **all 165 cards in the three core colour lists have been screened** — 125 cleared, 40 sent to the middle tier, and two cut. Nothing here is a promise that a cleared card is balanced forever; it is a record that it was read with early play in mind and nothing stopped it.

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

- **Lifesteal was decided as a keyword, not card by card.** It was at zero in both sets and living on three unseated cards; rather than seat one, the whole mechanic went to the middle tier on 2026-09-17. Healing off the damage you deal turns a winning exchange into two and pays the player who is already ahead. A first campaign does not need it on tap. SKEWER, BLEED and CONSUME moved with it, and nothing had to be unseated.
- **Lifesteal and Quick are at zero in the expansion.** Lifesteal left with PARADOX and Quick was never there. Blind, Ward and Vulnerable came back — PARRY, FOCUSED STANCE and PROFILE's rewrite covered them. No Blue bench card carries Lifesteal or Quick, so filling them means another colour or a new card, and it is not obvious either is owed a seat.
- **Seat pressure is real now.** STRIKE took a Red melee seat in the Oracle 63 on 2026-09-17 and PUSH came out for it; PRESSURE and CORNER took the two Blue melee seats the tie-winners vacated. The 12/6/3 ratio means every addition is a swap, so a card cannot simply be added — something has to have a reason to leave.

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
