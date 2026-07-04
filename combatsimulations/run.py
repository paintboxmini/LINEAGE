"""
Duel runner — Monte Carlo over Frost vs Steele.

Usage:
    python3 run.py [N] [frost_policy] [steele_policy] [--sample]

    N              number of duels (default 20000)
    frost_policy   random | greedy | reader   (default reader)
    steele_policy  random | greedy | reader   (default reader)
    --sample       print a single verbose duel transcript, then stop

Examples:
    python3 run.py
    python3 run.py 50000 greedy greedy
    python3 run.py 1 reader reader --sample
"""

import sys
from collections import Counter

import engine as E
from engine import Combatant, Duel
from content import (build_cards, FROST_DECK, STEELE_DECK,
                     FROST_STATS, STEELE_STATS)
from policies import make_policy


def one_duel(cards, frost_pol, steele_pol, seed, log=None):
    frost = Combatant("Frost", decklist=FROST_DECK, policy=frost_pol, **FROST_STATS)
    steele = Combatant("Steele", decklist=STEELE_DECK, policy=steele_pol, **STEELE_STATS)
    duel = Duel(frost, steele, cards, seed=seed, log=log)
    result = duel.run()
    return result, duel


def sample(frost_name, steele_name):
    cards = build_cards()
    log = []
    result, duel = one_duel(cards, make_policy(frost_name),
                            make_policy(steele_name), seed=7, log=log)
    print(f"--- sample duel: Frost({frost_name}) vs Steele({steele_name}) ---")
    for line in log:
        print(line)
    print(f"\nRESULT: {result}  (turns: {duel.turn_count})")
    _print_rulings()


def monte_carlo(n, frost_name, steele_name):
    cards = build_cards()
    wins = Counter()
    turns_total = 0
    frost_first = Counter()   # who won when Frost had initiative
    hp_left = {"Frost": [], "Steele": []}
    for i in range(n):
        result, duel = one_duel(cards, make_policy(frost_name),
                                make_policy(steele_name), seed=i)
        wins[result] += 1
        turns_total += duel.turn_count
        winner_first = duel.order[0].name
        frost_first[(winner_first, result)] += 1
        for c in duel.combatants:
            if not c.collapsed:
                hp_left[c.name].append(c.hp)

    print(f"=== Frost({frost_name}) vs Steele({steele_name}) — {n} duels ===")
    for name in ("Frost", "Steele", "TIE"):
        w = wins.get(name, 0)
        print(f"  {name:7} {w:6}  ({100*w/n:5.1f}%)")
    print(f"  avg turns: {turns_total/n:.1f}")

    # initiative effect: win rate of whoever acted first
    first_wins = sum(v for (first, res), v in frost_first.items() if first == res)
    decisive = sum(v for (first, res), v in frost_first.items() if res != "TIE")
    if decisive:
        print(f"  going-first win rate: {100*first_wins/decisive:.1f}%")

    for name in ("Frost", "Steele"):
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
    fp = args[1] if len(args) > 1 else "reader"
    sp = args[2] if len(args) > 2 else "reader"
    if "--sample" in flags:
        sample(fp, sp)
    else:
        monte_carlo(n, fp, sp)
