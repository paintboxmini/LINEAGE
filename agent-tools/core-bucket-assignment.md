# Core Set Bucket Assignment

**Recorded, not executed.** All 143 core-set cards have a bucket assigned. **No cards have been moved** (2026-08-17, Drew: *"record the assignment, don't move the cards yet"*).

Card lists live in `cards/buckets/`; archetype lists in `cards/archetypes/`. Neither holds card text — `cards/` remains the only source of that. This file holds the assignment and the reasoning behind it.

## Why this exists

Drew: *"the goal isn't to empty the Oracle pool. it's to create buckets so that when we slim the Oracle pool down the cards have a home already."*

Buckets must exist before the core sets can mean "Oracle candidates only," and bestiary deck-filling cannot be repointed at buckets until there are buckets.

## Home and index

**One home, many indexes.** Home is the single file a card moves to when the pool is slimmed. Secondary buckets are every other bucket it genuinely belongs to, and search reads those too.

**50 of 143 cards carry a secondary**, because Effect, Defensive Bonus and Special Rule frequently do different jobs — Drew: *"what about cards that have differentiated effect and bonus? they would go in two buckets."* Filing by home alone hides real coverage: **defense homes 16 and indexes 30.**

### Which line sets the home

**Special Rule → Effect → Defensive Bonus.** Special Rule wins because `rules/card-glossary.md` defines it as overriding normal resolution outright; when a card has one, it is the card. Where the Effect reads *None*, the Defensive Bonus sets the home — **15 cards carry their whole identity there**, including STRIKE, DEAD HEAT and UNNAME, and filing strictly by Effect would dump all of them into plain attack.

**Special Rules were missed on the first pass and changed two homes when added** (2026-08-17, Drew: *"make sure to get a read on what special rules are doing as well"*):

- **PARADOX** was homed under sustain for its Lifesteal. Its Special Rule *reverses the RPS outcome* — a headline RPS-pillar mechanic that was absent from the bucket entirely. Now homes under rps manipulation, sustain and defense secondary.
- **STEAL** was homed under initiative, matched off an Initiative Shift in its defensive line. All three of its lines do different things, and Drew set each one: the Special Rule exiles the card after use, which is a **self-inflicted cost** and its home; the Effect steals a consumable, which is **misc**; the Defensive Bonus is **initiative**. One card, three buckets — the clearest case in the set for why home-plus-index was needed.

**FRAME-TRAP** keeps its rps manipulation home but gained two secondaries. Drew: *"FRAME-TRAP's special rule interacts with the rps pillar. it relies on the previous ally winning rps."* Its Special Rule auto-wins only if the defender was hit on the turn immediately before — so it also cashes in an existing condition (**payoff**) and depends on an ally having acted first (**team support**). Neither was visible from Effect or Defensive Bonus alone.

**STEAL is the only item-touching card in all 143 core cards** — and in the whole 341-card corpus. Item theft is a singleton behaviour, so it indexes to **misc**: a holding pen for behaviours too rare to justify a bucket, revisited if a second card ever joins one.

A bucket names **what a card is for**, never the keyword it uses. Drew: *"discard by itself doesn't tell us the useful part about what a card is doing."*



## Counts

| Bucket | Homes | Indexed |
|---|--:|--:|
| **self-inflicted cost** | 11 | 11 |
| **position** | 30 | 35 |
| **control** | 19 | 23 |
| **damage amp** | 12 | 22 |
| **defense** | 16 | 30 |
| **initiative** | 10 | 16 |
| **team support** | 10 | 16 |
| **sustain** | 5 | 9 |
| **card flow** | 9 | 12 |
| **hand denial** | 5 | 7 |
| **payoff** | 4 | 5 |
| **buff removal** | 3 | 5 |
| **rps manipulation** | 5 | 5 |
| **status inserters** | 2 | 2 |
| **cleansing** | 1 | 1 |
| **plain attack** | 1 | 1 |
| **misc** | 0 | 1 |
| | **143** | |

### self-inflicted cost — 11 homed, 11 indexed

A benefit bought with a real price paid by the user, including a card that exiles itself. The cost is the card's identity, not a drawback bolted on.

BALANCE *(G)*, BERSERKER'S PRICE *(R)* → control, BLOOD TITHE *(R)* → team support, EMERGENCY REPAIRS *(R)* → sustain, OVERDRIVE *(R)* → position, RALLY *(R)* → position, SACRIFICE STRIKE *(R)* → damage amp, SHARED BURDEN *(G)* → defense/team support, STEAL *(G)* → initiative/misc, TABLE STAKES *(R)* → defense/team support, UNMAKE *(B)* → buff removal

