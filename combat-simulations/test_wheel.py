"""The worked cases from `rules/initiative-shift-examples.md`, as assertions.

That file is the spec for this module. If a rule there changes, this fails,
which is the point — it is the one part of the engine with a written oracle.

Run: python3 test_wheel.py
"""

from wheel import Wheel, SKIP, BONUS


def case(name, fn):
    try:
        fn()
    except AssertionError as e:
        print(f'  FAIL  {name}\n        {e}')
        return False
    print(f'  ok    {name}')
    return True


def ex1():
    """`a, b, c, d.` a acting, plays Initiative Shift +1 on c.
    Result: a, c, b, d. No chip."""
    w = Wheel(['a', 'b', 'c', 'd'])
    w.shift('c', +1)
    assert w.order() == ['a', 'c', 'b', 'd'], w.order()
    assert w.chips == {}, w.chips
    # "a's turn ends; c goes next, then b, then d."
    assert w.advance('a') == 'c'


def ex2():
    """`a, b, c, d.` a plays Initiative Shift -2 on d.
    Result: b, d, c, a, with a skip chip on d."""
    w = Wheel(['a', 'b', 'c', 'd'])
    w.shift('d', -2)
    assert w.order() == ['b', 'd', 'c', 'a'], w.order()
    assert w.chips == {'d': SKIP}, w.chips
    # a's turn ends -> b -> d skipped -> c -> a again.
    assert w.advance('a') == 'b'
    assert w.advance('b') is None          # d, skipped
    assert w.chips == {}
    assert w.advance('d') == 'c'
    assert w.advance('c') == 'a'


def ex3():
    """`a, b, c, d.` a plays Initiative Shift +3 on d. d sits 3 from the
    marker and the shift is 3, so it lands exactly on the marker's slot —
    onto is not across. Result: d, a, b, c, no chips on anyone."""
    w = Wheel(['a', 'b', 'c', 'd'])
    w.shift('d', +3)
    assert w.order() == ['d', 'a', 'b', 'c'], w.order()
    assert w.chips == {}, w.chips
    assert w.take_bonus() is None
    # The marker belongs to a slot and hasn't finished with its own, so the
    # token that slid into it takes the next turn. Nobody is skipped.
    # a's turn ends -> d -> a -> b -> c.
    assert w.advance('a') == 'd'
    assert w.advance('d') == 'a'
    assert w.advance('a') == 'b'
    assert w.advance('b') == 'c'


def ex3b():
    """`a, b, c, d.` a plays Initiative Shift +2 on b. b sits 1 from the
    marker and the shift is 2 — further to travel than the distance, so it
    crosses. Result: b, a, c, d — bonus on b, skip on a."""
    w = Wheel(['a', 'b', 'c', 'd'])
    w.shift('b', +2)
    assert w.order() == ['b', 'a', 'c', 'd'], w.order()
    assert w.chips == {'b': BONUS, 'a': SKIP}, w.chips
    assert w.take_bonus() == 'b'           # immediate extra turn
    assert w.take_bonus() is None
    # a's turn ends -> b goes next (bonus) -> a skipped -> c -> d.
    assert w.advance('b') is None          # a, skipped in compensation
    assert w.chips == {}
    assert w.advance('a') == 'c'
    assert w.advance('c') == 'd'


def ex4():
    """`a, b, c, d.` a plays Initiative Shift -2 on c.
    Result: c, b, d, a — skip chip on c, and no chip on a."""
    w = Wheel(['a', 'b', 'c', 'd'])
    w.shift('c', -2)
    assert w.order() == ['c', 'b', 'd', 'a'], w.order()
    assert w.chips == {'c': SKIP}, w.chips
    # a's turn ends -> c skipped -> b -> d -> a normally.
    assert w.advance('a') is None          # c, skipped
    assert w.advance('c') == 'b'
    assert w.advance('b') == 'd'
    assert w.advance('d') == 'a'


def ex5():
    """Continuing from Example 2 (b, d, c, a; d holds a skip chip): during
    b's turn, b plays Initiative Shift +1 on d.

    The pending chip is cancelled, and the fresh shift resolves under
    whatever case it actually lands in — which here is Example 3's, since d
    sits one slot off the marker and the shift is 1. Onto is not across:
    result d, b, c, a with no chips.
    """
    w = Wheel(['a', 'b', 'c', 'd'])
    w.shift('d', -2)
    assert w.chips == {'d': SKIP}
    assert w.advance('a') == 'b'           # b is acting now
    w.shift('d', +1)
    assert w.order() == ['d', 'b', 'c', 'a'], w.order()
    assert w.chips == {}, w.chips
    # b's turn ends -> d (slid into the marker's slot) -> b -> c -> a.
    assert w.advance('b') == 'd'
    assert w.advance('d') == 'b'
    assert w.advance('b') == 'c'
    assert w.advance('c') == 'a'


