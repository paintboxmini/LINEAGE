# Core Set Bucket Assignment

**Recorded, not executed.** All 143 cards in the three core sets have a bucket assigned here. **No cards have been moved** (2026-08-17, Drew: *"record the assignment, don't move the cards yet"*). This file *is* the home — when the Oracle pool is slimmed, each card's destination is already decided and reviewable.

## Why this exists

Drew: *"the goal isn't to empty the Oracle pool. it's to create buckets so that when we slim the Oracle pool down the cards have a home already."*

Three steps, in order: buckets must exist before the core sets can mean "Oracle candidates only," and bestiary deck-filling cannot be repointed at buckets until there are buckets. This file is step one.

## Home and index

A card has **one home** and may carry **secondary buckets**. Both are needed because they answer different questions:

- **Home** — the one file the card moves to when the pool is slimmed. A card can only live in one place.
- **Secondary** — every other bucket the card genuinely belongs to. Search looks here too.

**48 of 143 cards carry a secondary**, because Effect and Defensive Bonus often do different jobs — Drew: *"what about cards that have differentiated effect and bonus? they would go in two buckets."* Filing by home alone would hide real coverage: **defense homes 16 cards but indexes 30.** Half of it would be invisible.

**Which side sets the home.** The Effect by default. But **15 cards have a plain Effect and carry their whole identity in the Defensive Bonus** — STRIKE, DEAD HEAT, FRAME-TRAP, UNNAME among them — so for those the Defensive Bonus sets the home. Filing strictly by Effect would dump all 15 into plain attack, which is how DRAIN and WAITING GAME got mislaid on the first pass.

Buckets name **what a card is for**, never the keyword it uses. Drew: *"discard by itself doesn't tell us the useful part about what a card is doing."* That is why FIELD MEDICINE homes under cleansing rather than with the discard-pile cards — it heals, but what disqualifies it from a starter pool is Wound removal presupposing Wounds.

Multi-label *function* analysis (a different vocabulary, nine categories) stays in `agent-tools/card-corpus-analysis.md`'s design-space grid.


## Counts

| Bucket | Homes | Indexed |
|---|--:|--:|
| **self-inflicted cost** | 10 | 10 |
| **position** | 30 | 35 |
| **control** | 19 | 23 |
| **damage amp** | 12 | 22 |
| **defense** | 16 | 30 |
| **initiative** | 11 | 16 |
| **team support** | 10 | 15 |
| **sustain** | 6 | 9 |
| **card flow** | 9 | 12 |
| **hand denial** | 5 | 7 |
| **payoff** | 4 | 4 |
| **buff removal** | 3 | 5 |
| **rps manipulation** | 4 | 4 |
| **status inserters** | 2 | 2 |
| **cleansing** | 1 | 1 |
| **plain attack** | 1 | 1 |
| | **143** | |

### self-inflicted cost — 10 homed, 10 indexed

A benefit bought with a real price paid by the user — Exhaust into your own hand, HP, your own card, a skipped turn, a self-debuff. The cost is the card's identity, not a drawback bolted on.

*Archetype:* The Gambler — TABLE STAKES files here. GAMBLER'S RUIN is the archetype's other shipped card but homes under damage amp; the archetype spans both, which is why archetypes index rather than file.

BALANCE *(G)*, BERSERKER'S PRICE *(R)* → control, BLOOD TITHE *(R)* → team support, EMERGENCY REPAIRS *(R)* → sustain, OVERDRIVE *(R)* → position, RALLY *(R)* → position, SACRIFICE STRIKE *(R)* → damage amp, SHARED BURDEN *(G)* → defense/team support, TABLE STAKES *(R)* → defense/team support, UNMAKE *(B)* → buff removal

### position — 30 homed, 35 indexed

Moving yourself or someone else, or gaining something for holding still. Includes Anchored, Rooted, Rushdown, Quick, and Position-gated payoffs.

