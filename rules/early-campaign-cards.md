# Early-Campaign Cards

The Oracle content rule in `rules/cards.md` says what a starting deck **may not do**. This is the other half: the specific cards that have been looked at and cleared for a first campaign. A card being legal under the content rule is not the same as a card being right for players who are still learning what the reveal is.

Started 2026-09-17 from the cards already seated — the Oracle 63 and the expansion. **82 more cards sit in the core lists unscreened**, so this roster is a floor, not a ceiling. Nothing here is a promise that a cleared card is balanced forever; it is a record that it was read with early play in mind and nothing stopped it.

---

## The screen

Four bars. The first two were derived from three cards Drew pulled on 2026-09-17, then tested against every seated card to check they were real lines and not a rule invented to fit three examples.

**1. It does not switch off a rule the players are still learning.** The reveal, the Effect, the Defense Effect — a first deck should have players using those, not turning them off. UNNAME stopped a Defense Effect from ever firing; PARADOX reversed the RPS outcome outright.

*Tested:* exactly two seated cards touch resolution at all, and both only improve a bad outcome by one step rather than inverting it — ANTICIPATE wins a tie, REBUTTAL turns a loss into a tie. Nudging the result one step is a different thing from reversing it. Both are flagged below rather than cut, because that line is a judgement call and the cards are already in players' hands.

**2. One status per half.** UNRAVEL granted Vulnerable *and* Blind on the same Effect.

*Tested:* with UNRAVEL out, no seated card grants two debuffs in a single half. It really was the only one, so this bar costs nothing to hold.

**3. The Oracle content rule, in full.** Nothing reaching into an enemy's hand, deck or stats; no Sealed; Staggered near-banned with OFF BALANCE the one exception; exiling an enemy's played card counts as deck manipulation. See `rules/cards.md`, The Oracle Deck.

**4. Name breadth is part of the card, but it is not a bar by itself.** A name is spent out of combat on an Advantage discard, so a wide name is real power (`rules/cards.md`, The Name Is Half the Card). It is a reason to read a card harder, not a reason to rename it. Renaming five seated cards for breadth was tried on 2026-09-17 and reverted the same day: **when a card does not belong in the early set, take the card out — do not rename it into disguise.** CHANNEL keeps a broad name and a seat, because the card underneath it is fine.

---

## The roster (84)

`*` marks a card from the expansion; the rest are the Oracle 63.

### Red — Body (28)

**Melee (16).** ATTRITION · BLINDSIDE · CLOSE IN · DOUBLE DOWN* · GAMBLER'S RUIN* · GRAPPLE* · GUARD · OFF BALANCE · OPEN GUARD · PAIN IS FUEL · PUSH · RETALIATE · SPARK OF VIOLENCE* · TRAMPLE · UNBROKEN · WEATHERED

**Ranged (4).** BURN BRIGHT* · CERTAIN STRIKE · SHARPEN · STARING CONTEST

**Both (8).** BLOOD TITHE* · CHARGE · FOOTWORK · GROUNDING STANCE · PROVOKE* · PULL · SECOND WIND · SLIP THE BLADE


### Blue — Mind (28)

**Melee (8).** ANTICIPATE · CLIMB · DEFLECT · DISTRACT · FOCUSED STANCE* · INTERRUPT · PARRY* · REBUTTAL

**Ranged (16).** AXIOM · CALCULATE · CALLED SHOT · ENFEEBLE · FOCUS · FORESEE · LAST RESORT · MARKED · MATCHED PAIR* · PARTITION · PINNED · PROFILE* · RETORT* · STUDY · UNDERSTANDING* · VEIL

**Both (4).** REALIGNMENT · SIDESTEP · STILL POINT · WAITING GAME*


### Green — Soul (28)

**Melee (4).** BIND · BRISTLE · CONFRONT* · SMOKESCREEN

**Ranged (8).** AID · COMMUNION · DISORIENT · FIELD MEDICINE* · FLOW · GUIDE* · HEALING SONG · MOCKERY

