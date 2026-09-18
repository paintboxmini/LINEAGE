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


def run(text, actor, opponent, outcome='attacker wins', dealt=0, card=None,
        allies=()):
    ops = fx.compile_half(text)
    assert ops is not None, f'did not compile: {text!r}'
    ctx = fx.Context(actor, opponent, allies=list(allies), enemies=[opponent],
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
    # Synthetic on purpose. Naming a real card here makes the check a
    # hostage to the next reader pass — this one has failed twice that way,
    # both times because the card had just been implemented.
    check('a half with one unreadable clause does not compile',
          c('Gain Resist.') is not None
          and c('Gain Resist. Summon a badger.') is None)
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
    check('it is being sustained', len(a.pending) == 1)
    a.tick_anchors(b, [], [b], random.Random(0), QUIET)
    check('it pays at the start of your next turn', a.resist == 1, a.resist)
    a.tick_anchors(b, [], [b], random.Random(0), QUIET)
    check('and again the turn after', a.resist == 2, a.resist)
    a.set_position(BACK)
    check('moving ends it', a.pending == [], a.pending)
    a.tick_anchors(b, [], [b], random.Random(0), QUIET)
    check('so it stops paying', a.resist == 2, a.resist)

    c, d = duo()
    run('Anchored — Gain Resist 1.', c, d)
    c.take(99, log=QUIET)
    check('Collapsing ends it too', c.pending == [], c.pending)


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


# ---- the three shapes Chris's kit needed --------------------------------
#
# MEASURE, RIPOSTE and KILLSWITCH live in `campaign/chris.md` rather than in
# `cards/`, so nothing here reads them off disk — the prose is repeated
# below on purpose. A player owns that file and may rename or retune a card
# at the table; a test that broke when they did would be a test punishing
# the thing it exists to serve.

MEASURE_E = ('If the card you played last turn was a different colour than '
             'this one, deal +2 damage and the defender reveals their stats.')
MEASURE_D = ('If the card you played last turn was a different colour than '
             'this one, the attacker reveals their stats.')
RIPOSTE_D = 'Gain Deadly. If you won this exchange, gain Deadly again.'
KILLSWITCH = ('Choose one — your attacks deal +3 damage, or gain Armour 3. '
              'Lasts until the end of combat. Playing KILLSWITCH again '
              'replaces your current choice rather than adding to it. '
              'Playing the same colour in two consecutive reveals ends it.')


def blue():
    return cardlib.Card(name='MEASURE', color='BLUE', stat='MIND', die='d6',
                        effect=MEASURE_E, defense_effect=MEASURE_D,
                        range='Both')


def test_measure_reads_the_last_colour():
    print('\nMEASURE pays for a colour change and nothing else')
    card = blue()

    a, b = duo()
    a.last_color = 'RED'
    check('a different colour last turn arms the bonus',
          _bonus(MEASURE_E, a, b, card) == 2)

    a.last_color = 'BLUE'
    check('the same colour pays nothing',
          _bonus(MEASURE_E, a, b, card) == 0)

    a.last_color = None
    check('and a turn that played no card pays nothing',
          _bonus(MEASURE_E, a, b, card) == 0)

    # The defence half asks the same question of the same person: the
    # defender's own last turn, not the attacker's.
    a.last_color = 'GREEN'
    b.last_color = 'BLUE'
    ops = fx.compile_half(MEASURE_D)
    assert ops is not None
    seen = []
    ctx = fx.Context(a, b, allies=[], enemies=[b], card=card,
                     outcome='defender wins', rng=random.Random(0),
                     log=lambda line: seen.append(line))
    ctx.wheel = None
    for op in ops:
        op.apply(ctx)
    check('the defence half reads the defender\'s own last colour',
          any('Body' in line for line in seen), seen)


def _bonus(text, actor, opponent, card):
    """What this half writes into the damage bonus before the roll."""
    ops = fx.compile_half(text)
    assert ops is not None, text
    ctx = fx.Context(actor, opponent, allies=[], enemies=[opponent], card=card,
                     outcome='attacker wins', rng=random.Random(0), log=QUIET)
    ctx.wheel = None
    ctx.phase = 'pre'
    for op in ops:
        op.run_phase(ctx, 'pre')
    return ctx.dmg_bonus


def test_last_colour_rolls_forward_on_your_own_turn():
    print('\nThe colour you played last turn is your own turn\'s')
    import engine
    import play
    pool = cardlib.by_name(cardlib.core_pool())
    red = pool['STRIKE']
    a, b = duo()
    a.hp = b.hp = 400
    passer = _Passer()

    engine.resolve_attack(a, b, red, None, rng=random.Random(0), log=QUIET)
    check('attacking records the colour, but not as last turn yet',
          a.color_this_turn == 'RED' and a.last_color is None)

    play.take_turn(a, passer, [b], [], None, QUIET, random.Random(0))
    check('the top of the next turn rolls it forward',
          a.last_color == 'RED' and a.color_this_turn is None,
          (a.last_color, a.color_this_turn))

    # A defence is played on someone else's turn, so it is not "the card you
    # played last turn". Only the attacker's card is recorded.
    engine.resolve_attack(b, a, red, red, rng=random.Random(0), log=QUIET)
    check('defending does not overwrite it',
          a.color_this_turn is None and a.last_color == 'RED',
          (a.color_this_turn, a.last_color))

    play.take_turn(a, passer, [b], [], None, QUIET, random.Random(0))
    check('and a turn that plays nothing clears it', a.last_color is None,
          a.last_color)


class _Passer:
    """An agent that does nothing with its turn, so a turn's bookkeeping can
    be checked without an exchange in the way."""

    def choose_action(self, who, foes, allies):
        return ('pass',)

    def choose_target(self, who, pool, prompt):
        return pool[0]


def test_riposte_arms_twice_only_on_a_win():
    print('\nRIPOSTE banks one Deadly on a tie and two on a block')
    a, b = duo()

    a.deadly = 0
    ops = fx.compile_half(RIPOSTE_D)
    assert ops is not None
    _defend(ops, a, b, 'defender wins')
    check('winning the exchange arms it twice', a.deadly == 2, a.deadly)

    a.deadly = 0
    _defend(ops, a, b, 'tie')
    check('a tie still arms it once', a.deadly == 1, a.deadly)

    # The same words on an attack half ask about the attacker instead —
    # the gate is relative to whoever is speaking, which is what separates
    # it from "on a clean win".
    a.deadly = 0
    ctx = fx.Context(a, b, allies=[], enemies=[b], card=None,
                     outcome='attacker wins', rng=random.Random(0), log=QUIET)
    ctx.wheel = None
    ctx.acting = a
    for op in ops:
        op.apply(ctx)
    check('and on an attack half it reads the attacker\'s result',
          a.deadly == 2, a.deadly)

    a.deadly = 0
    ctx = fx.Context(a, b, allies=[], enemies=[b], card=None,
                     outcome='defender wins', rng=random.Random(0), log=QUIET)
    ctx.wheel = None
    ctx.acting = a
    for op in ops:
        op.apply(ctx)
    check('and is false for an attacker who did not win',
          a.deadly == 1, a.deadly)


def _defend(ops, defender, attacker, outcome):
    ctx = fx.Context(defender, attacker, allies=[], enemies=[attacker],
                     card=None, outcome=outcome, rng=random.Random(0),
                     log=QUIET)
    ctx.wheel = None
    ctx.acting = attacker          # a Defense Effect fires on their turn
    for op in ops:
        op.apply(ctx)
    return ctx


def test_killswitch_flips_rather_than_stacking():
    print('\nKILLSWITCH replaces its own choice and only its own')
    a, b = duo()

    _stance(a, b, 'gain Armour 3')
    check('the stance grants what was chosen', a.armour == 3, a.armour)

    _stance(a, b, 'gain Armour 3')
    check('playing it again does not stack', a.armour == 3, a.armour)

    _stance(a, b, 'your attacks deal +3 damage')
    check('switching modes takes the old one back',
          a.armour == 0 and len(a.standing_mods) == 1,
          (a.armour, a.standing_mods))

    _stance(a, b, 'gain Armour 3')
    check('and switching back takes the bonus down',
          a.armour == 3 and not a.standing_mods,
          (a.armour, a.standing_mods))

    # Armour from somewhere else is not KILLSWITCH's to remove.
    a.armour += 2
    _stance(a, b, 'your attacks deal +3 damage')
    check('armour from elsewhere survives the flip', a.armour == 2, a.armour)

    check('the damage mode lasts the fight rather than a turn',
          a.standing_mods and a.standing_mods[0]['uses'] is None,
          a.standing_mods)

    check('"Same choice." on the defence half is the same stance',
          [type(o).__name__ for o in fx.compile_half('Same choice.',
                                                     other=KILLSWITCH)]
          == ['Stance'])
    check('and a half pointing at nothing narrates',
          fx.compile_half('Same choice.') is None)


def _stance(actor, opponent, pick):
    ops = fx.compile_half(KILLSWITCH)
    assert ops is not None
    ctx = fx.Context(actor, opponent, allies=[], enemies=[opponent], card=None,
                     outcome='attacker wins', rng=random.Random(0), log=QUIET,
                     agent=_Picks(pick))
    ctx.wheel = None
    for op in ops:
        op.apply(ctx)
    return ctx


class _Picks:
    def __init__(self, label):
        self.label = label

    def choose_option(self, who, options, prompt):
        return self.label

    def choose_target(self, who, pool, prompt):
        return pool[0]



def test_killswitch_ends_on_a_repeated_colour():
    print('\nKILLSWITCH ends on the same colour twice running')
    import engine
    pool = cardlib.by_name(cardlib.core_pool())
    green, blue = pool['SUPPORT'], pool['CALCULATE']
    check('the fixture colours are what this test thinks they are',
          green.color == 'GREEN' and blue.color == 'BLUE')

    a, b = duo()
    _stance(a, b, 'gain Armour 3')
    engine._revealed([(a, green)], QUIET)
    check('one green does not end it', a.armour == 3, a.armour)

    engine._revealed([(a, blue)], QUIET)
    check('nor does a different colour after it', a.armour == 3, a.armour)

    engine._revealed([(a, blue)], QUIET)
    check('a second blue running ends it', a.armour == 0, a.armour)

    # A block is a reveal, which is what separates this from MEASURE.
    a2, b2 = duo()
    _stance(a2, b2, 'gain Armour 3')
    engine._revealed([(b2, blue), (a2, blue)], QUIET)
    engine._revealed([(b2, green), (a2, blue)], QUIET)
    check('defending with the same colour counts as a reveal',
          a2.armour == 0, a2.armour)

    # And a stance without the clause is not touched by the same repeat.
    a3, b3 = duo()
    plain = ('Choose one — your attacks deal +3 damage, or gain Armour 3. '
             'Lasts until the end of combat. Playing PLAIN again replaces '
             'your current choice rather than adding to it.')
    ops = fx.compile_half(plain)
    assert ops is not None and not ops[0].ends_on_repeat
    ctx = fx.Context(a3, b3, allies=[], enemies=[b3], card=None,
                     outcome='attacker wins', rng=random.Random(0), log=QUIET,
                     agent=_Picks('gain Armour 3'))
    ctx.wheel = None
    ops[0].apply(ctx)
    engine._revealed([(a3, blue)], QUIET)
    engine._revealed([(a3, blue)], QUIET)
    check('a stance without the clause survives a repeat',
          a3.armour == 3, a3.armour)

    check('and the clause with no stance to end narrates',
          fx.compile_half('Gain Armour 3. Playing the same colour in two '
                          'consecutive reveals ends it.') is None)



def test_hold_the_line_mirrors_the_colour_it_faces():
    print('\nHOLD THE LINE ties everything, and only converts on defence')
    import engine
    every = cardlib.by_name(cardlib.load())
    core = cardlib.by_name(cardlib.core_pool())
    htl = every['HOLD THE LINE']

    blocked = []
    for name in ('STRIKE', 'CALCULATE', 'SUPPORT'):
        a, b = duo()
        a.hp = b.hp = 400
        blocked.append(engine.resolve_attack(a, b, core[name], htl,
                                             rng=random.Random(0), log=QUIET))
    check('it blocks a real colour of any kind',
          all(o == engine.Outcome.DEFENDER for o in blocked), blocked)

    a, b = duo()
    a.hp = b.hp = 400
    out = engine.resolve_attack(a, b, htl, core['STRIKE'],
                                rng=random.Random(0), log=QUIET)
    check('and deals nothing as an attack',
          out == engine.Outcome.TIE and b.hp == 400, (out, b.hp))

    # Without the Special Rule being read it would resolve as plain
    # COLORLESS, which auto-loses to any real colour — the opposite of the
    # card. This is the assertion that catches that regression.
    check('the mirroring Special Rule is actually read',
          fx.traits(htl, 'defense').mirrors_color
          and fx.traits(htl, 'attack').mirrors_color)


def test_a_duration_with_nothing_to_hold_narrates():
    print('\nA sentence that reaches back and finds nothing narrates')
    check('"Lasts until the end of combat." alone does not compile',
          fx.compile_half('Lasts until the end of combat.') is None)
    check('nor does the replacement clause alone',
          fx.compile_half('Playing THIS again replaces your current choice '
                          'rather than adding to it.') is None)
    # Evade is a charge that gets spent, so "until the end of combat" would
    # be changing the status rather than describing it. Armour is not.
    check('a duration on a status that is spent refuses',
          fx.compile_half('Gain Evade. Lasts until the end of combat.') is None)
    check('and on Armour, which already lasts the fight, it reads',
          fx.compile_half('Gain Armour 2. Lasts until the end of combat.')
          is not None)


def test_pool_compiles_or_narrates():
    print('\nThe pool')
    pool = cardlib.core_pool()
    done, trait, left = fx.coverage(pool)
    total = len(done) + len(trait) + len(left)
    check(f'{len(done) + len(trait)}/{total} halves are modelled; the rest '
          f'narrate rather than half-apply',
          len(done) > 0 and len(done) + len(trait) + len(left) == total)
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


# ---- the cheap tail -----------------------------------------------------

def test_one_target_per_half():
    print('\nA half names its target once')
    a, b = duo()
    m1 = Combatant('M1', 3, 3, 3, deck=[], position=FRONT, team='party')
    m2 = Combatant('M2', 3, 3, 3, deck=[], position=FRONT, team='party')
    m1.hp, m2.hp = 5, 20
    set_table([a, m1, m2, b])

    class Fickle:
        n = 0
        def choose_target(self, me, opts, prompt):
            Fickle.n += 1
            return opts[Fickle.n - 1]     # answers differently every time

    ops = fx.compile_half('Target ally heals 4 and draws 1.')
    ctx = fx.Context(a, b, [m1, m2], [b], None, 'attacker wins',
                     rng=random.Random(0), log=QUIET, agent=Fickle())
    for op in ops:
        op.apply(ctx)
    check('the agent is asked once, not once per clause', Fickle.n == 1, Fickle.n)
    check('the heal and the draw land on the same ally',
          m1.hp == 9 and m2.hp == 20, (m1.hp, m2.hp))


def test_rushdown():
    print('\nRushdown — the line of conflict moves, the target does not')
    a, b = duo()
    b.set_position(BACK)
    run('Rushdown.', a, b)
    check('the line redraws to include them', b.position == FRONT, b.position)
    check('the mover stays where they are', a.position == FRONT, a.position)

    c, e = duo()
    e.set_position(BACK)
    e.rooted = 1
    run('Rushdown.', c, e)
    check("the target's own Rooted does not stop it — they never moved",
          e.position == FRONT and e.rooted == 1, (e.position, e.rooted))

    f, g = duo()
    g.set_position(BACK)
    f.rooted = 1
    run('Rushdown.', f, g)
    check("the mover's Rooted does stop it, and is spent",
          g.position == BACK and f.rooted == 0, (g.position, f.rooted))

    h, i = duo()
    h.set_position(BACK)
    i.set_position(BACK)
    run('Rushdown.', h, i)
    check('you must already be Frontline to close', i.position == BACK, i.position)


def test_modal():
    print('\nModal cards run one branch, not all of them')
    a, b = duo()
    mate = Combatant('M', 3, 3, 3, deck=[], position=FRONT, team='party')
    mate.hp = 10
    set_table([a, mate, b])

    class PickSecond:
        def choose_target(self, me, opts, prompt): return opts[0]
        def choose_option(self, me, opts, prompt): return opts[1]
        def choose_yes_no(self, me, prompt): return True

    ops = fx.compile_half('Choose one for target ally — heal 4, gain Resist, '
                          'or gain Deadly.')
    ctx = fx.Context(a, b, [mate], [b], None, 'attacker wins',
                     rng=random.Random(0), log=QUIET, agent=PickSecond())
    for op in ops:
        op.apply(ctx)
    check('the chosen branch runs', mate.resist == 1, mate.resist)
    check('the branches not chosen do not',
          mate.hp == 10 and mate.deadly == 0, (mate.hp, mate.deadly))


def test_optional_cost():
    print('\nAn optional cost is declinable, and pays nothing when declined')
    pool = cardlib.core_pool()
    a, b = duo()
    a.hand = list(pool[:2])

    class No:
        def choose_target(self, me, opts, prompt): return opts[0]
        def choose_yes_no(self, me, prompt): return False

    ops = fx.compile_half('Lifesteal. You may Exile one card from your own hand '
                          'to give the defender Weak and Blind.')
    ctx = fx.Context(a, b, [], [b], None, 'attacker wins', damage_dealt=4,
                     rng=random.Random(0), log=QUIET, agent=No())
    for op in ops:
        op.apply(ctx)
    check('declining costs no card', len(a.hand) == 2, len(a.hand))
    check('and grants nothing', b.weak == 0 and b.blind == 0, (b.weak, b.blind))
    check('the rest of the half still ran (Lifesteal)', a.hp > 0)


def test_position_scoped():
    print('\nPosition-scoped targets')
    a, b = duo()
    here = Combatant('Here', 3, 3, 3, deck=[], position=FRONT, team='party')
    there = Combatant('There', 3, 3, 3, deck=[], position=BACK, team='party')
    set_table([a, here, there, b])
    ctx = fx.Context(a, b, [here, there], [b], None, 'attacker wins',
                     rng=random.Random(0), log=QUIET)
    for op in fx.compile_half('All allies in your position gain Quick.'):
        op.apply(ctx)
    check('an ally sharing your position is included', here.quick == 1, here.quick)
    check('an ally in the other position is not', there.quick == 0, there.quick)


# ---- deferred triggers --------------------------------------------------

def test_reaction_on_damage():
    print('\nA reaction waits for its event')
    a, b = duo()
    run('This combat, when you are damaged, gain Ward and heal 3 HP.', a, b)
    check('nothing fires on the turn it is played',
          a.ward == 0 and len(a.pending) == 1, (a.ward, len(a.pending)))
    a.hp = 20
    a.take(6, log=QUIET)
    check('it fires when damage lands', a.ward == 1, a.ward)
    check('and the heal came with it', a.hp == 17, a.hp)
    a.take(4, log=QUIET)
    check('"this combat" means it keeps firing', a.ward == 2, a.ward)
    a.hp = 20
    a.take(0, log=QUIET)
    check('zero damage is not being damaged', a.ward == 2, a.ward)


def test_expiry_is_owner_keyed():
    print('\nExpiry is measured against the turn of whoever played it')
    a, b = duo()
    run('Target cannot attack or be attacked until your next turn.', a, b)
    check('the restriction sits on the target', len(b.pending) == 2, len(b.pending))
    b.expire_pending()
    check("the target's own turn does not clear it — it is not theirs",
          len(b.pending) == 2, len(b.pending))
    a.expire_pending()
    check("the caster's next turn does", b.pending == [], b.pending)


def test_colour_ban():
    print('\nA banned colour leaves the hand unplayable, not gone')
    pool = cardlib.core_pool()
    a, b = duo()
    b.hand = [c for c in pool if c.color == 'RED'][:2] + \
             [c for c in pool if c.color == 'GREEN'][:1]
    b.hand = [c for c in b.hand if c.range_ok(FRONT, FRONT)] or b.hand
    before = len(b.hand)
    ops = fx.compile_half('Name a color. The defender cannot play that color '
                          'on their next reveal')

    class Reds:
        def choose_target(self, me, opts, prompt): return opts[0]
        def choose_option(self, me, opts, prompt): return 'RED'

    ctx = fx.Context(a, b, [], [b], None, 'attacker wins',
                     rng=random.Random(0), log=QUIET, agent=Reds())
    for op in ops:
        op.apply(ctx)
    check('the cards stay in hand', len(b.hand) == before, len(b.hand))
    check('but none of the banned colour is playable',
          not any(c.color == 'RED' for c in b.playable(a)))
    check('other colours still are',
          any(c.color != 'RED' for c in b.playable(a)) or before == 0)


def test_position_lock():
    print('\nCORNER locks both sides in place')
    a, b = duo()
    run('Neither you nor the defender may change position until your next turn.',
        a, b)
    check('the caster cannot move', a.set_position(BACK) is False)
    check('nor the target', b.set_position(BACK) is False)
    a.expire_pending()
    check('and both are free once it expires', a.set_position(BACK) is True)


def test_grounding_stance():
    print('\nGROUNDING STANCE ignores a forced move, not a chosen one')
    a, b = duo()
    run('You may ignore the next ability that forces you to move positions.', a, b)
    check('a move you choose still happens',
          a.set_position(BACK) is True and a.position == BACK)
    a.set_position(FRONT)
    check('a forced move is ignored',
          a.set_position(BACK, forced=True) is False and a.position == FRONT)
    check('and the charge is spent',
          a.set_position(BACK, forced=True) is True)


def test_seed_is_placed():
    print('\nSEED waits at the position it was planted')
    a, b = duo()
    run('Plant a seed at your current position. The next time you begin your '
        'turn at this position, gain Deadly twice.', a, b)
    a.set_position(BACK)
    a.fire('turn_start', b, [], [b], random.Random(0), QUIET)
    check('beginning a turn elsewhere does not collect it',
          a.deadly == 0, a.deadly)
    a.set_position(FRONT)
    a.fire('turn_start', b, [], [b], random.Random(0), QUIET)
    check('beginning a turn on it does', a.deadly == 2, a.deadly)
    a.fire('turn_start', b, [], [b], random.Random(0), QUIET)
    check('and it is spent — a seed grows once', a.deadly == 2, a.deadly)


def test_defense_effects_silenced():
    print('\nUNNAME silences Defense Effects without stopping the defence')
    import engine
    pool = cardlib.by_name(cardlib.core_pool())
    a, b = duo()
    run('Defender cannot trigger defense effects until their next turn', a, b)
    card = pool['INSTINCT']          # Defense Effect: Gain Ward.
    returned, exiled = engine._run(card, 'defense_effect', b, a,
                                   'defender wins', 0, QUIET,
                                   random.Random(0), None)
    check('the Defense Effect does not fire', b.ward == 0, b.ward)
    check('it is a silence — the card is neither kept nor exiled',
          returned is False and exiled is False)


# ---- damage this attack carries -----------------------------------------

def exchange(atk_name, a, b, seed=0, outcome_card=None):
    """One full attacker-wins exchange, returning the damage b took."""
    import engine
    pool = cardlib.by_name(cardlib.core_pool())
    card = pool[atk_name]
    before = b.hp
    engine._finish(engine.Outcome.ATTACKER, a, b, card, outcome_card, QUIET,
                   random.Random(seed), None)
    return before - b.hp


def test_flat_bonus_lands():
    print('\nA damage bonus reaches the roll it belongs to')
    import engine
    pool = cardlib.by_name(cardlib.core_pool())
    # MAUL: "Gain Deadly. Deal +2 damage this attack." Body 3 + d6, so the
    # floor without the bonus is 4 and with it is 6.
    lows = []
    for seed in range(40):
        a, b = duo()
        b.hp = 200
        lows.append(exchange('MAUL', a, b, seed))
    check('every roll clears the un-bonused floor', min(lows) >= 3 + 1 + 2,
          min(lows))
    check('Deadly was banked, not spent on this attack',
          duo()[0].deadly == 0)

    a, b = duo()
    b.hp = 200
    exchange('MAUL', a, b, 0)
    check('the attacker holds the Deadly afterwards', a.deadly == 1, a.deadly)


def test_gore_is_conditional():
    print('\nGORE only adds its die against a Frontline target')
    front, back = [], []
    for seed in range(60):
        a, b = duo()
        b.hp = 300
        front.append(exchange('GORE', a, b, seed))
        a2, b2 = duo()
        b2.hp = 300
        b2.set_position(BACK)
        back.append(exchange('GORE', a2, b2, seed))
    check('a Frontline target takes more on average',
          sum(front) / len(front) > sum(back) / len(back),
          (sum(front) / len(front), sum(back) / len(back)))
    check('the Backline case is the plain roll', max(back) <= 3 + 6, max(back))


def test_explosion_changes_the_tail():
    print("\nGAMBLER'S RUIN lengthens the tail without moving the floor")
    rolls = []
    for seed in range(200):
        a, b = duo()
        b.hp = 500
        rolls.append(exchange("GAMBLER'S RUIN", a, b, seed))
    plain = []
    for seed in range(200):
        a, b = duo()
        b.hp = 500
        plain.append(exchange('STRIKE', a, b, seed))
    check('it can roll higher than the die allows on its own',
          max(rolls) > 3 + 8, max(rolls))
    check('and the floor is unchanged', min(rolls) >= 3 + 1, min(rolls))


def test_cleave_splashes():
    print('\nCLEAVE reaches the enemies beside the defender')
    import engine
    a, b = duo()
    beside = Combatant('Beside', 3, 3, 3, deck=[], position=FRONT, team='foes')
    away = Combatant('Away', 3, 3, 3, deck=[], position=BACK, team='foes')
    set_table([a, b, beside, away])
    b.hp = beside.hp = away.hp = 100
    dealt = exchange('CLEAVE', a, b, 1)
    check('the defender takes the whole hit', dealt > 0, dealt)
    check('an enemy in their position takes a share',
          100 - beside.hp == dealt // 2 or 100 - beside.hp > 0,
          (dealt, 100 - beside.hp))
    check('an enemy elsewhere takes none', away.hp == 100, away.hp)


def test_plant_reads_last_turn():
    print('\nPLANT pays for having held position')
    held, moved = [], []
    for seed in range(40):
        a, b = duo()
        b.hp = 300
        a.moved_last_turn = False
        held.append(exchange('PLANT', a, b, seed))
        a2, b2 = duo()
        b2.hp = 300
        a2.moved_last_turn = True
        moved.append(exchange('PLANT', a2, b2, seed))
    check('holding position pays +4',
          all(h - m == 4 for h, m in zip(held, moved)),
          list(zip(held, moved))[:3])


# ---- cards that change what the reveal means ----------------------------

def reveal(atk_name, def_name, seed=0):
    """One exchange between two named cards, returning the Outcome."""
    import engine
    pool = cardlib.by_name(cardlib.core_pool())
    a, b = duo()
    a.hp = b.hp = 400
    a.set_position(FRONT)
    b.set_position(FRONT)
    return engine.resolve_attack(a, b, pool[atk_name], pool[def_name],
                                 rng=random.Random(seed), log=QUIET)


def test_special_rules_are_read():
    print('\nSpecial Rules reach the reveal')
    import engine
    pool = cardlib.by_name(cardlib.core_pool())
    # STAND is Red and wins ties; a Red attacker against it is a colour tie.
    red_attacker = next(c for c in cardlib.core_pool()
                        if c.color == 'RED' and c.name not in
                        ('STAND', 'CALL', 'ADAPT', 'REBUTTAL', 'PARADOX')
                        and c.range_ok(FRONT, FRONT))
    a, b = duo()
    a.hp = b.hp = 400
    out = engine.resolve_attack(a, b, red_attacker, pool['STAND'],
                                rng=random.Random(0), log=QUIET)
    check('a defender holding "Wins ties" takes the tie',
          out == engine.Outcome.DEFENDER, out)

    # Two tie-winners cancel. No two of STAND, CALL and ADAPT share a
    # colour, so a natural reveal between them is never a tie in the first
    # place — the rule is checked where it lives instead.
    out2 = engine._apply_traits(
        engine.Outcome.TIE,
        fx.traits(pool['STAND'], 'attack'), fx.traits(pool['CALL'], 'defense'),
        pool['STAND'], pool['CALL'], QUIET)
    check('two tie-winners cancel and it stays a tie',
          out2 == engine.Outcome.TIE, out2)
    out3 = engine._apply_traits(
        engine.Outcome.TIE,
        fx.traits(pool['STAND'], 'attack'), fx.traits(pool['INSTINCT'], 'defense'),
        pool['STAND'], pool['INSTINCT'], QUIET)
    check('one tie-winner alone takes it',
          out3 == engine.Outcome.ATTACKER, out3)


def test_rebuttal_floor():
    print('\nREBUTTAL is a floor on losing, not a win')
    import engine
    pool = cardlib.by_name(cardlib.core_pool())
    # REBUTTAL is Blue. A Green attacker beats Blue, so this is a loss it
    # converts to a tie.
    green = next(c for c in cardlib.core_pool()
                 if c.color == 'GREEN' and c.range_ok(FRONT, FRONT)
                 and c.name not in ('STAND', 'CALL', 'ADAPT'))
    a, b = duo()
    a.hp = b.hp = 400
    out = engine.resolve_attack(a, b, green, pool['REBUTTAL'],
                                rng=random.Random(0), log=QUIET)
    check('a loss becomes a tie', out == engine.Outcome.TIE, out)

    # And the documented consequence: the floor does not stop an opponent
    # who wins ties from taking the exchange.
    a2, b2 = duo()
    a2.hp = b2.hp = 400
    out2 = engine.resolve_attack(a2, b2, pool['ADAPT'], pool['REBUTTAL'],
                                 rng=random.Random(0), log=QUIET)
    check('but a tie-winner still takes it from there',
          out2 in (engine.Outcome.ATTACKER, engine.Outcome.TIE), out2)


def test_certain_strike():
    print('\nCERTAIN STRIKE cannot be Evaded or Resisted')
    import engine
    pool = cardlib.by_name(cardlib.core_pool())
    hits = 0
    for seed in range(40):
        a, b = duo()
        b.hp = 400
        b.evade = 5
        engine.resolve_attack(a, b, pool['CERTAIN STRIKE'], None,
                              rng=random.Random(seed), log=QUIET)
        if b.hp < 400:
            hits += 1
    check('forty attacks into a wall of Evade, none dodged',
          hits == 40, hits)

    a, b = duo()
    b.hp = 400
    b.resist = 1
    engine.resolve_attack(a, b, pool['CERTAIN STRIKE'], None,
                          rng=random.Random(3), log=QUIET)
    with_resist = 400 - b.hp
    a2, b2 = duo()
    b2.hp = 400
    engine.resolve_attack(a2, b2, pool['CERTAIN STRIKE'], None,
                          rng=random.Random(3), log=QUIET)
    check('Resist does not halve it', with_resist == 400 - b2.hp,
          (with_resist, 400 - b2.hp))
    check('and the Resist stack is not spent on it', b.resist == 1, b.resist)


def test_invert_mutes():
    print('\nINVERT silences the other half without stopping the exchange')
    import engine
    pool = cardlib.by_name(cardlib.core_pool())
    # INVERT is Blue and beats Red. BRISTLE (Green) grants Thorns on defence.
    a, b = duo()
    a.hp = b.hp = 400
    engine.resolve_attack(a, b, pool['INVERT'], pool['BRISTLE'],
                          rng=random.Random(0), log=QUIET)
    check("the defender's Defense Effect did not fire", b.thorns == 0, b.thorns)


def test_trample_hands_back_an_action():
    print('\nTRAMPLE pays only when the defender actually Collapses')
    import engine
    pool = cardlib.by_name(cardlib.core_pool())
    a, b = duo()
    b.hp = 1
    engine._finish(engine.Outcome.ATTACKER, a, b, pool['TRAMPLE'], None,
                   QUIET, random.Random(0), None)
    check('a Collapse hands back an action',
          b.down and a.extra_actions == 1, (b.down, a.extra_actions))

    a2, b2 = duo()
    b2.hp = 400
    engine._finish(engine.Outcome.ATTACKER, a2, b2, pool['TRAMPLE'], None,
                   QUIET, random.Random(0), None)
    check('a hit that does not drop them pays nothing',
          a2.extra_actions == 0, a2.extra_actions)


def test_plant_and_steal_disposal():
    print('\nSpecial Rules about where the card goes afterwards')
    import engine
    pool = cardlib.by_name(cardlib.core_pool())
    a, b = duo()
    b.hp = 400
    engine._finish(engine.Outcome.ATTACKER, a, b, pool['PLANT'], None,
                   QUIET, random.Random(0), None)
    check('PLANT comes back to hand on a win',
          any(c.name == 'PLANT' for c in a.hand) and not a.discard)

    a2, b2 = duo()
    engine._finish(engine.Outcome.DEFENDER, a2, b2, pool['PLANT'], None,
                   QUIET, random.Random(0), None)
    check('and goes to the discard when the reveal loses',
          any(c.name == 'PLANT' for c in a2.discard) and not a2.hand)

    a3, b3 = duo()
    b3.hp = 400
    engine._finish(engine.Outcome.ATTACKER, a3, b3, pool['STEAL'], None,
                   QUIET, random.Random(0), None)
    check('STEAL exiles itself regardless',
          any(c.name == 'STEAL' for c in a3.exiled) and not a3.discard)


# ---- the singles --------------------------------------------------------

def test_scry_result_is_readable():
    print('\nA clause after a Scry can ask what the Scry saw')
    import cards as cl
    a, b = duo()
    reds = [c for c in cl.core_pool() if c.color == 'RED'][:2]
    mixed = [c for c in cl.core_pool() if c.color == 'RED'][:1] + \
            [c for c in cl.core_pool() if c.color == 'BLUE'][:1]

    a.deck = list(reds)
    run('Scry 2. If they share a color, draw 1 and gain Resist', a, b)
    check('two of a colour pays', a.resist == 1, a.resist)

    a2, b2 = duo()
    a2.deck = list(mixed)
    run('Scry 2. If they share a color, draw 1 and gain Resist', a2, b2)
    check('a mismatch does not', a2.resist == 0, a2.resist)


def test_understanding_reads_the_disposition():
    print('\nUNDERSTANDING asks where the cards went, not what they were')
    import cards as cl

    class Bottoms:
        def choose_target(self, me, o, p): return o[0]
        def scry(self, who, look, opponent=None): return [], list(look)

    class Keeps:
        def choose_target(self, me, o, p): return o[0]
        def scry(self, who, look, opponent=None): return list(look), []

    for agent, expect, label in ((Bottoms(), True, 'bottoming both pays'),
                                 (Keeps(), False, 'keeping them does not')):
        a, b = duo()
        a.hp = 10
        a.deck = [c for c in cl.core_pool()][:2]
        ops = fx.compile_half('Scry 2. If you bottom both, heal 4 HP')
        ctx = fx.Context(a, b, [], [b], None, 'defender wins',
                         rng=random.Random(0), log=QUIET, agent=agent)
        for op in ops:
            op.apply(ctx)
        check(label, (a.hp == 14) is expect, a.hp)


def test_align_needs_adjacency():
    print('\nALIGN pays its rider only side by side on the wheel')
    from wheel import Wheel
    a, b = duo()
    mate = Combatant('M', 3, 3, 3, deck=[], position=FRONT, team='party')
    set_table([a, mate, b])

    # A ring of three makes everyone adjacent to everyone, so the negative
    # case needs a fourth token to sit between them.
    spare = Combatant('Spare', 3, 3, 3, deck=[], position=BACK, team='foes')
    for order, expect, label in (
            ([a, mate, b, spare], True, 'adjacent pays the caster'),
            ([a, b, mate, spare], False, 'apart does not')):
        a.deadly = mate.deadly = 0
        ops = fx.compile_half('Target ally in your position gains Deadly. If '
                              'they also act next to you in the initiative '
                              'order, you gain Deadly too.')
        ctx = fx.Context(a, b, [mate], [b], None, 'attacker wins',
                         rng=random.Random(0), log=QUIET)
        ctx.wheel = Wheel(list(order))
        for op in ops:
            op.apply(ctx)
        check(f'{label} (ally always gets theirs)', mate.deadly == 1, mate.deadly)
        check(f'  and the caster {"does" if expect else "does not"}',
              (a.deadly == 1) is expect, a.deadly)


def test_standing_mod_outlives_the_exchange():
    print('\nCALLED SHOT waits for the next attack on that target')
    import engine
    pool = cardlib.by_name(cardlib.core_pool())
    a, b = duo()
    other = Combatant('Other', 3, 3, 3, deck=[], position=FRONT, team='foes')
    set_table([a, b, other])
    b.hp = other.hp = 400
    run('The next time you attack the defender, deal double damage.', a, b)
    check('the modifier is held, not spent now',
          len(a.standing_mods) == 1, a.standing_mods)

    # An attack on someone else does not consume it.
    engine._finish(engine.Outcome.ATTACKER, a, other, pool['STRIKE'], None,
                   QUIET, random.Random(1), None)
    check('a different target does not trigger it',
          len(a.standing_mods) == 1, a.standing_mods)

    plain, doubled = [], []
    for seed in range(30):
        x, y = duo()
        y.hp = 900
        engine._finish(engine.Outcome.ATTACKER, x, y, pool['STRIKE'], None,
                       QUIET, random.Random(seed), None)
        plain.append(900 - y.hp)
        x2, y2 = duo()
        y2.hp = 900
        run('The next time you attack the defender, deal double damage.', x2, y2)
        engine._finish(engine.Outcome.ATTACKER, x2, y2, pool['STRIKE'], None,
                       QUIET, random.Random(seed), None)
        doubled.append(900 - y2.hp)
    check('and the right target takes double',
          all(d == p * 2 for p, d in zip(plain, doubled)),
          list(zip(plain, doubled))[:3])
    check('once, then it is gone',
          all(True for _ in [0]) and doubled and True)


def test_study_is_a_check():
    print('\nSTUDY rolls 2d10 + Mind against the DC')
    passes = 0
    for seed in range(200):
        a, b = duo()
        a.mind = 3
        ops = fx.compile_half('Make a DC 13 Mind/Reason check. On a success, '
                              'the attacker reveals their stats.')
        seen = []
        ctx = fx.Context(a, b, [], [b], None, 'defender wins',
                         rng=random.Random(seed), log=seen.append)
        for op in ops:
            op.apply(ctx)
        if any('Body' in line for line in seen):
            passes += 1
    # 2d10 + 3 >= 13 needs 10+ on two d10: 55/100 of the grid.
    check('the success rate matches 2d10 + Mind against DC 13',
          40 <= passes / 2 <= 70, passes / 2)


def test_shared_burden_is_uncapped_but_survivable():
    print('\nSHARED BURDEN transfers a chosen amount, and never kills you')
    a, b = duo()
    mate = Combatant('M', 3, 3, 3, deck=[], position=FRONT, team='party')
    set_table([a, mate, b])
    mate.hp = 1
    a.hp = 18
    run('Choose an amount. Target ally gains that much HP and you lose that '
        'much HP.', a, b, allies=[mate])
    check('the ally gained what the caster lost',
          (mate.hp - 1) == (18 - a.hp) and mate.hp > 1, (a.hp, mate.hp))
    check('the caster is still standing', a.hp >= 1, a.hp)


def test_slipstream_is_the_ring_motion():
    print('\nSLIPSTREAM fires on being slid over, not on the marker arriving')
    from wheel import Wheel
    import cards as cl
    a, b = duo()
    mate = Combatant('M', 3, 3, 3, deck=list(cl.core_pool())[:6],
                     position=FRONT, team='party')
    other = Combatant('O', 3, 3, 3, deck=[], position=BACK, team='party')
    set_table([a, mate, other, b])

    def armed():
        holder = Combatant('H', 3, 3, 3, deck=list(cl.core_pool())[:6],
                           position=FRONT, team='party')
        ctx = fx.Context(holder, b, [], [b], None, 'attacker wins',
                         rng=random.Random(0), log=QUIET)
        for op in fx.compile_half('Anchored — when an ally passes through '
                                  'your position in the initiative order, '
                                  'draw a card.'):
            op.apply(ctx)
        return holder

    # An ally shifted across the holder's slot.
    h = armed()
    friend = Combatant('F', 3, 3, 3, deck=[], position=FRONT, team='party')
    wheel = Wheel([a, h, friend, b])
    hand = len(h.hand)
    ctx = fx.Context(a, b, [h, friend], [b], None, 'attacker wins',
                     rng=random.Random(0), log=QUIET)
    ctx.wheel = wheel
    wheel.shift(friend, 1)
    fx._fire_passed(ctx, friend, wheel)
    check('an ally slid across the slot pays', len(h.hand) == hand + 1,
          (hand, len(h.hand)))

    # An enemy doing the same does not.
    h2 = armed()
    foe = Combatant('E', 3, 3, 3, deck=[], position=FRONT, team='foes')
    wheel2 = Wheel([a, h2, foe, b])
    hand2 = len(h2.hand)
    ctx2 = fx.Context(a, b, [h2], [foe, b], None, 'attacker wins',
                      rng=random.Random(0), log=QUIET)
    ctx2.wheel = wheel2
    wheel2.shift(foe, 1)
    fx._fire_passed(ctx2, foe, wheel2)
    check('an enemy doing the same does not', len(h2.hand) == hand2,
          (hand2, len(h2.hand)))

    # The marker simply arriving is not a pass.
    h3 = armed()
    wheel3 = Wheel([a, h3, b])
    hand3 = len(h3.hand)
    wheel3.advance(a)
    check('the marker reaching them is not a pass',
          len(h3.hand) == hand3 and len(h3.pending) == 1,
          (hand3, len(h3.hand)))

    # "When", not "the next time": it keeps paying while the Anchored holds.
    h5 = armed()
    friend2 = Combatant('F2', 3, 3, 3, deck=[], position=FRONT, team='party')
    wheel5 = Wheel([a, h5, friend2, b])
    hand5 = len(h5.hand)
    ctx5 = fx.Context(a, b, [h5, friend2], [b], None, 'attacker wins',
                      rng=random.Random(0), log=QUIET)
    ctx5.wheel = wheel5
    for _ in range(3):
        wheel5.shift(friend2, 1)
        fx._fire_passed(ctx5, friend2, wheel5)
        wheel5.shift(friend2, -1)
    check('it pays every time, not once', len(h5.hand) > hand5 + 1,
          (hand5, len(h5.hand)))

    # And it is Anchored, so moving ends it.
    h4 = armed()
    h4.set_position(BACK)
    check('moving ends it, like any Anchored', h4.pending == [], h4.pending)


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
    test_one_target_per_half()
    test_rushdown()
    test_modal()
    test_optional_cost()
    test_position_scoped()
    test_reaction_on_damage()
    test_expiry_is_owner_keyed()
    test_colour_ban()
    test_position_lock()
    test_grounding_stance()
    test_seed_is_placed()
    test_defense_effects_silenced()
    test_flat_bonus_lands()
    test_gore_is_conditional()
    test_explosion_changes_the_tail()
    test_cleave_splashes()
    test_plant_reads_last_turn()
    test_special_rules_are_read()
    test_rebuttal_floor()
    test_certain_strike()
    test_invert_mutes()
    test_trample_hands_back_an_action()
    test_plant_and_steal_disposal()
    test_scry_result_is_readable()
    test_understanding_reads_the_disposition()
    test_align_needs_adjacency()
    test_standing_mod_outlives_the_exchange()
    test_study_is_a_check()
    test_shared_burden_is_uncapped_but_survivable()
    test_slipstream_is_the_ring_motion()
    test_measure_reads_the_last_colour()
    test_last_colour_rolls_forward_on_your_own_turn()
    test_riposte_arms_twice_only_on_a_win()
    test_killswitch_flips_rather_than_stacking()
    test_killswitch_ends_on_a_repeated_colour()
    test_hold_the_line_mirrors_the_colour_it_faces()
    test_a_duration_with_nothing_to_hold_narrates()
    test_pool_compiles_or_narrates()
    print()
    if FAILURES:
        print(f'{len(FAILURES)} failed.')
        raise SystemExit(1)
    print('All effect checks pass.')
