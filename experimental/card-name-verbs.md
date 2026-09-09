# Card Name Verbs

A working vocabulary for naming new cards, from Drew. Kept as a source to pull from when a gap needs filling — not a design spec, and nothing here is committed to becoming a card.

**Names already used by a card have been struck from these lists**, so anything still written here was free as of 2026-09-07. Re-check anyway before committing to one — this file goes stale the moment a card is added or renamed, and duplicate names are not merely untidy: `printing/generate-cards.py` resolves a set's fixed card list by name into a first-wins dict, so a collision silently prints the wrong card. That is exactly what the Red/Green BRACE duplicate did to the Oracle deck (`experimental/archives/cut-cards.md`). To re-check: `python3 combatsimulations/cards.py` loads every card, and `by_name()` in that module is the same lookup the printer builds.

**Breadth is the thing to weigh.** A card's name is what a player spends outside combat on an Advantage discard, so a broad verb applies to more attempts and is worth more than a narrow one — see `rules/cards.md`, The Name Is Half the Card. Most of the words below are broad by construction, which is what makes them useful; the parser-style multi-word entries are narrower and correspondingly cheaper.

---

## Combat Maneuvers — martial, Body-leaning

Disarm · Shove · Bash · Parry · Riposte · Tackle · Hamstring · Stagger · Overrun · Trip · Pin · Vault · Clinch · Slam · Drive · Press · Smash · Hook · Shoulder · Headbutt · Backstep · Sweep · Rush · Crush

## Mobility & Positioning

Leap · Somersault · Roll · Slide · Vault · Drop · Dive · Duck · Weave · Advance · Retreat · Circle · Flank · Pivot · Shift · Dash · Stride · Withdraw · Spring · Bound · Scramble

## Tactical — Mind-leaning

Probe · Assess · Track · Decode · Redirect · Corner · Pressure

## Soul — emotional, intent-leaning

Invoke · Encourage · Channel · Vow · Inspire · Provoke · Challenge · Unify · Confront · Sanctify

## High-risk / flashy

Somersault · Whirl · Commit · Overcharge · Berserk · Breakthrough · Overwhelm · Unleash

## Clean one-word actions

Tight, parser-friendly verbs:

Leap · Shove · Clash · Roll · Pin · Dash · Lure · Shift · Mark · Cut · Hold · Drive · Skewer · Slam · Step · Turn · Split · Catch

---

# By Colour

## Red — Body: force, position, physical control

Imply movement, HP swing, forced interaction, frontline density.

**Combat:** Disarm · Trip · Shove · Pin · Slam · Overrun · Bash · Sweep · Tackle · Drive · Shoulder · Crush · Hammer · Skewer · Cleave · Maul · Rush · Ram

**Mobility:** Vault · Somersault · Leap · Dive · Roll · Slide · Advance · Withdraw · Drop

**Control:** Anchor · Intercept · Press · Corner · Throw

## Blue — Mind: prediction, denial, manipulation

Imply information, restriction, redirection, colour pressure, conditional advantage.

Decode · Dissect · Expose · Redirect · Probe · Evaluate · Inspect · Unravel · Deconstruct · Invert

Anchor card name: **Focused Stance**

## Green — Soul: initiative, bonds, flow, shared power

Imply tempo, unity, sacrifice, emotional pressure, shared state changes.

Inspire · Unite · Harmonize · Invoke · Entreat · Commit · Vow · Channel · Share · Restore · Guide · Stir · Release · Confront · Provoke

---

# By Mechanic

## Initiative manipulation

Imply tempo control, ordering, urgency, delay.

Accelerate · Advance · Urge · Hasten · Seize · Preempt · Cut In · Overtake · Defer · Stall · Postpone · Suspend · Lag · Reorder · Interject · Insert · Supplant · Override · Reclaim

**Stronger parser titles:** Seize Initiative · Cut Ahead · Hold Priority · Delay Step · Force Delay · Sudden Surge

## Evade — the pre-reveal layer

Evade inserts a step before reveal resolution, which is a surgical layer addition rather than an effect.

Slip · Fade · Blur · Skirt · Duck · Vanish · Flicker · Skim · Elude

**Parser style:** Preemptive Dodge

## Cost-based power

Where a card offsets strength with a cost, the name should imply sacrifice or strain.

**Discard cost:** Expend · Sacrifice · Purge · Abandon · Cast Off · Overextend · Gamble · Risk · Trade · Bleed

**Parser versions:** Pay in Blood · Burn Within · Overdraw · Reckless Surge

**Initiative cost:** Defer

---

## Where the gaps are

The 2026-09-06 balance pass left the pool thin in exactly two places. One is now filled; new cards land most usefully in the other.

- **Green melee.** Filled on 2026-09-07 with MEND, BOLSTER, and AWAKEN, all three taken from the Green list above and struck from it. Before that the only untaken Green melee cards were BRISTLE and CONSUME. Green now has bench depth at melee; the Oracle's three melee seats are BIND, SMOKESCREEN and BRISTLE, with BOLSTER, AWAKEN and CONSUME behind them.
- **Blue melee.** Six of ten are in the Oracle; of the rest, UNNAME and TAINT are barred by the Oracle content rule (`rules/cards.md`, The Oracle Deck) and CLIMB is now spoken for.

Red has bench depth at every range.

---

## Related Documents

- `rules/cards.md` — colour conventions, the die-and-range ladder, and why a name's breadth is part of its power
- `rules/card-glossary.md` — the keywords a new card's Effect can draw on
- `experimental/archives/cut-cards.md` — cards already tried and cut, with reasons