BIND *(G)*, CALCULATE *(B)*, CHARGE *(R)*, DART *(R)*, DEAD END *(B)*, DIG IN *(R)*, DUST *(G)* → control, FLOW *(G)*, FOOTWORK *(R)*, FRACTURE *(B)* → card flow, GORE *(R)*, GRAPPLE *(R)*, GROUNDING STANCE *(R)* → defense, HEAVE AND HAUL *(G)*, IRON GRIP *(R)*, MIRROR STEP *(G)*, PARTITION *(B)* → team support, PATIENCE OF STONE *(G)* → damage amp, PULL *(R)*, PUSH *(R)*, REALIGNMENT *(B)*, REPEL *(R)*, ROOTED OATH *(G)*, SEED *(G)* → damage amp/defense, SEISMIC REDIRECT *(R)* → damage amp, SLIPSTREAM *(B)* → defense, STARING CONTEST *(R)*, STILL POINT *(B)* → defense, SWAY *(G)*, TRAMPLE *(R)*

*Also indexed here (homed elsewhere):* OVERDRIVE, PATIENCE, RALLY, SIDESTEP, SLIP THE BLADE

### control — 19 homed, 23 indexed

Taking away what a target can do or how well they do it — Staggered, Blind, Sealed, Locked, Weak, Vulnerable.

ATTRITION *(R)*, AXIOM *(B)*, BLINDSIDE *(R)*, CALLED SHOT *(B)* → defense, CERTAIN STRIKE *(R)* → defense, DEAD RECKONING *(G)*, INTIMIDATE *(G)*, MARKED *(B)*, OPEN GUARD *(R)*, OPENING *(G)*, PREDICT *(B)*, REBUTTAL *(B)* → initiative, REELING *(R)*, REFRACT *(B)*, SECOND GUESS *(B)*, SHIELD BASH *(R)* → defense, TELL *(B)*, TWIN STRIKE *(G)*, VEIL *(B)*

*Also indexed here (homed elsewhere):* ANTICIPATE, BERSERKER'S PRICE, DUST, VOID

### damage amp — 12 homed, 22 indexed

Making damage bigger or landing it where it otherwise would not: Deadly, Critical, Thorns, Counter Attack, splash, flat bonuses, exploding dice.

BRAMBLE *(G)*, BREAK *(R)*, BRISTLE *(G)*, CHAIN *(B)*, DEAD HEAT *(R)*, EXPOSED *(B)* → defense, GAMBLER'S RUIN *(R)*, PATIENCE *(G)* → position, RETALIATE *(R)* → initiative, RETORT *(B)*, SPARK OF VIOLENCE *(R)*, STRIKE *(R)*

*Also indexed here (homed elsewhere):* BLOOD IN THE GAP, DEFLECT, PAIN IS FUEL, PATIENCE OF STONE, ROLLOUT, SACRIFICE STRIKE, SEED, SEISMIC REDIRECT, SHARPEN, YOU'RE NEXT

### defense — 16 homed, 30 indexed

Refusing or reducing incoming damage — Evade, Resist, Ward, Armour, Protect, Immunity, Deflect.

BRACE *(R)*, DEFLECT *(B)* → damage amp, ENDURE *(R)* → sustain, FORESEEN *(B)*, GIVE WAY *(G)*, INSTINCT *(G)*, INTERCEPT *(R)*, LAST RESORT *(B)*, PAIN IS FUEL *(R)* → damage amp, SETTLE *(G)*, SHADE AWAY *(G)*, SIDESTEP *(B)* → position, SLIP THE BLADE *(R)* → position, STEADFAST *(G)*, UNBROKEN *(R)*, UNTOUCHED *(G)*

*Also indexed here (homed elsewhere):* CALLED SHOT, CERTAIN STRIKE, EXPOSED, GROUNDING STANCE, PARADOX, ROLLOUT, SEED, SHARED BURDEN, SHIELD BASH, SLIPSTREAM, STILL POINT, SYNCHRONY, TABLE STAKES, WEATHERED

### initiative — 11 homed, 16 indexed

Turn order: Initiative Shift, acting first, extra or skipped turns.

DELAY *(G)*, DISTRACT *(B)*, DOUBLE DOWN *(R)*, HESITATE *(B)*, INTERRUPT *(B)*, MOCKERY *(G)*, QUICKEN *(G)*, RHYTHM BREAK *(R)*, STEAL *(G)*, URGENCY *(G)*, YOU'RE NEXT *(G)* → damage amp

*Also indexed here (homed elsewhere):* ACCEPTANCE, FOCUS, REBUTTAL, RETALIATE, WARSONG

### team support — 10 homed, 15 indexed

Aimed at an ally rather than an enemy or yourself.

AID *(G)*, CLIFF SONG *(R)*, GUARD *(R)*, RENEWAL *(G)*, RESONATE *(G)*, SHARPEN *(B)* → damage amp, SUPPORT *(G)*, SYNCHRONY *(G)* → defense, WARSONG *(G)* → initiative, WITNESS *(G)*

