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
from engine import (BACK, FRONT, MUST_TARGET, NO_ATTACK, NO_TARGET,
                    SKIP_DRAW, Combatant, Outcome, d, resolve_attack,
                    set_table)
from wheel import Wheel


def build_deck(pool, size, body, mind, soul, rng):
    """`rules/cards.md`: deck size equals total stats, each colour's count
    equal to the matching stat.

    Drawn **without** replacement. No written deck in the repo runs the same
    card twice — 43 decklists, checked by `agent-tools/check-references.py` —
    and this used to pick each slot independently, so it built creatures no
    bestiary entry could describe. It also let one Card object sit in two
    piles at once, which is the shape of bug that made FORGET file the same
    card twice.

    A colour with fewer distinct cards than the stat asks for takes what
    there is rather than padding with repeats.
    """
    want = {'RED': body, 'BLUE': mind, 'GREEN': soul}
    deck = []
    for color, n in want.items():
        avail = [c for c in pool if c.color == color]
        if not avail:
            continue
        deck += rng.sample(avail, min(n, len(avail)))
    return deck[:size] if size else deck


def take_turn(who, agent, foes, allies, wheel, log, rng):
    if not who.alive():
        return

    # Anything measured against this combatant's next turn ends now, before
    # anything else this turn reads it.
    who.expire_pending(log=log)

    who.moved_last_turn = who.moved_this_turn
    who.moved_this_turn = False

    # Same shape, and for the same reason: rolled forward once at the top of
    # the turn so every early return below still leaves it right. A turn
    # spent moving, taking cover, Staggered, or barred from attacking plays
    # no card at all, so there is no card you played last turn and MEASURE
    # finds nothing to be a different colour from.
    who.last_color = who.color_this_turn
    who.color_this_turn = None

    skip = who.restriction(SKIP_DRAW)
    if skip is not None:
        who.spend_restriction(skip, log=log)
        log(f'{who.name} skips their draw step.')
    else:
        who.draw_up(log=log)

    # `rules/card-glossary.md`, Anchored: triggers at the start of each of
    # your turns, for as long as you have held position. SEED and the other
    # start-of-turn reactions ride the same event.
    if who.pending:
        who.tick_anchors(foes[0] if foes else None, allies, foes, rng, log)

    if who.restriction(NO_ATTACK) is not None:
        log(f'{who.name} cannot attack this turn.')
        return

    # A partitioned enemy is not a legal target, so it should never reach
    # the agent as one.
    foes = [f for f in foes if f.restriction(NO_TARGET) is None]

    if who.staggered:
        who.staggered -= 1
        log(f'{who.name} is Staggered — their attack is skipped.')
        return

    who.extra_attacks = who.extra_actions = 0

    # One Action, plus anything a card hands back mid-turn. The cap is a
    # safety rail rather than a rule: DOUBLE DOWN can draw into a second
    # DOUBLE DOWN, and a turn that never ends is worse than one that stops.
    for _ in range(8):
        acted = _one_action(who, agent, foes, allies, wheel, log, rng)
        if who.extra_attacks > 0 and acted is not None and acted[0] == 'attack':
            who.extra_attacks -= 1
            log(f'{who.name} presses the attack.')
            continue
        if who.extra_actions > 0:
            who.extra_actions -= 1
            log(f'{who.name} takes another action.')
            continue
        break


def _one_action(who, agent, foes, allies, wheel, log, rng):
    """One Action from the turn structure. Returns the action taken."""
    if not who.alive():
        return None

    action = agent.choose_action(who, foes, allies)
    kind = action[0]

    if kind == 'attack':
        target = action[1]
        # MOCKERY, CHAIN, INTERCEPT: someone has to be answered first.
        forced = who.restriction(MUST_TARGET)
        if forced is not None:
            pull = forced.data.get('who')
            if pull is not None and pull.alive() and who.playable(pull):
                if pull is not target:
                    log(f'{who.name} is compelled to answer {pull.name}.')
                target = pull
            who.spend_restriction(forced, log=log)

        card = agent.choose_attack(who, target)
        if card is None:
            log(f'{who.name} has nothing legal to play.')
            return None
        who.hand.remove(card)

        # ANTICIPATE: "draw 1 card before defending" — the reaction has to
        # land while there is still a defence to choose.
        target.fire('attacked', who,
                    [c for c in allies + [who] if c.team == target.team],
                    [c for c in foes + [who] if c.team != target.team],
                    rng, log)

        dagent = target._agent
        dcard = dagent.choose_defense(target, who)
        if dcard is not None:
            target.hand.remove(dcard)

        if who.in_cover:
            who.in_cover = False
            log(f'{who.name} leaves cover to attack.')

        resolve_attack(who, target, card, dcard, rng=rng, log=log, wheel=wheel)
        return action

    if kind == 'move':
        who.set_position(BACK if who.position == FRONT else FRONT, log=log)
    elif kind == 'cover':
        who.in_cover = True
        log(f'{who.name} takes cover.')
    else:
        log(f'{who.name} passes.')
    return action


def run(party, foes, wheel, log, rng, max_rounds=40):
    everyone = party + foes
    # The engine resolves "all allies" and "any enemy" against this, so it
    # has to be the fight actually being run. Set here rather than left to
    # the caller: a stale table silently points effects at combatants from
    # a previous fight, which is a wrong result rather than a crash.
    set_table(everyone)
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
                  deck=build_deck(pool, 12, 5, 4, 3, rng), position=FRONT,
                  team='party', rng=rng),
        Combatant('Corr', body=3, mind=5, soul=4,
                  deck=build_deck(pool, 12, 3, 5, 4, rng), position=BACK,
                  team='party', rng=rng),
    ]
    foes = [
        Combatant('Rootstalker', body=5, mind=2, soul=3,
                  deck=build_deck(pool, 10, 5, 2, 3, rng), position=FRONT,
                  team='foes', rng=rng),
        Combatant('Briarbundle', body=3, mind=3, soul=3,
                  deck=build_deck(pool, 9, 3, 3, 3, rng), position=BACK,
                  team='foes', rng=rng),
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
    set_table(everyone)
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
