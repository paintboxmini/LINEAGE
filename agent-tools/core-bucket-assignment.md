# Card Bucket Assignment

**All 341 cards are bucketed** as of 2026-08-17 — the core sets first, then the remaining 198 across signature sets, location pools and stat adjusters. Cards are one-per-file in `cards/`, so nothing moves: a bucket is membership, not a destination (2026-08-17, Drew: *"record the assignment, don't move the cards yet"*).

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

## The second pass — the other 198

The first pass covered only the three core sets (143 of 341). The remaining 198 — every signature set, location pool and the stat adjusters — were classified on 2026-08-17 using the same Special Rule → Effect → Defensive Bonus ordering.

**One new bucket fell out: `stat adjustment`.** SUNDER, ERODE and WITHER changed a stat and matched nothing, because the core pass never had to classify them — they had already left the core sets into `cards/stat-adjusters.md` before bucketing started.

**A precision fix worth keeping.** Position words appear as *conditions* as often as effects, and the first run misread them: CAMOUFLAGE STRIKE (*"If you are in the Backline, gain Evade"*) filed as position rather than defense, CENSER SWING (*"If target is Frontline, deal +2 damage"*) as position rather than damage amp. Stripping `if …,` clauses before classifying — the condition is context, the remainder is what the card *does* — moved position from 69 homes down to 43 and corrected roughly twenty cards. The same fix over-tightened once and lost THE ROOM LEANS IN (*"Pull all enemies to the Frontline"*), hand-restored.

**Hand-assigned in this pass:** SIGNATURE THRUST → position (it manipulates glyphs, which are Objects and position-anchored), BECOMING → card flow (permanent hand replacement), FOLLOW-UP → buff removal (it copies another card wholesale), ANOTHER JOINT → control (Staggered is its unconditional effect; the Rooted is conditional escalation), THE ROOM LEANS IN → position.

## Counts

| Bucket | Homes | Indexed |
|---|--:|--:|
| **position** | 73 | 91 |
| **control** | 49 | 55 |
| **damage amp** | 46 | 62 |
| **defense** | 41 | 110 |
| **card flow** | 27 | 41 |
| **team support** | 25 | 32 |
| **initiative** | 16 | 25 |
| **sustain** | 14 | 22 |
| **self-inflicted cost** | 11 | 11 |
| **hand denial** | 11 | 13 |
| **status inserters** | 9 | 9 |
| **buff removal** | 5 | 7 |
| **payoff** | 4 | 5 |
| **rps manipulation** | 5 | 5 |
| **stat adjustment** | 3 | 3 |
| **cleansing** | 1 | 1 |
| **plain attack** | 1 | 1 |
| **misc** | 0 | 1 |
| | **341** | |

### position — 73 homed, 91 indexed

Moving yourself or someone else, or gaining something for holding still. Anchored, Rooted, Rushdown, Quick, Objects and glyphs, Position-gated payoffs.

BIND, BOLT, BORROWED SCREAM → control, BOUND TO THE STONE → defense, CALCULATE, CARRION PULL → defense, CENSURE, CHARGE, CLOSE THE TANGLE → damage amp, COIL DROP → defense, CRAWL LANE, DART, DEAD END, DIG IN, DRAG UNDER → sustain, DUST → control, ENVELOP, ENVELOPING PRESS → defense, FLOW, FOLLOWS WARMTH, FOOTWORK, FRACTURE → card flow, GORE, GRAFT, SUBDUE, GROUNDING STANCE → defense, HARVEST CHAIN → defense, HAUL, HEAVE, HEAVE AND HAUL, IMPALING DIVE, INK THE AIR → card flow, IRON GRIP, KEEPING PEOPLE OUT, LIGHTNING DASH, LOW GREY HAZE → defense, LUNGE, MIRROR STEP, NO VACANCY → defense, NOT WHERE YOU LEFT IT, OFF THE EDGE → defense, PARTITION → team support, PATIENCE OF STONE → damage amp, PATTERN READ → card flow, PINCH → defense, PULL, PUSH, QUICKSTEP, REALIGNMENT, REPEL, ROLLING THUNDER, ROOT LASH, ROOTED OATH, RUSTLE AND GONE → defense, SEED → damage amp/defense, SEISMIC REDIRECT → damage amp, SHED → defense, SIGNATURE THRUST, SLIPSTREAM → defense, STARING CONTEST, STEP ASIDE → defense, STILL POINT → defense, SWAY, SYSTEM PURGE → defense, TALON RUSH, THE LEDGER NEVER CLOSES → card flow, THE ROOM LEANS IN, TRAMPLE, UNDERBRUSH DASH, VOLT → damage amp, WATCHFUL PERCH → initiative, WITHERING GLYPH, YOUR OWN HEARTBEAT

