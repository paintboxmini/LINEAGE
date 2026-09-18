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
| `wheel.py` | The initiative wheel and Initiative Shift, including the chip rules. |
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

Run `python3 effects.py` for the live figure; it was 278/319 (87%) when this
paragraph was written — 270 compiling and 8 read as traits.

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