def no_table_size_correction():
    """The old "with exactly 3 combatants, reduce X by 1" rule is retired.
    Three on the wheel behaves exactly like four, scaled down."""
    w = Wheel(['a', 'b', 'c'])
    w.shift('c', +1)                       # slot 2 -> slot 1, an ordinary move
    assert w.order() == ['a', 'c', 'b'], w.order()
    assert w.chips == {}, w.chips

    w2 = Wheel(['a', 'b', 'c'])
    w2.shift('c', +2)                      # lands exactly on the marker: onto
    assert w2.order() == ['c', 'a', 'b'], w2.order()
    assert w2.chips == {}, w2.chips

    w3 = Wheel(['a', 'b', 'c'])
    w3.shift('b', +2)                      # 1 from the marker, shift 2: across
    assert w3.chips == {'b': BONUS, 'a': SKIP}, w3.chips


def join_and_leave():
    """The wheel always has exactly as many slots as combatants."""
    w = Wheel(['a', 'b', 'c'])
    w.add_after('s', 'a')
    assert w.order() == ['a', 's', 'b', 'c'], w.order()
    w.remove('b')
    assert w.order() == ['a', 's', 'c'], w.order()


# ---- reordering that is not a shift -------------------------------------
#
# PRIORITY and STARING CONTEST move a token without sliding the ring the way
# Initiative Shift does. No worked cases exist for these — they are checked
# against the general principles the glossary states rather than against a
# written example, and that difference is worth knowing when reading a
# failure here.

def swap_moves_only_two():
    """PRIORITY: two tokens exchange slots and nobody else is touched.
    A shift of the same distance would drag everyone between them along."""
    w = Wheel(list('ABCDE'))
    w.swap('A', 'D')
    assert w.order() == list('DBCAE'), w.order()
    w2 = Wheel(list('ABCDE'))
    w2.shift('D', 3)
    assert w2.order() != list('DBCAE'), 'a shift should slide, not swap'
    w3 = Wheel(list('ABCDE'))
    w3.swap('B', 'C')
    assert w3.order() == list('ACBDE'), w3.order()


def swap_gives_no_second_turn():
    """"The combatant already acting when this happens is not shorted a
    turn, but doesn't get a second one either." A swap off the marker's slot
    by whoever is acting leaves them a skip at their new slot."""
    w = Wheel(list('ABCD'))
    w.swap('A', 'C', acting='A')
    assert w.order() == list('CBAD'), w.order()
    assert w.chips == {'A': SKIP}, w.chips

    seen, cur = [], 'A'
    for _ in range(6):
        nxt = w.advance(cur)
        while nxt is None:
            nxt = w.advance(w.order()[0])
        seen.append(nxt)
        cur = nxt
    assert seen.count('A') <= 1, seen


def move_after_closes_the_gap():
    """STARING CONTEST: a move rather than an exchange. The token comes out,
    goes back in behind the target, and everyone between closes up."""
    w = Wheel(list('ABCD'))
    w.move_after('A', 'C')
    assert w.order() == list('BCAD'), w.order()
    w2 = Wheel(list('ABCD'))
    w2.move_after('D', 'A')
    assert w2.order() == list('ADBC'), w2.order()
    w3 = Wheel(list('ABCD'))
    w3.move_after('B', 'C')
    assert w3.order() == list('ACBD'), w3.order()
    w4 = Wheel(list('ABCD'))
    w4.move_after('B', 'B')
    assert w4.order() == list('ABCD'), w4.order()


def reorders_place_no_chips():
    """Neither card is an Initiative Shift, and the bonus-turn rule is
    written about shifts. Crossing the marker by swapping earns nothing."""
    w = Wheel(list('ABCDE'))
    w.swap('E', 'B')
    assert not w.chips and not w.pending_bonus, (w.chips, w.pending_bonus)
    w2 = Wheel(list('ABCDE'))
    w2.move_after('E', 'A')
    assert not w2.chips and not w2.pending_bonus, (w2.chips, w2.pending_bonus)
    # +4 from slot 4 lands *onto* the marker's slot, which Example 3 says is
    # not across it. +5 is the crossing that earns the bonus turn.
    w3 = Wheel(list('ABCDE'))
    w3.shift('E', 4)
    assert not w3.pending_bonus, 'onto the marker is not across it'
    w4 = Wheel(list('ABCDE'))
    w4.shift('E', 5)
    assert w4.pending_bonus == ['E'], w4.pending_bonus