*Also indexed here:* ANOTHER JOINT, ASHBURY, BINDING RITE, CAMOUFLAGE STRIKE, COIL LATCH, DRAG, FOGBURST, FROM ABOVE, KNOWN GROUND, OVERDRIVE, PATIENCE, RALLY, SIDESTEP, SLIP THE BLADE, SLITHER LUNGE, THORN-BIND, THORNFAST, TITHE COLLECTION

### control — 49 homed, 55 indexed

Taking away what a target can do or how well they do it.

AFTERIMAGE → defense, ANOTHER JOINT → damage amp/defense/position, ATTRITION, AXIOM, BLINDSIDE, CALIBRATION PULSE → card flow, CALLED SHOT → defense, CAMOUFLAGE SHIFT → defense, CERTAIN STRIKE → defense, CUT OFF → defense, DARK CORRIDOR → defense, DEAD RECKONING, DEPTH SLAM, DIRGE → defense, DOWNWARD, FOGBURST → position, INEVITABILITY, INK BURST → defense, INTIMIDATE, IRON ANCHOR → defense, LABYRINTH ECHO, MARKED, NO FACE, NOTHING TO READ, OPEN GUARD, OPENING, PETAL FEINT → defense, PREDICT, REBUTTAL → initiative, REELING, REFRACT, SEALED CHORD, SECOND GUESS, SHIELD BASH → defense, SLOW HANDS, SNUFF → defense, SURGE, TARGETING LOCK → card flow, TELL, THE EASIEST SHAPE → card flow, THE HELD NOTE, THIN SKIN, THORN-BIND → position, TWIN STRIKE, UNDERTOW → defense, VEIL, VENOM MIND → defense, WARNING SHOT → defense, WATCHES FEET → card flow

*Also indexed here:* ANTICIPATE, BERSERKER'S PRICE, BORROWED SCREAM, DUST, FEINT, VOID

### damage amp — 46 homed, 62 indexed

Making damage bigger or landing it where it otherwise would not.

ADAPTIVE BITE, ASHBORN FLARE → sustain, BORROWED POWER → defense, BRAMBLE, BREAK, BRISTLE, CENSER SWING, CHAIN, CHAIN REACH, COIL LATCH → position, CRYSTAL EDGE, DEAD HEAT, DRAG → position, EXPOSED → defense, FAULT EXPLOIT → defense, FENCE-POST REACH, FROM ABOVE → position, GAMBLER'S RUIN, HEADLONG → defense, HEAT TRACE → defense, IDLE TO ENGAGE, LIMB-SNAPPER, NEEDLE BITE → defense, NIP, NIP AND TEAR → sustain, NOTHING PERSONAL → initiative, OBSIDIAN SIX, OPEN FIRE, PATIENCE → position, PATIENT WAIT → defense, RETALIATE → initiative, RETORT, SLITHER LUNGE → position, SPARK OF VIOLENCE, SPLINTER-BURST, STRIKE, THE FIELD IS THE LINE → defense, THE PACK REMEMBERS → defense, THERMAL VECTOR → defense, THRESHOLD → initiative, THUNDERBOLT STRIKE, THUNDERCLAP, TWINE AND WEIGHT, TWO POLES, VENT CYCLE → defense, WIDE SWING

*Also indexed here:* ANOTHER JOINT, BLOOD IN THE GAP, CLOSE THE TANGLE, CUTS BOTH WAYS, DEFLECT, MAWS, PAIN IS FUEL, PATIENCE OF STONE, ROLLOUT, SACRIFICE STRIKE, SEED, SEISMIC REDIRECT, SHARPEN, STITCHED CASE, VOLT, YOU'RE NEXT

### defense — 41 homed, 110 indexed

Refusing or reducing incoming damage, including untargetability.

