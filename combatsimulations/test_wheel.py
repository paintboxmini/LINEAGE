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
    """`a, b, c, d.` a plays Initiative Shift +3 on d.
    Result: d, a, b, c — bonus chip on d, skip chip on a."""
    w = Wheel(['a', 'b', 'c', 'd'])
    w.shift('d', +3)
    assert w.order() == ['d', 'a', 'b', 'c'], w.order()
    assert w.chips == {'d': BONUS, 'a': SKIP}, w.chips
    assert w.take_bonus() == 'd'           # immediate extra turn
    assert w.take_bonus() is None


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

    What this example is demonstrating is the chip rule — "a fresh shift on
    a chip-holding token cancels whatever was pending, rather than stacking
    or compounding it" — so that is what is asserted here: d's pending SKIP
    does not survive, and does not carry its unresolved math forward.

    The example also narrates the outcome as "no bonus, no skip." That part
    is NOT asserted, because it conflicts with Example 3: d sits one slot
    off the marker, so a +1 lands it exactly on the marker's own slot, which
    Example 3 defines as the bonus-turn case. Both cannot hold. See
    README.md, Known discrepancies.
    """
    w = Wheel(['a', 'b', 'c', 'd'])
    w.shift('d', -2)
    assert w.chips == {'d': SKIP}
    assert w.advance('a') == 'b'           # b is acting now
    w.shift('d', +1)
    assert w.chips.get('d') != SKIP, w.chips
    assert 'd' in w.order()


def three_on_the_wheel():
    """"With exactly 3 combatants, reduce X's magnitude by 1 (toward zero)
    before applying. A shift of +/-1 becomes no shift at all.\""""
    w = Wheel(['a', 'b', 'c'])
    w.shift('c', +1)
    assert w.order() == ['a', 'b', 'c'], w.order()
    w2 = Wheel(['a', 'b', 'c'])
    w2.shift('c', -1)
    assert w2.order() == ['a', 'b', 'c'], w2.order()
    w3 = Wheel(['a', 'b', 'c'])
    w3.shift('c', +2)          # becomes +1
    assert w3.order() == ['a', 'c', 'b'], w3.order()


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
        case('Example 4 — negative shift onto the marker\'s slot', ex4),
        case('Example 5 — reshifting a chip-holding token', ex5),
        case('3 on the wheel — magnitude reduced by 1', three_on_the_wheel),
        case('joining and leaving', join_and_leave),
    ]
    print(f'\n{sum(results)}/{len(results)} passed')
    raise SystemExit(0 if all(results) else 1)
