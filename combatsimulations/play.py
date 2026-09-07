"""Run a fight.

    python3 play.py                 # a demo fight, scripted on both sides
    python3 play.py --human         # you play the first party member
    python3 play.py --seed 7        # reproducible
    python3 play.py --rounds 40     # safety cap on lap count

The turn loop follows `rules/combat.md`, Turn Structure: draw up, then one
Action plus one free action. Card Effects are printed rather than executed
(see engine.py) — this drives the structured part of a fight and reads the
prose out to whoever is playing.
"""

import argparse
import random
import sys

import cards as cardlib
from agents import HumanAgent, RandomAgent, SimpleAI
from engine import BACK, FRONT, Combatant, Outcome, d, resolve_attack
from wheel import Wheel


def build_deck(pool, size, body, mind, soul, rng):
    """`rules/cards.md`: deck size equals total stats, each colour's count
    equal to the matching stat."""
    want = {'RED': body, 'BLUE': mind, 'GREEN': soul}
    deck = []
    for color, n in want.items():
        avail = [c for c in pool if c.color == color]
        if not avail:
            continue
        deck += [rng.choice(avail) for _ in range(n)]
    return deck[:size] if size else deck


def take_turn(who, agent, foes, allies, wheel, log, rng):
    if not who.alive():
        return

    who.draw_up(log=log)

    if who.staggered:
        who.staggered -= 1
        log(f'{who.name} is Staggered — their attack is skipped.')
        return

    action = agent.choose_action(who, foes, allies)
    kind = action[0]

    if kind == 'attack':
        target = action[1]
        card = agent.choose_attack(who, target)
        if card is None:
            log(f'{who.name} has nothing legal to play.')
            return
        who.hand.remove(card)

        dagent = target._agent
        dcard = dagent.choose_defense(target, who)
        if dcard is not None:
            target.hand.remove(dcard)

        if who.in_cover:
            who.in_cover = False
            log(f'{who.name} leaves cover to attack.')

        resolve_attack(who, target, card, dcard, rng=rng, log=log)

    elif kind == 'move':
        who.position = BACK if who.position == FRONT else FRONT
        log(f'{who.name} moves to the {who.position}.')

    elif kind == 'cover':
        who.in_cover = True
        log(f'{who.name} takes cover.')

    else:
        log(f'{who.name} passes.')


def run(party, foes, wheel, log, rng, max_rounds=40):
    everyone = party + foes
    turns = 0
    cap = max_rounds * len(everyone)

    current = wheel.order()[0]
    while turns < cap:
        turns += 1

        if all(not c.alive() or c.down for c in party):
            log('\nThe party is down.')
            return 'foes'
        if all(not c.alive() or c.down for c in foes):
            log('\nThe party wins.')
            return 'party'

        if current is not None and current.alive():
            allies = [c for c in everyone if c.team == current.team and c is not current]
            enemies = [c for c in everyone if c.team != current.team]
            log(f'\n--- {current.name}\'s turn ---')
            take_turn(current, current._agent, enemies, allies, wheel, log, rng)

        # A bonus turn is taken immediately, and spends the marker's slot
        # the same way an ordinary turn does — so the taker becomes the
        # actor the next advance is measured from.
        bonus = wheel.take_bonus()
        if bonus is not None:
            log(f'{bonus.name} takes an immediate extra turn.')
            current = bonus
            continue

        nxt = wheel.advance(current)
        while nxt is None:
            skipped = wheel.order()[0]
            log(f"{skipped.name}'s turn is skipped.")
            nxt = wheel.advance(skipped)
        current = nxt

        # "A combatant who leaves the fight entirely removes their slot, and
        # the wheel closes around it." The marker sits on `current`, so
        # pruning anyone else never moves it.
        for c in wheel.order():
            if c.dead and c is not current:
                wheel.remove(c)

    log('\nRound cap reached — calling it a draw.')
    return 'draw'


def main(argv=None):
    ap = argparse.ArgumentParser(description='Play out a Tales Untold fight.')
    ap.add_argument('--human', action='store_true',
                    help='play the first party member yourself')
    ap.add_argument('--seed', type=int, default=None)
    ap.add_argument('--rounds', type=int, default=40)
    ap.add_argument('--quiet', action='store_true')
    args = ap.parse_args(argv)

    rng = random.Random(args.seed)
    log = (lambda *a: None) if args.quiet else print

    pool = cardlib.core_pool()

    party = [
        Combatant('Vess', body=5, mind=4, soul=3,
                  deck=build_deck(pool, 12, 5, 4, 3, rng), position=FRONT, team='party'),
        Combatant('Corr', body=3, mind=5, soul=4,
                  deck=build_deck(pool, 12, 3, 5, 4, rng), position=BACK, team='party'),
    ]
    foes = [
        Combatant('Rootstalker', body=5, mind=2, soul=3,
                  deck=build_deck(pool, 10, 5, 2, 3, rng), position=FRONT, team='foes'),
        Combatant('Briarbundle', body=3, mind=3, soul=3,
                  deck=build_deck(pool, 9, 3, 3, 3, rng), position=BACK, team='foes'),
    ]

    for i, c in enumerate(party):
        c._agent = HumanAgent() if (args.human and i == 0) else SimpleAI(rng)
    for c in foes:
        c._agent = SimpleAI(rng)

    everyone = party + foes
    # Initiative: 1d6 + Soul, highest first; ties to higher Soul, then to
    # the player (`rules/combat.md`, Initiative).
    rolled = [(d(6, rng) + c.soul, c.soul, c.team == 'party', c) for c in everyone]
    rolled.sort(key=lambda t: (-t[0], -t[1], not t[2]))
    log('Initiative:')
    for total, _, _, c in rolled:
        log(f'  {total:>3}  {c.name}')

    wheel = Wheel([c for *_, c in rolled])
    for c in everyone:
        c.draw_up()

    log('\n' + '=' * 46)
    result = run(party, foes, wheel, log, rng, max_rounds=args.rounds)
    log('=' * 46)
    for c in everyone:
        state = 'dead' if c.dead else ('down' if c.down else f'{c.hp}/{c.max_hp}')
        log(f'  {c.name:<14} {state}')
    return result


if __name__ == '__main__':
    main()
