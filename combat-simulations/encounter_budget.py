"""How many of a thing is a fight?

The balance lever in Tales Untold is the number of opponents, not the
opponents' numbers — a weak creature is only weak alone. So this sweeps
count rather than stats: it runs the party against 1, 2, 3 ... copies of a
creature and reports where the fight stops being free and starts being
lethal.

    python3 encounter_budget.py                    # the default early roster
    python3 encounter_budget.py --runs 800
    python3 encounter_budget.py rootstalker ocellus
    python3 encounter_budget.py --max-count 8

Caveat that governs every number below: roughly seven in eight Effect
halves are modelled (see `effects.py`); the rest are narrated and therefore
absent from these runs. The tables were originally measured with none of
them running, on the argument that Effects push both sides up. Re-measured
2026-09-18 at three thousand fights a row: the heavy end did not move —
one and two minotaurs at 94.5% and 65.0% against 94.5% and 64.6% before —
but the swarm end did, six wrackclaws going from a 48% fight to a 54-56%
one. Effects widen the over-count at the weak end rather than closing it.
Treat a 50% line as "a real fight" rather than a precise coin flip, and
expect drift from a party built around the cards still narrated.
"""

import argparse
import io
import os
import random
import re
import sys

import cards as cardlib
import play
from engine import BACK, FRONT, Combatant, d
from agents import SimpleAI
from wheel import Wheel

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The party as written, at session one: nine total stats each, so nine-card
# decks (`rules/character-creation.md`, Starting Deck).
PARTY = [
    ('Chris', dict(mind=4, body=3, soul=2), FRONT, 'campaign/chris.md'),
    ('Kevin', dict(mind=3, body=4, soul=2), FRONT, 'campaign/kevin.md'),
    ('Pat',   dict(mind=2, body=3, soul=4), BACK,  'campaign/pat.md'),
]

STATS = re.compile(
    r'\*\*?(?:Mind (?P<m1>\d+) / Body (?P<b1>\d+) / Soul (?P<s1>\d+)'
    r'|Body (?P<b2>\d+) / Mind (?P<m2>\d+) / Soul (?P<s2>\d+))')


def stat_block(path):
    """Pull Mind/Body/Soul out of a bestiary or character file."""
    with open(path, encoding='utf-8') as fh:
        text = fh.read()
    m = STATS.search(text)
    if not m:
        return None
    g = m.groupdict()
    if g['m1'] is not None:
        return dict(mind=int(g['m1']), body=int(g['b1']), soul=int(g['s1']))
    return dict(mind=int(g['m2']), body=int(g['b2']), soul=int(g['s2']))


def find(slug):
    """A creature by slug, from bestiary/ first and then characters/."""
    for folder in ('bestiary', 'characters'):
        path = os.path.join(REPO, folder, slug + '.md')
        if os.path.exists(path):
            st = stat_block(path)
            if st:
                return st, os.path.join(folder, slug + '.md')
    return None, None


def make(name, st, pool, position, team, rng, sig=None):
    """Build the creature, signatures first and the rest filled by colour.

    The fill used to be `sig + deck[len(sig):]` — prepend the signatures and
    keep the tail of a correctly-coloured random deck. That silently broke
    the one rule every deck in the world obeys: **deck size equals total
    stats and each colour's count equals its matching stat** (`CLAUDE.md`,
    Derived math). Measured 2026-09-21 on the Wrackclaw, whose four cards
    should be 1 Blue / 2 Red / 1 Green: **none of five hundred builds were
    legal**, and the slot that should always have been Red came up Green
    about half the time.

    The slot matters more than it sounds on a small creature. A Wrackclaw
    holds four cards, so the fill *is* a quarter of everything it does, and
    the bestiary names the card that belongs there. Getting it wrong made
    the creature measurably safer than the one a table would actually face.
    """
    sig = list(sig or ())
    want = {'RED': st['body'], 'BLUE': st['mind'], 'GREEN': st['soul']}
    for c in sig:
        want[c.color] = want.get(c.color, 0) - 1
    deck = list(sig)
    for color, n in want.items():
        if n <= 0:
            continue
        avail = [c for c in pool if c.color == color and c not in deck]
        deck += rng.sample(avail, min(n, len(avail)))
    c = Combatant(name, body=st['body'], mind=st['mind'], soul=st['soul'],
                  deck=deck, position=position, team=team)
    c._agent = SimpleAI(rng)
    return c


