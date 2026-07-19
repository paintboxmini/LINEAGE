"""
Team-battle runner. Monte Carlo over N-vs-N with decks from the roster.

Usage:
    python3 team_run.py [N] "deckA1,deckA2,..." "deckB1,deckB2,..." [--sample]

    N        number of battles (default 10000)
    teams    comma-separated roster deck names per side
    --sample print one verbose battle transcript, then stop

Examples:
    python3 team_run.py 10000 "steele,sage,adept" "frost,frost,frost"
    python3 team_run.py 1 "adept,adept,adept" "steele,steele,steele" --sample
"""

import sys
from collections import Counter

from engine import Combatant
from team_engine import Battle
from content import build_cards, ROSTER
from team_policies import make_team_policy


def build_team(names):
    team = []
    for i, nm in enumerate(names):
        stats, deck = ROSTER[nm]
        team.append(Combatant(f"{nm.capitalize()}{i+1}", decklist=deck,
                              policy=make_team_policy(), **stats))
    return team


def one_battle(cards, a_names, b_names, seed, log=None):
    battle = Battle(build_team(a_names), build_team(b_names), cards, seed=seed, log=log)
    return battle.run(), battle


def sample(a_names, b_names):
    cards = build_cards()
    log = []
    result, battle = one_battle(cards, a_names, b_names, seed=7, log=log)
    print(f"--- {'+'.join(a_names)}  vs  {'+'.join(b_names)} ---")
    for line in log:
        print(line)
    label = {0: 'TEAM A', 1: 'TEAM B', 'TIE': 'TIE'}[result]
    print(f"\nRESULT: {label}  (turns: {battle.turn_count})")


def monte_carlo(n, a_names, b_names):
    cards = build_cards()
    wins = Counter()
    turns = 0
    deaths_a = deaths_b = 0        # total individual deaths, across all battles
    battles_with_death_a = battles_with_death_b = 0   # "did anyone die this battle" — the number that maps to Drew's 1-in-20-sessions target
    for i in range(n):
        result, battle = one_battle(cards, a_names, b_names, seed=i)
        wins[result] += 1
        turns += battle.turn_count
        da = sum(1 for c in battle.teams[0] if c.is_dead)
        db = sum(1 for c in battle.teams[1] if c.is_dead)
        deaths_a += da
        deaths_b += db
        battles_with_death_a += bool(da)
        battles_with_death_b += bool(db)
    print(f"=== [{'+'.join(a_names)}] vs [{'+'.join(b_names)}] — {n} battles ===")
    print(f"  Team A  {wins[0]:6}  ({100*wins[0]/n:5.1f}%)")
    print(f"  Team B  {wins[1]:6}  ({100*wins[1]/n:5.1f}%)")
    print(f"  TIE     {wins['TIE']:6}  ({100*wins['TIE']/n:5.1f}%)")
    print(f"  avg turns: {turns/n:.1f}")
    print(f"  Team A deaths: {deaths_a} total ({deaths_a/n:.3f}/battle) — "
          f"a death occurred in {100*battles_with_death_a/n:.2f}% of battles")
    print(f"  Team B deaths: {deaths_b} total ({deaths_b/n:.3f}/battle) — "
          f"a death occurred in {100*battles_with_death_b/n:.2f}% of battles")
    print(f"  (Drew's target: a PC dies ~once per 20 sessions, party-wide — "
          f"compare 'battle-with-a-death' rate above against how many of "
          f"these encounters actually happen per session.)")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    n = int(args[0]) if args else 10000
    a_names = args[1].split(",") if len(args) > 1 else ["steele", "sage", "adept"]
    b_names = args[2].split(",") if len(args) > 2 else ["frost", "frost", "frost"]
    if "--sample" in sys.argv:
        sample(a_names, b_names)
    else:
        monte_carlo(n, a_names, b_names)
