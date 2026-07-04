"""
Duel runner — Monte Carlo over any two decks in the roster.

Usage:
    python3 run.py [N] [deckA] [polA] [deckB] [polB] [--sample]

    N       number of duels (default 20000)
    deck    frost | steele | mire      (default frost vs steele)
    pol     random | greedy | reader   (default reader)
    --sample  print one verbose transcript, then stop

Examples:
    python3 run.py
    python3 run.py 20000 mire reader frost reader
    python3 run.py 1 mire reader steele reader --sample
"""

import sys
from collections import Counter

import engine as E
from engine import Combatant, Duel
from content import build_cards, ROSTER
from policies import make_policy


def make_combatant(name, policy_name, label=None):
    stats, deck = ROSTER[name]
    return Combatant(label or name.capitalize(), decklist=deck,
                     policy=make_policy(policy_name), **stats)


def labels(a_name, b_name):
    # disambiguate mirror matches so the win counter doesn't collide
    if a_name == b_name:
        return a_name.capitalize() + "-A", b_name.capitalize() + "-B"
    return a_name.capitalize(), b_name.capitalize()


def one_duel(cards, a_name, a_pol, b_name, b_pol, seed, log=None):
    la, lb = labels(a_name, b_name)
    a = make_combatant(a_name, a_pol, la)
    b = make_combatant(b_name, b_pol, lb)
    duel = Duel(a, b, cards, seed=seed, log=log)
    result = duel.run()
    return result, duel


def sample(a_name, a_pol, b_name, b_pol):
    cards = build_cards()
    log = []
    result, duel = one_duel(cards, a_name, a_pol, b_name, b_pol, seed=7, log=log)
    print(f"--- sample: {a_name}({a_pol}) vs {b_name}({b_pol}) ---")
    for line in log:
        print(line)
    print(f"\nRESULT: {result}  (turns: {duel.turn_count})")
    _print_rulings()


def monte_carlo(n, a_name, a_pol, b_name, b_pol):
    cards = build_cards()
    A, B = labels(a_name, b_name)
    wins = Counter()
    turns_total = 0
    first_decisive = 0
    first_wins = 0
    hp_left = {A: [], B: []}
    for i in range(n):
        result, duel = one_duel(cards, a_name, a_pol, b_name, b_pol, seed=i)
        wins[result] += 1
        turns_total += duel.turn_count
        if result != "TIE":
            first_decisive += 1
            if duel.order[0].name == result:
                first_wins += 1
        for c in duel.combatants:
            if not c.collapsed:
                hp_left[c.name].append(c.hp)

    print(f"=== {a_name}({a_pol}) vs {b_name}({b_pol}) — {n} duels ===")
    for name in (A, B, "TIE"):
        w = wins.get(name, 0)
        print(f"  {name:8} {w:6}  ({100*w/n:5.1f}%)")
    print(f"  avg turns: {turns_total/n:.1f}")
    if first_decisive:
        print(f"  going-first win rate: {100*first_wins/first_decisive:.1f}%")
    for name in (A, B):
        vals = hp_left[name]
        if vals:
            print(f"  {name} avg HP on win: {sum(vals)/len(vals):.1f}")
    _print_rulings()


def _print_rulings():
    if not E._RULINGS:
        return
    print("\n--- rulings the engine had to assume (errata queue) ---")
    for k, note in sorted(E._RULINGS.items()):
        print(f"  [{k}] {note}")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    n = int(args[0]) if len(args) > 0 else 20000
    a_name = args[1] if len(args) > 1 else "frost"
    a_pol = args[2] if len(args) > 2 else "reader"
    b_name = args[3] if len(args) > 3 else "steele"
    b_pol = args[4] if len(args) > 4 else "reader"
    if "--sample" in flags:
        sample(a_name, a_pol, b_name, b_pol)
    else:
        monte_carlo(n, a_name, a_pol, b_name, b_pol)
