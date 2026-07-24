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


def _make_grant_fn(attr, is_bool, amount, target):
    if is_bool:
        def fn(engine, me, foe):
            setattr(target(me, foe), attr, True)
    else:
        def fn(engine, me, foe):
            t = target(me, foe)
            setattr(t, attr, getattr(t, attr) + amount)
    return fn


_TARGET = {"self": lambda me, foe: me, "foe": lambda me, foe: foe}


def build_test_cards(cards, keyword_a, amount_a, keyword_b, amount_b):
    """Registers FILLER_R/B/G (neutral, no Effect, Range: Both, d6) and one
    GRANT_<KEYWORD> card per side, sharing the same die/range/color/stat so
    the only variable between the two decks is which keyword each grants."""
    def add(name, color, stat, effect=None, defense=None):
        cards[name] = Card(name=name, color=color, stat=stat, reach="both",
                            base_die=6, effect=effect, defense=defense, damage=None)

    add("FILLER_R", "R", "body")
    add("FILLER_B", "B", "mind")
    add("FILLER_G", "G", "soul")

    for label, kw, amount in (("A", keyword_a, amount_a), ("B", keyword_b, amount_b)):
        attr, is_bool, target = KEYWORD_GRANTS[kw]
        fn = _make_grant_fn(attr, is_bool, amount, _TARGET[target])
        add(f"GRANT_{label}", "R", "body", effect=fn, defense=fn)

    filler = ["FILLER_R"] * 3 + ["FILLER_B"] * 3 + ["FILLER_G"] * 2   # 8 cards
    deck_a = filler + ["GRANT_A"]
    deck_b = filler + ["GRANT_B"]
    return deck_a, deck_b


def run(n, deck_a, deck_b, cards, label):
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


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("keyword_a", choices=sorted(KEYWORD_GRANTS))
    p.add_argument("keyword_b", choices=sorted(KEYWORD_GRANTS))
    p.add_argument("amount", nargs="?", type=int, default=1,
                    help="stack count / value for both keywords if they take one (default 1)")
    p.add_argument("--n", type=int, default=20000)
    args = p.parse_args()

    cards = content.build_cards()
    deck_a, deck_b = build_test_cards(cards, args.keyword_a, args.amount, args.keyword_b, args.amount)

    run(args.n, deck_a, deck_b, cards, f"A={args.keyword_a} vs B={args.keyword_b}")
    # swap sides to rule out any going-first asymmetry
    run(args.n, deck_b, deck_a, cards, f"A={args.keyword_b} vs B={args.keyword_a} (sides swapped)")


if __name__ == "__main__":
    main()
