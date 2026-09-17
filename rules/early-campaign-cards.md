# Early-Campaign Cards

The Oracle content rule in `rules/cards.md` says what a starting deck **may not do**. This is the other half: the specific cards that have been looked at and cleared for a first campaign. A card being legal under the content rule is not the same as a card being right for players who are still learning what the reveal is.

Started 2026-09-17 from the cards already seated, and finished the same day: **all 163 cards in the three core colour lists have been screened** — 139 cleared, 24 sent to the middle tier. Nothing here is a promise that a cleared card is balanced forever; it is a record that it was read with early play in mind and nothing stopped it.

---

## The screen

Four bars. The first two were derived from three cards Drew pulled on 2026-09-17, then tested against every seated card to check they were real lines and not a rule invented to fit three examples.

**1. It does not switch off a rule the players are still learning.** The reveal, the Effect, the Defense Effect — a first deck should have players using those, not turning them off. UNNAME stopped a Defense Effect from ever firing; PARADOX reversed the RPS outcome outright.

*Tested:* the line that came out of it is **one step against an inversion**. ANTICIPATE turns a tie into a win, REBUTTAL turns a loss into a tie — one step, and they clear. PARADOX flips the outcome, DEAD HEAT and INVERT cancel an Effect outright — those fail. Reading the whole pool turned up four more one-step cards (STAND, ADAPT, CALL, PUNISH); all four clear, and the family is six, which is worth knowing before somebody drafts toward it.

**2. One status per half.** UNRAVEL granted Vulnerable *and* Blind on the same Effect.

*Tested:* with UNRAVEL out, no seated card grants two debuffs in a single half. It really was the only one, so this bar costs nothing to hold.

**3. The Oracle content rule, in full.** Nothing reaching into an enemy's hand, deck or stats; no Sealed; Staggered near-banned with OFF BALANCE the one exception; exiling an enemy's played card counts as deck manipulation. See `rules/cards.md`, The Oracle Deck.

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

- **The Staggered near-ban has a loophole, and ABANDON is standing in it.** The ban is written against the keyword. ABANDON's defence half stops the attacker defending at all the next time you attack them, which is Staggered's whole effect without the word, so nothing catches it. ABANDON is in the middle tier on judgement; the rule itself should probably be rewritten to bar the effect rather than the keyword.
- **Lifesteal and Quick are at zero in the expansion.** Lifesteal left with PARADOX and Quick was never there. Blind, Ward and Vulnerable came back — PARRY, FOCUSED STANCE and PROFILE's rewrite covered them. No Blue bench card carries Lifesteal or Quick, so filling them means another colour or a new card, and it is not obvious either is owed a seat.
- **STRIKE has never been seated.** The plainest card in the game, and the one `rules/combat.md` cites to explain the d10 tier, is on the bench in both sets.

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
