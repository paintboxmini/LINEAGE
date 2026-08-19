"""
Stat Spread Lab — does maxing one stat actually help, and if not, why not?

Built from Drew's framing (2026-08-18): "I still think that maxing a single
stat already has a built in flaw in rps." The question came up while deciding
whether Advancement needs a numeric stat cap after character creation, since
the existing cap reads "no single stat may exceed 5 at character creation" and
then says nothing about afterwards.

The method, same shape as keyword_lab.py: hold everything constant except the
one thing being measured. Both sides run the same policy and the same deck
*construction*, and only the stat spread differs — every spread totals 9, the
starting total (2/2/2 plus 3 distributed). Both orderings are run and summed so
first-player advantage cancels.

Two deck conditions matter, and separating them is the whole point:

  MONO      the specialist leans their deck into their maxed colour (9 of it).
            This is what a player is tempted to do, and it is what the RPS
            pillar can read: the defender chooses blind from revealed-colour
            history, so a mono-colour attacker answers the prediction for them.

  BALANCED  the specialist keeps a 3/3/3 deck. Their maxed colour hits hard,
            the other six cards swing at stat 2.

Card quality is a confound — a mono-red deck is nine specific red cards, not an
abstraction — so decks are drawn randomly and the result averaged over several
draws rather than taken from one hand-picked set.

    python3 stat_spread_lab.py            # both conditions, both policies
    python3 stat_spread_lab.py --trials 20 --duels 40

This file measures spreads totalling 9, the starting total. The cap question is
about growth, so the same method was run at total 12 (three advancement points)
piled into one stat against a spread 4/4/4 — see `memory.md`, "Maxing a Stat Is
Priced, Except Mind". That is where the interesting result is: Body and Soul are
punished, Mind is not.
"""

import argparse
import collections
import random

import content
import engine
import policies

SPREADS = {
    'Body/Red':   ((5, 2, 2), 'R'),
    'Mind/Blue':  ((2, 5, 2), 'B'),
    'Soul/Green': ((2, 2, 5), 'G'),
}
BALANCED = (3, 3, 3)


def _pools(cards):
    by_col = collections.defaultdict(list)
    for name, c in cards.items():
        if not getattr(c, 'is_status', False) and c.color in ('R', 'B', 'G'):
            by_col[c.color].append(name)
    for k in by_col:
        by_col[k].sort()      # sorted first so the rng, not dict order, decides
    return by_col


def _duel(cards, spread_a, deck_a, spread_b, deck_b, pol, seed):
    a = engine.Combatant('A', *spread_a, list(deck_a), policies.make_policy(pol))
    b = engine.Combatant('B', *spread_b, list(deck_b), policies.make_policy(pol))
    engine.Duel(a, b, cards, seed=seed).run()
    if a.is_dead or a.collapsed:
        return 'B'
    if b.is_dead or b.collapsed:
        return 'A'
    return 'draw'


def run(trials, duels, policy_names):
    cards = content.build_cards()
    by_col = _pools(cards)
    hp = lambda s: 3 * s[0] + s[2] + s[1]

    print(f'{trials} random deck draws x {duels} duels x 2 orderings per cell\n')
    print(f'{"specialist":<13}{"HP":>4}  {"policy":<11}{"mono deck":>12}{"balanced deck":>16}')
    for label, (spread, col) in SPREADS.items():
        for pol in policy_names:
            mono_w = bal_w = n = 0
            rng = random.Random(4)
            for t in range(trials):
                bal = (rng.sample(by_col['R'], 3) + rng.sample(by_col['B'], 3)
                       + rng.sample(by_col['G'], 3))
                mono = rng.sample(by_col[col], 9)
                for i in range(duels):
                    s = t * 1000 + i
                    mono_w += _duel(cards, spread, mono, BALANCED, bal, pol, s) == 'A'
                    mono_w += _duel(cards, BALANCED, bal, spread, mono, pol, s + 500) == 'B'
                    bal_w += _duel(cards, spread, bal, BALANCED, bal, pol, s) == 'A'
                    bal_w += _duel(cards, BALANCED, bal, spread, bal, pol, s + 500) == 'B'
                    n += 2
            print(f'  {label:<11}{hp(spread):>4}  {pol:<11}'
                  f'{mono_w / n * 100:11.1f}%{bal_w / n * 100:15.1f}%')
    print('\nAnything at or below 50% means the specialist is not being rewarded.')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__.split('\n')[1])
    p.add_argument('--trials', type=int, default=8)
    p.add_argument('--duels', type=int, default=25)
    p.add_argument('--policies', default='tactician,punisher')
    a = p.parse_args()
    run(a.trials, a.duels, a.policies.split(','))
