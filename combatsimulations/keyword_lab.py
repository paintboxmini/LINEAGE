"""
Keyword Lab — isolate one keyword against another and measure which actually
wins more, controlling for everything else that could confound the answer.

Built from Drew's own framing (2026-07-24): "if we were comparing deadly
versus evade we could make the both decks have the both range on every card
since that's not what's being checked." The method: two decks, identical in
every respect (stats, filler cards, die sizes, Range: Both on every card so
range legality is never a confound) except ONE card, which grants keyword A
in one deck and keyword B in the other. Run them against each other. Whatever
separates the win rate from 50/50 is the keyword's own relative power, not
deckbuilding noise.

Only supports keywords that are a single stackable counter or a single
boolean flag on Combatant (deadly, weak, resist, vulnerable, evade, thorns,
blind, ward, immune, rooted, staggered, quick) — see KEYWORD_GRANTS below.
Anchored, Expose[Color], Initiative Shift X, Locked, and Sealed aren't single
flags and need a bespoke grant function if they're ever worth testing this
way; add one next to KEYWORD_GRANTS rather than forcing them into this shape.

Usage:
    python3 keyword_lab.py deadly evade
    python3 keyword_lab.py resist thorns 3          # thorns X=3, default 1
    python3 keyword_lab.py evade ward --n 20000

Gated grants (2026-07-29): --condition-a/--condition-b make a keyword only
apply when a real card-gate condition is true (see CONDITIONS below), instead
of every play. The tool then reports how often the condition actually fired —
a measured P(X), not a guessed one — alongside the win rate, so a gated
keyword's real expected value (win-rate delta already includes the gate) can
be read straight off the output instead of hand-computing value(Y) x P(X).
    python3 keyword_lab.py deadly evade --condition-a foe_moved   # RHYTHM BREAK's gate
    python3 keyword_lab.py deadly ward --condition-a backline     # NIP's gate
"""

import argparse
from collections import Counter

import content
from engine import Card, Combatant, Duel
from policies import TacticianPolicy

# keyword -> (attr name on Combatant, is a bool flag rather than a stack,
# is it a Debuff per card-glossary.md — i.e. does a real card apply it to the
# FOE, not the caster). Getting this backwards silently tests "how much does
# self-inflicted Weak hurt you" instead of "how strong is Weak as a debuff" —
# caught by hand once (2026-07-23): the four lowest-ranked keywords in the
# first round-robin pass were exactly Blind/Vulnerable/Weak/Staggered, all
# self-targeted by mistake. Rooted is a Debuff too (card-glossary.md, Debuff)
# even though granting it to yourself isn't obviously harmful in a vacuum —
# targeted at foe here for consistency with its actual glossary category and
# how real cards use it (an enemy applies it to you), not by vibes.
KEYWORD_GRANTS = {
    "deadly": ("deadly", False, "self"),
    "weak": ("weak", False, "foe"),
    "resist": ("resist", False, "self"),
    "vulnerable": ("vulnerable", False, "foe"),
    "evade": ("evade", False, "self"),
    "thorns": ("thorns", False, "self"),
    "blind": ("blind", False, "foe"),
    "ward": ("ward", True, "self"),
    "immune": ("immune", True, "self"),
    "rooted": ("rooted", True, "foe"),
    "staggered": ("staggered", True, "foe"),
    "quick": ("_quick", True, "self"),
}

# Conditional-grant predicates (2026-07-29) — mirror real card gates so a
# measured P(X) means something ("how often does THIS gate actually fire for
# a real policy") instead of testing a synthetic condition no card uses.
# Each predicate takes (engine, me, foe) and returns bool. NIP -> backline,
# GORE -> foe_frontline/foe_backline, RHYTHM BREAK -> foe_moved. Add more as
# specific cards need testing; don't invent conditions no card actually has.
CONDITIONS = {
    "backline": lambda engine, me, foe: me.position == 'backline',
    "frontline": lambda engine, me, foe: me.position == 'frontline',
    "foe_backline": lambda engine, me, foe: foe.position == 'backline',
    "foe_frontline": lambda engine, me, foe: foe.position == 'frontline',
    "foe_moved": lambda engine, me, foe: foe._repositioned_since_last_turn,
}

# Every predicate above is position-based, and the FILLER cards never move
# anyone — a pure filler+grant deck sits frontline the whole duel, so any
# position condition would silently and permanently measure 0%, not because
# the tool is broken but because there's nothing in the deck that ever
# triggers it. Real cards that gate on position pair with a real mover in
# the same deck (NIP needs BOLT/QUICKSTEP nearby to ever pay off) — so when a
# position condition is requested, build_test_cards adds a MOVER filler
# (toggles own position, identical in both decks, so it's not a confound)
# to give the condition an honest chance to fire.
_MOVER_CONDITIONS = {"backline", "frontline", "foe_backline", "foe_frontline", "foe_moved"}


def _mover_fn(engine, me, foe):
    me.position = 'backline' if me.position == 'frontline' else 'frontline'


def _make_grant_fn(attr, is_bool, amount, target, condition=None, counter=None):
    """counter, if given, is a mutable dict with 'hit'/'total' keys — every
    call records whether the condition was true, so the real trigger rate is
    measured across the run, not assumed. Unconditional grants (condition is
    None) don't touch the counter at all — nothing to measure."""
    def apply(t):
        if is_bool:
            setattr(t, attr, True)
        else:
            setattr(t, attr, getattr(t, attr) + amount)

    if condition is None:
        def fn(engine, me, foe):
            apply(target(me, foe))
    else:
        def fn(engine, me, foe):
            ok = condition(engine, me, foe)
            counter['total'] += 1
            if ok:
                counter['hit'] += 1
                apply(target(me, foe))
    return fn


