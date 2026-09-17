# Middle Tier

Cards that are good and are not beginner cards. Most are legal under every rule in the game and simply hit too hard, or ask too much of a table still learning the reveal. A few break the Oracle content rule specifically, which is a rule about starting decks — past that point it has nothing to say about them.

Nothing here is cut. The screen in `rules/early-campaign-cards.md` decides eligibility for the beginner pool; a card that fails it moves here.

**Status: the whole core pool has now been read.** 163 cards across the three colour lists — 84 seated, 79 on the bench, every one of them given a verdict on 2026-09-17. The lists are complete as of that date, not finished forever.

---

## Too strong to start

Clean under every rule. They belong to a table that already knows what it is doing.

| Card | | | Why it waits |
|------|---|---|---|
| **TURN** | Blue | Ranged d4 | Redirects an incoming attack onto a target of your choice at full damage, spending the attacker's statuses on it as it goes — their Deadly lands on someone else, their Blind can make it miss entirely. Weak and Initiative Shift -2 on the attack half. The card the tier was invented for. |
| **HEAVE AND HAUL** | Green | Both d8 | Moves every enemy in a chosen position to the other one, and lets all allies reposition freely on defence. Cut from the expansion on 2026-09-17 as too strong for that set. |

---

## Fails bar 1 — cancels or reverses, rather than nudging

The line is one step against an inversion. ANTICIPATE turning a tie into a win is a nudge and stays in the beginner pool; a card that cancels an Effect or flips the outcome does not.

| Card | | | What it switches off |
|------|---|---|---|
| **DEAD HEAT** | Red | Ranged d8 | On a tie, the defender's Defense Effect does not trigger. |
| **INVERT** | Blue | Both d4 | Cancels the other side's Effect outright, either half. |
| **PARADOX** | Blue | Ranged d6 | Reverses the RPS outcome outright. Not a nudge — an inversion. |
| **UNNAME** | Blue | Melee d4 | The other side's Defense Effect never fires. |

---

## Fails bar 2 — more than one status on a single half

| Card | | | |
|------|---|---|---|
| **UNRAVEL** | Blue | Melee d6 | Vulnerable and Blind, both on the attack half. |
| **INTIMIDATE** | Green | Ranged d4 | Weak and Staggered on the same half — and Staggered is barred anyway. |

---

## Fails bar 3 — the Oracle content rule

The rule is in `rules/cards.md`, The Oracle Deck. It governs starting decks only.

| Card | | | Which line |
|------|---|---|---|
| **BLANK** | Blue | Ranged d6 | Forces a discard at random. |
| **BREAK** | Red | Melee d6 | Defender reveals their hand. |
| **ERODE** | Blue | Ranged d6 | Reduces an enemy's Soul for the combat. |
| **FORGET** | Blue | Melee d4 | Exiles the enemy's played card, which takes it out of their discard-and-reshuffle cycle for the fight. |
| **FRACTURE** | Blue | Ranged d8 | Same, conditionally. |
| **PRESS THE WOUND** | Red | Both d6 | Defender announces their status cards, and the damage scales off the count. |
| **PROBE** | Blue | Ranged d4 | Looks at the defender's hand. |
| **RATTLE** | Red | Melee d8 | Staggered on both halves. The near-ban keeps exactly one Red card, and it is OFF BALANCE. |
| **REND** | Red | Melee d6 | Adds a Wound to the bottom of the defender's deck. |
| **SUNDER** | Red | Melee d6 | Target loses 1 Mind for the combat. |
| **TABLE STAKES** | Red | Both d6 | Staggered on the Blue branch of its gamble. |
| **TAINT** | Blue | Melee d4 | Adds a Wound to the bottom of the enemy's deck. |
| **TOPPLE** | Green | Both d4 | Staggered on both halves. |
| **UNBURDEN** | Green | Both d4 | Transfers status cards out of an ally's hand into the defender's. |
| **WITHER** | Green | Ranged d6 | Target loses 1 Body for the combat. |

---

## Judgement calls, not bar failures

Neither is caught by the letter of a bar. Both are here on the spirit of one, and both are cheap to move back.

| Card | | | The argument |
|------|---|---|---|
| **ABANDON** | Red | Melee 2d8 | The defence half stops the attacker defending at all the next time you attack them. That is Staggered without the keyword, so the near-ban does not catch it — but it is the same swing, and it is the reason the ban exists. |
| **STEAL** | Green | Both d4 | Takes a consumable off the defender. It touches no card and no stat, so the content rule's list does not name it, but the sentence that list ends on does: the line is between changing the situation and going through their possessions. |

---

## Notes

**The tie-winning family is six cards, not two.** ANTICIPATE and REBUTTAL are seated and knowingly kept — winning a tie advances nobody on its own, and Pat is going to chase it anyway. Reading the rest of the pool turned up four more that do the same thing: STAND (Red), ADAPT (Green), CALL (Blue) and PUNISH (Blue). All four are cleared for the beginner pool, because filing them anywhere else would contradict the call already made on the first two. **CALL sat in this file for one day before that was caught.** The exposure is three times what it looked like — worth knowing before a deck gets built out of the bench.

**ABANDON inflicts Staggered without the word.** The near-ban is written against the keyword, and ABANDON's defence half stops the attacker defending at all next time you attack them, which is the same swing by another name. It is here on judgement rather than on the letter of the bar, and the loophole is worth closing in the rule itself.

**PROBE and PROFILE traded jobs on 2026-09-17.** PROFILE's defence half used to read the attacker's hand, and was rewritten on 2026-09-08 to qualify for the expansion. PROBE has taken that job over — looking at the defender's hand is now its whole attack half — which moves PROBE here and leaves PROFILE a beginner card. It also settles a dominance bug: the two were separated by a die and one point of Scry, with PROFILE strictly better in every game state. They are different cards now, in different tiers.

**TURN and the older fix.** TURN's redirect was sanded off by an earlier pass because the card sat in the Oracle pool and the effect was too strong for a starting deck. What was left could not resolve — it redirected "this attack's damage" on a clean defender win, and a defender who wins cleanly takes no damage in the first place. Its own flavour line kept the original intent the whole time: *"It has to land somewhere. Somewhere is negotiable."* **This tier exists so that the answer to "too strong to start" stops being "weaken it until it is not."**

---

## Related Documents

- `cards/tiers/README.md` — what the tiers are and how a card moves between them
- `cards/tiers/beginner.md` — the cards that cleared
- `rules/early-campaign-cards.md` — the screen and its four bars
