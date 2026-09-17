# Card Name Verbs

A working vocabulary for naming new cards, from Drew. Kept as a source to pull from when a gap needs filling — not a design spec, and nothing here is committed to becoming a card.

**Names already used by a card have been struck from these lists**, so anything still written here was free as of the last strike — 2026-09-17, when 27 names the file was still offering turned out to be held by cards. Re-check anyway before committing to one — this file goes stale the moment a card is added or renamed, and duplicate names are not merely untidy: `printing/generate-cards.py` resolves a set's fixed card list by name into a first-wins dict, so a collision silently prints the wrong card. That is exactly what the Red/Green BRACE duplicate did to the Oracle deck (`experimental/archives/cut-cards.md`). To re-check: `python3 combat-simulations/cards.py` loads every card, and `by_name()` in that module is the same lookup the printer builds.

**Breadth is the thing to weigh.** A card's name is what a player spends outside combat on an Advantage discard, so a broad verb applies to more attempts and is worth more than a narrow one — see `rules/cards.md`, The Name Is Half the Card. Most of the words below are broad by construction, which is what makes them useful; the parser-style multi-word entries are narrower and correspondingly cheaper.

---

## Combat Maneuvers — martial, Body-leaning

Disarm · Shove · Bash · Parry · Riposte · Tackle · Hamstring · Stagger · Overrun · Trip · Pin · Vault · Clinch · Slam · Drive · Press · Smash · Hook · Headbutt · Backstep · Sweep · Rush · Crush

## Mobility & Positioning

Leap · Somersault · Roll · Slide · Vault · Drop · Dive · Duck · Weave · Advance · Retreat · Circle · Flank · Pivot · Shift · Dash · Stride · Withdraw · Spring · Bound · Scramble

## Tactical — Mind-leaning

Assess · Track · Pressure

## Soul — emotional, intent-leaning

Invoke · Encourage · Vow · Inspire · Challenge · Sanctify

## High-risk / flashy

Somersault · Whirl · Commit · Overcharge · Berserk · Breakthrough · Overwhelm · Unleash

## Clean one-word actions

Tight, parser-friendly verbs:

Leap · Shove · Clash · Roll · Pin · Dash · Lure · Shift · Mark · Cut · Hold · Drive · Slam · Step · Split · Catch

---

# By Colour

## Red — Body: force, position, physical control

Imply movement, HP swing, forced interaction, frontline density.

**Combat:** Disarm · Trip · Shove · Pin · Slam · Overrun · Bash · Sweep · Tackle · Drive · Crush · Rush · Ram

**Mobility:** Vault · Somersault · Leap · Dive · Roll · Slide · Advance · Withdraw · Drop

**Control:** Intercept · Press · Throw

## Blue — Mind: prediction, denial, manipulation

Imply information, restriction, redirection, colour pressure, conditional advantage.

Expose · Evaluate · Inspect · Deconstruct

Anchor card name: **Focused Stance**

## Green — Soul: initiative, bonds, flow, shared power

Imply tempo, unity, sacrifice, emotional pressure, shared state changes.

Inspire · Unite · Invoke · Commit · Vow · Share · Restore

---

# By Mechanic

## Initiative manipulation

Imply tempo control, ordering, urgency, delay.

Accelerate · Advance · Urge · Seize · Preempt · Cut In · Overtake · Defer · Stall · Postpone · Suspend · Lag · Reorder · Interject · Insert · Supplant · Override · Reclaim

**Stronger parser titles:** Seize Initiative · Cut Ahead · Hold Priority · Delay Step · Force Delay · Sudden Surge

## Evade — the pre-reveal layer

Evade inserts a step before reveal resolution, which is a surgical layer addition rather than an effect.

Slip · Fade · Blur · Skirt · Duck · Vanish · Flicker · Skim · Elude

**Parser style:** Preemptive Dodge

## Cost-based power

Where a card offsets strength with a cost, the name should imply sacrifice or strain.

**Discard cost:** Sacrifice · Purge · Cast Off · Overextend · Gamble · Risk · Trade

**Parser versions:** Pay in Blood · Burn Within · Overdraw · Reckless Surge

**Initiative cost:** Defer

---

## Where the gaps are

The 2026-09-06 balance pass left the pool thin in exactly two places. One is now filled; new cards land most usefully in the other.

- **Green melee.** Filled on 2026-09-07 with MEND, BOLSTER, and AWAKEN, all three taken from the Green list above and struck from it. Before that the only untaken Green melee cards were BRISTLE and CONSUME. Green now has bench depth at melee; the Oracle's three melee seats are BIND, SMOKESCREEN and BRISTLE, with BOLSTER, AWAKEN and CONSUME behind them.
- **Blue melee — still the thinnest place in the pool, and it got thinner.** Six of ten are in the Oracle; of the rest, TAINT is barred by the Oracle content rule (`rules/cards.md`, The Oracle Deck) and CLIMB is now spoken for. UNNAME was barred by that rule too until its 2026-09-08 rewrite cleared it, but on 2026-09-17 both UNNAME and UNRAVEL failed the early-campaign screen (`rules/early-campaign-cards.md`). That leaves CORNER as the only Blue melee card in the pool that is both legal and early-appropriate, against two melee seats the expansion needs filled. **This is where a new card is most worth writing.**

### Blue melee names still free

Checked against all 377 cards on 2026-09-17. The hard part is that Blue's own vocabulary leans observational, and watching reads as Ranged — a Blue melee name has to be a *mind at contact range*, which is a narrower thing than the Blue list was built for.

**Best fits.**

- **PRESSURE** — crowding somebody so their options close. Contact-range by nature, and restriction is squarely Blue's brief. Nothing anywhere near it in the pool.
- **CLINCH** — the file files it under martial, but holding someone where they cannot work is denial, not force. Clean, narrow, no collisions.
- **EXPOSE** — from Blue's own list. Caveat: EXPOSED was cut on 2026-09-07 along with the Critical keyword, and MARKED took over its slot in the Trisect decklist. The concepts overlap and MARKED is seated in the Oracle.
- **PARRY** / **RIPOSTE** — prediction at contact, which is Blue however the martial list files them. Caveat: DEFLECT and RETALIATE already hold the Counter Attack shapes, so these would need to be something else.
- **INTERCEPT** — reading where it is going and arriving first. Caveat: this was a Red d4 Melee card until 2026-09-06, when GUARD absorbed it (`experimental/archives/cut-cards.md`). The name is free; a reader who knows the archive may expect the old card.

**Free, but they read Ranged.** ASSESS · TRACK · INSPECT · EVALUATE · DECONSTRUCT — all observation verbs. TRACK also sits beside the cut TRACK SIGN.

**Traps.** STAGGER collides with the near-banned Staggered keyword. MARK, PIN, PRESS and DELAY STEP are one letter or one word from MARKED, PINNED, PRESS THE WOUND and DELAY. PREEMPT, SEIZE, CUT IN and HOLD PRIORITY are strong words, but ANTICIPATE already holds "read it coming" in Blue melee.

**Still unclaimed:** the anchor name this file gives Blue, **Focused Stance**.

Red has bench depth at every range.

---

## Related Documents

- `rules/cards.md` — colour conventions, the die-and-range ladder, and why a name's breadth is part of its power
- `rules/card-glossary.md` — the keywords a new card's Effect can draw on
- `experimental/archives/cut-cards.md` — cards already tried and cut, with reasons