### position — 30 homed, 35 indexed

Moving yourself or someone else, or gaining something for holding still.

BIND *(G)*, CALCULATE *(B)*, CHARGE *(R)*, DART *(R)*, DEAD END *(B)*, DIG IN *(R)*, DUST *(G)* → control, FLOW *(G)*, FOOTWORK *(R)*, FRACTURE *(B)* → card flow, GORE *(R)*, GRAPPLE *(R)*, GROUNDING STANCE *(R)* → defense, HEAVE AND HAUL *(G)*, IRON GRIP *(R)*, MIRROR STEP *(G)*, PARTITION *(B)* → team support, PATIENCE OF STONE *(G)* → damage amp, PULL *(R)*, PUSH *(R)*, REALIGNMENT *(B)*, REPEL *(R)*, ROOTED OATH *(G)*, SEED *(G)* → damage amp/defense, SEISMIC REDIRECT *(R)* → damage amp, SLIPSTREAM *(B)* → defense, STARING CONTEST *(R)*, STILL POINT *(B)* → defense, SWAY *(G)*, TRAMPLE *(R)*

*Also indexed here:* OVERDRIVE, PATIENCE, RALLY, SIDESTEP, SLIP THE BLADE

### control — 19 homed, 23 indexed

Taking away what a target can do or how well.

ATTRITION *(R)*, AXIOM *(B)*, BLINDSIDE *(R)*, CALLED SHOT *(B)* → defense, CERTAIN STRIKE *(R)* → defense, DEAD RECKONING *(G)*, INTIMIDATE *(G)*, MARKED *(B)*, OPEN GUARD *(R)*, OPENING *(G)*, PREDICT *(B)*, REBUTTAL *(B)* → initiative, REELING *(R)*, REFRACT *(B)*, SECOND GUESS *(B)*, SHIELD BASH *(R)* → defense, TELL *(B)*, TWIN STRIKE *(G)*, VEIL *(B)*

*Also indexed here:* ANTICIPATE, BERSERKER'S PRICE, DUST, VOID

### damage amp — 12 homed, 22 indexed

Making damage bigger or landing it where it otherwise would not.

BRAMBLE *(G)*, BREAK *(R)*, BRISTLE *(G)*, CHAIN *(B)*, DEAD HEAT *(R)*, EXPOSED *(B)* → defense, GAMBLER'S RUIN *(R)*, PATIENCE *(G)* → position, RETALIATE *(R)* → initiative, RETORT *(B)*, SPARK OF VIOLENCE *(R)*, STRIKE *(R)*

*Also indexed here:* BLOOD IN THE GAP, DEFLECT, PAIN IS FUEL, PATIENCE OF STONE, ROLLOUT, SACRIFICE STRIKE, SEED, SEISMIC REDIRECT, SHARPEN, YOU'RE NEXT

### defense — 16 homed, 30 indexed

Refusing or reducing incoming damage.

BRACE *(R)*, DEFLECT *(B)* → damage amp, ENDURE *(R)* → sustain, FORESEEN *(B)*, GIVE WAY *(G)*, INSTINCT *(G)*, INTERCEPT *(R)*, LAST RESORT *(B)*, PAIN IS FUEL *(R)* → damage amp, SETTLE *(G)*, SHADE AWAY *(G)*, SIDESTEP *(B)* → position, SLIP THE BLADE *(R)* → position, STEADFAST *(G)*, UNBROKEN *(R)*, UNTOUCHED *(G)*

*Also indexed here:* CALLED SHOT, CERTAIN STRIKE, EXPOSED, GROUNDING STANCE, PARADOX, ROLLOUT, SEED, SHARED BURDEN, SHIELD BASH, SLIPSTREAM, STILL POINT, SYNCHRONY, TABLE STAKES, WEATHERED

### initiative — 10 homed, 16 indexed

Turn order: Initiative Shift, acting first, extra or skipped turns.

DELAY *(G)*, DISTRACT *(B)*, DOUBLE DOWN *(R)*, HESITATE *(B)*, INTERRUPT *(B)*, MOCKERY *(G)*, QUICKEN *(G)*, RHYTHM BREAK *(R)*, URGENCY *(G)*, YOU'RE NEXT *(G)* → damage amp

*Also indexed here:* ACCEPTANCE, FOCUS, REBUTTAL, RETALIATE, STEAL, WARSONG

