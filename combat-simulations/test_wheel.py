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


def negative_self_shift_never_arrives_sooner():
    """The mirror case. A negative shift is later, and a combatant who has
    just acted is already last, so it must not hand them an earlier turn."""
    base = Wheel(['a', 'b', 'c', 'd'])
    cur, seq = 'a', []
    for _ in range(4):
        nxt = base.advance(cur)
        while nxt is None:
            nxt = base.advance(base.order()[0])
        seq.append(nxt)
        cur = nxt
    normal = seq.index('a')

    for amount in (-1, -2, -3):
        w = Wheel(['a', 'b', 'c', 'd'])
        w.shift('a', amount, acting='a')
        cur, got = 'a', []
        for _ in range(4):
            nxt = w.advance(cur)
            while nxt is None:
                nxt = w.advance(w.order()[0])
            got.append(nxt)
            cur = nxt
        assert got.index('a') >= normal, (amount, got)


def a_bystander_still_earns_the_bonus():
    """Only the acting token's own shift changes. Example 3b stands."""
    w = Wheel(['a', 'b', 'c', 'd'])
    w.shift('d', +4, acting='a')
    assert w.pending_bonus == ['d'], w.pending_bonus


def a_defender_shifting_the_attacker_places_no_chip():
    """RETALIATE, INTERRUPT, DELAY, DOUBLE DOWN, HASTEN and STEAL all shift
    the attacker from a defence half — and the attacker is the one acting,
    standing on the marker's slot. Moving them off it must not place a
    bonus or a skip chip on anyone.

    The wheel is told who is acting, not who cast the shift, so this is the
    same guard as a self-shift. What it does *not* do is make the attacker
    later: they have just acted and are already last. See the note on
    _shift_self_while_acting.
    """
    for amount in (-1, -2, -3):
        w = Wheel(['att', 'def', 'c', 'd'])
        w.shift('att', amount, acting='att')
        assert not w.chips, (amount, w.chips)
        assert not w.pending_bonus, (amount, w.pending_bonus)

        cur, seq = 'att', []
        for _ in range(4):
            nxt = w.advance(cur)
            while nxt is None:
                nxt = w.advance(w.order()[0])
            seq.append(nxt)
            cur = nxt
        assert sorted(seq) == ['att', 'c', 'd', 'def'], ('a turn was lost', seq)
        assert seq.index('att') == 3, ('the attacker came sooner', amount, seq)


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
        case('a negative shift on yourself never arrives sooner',
             negative_self_shift_never_arrives_sooner),
        case('a bystander crossing the marker still earns one',
             a_bystander_still_earns_the_bonus),
        case('a defender shifting the attacker places no chip',
             a_defender_shifting_the_attacker_places_no_chip),
        case('shifting someone who is not acting still works',
             shifting_someone_who_is_not_acting_still_works),
    ]
    print(f'\n{sum(results)}/{len(results)} passed')
    raise SystemExit(0 if all(results) else 1)