def one_fight(foe_st, count, pool, rng, foe_sig=None, running_hot=False):
    party = [make(n, st, pool, pos, 'party', rng) for n, st, pos, _ in PARTY]
    foes = []
    for i in range(count):
        f = make(f'foe{i+1}', foe_st, pool,
                 FRONT if i % 2 == 0 else BACK, 'foes', rng, sig=foe_sig)
        if running_hot:
            _arm_running_hot(f)
        foes.append(f)

    everyone = party + foes
    rolled = [(d(6, rng) + c.soul, c.soul, c.team == 'party', c) for c in everyone]
    rolled.sort(key=lambda t: (-t[0], -t[1], not t[2]))
    wheel = Wheel([c for *_, c in rolled])
    for c in everyone:
        c.draw_up()

    result = play.run(party, foes, wheel, lambda *a: None, rng, max_rounds=30)
    hp = sum(max(0, c.hp) for c in party)
    return result, hp, sum(1 for c in party if c.down), sum(1 for c in party if c.dead)


def _arm_running_hot(c):
    """Trait — Running Hot: each time he takes damage he gains 1 Deadly
    (`characters/harlock.md`). The engine tracks Deadly but executes no
    Effects, so the trait is wired on by hand here."""
    original = c.take

    def take(amount, **kw):
        dealt = original(amount, **kw)
        if dealt > 0:
            c.deadly += 1
        return dealt

    c.take = take


def sweep(slug, pool, runs, max_count, seed):
    st, src = find(slug)
    if st is None:
        print(f'  ?  {slug}: no stat block found')
        return
    try:
        sig = cardlib.load(slug) or None
    except FileNotFoundError:
        sig = None  # creature with no signature cards; core fill only
    hot = slug == 'harlock'
    total = sum(st.values())
    hp = 4 * st['body'] + st['soul'] + st['mind']
    label = f"{slug}  (M{st['mind']}/B{st['body']}/S{st['soul']}, HP {hp}, CTR {total})"
    print(f'\n{label}')
    print(f'  {"n":>2}  {"party wins":>10}  {"avg HP left":>11}  {"downs":>6}  {"deaths":>7}')
    for n in range(1, max_count + 1):
        rng = random.Random(seed)
        wins = hps = downs = deaths = 0
        for _ in range(runs):
            r, h, dn, dd = one_fight(st, n, pool, rng, foe_sig=sig, running_hot=hot)
            wins += (r == 'party')
            hps += h
            downs += dn
            deaths += dd
        pct = 100.0 * wins / runs
        print(f'  {n:>2}  {pct:>9.1f}%  {hps/runs:>11.1f}  '
              f'{downs/runs:>6.2f}  {deaths/runs:>7.2f}')
        if pct < 5:
            break


DEFAULT = ['ocellus', 'harlock', 'briarbundles', 'rootstalker', 'duskwick',
           'chitterer', 'tollbird', 'wrackclaw', 'hullback', 'minotaur']


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('slugs', nargs='*', default=None)
    ap.add_argument('--runs', type=int, default=300)
    ap.add_argument('--max-count', type=int, default=6)
    ap.add_argument('--seed', type=int, default=11)
    args = ap.parse_args(argv)

    pool = cardlib.core_pool()
    party_hp = sum(4 * st['body'] + st['soul'] + st['mind'] for _, st, _, _ in PARTY)
    print(f'Party: ' + ', '.join(
        f"{n} (M{st['mind']}/B{st['body']}/S{st['soul']})" for n, st, _, _ in PARTY))
    print(f'Total party HP {party_hp}. {args.runs} runs per row, seed {args.seed}.')
    print('Effects are executed — 93% of halves compile or read as traits '
          '(`effects.py`); the remaining 22 narrate and are absent.')

    for slug in (args.slugs or DEFAULT):
        sweep(slug, pool, args.runs, args.max_count, args.seed)


if __name__ == '__main__':
    main()
