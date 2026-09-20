"""Invariants the agents have to keep, checked because they are easy to break.

An agent is not specified by a rules file the way the engine is, so there is
nothing here to check it against except the properties it was built to have.
These are the ones whose failure would be silent.
"""

import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import cards as cardlib
import engine
from agents import KitAI, SimpleAI

FAILED = []


def check(name, ok, detail=''):
    print(f'  {"ok  " if ok else "FAIL"}  {name}' + (f'  — {detail}' if detail else ''))
    if not ok:
        FAILED.append(name)


def _pc(team):
    """A character with a mixed deck and two Passives, built here rather
    than read out of campaign/ so this test does not fail when a player
    edits their own sheet."""
    pool = cardlib.by_name(cardlib.core_pool())
    deck = [pool[n] for n in ('STRIKE', 'CHARGE', 'ENDURE', 'CALCULATE',
                              'STUDY', 'FOCUS', 'SUPPORT', 'ADAPT')
            if n in pool]
    c = engine.Combatant('probe', 3, 4, 2, deck=deck, team=team)
    c.passives = [
        cardlib.Card(name='RED PASSIVE', color='RED', stat='BODY',
                     attack='Body + d6', die=6, range='Melee'),
        cardlib.Card(name='BLUE PASSIVE', color='BLUE', stat='MIND',
                     attack='Mind + d4', die=4, range='Both'),
    ]
    return c


def colour_read_starts_neutral():
    """**An agent that has watched nothing must score exactly what a
    colour-blind one does.**

    `_attack_value` weights damage by the chance of winning the reveal, and
    that weighting is normalised so a flat prior is a no-op. If it stops
    being a no-op, every weight in the class silently changes meaning,
    because all of them were tuned against the unweighted scorer — and
    nothing else would report it.
    """
    me, foe = _pc('party'), _pc('foes')
    engine.set_table([me, foe])
    ag = KitAI()

    # Anchored on the arithmetic, not on the class with a flag flipped.
    # The first version of this test compared KitAI against a subclass with
    # the trust dialled to zero, which runs the same code — so breaking the
    # normalisation broke both sides equally and the test passed on code
    # that was measurably wrong. A self-comparison is not a check.
    worst, where = 0.0, ''
    for p in me.passives:                      # no Effect, so damage alone
        expected = me.stat(p.stat) + p.die / 2
        got = ag._attack_value(me, p, foe)
        if abs(got - expected) > worst:
            worst, where = abs(got - expected), f'{p.name} {got:.3f} vs {expected:.3f}'
    check('an unwatched opponent scores exactly stat + die/2', worst < 1e-9,
          where or 'no difference')


def colour_read_moves_with_evidence():
    """And once it has watched, it must actually move — a normalisation
    that is a no-op forever is just the old scorer with extra arithmetic."""
    me, foe = _pc('party'), _pc('foes')
    engine.set_table([me, foe])
    ag = KitAI()
    red = [c for c in cardlib.core_pool() if c.color == 'RED'][:8]
    foe.discard.extend(red)
    by_colour = {p.color: ag._attack_value(me, p, foe) for p in me.passives}
    # BLUE beats RED (cards.BEATS), so against a Red-heavy discard the Blue
    # option has to outscore the Red one.
    check('a watched Red deck makes Blue the better lead',
          by_colour['BLUE'] > by_colour['RED'],
          f'BLUE {by_colour["BLUE"]:.2f} against RED {by_colour["RED"]:.2f}')


def simple_ai_stays_colour_blind():
    """`SimpleAI` is the creature baseline the encounter figures in
    `rules/gm-guide.md` are built on. It plays to type and is not supposed
    to read a matchup; if it starts to, those figures move underneath the
    guide without anyone touching the guide."""
    check('SimpleAI does not read the matchup',
          not hasattr(SimpleAI, '_attack_value')
          and not hasattr(SimpleAI, '_MATCHUP_TRUST'))


def a_passive_is_free_to_play():
    """The Passive decision is a card-economy one (`Agent._card_price`):
    a Passive never leaves its zone, so it is never priced."""
    me = _pc('party')
    foes = [engine.Combatant(f'w{i}', 2, 1, 1, deck=[], team='foes')
            for i in range(3)]
    engine.set_table([me] + foes)
    engine.set_wheel(None)      # no wheel: the fallback counts live enemies
    ag = KitAI()

    me.hand = list(me.deck[:2])
    priced = ag._card_price(me)
    check('a hand card is priced when cards are tight', priced > 0,
          f'price {priced:.2f} holding 2 against 3')

    me.hand = list(me.deck[:8])
    check('and free when the hand covers what is coming',
          ag._card_price(me) == 0.0, 'holding 8 against 3')

    # A Passive is never priced, whatever the hand looks like, because it
    # does not leave its zone — that is the whole of why it gets reached for.
    me.hand = list(me.deck[:2])
    blade = me.passives[0]
    check('a Passive is never priced', me.is_passive(blade))


