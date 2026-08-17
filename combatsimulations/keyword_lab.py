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
Anchored, Initiative Shift X, Locked, and Sealed aren't single
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

Raw die-bonus testing (2026-07-29): TRACE and STILL COUNTING don't grant a
KEYWORD_GRANTS keyword at all — their Attack line reads "+1d6" directly
("Attack: Mind + d6. If [condition], +1d6."), a raw bonus die, not a status
flag. That shape needs a different comparison than keyword-vs-keyword: three
otherwise-identical decks (GATED = the real card's own condition, UNGATED =
the same +1d6 with no gate at all, PLAIN = no bonus, a vanilla d6 attack),
run GATED-vs-UNGATED (isolates exactly what the gate costs) and GATED-vs-
PLAIN (is the gated card worth its slot at all). --die-bonus switches modes;
keyword_a/keyword_b are ignored when it's set.
    python3 keyword_lab.py --die-bonus foe_discard_streak --die-bonus-color B --die-bonus-stat mind   # TRACE
    python3 keyword_lab.py --die-bonus self_never_moved --die-bonus-color G --die-bonus-stat soul     # STILL COUNTING

Team battles (2026-07-29): everything above runs a 1v1 Duel, which is blind
to anything that only matters with real teammates present — ally-targeting
text ("target ally", "all allies") is a no-op in a Duel, and focus-fire /
blocking-capacity dynamics (a combatant attacked several times between its
own turns spends a card each block, so hands run dry) simply don't exist
there. --team switches every mode above (keyword grants, conditions,
die-bonus) to team_engine.Battle instead, with --team-size (default 3)
combatants per side, all running the same real team policy (team_tactician)
team_run.py itself uses — not a blanket default, opt in only when the
mechanic under test is actually team-shaped.
    python3 keyword_lab.py deadly evade --team                       # is Deadly still ahead with real teammates around?
    python3 keyword_lab.py --die-bonus foe_moved --team --team-size 4
