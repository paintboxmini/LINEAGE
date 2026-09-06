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

## Known discrepancies

Two places where `rules/initiative-shift-examples.md` cannot be satisfied in
full. Both are flagged rather than papered over, because the examples file
is the spec and a silent choice would hide a real question.

**Example 5 contradicts Example 3.** Example 5 continues from Example 2's
`b, d, c, a` with d holding a skip chip, and has b play Initiative Shift +1
on d. It narrates the outcome as "no bonus, no skip." But d sits one slot
off the marker, so +1 lands it exactly on the marker's own slot — which
Example 3 defines as precisely the bonus-turn case. Both cannot be true.
The engine follows Example 3, since that example states the rule and
Example 5's stated purpose is the chip-clearing behaviour rather than the
boundary. `test_wheel.py` asserts the chip clearing, which is what Example 5
is actually demonstrating, and does not assert the "no bonus" narration.

**Example 3's turn sequence.** All four worked cases' resulting wheel
layouts are reproduced exactly, and Examples 1, 2 and 4 reproduce their turn
sequences exactly too. Example 3's does not: after d's bonus turn the
example has a skipped immediately, then b, then c, whereas the engine
advances the marker past the acting token's new slot and so reaches a's skip
chip on the following lap. The three unambiguous cases pin the marker rule
down; Example 3 needs a marker rule the other three contradict. Worth a
ruling.

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