def knowledge_is_watched_not_known():
    """**An opponent's kit has to be established before it can be used.**

    Watching what someone plays is fair — that is the whole of
    `Knowledge`. Knowing how their cards *work* before they have shown you
    is not: an agent that reached into an opponent's stance list would know
    KILLSWITCH ends on a repeated colour, and which of its two modes was
    taken, having been shown neither.

    So what the tracker retains about anyone is asserted to be colour
    counts and nothing else. `test_information.py` holds the static half —
    that no agent reads those attributes at all; this holds the stored
    half, in case a future version keeps more than it reads out.
    """
    me, foe = _pc('party'), _pc('foes')
    engine.set_table([me, foe])
    ag = KitAI()

    pool = cardlib.by_name(cardlib.load())
    if 'KILLSWITCH' in pool:                       # a real Ongoing, face up
        foe.in_play.append(pool['KILLSWITCH'])
    foe.discard.extend([c for c in cardlib.core_pool() if c.color == 'RED'][:4])
    ag.known.observe(foe)

    stored = ag.known.colors.get(foe.name, {})
    ok = stored and all(k in ('RED', 'BLUE', 'GREEN', 'COLORLESS')
                        for k in stored)
    check('the tracker keeps colours and nothing else', bool(ok),
          f'{dict(stored)}')

    # Nothing anywhere in the tracker should be holding a card or its text.
    leaked = [k for k, v in vars(ag.known).items()
              if any(isinstance(x, cardlib.Card)
                     for x in (v.values() if isinstance(v, dict) else []))]
    check('and holds no cards of theirs', not leaked, str(leaked))


def position_is_a_decision():
    """Moving buys range legality and nothing else, so an agent holding
    cards that cannot reach from where it stands should walk.

    None of this shows up in the party benchmark — everyone starts at the
    Frontline and stays there, so the sweep says movement never pays and
    the agent almost never moves. These are the cases the benchmark cannot
    produce, checked directly so that "it never moves" stays a decision
    rather than quietly going back to being a limitation.
    """
    pool = cardlib.by_name(cardlib.core_pool())
    ag = KitAI(random.Random(0))

    # Frontline, holding only Ranged cards, against a Frontline enemy:
    # nothing reaches, and the Backline makes all of it live.
    me = engine.Combatant('me', 3, 4, 2, deck=[], position=engine.FRONT,
                          team='party')
    foe = engine.Combatant('foe', 3, 3, 3, deck=[], position=engine.FRONT,
                           team='foes')
    me._agent = ag
    engine.set_table([me, foe])
    me.hand = [pool['FOCUS'], pool['SUPPORT']]     # both Ranged
    check('walks when nothing in hand reaches from here',
          ag.choose_action(me, [foe], [])[0] == 'move',
          f'holding {[c.name for c in me.hand]} at {me.position}')

    # Same hand, now in the Backline: it reaches, so stay and use it.
    me.set_position(engine.BACK)
    act = ag.choose_action(me, [foe], [])
    check('and stays once the cards reach', act[0] == 'attack',
          f'chose {act[0]} at {me.position}')

    # Melee-only hand at the Backline against a Frontline enemy: nothing
    # reaches from here either, so close.
    me.hand = [pool['STRIKE']]
    check('closes when the hand is melee and the enemy is not',
          ag.choose_action(me, [foe], [])[0] == 'move',
          f'holding STRIKE at {me.position}')

    # Rooted: the same character cannot move, and Backline with a
    # melee-only hand has nothing to do but take cover.
    me.rooted = True
    act = ag.choose_action(me, [foe], [])
    check('takes cover when rooted with nothing that reaches',
          act[0] == 'cover', f'chose {act[0]}')
    me.rooted = False


def moving_does_not_cost_the_focus_fire():
    """Position is one decision and target is another. An earlier cut
    folded them together and quietly dropped `_weakest`, which cost six
    points of party win rate and read as a finding about movement."""
    ag = KitAI(random.Random(0))
    pool = cardlib.by_name(cardlib.core_pool())
    me = engine.Combatant('me', 3, 4, 2, deck=[], position=engine.FRONT,
                          team='party')
    hurt = engine.Combatant('hurt', 3, 3, 3, deck=[], position=engine.FRONT,
                            team='foes')
    fresh = engine.Combatant('fresh', 3, 3, 3, deck=[], position=engine.FRONT,
                             team='foes')
    me._agent = ag
    engine.set_table([me, hurt, fresh])
    me.hand = [pool['STRIKE']]
    hurt.seen_damage = 9
    act = ag.choose_action(me, [hurt, fresh], [])
    check('still hits whoever has taken the most',
          act[0] == 'attack' and act[1] is hurt,
          f'{act[0]} {getattr(act[1], "name", "")}')


print('Agent invariants:')
colour_read_starts_neutral()
colour_read_moves_with_evidence()
knowledge_is_watched_not_known()
position_is_a_decision()
moving_does_not_cost_the_focus_fire()
simple_ai_stays_colour_blind()
a_passive_is_free_to_play()

if FAILED:
    print(f'\n{len(FAILED)} agent invariant(s) broken.')
    raise SystemExit(1)
print('\nAll agent invariants hold.')