**Both (16).** BRAMBLE · CHANNEL* · INSTINCT · LEVEL THE FIELD · MEND · MIRROR STEP · OPENING · PATIENCE · PRIORITY · QUICKEN · RELEASE · RENEWAL · ROOTED OATH* · SHADE AWAY · SHARED BURDEN* · UNTOUCHED*

---

## Cleared, but worth watching

- **ANTICIPATE** *(Blue, Melee)* — `Defense Effect: You win on a tie.`
- **REBUTTAL** *(Blue, Melee)* — `Special Rule: If you would lose this exchange, it is a tie instead.`

These are the only two seated cards that reach into resolution. They are one step, not a reversal, which is why they survive bar 1 where PARADOX did not. If that distinction turns out to be too fine at the table, these are the two to pull — and note that both are Blue melee, the range Blue can least afford to lose right now.

---

## Not cleared

| Card | Why |
|------|-----|
| UNNAME | Defense Effects never fire — bar 1 |
| PARADOX | Reverses the RPS outcome — bar 1 |
| UNRAVEL | Vulnerable and Blind on one half — bar 2 |
| FORGET | Exiles the enemy's played card — bar 3 |
| TAINT | Adds a Wound to the enemy's deck — bar 3 |
| CONSUME | Cleared on the rules, cut for composition on 2026-09-17 |
| HEAVE AND HAUL | Cleared on the rules, cut as too strong for the set |

Every one of these is a perfectly good card. They belong in creature decks, character decks, and later Oracle seats — the same place the content rule has always sent its exclusions.

---

## Open

- **Lifesteal, Vulnerable and Quick are all at zero in the expansion.** Lifesteal and Ward left with PARADOX, Vulnerable and Blind with UNRAVEL; PARRY and FOCUSED STANCE recovered Blind and Ward, but no Blue bench card carries the other three at all. Filling them means another colour or a new card, and it is not obvious any of the three is owed a seat.
- **82 core-list cards have never been screened.** Red has the most depth and is the likeliest place to find early-campaign cards the deck could still use.

---

## Bugs the screen turned up

Neither is a verdict on early play — both are pool problems worth fixing whoever ends up holding the card.

- **PROBE is strictly dominated by PROFILE.** Same colour, same Ranged, identical defence halves. PROFILE has the bigger die (d6 against d4) and the better attack half (Scry 2 against Scry 1). There is no state of the game in which you would rather hold PROBE. This is the shape of the Red/Green BRACE collision (`experimental/archives/cut-cards.md`) without the shared name: two cards, one job, one of them strictly worse.
- **TURN's defence half was unresolvable, and is fixed.** It read `Redirect this attack's damage, in full, to a target of your choice. Only on a clean win — not a tie.` — but a defender who wins cleanly takes no damage at all, so on the only outcome the card allowed there was nothing to redirect. The history: the card was always meant to send the attack somewhere else, and an earlier pass sanded that off because the card sat in the Oracle pool and the effect was too strong for a starting deck. Its own flavour line kept the original intent on the card the whole time — *"It has to land somewhere. Somewhere is negotiable."* The redirect is restored and now says outright that the attack is not stopped, along with the detail that makes it bite: the attacker's statuses are spent on the redirected attack, so their Deadly lands on someone else and their Blind can make it miss entirely. It also applies Initiative Shift -1 to the attacker, which the card should have carried all along for something named TURN. **It is not an early-campaign card** — see below.

---

## The middle tier

Not a thing yet — Drew's idea, recorded here so the first candidate doesn't get lost. Some cards are clean under the content rule and simply too strong for a first campaign, which is a different verdict from "cut it." They want a pool of their own between the Oracle and the deep bench, to draw from once the table is past learning the reveal.

- **TURN** *(Blue, Ranged, d4)* — redirects an incoming attack onto a target of your choice, spending the attacker's statuses on it. The first entry, and the reason the tier came up.

---

## Related Documents

- `rules/cards.md` — the Oracle content rule, the colour conventions, and why a name's breadth is part of its power
- `printing/generate-cards.py` — the seated sets themselves, with the dated passes that produced them
- `experimental/card-name-verbs.md` — a naming vocabulary to draw from
