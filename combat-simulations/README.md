# Combat Simulator

A playable engine for Tales Untold combat — drives a fight turn by turn so
an encounter can be played out away from the table. Rebuilt from the ground
up on 2026-09-06; nothing here carries over from whatever was here before.

Pure standard-library Python 3, no dependencies, same convention as
`printing/`.

## Running it

```
python3 play.py                 # demo fight, both sides played by the AI
python3 play.py --human         # you play the first party member
python3 play.py --seed 7        # reproducible
python3 play.py --rounds 40     # lap cap before it calls a draw
python3 play.py --quiet         # result only

python3 test_wheel.py           # the initiative-shift worked cases
python3 test_invariants.py      # rules/invariants.md, Confirmed
python3 test_effects.py         # the keyword rulings, through the cards
python3 effects.py              # how much of the pool compiles
python3 cards.py                # card counts, as a load check

python3 encounter_budget.py     # how many of each creature is a fight
python3 encounter_budget.py harlock ocellus --runs 1000
```

## What's here

| File | |
|---|---|
| `cards.py` | Loads `cards/*.md` directly — the markdown is the source of truth, same as `printing/` treats it. Parses name, colour, stat, die and range; carries Effect text verbatim. |
| `effects.py` | Reads Effect and Defense Effect prose and compiles the regular part of it into operations. A half either compiles whole or narrates; nothing half-applies. `python3 effects.py -v` lists what still narrates. |
| `wheel.py` | The initiative wheel and Initiative Shift, including the chip rules. Also the two reorders that are not shifts — PRIORITY's swap and STARING CONTEST's move — which slide nothing and place no chips. |
| `engine.py` | Combatants, statuses, the damage pipeline, and Attack Resolution. |
| `agents.py` | Who decides: `HumanAgent` prompts at the terminal, `SimpleAI` plays to type, `RandomAgent` plays legally at random. Any mix can share a table. |
| `play.py` | Turn loop and CLI. |
| `encounter_budget.py` | Sweeps opponent *count* against the written party and reports where a fight stops being free and starts being lethal. Count is the balance lever, so this varies count rather than stats. Reads stat blocks straight out of `bestiary/` and `characters/`, and checks the engine's derived HP against the published one on the way past. Conclusions live in `rules/gm-guide.md`, How many of them. |
| `test_wheel.py` | `rules/initiative-shift-examples.md` as assertions. |
| `test_invariants.py` | `rules/invariants.md`, Confirmed, as assertions — derived stats stay live under stat changes, and card count is conserved per combatant across 600 randomised fights, both agents. |
| `test_effects.py` | `rules/card-glossary.md` as assertions, through the cards that use each keyword. |

`rules/invariants.md` is the specification this is checked against.

## What it does and doesn't resolve

The engine resolves the **structured** part of a fight: initiative and the
wheel, drawing to hand size, range legality, the Blind/Evade checks and
their resolution order, the RPS reveal, the damage pipeline, Collapse and
death, and positioning.

Card Effects are read by `effects.py` in two ways. Most halves compile into
**operations** the engine runs — grants and their stacking, healing and HP costs, damage, draw,
discard, Exile, Scry, movement, Initiative Shift, stat drain, Counter
Attack, Lifesteal, Rushdown, buff stripping and stealing, Wound and
Exhaust insertion, modal cards where only the chosen branch runs, optional
costs, and the gates around them (clean-win-only, HP thresholds).

A few are not operations at all but **traits** of the card while the
exchange resolves — "Wins ties" is not something you do, it is something
the reveal has to ask about. Those are read off the card once and consulted
by `resolve_attack`: winning ties and the mutual cancel, REBUTTAL's floor
on losing, PARADOX reversing the outcome, CERTAIN STRIKE ignoring Evade and
Resist, INVERT and DEAD HEAT silencing the other half, DOUBLE DOWN and
TRAMPLE handing back a turn, and PLANT and STEAL changing where the card
goes afterwards. **Special Rule lines live here and nowhere else**: seven
core cards carry one, every one of them is about resolution, and until this
existed nothing read them at all.

**An Effect gets a look in before the damage it modifies.** A half resolves
in two phases: the ops that change this attack's damage run before the
roll, and everything else after it has landed. The split matters on a card
that does both — MAUL grants Deadly *and* adds +2 to this attack, and
Deadly has to stay in the second phase or it would be spent on the very
roll it is meant to improve next time.

