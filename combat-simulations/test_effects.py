"""`rules/card-glossary.md` as assertions, through the cards that use it.

Two things are checked. First that the reader in effects.py turns prose
into the ops it should — a compile test, no fight required. Then that the
ops do what the glossary says when they run, which is where a keyword's
actual ruling gets tested: Ward eating a Debuff, Rooted cancelling forced
movement, Anchored not paying on the turn it is played.

    python3 test_effects.py
"""

import random

import cards as cardlib
import effects as fx
from engine import BACK, FRONT, Combatant, set_table

FAILURES = []
QUIET = lambda *a: None


def check(label, condition, detail=''):
    if condition:
        print(f'  ok    {label}')
    else:
        print(f'  FAIL  {label}' + (f' — {detail}' if detail else ''))
        FAILURES.append(label)


def duo(**kw):
    a = Combatant('A', kw.get('ab', 3), kw.get('am', 3), kw.get('as_', 3),
                  deck=[], position=FRONT, team='party')
    b = Combatant('B', 3, 3, 3, deck=[], position=FRONT, team='foes')
    set_table([a, b])
    return a, b


def run(text, actor, opponent, outcome='attacker wins', dealt=0, card=None):
    ops = fx.compile_half(text)
    assert ops is not None, f'did not compile: {text!r}'
    ctx = fx.Context(actor, opponent, allies=[], enemies=[opponent],
                     card=card, outcome=outcome, damage_dealt=dealt,
                     rng=random.Random(0), log=QUIET)
    ctx.wheel = None
    for op in ops:
        op.apply(ctx)
    return ctx


# ---- reading the prose --------------------------------------------------

def test_compile():
    print('The reader')
    c = fx.compile_half
    check('a bare grant is self-targeted',
          c('Gain Resist.')[0].target == fx.SELF)
    check('"Defender gains" and "Attacker gains" are the same op',
          repr(c('Defender gains Weak.')) == repr(c('Attacker gains Weak.')))
    check('a number after the keyword is the stack count',
          c('Gain Thorns 4.')[0].n == 4)
    check('"twice" is two stacks', c('Gain Deadly twice.')[0].n == 2)
    check('a clause list keeps its order',
          [o.status for o in c('Gain Deadly, Resist, and Quick.')]
          == ['deadly', 'resist', 'quick'])
    check('a bare verb inherits the subject named before it',
          c('Target ally heals 4 and draws 1.')[1].target == fx.ALLY)
    check('with no subject named, the actor is the subject',
          c('Draw 1 and heal 5 HP')[1].target == fx.SELF)
    check('Anchored wraps what follows it',
          isinstance(c('Anchored — Gain Resist 1.')[0], fx.Anchored))
    check('a trailing win condition reads as a leading one',
          isinstance(c('Counter Attack. On a clean win only.')[0], fx.Gated))
    check('a half with one unreadable clause does not compile',
          c('Heal 2 × your Soul. Skip your draw step next turn.') is None)
    check('an unknown keyword does not silently drop',
          c('Gain Sparkle.') is None)


# ---- what the ops do ----------------------------------------------------

def test_ward():
    print('\nWard — prevents the next Debuff, expires on use')
    a, b = duo()
    b.ward = 1
    run('Defender gains Weak.', a, b)
    check('the Debuff is prevented', b.weak == 0, b.weak)
    check('the Ward is spent', b.ward == 0, b.ward)
    run('Defender gains Weak.', a, b)
    check('the next one lands', b.weak == 1, b.weak)

    a2, b2 = duo()
    b2.ward = 1
    run('Defender gains Resist.', a2, b2)
    check('a Positive Status Effect does not consume Ward',
          b2.resist == 1 and b2.ward == 1, (b2.resist, b2.ward))


def test_rooted():
    print('\nRooted — cancels the next movement, forced included')
    a, b = duo()
    b.rooted = 1
    run('Move target to backline', a, b)
    check('forced movement is cancelled', b.position == FRONT, b.position)
    check('the charge is spent doing it', b.rooted == 0, b.rooted)
    run('Move target to backline', a, b)
    check('the next movement goes through', b.position == BACK, b.position)

    c, _ = duo()
    c.rooted = 1
    check('it stops the holder\'s own move too',
          c.set_position(BACK) is False and c.position == FRONT)