### team support — 10 homed, 16 indexed

Aimed at an ally.

AID *(G)*, CLIFF SONG *(R)*, GUARD *(R)*, RENEWAL *(G)*, RESONATE *(G)*, SHARPEN *(B)* → damage amp, SUPPORT *(G)*, SYNCHRONY *(G)* → defense, WARSONG *(G)* → initiative, WITNESS *(G)*

*Also indexed here:* BLOOD TITHE, COMMUNION, FRAME-TRAP, PARTITION, SHARED BURDEN, TABLE STAKES

### sustain — 5 homed, 9 indexed

Getting HP back.

BLOOD IN THE GAP *(R)* → damage amp, CONSUME *(G)*, RECOVER *(R)*, UNDERSTANDING *(B)*, WEATHERED *(R)* → defense

*Also indexed here:* EMERGENCY REPAIRS, ENDURE, PARADOX, PRESS THE WOUND

### card flow — 9 homed, 12 indexed

Moving your own cards around.

ACCEPTANCE *(G)* → initiative, ALIGN *(B)*, ANTICIPATE *(B)* → control, ATTUNE *(G)*, CLIMB *(B)*, COMMUNION *(G)* → team support, FOCUS *(B)* → initiative, PROFILE *(B)*, STUDY *(B)*

*Also indexed here:* BURN BRIGHT, FORGET, FRACTURE

### hand denial — 5 homed, 7 indexed

Reaching into a hand you cannot see.

FORGET *(B)* → card flow, READ *(G)*, STILLNESS *(B)*, UNNAME *(B)*, VOID *(G)* → control

*Also indexed here:* FIELD MEDICINE, PRESS THE WOUND

### payoff — 4 homed, 5 indexed

Cashes in a condition that already exists.

BURN BRIGHT *(R)* → card flow, PRESS THE WOUND *(R)* → hand denial/sustain, ROLLOUT *(R)* → damage amp/defense, TRACE *(B)* → buff removal

*Also indexed here:* FRAME-TRAP

### buff removal — 3 homed, 5 indexed

Taking from the opponent — stripping, stealing, or copying what they already have.

DRAIN *(R)*, LEVEL THE FIELD *(G)*, WAITING GAME *(R)*

*Also indexed here:* TRACE, UNMAKE

### rps manipulation — 5 homed, 5 indexed

Changing how the reveal itself resolves.

ADAPT *(G)*, CERTAINTY *(B)*, EQUAL FOOTING *(R)*, FRAME-TRAP *(B)* → payoff/team support, PARADOX *(B)* → defense/sustain

### status inserters — 2 homed, 2 indexed

Putting status cards into someone else's deck or hand.

REND *(R)*, TAINT *(B)*

### cleansing — 1 homed, 1 indexed

Removing status cards that are already there.

FIELD MEDICINE *(G)* → hand denial

### plain attack — 1 homed, 1 indexed

No effect on any line.

OVERCOMMIT *(R)*

### misc — 0 homed, 1 indexed

Behaviours with exactly one card in the corpus. A holding pen, revisited if a second card joins.

*(none homed here yet)*

*Also indexed here:* STEAL

---

## Hand-assigned homes

Set by hand; do not recompute away.

- **CLIMB** → card flow · **CHAIN** → damage amp · **SEED** → position · **DEFLECT** → defense
- **DRAIN, LEVEL THE FIELD, WAITING GAME** → buff removal — a bucket the first pass missed entirely; all three had fallen into plain attack.
- **STEAL** → self-inflicted cost, with misc and initiative secondary (2026-08-17, Drew).
- **FRAME-TRAP** → payoff and team support as secondaries, from reading its Special Rule.

**The misfilings clustered on archetype cards.** SEED is The Cultivator's shipped example, GAMBLER'S RUIN The Gambler's, WAITING GAME The Mirror's. They resist mechanical sorting because their identity is a strategy rather than a mechanic — the gap Drew predicted keyword sorting would leave, arriving as data. That is what `cards/archetypes/` is for.

## What this does not decide

- **Which cards leave the core sets.** The pool-slimming pass has not happened. Every card here is still in `cards/buckets/red.md`, `cards/buckets/blue.md`, or `cards/buckets/green.md`.
- **Whether a bucket earns its own card file.** Cleansing and plain attack hold one card each — an argument for merging later, not for forcing members in now.
- **Non-core cards.** Signature sets, location pools, and `cards/stat-adjusters.md` are unbucketed.