Effects that wait are held as **pending** state on the combatant, in two
shapes that share one lifetime. A *reaction* carries ops and runs them when
its event fires — WEATHERED on being damaged, SEED on beginning a turn where
it was planted, Anchored at the start of every turn. A *restriction* carries
none: the engine asks whether one is in force before playing a colour,
moving, attacking, or triggering a Defense Effect. Expiry is measured
against the turn of whoever played the card, not whoever is holding it,
because that is what "until your next turn" says on the card.

Run `python3 effects.py` for the live figure; it was 297/319 (93%) when this
paragraph was written — 289 compiling and 8 read as traits — and
**166/166 across the 84 cards actually seated in a printed set**.

**A half either compiles completely or narrates.** Partial execution is the
one outcome worth avoiding: an effect that grants the buff and quietly
drops the "and draw 1" produces a wrong fight that reports as a right one.
When any clause fails to read, the whole half is printed for whoever is
playing — the behaviour every card had before `effects.py` existed.

The remaining third is narrated on purpose. Most of it needs a judgement a
person makes at the table (BECOMING rewriting a deck permanently, FOLLOW-UP
copying another card, PRESS THE WOUND counting status cards), or a hook the
engine does not have yet (ANTICIPATE and PUNISH winning ties, AXIOM banning
a colour on the next reveal). `python3 effects.py -v` lists them.

Statuses the engine tracks (Deadly, Weak, Resist, Vulnerable, Evade, Blind,
Rooted, Staggered, Thorns, Armour, Ward, Quick, Immunity, Protect) can also
be set on a `Combatant` directly, so a narrated Effect that grants one can
be applied by hand and the engine honours it from then on.

Current as of the 2026-09-06 rules, including that day's changes: the
always-roll Blind/Evade order and the Mutual Miss outcome, Immunity scoped
to damage inside the pipeline, Cover Evade as a persistent dodge distinct
from the Evade keyword, and Down combatants defending normally.

Not yet implemented: free actions (the engine gives one Action per turn),
Anchored's start-of-turn triggers, Ongoing Effects, summoning mid-fight
(`wheel.add_after` exists but nothing calls it), and multi-target Effects.

## The marker rule

Every worked case in `rules/initiative-shift-examples.md` passes, layout and
turn sequence both. Getting there took one non-obvious rule, worth stating
because it is easy to implement wrongly and the wrong version passes three
of the five cases:

**The marker belongs to a slot, not to a combatant.** When a turn ends,
if the acting token is still on the marker's slot then that slot is spent
and the marker moves on. But if a shift slid the acting token away and
another token slid in behind it, the marker has not finished with its own
slot — the new occupant acts, and the marker does not move.

That is the difference between Example 1 (a stays put, so the marker moves
on to c) and Example 2 (a is slid to the far slot, b slides in underneath,
and b acts). A bonus turn spends the marker's slot exactly as an ordinary
turn does, which is what makes Example 3 come out right.

Example 5 was corrected in the source file on 2026-09-06 as part of this
rebuild: it previously read "no bonus, no skip" on geometry identical to
Example 3's bonus case. Example 3 governs, per Drew.

## What measuring the party characters actually found

*2026-09-19. Recorded because two of these were mistakes in how the
question was asked, and the next person should not repeat them.*

**Two artifacts, both mine, both of which read as findings about a
character:**

- **The enemy AI had a scapegoat.** `choose_action` picked its target with
  `min(reachable, key=lambda f: f.hp)` — raw HP, and `min` breaks a tie by
  list order. With two party members on equal HP, every creature in every
  fight picked the same one, every turn. Measured over 250 fights: whoever
  was listed first of two 18 HP characters took ~1600 attacks and went down
  62–71% of the time, the other took ~700 and went down under 30%, **and
  the two swapped when the list was reordered.** Fixed — it reads the HP
  fraction now, the same definition `choose_target` in the same class was
  already using, and ties break at random.
- **The draft was doing the comparing.** A hand-built fill gave the
  Blue-primary character utility cards and the Red-primary one STRIKE at
  d10. Once the fill was a real random colour-matched draft, the gap
  between those two characters mostly went away.

**What survived, measured over 400 fights with a random draft:**