ASH REDIRECT, BLOOM STILLNESS, BRACE, CAMOUFLAGE STRIKE → position, CINDER SPIRAL, CRIMSON MIRROR, CURRENT SENSE, DEFLECT → damage amp, DISSOLVE CONTACT, EMBER CIRCLE, ENDURE → sustain, FEEDING FRENZY, FELT YOU COMING, FLATTEN, FORESEEN, GIVE WAY, GUTTERING, HULLGUARD, INSTINCT, INTERCEPT, LAST RESORT, MIMICRY PULSE, MIRROR CIRCLE, OUT OF REACH, PAIN IS FUEL → damage amp, PECK, SETTLE, SHADE AWAY, SHED SKIN → card flow, SHROUD, SIDESTEP → position, SKITTER AWAY, SLIP THE BLADE → position, STEADFAST, STILL AS LITTER, STILL COUNTING, STITCHED CASE → damage amp, THORN CIRCLE, UNBROKEN, UNTOUCHED, VERDANT WARD

*Also indexed here:* AFTERIMAGE, ALWAYS ONE MORE, ANOTHER JOINT, ASH EXHAUST, BORROWED POWER, BOUND TO THE STONE, CALLED SHOT, CAMOUFLAGE SHIFT, CARRION PULL, CERTAIN STRIKE, COIL DROP, COLD READ, CORRECTION LOAD, CUT OFF, DARK CORRIDOR, DIRGE, DUSK COUNT, EMBER WARD, ENVELOPING PRESS, EXPOSED, FAULT EXPLOIT, FREEZE, GENETIC SAMPLE, GROUNDING STANCE, HALF-SEEN, HARVEST CHAIN, HEADLONG, HEAT TRACE, HOLD FAST, INCENSE WARD, INK BURST, IRON ANCHOR, LOW GREY HAZE, NEEDLE BITE, NO VACANCY, OFF THE EDGE, PARADOX, PATIENT WAIT, PETAL FEINT, PINCH, REGISTERED, RESIST BLESSING, ROLLOUT, RUSTLE AND GONE, SEED, SENSE THE SPENT, SHARED BURDEN, SHED, SHIELD BASH, SIDELONG SCUTTLE, SIPHON, SLIPSTREAM, SNUFF, STEP ASIDE, STILL POINT, SYNCHRONY, SYSTEM PURGE, TABLE STAKES, THE FIELD IS THE LINE, THE PACK REMEMBERS, THE WOOL IS MUSCLE, THERMAL VECTOR, THORN LARDER, TOO HIGH TO HEAR, UNDERTOW, VENOM MIND, VENT CYCLE, WARNING SHOT, WEATHERED

### card flow — 27 homed, 41 indexed

Moving your own cards around.

ACCEPTANCE → initiative, ALIGN, ANTICIPATE → control, ATTUNE, AZURE MIRROR, AZURE WARD, BECOMING, CASE FILE, CLAY BOWL, CLIMB, COLD READ → defense, COMMUNION → team support, FOCUS → initiative, FREEZE → defense, GENETIC SAMPLE → defense, MAZE SENSE, PROFILE, REGISTERED → defense, STEADY HAND, STILL GROUND, STUDY, SURVEY, THORN LARDER → defense, TOO HIGH TO HEAR → defense, TRUTINATE SIGNAL, VIBRATION LOCK, WHERE IT'S GATHERING

*Also indexed here:* BURN BRIGHT, CALIBRATION PULSE, FOREST MEMORY, FORGET, FRACTURE, INK THE AIR, PATTERN READ, PRECISE REMOVAL, SHED SKIN, SILK THREAD MEASURE, TARGETING LOCK, THE EASIEST SHAPE, THE LEDGER NEVER CLOSES, WATCHES FEET

### team support — 25 homed, 32 indexed

Aimed at an ally.

AID, BARBED GLYPH, CARRIED WOUND, CIPHER GLYPH, CLIFF SONG, CUTS BOTH WAYS → damage amp, EMBER WARD → defense, ENTWINED, GUARD, HONING GLYPH, INCENSE WARD → defense, KNOWN GROUND → position, MENDING GLYPH, PACK LOGIC → sustain, RENEWAL, RESIST BLESSING → defense, RESONATE, SANCTUARY, SHARPEN → damage amp, SUPPORT, SYNCHRONY → defense, THORNFAST → position, VERDANT MIRROR, WARSONG → initiative, WITNESS