*Also indexed here (homed elsewhere):* BLOOD TITHE, COMMUNION, PARTITION, SHARED BURDEN, TABLE STAKES

### sustain — 6 homed, 9 indexed

Getting HP back — heals, Lifesteal, recovery.

BLOOD IN THE GAP *(R)* → damage amp, CONSUME *(G)*, PARADOX *(B)* → defense, RECOVER *(R)*, UNDERSTANDING *(B)*, WEATHERED *(R)* → defense

*Also indexed here (homed elsewhere):* EMERGENCY REPAIRS, ENDURE, PRESS THE WOUND

### card flow — 9 homed, 12 indexed

Moving your own cards around: draw, Scry, deck manipulation, Exile, returns to hand.

ACCEPTANCE *(G)* → initiative, ALIGN *(B)*, ANTICIPATE *(B)* → control, ATTUNE *(G)*, CLIMB *(B)*, COMMUNION *(G)* → team support, FOCUS *(B)* → initiative, PROFILE *(B)*, STUDY *(B)*

*Also indexed here (homed elsewhere):* BURN BRIGHT, FORGET, FRACTURE

### hand denial — 5 homed, 7 indexed

Reaching into a hand you cannot see — forced discard, forced reveal.

FORGET *(B)* → card flow, READ *(G)*, STILLNESS *(B)*, UNNAME *(B)*, VOID *(G)* → control

*Also indexed here (homed elsewhere):* FIELD MEDICINE, PRESS THE WOUND

### payoff — 4 homed, 4 indexed

Cashes in a condition that already exists. Weak or dead on turn one, dangerous once something has accumulated.

*Archetype:* No archetype yet. Closest unbuilt candidate is The Opportunist.

BURN BRIGHT *(R)* → card flow, PRESS THE WOUND *(R)* → hand denial/sustain, ROLLOUT *(R)* → damage amp/defense, TRACE *(B)* → buff removal

### buff removal — 3 homed, 5 indexed

Operating on the opponent's *positive* status effects — stripping, stealing, or copying them.

*Archetype:* The Parasite (steals) and The Mirror (copies) — `agent-tools/archetypes.md` defines these two against each other, and both land here.

DRAIN *(R)*, LEVEL THE FIELD *(G)*, WAITING GAME *(R)*

*Also indexed here (homed elsewhere):* TRACE, UNMAKE

### rps manipulation — 4 homed, 4 indexed

Changing how the reveal itself resolves: tie wins, auto-wins, cancelled effects.

ADAPT *(G)*, CERTAINTY *(B)*, EQUAL FOOTING *(R)*, FRAME-TRAP *(B)*

### status inserters — 2 homed, 2 indexed

Putting status cards into someone else's deck or hand.

REND *(R)*, TAINT *(B)*

### cleansing — 1 homed, 1 indexed

Removing status cards that are already there.

FIELD MEDICINE *(G)* → hand denial

### plain attack — 1 homed, 1 indexed

No effect on either side. The baseline the rest is measured against.

OVERCOMMIT *(R)*


---

## Hand-assigned homes

The mechanical pass misfiled these; set by hand, do not recompute away.

- **CLIMB** → card flow · **CHAIN** → damage amp · **SEED** → position · **DEFLECT** → defense
- **DRAIN, LEVEL THE FIELD, WAITING GAME** → buff removal — a bucket the first pass missed entirely; all three had fallen into plain attack.

**The misfilings clustered on archetype cards**, which is the finding rather than the annoyance. SEED is The Cultivator's shipped example, GAMBLER'S RUIN The Gambler's, WAITING GAME The Mirror's. They resist mechanical sorting because their identity is a strategy rather than a mechanic — the gap Drew predicted keyword sorting would leave, showing up as data.

## What this does not decide

- **Which cards leave the core sets.** That is the pool-slimming pass, and it has not happened. Every card here is still in `cards/red-body.md`, `cards/blue-mind.md`, or `cards/green-soul.md`.
- **Bucket file names or paths.** Nothing has been created. `cards/stat-adjusters.md` is the only bucket that physically exists, built ahead of this file for cards that had already left core.
- **Whether a bucket earns its own file.** Cleansing and plain attack hold one card each. That is an argument for merging them later, not for forcing members in now.