"""

import argparse
from collections import Counter

import content
from engine import Card, Combatant, Duel, roll, _rolled_die
from content import _same_as_discard_top
from policies import TacticianPolicy
from team_engine import Battle
from team_policies import make_team_policy

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
    # RETALIATE's real gate ("if you were hit last turn by the foe"), same
    # engine._prior_turn_hit check _retaliate_effect itself makes in content.py.
    "was_hit_last_turn": lambda engine, me, foe: (
        engine._prior_turn_hit['hit']
        and engine._prior_turn_hit['target'] is me
        and engine._prior_turn_hit['actor'] in engine.enemies(me)
    ),
    # TRACE's real gate: did the foe's last two discards share a color? Same
    # check _trace_dmg itself makes (content._same_as_discard_top(foe)).
    "foe_discard_streak": lambda engine, me, foe: _same_as_discard_top(foe),
    # TRACE's gate, "lowered by 1" (2026-07-29, Drew's own framing after the
    # payoff-bump pass found the ~10% trigger rate itself was the actual
    # problem, not either payoff form) — the real gate has no numeric dial
    # to decrement, so this is a translation, flagged as one: instead of
    # requiring the just-played card to match ONLY the single immediately-
    # preceding discard, it also succeeds if it matches the one before that
    # — one additional card added to the lookback window, the most literal
    # "one step looser" reading of the actual mechanic. Test-only — not
    # wired into content.py's real TRACE, which still matches
    # foe_discard_streak exactly above.
    "foe_discard_streak_loose": lambda engine, me, foe: (
        len(foe.discard) >= 2
        and (foe.discard[-1].color == foe.discard[-2].color
             or (len(foe.discard) >= 3 and foe.discard[-1].color == foe.discard[-3].color))
    ),
    # STILL COUNTING's real gate: "have you not changed position this
    # combat" — cumulative, not just since-last-turn (that's foe_moved's
    # job). No engine-level tracker for "ever repositioned" exists (only
    # _repositioned_since_last_turn, a one-turn window), and building one
    # would mean touching Combatant.position engine-wide for a test-only
    # need. Instead tracked locally: _mover_fn (the only thing that can
    # move a combatant in these test decks) sets _ever_repositioned itself,
    # which is exact here because it's the sole mover in play — would NOT
    # generalize to a real mixed deck with multiple move cards.
    "self_never_moved": lambda engine, me, foe: not getattr(me, '_ever_repositioned', False),
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
_MOVER_CONDITIONS = {"backline", "frontline", "foe_backline", "foe_frontline",
                      "foe_moved", "self_never_moved"}


def _mover_fn(engine, me, foe):
    me._ever_repositioned = True
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
                      condition_a=None, condition_b=None, base_die_a=6, base_die_b=6):
    """Registers FILLER_R/B/G (neutral, no Effect, Range: Both, d6) and one
    GRANT_<KEYWORD> card per side, sharing the same range/color/stat so the
    only variables between the two decks are which keyword each grants and
    (if base_die_a/b differ) each GRANT card's own die — e.g. to check what
    a die-size bump does to a specific gated card (RETALIATE at d8 instead
    of its current d6). Filler stays d6 regardless — it's generic deck
    padding, not the card under test. condition_a/condition_b are names
    from CONDITIONS (or None for an unconditional grant, the original
    behavior). Returns (deck_a, deck_b, counter_a, counter_b) — the
    counters are empty dicts when the matching condition is None (nothing
    to measure)."""
    def add(name, color, stat, effect=None, defense=None, base_die=6):
        cards[name] = Card(name=name, color=color, stat=stat, reach="both",
                            base_die=base_die, effect=effect, defense=defense, damage=None)

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
    for label, kw, amount, cond_name, counter, base_die in (
        ("A", keyword_a, amount_a, condition_a, counter_a, base_die_a),
        ("B", keyword_b, amount_b, condition_b, counter_b, base_die_b),
    ):
        attr, is_bool, target = KEYWORD_GRANTS[kw]
        condition = CONDITIONS[cond_name] if cond_name else None
        fn = _make_grant_fn(attr, is_bool, amount, _TARGET[target], condition, counter)
        add(f"GRANT_{label}", "R", "body", effect=fn, defense=fn, base_die=base_die)

    deck_a = filler + ["GRANT_A"]
    deck_b = filler + ["GRANT_B"]
    return deck_a, deck_b, counter_a, counter_b


def _make_damage_bonus_fn(stat, condition, counter, base_die=6, bonus_dice=1):
    """TRACE/STILL COUNTING's shape: base = stat + base_die (respects a held
    Deadly/Weak stack, same as the real cards' own base roll), +bonus_dice
    more d6 if the gate is true (independent dice, NOT routed through
    Deadly/Weak — matches _trace_dmg's own comment on why its bonus uses
    plain roll() instead of _rolled_die()). condition=None means the bonus
    always applies (the UNGATED comparison case). base_die only scales the
    card's OWN base roll — the bonus die(s) are a separate, independently-
    named part of the real card text and stay d6 regardless (matches
    RHYTHM BREAK's real shape: "Attack: Body + d8. If X, +1d6."). bonus_dice
    is the payoff lever (default 1, matching the real "+1d6" text) — bump
    to check what a bigger payoff does to a gate that's already at its
    real trigger rate."""
    def fn(engine, me, foe):
        base = me.eff(stat) + _rolled_die(base_die, engine.rng, me)
        bonus = sum(roll(6, engine.rng) for _ in range(bonus_dice))
        if condition is None:
            return base + bonus
        counter['total'] += 1
        if condition(engine, me, foe):
            counter['hit'] += 1
            base += bonus
        return base
    return fn


def build_damage_bonus_deck(cards, color, stat, mode, needs_mover, condition_name=None,
                             counter=None, deck_id="", base_die=6, bonus_dice=1):
    """One filler+1-special-card deck (same shape as build_test_cards) where
    the special card's Attack line carries a raw +Nd6 bonus instead of a
    KEYWORD_GRANTS keyword — TRACE/STILL COUNTING's actual shape, which
    doesn't fit build_test_cards at all. mode is 'gated' (condition_name's
    real gate), 'ungated' (bonus always applies — isolates what the gate
    costs), or 'plain' (no bonus at all — the vanilla-card baseline;
    bonus_dice has no effect in this mode).
    base_die scales only the SPECIAL card's own base roll (e.g. to check
    what a die-size bump does to TRACE) — filler stays d6 regardless, same
    reasoning as build_test_cards's base_die_a/b. bonus_dice scales the
    gated payoff itself (e.g. to check what a bigger bonus does instead of
    a bigger base die) — held equal between GATED and UNGATED so "cost of
    the gate" is measured at the same payoff level, same principle as
    base_die.
    needs_mover is decided once by the caller for the whole test (not
    per-deck) and applied to every mode uniformly — the MOVER card only
    matters for GATED's own condition, but if it changed the filler mix
    only on the GATED side, that would itself become a second confound on
    top of the one thing this test isolates.
    Defensive Bonus deliberately left unset: the real cards' own Defensive
    Bonus text (TRACE strips status, STILL COUNTING grants Resist) is a
    second, unrelated mechanic — mixing it in here would confound the one
    thing this test isolates, the Attack-line gate."""
    def add(name, c, s, damage=None, effect=None, defense=None, die=6):
        cards[name] = Card(name=name, color=c, stat=s, reach="both", base_die=die,
                            damage=damage, effect=effect, defense=defense)

    add("FILLER_R" + deck_id, "R", "body")
    add("FILLER_B" + deck_id, "B", "mind")
    add("FILLER_G" + deck_id, "G", "soul")
    filler = [f"FILLER_R{deck_id}"] * 3 + [f"FILLER_B{deck_id}"] * 3

    if needs_mover:
        add("MOVER" + deck_id, "G", "soul", effect=_mover_fn, defense=_mover_fn)
        filler += [f"FILLER_G{deck_id}", "MOVER" + deck_id]   # 8 cards total
    else:
        filler += [f"FILLER_G{deck_id}"] * 2                  # 8 cards total

    if mode == 'plain':
        fn = None
    elif mode == 'ungated':
        fn = _make_damage_bonus_fn(stat, None, None, base_die, bonus_dice)
    else:  # gated
        fn = _make_damage_bonus_fn(stat, CONDITIONS[condition_name], counter, base_die, bonus_dice)
    add("SPECIAL" + deck_id, color, stat, damage=fn, die=base_die)

    return filler + ["SPECIAL" + deck_id]


def run_damage_bonus_test(color, stat, condition_name, n, base_die=6, bonus_dice=1, runner=None):
    """The 'different approach' TRACE/STILL COUNTING need: not keyword-vs-
    keyword, but GATED-vs-UNGATED (what does the gate itself cost?) and
    GATED-vs-PLAIN (is the gated card worth its slot at all?), holding
    color/stat/filler identical throughout so the gate is the only variable.
    base_die (default 6, the current printed die) lets a bumped die (e.g. 8)
    be checked the same way, PLAIN included, so "is it worth its slot"
    reflects the same bumped base, not a stale d6 comparison. bonus_dice
    (default 1, the current printed "+1d6") lets a bigger payoff be checked
    instead of/alongside a bigger die — the other lever named when TRACE
    first came up as underpowered. runner defaults to the 1v1 run() below;
    pass run_team (or a partial binding team_size) to run this as a team
    battle instead — the deck-building logic is identical either way, only
    how the deck gets fought out changes."""
    runner = runner or run
    needs_mover = condition_name in _MOVER_CONDITIONS
    for opponent_mode, note in (("ungated", "cost of the gate itself"),
                                 ("plain", "value of the card at all")):
        cards = content.build_cards()
        counter = {"hit": 0, "total": 0}
        deck_gated = build_damage_bonus_deck(cards, color, stat, "gated", needs_mover, condition_name,
                                              counter, deck_id="1", base_die=base_die, bonus_dice=bonus_dice)
        deck_other = build_damage_bonus_deck(cards, color, stat, opponent_mode, needs_mover,
                                              deck_id="2", base_die=base_die, bonus_dice=bonus_dice)
        runner(n, deck_gated, deck_other, cards,
               f"GATED({condition_name}, d{base_die}+{bonus_dice}d6) vs {opponent_mode.upper()}(d{base_die}) [{note}]", counter, None)
        # swap sides to rule out going-first asymmetry
        cards2 = content.build_cards()
        counter2 = {"hit": 0, "total": 0}
        deck_other2 = build_damage_bonus_deck(cards2, color, stat, opponent_mode, needs_mover,
                                               deck_id="1", base_die=base_die, bonus_dice=bonus_dice)
        deck_gated2 = build_damage_bonus_deck(cards2, color, stat, "gated", needs_mover, condition_name,
                                               counter2, deck_id="2", base_die=base_die, bonus_dice=bonus_dice)
        runner(n, deck_other2, deck_gated2, cards2,
               f"{opponent_mode.upper()}(d{base_die}) vs GATED({condition_name}, d{base_die}+{bonus_dice}d6) (sides swapped)", None, counter2)


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


def run_team(n, deck_a, deck_b, cards, label, team_size, counter_a=None, counter_b=None):
    """Same A/B comparison as run() above, but team_size-vs-team_size via
    team_engine.Battle instead of a 1v1 Duel — every teammate on a side
    runs the identical deck (same isolate-one-variable principle as the
    rest of this file, just with real allies now actually present for
    ally-targeting text to reach), using team_tactician (team_policies.py),
    the real team-aware policy team_run.py itself uses — TacticianPolicy
    doesn't even have the right interface (it picks a single foe; team
    battles pick a target among several)."""
    wins = Counter()
    total_turns = 0
    for i in range(n):
        team_a = [Combatant(f"A{j+1}", body=3, mind=3, soul=3, decklist=deck_a, policy=make_team_policy())
                  for j in range(team_size)]
        team_b = [Combatant(f"B{j+1}", body=3, mind=3, soul=3, decklist=deck_b, policy=make_team_policy())
                  for j in range(team_size)]
        battle = Battle(team_a, team_b, cards, seed=i)
        result = battle.run()
        wins[{0: 'A', 1: 'B', 'TIE': 'TIE'}[result]] += 1
        total_turns += battle.turn_count
    print(f"{label} [team x{team_size}]: A {wins['A']:6} ({100*wins['A']/n:5.1f}%)  "
          f"B {wins['B']:6} ({100*wins['B']/n:5.1f}%)  "
          f"TIE {wins.get('TIE', 0):6} ({100*wins.get('TIE', 0)/n:5.1f}%)  "
          f"avg turns {total_turns/n:.1f}")
    for tag, counter in (("A", counter_a), ("B", counter_b)):
        if counter and counter["total"]:
            pct = 100 * counter["hit"] / counter["total"]
            print(f"    condition {tag}: true on {counter['hit']}/{counter['total']} plays ({pct:.1f}%)")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("keyword_a", nargs="?", choices=sorted(KEYWORD_GRANTS))
    p.add_argument("keyword_b", nargs="?", choices=sorted(KEYWORD_GRANTS))
    p.add_argument("amount", nargs="?", type=int, default=1,
                    help="stack count / value for both keywords if they take one (default 1)")
    p.add_argument("--n", type=int, default=20000)
    p.add_argument("--condition-a", choices=sorted(CONDITIONS), default=None,
                    help="only grant keyword_a when this real card-gate condition is true (default: unconditional)")
    p.add_argument("--condition-b", choices=sorted(CONDITIONS), default=None,
                    help="only grant keyword_b when this real card-gate condition is true (default: unconditional)")
    p.add_argument("--die-bonus", choices=sorted(CONDITIONS), default=None,
                    help="switch modes entirely: test a raw +1d6 Attack-line bonus gated on "
                         "this condition (TRACE/STILL COUNTING's shape) instead of a keyword "
                         "grant. keyword_a/keyword_b are ignored when this is set.")
    p.add_argument("--die-bonus-color", choices=["R", "B", "G"], default="B",
                    help="color of the special card in --die-bonus mode (default B, TRACE's own)")
    p.add_argument("--die-bonus-stat", choices=["mind", "body", "soul"], default="mind",
                    help="stat of the special card in --die-bonus mode (default mind, TRACE's own)")
    p.add_argument("--die-bonus-base-die", type=int, choices=[2, 4, 6, 8, 10], default=6,
                    help="base die of the special card in --die-bonus mode (default 6) — bump "
                         "this to check what a die-size change does to a real gated card")
    p.add_argument("--die-bonus-payoff-dice", type=int, default=1,
                    help="number of d6 the gate grants in --die-bonus mode (default 1, matching "
                         "the real '+1d6' text) — bump this to check what a bigger payoff does "
                         "instead of/alongside a bigger base die")
    p.add_argument("--base-die-a", type=int, choices=[2, 4, 6, 8, 10], default=6,
                    help="base die of GRANT_A in keyword mode (default 6) — bump this to check "
                         "what a die-size change does to a real gated card")
    p.add_argument("--base-die-b", type=int, choices=[2, 4, 6, 8, 10], default=6,
                    help="base die of GRANT_B in keyword mode (default 6)")
    p.add_argument("--team", action="store_true",
                    help="run team_size-vs-team_size battles (team_engine.Battle) instead of "
                         "1v1 duels, for cards/mechanics that only matter with real teammates "
                         "present (ally-targeting text, focus-fire, blocking capacity) — not a "
                         "default, opt in when the mechanic under test is actually team-shaped")
    p.add_argument("--team-size", type=int, default=3,
                    help="combatants per side in --team mode (default 3, matching team_run.py)")
    args = p.parse_args()

    runner = (lambda n, da, db, c, label, ca=None, cb=None:
              run_team(n, da, db, c, label, args.team_size, ca, cb)) if args.team else run

    if args.die_bonus:
        run_damage_bonus_test(args.die_bonus_color, args.die_bonus_stat, args.die_bonus,
                               args.n, args.die_bonus_base_die, args.die_bonus_payoff_dice, runner)
        return

    if not args.keyword_a or not args.keyword_b:
        p.error("keyword_a and keyword_b are required unless --die-bonus is given")

    cards = content.build_cards()
    deck_a, deck_b, counter_a, counter_b = build_test_cards(
        cards, args.keyword_a, args.amount, args.keyword_b, args.amount,
        args.condition_a, args.condition_b, args.base_die_a, args.base_die_b)

    runner(args.n, deck_a, deck_b, cards, f"A={args.keyword_a}(d{args.base_die_a}) vs B={args.keyword_b}(d{args.base_die_b})", counter_a, counter_b)
    # swap sides to rule out any going-first asymmetry
    cards2 = content.build_cards()
    deck_b2, deck_a2, counter_b2, counter_a2 = build_test_cards(
        cards2, args.keyword_b, args.amount, args.keyword_a, args.amount,
        args.condition_b, args.condition_a, args.base_die_b, args.base_die_a)
    runner(args.n, deck_b2, deck_a2, cards2, f"A={args.keyword_b}(d{args.base_die_b}) vs B={args.keyword_a}(d{args.base_die_a}) (sides swapped)", counter_b2, counter_a2)


if __name__ == "__main__":
    main()
