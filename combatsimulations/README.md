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
python3 cards.py                # card counts, as a load check
```

## What's here

| File | |
|---|---|
| `cards.py` | Loads `cards/*.md` directly — the markdown is the source of truth, same as `printing/` treats it. Parses name, colour, stat, die and range; carries Effect text verbatim. |
| `wheel.py` | The initiative wheel and Initiative Shift, including the chip rules. |
| `engine.py` | Combatants, statuses, the damage pipeline, and Attack Resolution. |
| `agents.py` | Who decides: `HumanAgent` prompts at the terminal, `SimpleAI` plays to type, `RandomAgent` plays legally at random. Any mix can share a table. |
| `play.py` | Turn loop and CLI. |
| `test_wheel.py` | `rules/initiative-shift-examples.md` as assertions. |

`rules/invariants.md` is the specification this is checked against.

## What it does and doesn't resolve

The engine resolves the **structured** part of a fight: initiative and the
wheel, drawing to hand size, range legality, the Blind/Evade checks and
their resolution order, the RPS reveal, the damage pipeline, Collapse and
death, and positioning.

It does **not** execute card Effects. Effect and Defense Effect text is
prose written for a person — "discard a card, gain +2 damage with that
colour the rest of combat" — and parsing that reliably is a different
project from running a fight. The engine prints the text at the moment it
triggers and leaves it to whoever is playing. Statuses the engine tracks
(Deadly, Weak, Resist, Vulnerable, Evade, Blind, Rooted, Staggered, Thorns,
Armour, Ward, Quick, Immunity, Protect) can be set on a `Combatant`
directly, so a Effect that grants one can be applied by hand and the engine
will honour it from then on.

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
# from inside combatsimulations/
import cards, engine
sig = cards.load('fermata')
fermata = engine.Combatant('Fermata', body=12, mind=10, soul=20,
                           deck=sig, team='foes')
fermata.max_hp        # 66, matching bestiary/fermata.md
```

The HP formula is derived from the stat block rather than copied from it,
so that last line is a useful check when adding a creature: if the engine
and the bestiary disagree on a published HP, one of them is wrong.

Deck construction rules — size equals total stats, colour counts equal each
stat — are in `rules/cards.md`, Deck Building. `play.py`'s `build_deck` is a
rough version of it.