- **Kevin's gear economy is the whole of his lead, and it is not his
  dice.** He deals ~4.8 damage an attack against ~2.8 and ~3.1 for the
  other two. Cutting GRIND SHOT from d8 to d6 changed nothing at all
  (5.1). Taking away his loads, oranges and drinks dropped him to **3.3 —
  level with everyone else — and cost the party ten points of win rate,
  85% to 75%.** The proposed die lever was wrong; the lever is supply.
  That is `campaign/kevin.md`'s own design note, confirmed rather than
  assumed.
- **The core pool's dice are colour-skewed, and that is the design rather
  than a finding.** Mean die by colour is Red 6.27, Blue 5.36, Green 5.04 —
  which this file first recorded as a quirk worth watching. It is not. **The
  die is bought with range, and each colour spends its range budget
  differently**: Red is 53% Melee, Blue 60% Ranged, Green 56% Both. Sort the
  same cards by range and ignore colour and the ordering is identical —
  **Melee d6.44, Ranged d5.39, Both d4.93** — so restriction is the driver
  and the colour spread falls out of it. Now written up properly at
  `rules/cards.md`, Why Red has the biggest dice. *The lesson for anyone
  measuring here: a number that looks like an imbalance may be a rule
  nobody had written down yet, so ask before reporting.*
- **A Both-range deck defends far more often.** The character who could
  not legally block only 33% of the time, against ~50% for the other two,
  was the one whose cards are mostly Both. Unglamorous and real.

## What Passives are actually for

*2026-09-19. This section replaces one that said hand size was the dominant
stat in the game. That was wrong, and it was wrong because the measurement
left Passives out.*

The question was whether Red's die premium should close now that Body
weighs ×4 on HP instead of ×3. Three archetypes, stats rotated, nine cards
drafted at random from the core pool at each one's colour split, 500 duels
a pairing — so the only thing differing is which stat is primary. Each one
carries **two generic Passives in its primary colour**, in the canonical
shape `rules/character-creation.md` prices: one committed to Melee for the
d6, one Both at the d4 default.

| | Red B4 | Blue M4 | Green S4 | spread |
|---|---|---|---|---|
| **with Passives** | 50.5% | 50.4% | 49.1% | **1.4** |
| with Passives, hand forced equal | 50.4% | 50.1% | 49.5% | 0.9 |
| **without Passives** | 56.0% | 63.7% | 30.3% | 33.4 |
| without, Body ×3 | 54.3% | 65.8% | 29.9% | 35.9 |
| without, Red Melee d10s → d8 | 54.7% | 66.7% | 28.6% | 38.1 |

**The stat economy is balanced, and Passives are what balance it.** Three
points fall out:

- **With Passives the three colours are within 1.4 points of each other.**
  Nothing needs adjusting. The Red die premium is doing its job at about
  the right size, and the ×3 → ×4 change created no debt for it to repay.
- **Forcing hand size equal then changes almost nothing** (1.4 → 0.9). Hand
  size is *not* a dominant dial. It looked like one only because the
  earlier run measured a game in which nobody could use their Passives.
- **The mechanism is a floor, not an edge.** How often an archetype had no
  legal block at all: **38.8% / 19.4% / 41.7%** without Passives, and
  **0.0% / 0.0% / 0.0%** with them. A Both-range Passive is a legal defence
  in every exchange, so a Mind-2 character is never punished for a small
  hand the way the earlier numbers suggested.

**Two lessons about measuring, both learned the hard way here.**

- **Leave nothing out of the model and then reason about the gap.** A
  36-point spread between colours was entirely an artifact of an
  unimplemented rule. The number was real; the game it described was not.
- **Seed everything, including the combatants.** `Combatant.__init__` falls
  back to the module-level `random` when no rng is passed, so a harness
  that seeds only its own loop still shuffles differently every run. Two
  identical runs of the party comparison differed by three to five points
  before this was noticed, which is wider than several differences that had
  been reported as findings. The harnesses pass `rng=` now.

### Where the agents landed after it

`KitAI` beat `SimpleAI` by ten to twenty points of party win rate when
Passives could not block. With them blocking it fell to parity — 82.0%
against 84.7% at four wrackclaws, 76.0% against 75.3% at five — and it was
dropping the Blue-primary character twice as often as `SimpleAI` did, 28%
against 14%. Both of those turned out to be **one bug in the agent**, and
with it fixed the figures are 82.0% against **89.0%** and 76.0% against
**86.7%**, with every character going down less often than under
`SimpleAI`. Chasing the character was what found it; see below.