*Also indexed here:* BLOOD TITHE, COMMUNION, FRAME-TRAP, GENERATIONS OF HANDS, PARTITION, SHARED BURDEN, TABLE STAKES

### initiative — 16 homed, 25 indexed

Turn order: Initiative Shift, acting first, extra or skipped turns.

DELAY, DISTRACT, DOUBLE DOWN, DUSK COUNT → defense, EVEN CHURN, FACING YOU NOW, HESITATE, INTERRUPT, MIRING GLYPH, MOCKERY, QUICKEN, RHYTHM BREAK, SIDELONG SCUTTLE → defense, URGENCY, YOU'RE NEXT → damage amp, YOUR TURN WILL COME

*Also indexed here:* ACCEPTANCE, FOCUS, NOTHING PERSONAL, REBUTTAL, RETALIATE, STEAL, THRESHOLD, WARSONG, WATCHFUL PERCH

### sustain — 14 homed, 22 indexed

Getting HP back.

ALWAYS ONE MORE → defense, BLOOD IN THE GAP → damage amp, CONSUME, DISSOLVE AND KEEP, FOREST MEMORY → card flow, GENERATIONS OF HANDS → team support, HOLD FAST → defense, MAWS → damage amp, PHOENIX'S LAST BREATH, RECOVER, THE WOOL IS MUSCLE → defense, TITHE COLLECTION → position, UNDERSTANDING, WEATHERED → defense

*Also indexed here:* ASHBORN FLARE, DRAG UNDER, EMERGENCY REPAIRS, ENDURE, NIP AND TEAR, PACK LOGIC, PARADOX, PRESS THE WOUND

### self-inflicted cost — 11 homed, 11 indexed

A benefit bought with a real price paid by the user.

BALANCE, BERSERKER'S PRICE → control, BLOOD TITHE → team support, EMERGENCY REPAIRS → sustain, OVERDRIVE → position, RALLY → position, SACRIFICE STRIKE → damage amp, SHARED BURDEN → defense/team support, STEAL → initiative/misc, TABLE STAKES → defense/team support, UNMAKE → buff removal

### hand denial — 11 homed, 13 indexed

Reaching into a hand you cannot see.

ASH EXHAUST → defense, CRIMSON WARD, FEINT → control, FORGET → card flow, HALF-SEEN → defense, PRECISE REMOVAL → card flow, READ, SILK THREAD MEASURE → card flow, STILLNESS, UNNAME, VOID → control

*Also indexed here:* FIELD MEDICINE, PRESS THE WOUND

### status inserters — 9 homed, 9 indexed

Putting status cards into someone else's deck or hand.

ASHBURY → position, BINDING RITE → position, CORRECTION LOAD → defense, RAKING CUT, REND, SENSE THE SPENT → defense, SMALL DOSES, TAINT, TWO CUTS

### buff removal — 5 homed, 7 indexed

Taking from the opponent — stripping, stealing, or copying what they already have.

DRAIN, FOLLOW-UP, LEVEL THE FIELD, SIPHON → defense, WAITING GAME

*Also indexed here:* TRACE, UNMAKE

### payoff — 4 homed, 5 indexed

Cashes in a condition that already exists.

BURN BRIGHT → card flow, PRESS THE WOUND → hand denial/sustain, ROLLOUT → damage amp/defense, TRACE → buff removal

*Also indexed here:* FRAME-TRAP

### rps manipulation — 5 homed, 5 indexed

Changing how the reveal itself resolves.

ADAPT, CERTAINTY, EQUAL FOOTING, FRAME-TRAP → payoff/team support, PARADOX → defense/sustain

### stat adjustment — 3 homed, 3 indexed

Changing one of the three stats for a combat.

ERODE, SUNDER, WITHER

### cleansing — 1 homed, 1 indexed

Removing status cards that are already there.

FIELD MEDICINE → hand denial

### plain attack — 1 homed, 1 indexed

No effect on any line.

OVERCOMMIT

### misc — 0 homed, 1 indexed

Behaviours with exactly one card in the corpus.

*(none homed here)*

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
- **Bucket file names.** `cards/buckets/` holds one list per bucket; nothing in `cards/` moves, since each card already has its own file.

