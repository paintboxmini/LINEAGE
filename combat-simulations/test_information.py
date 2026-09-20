"""Nobody at the table reads a zone they were never shown.

Hands and decks are hidden. So are HP, max HP and the stat line. An agent
may look at what happens in front of everyone — cards face up in the
discard pile, Ongoing Effects on the table, position, Down, status tokens,
and
the damage called out as it lands (`engine.Combatant.seen_damage`) — and
nothing else.

This is checked rather than trusted because it has been broken twice, both
times by a change that measured *better* for it: `KitAI._odds` read
`attacker.hand + attacker.deck`, and its first replacement read the
attacker's stat line. A rule that only holds while nobody is optimising
against it is not a rule.

Read statically, over the source, so it catches a leak that no fight in
the test suite happens to exercise.
"""

import ast
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, 'agents.py')

# Attributes nobody may read off anyone but themselves and their own team.
#
# `stances` and `passives` are here for a reason worth stating: the cards
# are face up, so an opponent may *see* them, but an agent reaching into
# those lists is reading the kit rather than watching it — it would know
# that KILLSWITCH ends on a repeated colour, or which of its two modes was
# taken, without ever having been shown. What is public is that a card was
# revealed and what colour it was, which is all `Knowledge` takes.
HIDDEN = {'hp', 'max_hp', 'body', 'mind', 'soul', 'hand', 'deck',
          'death_threshold', 'stances', 'passives'}

# Names that refer to the agent's own combatant, whose sheet is its own to
# read. `who` is `scry`'s name for it; `other`/`c` inside HumanAgent._health
# are guarded by the team check in that method, which is the one place
# allowed to decide what a player may be shown.
OWN = {'me', 'who', 'self'}
EXEMPT = {
    ('HumanAgent', '_health'),
    # A character's own seed is a piece of them, paid for out of their own
    # HP and grown at the start of each of their own turns
    # (`campaign/chris.md`, Seeds). Knowing how big it is is knowing what
    # they are carrying, not reading somebody else's sheet. Exempted by
    # function rather than by the method that calls it, so it stays the
    # size of its reason.
    ('KitAI', '_my_seed'),
}


def offences(path=SOURCE):
    tree = ast.parse(open(path).read(), os.path.basename(path))
    found = []
    for cls in [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]:
        for fn in [n for n in cls.body
                   if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]:
            if (cls.name, fn.name) in EXEMPT:
                continue
            for node in ast.walk(fn):
                if not isinstance(node, ast.Attribute):
                    continue
                if node.attr not in HIDDEN:
                    continue
                base = node.value
                if isinstance(base, ast.Name) and base.id in OWN:
                    continue
                who = base.id if isinstance(base, ast.Name) else '<expr>'
                found.append((cls.name, fn.name, node.lineno,
                              f'{who}.{node.attr}'))
    return found


def main():
    bad = offences()
    if bad:
        print(f'agents.py reads hidden state:\n')
        for cls, fn, line, what in bad:
            print(f'  agents.py:{line}  {cls}.{fn} reads {what}')
        print(f'\n{len(bad)} leak(s). Hands, decks, HP and stats are hidden '
              f'— infer them from play instead (agents.Knowledge).')
        return 1
    print('No agent reads a hidden zone.')

    # And the public channel it is supposed to use instead exists.
    sys.path.insert(0, HERE)
    import engine
    c = engine.Combatant('probe', 2, 2, 2, deck=[])
    assert c.seen_damage == 0, 'seen_damage should start at zero'
    c.take(3)
    c.take(2)
    assert c.seen_damage == 5, f'seen_damage should total 5, got {c.seen_damage}'
    print('Damage announcements accumulate where an agent can read them.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