_TARGET = {"self": lambda me, foe: me, "foe": lambda me, foe: foe}


def build_test_cards(cards, keyword_a, amount_a, keyword_b, amount_b,
                      condition_a=None, condition_b=None):
    """Registers FILLER_R/B/G (neutral, no Effect, Range: Both, d6) and one
    GRANT_<KEYWORD> card per side, sharing the same die/range/color/stat so
    the only variable between the two decks is which keyword each grants.
    condition_a/condition_b are names from CONDITIONS (or None for an
    unconditional grant, the original behavior). Returns
    (deck_a, deck_b, counter_a, counter_b) — the counters are empty dicts
    when the matching condition is None (nothing to measure)."""
    def add(name, color, stat, effect=None, defense=None):
        cards[name] = Card(name=name, color=color, stat=stat, reach="both",
                            base_die=6, effect=effect, defense=defense, damage=None)

    add("FILLER_R", "R", "body")
    add("FILLER_B", "B", "mind")

    needs_mover = (condition_a in _MOVER_CONDITIONS) or (condition_b in _MOVER_CONDITIONS)
    if needs_mover:
        add("FILLER_G", "G", "soul")
        add("MOVER", "G", "soul", effect=_mover_fn, defense=_mover_fn)
        filler = ["FILLER_R"] * 3 + ["FILLER_B"] * 3 + ["FILLER_G", "MOVER"]  # 8 cards
    else:
        add("FILLER_G", "G", "soul")
        filler = ["FILLER_R"] * 3 + ["FILLER_B"] * 3 + ["FILLER_G"] * 2       # 8 cards

    counter_a = {"hit": 0, "total": 0}
    counter_b = {"hit": 0, "total": 0}
    for label, kw, amount, cond_name, counter in (
        ("A", keyword_a, amount_a, condition_a, counter_a),
        ("B", keyword_b, amount_b, condition_b, counter_b),
    ):
        attr, is_bool, target = KEYWORD_GRANTS[kw]
        condition = CONDITIONS[cond_name] if cond_name else None
        fn = _make_grant_fn(attr, is_bool, amount, _TARGET[target], condition, counter)
        add(f"GRANT_{label}", "R", "body", effect=fn, defense=fn)

    deck_a = filler + ["GRANT_A"]
    deck_b = filler + ["GRANT_B"]
    return deck_a, deck_b, counter_a, counter_b


def run(n, deck_a, deck_b, cards, label, counter_a=None, counter_b=None):
    wins = Counter()
    total_turns = 0
    for i in range(n):
        a = Combatant("A", body=3, mind=3, soul=3, decklist=deck_a, policy=TacticianPolicy())
        b = Combatant("B", body=3, mind=3, soul=3, decklist=deck_b, policy=TacticianPolicy())
        d = Duel(a, b, cards, seed=i)
        wins[d.run()] += 1
        total_turns += d.turn_count
    print(f"{label}: A {wins['A']:6} ({100*wins['A']/n:5.1f}%)  "
          f"B {wins['B']:6} ({100*wins['B']/n:5.1f}%)  "
          f"TIE {wins.get('TIE', 0):6} ({100*wins.get('TIE', 0)/n:5.1f}%)  "
          f"avg turns {total_turns/n:.1f}")
    for tag, counter in (("A", counter_a), ("B", counter_b)):
        if counter and counter["total"]:
            pct = 100 * counter["hit"] / counter["total"]
            print(f"    condition {tag}: true on {counter['hit']}/{counter['total']} plays ({pct:.1f}%)")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("keyword_a", choices=sorted(KEYWORD_GRANTS))
    p.add_argument("keyword_b", choices=sorted(KEYWORD_GRANTS))
    p.add_argument("amount", nargs="?", type=int, default=1,
                    help="stack count / value for both keywords if they take one (default 1)")
    p.add_argument("--n", type=int, default=20000)
    p.add_argument("--condition-a", choices=sorted(CONDITIONS), default=None,
                    help="only grant keyword_a when this real card-gate condition is true (default: unconditional)")
    p.add_argument("--condition-b", choices=sorted(CONDITIONS), default=None,
                    help="only grant keyword_b when this real card-gate condition is true (default: unconditional)")
    args = p.parse_args()

    cards = content.build_cards()
    deck_a, deck_b, counter_a, counter_b = build_test_cards(
        cards, args.keyword_a, args.amount, args.keyword_b, args.amount,
        args.condition_a, args.condition_b)

    run(args.n, deck_a, deck_b, cards, f"A={args.keyword_a} vs B={args.keyword_b}", counter_a, counter_b)
    # swap sides to rule out any going-first asymmetry
    cards2 = content.build_cards()
    deck_b2, deck_a2, counter_b2, counter_a2 = build_test_cards(
        cards2, args.keyword_b, args.amount, args.keyword_a, args.amount,
        args.condition_b, args.condition_a)
    run(args.n, deck_b2, deck_a2, cards2, f"A={args.keyword_b} vs B={args.keyword_a} (sides swapped)", counter_b2, counter_a2)


if __name__ == "__main__":
    main()
