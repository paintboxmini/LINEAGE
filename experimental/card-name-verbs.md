# Card Name Verbs

A working vocabulary for naming new cards, from Drew. Kept as a source to pull from when a gap needs filling — not a design spec, and nothing here is committed to becoming a card.

**Before using a name, check it isn't taken.** Duplicate card names are not merely untidy: `printing/generate-cards.py` resolves a set's fixed card list by name into a first-wins dict, so a collision silently prints the wrong card. That is exactly what the Red/Green BRACE duplicate did to the Oracle deck (`experimental/archives/cut-cards.md`). The list of names already in use as of 2026-09-06 is at the bottom of this file.

**Breadth is the thing to weigh.** A card's name is what a player spends outside combat on an Advantage discard, so a broad verb applies to more attempts and is worth more than a narrow one — see `rules/cards.md`, The Name Is Half the Card. Most of the words below are broad by construction, which is what makes them useful; the parser-style multi-word entries are narrower and correspondingly cheaper.

---

## Combat Maneuvers — martial, Body-leaning

Disarm · Grapple · Shove · Bash · Feint · Lunge · Parry · Riposte · Tackle · Hamstring · Stagger · Overrun · Trip · Pin · Vault · Clinch · Break · Slam · Drive · Press · Smash · Hook · Shoulder · Headbutt · Backstep · Sweep · Rush · Crush · Drag · Brace

## Mobility & Positioning

Leap · Somersault · Roll · Slide · Vault · Drop · Dive · Duck · Weave · Advance · Retreat · Circle · Flank · Pivot · Shift · Dash · Stride · Withdraw · Spring · Bound · Scramble

## Tactical — Mind-leaning

Probe · Assess · Track · Decode · Redirect · Corner · Pressure

## Soul — emotional, intent-leaning

Invoke · Rally · Encourage · Bolster · Channel · Vow · Inspire · Provoke · Challenge · Unify · Witness · Confront · Sanctify

## High-risk / flashy

Somersault · Whirl · Commit · Overcharge · Berserk · Breakthrough · Overwhelm · Unleash · Surge

## Clean one-word actions

Tight, parser-friendly verbs:

Leap · Shove · Brace · Feint · Clash · Roll · Pin · Dash · Guard · Rally · Lure · Bind · Break · Shift · Mark · Cut · Hold · Drive · Skewer · Slam · Step · Turn · Split · Catch

---

# By Colour

## Red — Body: force, position, physical control

Imply movement, HP swing, forced interaction, frontline density.

**Combat:** Disarm · Grapple · Trip · Shove · Pin · Slam · Overrun · Bash · Lunge · Sweep · Tackle · Drive · Shoulder · Crush · Hammer · Skewer · Cleave · Maul · Rush · Ram · Break

**Mobility:** Vault · Somersault · Leap · Dive · Roll · Slide · Charge · Advance · Withdraw · Climb · Drop

**Control:** Anchor · Brace · Intercept · Guard · Press · Corner · Drag · Throw

## Blue — Mind: prediction, denial, manipulation

Imply information, restriction, redirection, colour pressure, conditional advantage.

Decode · Dissect · Expose · Redirect · Probe · Evaluate · Inspect · Unravel · Deconstruct · Invert

Anchor card name: **Focused Stance**

## Green — Soul: initiative, bonds, flow, shared power

Imply tempo, unity, sacrifice, emotional pressure, shared state changes.

Rally · Bolster · Inspire · Resonate · Unite · Harmonize · Invoke · Entreat · Witness · Commit · Vow · Channel · Share · Mend · Restore · Awaken · Guide · Stir · Align *(spiritual sense)* · Bind *(relational sense)* · Release · Confront · Provoke

---

# By Mechanic

## Initiative manipulation

Imply tempo control, ordering, urgency, delay.

Surge · Accelerate · Advance · Urge · Rally · Hasten · Seize · Preempt · Cut In · Overtake · Defer · Stall · Postpone · Delay · Suspend · Lag · Reorder · Interject · Interrupt · Insert · Supplant · Override · Reclaim

**Stronger parser titles:** Seize Initiative · Cut Ahead · Hold Priority · Delay Step · Force Delay · Sudden Surge

## Evade — the pre-reveal layer

Evade inserts a step before reveal resolution, which is a surgical layer addition rather than an effect.

Slip · Fade · Blur · Skirt · Duck · Sidestep · Vanish · Flicker · Skim · Elude

**Parser style:** Preemptive Dodge · Step Aside

## Cost-based power

Where a card offsets strength with a cost, the name should imply sacrifice or strain.

**Discard cost:** Expend · Shed · Sacrifice · Purge · Abandon · Cast Off · Overextend · Gamble · Risk · Trade · Bleed

**Parser versions:** Pay in Blood · Burn Within · Overdraw · Reckless Surge

**Initiative cost:** Delay · Defer

---

## Already in use

These 22 are live card names as of 2026-09-07 and cannot be reused as-is. Recheck rather than trust this list once cards have been added or renamed — `python3 combatsimulations/cards.py` loads every card, and `printing/generate-cards.py` is what actually breaks on a collision.

Align · Awaken · Bind · Bolster · Brace · Break · Charge · Climb · Delay · Drag · Feint · Grapple · Guard · Interrupt · Lunge · Mend · Rally · Resonate · Shed · Sidestep · Surge · Witness

---

## Where the gaps are

The 2026-09-06 balance pass left the pool thin in exactly two places. One is now filled; new cards land most usefully in the other.

- **Green melee.** Filled on 2026-09-07 with MEND, BOLSTER, and AWAKEN, drawn from the Green list above. Before that the only untaken Green melee cards were BRISTLE, a mechanical duplicate of BRAMBLE, and CONSUME, and Green could not absorb another melee loss from the Oracle. It now has three benched melee cards to lose.
- **Blue melee.** Six of ten are in the Oracle; of the rest, UNNAME and TAINT are barred by the Oracle content rule (`rules/cards.md`, The Oracle Deck) and CLIMB is now spoken for.

Red has bench depth at every range.

---

## Related Documents

- `rules/cards.md` — colour conventions, the die-and-range ladder, and why a name's breadth is part of its power
- `rules/card-glossary.md` — the keywords a new card's Effect can draw on
- `experimental/archives/cut-cards.md` — cards already tried and cut, with reasons
