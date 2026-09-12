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
    print(f'\n{sum(results)}/{len(results)} passed')
    raise SystemExit(0 if all(results) else 1)