### The prior that was worse than no prior

`KitAI._defence_value` scores a block by the odds of winning the reveal,
and read those odds off `attacker.hand + attacker.deck`. **That is the one
set of cards guaranteed not to contain the attack being defended against.**
`play.py` pulls the attack card out of hand before it asks the defender to
block, so the pile the defender consults is, by construction, everything
the attacker is *not* about to play.

The instrument said so plainly once it was asked. Over 1950 defences, a
colour holding **none** of the visible pool was the colour actually played
**62%** of the time, and a colour holding 70% of it was played **0%** of
the time — monotonically inverted across every bin. The model's confidence
ran the same way: where it predicted no damage with certainty, damage got
through 65% of the time.

Three things about this are worth keeping:

- **It was found by ablation, not by reading the code.** Handing Chris's
  `choose_defense` back to `SimpleAI` and changing nothing else restored
  him exactly — 9% down against 9%, 4.8 damage taken against 4.8. Four
  other methods were ablated the same way and moved nothing.
- **Summing the other zones does not fix it**, and measuring beats
  reasoning about it. The obvious repair — count hand, deck, discard and
  play, so the removal cannot skew the total — was *no better than the
  bug* (31% down against 28%). The card in flight sits in a local variable
  in `play.py` and is in no zone at all, so against a four-card creature
  three cards are visible and the missing quarter is exactly the one that
  decides the exchange. The most common thing the defender saw was a
  perfectly flat 1/1/1 — because the second RED was the one coming.
- **The fix was already written down in the rules.** Deck size is total
  stats and each colour's count equals its matching stat, so a stat block
  *is* a colour composition (`rules/cards.md`). That prior is not
  conditioned on the choice the attacker has already made, which is the
  whole of what was wrong. Weighting it further by each colour's mean die
  — Red is played more because Red's dice are bigger — was a wash across
  six different foe shapes, so it was not kept.

The fixed prior wins against every foe shape tried, not just the red-heavy
one that exposed it: 250 fights each at 1/2/1, 1/1/2, 2/2/2, 3/1/1 and
1/3/1, it is ahead of both `SimpleAI` and the old `KitAI` on win rate and
on down rate in every row.

### A card note that fell out of the weight sweep

Re-sweeping `KitAI`'s weights on the party fight — the duel having been
measured to see none of them — showed that four of the five barely move
the result, and turned up something about a card rather than about the
agent. **Chris never sets his stance.** KILLSWITCH was a
legal attack 2232 times in 300 fights and was chosen twice; a stance was
up on 3 turns out of 2942. Soul 2 + d4 scores 4.0, and his MIMETIC BLADE
Passive scores 6.0 and costs no card at all, so the stance is dominated by
a card he never has to spend.

Forcing him to set it changes nothing measurable: raise the setup weight
until he plays it about once a fight and the party result moves under a
point either way. So this is **not** a case of the agent misplaying a good
card, and it is not an argument for changing KILLSWITCH — it is one
measurement, on one fill deck, against one creature, and what it says is
that a stance priced against a free Passive has a hard time getting played.
Whether that matters is a question about the card, and the card is Chris's
(`campaign/chris.md`).

**And judge an agent on the fight the character was built for.** `KitAI`
is at parity with `SimpleAI` in a duel and worth ten to twenty points of
party win rate in a group fight — see its class docstring. A duel has no
allies and no time, so nothing a setup play buys can pay back in one.

## Extending it

To play a real creature, build a `Combatant` with its stat block from
`bestiary/` and a deck from its signature cards plus core fill:

```python
# from inside combat-simulations/
import cards, engine
sig = cards.load('fermata')
fermata = engine.Combatant('Fermata', body=12, mind=10, soul=20,
                           deck=sig, team='foes')
fermata.max_hp        # 78, matching bestiary/fermata.md
```

The HP formula is derived from the stat block rather than copied from it,
so that last line is a useful check when adding a creature: if the engine
and the bestiary disagree on a published HP, one of them is wrong.

Deck construction rules — size equals total stats, colour counts equal each
stat — are in `rules/cards.md`, Deck Building. `play.py`'s `build_deck` is a
rough version of it.
