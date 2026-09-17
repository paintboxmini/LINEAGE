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

## The roster (81)

`*` marks a card from the expansion; the rest are the Oracle 63.

### Red — Body (28)

**Melee (16).** ATTRITION · BLINDSIDE · CLOSE IN · DOUBLE DOWN* · GAMBLER'S RUIN* · GRAPPLE* · GUARD · OFF BALANCE · OPEN GUARD · PAIN IS FUEL · PUSH · RETALIATE · SPARK OF VIOLENCE* · TRAMPLE · UNBROKEN · WEATHERED

**Ranged (4).** BURN BRIGHT* · CERTAIN STRIKE · SHARPEN · STARING CONTEST

**Both (8).** BLOOD TITHE* · CHARGE · FOOTWORK · GROUNDING STANCE · PROVOKE* · PULL · SECOND WIND · SLIP THE BLADE


### Blue — Mind (25)

**Melee (6).** ANTICIPATE · CLIMB · DEFLECT · DISTRACT · INTERRUPT · REBUTTAL

**Ranged (15).** AXIOM · CALCULATE · CALLED SHOT · ENFEEBLE · FOCUS · FORESEE · LAST RESORT · MARKED · MATCHED PAIR* · PARTITION · PINNED · PROFILE* · STUDY · UNDERSTANDING* · VEIL

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

- **Blue's expansion block is at 4 of 7.** It needs one ranged and two melee. The melee shortage is solved: PRESSURE, FOCUSED STANCE, PARRY and INTERCEPT were written on 2026-09-17 to sit beside CORNER, so Blue melee has five candidates where it had one. Which two get seated is open, and it interacts with the die means — PRESSURE is a d8, and any melee pair including it puts Blue at 3.36 or above, level with Red. Holding Blue's old 3.21 needs the three open seats to come to 9.5 in mean die, which is one d8 and two d4s.
- **The ranged seat has not been shortlisted.** Blue's ranged bench is deep but much of it fails the screen — BLANK forces a discard, FRACTURE exiles the enemy's played card, ERODE reduces a stat. DECODE, PROBE, DISSECT, RETORT, CHAIN and DRAIN are the likely candidates and have not been read properly yet.
- **82 core-list cards have never been screened.** Red has the most depth and is the likeliest place to find early-campaign cards the deck could still use.

---

## Related Documents

- `rules/cards.md` — the Oracle content rule, the colour conventions, and why a name's breadth is part of its power
- `printing/generate-cards.py` — the seated sets themselves, with the dated passes that produced them
- `experimental/card-name-verbs.md` — a naming vocabulary to draw from