def ring_stays_intact():
    """Three hundred random reorders; the ring keeps everyone, once each."""
    import random as _r
    rng = _r.Random(0)
    for _ in range(300):
        n = rng.randint(2, 6)
        toks = list('ABCDEF')[:n]
        w = Wheel(list(toks))
        for _ in range(rng.randint(1, 6)):
            x, y = rng.sample(toks, 2)
            if rng.random() < 0.5:
                w.swap(x, y, acting=rng.choice([None, x]))
            else:
                w.move_after(x, y, acting=rng.choice([None, x]))
            assert sorted(w.order()) == sorted(toks), (toks, w.order())


def self_shift_while_acting_is_not_a_bonus_turn():
    """A combatant shifting itself on its own turn stands on the marker's
    slot, so the distance to the marker is zero and the general rule would
    make every such shift a crossing — a free extra turn off QUICKEN, every
    time. Measured where the glossary says to measure it instead: against
    when the token's own next turn would have arrived, which having acted
    is after everyone else."""
    def when_next(amount):
        w = Wheel(['a', 'b', 'c', 'd'])
        w.shift('a', amount, acting='a')
        assert not w.chips and not w.pending_bonus, (w.chips, w.pending_bonus)
        cur, seq = 'a', []
        for _ in range(4):
            nxt = w.advance(cur)
            while nxt is None:
                nxt = w.advance(w.order()[0])
            seq.append(nxt)
            cur = nxt
        assert seq.count('a') == 1, ('acted twice', seq)
        assert sorted(seq) == ['a', 'b', 'c', 'd'], ('someone lost a turn', seq)
        return seq.index('a')

    assert when_next(1) == 2, when_next(1)     # after 3 others normally
    assert when_next(2) == 1, when_next(2)
    assert when_next(3) == 1, when_next(3)     # floored at acting next
    assert when_next(9) == 1, when_next(9)


def when_next(w, token, depth=40):
    """How many other turns pass before `token` acts again."""
    cur, seq = token, []
    for _ in range(depth):
        nxt = w.advance(cur)
        while nxt is None:
            nxt = w.advance(w.order()[0])
        seq.append(nxt)
        cur = nxt
    return seq.index(token) if token in seq else None


def a_negative_shift_puts_one_more_person_in_front_per_point():
    """The whole rule in one line: -X means X more turns happen before
    yours. A combatant on the marker's slot has just acted, so their next
    turn is n away, not 0 — read the slot as their place in the queue and
    every shift comes out backwards.

    Drew's numbers, table of four, baseline after three others:
        -1 after 4, -2 after 5, -3 after 6.
    """
    assert when_next(Wheel(['a', 'b', 'c', 'd']), 'a') == 3

    for amount, expect in ((-1, 4), (-2, 5), (-3, 6)):
        w = Wheel(['a', 'b', 'c', 'd'])
        w.shift('a', amount, acting='a')
        assert not w.pending_bonus, (amount, w.pending_bonus)
        assert list(w.chips) == ['a'], (amount, w.chips)
        got = when_next(w, 'a', depth=40)
        assert got == expect, (amount, got, expect)


def the_delay_scales_with_the_table():
    """Not tuned to four. One more person per point, whatever the table."""
    for n in (3, 4, 5, 6):
        toks = list('abcdef')[:n]
        base = when_next(Wheel(list(toks)), 'a', depth=60)
        assert base == n - 1, (n, base)
        for amount in (-1, -2, -3):
            w = Wheel(list(toks))
            w.shift('a', amount, acting='a')
            got = when_next(w, 'a', depth=60)
            assert got == n - 1 - amount, (n, amount, got)


def every_delay_is_reachable_at_every_table():
    """There is no delay the ring cannot express. A -3 at a table of three
    is the awkward one — Drew's case — and it works: skipped the first time
    the marker reaches them, acting again after five others.

    An earlier version of this file asserted that case was unreachable and
    landed one short. It was not unreachable; it needed two laps and a slot
    rather than one lap, and nobody had looked."""
    w = Wheel(['a', 'b', 'c'])
    w.shift('a', -3, acting='a')
    assert when_next(w, 'a', depth=60) == 5, when_next(w, 'a', depth=60)

    for n in range(3, 8):
        toks = list('abcdefg')[:n]
        for amount in range(-1, -8, -1):
            w = Wheel(list(toks))
            w.shift('a', amount, acting='a')
            got = when_next(w, 'a', depth=120)
            assert got == (n - 1) - amount, (n, amount, got)


