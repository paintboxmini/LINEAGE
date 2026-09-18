"""`rules/invariants.md`, Confirmed, as assertions.

Two invariants are listed there. Both are properties of the engine that no
single fight demonstrates on its own, so each is checked directly and then
again across randomised play.

    python3 test_invariants.py
"""

import random

import cards as cardlib
from engine import Combatant, FRONT, BACK
from play import build_deck, run
from agents import RandomAgent, SimpleAI
from wheel import Wheel

FAILURES = []


def check(label, condition, detail=''):
    if condition:
        print(f'  ok    {label}')
    else:
        print(f'  FAIL  {label}' + (f' — {detail}' if detail else ''))
        FAILURES.append(label)


def piles(c, written_only=True):
    """Cards held across every pile.

    `rules/invariants.md` allows the total to change at two nameable
    events, one of which is a Wound/Exhaust insertion — so the conserved
    quantity is the *written* cards. Status cards are counted separately
    and are expected to appear and vanish.
    """
    everything = c.deck + c.hand + c.discard + c.exiled
    if written_only:
        everything = [x for x in everything if x.source != 'status']
    return len(everything)


def status_held(c):
    return len([x for x in c.deck + c.hand + c.discard + c.exiled
                if x.source == 'status'])


# ---- 1. Derived stats are computed live, never cached -------------------

def test_derived_live():
    print('Derived stats are computed live, never cached')
    pool = cardlib.core_pool()
    rng = random.Random(1)
    c = Combatant('Subject', body=3, mind=2, soul=2,
                  deck=build_deck(pool, 7, 3, 2, 2, rng))

    check('max HP matches the formula', c.max_hp == 4 * 3 + 2 + 2, c.max_hp)
    check('hand size is Mind', c.hand_size == 2, c.hand_size)

    # The named bug: raise a stat and every derived value must move with it,
    # with nothing to invalidate.
    c.body += 1
    check('max HP follows Body up', c.max_hp == 4 * 4 + 2 + 2, c.max_hp)
    check('death threshold follows Max HP',
          c.death_threshold == -10, c.death_threshold)
    c.mind += 2
    check('hand size follows Mind up', c.hand_size == 4, c.hand_size)
    check('max HP follows Mind up', c.max_hp == 4 * 4 + 4 + 2, c.max_hp)
    c.body -= 2
    check('max HP follows Body back down', c.max_hp == 4 * 2 + 4 + 2, c.max_hp)

    # A stat drop must not leave current HP above the new maximum when it
    # is next healed against.
    c.hp = c.max_hp
    c.body -= 1
    c.heal(99)
    check('healing cannot exceed the recomputed maximum',
          c.hp == c.max_hp, f'{c.hp}/{c.max_hp}')

    # Nothing stores it.
    check('max_hp is not an instance attribute',
          'max_hp' not in vars(c), sorted(vars(c))[:4])


# ---- 2. Card count is conserved per combatant --------------------------

def test_conservation():
    print('\nCard count is conserved per combatant across all piles')
    pool = cardlib.core_pool()

    # Wide rather than deep, and both agents. Twelve seeds missed a card
    # leak that showed up in roughly one fight in forty — the shapes that
    # break conservation (a card exiled out of an exchange, an attack that
    # does not happen after both cards are committed) need an unusual
    # exchange to reach at all.
    bad_seeds = []
    for AgentCls in (RandomAgent, SimpleAI):
        for seed in range(300):
            rng = random.Random(seed)
            party = [Combatant('A', 4, 3, 3, build_deck(pool, 10, 4, 3, 3, rng),
                               position=FRONT, team='party', rng=rng),
                     Combatant('B', 3, 4, 3, build_deck(pool, 10, 3, 4, 3, rng),
                               position=BACK, team='party', rng=rng)]
            foes = [Combatant('X', 4, 2, 3, build_deck(pool, 9, 4, 2, 3, rng),
                              position=FRONT, team='foes', rng=rng),
                    Combatant('Y', 3, 3, 2, build_deck(pool, 8, 3, 3, 2, rng),
                              position=BACK, team='foes', rng=rng)]
            everyone = party + foes
            for c in everyone:
                c._agent = AgentCls(rng)
            start = {c.name: piles(c) for c in everyone}
            for c in everyone:
                c.draw_up()
            run(party, foes, Wheel(list(everyone)), lambda *a: None, rng,
                max_rounds=25)
            bad = [(c.name, start[c.name], piles(c)) for c in everyone
                   if piles(c) != start[c.name]]
            if bad:
                bad_seeds.append((AgentCls.__name__, seed, bad))

    check('600 fights end with the written cards they started',
          not bad_seeds, bad_seeds[:3])


if __name__ == '__main__':
    test_derived_live()
    test_conservation()
    print()
    if FAILURES:
        print(f'{len(FAILURES)} failed.')
        raise SystemExit(1)
    print('All invariants hold.')