def test_anchored():
    print('\nAnchored — pays from your next turn, ends when you move')
    a, b = duo()
    run('Anchored — Gain Resist 1.', a, b)
    check('nothing happens on the turn it is played', a.resist == 0, a.resist)
    check('it is being sustained', len(a.anchored) == 1)
    a.tick_anchors(b, [], [b], random.Random(0), QUIET)
    check('it pays at the start of your next turn', a.resist == 1, a.resist)
    a.tick_anchors(b, [], [b], random.Random(0), QUIET)
    check('and again the turn after', a.resist == 2, a.resist)
    a.set_position(BACK)
    check('moving ends it', a.anchored == [], a.anchored)
    a.tick_anchors(b, [], [b], random.Random(0), QUIET)
    check('so it stops paying', a.resist == 2, a.resist)

    c, d = duo()
    run('Anchored — Gain Resist 1.', c, d)
    c.take(99, log=QUIET)
    check('Collapsing ends it too', c.anchored == [], c.anchored)


def test_gates():
    print('\nGates — a clause that only fires on its condition')
    a, b = duo()
    run('Only on a clean win — not a tie. Defender gains Staggered.',
        a, b, outcome='tie')
    check('a tie does not satisfy "clean win only"', b.staggered == 0)
    run('Only on a clean win — not a tie. Defender gains Staggered.',
        a, b, outcome='attacker wins')
    check('a clean win does', b.staggered == 1)

    c, dd = duo()
    c.hp = 20
    run('If your HP is 6 or less, gain Immunity.', c, dd)
    check('above the threshold, nothing', c.immunity == 0)
    c.hp = 6
    run('If your HP is 6 or less, gain Immunity.', c, dd)
    check('at the threshold, it fires', c.immunity == 1)


def test_lifesteal():
    print('\nLifesteal — half the damage that actually landed, rounded down')
    a, b = duo()
    a.hp = 10
    run('Lifesteal', a, b, dealt=7)
    check('7 damage heals 3', a.hp == 13, a.hp)
    a.hp = 10
    run('Lifesteal', a, b, dealt=0)
    check('no damage heals nothing', a.hp == 10, a.hp)


def test_costs_are_unpreventable():
    print('\nHP costs ignore the damage pipeline')
    a, b = duo()
    a.resist = 1
    a.hp = 20
    run('Pay 2 HP, target ally heals 5 HP', a, b)
    check('Resist does not halve an HP cost', a.hp == 18, a.hp)
    check('and is not spent by one', a.resist == 1, a.resist)


def test_statloss():
    print('\nStat loss moves Max HP with it')
    a, b = duo()
    before = b.max_hp
    run('Target loses 1 Body this combat.', a, b)
    check('Max HP drops by 4 when Body drops by 1',
          b.max_hp == before - 4, (before, b.max_hp))
    check('current HP is pulled down to the new maximum',
          b.hp <= b.max_hp, (b.hp, b.max_hp))


def test_status_cards():
    print('\nStatus cards are real cards that cannot be played')
    a, b = duo()
    run('Add 1 Wound to the bottom of the defender\'s deck.', a, b)
    check('the Wound is in the deck', len(b.deck) == 1 and b.deck[0].name == 'WOUND')
    b.hand.append(b.deck.pop())
    check('and it is not playable', b.playable(a) == [], b.playable(a))


def test_pool_compiles_or_narrates():
    print('\nThe pool')
    pool = cardlib.core_pool()
    done, left = fx.coverage(pool)
    total = len(done) + len(left)
    check(f'{len(done)}/{total} halves compile; the rest narrate rather '
          f'than half-apply', len(done) > 0 and len(done) + len(left) == total)
    broken = []
    for c in pool:
        for half in ('effect', 'defense_effect'):
            text = getattr(c, half)
            if not text:
                continue
            try:
                fx.compile_half(text)
            except Exception as e:                      # noqa: BLE001
                broken.append((c.name, half, e))
    check('no half raises while being read', not broken, broken[:3])


if __name__ == '__main__':
    test_compile()
    test_ward()
    test_rooted()
    test_anchored()
    test_gates()
    test_lifesteal()
    test_costs_are_unpreventable()
    test_statloss()
    test_status_cards()
    test_pool_compiles_or_narrates()
    print()
    if FAILURES:
        print(f'{len(FAILURES)} failed.')
        raise SystemExit(1)
    print('All effect checks pass.')