def a_bystander_still_earns_the_bonus():
    """Only the acting token's own shift changes. Example 3b stands."""
    w = Wheel(['a', 'b', 'c', 'd'])
    w.shift('d', +4, acting='a')
    assert w.pending_bonus == ['d'], w.pending_bonus


def a_defender_shifting_the_attacker_costs_only_the_attacker():
    """RETALIATE, INTERRUPT, DELAY, DOUBLE DOWN, HASTEN and STEAL all shift
    the attacker from a defence half, and the attacker is the one acting.

    Two different things are both true here and it is worth keeping them
    apart. Nobody earns a bonus turn and no *third party* is skipped in
    compensation — that machinery belongs to a shift crossing the marker,
    and standing on it is not crossing it. But the attacker's own delay is
    spent as skipped laps, which is the whole point of a defensive shift.
    """
    for amount in (-1, -2, -3):
        w = Wheel(['att', 'def', 'c', 'd'])
        w.shift('att', amount, acting='att')
        assert not w.pending_bonus, (amount, w.pending_bonus)
        assert list(w.chips) == ['att'], (amount, w.chips)
        # Everyone else keeps their turn; only the attacker is delayed.
        assert when_next(w, 'att', depth=40) == 3 - amount, (amount,)
        for other in ('def', 'c', 'd'):
            assert when_next(w, other, depth=40) is not None, other


def the_chip_clears_and_the_turn_arrives():
    """A delayed turn is late, not lost. The chip is spent when the marker
    first reaches them and the combatant acts normally from then on."""
    w = Wheel(['a', 'b', 'c', 'd'])
    w.shift('a', -2, acting='a')
    cur, seq = 'a', []
    for _ in range(20):
        nxt = w.advance(cur)
        while nxt is None:
            nxt = w.advance(w.order()[0])
        seq.append(nxt)
        cur = nxt
    assert seq.count('a') >= 2, ('the turn never came back', seq)
    assert 'a' not in w.chips, ('the chip outlived its delay', w.chips)


def shifting_someone_who_is_not_acting_still_works():
    """The attack-half versions — DELAY, DISTRACT, MOCKERY, TURN — aim at
    someone who is not on the marker, and are untouched by any of this."""
    w = Wheel(['att', 'def', 'c', 'd'])
    w.shift('def', -2, acting='att')
    assert w.order() != ['att', 'def', 'c', 'd'], w.order()


if __name__ == '__main__':
    print('rules/initiative-shift-examples.md:')
    results = [
        case('Example 1 — an ordinary shift', ex1),
        case('Example 2 — a negative shift that overshoots', ex2),
        case('Example 3 — positive shift onto the marker\'s slot', ex3),
        case('Example 3b — positive shift across the marker', ex3b),
        case('Example 4 — negative shift onto the marker\'s slot', ex4),
        case('Example 5 — reshifting a chip-holding token', ex5),
        case('no table-size correction', no_table_size_correction),
        case('joining and leaving', join_and_leave),
    ]
    print('\nreordering that is not a shift (no written oracle):')
    results += [
        case('PRIORITY moves only two tokens', swap_moves_only_two),
        case('a swap off the marker grants no second turn',
             swap_gives_no_second_turn),
        case('STARING CONTEST closes the gap behind it',
             move_after_closes_the_gap),
        case('neither reorder places a chip', reorders_place_no_chips),
        case('the ring keeps everyone, once each', ring_stays_intact),
        case('shifting yourself on your own turn is not a bonus turn',
             self_shift_while_acting_is_not_a_bonus_turn),
        case('a negative shift puts one more person in front per point',
             a_negative_shift_puts_one_more_person_in_front_per_point),
        case('the delay scales with the table', the_delay_scales_with_the_table),
        case('every delay is reachable at every table',
             every_delay_is_reachable_at_every_table),
        case('a bystander crossing the marker still earns one',
             a_bystander_still_earns_the_bonus),
        case('a defender shifting the attacker costs only the attacker',
             a_defender_shifting_the_attacker_costs_only_the_attacker),
        case('the chip clears and the turn arrives',
             the_chip_clears_and_the_turn_arrives),
        case('shifting someone who is not acting still works',
             shifting_someone_who_is_not_acting_still_works),
    ]
    print(f'\n{sum(results)}/{len(results)} passed')
    raise SystemExit(0 if all(results) else 1)
