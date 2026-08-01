"""
Card content for the duel simulator — exactly Frost's and Steele's decks.

Each card's Effect and Defensive Bonus is implemented as faithfully as the rules
allow. Ally-only effects are deliberately no-ops in a 1v1 (You Are Not Your Own
Ally) and are marked DEAD — the sim will show how much dead weight each deck
carries into single combat. Simplifications are logged via RULING().
"""

from engine import Card, roll, RULING, COLOR_TO_STAT, _rushdown, _rolled_die, _deadly_weak_bonus, can_attack


def warded(target):
    """Consume a Ward/Deflect-ward if present; True means the debuff is blocked."""
    if target.ward:
        target.ward = False
        RULING("ward-blocks-debuff",
               "Ward/DEFLECT blocks the next auxiliary debuff — status conditions, "
               "stat reductions, discard, Injury/Exhaust seeding, disabling a "
               "Defensive Bonus, Positive Status Effect removal. Never "
               "RPS/Initiative/Position pillar manipulation (rules/card-glossary.md "
               "Debuff) — those callers don't route through warded() at all.")
        return True
    return False


def debuff(target, apply_fn):
    """The one gate every simple Debuff-granting effect should route through
    (card-glossary.md, Ward/Debuff), instead of calling warded() ad hoc — or
    not at all — per card. If target is Warded, the Ward is consumed here and
    apply_fn() never runs, so a compound grant (e.g. Weak-and-Blind together)
    either fully lands or fully doesn't, never half-resolves. Returns whether
    the debuff actually landed. Built 2026-07-24 after an audit found ~20 real
    cards silently skipping warded() entirely — the same recurring miss
    Drew named directly ("the sim... based it incorrectly off of where the
    status comes from instead of correctly identifying debuffs and preventing
    them," unresolved-concerns.md) — the same shape of fix as
    _deadly_weak_bonus for Deadly/Weak: one shared function instead of dozens
    of places each individually free to forget the check."""
    if warded(target):
        return False
    apply_fn()
    return True


def apply_blind(target, n=1):
    debuff(target, lambda: setattr(target, 'blind', target.blind + n))


def apply_weak(target, n=1):
    debuff(target, lambda: setattr(target, 'weak', target.weak + n))


def apply_vulnerable(target, n=1):
    """No card applied Vulnerable to a foe anywhere in the pool before
    2026-08-01 (OVERCOMMIT's is a deliberate self-inflicted exception, not
    routed through debuff() since Ward never blocks a self-application) —
    the Oracle keyword-coverage pass needed it for real, so it's built here
    the same shape as apply_weak/apply_blind, not invented fresh."""
    debuff(target, lambda: setattr(target, 'vulnerable', target.vulnerable + n))


def apply_rooted(target):
    debuff(target, lambda: setattr(target, 'rooted', True))


def apply_staggered(target):
    debuff(target, lambda: setattr(target, 'staggered', True))


def apply_stat_drain(target, stat, n=1):
    debuff(target, lambda: target.adjust(stat, -n))


def apply_injury(engine, target):
    debuff(target, lambda: engine.insert_injury(target))


def apply_exhaust(engine, target, n=1):
    debuff(target, lambda: engine.insert_exhaust(target, n))


def strip_positive_status(target):
    return debuff(target, lambda: remove_positive_status(target))


def remove_positive_status(target):
    """Positive Status Effects (rules/card-glossary.md): Evade, Resist, Deadly,
    Protect, Anchored, Quick. Quick is real now (OVERDRIVE, formerly
    OVERCOMMIT's own mechanic before the 2026-07-29 split — engine.py's
    Duel.take_turn) — this docstring was stale from before that; a pending
    Quick grant is exactly as much a Positive Status Effect as the rest and
    belongs here too."""
    target.evade = 0
    target.resist = 0
    target.deadly = 0
    target._protect = False
    target._quick = False
    target.ongoing = [o for o in target.ongoing if 'anchor' not in o]   # Anchored-flavored entries only


def _same_as_discard_top(target):
    """TRACE's condition: did the card just played match either of the top
    two cards already sitting in the discard pile before it? discard[-1] is
    the just-played card (already appended by the time Effect/Defense
    fires); discard[-2] and discard[-3] are what was on top before that.
    Widened from checking only discard[-2] (2026-07-29, Drew: "lower
    TRACE's gate by 1") — the keyword_lab dice-pass check found the ~10%
    trigger rate on the original single-card check, not the payoff or base
    die (both tried first and ruled out), was the actual reason the card
    underperformed."""
    d = target.discard
    if len(d) < 2:
        return False
    if d[-1].color == d[-2].color:
        return True
    return len(d) >= 3 and d[-1].color == d[-3].color


# ============================ FROST ==========================================

def _burn_bright_dmg(engine, me, foe):
    base = me.body + roll(8, engine.rng) + _deadly_weak_bonus(engine.rng, me)
    if me.hand:  # exile 1 from hand for +2 this attack
        me.exile.append(me.hand.pop(engine.rng.randrange(len(me.hand))))
        base += 2
    return base


def _burn_bright_defense(engine, me, foe):
    if me.discard:
        me.exile.append(me.discard.pop())


def _fracture_dmg(engine, me, foe):
    return me.eff('mind') + roll(6, engine.rng) + _deadly_weak_bonus(engine.rng, me)


def _fracture_effect(engine, me, foe):
    top3 = me.discard[-3:]
    if len(top3) != 3 or len({c.color for c in top3}) != 3:
        return
    enemies = engine.enemies(me)
    front = [e for e in enemies if e.position == 'frontline']
    back = [e for e in enemies if e.position == 'backline']
    side = front if len(front) >= len(back) else back   # "your choice" — pick the fuller side
    for e in side:
        engine.deal(e, 5)   # bumped 3 -> 5, 2026-07-24

def _fracture_defense(engine, me, foe):
    # Fixed 2026-07-24: no defense= was registered at all — this Defensive
    # Bonus never fired once, regardless of discard-pile state.
    top3 = me.discard[-3:]
    if len(top3) != 3 or len({c.color for c in top3}) != 3:
        return
    if foe.discard:   # foe = attacker here; their just-played card is on top
        foe.exile.append(foe.discard.pop())


def _trace_dmg(engine, me, foe):
    # Base roll still respects a Deadly/Weak stack the caster is already
    # holding from an earlier card (was silently dropped before 2026-07-23 —
    # see _deadly_weak_bonus). Card text reworded 2026-07-28 to drop the word
    # "Deadly" entirely (Drew's call) — this was never the stackable keyword,
    # just a flat conditional bonus on this attack's own roll; still a
    # second, independent bonus (now 2d6, bumped from 1d6 2026-07-29 —
    # payoff alone didn't fix the card, per the dice-pass check, but shipped
    # together with the widened gate above, not on its own) on top of any
    # held stack, not routed through it.
    base = me.eff('mind') + _rolled_die(6, engine.rng, me)
    if _same_as_discard_top(foe):
        base += roll(6, engine.rng) + roll(6, engine.rng)
    return base


def _trace_defense(engine, me, foe):
    if _same_as_discard_top(foe):   # foe = attacker here
        strip_positive_status(foe)


def _twin_strike_dmg(engine, me, foe):
    RULING("twin-strike-double-roll",
           "TWIN STRIKE '(Soul + d2) x2' is read as two independent (Soul + d2) "
           "instances summed, not one roll doubled.")
    # Two independent damage rolls means a held Deadly/Weak stack can apply
    # to either (or, with 2+ stacks, both) — each _rolled_die call checks and
    # consumes its own stack, same as if these were two separate cards.
    return (me.soul + _rolled_die(4, engine.rng, me)) + (me.soul + _rolled_die(4, engine.rng, me))


def _axiom_effect(engine, me, foe):
    # RPS-pillar manipulation — not a Debuff, Ward never touches it (rules/card-glossary.md).
    color = me.policy.name_axiom_color(engine, me, foe)
    foe.axiom_ban = color
    engine._say(f"    AXIOM bans {color} on {foe.name}'s next reveal")


def _sacrifice_strike_dmg(engine, me, foe):
    # Reworded 2026-07-28 (Drew's call): "Pay 3 HP" moved from Effect (which
    # fires on a win OR a tie) onto the Attack line — damage() only ever runs
    # on an attacker win, so this narrows the cost to win-only, dropping the
    # old tie case entirely. Effect is genuinely None now, not just relabeled.
    engine.deal(me, 3, unpreventable=True)
    return me.eff('body') + _rolled_die(10, engine.rng, me)


def _sacrifice_strike_defense(engine, me, foe):
    engine.deal(me, 5, unpreventable=True)
    engine.deal(foe, me.eff('body') + roll(10, engine.rng), unpreventable=True)   # Counter Attack: this card's own damage back (SACRIFICE STRIKE, base die capped at d10)


def _blood_in_the_gap_effect(engine, me, foe):
    engine.heal(me, me._last_hit // 2)   # Lifesteal: half of this attack's landed damage


def _blood_in_the_gap_defense(engine, me, foe):
    me.thorns += 1


def _spark_effect(engine, me, foe):
    engine.deal(foe, 3, unpreventable=True)


def _deflect_effect(engine, me, foe):
    me.ward = True


def _deflect_defense(engine, me, foe):
    # Only on a clean win, never a tie — same `_redirect_dmg`-is-set-only-on-a-
    # clean-win signal REFRACT/FORGET already use.
    if getattr(foe, '_redirect_dmg', None) is None:
        return
    engine.deal(foe, me.mind + roll(6, engine.rng), unpreventable=True)  # counter, no new RPS


def _realignment_effect(engine, me, foe):
    me.position = 'backline' if me.position == 'frontline' else 'frontline'
def _realignment_defense(engine, me, foe):
    # Fixed 2026-07-24: this was marked unmodeled citing "Quick has never
    # been implemented anywhere in the sim" — stale by the time OVERCOMMIT
    # shipped Quick for real (`_quick`, checked in both engines' take_turn).
    # "All allies" excludes the caster, matching WARSONG/URGENCY's own
    # established convention for the same phrase.
    for a in engine.allies(me):
        a._quick = True


def _climb_effect(engine, me, foe):
    n = min(2, len(me.deck))
    bottom = [me.deck.pop(0) for _ in range(n)]   # index 0 = bottom (deck.pop() draws the end = top)
    for c in bottom:
        if c.is_status:
            me.discard.append(c)    # bury the Injury properly rather than hand it back the top
        else:
            me.deck.append(c)       # place on top (append = top, drawn next)


def _climb_defense(engine, me, foe):
    me.ongoing.append({'kind': 'handsize'})


# ============================ STEELE =========================================

def _forget_effect(engine, me, foe):
    # Fixed 2026-07-24: forced discard is now a Debuff, Ward-blockable — this
    # comment used to say the opposite ("ignores Ward, not a debuff"), which
    # was the rule before Drew's direct call expanding Debuff's scope.
    # Discard a real card, not an Injury — forcing away their Injury would help them.
    if warded(foe):
        return
    reals = [i for i, c in enumerate(foe.hand) if not c.is_status]
    if reals:
        foe.discard.append(foe.hand.pop(engine.rng.choice(reals)))


def _forget_defense(engine, me, foe):
    # Only on a clean win, never a tie — `foe._redirect_dmg` is set by attack()
    # only on a genuine defender-win right before defense() fires (same signal
    # REFRACT's defense uses), and is None on a tie.
    if getattr(foe, '_redirect_dmg', None) is None:
        return
    # exile the attacker's just-played card (top of their discard)
    if foe.discard:
        foe.exile.append(foe.discard.pop())


def _blood_tithe_effect(engine, me, foe):
    engine.deal(me, 2, unpreventable=True)
    allies = engine.allies(me)     # heal the most-hurt ally 6 (dead in 1v1)
    if allies:
        engine.heal(min(allies, key=lambda a: a.hp), 6, source=me)


def _blood_tithe_defense(engine, me, foe):
    engine.deal(me, 2, unpreventable=True)   # "Pay 2 HP"
    allies = engine.allies(me)             # heal the most-hurt ally 8 (dead in 1v1)
    if allies:
        engine.heal(min(allies, key=lambda a: a.hp), 8, source=me)


def _gamblers_ruin_dmg(engine, me, foe):
    die = roll(4, engine.rng)          # the DIE result explodes, not the total (d6 -> d4, 2026-07-29)
    total = me.body + die
    rerolls = 0
    while rerolls < 3 and die % 2 == 1:
        die = roll(4, engine.rng)
        total += die
        rerolls += 1
    # Deadly/Weak apply once, to the attack overall, added after the
    # explosion resolves — kept out of the loop above so a Deadly-inflated
    # roll can't itself trigger (or a Weak-deflated one avoid) an explosion
    # that shouldn't have happened.
    return total + _deadly_weak_bonus(engine.rng, me)


def _gamblers_ruin_defense(engine, me, foe):
    # Reworded 2026-07-28 (Drew's call) — was a pre-rolled flat bonus banked
    # in next_attack_bonus, now the real Deadly stack: rolled fresh whenever
    # the next attack actually happens, consumable/cancelable like any other
    # held Deadly, and correctly respected by _deadly_weak_bonus everywhere.
    me.deadly += 1


def _repel_effect(engine, me, foe):
    # Position-pillar manipulation — not a Debuff, Ward never touches it (rules/card-glossary.md).
    # Fixed 2026-07-24: was single-target (just `foe`) — text says "all
    # enemies," invisible in a 1v1 (only one enemy exists) but a real gap in
    # team play against SMOKE SCREEN's own correct "all enemies" precedent.
    for e in engine.enemies(me):
        if e.position == 'frontline' and not e._grounded:   # GROUNDING STANCE
            e.position = 'backline'


def _pain_is_fuel_effect(engine, me, foe):
    me.resist += 1


def _pain_is_fuel_defense(engine, me, foe):
    me.thorns += 1


def _brace_effect(engine, me, foe):
    me.resist += 2
def _brace_defense(engine, me, foe):
    me.resist += 2


def _paradox_effect(engine, me, foe):
    engine.heal(me, me._last_hit // 2)     # Lifesteal: half of this attack's landed damage


def _paradox_defense(engine, me, foe):
    me.ward = True


def _spiral_current_effect(engine, me, foe):
    for c in (me, foe):
        c.position = 'backline' if c.position == 'frontline' else 'frontline'


def _align_effect(engine, me, foe):
    seen = engine.scry(me, me, 2)              # reorder own deck; then conditional draw + Resist
    if len(seen) == 2 and seen[0].color == seen[1].color and seen[0].color is not None:
        c = me.draw_one(engine.rng)
        if c:
            me.hand.append(c)
        me.resist += 1


def _align_defense(engine, me, foe):
    seen = engine.scry(me, me, 2)
    if len(seen) == 2 and seen[0].color == seen[1].color and seen[0].color is not None:
        c = me.draw_one(engine.rng)
        if c:
            me.hand.append(c)
        me.deadly += 1


def _axiom_defense(engine, me, foe):
    # RPS-pillar manipulation — not a Debuff, Ward never touches it (rules/card-glossary.md).
    color = me.policy.name_axiom_color(engine, me, foe)   # mirror-ban the attacker
    foe.axiom_ban = color
    engine._say(f"    AXIOM bans {color} on {foe.name}'s next reveal")


def _anticipate_effect(engine, me, foe):
    me._anticipating = True   # draws before defending, every qualifying attack, until my next turn


def _anticipate_defense(engine, me, foe):
    apply_weak(foe)


def _renewal_effect(engine, me, foe):
    # Fixed 2026-07-24: was unconditional heal, no discard-then-draw branch
    # at all. Real per-ally choice now: cycle a held status card (Injury/
    # Exhaust) if there's one worth clearing, otherwise take the flat heal —
    # a simple, real heuristic for "which is better right now" rather than
    # always defaulting to the same branch.
    for a in engine.allies(me):    # ally-only: no self
        statuses = [i for i, c in enumerate(a.hand) if c.is_status]
        if statuses:
            a.discard.append(a.hand.pop(statuses[0]))
            c = a.draw_one(engine.rng)
            if c:
                a.hand.append(c)
        else:
            engine.heal(a, 4, source=me)


def _renewal_defense(engine, me, foe):
    downed = engine.downed_allies(me)
    if downed:
        engine.heal(downed[0], 8, source=me)   # revival heal — source= places them right after me in the wheel


def _twin_strike_defense(engine, me, foe):
    apply_weak(foe)   # foe = attacker here


# ==================== MIRE (Injury-attrition, 3/3/3) ==========================
# A control deck built on shuffling Injuries into the opponent's deck (Rend,
# Taint), then cashing them in (Press the Injury), plus combat-long stat erosion
# (Wither -Body, Erode -Soul). Perfectly balanced 3R/3B/3G across the RPS wheel.


def remove_injuries(target, n=None):
    """Permanently destroy up to n Injuries (all if n is None) from HAND + DISCARD
    only — never the deck (Drew: no tracking/searching hidden Injuries)."""
    removed = 0
    for pile in (target.hand, target.discard):
        i = 0
        while i < len(pile):
            if pile[i].is_status and pile[i].name == 'INJURY' and (n is None or removed < n):
                pile.pop(i)
                removed += 1
            else:
                i += 1
    return removed


def remove_status_cards(target, n=None):
    """Permanently destroy up to n status cards — Injury OR Exhaust — from HAND
    + DISCARD only, never the deck. Press the Injury's Defensive Bonus (broadened
    2026-07-24 to match its now-broader status_cards_visible() count)."""
    removed = 0
    for pile in (target.hand, target.discard):
        i = 0
        while i < len(pile):
            if pile[i].is_status and (n is None or removed < n):
                pile.pop(i)
                removed += 1
            else:
                i += 1
    return removed


# --- Green ---
def _balance_effect(engine, me, foe):
    if me.hand:
        me.discard.append(me.hand.pop(engine.rng.randrange(len(me.hand))))
        apply_staggered(foe)


def _balance_defense(engine, me, foe):
    if me.hand:
        me.discard.append(me.hand.pop(engine.rng.randrange(len(me.hand))))
        apply_staggered(foe)   # foe = attacker here


def _wither_effect(engine, me, foe):
    apply_stat_drain(foe, 'body')   # -1 Body AND -3 max HP; no self-Injury cost anymore


def _mockery_effect(engine, me, foe):
    engine.initiative_shift(foe, -2)


def _mockery_defense(engine, me, foe):
    foe._forced_target = me   # taunt: attacker must target me next turn (team play)


# --- Red ---
def _rend_effect(engine, me, foe):
    if me._last_hit > 0:
        apply_injury(engine, foe)


def _rend_defense(engine, me, foe):
    me._rend_guard = True


def _press_the_injury_dmg(engine, me, foe):
    # Broadened 2026-07-24: counts every status card (Injury + Exhaust), not
    # just Injury — Drew's call (card-glossary.md's Debuff/status-card scope
    # already treats them as the same kind of thing).
    return me.eff('body') + roll(6, engine.rng) + _deadly_weak_bonus(engine.rng, me) + 2 * foe.status_cards_visible()


def _press_the_injury_defense(engine, me, foe):
    n = me.status_cards_visible()
    if n:
        engine.heal(me, 2 * n)
        remove_status_cards(me)


# --- Blue ---
def _partition_effect(engine, me, foe):
    foe.must_target_frontline = True


def _partition_defense(engine, me, foe):
    # Dead in a 1v1 (You Are Not Your Own Ally) — engine.allies(me) is always
    # empty there, same as every other ally-only effect. Real in team play:
    # shields the most-hurt ally from being targeted by an attack until MY
    # next turn (take_turn clears it then, tracked via me._partition_shield_target).
    a = _most_hurt(engine.allies(me))
    if a:
        a._partition_shield = True
        me._partition_shield_target = a


def _unname_effect(engine, me, foe):
    # Ward-blockable (card-glossary.md, Debuff) — Drew's call 2026-07-24, for
    # simplicity: a Debuff, full stop, no carved-out exception.
    debuff(foe, lambda: setattr(foe, '_no_defensive_bonus', True))   # until foe's own next turn (take_turn clears it)


def _unname_defense(engine, me, foe):
    if warded(foe):   # forced discard is a Debuff now, see STILLNESS above
        return
    reals = [i for i, c in enumerate(foe.hand) if not c.is_status]
    if reals:
        foe.discard.append(foe.hand.pop(engine.rng.choice(reals)))


def _taint_effect(engine, me, foe):
    apply_injury(engine, foe)


def _taint_defense(engine, me, foe):
    apply_injury(engine, foe)   # foe = attacker here


def _erode_effect(engine, me, foe):
    # Registered as both effect= and defense= below. `foe` means "the other
    # combatant" in both calling conventions — the defender during Effect,
    # the attacker during a Defensive Bonus — so this one function already
    # correctly drains whichever of them the card text calls for without
    # needing two copies.
    apply_stat_drain(foe, 'soul')   # -1 Soul (no HP change — Soul isn't Body); no self-cost


# ==================== GREEN SUPPORT KIT (team play) ==========================
# The cards that make green the team anchor. All ally-targeting, so they're inert
# in 1v1 (engine.allies == []) and come alive in a Battle. Targeting heuristics
# are baked in: heals go to the most-hurt ally, buffs to the best attacker.

# Green's support can target the user too — its effects treat the caster as a
# valid "ally." This is green's color identity and it's what gives green a floor
# in 1v1 (where it otherwise has no ally to support). Only Body/Mind's own
# effects still obey You-Are-Not-Your-Own-Ally.
def _team(engine, me):
    return [me] + engine.allies(me)


def _best_attacker(allies):
    return max(allies, key=lambda a: max(a.eff('body'), a.eff('mind'), a.eff('soul'))) \
        if allies else None


def _most_hurt(allies):
    return min(allies, key=lambda a: a.hp) if allies else None


def _resonate_effect(engine, me, foe):
    for a in engine.allies(me):
        a.deadly += 1                     # all allies gain Deadly (no self)
def _resonate_defense(engine, me, foe):
    for a in engine.allies(me):
        a.resist += 1                     # all allies gain Resist 1 (no self)


def _support_effect(engine, me, foe):
    a = _best_attacker(engine.allies(me))
    if a:
        a.deadly += 1                     # target ally gains Deadly
def _support_defense(engine, me, foe):
    a = _best_attacker(engine.allies(me))
    if a:
        for _ in range(2):                # target ally draws 2
            c = a.draw_one(engine.rng)
            if c:
                a.hand.append(c)




def _witness_effect(engine, me, foe):
    a = _most_hurt(engine.allies(me))
    if a:
        engine.heal(a, 6, source=me)
def _witness_defense(engine, me, foe):
    a = _most_hurt(engine.allies(me))
    if a:
        engine.heal(a, 6, source=me)


def _shared_burden_effect(engine, me, foe):
    me._protect = True
    me.evade += 1
def _shared_burden_defense(engine, me, foe):
    a = _most_hurt(engine.allies(me))
    if a:
        # Fixed 2026-07-24: "choose an amount" had no policy hook to make a
        # real choice with, so it silently capped at a flat, undocumented 4.
        # Give as much as the ally is actually missing, capped by what I can
        # afford to lose without collapsing myself — a real amount tied to
        # the ally's actual need, not an arbitrary number.
        x = min(a.max_hp - a.hp, me.hp - 1)
        if x > 0:
            engine.heal(a, x, source=me)
            engine.deal(me, x, unpreventable=True)   # transfer HP to the ally


# ==================== EXPANDED SET (team-combat variety) =====================
# ~20 more cards covering tanks, team buffs, AoE, tempo denial, positioning,
# ongoing heals, and control. Ally effects route through engine.allies / _team so
# they're live in a Battle and inert in a duel.

# --- Red: front-line, protection, AoE ---
def _strike_defense(engine, me, foe):
    engine.deal(foe, 3, unpreventable=True)

def _guard_effect(engine, me, foe):
    for a in engine.allies(me):
        a.resist += 1                      # all allies gain Resist
def _guard_defense(engine, me, foe):
    for a in engine.allies(me):
        a.resist += 1                      # all allies gain Resist

def _intercept_effect(engine, me, foe):
    me._protect = True
    me.resist += 2
_intercept_defense = _intercept_effect   # same text both sides

def _rally_effect(engine, me, foe):
    engine.deal(me, 5, unpreventable=True)
    for a in engine.allies(me):
        if a.position == 'frontline':
            a.deadly += 1
def _rally_defense(engine, me, foe):
    engine.deal(me, 5, unpreventable=True)
    for a in engine.allies(me):
        if a.position == 'backline':
            a.deadly += 1

def _trample_effect(engine, me, foe):
    if foe.collapsed:                      # this attack dropped the defender
        me._bonus_action = True            # gain another action this turn (take_turn checks this)
def _trample_defense(engine, me, foe):
    foe.position = 'backline'              # push the attacker back

# BREAK's Effect ("Defender reveals hand") is pure information, no state
# change — same treatment as READ, never sim-implemented for the same reason.
def _break_defense(engine, me, foe):
    # Only on a clean win, never a tie (same `_redirect_dmg` signal pattern).
    if getattr(foe, '_redirect_dmg', None) is None:
        return
    engine.deal(foe, me.eff('body') + roll(6, engine.rng), unpreventable=True)   # Counter Attack: this card's own damage back

def _charge_move(engine, me, foe):
    me.position = 'frontline'
    foe.position = 'frontline'

# --- Blue: tempo, control, AoE ---
def _interrupt_effect(engine, me, foe):
    foe.skip_turns += 1                    # target loses their next turn
    me.cannot_defend = True                # you can't defend until your next turn
def _interrupt_defense(engine, me, foe):
    engine.initiative_shift(foe, -2)       # -2 to the attacker (foe), not to yourself

def _sharpen_effect(engine, me, foe):
    # Ally-only (You Are Not Your Own Ally) — correctly a no-op in 1v1, same
    # convention as SUPPORT/ROOTED OATH's identical "target ally" pattern.
    # Fixed 2026-07-24: used to fall back to buffing the caster when no ally
    # existed, which quietly buffed every solo duel instead of doing nothing.
    a = _best_attacker(engine.allies(me))
    if a:
        a.deadly += 1
def _sharpen_defense(engine, me, foe):
    me.deadly += 1

def _chain_effect(engine, me, foe):
    if me._last_hit > 0:
        half = (me._last_hit + 1) // 2
        others = [x for x in engine.enemies(me) if x is not foe]
        if others:
            engine.deal(others[0], half)   # splash to a second enemy
def _chain_defense(engine, me, foe):
    foe._forced_target = me                # taunt the attacker

def _calculate_effect(engine, me, foe):
    if not foe._grounded:   # GROUNDING STANCE
        foe.position = 'backline'
def _calculate_defense(engine, me, foe):
    if not foe._grounded:
        foe.position = 'frontline'

def _analyze_effect(engine, me, foe):
    for a in _team(engine, me):            # you and your allies scry 2
        engine.scry(a, a, 2)

def _study_effect(engine, me, foe):
    for _ in range(2):                     # discard 2, draw 2 — Injuries first if held
        injuries = [c for c in me.hand if c.is_status and c.name == 'INJURY']
        drop = injuries[0] if injuries else next((c for c in me.hand if not c.is_status), None)
        if drop is None:
            break
        me.hand.remove(drop); me.discard.append(drop)
        c = me.draw_one(engine.rng)
        if c:
            me.hand.append(c)
def _study_defense(engine, me, foe):
    me.deadly += 1

def _profile_effect(engine, me, foe):
    engine.scry(me, me, 2)
    c = me.draw_one(engine.rng)            # buffed: scry 2, then draw 1
    if c:
        me.hand.append(c)
def _profile_defense(engine, me, foe):
    apply_staggered(foe)                   # skips their next attack or defend, then clears itself

def _refract_effect(engine, me, foe):
    apply_weak(foe)                        # defender gains Weak
def _refract_defense(engine, me, foe):
    # redirect the attack's full damage to a target of choice -- only on a
    # clean win, never a tie (rules/card-glossary.md, REFRACT). `foe._redirect_dmg`
    # is set by attack() itself right before this fires on a genuine
    # defender-win, and left unset on a tie, so this is a no-op there.
    dmg = getattr(foe, '_redirect_dmg', None)
    if not dmg:
        return
    targets = [e for e in engine.enemies(me) if e is not foe]
    if targets:
        engine.deal(min(targets, key=lambda e: e.hp), dmg)

# --- Green: ongoing support, tempo, position ---
def _synchrony_effect(engine, me, foe):
    # Flagged, not fully fixed, 2026-07-24: text is "allies NEXT TO YOU IN
    # THE INITIATIVE ORDER heal 1 HP AT THE START OF THEIR TURNS" — the same
    # "wheel's own path-walk" gap SLIPSTREAM's own effect already names as
    # unmodeled (no hook exists for initiative-adjacency). The tick below
    # (engine.py's _ongoing_support_tick) instead heals ALL allies, at the
    # start of the CASTER's turn — a real, working simplification, just not
    # the card's actual scope. Left as-is rather than torn out to a no-op
    # (SLIPSTREAM's route): a broader, imprecise heal at least does
    # something, and building genuine adjacency tracking is new engineering,
    # not a bug fix.
    me.ongoing.append({'kind': 'synchrony', 'owner': me})
def _synchrony_defense(engine, me, foe):
    me.resist += 1

def _slipstream_defense(engine, me, foe):
    me.evade += 1

def _slipstream_effect(engine, me, foe):
    # "Whenever an ally passes through your position in the initiative order"
    # needs the wheel's own path-walk (_apply_shift/_rotate_current) to know
    # when that happens — no hook for it yet, left unmodeled, same as STARING
    # CONTEST's positional trigger. What IS real and tested: the ongoing entry
    # itself, and that it's correctly cleared on Collapse (_clear_ongoing_on_collapse).
    me.ongoing.append({'kind': 'slipstream', 'owner': me, 'anchor': me.position})

def _dig_in_effect(engine, me, foe):
    me.ongoing.append({'kind': 'dig_in', 'owner': me, 'anchor': me.position})
_dig_in_defense = _dig_in_effect   # same text both sides

def _rooted_oath_effect(engine, me, foe):
    a = _best_attacker(engine.allies(me))
    if a:
        me.ongoing.append({'kind': 'rooted_oath', 'owner': me, 'anchor': me.position, 'target': a})
def _rooted_oath_defense(engine, me, foe):
    a = _best_attacker(engine.allies(me))
    if a:
        me.ongoing.append({'kind': 'rooted_oath_def', 'owner': me, 'anchor': me.position, 'target': a})

def _urgency_effect(engine, me, foe):
    for a in engine.allies(me):
        engine.initiative_shift(a, 1)
def _urgency_defense(engine, me, foe):
    engine.initiative_shift(me, 1)          # the "-1 to the attacker" choice is unmodeled

def _delay_effect(engine, me, foe):
    engine.initiative_shift(foe, -1)       # defender skips (negative shift)
def _delay_defense(engine, me, foe):
    engine.initiative_shift(foe, -1)

# ==================== Turn-order payoff trio (Retaliate/Warsong/Rebuttal) =====
# All three read engine._prior_turn_hit — a frozen snapshot of whoever's turn
# resolved immediately before this one (see Duel/Battle.take_turn), not a
# rolling window of the last several turns. Landing next to the right ally or
# enemy on the wheel is a live tactical choice (Wait, Initiative Shift), not a
# passive stat — that's the whole point of tying a payoff to it.

def _retaliate_effect(engine, me, foe):
    prior = engine._prior_turn_hit
    if prior['hit'] and prior['target'] is me and prior['actor'] in engine.enemies(me):
        me.deadly += 2
def _retaliate_defense(engine, me, foe):
    engine.initiative_shift(foe, -1)

def _warsong_effect(engine, me, foe):
    # "All allies" excludes the caster, matching URGENCY's own established
    # convention for the same phrase — inert in a Duel (no allies exist
    # there), same accepted shape as Resonate/Support/every other team-play
    # Green card. Simplified 2026-07-24: was gated on "an ally attacked
    # successfully last turn," per Drew's direct text now unconditional.
    for a in engine.allies(me):
        a.deadly += 1
def _warsong_defense(engine, me, foe):
    a = _best_attacker(engine.allies(me)) or me
    engine.initiative_shift(a, 2)

def _rebuttal_effect(engine, me, foe):
    prior = engine._prior_turn_hit
    if prior['hit'] and prior['actor'] in engine.enemies(me):
        apply_staggered(prior['actor'])
def _rebuttal_defense(engine, me, foe):
    engine.initiative_shift(foe, -1)

def _communion_effect(engine, me, foe):
    # Fixed 2026-07-24: was scrying immediately and unconditionally, no
    # deferred trigger at all. "If you are attacked before your next turn"
    # is the same shape as WEATHERED's own "each time you are attacked" —
    # a simple flag checked in attack() itself (engine.py, right next to
    # WEATHERED's check), not an unconditional same-turn effect.
    me._communion_active = True
def _communion_defense(engine, me, foe):
    for a in _team(engine, me):
        a.deadly += 1                      # you and allies gain Deadly

def _mirror_step_effect(engine, me, foe):
    for c in (me, foe):
        c.position = 'backline' if c.position == 'frontline' else 'frontline'

# ADAPT (Green), EQUAL FOOTING (Red), and CERTAINTY (Blue) below are the
# "wins ties" Special Rule family — vanilla otherwise, no effect/defense
# function needed at all. See engine.py's Card.wins_ties / Duel.rps().

# VOID's Effect ("Defender gains Sealed") unmodeled — no item-usage mechanic
# exists in the sim, same treatment as PREDICT/DISTRACT.
def _void_defense(engine, me, foe):
    if warded(foe):   # forced discard is a Debuff now, see STILLNESS above
        return
    reals = [i for i, c in enumerate(foe.hand) if not c.is_status]
    if reals:
        foe.discard.append(foe.hand.pop(engine.rng.choice(reals)))

def _acceptance_effect(engine, me, foe):
    n = len(me.hand)
    if n:
        me.discard.extend(me.hand)
        me.hand = []
        for _ in range(n):
            c = me.draw_one(engine.rng)
            if c:
                me.hand.append(c)
def _acceptance_defense(engine, me, foe):
    # "move position or gain Initiative Shift +1" simplified to the shift for
    # every ally — the choice a bot can't get wrong, unlike a reposition that
    # might walk an ally into worse range legality.
    for a in engine.allies(me):
        engine.initiative_shift(a, 1)

def _field_medicine_effect(engine, me, foe):
    allies = engine.allies(me)
    if not allies:
        return
    a = max(allies, key=lambda x: x.injuries_visible())
    if a.injuries_visible() > 0:
        remove_injuries(a)
        engine.heal(a, 3, source=me)
def _field_medicine_defense(engine, me, foe):
    if me.injuries_visible() > 0:
        remove_injuries(me)
    engine.heal(me, 3)

def _dead_reckoning_effect(engine, me, foe):
    apply_weak(foe)
def _dead_reckoning_defense(engine, me, foe):
    apply_blind(foe)

def _patience_dmg(engine, me, foe):
    bonus = 0 if getattr(me, '_attacked_last', False) else 4   # +4 if you waited
    return me.eff('soul') + roll(6, engine.rng) + _deadly_weak_bonus(engine.rng, me) + bonus
def _patience_defense(engine, me, foe):
    a = _most_hurt(engine.allies(me))
    if a:
        me.ongoing.append({'kind': 'patience_def', 'owner': me, 'anchor': me.position, 'target': a})


# ==================== Missing simple core cards (Patient Host deck-fill) =====
# None of these were ever wired to a roster deck before, so nobody caught the
# gap until building the Host's actual 24-card deck required all of them.

def _stillness_effect(engine, me, foe):
    # Fixed 2026-07-24: forced discard is now a Debuff, Ward-blockable
    # (rules/card-glossary.md, Debuff's scope expanded per Drew's direct call).
    if warded(foe):
        return
    reals = [i for i, c in enumerate(foe.hand) if not c.is_status]
    if reals:
        foe.discard.append(foe.hand.pop(engine.rng.choice(reals)))
_stillness_defense = _stillness_effect   # same text, target is just always foe here

def _focus_effect(engine, me, foe):
    engine.scry(me, me, 2)   # "returns to hand instead of discard" unmodeled — no engine hook for it
def _focus_defense(engine, me, foe):
    if me.discard:
        me.deck.append(me.discard.pop())   # top of discard -> top of deck (append = top, draws next)

def _understanding_dmg(engine, me, foe):
    # discard the played card's already gone from hand by this point (removed
    # at the top of attack()), so any index here is a genuinely different card
    # Base roll respects a held Deadly/Weak stack (_rolled_die); card text
    # reworded 2026-07-28 to drop "Deadly" (Drew's call, same reasoning as
    # TRACE above) — this is a flat conditional +1d6 on top when the discard
    # actually happens, independent of any held stack.
    base = me.eff('mind') + _rolled_die(8, engine.rng, me)
    if me.hand:
        me.discard.append(me.hand.pop(engine.rng.randrange(len(me.hand))))
        base += roll(6, engine.rng)
    return base
def _understanding_defense(engine, me, foe):
    engine.scry(me, me, 2)   # "heal 4 if you bottom both" unmodeled — needs scry-outcome introspection the engine doesn't expose

# ==================== 13 core cards found unregistered (2026-07-23 audit) ===
# Never wired to any roster deck, so never caught — same shape as the
# Patient-Host-deck-fill gap above, found this time by a systematic sweep of
# cards/*.md against content.py rather than a specific deck build surfacing it.

def _distract_effect(engine, me, foe):
    pass   # Sealed: item-usage gate, no item mechanic exists in the sim (PREDICT's own precedent)
def _distract_defense(engine, me, foe):
    foe._forced_target = me   # taunt, same mechanism as MOCKERY's defense

def _phase_logic_effect(engine, me, foe):
    me.evade += 1
def _phase_logic_defense(engine, me, foe):
    me.position = 'backline' if me.position == 'frontline' else 'frontline'   # "may" -> always, established convention

def _cliff_song_heal(engine, me, foe):
    engine.heal(me, 2)
    for a in engine.allies(me):
        engine.heal(a, 2)
_cliff_song_effect = _cliff_song_heal
_cliff_song_defense = _cliff_song_heal

def _dart_move(engine, me, foe):
    me.position = 'backline' if me.position == 'frontline' else 'frontline'   # "any position" -> toggle, no policy hook for a free choice
_dart_effect = _dart_move
_dart_defense = _dart_move

def _berserkers_price_dmg(engine, me, foe):
    return me.eff('body') + roll(8, engine.rng) + roll(8, engine.rng) + _deadly_weak_bonus(engine.rng, me)
def _berserkers_price_effect(engine, me, foe):
    me.cannot_defend = True   # until my own next turn (take_turn resets it) — the flag already existed, reserved, unused until now
def _berserkers_price_defense(engine, me, foe):
    # "next time you attack them" simplified to "their very next turn" — no
    # per-target future-restriction exists in the engine, and in practice
    # there's only ever one live attacker to simplify away from anyway.
    foe.cannot_defend = True

def _slip_the_blade_effect(engine, me, foe):
    me.evade += 1
def _slip_the_blade_defense(engine, me, foe):
    me.position = 'frontline'

def _grounding_stance_effect(engine, me, foe):
    me._grounded = True   # until my own next turn — checked by PUSH/PULL/CALCULATE/REPEL/NO VACANCY below.
    # NOT checked by MIRROR STEP, HEAVE AND HAUL, TRAMPLE's defensive push, or
    # Rushdown — threading a guard through every forced-reposition source in
    # the game was more than this pass covered; flagged here rather than
    # silently claiming full coverage.
def _grounding_stance_defense(engine, me, foe):
    me.resist += 1

def _sunder_effect(engine, me, foe):
    apply_stat_drain(foe, 'mind')
_sunder_defense = _sunder_effect

def _dead_heat_effect(engine, me, foe):
    if me._tie:   # DEAD HEAT-style cancel — engine.py's tie branch checks for exactly this
        foe._no_defensive_bonus = True
def _dead_heat_defense(engine, me, foe):
    engine.deal(foe, 4 if me._tie else 2, unpreventable=True)

def _attune_effect(engine, me, foe):
    reals = [i for i, c in enumerate(me.hand) if not c.is_status]
    if not reals:
        return
    discarded = me.hand.pop(engine.rng.choice(reals))
    me.discard.append(discarded)
    # Existing ongoing entries for the same color don't stack — refreshing
    # the color is enough; a second copy would double-count in
    # _resolve_attacker_win's lookup below.
    if not any(o.get('kind') == 'attune' and o.get('color') == discarded.color for o in me.ongoing):
        me.ongoing.append({'kind': 'attune', 'owner': me, 'color': discarded.color})
def _attune_defense(engine, me, foe):
    engine.deal(me, 2, unpreventable=True)
    for _ in range(2):
        c = me.draw_one(engine.rng)
        if c:
            me.hand.append(c)
    reals = [i for i, c in enumerate(me.hand) if not c.is_status]
    if reals:
        me.discard.append(me.hand.pop(engine.rng.choice(reals)))

def _bind_effect(engine, me, foe):
    apply_rooted(foe)
def _bind_defense(engine, me, foe):
    apply_rooted(foe)   # foe = attacker here, same convention as GORE's defense

def _read_effect(engine, me, foe):
    pass   # "defender must reveal their hand" — pure info, no state change (BREAK's own precedent)
def _read_defense(engine, me, foe):
    # "Name a color" has no real choice to make without a live opponent to
    # bluff against — picks whichever color the foe has actually shown most,
    # same heuristic ANTICIPATE-style cards already use elsewhere.
    if warded(foe):   # forced discard is a Debuff now, see STILLNESS above
        return
    color = foe.attack_history.most_common(1)[0][0] if foe.attack_history else None
    if color is None:
        return
    matches = [i for i, c in enumerate(foe.hand) if not c.is_status and c.color == color]
    if matches:
        foe.discard.append(foe.hand.pop(engine.rng.choice(matches)))

def _take_any_status(who):
    """Find and remove one status card (Injury or Exhaust) from hand or
    discard — whichever this combatant is holding. Returns the name found
    ('INJURY'/'EXHAUST') or None. Broadened 2026-07-24 (was Injury-in-hand
    only) per Drew's direct text: "transfer 1 status card from your hand or
    discard.\""""
    for zone in (who.hand, who.discard):
        for i, c in enumerate(zone):
            if c.is_status:
                name = c.name
                zone.pop(i)
                return name
    return None

def _give_status(engine, target, name):
    if name == 'INJURY':
        engine.insert_injury(target)
    elif name == 'EXHAUST':
        engine.insert_exhaust(target)

def _carried_injury_effect(engine, me, foe):
    # Ally-sourced — a genuine no-op in 1v1 (You Are Not Your Own Ally), same
    # footing as every other "from any ally" effect in this file. Correct in
    # team play: pulls from whichever ally is actually carrying a status card.
    # Ward checked BEFORE taking from source (not via _give_status itself) —
    # otherwise a Warded target would still cost the ally their card with
    # nothing transferred, silently destroying it instead of blocking the
    # whole transfer the way a Debuff being Warded should.
    source = next((a for a in engine.allies(me) if any(c.is_status for c in a.hand + a.discard)), None)
    if source is None or warded(foe):
        return
    name = _take_any_status(source)
    if name:
        _give_status(engine, foe, name)
def _carried_injury_defense(engine, me, foe):
    if warded(foe):   # foe = attacker here
        return
    name = _take_any_status(me)
    if name:
        _give_status(engine, foe, name)

def _endure_effect(engine, me, foe):
    me.resist += 1
def _endure_defense(engine, me, foe):
    engine.heal(me, 3)

def _weathered_effect(engine, me, foe):
    me._weathered = True   # heal 2 each time attacked, until my next turn (engine.attack() checks this)
def _weathered_defense(engine, me, foe):
    me.ward = True

def _recover_effect(engine, me, foe):
    c = me.draw_one(engine.rng)
    if c:
        me.hand.append(c)
    engine.heal(me, 3)
_recover_defense = _recover_effect   # identical text both sides

def _flow_effect(engine, me, foe):
    me.position = 'backline' if me.position == 'frontline' else 'frontline'
_flow_defense = _flow_effect

def _shade_away_effect(engine, me, foe):
    me.evade += 1
def _shade_away_defense(engine, me, foe):
    # New Defensive Bonus 2026-07-24 (was the MOCKERY-style forced-target
    # taunt, which had an unmodeled "rushdown if they cannot reach you"
    # clause anyway) — simple Gain Evade instead, matching the Effect side.
    me.evade += 1

# STARING CONTEST (Red) — genuinely built at last: "move to immediately
# follow a chosen token" is a direct requeue, not a numeric shift, so it
# needed its own engine hook (engine.reposition_after) distinct from
# Initiative Shift X. Mirror archetype, per its own unique pillar-touching
# mechanic — kept as-is rather than folded into WAITING GAME below.
def _staring_contest_effect(engine, me, foe):
    # "any target" simplified to the defender for the bot — same treatment
    # as every other "your choice of any combatant" card this session.
    engine.reposition_after(me, foe)
def _staring_contest_defense(engine, me, foe):
    engine.reposition_after(me, foe)

# Shared by WAITING GAME (Mirror: copy, leaves foe's own untouched) and
# DRAIN (Parasite: steal, actually removes it from foe) — same fixed check
# order (Deadly > Resist > Evade > Protect > Immune) either way, since a
# heuristic brain can't "choose" the way a real player would at the table; a
# real player picks freely among whatever's visible. Capped at however many
# statuses are actually present rather than duplicated — copying/stealing
# one Deadly twice isn't "two effects." Immune included per its membership in
# Positive Status Effects (card-glossary.md) and its structural kinship with
# Evade (both single-charge, expire on trigger) — placed last in priority so
# it doesn't disturb existing regression behavior for decks without it.
# Anchored and Quick are both skipped here (not by the same reasoning,
# though): Anchored lives in `ongoing`, not a simple flag; Quick is real now
# (OVERDRIVE, formerly OVERCOMMIT's own mechanic before the 2026-07-29
# split), just never asked to be copyable/stealable by either of these two
# cards specifically.
def _transfer_statuses(me, foe, count, steal):
    order = []
    if foe.deadly > 0:
        order.append('deadly')
    if foe.resist > 0:
        order.append('resist')
    if foe.evade > 0:
        order.append('evade')
    if getattr(foe, '_protect', False):
        order.append('protect')
    if foe.immune:
        order.append('immune')
    for kind in order[:count]:
        if kind == 'protect':
            me._protect = True
            if steal:
                foe._protect = False
        elif kind == 'immune':
            me.immune = True
            if steal:
                foe.immune = False
        else:
            setattr(me, kind, getattr(me, kind) + 1)
            if steal:
                setattr(foe, kind, getattr(foe, kind) - 1)

def _waiting_game_effect(engine, me, foe):
    _transfer_statuses(me, foe, 2, steal=False)
def _waiting_game_defense(engine, me, foe):
    _transfer_statuses(me, foe, 2, steal=False)

# DRAIN (Red) — Parasite's first card: real predation, not imitation.
# Steals exactly 1 Positive Status Effect the foe currently holds — removed
# from them, not just copied, the distinction Drew drew between Mirror
# ("imitates, takes nothing") and Parasite ("predates: drains, hijacks,
# steals") when the two archetypes were first named.
def _drain_effect(engine, me, foe):
    _transfer_statuses(me, foe, 1, steal=True)
def _drain_defense(engine, me, foe):
    _transfer_statuses(me, foe, 1, steal=True)

# Pure removal, no benefit to the caster — same fixed priority order as
# _transfer_statuses (Deadly > Resist > Evade > Protect > Immune), shared by
# UNMAKE and LEVEL THE FIELD below. Anchored/Quick skipped for the same
# reasons as _transfer_statuses.
def _strip_one_status(target, count=1):
    order = []
    if target.deadly > 0:
        order.append('deadly')
    if target.resist > 0:
        order.append('resist')
    if target.evade > 0:
        order.append('evade')
    if getattr(target, '_protect', False):
        order.append('protect')
    if target.immune:
        order.append('immune')
    for kind in order[:count]:
        if kind == 'protect':
            target._protect = False
        elif kind == 'immune':
            target.immune = False
        else:
            setattr(target, kind, getattr(target, kind) - 1)

# UNMAKE (Blue) — the biggest buff-removal in the game: wipes every
# Positive Status Effect from the target in one go, via the existing
# `remove_positive_status` helper (already used by TRACE) — and, Drew's
# explicit call, ignores Ward entirely. A real, deliberate exception to the
# established Debuff/Ward rule, same category as AFTERIMAGE bypassing Axiom
# or FRAME-TRAP bypassing RPS — flagged here, not incidental, since
# normally a Positive-Status-Effect removal is exactly the kind of thing
# Ward is supposed to stop (`warded()`'s own ruling text). Paid for with an
# Exhaust cost — 2 (reduced from 3, 2026-07-24, Drew's call), same as
# OVERDRIVE's (formerly OVERCOMMIT's own mechanic before the 2026-07-29
# split).
def _unmake_effect(engine, me, foe):
    remove_positive_status(foe)
    engine.insert_exhaust(me, 2)
def _unmake_defense(engine, me, foe):
    remove_positive_status(foe)
    engine.insert_exhaust(me, 2)

# LAST RESORT — Immunity (card-glossary.md): the actual negation logic
# lives once in both engines' attack(), checked before anything else is even
# revealed. This just sets the flag. Not added to the Positive Status
# Effects list — a deliberate, unconfirmed-until-asked scope limit, same
# footing as Critical: UNMAKE/LEVEL THE FIELD/WAITING GAME/DRAIN don't strip
# or copy it. (BARRIER, Immunity's other former source, was cut 2026-07-24 —
# Drew's call; LAST RESORT is now the only card that grants it.)

# Gene-Thief Tardigrade signature cards (bestiary/gene-thief-tardigrade.md) —
# echo the creature's own Genetic Absorption passive rather than duplicating
# it (that passive is prose-only, GM-ruled, not modeled here — no ROSTER
# entry for this creature, same footing as every other narrative-only
# bestiary kit). Synced on request alongside the rest of this session's new
# cards, not because it entered a tournament roster.
def _genetic_sample_effect(engine, me, foe):
    engine.scry(me, foe, 1)
def _genetic_sample_defense(engine, me, foe):
    me.evade += 1

def _adaptive_bite_effect(engine, me, foe):
    me.deadly += 1
def _adaptive_bite_defense(engine, me, foe):
    me.thorns += 1

def _dissolve_and_keep_effect(engine, me, foe):
    engine.heal(me, 2)
def _dissolve_and_keep_defense(engine, me, foe):
    engine.heal(me, 2)

def _last_resort_effect(engine, me, foe):
    if me.hp <= 6:
        me.immune = True
def _last_resort_defense(engine, me, foe):
    if me.hp <= 6:
        me.immune = True

# FORESEEN (Oracle starter deck, 2026-08-01) — plain unconditional Resist
# both sides, same shape as BRACE (Red)/PAIN IS FUEL (Red)'s bare grants.
# Built to fill a real, measured gap: Blue's Oracle-19 had no clean,
# unconditional self-Resist card (ALIGN's is conditional on a shared-color
# check) — checked via CARD_TAGS["keyword:resist:self"] before writing
# this, not assumed.
def _foreseen_effect(engine, me, foe):
    me.resist += 1
def _foreseen_defense(engine, me, foe):
    me.resist += 1

# OPEN GUARD / MARKED / OPENING (Oracle keyword-coverage pass, 2026-08-01) —
# one per color, plain unconditional Vulnerable on the foe both sides. Fills
# the starkest gap the outside-designer review found: Vulnerable was at
# zero anywhere in the Oracle-59, and checking further, zero anywhere in
# the whole 240-card pool except OVERCOMMIT's own deliberate self-exception
# (see apply_vulnerable's docstring). Same bare-grant shape as
# FORESEEN/STEADFAST — under-designed on purpose, matching the pool's own
# bar, not an oversight.
def _open_guard_effect(engine, me, foe):
    apply_vulnerable(foe)
def _open_guard_defense(engine, me, foe):
    apply_vulnerable(foe)

def _marked_effect(engine, me, foe):
    apply_vulnerable(foe)
def _marked_defense(engine, me, foe):
    apply_vulnerable(foe)

def _opening_effect(engine, me, foe):
    apply_vulnerable(foe)
def _opening_defense(engine, me, foe):
    apply_vulnerable(foe)

# UNBROKEN / UNTOUCHED (Oracle keyword-coverage pass, 2026-08-01) — same
# exact shape as LAST RESORT (Blue): "if your HP is 6 or less, gain
# Immunity," both sides. Immune was at 1 total across the whole Oracle-59
# (LAST RESORT itself, conditional) and zero in Red/Green specifically —
# matching LAST RESORT's own threshold exactly rather than picking a new,
# unexplained number.
def _unbroken_effect(engine, me, foe):
    if me.hp <= 6:
        me.immune = True
def _unbroken_defense(engine, me, foe):
    if me.hp <= 6:
        me.immune = True

def _untouched_effect(engine, me, foe):
    if me.hp <= 6:
        me.immune = True
def _untouched_defense(engine, me, foe):
    if me.hp <= 6:
        me.immune = True

# ATTRITION / REELING / FOOTWORK / BLINDSIDE (Red), RETORT / VEIL / DEAD END
# (Blue), BRISTLE / INSTINCT (Green) — Oracle keyword-coverage pass, second
# round, 2026-08-01: Weak, Staggered, Quick, and Blind were all at zero in
# Red; Thorns and Rooted at zero in Blue; Thorns and Ward at zero in Green.
# Every foe-debuff routes through the existing apply_weak/apply_staggered/
# apply_blind/apply_rooted helpers (Ward-respecting); every self-buff
# (Thorns, Quick, Ward) sets the attribute directly, matching how every
# other self-buff of the same keyword already does it in this file (Thorns:
# _pain_is_fuel_defense; Quick: _overdrive_payout; Ward: _deflect_effect) —
# Ward never blocks a self-application, so these correctly skip debuff().
def _attrition_effect(engine, me, foe):
    apply_weak(foe)
def _attrition_defense(engine, me, foe):
    apply_weak(foe)

def _reeling_effect(engine, me, foe):
    apply_staggered(foe)
def _reeling_defense(engine, me, foe):
    apply_staggered(foe)

def _footwork_effect(engine, me, foe):
    me._quick = True
def _footwork_defense(engine, me, foe):
    me._quick = True

def _blindside_effect(engine, me, foe):
    apply_blind(foe)
def _blindside_defense(engine, me, foe):
    apply_blind(foe)

def _retort_effect(engine, me, foe):
    me.thorns += 1
def _retort_defense(engine, me, foe):
    me.thorns += 1

def _veil_effect(engine, me, foe):
    apply_blind(foe)
def _veil_defense(engine, me, foe):
    apply_blind(foe)

def _dead_end_effect(engine, me, foe):
    apply_rooted(foe)
def _dead_end_defense(engine, me, foe):
    apply_rooted(foe)

def _bristle_effect(engine, me, foe):
    me.thorns += 1
def _bristle_defense(engine, me, foe):
    me.thorns += 1

def _instinct_effect(engine, me, foe):
    me.ward = True
def _instinct_defense(engine, me, foe):
    me.ward = True

# SMOKE SCREEN (Vescal signature, promoted to core and rebalanced — the AOE
# Blind on the whole enemy Frontline was the card's actual identity, so it
# stayed; the gating changed instead of the scope: minimum base die, melee
# only, clean-win-only (`me._tie` gate, same as YOU'RE NEXT), and it blinds
# its own caster too. `warded()` blocking that self-inflicted Blind is a
# real, deliberate extension of Ward's scope, not a silent reuse — Ward's
# own rule (card-glossary.md Debuff) only ever covers what an ENEMY applies
# to you; this is the first card where Ward blocks a status a combatant
# inflicts on themselves. Only the self-Blind is Ward-eligible — the
# Frontline enemies' Blind lands regardless of whether Ward fires.
def _smoke_screen_effect(engine, me, foe):
    if me._tie:
        return
    for e in engine.enemies(me):
        if e.position == 'frontline':
            e.blind += 1   # deliberately NOT apply_blind — lands regardless of Ward, see above
    apply_blind(me)
def _smoke_screen_defense(engine, me, foe):
    apply_blind(foe)

# STEADFAST (Oracle starter deck, 2026-08-01) — plain unconditional Resist
# both sides, same shape as FORESEEN (Blue) above. Same real, measured gap
# on the Green side: Green's Oracle-19 had zero self-Resist grants at all
# (RESONATE's is ally-only), checked via CARD_TAGS before writing this.
def _steadfast_effect(engine, me, foe):
    me.resist += 1
def _steadfast_defense(engine, me, foe):
    me.resist += 1

# LEVEL THE FIELD (Green) — the lighter, team-wide counterpart: strips
# exactly one Positive Status Effect (same fixed priority as WAITING GAME/
# DRAIN) from each enemy, respecting Ward normally (`warded()`, same
# pattern as TRACE) — unlike UNMAKE, this follows the established rule
# rather than breaking it. In a 1v1 Duel, `engine.enemies(me)` is just the
# one foe, same as everywhere else this pattern is used.
def _level_the_field_effect(engine, me, foe):
    for e in engine.enemies(me):
        if not warded(e):
            _strip_one_status(e, 1)
def _level_the_field_defense(engine, me, foe):
    for e in engine.enemies(me):
        if not warded(e):
            _strip_one_status(e, 1)

# EXPOSED (Blue) — the first card to grant Critical (new keyword,
# `rules/card-glossary.md`): doubles this attack's base damage (stat + die,
# including any Deadly/Weak already rolled into it) before any other bonus
# applies. Gated hard by design, not just by naming it and hoping: the
# trigger needs an already-Staggered target — real setup elsewhere, since
# Staggered doesn't just happen — and the base die is kept low (d2) so
# what's being doubled is small on its own; the whole payoff lives in the
# multiplier, not a separately-large base too.
def _exposed_damage(engine, me, foe):
    base = me.eff('mind') + _rolled_die(4, engine.rng, me)
    if foe.staggered:
        base *= 2
    return base
def _exposed_defense(engine, me, foe):
    me.evade += 1

# Mason Glyphs / Objects (cards/mason-glyphs.md) — the Sync pass. Every glyph
# just calls `engine.create_object`; the actual per-turn payout lives in
# `engine._object_tick`, called from both engines' `start_of_turn` alongside
# the existing green-ongoing tick. CIPHER's "gain Obscure" has no function
# here at all — see `_object_tick`'s own docstring for why (genuinely
# unmodeled, same footing as Reveal Hand, not a gap).
def _mending_glyph_effect(engine, me, foe):
    engine.create_object(me, 'mending')
def _mending_glyph_defense(engine, me, foe):
    engine.create_object(me, 'mending')

def _honing_glyph_effect(engine, me, foe):
    engine.create_object(me, 'honing')
def _honing_glyph_defense(engine, me, foe):
    engine.create_object(me, 'honing')

def _barbed_glyph_effect(engine, me, foe):
    engine.create_object(me, 'barbed')
def _barbed_glyph_defense(engine, me, foe):
    engine.create_object(me, 'barbed')

def _cipher_glyph_effect(engine, me, foe):
    engine.create_object(me, 'cipher')
def _cipher_glyph_defense(engine, me, foe):
    engine.create_object(me, 'cipher')

def _withering_glyph_effect(engine, me, foe):
    engine.create_object(me, 'withering')
def _withering_glyph_defense(engine, me, foe):
    engine.create_object(me, 'withering')

def _miring_glyph_effect(engine, me, foe):
    engine.create_object(me, 'miring')
def _miring_glyph_defense(engine, me, foe):
    engine.create_object(me, 'miring')

# CONSUME (Green) — Parasite's second card, the generic "destroy a card for
# power" seed Drew flagged and parked earlier ("just having the odds of
# hitting a stolen card happens are enough"), generalized to your own hand
# rather than requiring a stolen card specifically. Mandatory cost, not
# optional — matches SACRIFICE STRIKE's existing always-fires pattern, and
# needs no new "pay this or not" decision point in the engine. The
# Defensive Bonus rolls its own fresh counter-damage (same shape as
# SACRIFICE STRIKE's Counter Attack) so Lifesteal has something real to
# heal off on the defense side too — CONSUME's own printed Attack line
# only pays out automatically on the Effect side. Destruction is permanent
# — routed to `exile`, never `discard`, so it can't come back even on a
# mid-combat reshuffle; picked uniformly at random from the remaining
# hand, same convention FORGET already uses for "remove a card from hand."
def _consume_destroy(engine, me, foe):
    reals = [i for i, c in enumerate(me.hand) if not c.is_status]
    if reals:
        me.exile.append(me.hand.pop(engine.rng.choice(reals)))
        # Weak and Blind land together as one Debuff grant, not two separate
        # ones — a single Ward blocks both or neither, never just one.
        def _apply():
            foe.weak += 1
            foe.blind += 1
        debuff(foe, _apply)

def _consume_effect(engine, me, foe):
    engine.heal(me, me._last_hit)   # Lifesteal: full damage just dealt
    _consume_destroy(engine, me, foe)

def _consume_defense(engine, me, foe):
    dmg = me.eff('soul') + roll(6, engine.rng)
    engine.deal(foe, dmg, unpreventable=True)
    engine.heal(me, dmg)            # Lifesteal off this counter-hit
    _consume_destroy(engine, me, foe)

# BECOMING (colorless) — the Oracle-drafting card. Unmodeled beyond a safe
# zero-damage function, same treatment as PREDICT/VOID's item-usage gaps:
# the Oracle pool (`testcampaigndecks/oracle.md`) is a session-persistent,
# end-of-session table ritual — a GM-curated pool, a player draft, cards
# that carry across combats entirely outside this simulator's scope, which
# resets every deck between duels/battles and has no concept of a shared
# pool or cross-combat card identity. The 3-uses-then-permanently-destroyed
# counter is real but lives at the table (character sheet / testcampaign-
# decks file), not here — same reasoning as why HP-cost-until-next-rest was
# flagged (not built) earlier this session: state that survives past a
# single combat's end isn't this engine's job to track.
def _becoming_damage(engine, me, foe):
    return 0

# FOLLOW-UP (Mirror, colorless) — the second colorless card, and a stronger
# transformation than AFTERIMAGE's: this fully BECOMES a copy of whatever an
# ally most recently revealed (never itself — allies only, matching the
# WARSONG convention, so it's a guaranteed dead card in a 1v1 Duel, same as
# every other team-only card), before RPS resolution. Effect/Defensive Bonus
# are entirely replaced by the copied card's real functions once a target is
# found (engine.py's attack(), both engines) — but damage still needs its
# own function: with nothing to copy, `card` stays FOLLOW-UP's own native
# object (stat=None), and the reveal can still legitimately reach a damage
# roll on an uncontested win (Drew's colorless rule — it only loses when
# actually challenged). Unlike AFTERIMAGE, FOLLOW-UP has no printed formula
# of its own at all to fall back on, so an unresolved copy deals flat 0.
def _follow_up_damage(engine, me, foe):
    return 0

# AFTERIMAGE (Mirror) — colorless until revealed, per Drew's real-table
# reasoning: Axiom's ban applies at the moment of commitment, and this card
# genuinely hasn't chosen a color yet at that point, so no named-color ban
# can ever catch it. Registered with color=None and special_reveal=
# 'mirror_color'; engine._effective_color resolves it everywhere else color
# actually gets read (messaging, history, RPS) — never by mutating this
# Card object itself, since the same instance is shared across every deck
# that includes it. The stat mirrors along with the color (you're rolling
# their identity for this one exchange, not half of it), so damage needs
# its own function rather than the default me.eff(self.stat) lookup. No
# Green fallback (Drew's correction: colorless stays colorless, same as
# FOLLOW-UP) — but this CAN still be called with nothing to mirror, on an
# uncontested win (no defense, or the defender collapsed/staggered): Drew's
# rule is that colorless only loses when actually challenged by a real
# color, not automatically, so the reveal itself can still succeed. With no
# identity to mirror, there's no stat bonus either — just the bare d4.
def _afterimage_damage(engine, me, foe):
    # Bonus catch, same class as ROLLOUT/GORE above, found by re-grepping
    # every `_*_damage` function rather than trusting the earlier `_*_dmg`-
    # only sweep. Not one of the 12 coreset findings (this is a Mirror
    # signature card) — fixed anyway since it's the identical one-line gap.
    color = engine._prior_turn_hit.get('color')
    if color is None:
        return _rolled_die(6, engine.rng, me)
    stat = COLOR_TO_STAT[color]
    return me.eff(stat) + _rolled_die(6, engine.rng, me)

def _afterimage_effect(engine, me, foe):
    apply_blind(foe)
def _afterimage_defense(engine, me, foe):
    me.evade += 1


# ==================== The Patient Host — boss signature cards ================

def _your_turn_will_come_effect(engine, me, foe):
    engine.initiative_shift(foe, -2)
def _your_turn_will_come_defense(engine, me, foe):
    engine.initiative_shift(foe, -2)   # foe = the attacker, from a defense call

def _registered_effect(engine, me, foe):
    # the Host reads the target's own top 2 — "the ledger already knew" — and
    # whatever the policy would have sent to discard gets struck from the book
    # instead: exiled, not just re-filed, so it doesn't come back before combat ends
    engine.scry(me, foe, 2, bin_to=foe.exile)
def _registered_defense(engine, me, foe):
    me.ward = True

def _no_vacancy_effect(engine, me, foe):
    if not foe._grounded:   # GROUNDING STANCE
        foe.position = 'backline'
def _no_vacancy_defense(engine, me, foe):
    me.resist += 2

def _ledger_effect(engine, me, foe):
    me.ongoing.append({'kind': 'ledger', 'owner': me, 'anchor': me.position})
def _ledger_defense(engine, me, foe):
    c = me.draw_one(engine.rng)
    if c:
        me.hand.append(c)

# SEED (Cultivator) — tempo-as-a-resource, the first card in this shape:
# telegraphed, invests now for a bigger payoff later, no counter to track —
# plants at the caster's current position and pays out the next time THEY
# begin a turn still standing there (engine._ongoing_support_tick), however
# many turns that takes. Moving off the position (or being forced off it)
# just delays the payout, doesn't cancel it — Position is a real lever
# against this card, not just killing/Warding the caster first (Ward is
# irrelevant here regardless: this is a positive self-buff, never a debuff,
# and never applied by anyone else, so it was never in Ward's scope at all).
# Effect and Defensive Bonus plant the same way, different payoff each —
# "plant" is flavor, not a fictional action that needs the Effect side's
# exclusive timing; nothing stops narrating the Defensive Bonus as dropping
# the seed as part of the block itself. Briefly renamed to STAKE over a
# too-plant-specific-flavor concern, then reverted the same session — Drew,
# on reflection: keep it flavored, promote/de-flavor later if it earns a
# spot in a broader "candidates for core-agnostic reuse" pass, the same
# process as the bestiary promotion batch, not a pre-emptive strip.
def _seed_effect(engine, me, foe):
    me.ongoing.append({'kind': 'seed_deadly', 'owner': me, 'anchor': me.position})
def _seed_defense(engine, me, foe):
    me.ongoing.append({'kind': 'seed_resist', 'owner': me, 'anchor': me.position})

# EMERGENCY REPAIRS (Gambler-adjacent — same "cost lands on your own next
# turn" shape as BERSERKER'S PRICE, paid in a skipped draw instead of a
# defense window) — Red on its face (Body + d4 attack), but the heal
# reaches across to Soul specifically: Drew's own read, "now it's really
# revealing where the cards want to touch other colors" — a card's printed
# color/stat governs its own Attack roll, nothing stops its Effect text
# from reading a different stat outright.
def _emergency_repairs_payout(engine, me, foe):
    engine.heal(me, 2 * me.eff('soul'))
    me._skip_draw_next = True

def _emergency_repairs_effect(engine, me, foe):
    _emergency_repairs_payout(engine, me, foe)
def _emergency_repairs_defense(engine, me, foe):
    _emergency_repairs_payout(engine, me, foe)

# OVERDRIVE (Gambler; was OVERCOMMIT's own mechanic until 2026-07-29 —
# Drew's call, "OVERCOMMIT is just... too much rn," split into two cards:
# this one keeps the original buff-bundle-for-Exhaust idea, OVERCOMMIT
# itself became a plain strong attack, below) — the archetype's actual
# thesis: a huge upfront swing (all four Positive Status Effects at once)
# paid for with Exhaust, which costs a full future action to ever clear
# (rules/card-glossary.md, EXHAUST) rather than costing HP or a single
# hand card the way every other cost mechanic shipped this session does.
# First card ever to grant Quick — see engine.py's Duel.take_turn for how
# the free reposition actually resolves.
def _overdrive_payout(engine, me, foe):
    me.deadly += 1
    me.resist += 1
    me._quick = True
    me.evade += 1
    engine.insert_exhaust(me, 2)

def _overdrive_effect(engine, me, foe):
    _overdrive_payout(engine, me, foe)
def _overdrive_defense(engine, me, foe):
    _overdrive_payout(engine, me, foe)

# OVERCOMMIT (Gambler) — redesigned 2026-07-29 (Drew's call) from the
# buff-bundle above (moved to OVERDRIVE) into what he described as "a
# strong attack that self inflicts vulnerable." Self-cost lives on the
# Attack line via damage=, same convention as SACRIFICE STRIKE's own "Pay
# 3 HP" — applies only on a win (damage= never fires on a tie), not
# unconditionally regardless of outcome.
def _overcommit_dmg(engine, me, foe):
    me.vulnerable += 1
    return me.eff('body') + _rolled_die(10, engine.rng, me)

# ==================== Bestiary promotions to core =============================
# First batch, per the bestiary-card audit — de-flavored, mechanics unchanged
# unless noted. Each creature's own card file gets a superseded-by note
# rather than duplicating the text twice.

# CERTAIN CONTACT (was NEVER LIFTED, Wall-Reader) — Drew's addition on
# promotion: also ignores Resist and Blind, not just Evade. `ignores` is a
# small, generic Card-level property (checked directly at the Blind/Evade
# checks in attack() and the Resist reduction in deal()) rather than a new
# keyword, since this describes the ATTACK itself, not a status granted to
# anyone.
def _certain_contact_defense(engine, me, foe):
    me.resist += 1

# HEAVE AND HAUL (was TUNNEL KNOWLEDGE, Borrower) — Effect always targets
# Backline (no policy has real "which position" decision logic to make this
# a genuine choice with, so the more generally useful default stands in,
# same simplification shape as Quick's own free action). Defensive Bonus
# reuses Quick's exact mechanism for "may change position freely" instead of
# an immediate auto-flip — a real free reposition on everyone's own next
# turn, not a forced one right now.
def _heave_and_haul_effect(engine, me, foe):
    for e in engine.enemies(me):
        if e.position == 'backline':
            e.position = 'frontline'
def _heave_and_haul_defense(engine, me, foe):
    for a in [me] + engine.allies(me):
        a._quick = True

# HEAVE / HAUL (Lefty, `cards/lefty.md`) — 2026-08-01, replacing Lefty's own
# HOOK AND HAUL (a single card that pulled everyone to him / pushed everyone
# away). Drew's original description, confirmed directly rather than
# assumed after the record showed HEAVE AND HAUL above was never actually
# Lefty's despite the shared name: HEAVE throws the whole enemy Frontline
# back, HAUL drags the whole enemy Backline in — two unconditional, forced,
# single-direction cards instead of one card doing both. Not team_only:
# engine.enemies(me) always includes the current 1v1 foe too, unlike the
# ally-referencing cards that tag actually covers.
def _heave_effect(engine, me, foe):
    for e in engine.enemies(me):
        if e.position == 'frontline':
            e.position = 'backline'
_heave_defense = _heave_effect

def _haul_effect(engine, me, foe):
    for e in engine.enemies(me):
        if e.position == 'backline':
            e.position = 'frontline'
_haul_defense = _haul_effect

# AEGE (Carrion Guide, `cards/aege.md`) — 2026-08-01, built per Drew's direct
# request: stat and deck her, CTR 13-17. Reads the field before committing to
# anything, same instinct that has her reading a traveler's tells before she
# agrees to guide them (`characters/aege.md`, Voice/What She Does). Deliberately
# not aggressive — control and information over damage, matching a guide who
# isn't built to win a fight through force. WHERE IT'S GATHERING is her GM
# Secret in disguise: plays as plain information-gathering, its printed text
# never says why she always seems to know which way a fight is about to go.
def _watches_feet_effect(engine, me, foe):
    if foe.position == 'backline':
        apply_weak(foe)
def _watches_feet_defense(engine, me, foe):
    engine.scry(me, me, 1)

def _known_ground_effect(engine, me, foe):
    me.position = 'backline' if me.position == 'frontline' else 'frontline'
    a = _best_attacker(engine.allies(me))
    if a:
        a.position = 'backline' if a.position == 'frontline' else 'frontline'
def _known_ground_defense(engine, me, foe):
    me.position = 'backline' if me.position == 'frontline' else 'frontline'
    me.evade += 1

def _where_its_gathering_effect(engine, me, foe):
    engine.scry(me, foe, 2)
def _where_its_gathering_defense(engine, me, foe):
    engine.scry(me, me, 1)
    if me.hp <= 6:
        me.ward = True

# RHYTHM BREAK (was YOU CHANGED WALLS, Wall-Reader; briefly TELLS — renamed
# again, "isn't gonna work," per Drew) — reworked on promotion, not just
# renamed. Effect uses "moved" (Drew's own call, the cleaner phrasing) via
# the new `_repositioned_since_last_turn` tracker (built for this and
# ROLLOUT below — first time "did X reposition since their last turn" has
# ever been tracked in the sim). Defensive Bonus is a genuinely new
# condition: gain Resist if the ATTACKER received a positive Initiative
# Shift or used Wait since their own last turn. Implementation note, flagged
# rather than silently assumed: "since your last turn" reads most literally
# as bound to the DEFENDER's own timeline, but the two new flags
# (`_shifted_positive`, `_used_wait`) are self-clearing on the AFFECTED
# combatant's own next turn (same shape as `_anticipating`/`_weathered`) —
# a materially simpler, self-contained approximation of the same intent,
# not a literal cross-combatant timeline comparison.
def _rhythm_break_dmg(engine, me, foe):
    # Fixed 2026-07-24: text said "this attack gains Deadly" (immediate) but
    # the old effect= version did `me.deadly += 1`, deferring it to a future
    # roll — disagreed with its own card text. Made immediate instead of
    # rewriting the text at the time, for consistency with TRACE/UNDERSTANDING.
    # Card text reworded 2026-07-28 to drop "Deadly" entirely (Drew's call) —
    # this was always a flat conditional +1d6, never the stackable keyword.
    base = me.eff('body') + _rolled_die(8, engine.rng, me)
    if foe._repositioned_since_last_turn:
        base += roll(6, engine.rng)
    return base
def _rhythm_break_defense(engine, me, foe):
    if foe._shifted_positive or foe._used_wait:
        me.resist += 1

# STILL COUNTING (Wall-Reader, `cards/wall-reader.md`) — found unregistered
# entirely (2026-07-29 dice-pass audit): real canon text, never wired into
# the sim. Unlike RHYTHM BREAK/CERTAIN CONTACT, Wall-Reader's other two
# cards, this one wasn't promoted to core — stays a signature card here.
# "Have not changed position this combat" is cumulative, not a one-turn
# window like RHYTHM BREAK's `_repositioned_since_last_turn` — needed the
# new `_ever_repositioned` tracker (engine.py's Combatant, set in both
# engines' take_turn). Same base-roll/bonus-die split as TRACE: the base d6
# respects a held Deadly/Weak stack via `_rolled_die`, the +1d6 bonus is an
# independent second die via plain `roll()`, not routed through the stack.
def _still_counting_dmg(engine, me, foe):
    base = me.eff('soul') + _rolled_die(6, engine.rng, me)
    if not me._ever_repositioned:
        base += roll(6, engine.rng)
    return base
def _still_counting_defense(engine, me, foe):
    me.resist += 1

# IRON GRIP (was CORRECTION GRIP, Alignment Marshal) — unchanged mechanically.
def _iron_grip_effect(engine, me, foe):
    apply_rooted(foe)
def _iron_grip_defense(engine, me, foe):
    me.ongoing.append({'kind': 'anchor_heal', 'owner': me, 'anchor': me.position, 'amount': 2})

# PATIENCE OF STONE (Delve Roller / Stonecoil, identical in both files —
# proven twice already) — Defensive Bonus stays an unconditional Deadly
# grant per Drew ("maybe that's okay though"). Heal bumped 2 -> 5, 2026-07-24.
def _patience_of_stone_effect(engine, me, foe):
    me.ongoing.append({'kind': 'anchor_heal', 'owner': me, 'anchor': me.position, 'amount': 5})
def _patience_of_stone_defense(engine, me, foe):
    me.deadly += 1

# Stonecoil's remaining signature cards (`cards/stonecoil-hollow.md`) — built
# to actually test the Rodent Burrow Basin fight rather than eyeball its
# difficulty. DRAG's own conditional reads foe.position before its Effect
# can change it — damage() runs before effect() in both engines' attack(),
# confirmed by reading the call order, not assumed.
def _drag_effect(engine, me, foe):
    if foe.position != 'frontline':
        foe.position = 'frontline'
def _drag_damage(engine, me, foe):
    base = me.eff('body') + _rolled_die(6, engine.rng, me)
    if foe.position == 'frontline':
        base += 2
    return base
def _drag_defense(engine, me, foe):
    apply_rooted(foe)

def _vibration_lock_effect(engine, me, foe):
    seen = engine.scry(me, foe, 1)
    if seen and foe.last_color is not None and seen[0].color == foe.last_color:
        apply_blind(foe)
def _vibration_lock_defense(engine, me, foe):
    engine.scry(me, me, 1)

def _shed_skin_effect(engine, me, foe):
    remove_injuries(me, 1)
    me.evade += 1
def _shed_skin_defense(engine, me, foe):
    if me.discard:
        me.exile.append(me.discard.pop())

def _dark_corridor_effect(engine, me, foe):
    apply_blind(foe)
def _dark_corridor_defense(engine, me, foe):
    me.resist += 1

def _coil_latch_damage(engine, me, foe):
    base = me.eff('body') + _rolled_die(6, engine.rng, me)
    if foe._repositioned_since_last_turn:
        base += 2
    return base
def _coil_latch_defense(engine, me, foe):
    apply_rooted(foe)

def _still_ground_effect(engine, me, foe):
    if foe._repositioned_since_last_turn:
        engine.scry(me, me, 1)
def _still_ground_damage(engine, me, foe):
    base = me.eff('mind') + _rolled_die(4, engine.rng, me)
    if foe._repositioned_since_last_turn:
        base += 1
    return base
def _still_ground_defense(engine, me, foe):
    engine.scry(me, me, 1)

# PULL/PUSH (core, cards/red-body.md) — a real, separate gap found while
# building the above: these two plain repositioning cards were never
# registered at all, Stonecoil signature or not.
def _pull_effect(engine, me, foe):
    if not foe._grounded:   # GROUNDING STANCE
        foe.position = 'frontline'
def _pull_defense(engine, me, foe):
    if not foe._grounded:
        foe.position = 'frontline'

def _push_effect(engine, me, foe):
    if not foe._grounded:   # GROUNDING STANCE
        foe.position = 'backline'
def _push_defense(engine, me, foe):
    if not foe._grounded:
        foe.position = 'backline'

# ROLLOUT (Delve Roller) — the Pokemon reference, made real: returns
# straight to hand after use (`returns_to_hand=True` on the Card itself)
# instead of ever sitting in discard. Fixed 2026-07-24: text used to say
# "regardless of outcome" — cut, since a reveal that lost the RPS exchange
# shouldn't get to keep the card; `_correct_return_on_loss` (engine.py)
# moves it to discard instead once the outcome is actually known. Needs its
# own damage function since the +4 bonus is conditional; reuses the same
# `_repositioned_since_last_turn` tracker as RHYTHM BREAK, just checking
# yourself instead of the target.
def _rollout_damage(engine, me, foe):
    # Fixed 2026-07-24: named `_rollout_damage`, not `_rollout_dmg` — missed
    # in the first Deadly/Weak-stack sweep because the search only matched
    # the `_*_dmg` naming pattern.
    base = me.eff('body') + roll(4, engine.rng) + _deadly_weak_bonus(engine.rng, me)
    if not me._repositioned_since_last_turn:
        base += 4
    return base
def _rollout_defense(engine, me, foe):
    me.resist += 1

# SEISMIC REDIRECT (Alignment Marshal) — the first core card to grant
# Rushdown for real (see engine.py's `_rushdown`, a genuine structural gap
# closed this session: fully defined as a table action, referenced by name
# in several bestiary cards, implemented nowhere until now).
def _seismic_redirect_effect(engine, me, foe):
    _rushdown(me, foe)
def _seismic_redirect_defense(engine, me, foe):
    # Counter Attack always means this card's own stat + die (Body + d6,
    # this card's printed Attack) — Counter Attack no longer has a
    # separate "stated die" form at all (card-glossary.md, simplified
    # 2026-07-24). Card text is bare "Counter Attack," no die restated.
    engine.deal(foe, me.eff('body') + roll(6, engine.rng), unpreventable=True)

# GORE (Minotaur) — base die bumped along with everything else.
def _gore_damage(engine, me, foe):
    # Fixed 2026-07-24: same naming-pattern miss as ROLLOUT above.
    base = me.eff('body') + roll(8, engine.rng) + _deadly_weak_bonus(engine.rng, me)
    if foe.position == 'frontline':
        base += roll(6, engine.rng)
    return base
def _gore_defense(engine, me, foe):
    apply_rooted(foe)

def _youre_next_effect(engine, me, foe):
    # Promoted to core: Drew's tweak — only a clean win, not a tie
    # (`attacker._tie` is set True only while an Effect resolves during a
    # tie, engine.py's rps()/tie branch).
    if me._tie:
        return
    engine.initiative_shift(me, 2)
def _youre_next_defense(engine, me, foe):
    engine.deal(foe, 3, unpreventable=True)

# TABLE STAKES (Gambler archetype, core Red) — discard 1 random card from
# your own hand (any card, status cards included — discarding an Injury this
# way is a fine outcome, not excluded the way CONSUME excludes them from its
# own "destroy for value" cost); the discarded card's own printed color
# decides what happens. Colorless discards (FOLLOW-UP, BECOMING) or an empty
# hand simply whiff — the gamble doesn't always pay off.
def _table_stakes_effect(engine, me, foe):
    if not me.hand:
        return
    idx = engine.rng.choice(range(len(me.hand)))
    discarded = me.hand.pop(idx)
    me.discard.append(discarded)
    if discarded.color == 'R':
        engine.deal(foe, 4, unpreventable=True)
    elif discarded.color == 'B':
        apply_staggered(foe)
    elif discarded.color == 'G':
        engine.heal(me, 3)
        for ally in engine.allies(me):
            engine.heal(ally, 3)
def _table_stakes_defense(engine, me, foe):
    me.resist += 1

# DOUBLE DOWN (Gambler archetype, core Red) — wired into the sim 2026-07-23 on
# Drew's direct request, after having been shipped as canon-text-only pending
# playtesting. On a clean win only (never a tie — matches SMOKE SCREEN/YOU'RE
# NEXT's `me._tie` gate precedent), immediately makes a second attack against
# the same defender using another legal card from hand — a genuine same-turn
# bonus attack, outside normal turn structure, which is exactly why this needed
# real design attention before being trusted in the sim. Guarded against
# chaining: `_double_down_active` is set for the duration of the bonus attack,
# and the effect refuses to fire again while it's set — so if the second card
# is ALSO Double Down and ALSO wins clean, it does not trigger a third attack.
# Caps the whole chain at exactly one bonus hit, regardless of hand contents.
# Deliberately does NOT gate on the defender being Collapsed (only on already
# being dead, since there's no legal target left) — a clean win into an
# already-Collapsed defender can be the second of the two hits the death rule
# requires, which reads as a real, intended "finish them" moment for this card
# rather than an edge case to suppress. Card selection mirrors the shape of
# `legal_attacks`/`legal_attacks_team` (policies.py/team_policies.py) without
# importing either — content.py sits below the policy layer in the dependency
# graph on purpose, so this reimplements the same legality check locally via
# engine.py's shared `can_attack`, then picks the single highest stat+die card
# available, a simple stand-in for "the attacker's own best next play" rather
# than routing through a specific policy's full valuation logic.
def _double_down_effect(engine, me, foe):
    if me._tie:
        return
    if getattr(me, '_double_down_active', False):
        return
    if foe.is_dead:
        return
    legal = [c for c in me.hand if not c.is_status and can_attack(me, foe, c)]
    if not legal:
        return
    card2 = max(legal, key=lambda c: me.eff(c.stat) + (c.base_die or 6))
    me._double_down_active = True
    try:
        engine.attack(me, foe, card2)
    finally:
        me._double_down_active = False
def _double_down_defense(engine, me, foe):
    engine.initiative_shift(foe, -1)


# BRIARWATCH JACKALOPE signature cards (`cards/briarwatch-jackalope.md`) —
# registered for the first time 2026-07-28, for the party-vs-3-Jackalopes
# test Drew asked for. Teaching-encounter identity (constant repositioning,
# low HP, quick fights) translated directly rather than left unmodeled, since
# the whole point of this creature is testing positioning/Rushdown.
def _bolt_effect(engine, me, foe):
    me.position = 'backline'
_bolt_defense = _bolt_effect

def _nip_dmg(engine, me, foe):
    base = me.eff('body') + _rolled_die(6, engine.rng, me)
    if me.position == 'backline':
        base += 2
    return base
# Defensive Bonus: None — no defense function registered.

# FREEZE (2026-07-28): one card, shared by Briarwatch Jackalope AND Flapjack
# Octopus (`cards/briarwatch-jackalope.md`, `cards/flapjack-octopus.md`) —
# Drew's direct call, same shape as PATIENCE OF STONE being identical across
# Delve Roller and Stonecoil. Not a name collision needing two registrations;
# one definition correctly serves both creatures' decks. Scry bumped 1->2 to
# match both files.
def _jackalope_freeze_effect(engine, me, foe):
    engine.scry(me, me, 2)
def _jackalope_freeze_defense(engine, me, foe):
    me.evade += 1

def _quickstep_effect(engine, me, foe):
    # "Move to any position" — no real choice logic for a bot to make this
    # decision with, so a simple deterministic toggle stands in (same
    # simplification shape as MIRROR STEP's identical toggle), not a real
    # optimization.
    me.position = 'backline' if me.position == 'frontline' else 'frontline'
_quickstep_defense = _quickstep_effect


# ============================ REGISTRY =======================================

def build_cards():
    C = {}

    def add(*a, **k):
        c = Card(*a, **k)
        C[c.name] = c

    # Frost — Red
    add("SACRIFICE STRIKE", 'R', 'body', 'melee', 10,
        damage=_sacrifice_strike_dmg, defense=_sacrifice_strike_defense)
    add("BLOOD IN THE GAP", 'R', 'body', 'ranged', 4,
        effect=_blood_in_the_gap_effect, defense=_blood_in_the_gap_defense)
    add("BURN BRIGHT", 'R', 'body', 'ranged', 8, damage=_burn_bright_dmg, defense=_burn_bright_defense)
    add("SPARK OF VIOLENCE", 'R', 'body', 'melee', 6,
        effect=_spark_effect, defense=_spark_effect)
    # Frost — Blue
    add("AXIOM", 'B', 'mind', 'ranged', 4, effect=_axiom_effect, defense=_axiom_defense)
    add("DEFLECT", 'B', 'mind', 'melee', 6,
        effect=_deflect_effect, defense=_deflect_defense)
    add("REALIGNMENT", 'B', 'mind', 'both', 6, effect=_realignment_effect, defense=_realignment_defense)
    add("CLIMB", 'B', 'mind', 'ranged', 6, effect=_climb_effect, defense=_climb_defense)
    add("FRACTURE", 'B', 'mind', 'ranged', 6,
        damage=_fracture_dmg, effect=_fracture_effect, defense=_fracture_defense)
    add("TRACE", 'B', 'mind', 'ranged', 6, damage=_trace_dmg, defense=_trace_defense)
    # Frost — Green
    add("TWIN STRIKE", 'G', 'soul', 'melee', None, damage=_twin_strike_dmg,
        defense=_twin_strike_defense)

    # Steele — Red
    add("BLOOD TITHE", 'R', 'body', 'both', 6,
        effect=_blood_tithe_effect, defense=_blood_tithe_defense)
    add("BRACE", 'R', 'body', 'melee', 4, effect=_brace_effect, defense=_brace_defense)
    add("GAMBLER'S RUIN", 'R', 'body', 'melee', None,
        damage=_gamblers_ruin_dmg, defense=_gamblers_ruin_defense)
    add("REPEL", 'R', 'body', 'melee', 4,
        effect=_repel_effect, defense=_repel_effect)
    add("PAIN IS FUEL", 'R', 'body', 'melee', 6,   # d6 -> d4 rebalance
        effect=_pain_is_fuel_effect, defense=_pain_is_fuel_defense)
    # Steele — Blue
    add("FORGET", 'B', 'mind', 'ranged', 4,
        effect=_forget_effect, defense=_forget_defense)
    add("PARADOX", 'B', 'mind', 'ranged', 6,
        effect=_paradox_effect, defense=_paradox_defense, special_reveal='paradox')
    add("ALIGN", 'B', 'mind', 'ranged', 6,
        effect=_align_effect, defense=_align_defense)
    add("ANTICIPATE", 'B', 'mind', 'melee', 6, effect=_anticipate_effect, defense=_anticipate_defense)
    # Steele — Green
    add("RENEWAL", 'G', 'soul', 'both', 4,
        effect=_renewal_effect, defense=_renewal_defense)

    # Mire — Green
    add("BALANCE", 'G', 'soul', 'ranged', 4,
        effect=_balance_effect, defense=_balance_defense)
    add("WITHER", 'G', 'soul', 'ranged', 6,
        effect=_wither_effect, defense=_wither_effect)
    add("MOCKERY", 'G', 'soul', 'ranged', 6,
        effect=_mockery_effect, defense=_mockery_defense)
    # Mire — Red
    add("REND", 'R', 'body', 'melee', 6,
        effect=_rend_effect, defense=_rend_defense)
    add("EQUAL FOOTING", 'R', 'body', 'melee', 8, wins_ties=True)   # Special Rule, vanilla otherwise
    add("PRESS THE INJURY", 'R', 'body', 'melee', 6,
        damage=_press_the_injury_dmg, defense=_press_the_injury_defense)
    add("DIG IN", 'R', 'body', 'melee', 4, effect=_dig_in_effect, defense=_dig_in_defense)
    # Mire — Blue
    add("PARTITION", 'B', 'mind', 'ranged', 4,
        effect=_partition_effect, defense=_partition_defense)
    add("UNNAME", 'B', 'mind', 'ranged', 4, effect=_unname_effect, defense=_unname_defense)
    add("SLIPSTREAM", 'B', 'mind', 'both', 4, effect=_slipstream_effect, defense=_slipstream_defense)
    add("TAINT", 'B', 'mind', 'ranged', 4,
        effect=_taint_effect, defense=_taint_defense)
    add("ERODE", 'B', 'mind', 'ranged', 6,
        effect=_erode_effect, defense=_erode_effect)

    # Green support kit (team play)
    add("RESONATE", 'G', 'soul', 'ranged', 4,
        effect=_resonate_effect, defense=_resonate_defense)
    add("SUPPORT", 'G', 'soul', 'ranged', 4,
        effect=_support_effect, defense=_support_defense)
    add("WITNESS", 'G', 'soul', 'melee', 4,
        effect=_witness_effect, defense=_witness_defense)
    add("SHARED BURDEN", 'G', 'soul', 'both', 8,
        effect=_shared_burden_effect, defense=_shared_burden_defense)

    # --- Expanded set: Red ---
    add("STRIKE", 'R', 'body', 'melee', 10, defense=_strike_defense)
    add("GUARD", 'R', 'body', 'melee', 4, effect=_guard_effect, defense=_guard_defense)
    add("INTERCEPT", 'R', 'body', 'melee', 4,
        effect=_intercept_effect, defense=_intercept_defense)
    add("RALLY", 'R', 'body', 'both', 4, effect=_rally_effect, defense=_rally_defense)
    add("TRAMPLE", 'R', 'body', 'melee', 6,
        effect=_trample_effect, defense=_trample_defense)
    add("BREAK", 'R', 'body', 'melee', 6, defense=_break_defense)
    add("CHARGE", 'R', 'body', 'melee', 6, effect=_charge_move, defense=_charge_move)
    # --- Expanded set: Blue ---
    add("INTERRUPT", 'B', 'mind', 'ranged', 4,
        effect=_interrupt_effect, defense=_interrupt_defense)
    add("SHARPEN", 'B', 'mind', 'both', 4, effect=_sharpen_effect, defense=_sharpen_defense)
    add("CHAIN", 'B', 'mind', 'ranged', 4, effect=_chain_effect, defense=_chain_defense)
    add("CALCULATE", 'B', 'mind', 'ranged', 8,
        effect=_calculate_effect, defense=_calculate_defense)
    add("STUDY", 'B', 'mind', 'ranged', 4, effect=_study_effect, defense=_study_defense)
    add("PROFILE", 'B', 'mind', 'ranged', 6, effect=_profile_effect, defense=_profile_defense)
    add("REFRACT", 'B', 'mind', 'ranged', 4,
        effect=_refract_effect, defense=_refract_defense)
    # --- Expanded set: Green ---
    add("SYNCHRONY", 'G', 'soul', 'both', 4,
        effect=_synchrony_effect, defense=_synchrony_defense)
    add("ROOTED OATH", 'G', 'soul', 'both', 6,
        effect=_rooted_oath_effect, defense=_rooted_oath_defense)
    add("URGENCY", 'G', 'soul', 'melee', 6,
        effect=_urgency_effect, defense=_urgency_defense)
    add("DELAY", 'G', 'soul', 'ranged', 8, effect=_delay_effect, defense=_delay_defense)
    add("COMMUNION", 'G', 'soul', 'ranged', 4,
        effect=_communion_effect, defense=_communion_defense)
    add("MIRROR STEP", 'G', 'soul', 'both', 6, effect=_mirror_step_effect)
    add("PATIENCE", 'G', 'soul', 'melee', None,
        damage=_patience_dmg, defense=_patience_defense)

    # Missing simple core cards (Patient Host deck-fill)
    add("STILLNESS", 'B', 'mind', 'ranged', 6,
        effect=_stillness_effect, defense=_stillness_defense)
    add("PREDICT", 'B', 'mind', 'melee', 8)   # Sealed unmodeled — no item-usage mechanic exists in the sim
    add("FOCUS", 'B', 'mind', 'ranged', 6, effect=_focus_effect, defense=_focus_defense)
    add("UNDERSTANDING", 'B', 'mind', 'ranged', 8,
        damage=_understanding_dmg, defense=_understanding_defense)

    # 13 more core cards found unregistered (2026-07-23 text-vs-sim audit)
    add("DISTRACT", 'B', 'mind', 'ranged', 6, effect=_distract_effect, defense=_distract_defense)
    add("PHASE LOGIC", 'B', 'mind', 'both', 4, effect=_phase_logic_effect, defense=_phase_logic_defense)
    add("CLIFF SONG", 'R', 'body', 'both', 4, effect=_cliff_song_effect, defense=_cliff_song_defense)
    add("DART", 'R', 'body', 'both', 6, effect=_dart_effect, defense=_dart_defense)
    add("BERSERKER'S PRICE", 'R', 'body', 'melee', None,
        damage=_berserkers_price_dmg, effect=_berserkers_price_effect, defense=_berserkers_price_defense)
    add("SLIP THE BLADE", 'R', 'body', 'both', 6, effect=_slip_the_blade_effect, defense=_slip_the_blade_defense)
    add("GROUNDING STANCE", 'R', 'body', 'both', 6,
        effect=_grounding_stance_effect, defense=_grounding_stance_defense)
    add("SUNDER", 'R', 'body', 'melee', 6, effect=_sunder_effect, defense=_sunder_defense)
    add("DEAD HEAT", 'R', 'body', 'ranged', 8, effect=_dead_heat_effect, defense=_dead_heat_defense)
    add("ATTUNE", 'G', 'soul', 'melee', 6, effect=_attune_effect, defense=_attune_defense)
    add("BIND", 'G', 'soul', 'melee', 4, effect=_bind_effect, defense=_bind_defense)
    add("READ", 'G', 'soul', 'ranged', 6, effect=_read_effect, defense=_read_defense)
    add("CARRIED INJURY", 'G', 'soul', 'both', 4,
        effect=_carried_injury_effect, defense=_carried_injury_defense)

    add("ENDURE", 'R', 'body', 'melee', 4, effect=_endure_effect, defense=_endure_defense)
    add("WEATHERED", 'R', 'body', 'melee', 6, effect=_weathered_effect, defense=_weathered_defense)
    add("STARING CONTEST", 'R', 'body', 'melee', 4,
        effect=_staring_contest_effect, defense=_staring_contest_defense)
    add("WAITING GAME", 'R', 'body', 'both', 4,
        effect=_waiting_game_effect, defense=_waiting_game_defense)
    add("AFTERIMAGE", None, None, 'both', None,
        damage=_afterimage_damage, effect=_afterimage_effect, defense=_afterimage_defense,
        special_reveal='mirror_color')
    add("DRAIN", 'R', 'body', 'melee', 4, effect=_drain_effect, defense=_drain_defense)
    add("CONSUME", 'G', 'soul', 'melee', 6, effect=_consume_effect, defense=_consume_defense)
    add("FOLLOW-UP", None, None, 'both', None, damage=_follow_up_damage)
    add("BECOMING", None, None, 'both', None, damage=_becoming_damage)
    add("SEED", 'G', 'soul', 'melee', 6, effect=_seed_effect, defense=_seed_defense)
    add("EMERGENCY REPAIRS", 'R', 'body', 'ranged', 6,
        effect=_emergency_repairs_effect, defense=_emergency_repairs_defense)
    add("OVERCOMMIT", 'R', 'body', 'melee', 10, damage=_overcommit_dmg)
    add("OVERDRIVE", 'R', 'body', 'melee', 6,
        effect=_overdrive_effect, defense=_overdrive_defense)
    # Bestiary promotions
    add("CERTAIN CONTACT", 'R', 'body', 'melee', 8,
        defense=_certain_contact_defense, ignores=frozenset({'evade', 'resist', 'blind'}))
    add("HEAVE AND HAUL", 'G', 'soul', 'both', 8,
        effect=_heave_and_haul_effect, defense=_heave_and_haul_defense)
    add("HEAVE", 'R', 'body', 'melee', 8,
        effect=_heave_effect, defense=_heave_defense)
    add("HAUL", 'R', 'body', 'melee', 8,
        effect=_haul_effect, defense=_haul_defense)
    add("WATCHES FEET", 'G', 'soul', 'melee', 4,
        effect=_watches_feet_effect, defense=_watches_feet_defense)
    add("KNOWN GROUND", 'G', 'soul', 'both', 6,
        effect=_known_ground_effect, defense=_known_ground_defense)
    add("WHERE IT'S GATHERING", 'B', 'mind', 'both', 6,
        effect=_where_its_gathering_effect, defense=_where_its_gathering_defense)
    add("RHYTHM BREAK", 'R', 'body', 'melee', 8,
        damage=_rhythm_break_dmg, defense=_rhythm_break_defense)
    add("STILL COUNTING", 'G', 'soul', 'both', 6,
        damage=_still_counting_dmg, defense=_still_counting_defense)
    add("IRON GRIP", 'R', 'body', 'melee', 8,
        effect=_iron_grip_effect, defense=_iron_grip_defense)
    add("PATIENCE OF STONE", 'G', 'soul', 'melee', 6,
        effect=_patience_of_stone_effect, defense=_patience_of_stone_defense)
    add("DRAG", 'R', 'body', 'both', None,
        effect=_drag_effect, damage=_drag_damage, defense=_drag_defense)
    add("VIBRATION LOCK", 'B', 'mind', 'both', 4,
        effect=_vibration_lock_effect, defense=_vibration_lock_defense)
    add("SHED SKIN", 'G', 'soul', 'both', 4,
        effect=_shed_skin_effect, defense=_shed_skin_defense)
    add("DARK CORRIDOR", 'G', 'soul', 'melee', 6,
        effect=_dark_corridor_effect, defense=_dark_corridor_defense)
    add("COIL LATCH", 'R', 'body', 'melee', None,
        damage=_coil_latch_damage, defense=_coil_latch_defense)
    add("STILL GROUND", 'B', 'mind', 'both', None,
        effect=_still_ground_effect, damage=_still_ground_damage, defense=_still_ground_defense)
    add("PULL", 'R', 'body', 'both', 6, effect=_pull_effect, defense=_pull_defense)
    add("PUSH", 'R', 'body', 'melee', 6, effect=_push_effect, defense=_push_defense)
    add("ROLLOUT", 'R', 'body', 'melee', 4,
        damage=_rollout_damage, defense=_rollout_defense, returns_to_hand=True)
    add("SEISMIC REDIRECT", 'R', 'body', 'melee', 6,
        effect=_seismic_redirect_effect, defense=_seismic_redirect_defense)
    add("GORE", 'R', 'body', 'melee', 8, damage=_gore_damage, defense=_gore_defense)
    # FRAME-TRAP: the auto-win-and-negate-defense special case lives in
    # attack() (both engines, checked by card.name), and the tie-win lives
    # in rps() (also by name) -- nothing for content.py to register beyond
    # the card's base stats. "Effect: none" and "Defensive Bonus: wins ties"
    # (which structurally already means the attacker's Effect never fires
    # on that tie, since a won tie IS a clean defender win) are both fully
    # satisfied with no functions of their own.
    add("FRAME-TRAP", 'B', 'mind', 'both', 4)
    add("EXPOSED", 'B', 'mind', 'both', None, damage=_exposed_damage, defense=_exposed_defense)
    add("UNMAKE", 'B', 'mind', 'ranged', 4, effect=_unmake_effect, defense=_unmake_defense)
    add("LAST RESORT", 'B', 'mind', 'both', 8,
        effect=_last_resort_effect, defense=_last_resort_defense)
    add("FORESEEN", 'B', 'mind', 'ranged', 6,
        effect=_foreseen_effect, defense=_foreseen_defense)
    add("MARKED", 'B', 'mind', 'ranged', 6,
        effect=_marked_effect, defense=_marked_defense)
    add("RETORT", 'B', 'mind', 'ranged', 4,
        effect=_retort_effect, defense=_retort_defense)
    add("VEIL", 'B', 'mind', 'ranged', 6,
        effect=_veil_effect, defense=_veil_defense)
    add("DEAD END", 'B', 'mind', 'ranged', 8,
        effect=_dead_end_effect, defense=_dead_end_defense)
    add("SMOKE SCREEN", 'G', 'soul', 'melee', 4,
        effect=_smoke_screen_effect, defense=_smoke_screen_defense)
    add("STEADFAST", 'G', 'soul', 'melee', 4,
        effect=_steadfast_effect, defense=_steadfast_defense)
    add("OPENING", 'G', 'soul', 'melee', 4,
        effect=_opening_effect, defense=_opening_defense)
    add("UNTOUCHED", 'G', 'soul', 'both', 8,
        effect=_untouched_effect, defense=_untouched_defense)
    add("BRISTLE", 'G', 'soul', 'melee', 4,
        effect=_bristle_effect, defense=_bristle_defense)
    add("INSTINCT", 'G', 'soul', 'both', 6,
        effect=_instinct_effect, defense=_instinct_defense)
    add("OPEN GUARD", 'R', 'body', 'melee', 6,
        effect=_open_guard_effect, defense=_open_guard_defense)
    add("UNBROKEN", 'R', 'body', 'both', 8,
        effect=_unbroken_effect, defense=_unbroken_defense)
    add("ATTRITION", 'R', 'body', 'melee', 6,
        effect=_attrition_effect, defense=_attrition_defense)
    add("REELING", 'R', 'body', 'melee', 4,
        effect=_reeling_effect, defense=_reeling_defense)
    add("FOOTWORK", 'R', 'body', 'both', 6,
        effect=_footwork_effect, defense=_footwork_defense)
    add("BLINDSIDE", 'R', 'body', 'melee', 8,
        effect=_blindside_effect, defense=_blindside_defense)
    add("LEVEL THE FIELD", 'G', 'soul', 'both', 6,
        effect=_level_the_field_effect, defense=_level_the_field_defense)
    add("GENETIC SAMPLE", 'B', 'mind', 'both', 6,
        effect=_genetic_sample_effect, defense=_genetic_sample_defense)
    add("ADAPTIVE BITE", 'R', 'body', 'melee', 8,
        effect=_adaptive_bite_effect, defense=_adaptive_bite_defense)
    add("DISSOLVE AND KEEP", 'G', 'soul', 'both', 6,
        effect=_dissolve_and_keep_effect, defense=_dissolve_and_keep_defense)
    # Mason Glyphs / Objects
    add("MENDING GLYPH", 'G', 'soul', 'both', 6,
        effect=_mending_glyph_effect, defense=_mending_glyph_defense)
    add("HONING GLYPH", 'R', 'body', 'both', 6,
        effect=_honing_glyph_effect, defense=_honing_glyph_defense)
    add("BARBED GLYPH", 'R', 'body', 'both', 6,
        effect=_barbed_glyph_effect, defense=_barbed_glyph_defense)
    add("CIPHER GLYPH", 'B', 'mind', 'both', 6,
        effect=_cipher_glyph_effect, defense=_cipher_glyph_defense)
    add("WITHERING GLYPH", 'G', 'soul', 'both', 6,
        effect=_withering_glyph_effect, defense=_withering_glyph_defense)
    add("MIRING GLYPH", 'B', 'mind', 'both', 6,
        effect=_miring_glyph_effect, defense=_miring_glyph_defense)
    add("RECOVER", 'R', 'body', 'both', 4, effect=_recover_effect, defense=_recover_defense)
    add("FLOW", 'G', 'soul', 'melee', 8, effect=_flow_effect, defense=_flow_defense)
    add("ADAPT", 'G', 'soul', 'both', 4, wins_ties=True)   # Special Rule, vanilla otherwise
    add("CERTAINTY", 'B', 'mind', 'ranged', 6, wins_ties=True)   # Special Rule, vanilla otherwise
    add("VOID", 'G', 'soul', 'melee', 6, defense=_void_defense)
    add("ACCEPTANCE", 'G', 'soul', 'both', 6, effect=_acceptance_effect, defense=_acceptance_defense)
    add("SHADE AWAY", 'G', 'soul', 'melee', 4,
        effect=_shade_away_effect, defense=_shade_away_defense)
    add("DEAD RECKONING", 'G', 'soul', 'ranged', 4,
        effect=_dead_reckoning_effect, defense=_dead_reckoning_defense)
    add("RETALIATE", 'R', 'body', 'melee', 8,   # d6 -> d8, 2026-07-29: below its own
        # stat's baseline die (Body = d8, CLAUDE.md) at d6; the keyword_lab
        # dice-pass check found this fixes the gate's real underpowered win
        # rate (~46% -> ~51% vs a flat Evade+1 reference)
        effect=_retaliate_effect, defense=_retaliate_defense)
    add("WARSONG", 'G', 'soul', 'both', 6,
        effect=_warsong_effect, defense=_warsong_defense)
    add("REBUTTAL", 'B', 'mind', 'ranged', 6,
        effect=_rebuttal_effect, defense=_rebuttal_defense)
    add("FIELD MEDICINE", 'G', 'soul', 'ranged', 4,
        effect=_field_medicine_effect, defense=_field_medicine_defense)

    # The Patient Host — boss signature cards
    add("YOUR TURN WILL COME", 'G', 'soul', 'ranged', 6,
        effect=_your_turn_will_come_effect, defense=_your_turn_will_come_defense)
    add("REGISTERED", 'B', 'mind', 'both', 6,
        effect=_registered_effect, defense=_registered_defense)
    add("NO VACANCY", 'R', 'body', 'melee', 8,
        effect=_no_vacancy_effect, defense=_no_vacancy_defense)
    add("THE LEDGER NEVER CLOSES", 'G', 'soul', 'both', 6,
        effect=_ledger_effect, defense=_ledger_defense)
    add("YOU'RE NEXT", 'G', 'soul', 'both', 6,
        effect=_youre_next_effect, defense=_youre_next_defense)

    # Gambler archetype (core) — cards/green-soul.md, cards/red-body.md
    add("TABLE STAKES", 'R', 'body', 'both', 6,
        effect=_table_stakes_effect, defense=_table_stakes_defense)
    add("DOUBLE DOWN", 'R', 'body', 'melee', 6,
        effect=_double_down_effect, defense=_double_down_defense)

    # Briarwatch Jackalope (bestiary) — cards/briarwatch-jackalope.md
    add("BOLT", 'G', 'soul', 'melee', 6, effect=_bolt_effect, defense=_bolt_defense)
    add("NIP", 'R', 'body', 'melee', None, damage=_nip_dmg)
    add("FREEZE", 'B', 'mind', 'both', 4,
        effect=_jackalope_freeze_effect, defense=_jackalope_freeze_defense)
    add("QUICKSTEP", 'G', 'soul', 'both', 6,
        effect=_quickstep_effect, defense=_quickstep_defense)

    # Status card
    add("INJURY", None, None, None, None, is_status=True)
    add("EXHAUST", None, None, None, None, is_status=True)

    return C


FROST_DECK = [
    "SACRIFICE STRIKE", "BLOOD IN THE GAP", "BURN BRIGHT", "SPARK OF VIOLENCE",
    "AXIOM", "DEFLECT", "REALIGNMENT", "CLIMB", "FRACTURE", "TWIN STRIKE",
]

STEELE_DECK = [
    "FORGET", "BLOOD TITHE", "GAMBLER'S RUIN", "REPEL", "PAIN IS FUEL",
    "PARADOX", "MIRROR STEP", "ALIGN", "ANTICIPATE", "RENEWAL",
]

MIRE_DECK = [
    "BALANCE", "WITHER", "MOCKERY", "REND", "EQUAL FOOTING",
    "PRESS THE INJURY", "PARTITION", "TAINT", "ERODE",
]

# VOLK — the stat-maxed test dummy: Body 5 (the cap), red-heavy. Represents the
# "problem" build — dump every point into one stat and spam its color. Two
# off-color cards keep it from being trivially hard-countered.
VOLK_DECK = [
    "SACRIFICE STRIKE", "BURN BRIGHT", "SPARK OF VIOLENCE", "BLOOD IN THE GAP",
    "PAIN IS FUEL", "GAMBLER'S RUIN", "BLOOD TITHE",   # 7 red
    "DEFLECT", "TWIN STRIKE",                           # 1 blue, 1 green (implemented)
]

# The minmax trifecta — a Latin square of 4/3/2 spreads: each stat takes 4, 3,
# and 2 exactly once across the three decks, and card colors match the spread
# (stat-matching heuristic). Steele = Body, Sage = Mind, Adept = Soul.
#   Steele  Body4/Mind3/Soul2  -> 4R/3B/2G  (canonical campaign deck, kept as-is)
#   Sage    Mind4/Soul3/Body2  -> 4B/3G/2R
#   Adept   Soul4/Body3/Mind2  -> 4G/3R/2B
SAGE_DECK = [
    "AXIOM", "PARADOX", "FRACTURE", "ANTICIPATE",   # 4 blue
    "TWIN STRIKE", "MIRROR STEP", "MOCKERY",      # 3 green
    "PAIN IS FUEL", "GAMBLER'S RUIN",                # 2 red
]
ADEPT_DECK = [
    "TWIN STRIKE", "MIRROR STEP", "BALANCE", "MOCKERY",  # 4 green
    "PAIN IS FUEL", "GAMBLER'S RUIN", "BLOOD TITHE",        # 3 red
    "PARADOX", "ALIGN",                                     # 2 blue
]

# WARDEN — a dedicated green-support build (Soul 4), to test whether green's real
# support kit + a support-piloting brain makes it the team anchor its identity
# claims. 7 green (5 support + attacker + taunt), 1 red, 1 blue.
WARDEN_DECK = [
    "RESONATE", "SUPPORT", "SUPPORT", "WITNESS", "SHARED BURDEN",
    "TWIN STRIKE", "MOCKERY",                 # 7 green
    "PAIN IS FUEL", "PARADOX",                # 1 red, 1 blue
]

FROST_STATS = dict(body=3, mind=3, soul=3)
STEELE_STATS = dict(body=4, mind=3, soul=2)
MIRE_STATS = dict(body=3, mind=3, soul=3)
VOLK_STATS = dict(body=5, mind=2, soul=2)   # HP 19
SAGE_STATS = dict(mind=4, soul=3, body=2)
ADEPT_STATS = dict(soul=4, body=3, mind=2)
WARDEN_STATS = dict(soul=4, body=3, mind=2)

# Two archetypes built on the expanded set, for testing the new mechanics in teams.
VANGUARD_DECK = [   # Body 4 — front-line tank/protection with real self-sustain
    "STRIKE", "GUARD", "INTERCEPT", "TRAMPLE", "BRACE", "PAIN IS FUEL",
    "WITNESS", "RENEWAL", "PARADOX",
]
VANGUARD_STATS = dict(body=4, soul=3, mind=2)
TEMPO_DECK = [      # Mind 4 — control/tempo denial
    "INTERRUPT", "CHAIN", "CALCULATE", "PROFILE", "REFRACT", "AXIOM",
    "DELAY", "PARADOX", "PAIN IS FUEL",
]
TEMPO_STATS = dict(mind=4, soul=3, body=2)

# Four Oracle-drafted test players (2026-07-23) — built by actually simulating
# `rules/character-creation.md`'s real draft process (3 random cards offered,
# pick 1, unchosen return to the shared pool, rotate pick order, repeat to 9
# cards each) against the 103-card core pool that's both printed untagged in
# cards/*.md and registered below, with a naive "new player" pick heuristic
# (prefer the offered card matching your highest stat's color, tie-broken by
# base_die). Not hand-tuned archetypes like the roster above — these stand in
# for what an actual new table produces, for testing real party comps against
# real creature encounters rather than symmetric mirrors.
# CRIMSON and SKY — Drew's own, from the live 2v2 test (`playtesting/live-test-2v2.md`).
# Real, human-built decks, same category as Frost/Steele, but their exact card
# choices were deliberately hidden during that test and never fully recorded —
# only their stats, color/range counts, and whichever cards happened to get
# revealed during the one fight are known. The known cards are used as-is;
# remaining slots are a flagged reconstruction (Drew's call, 2026-07-28).
#
# Range distribution derived the same way color is derived from stats — but
# deliberately de-correlated (Drew's own point: if every Ranged card were also
# Blue, range would leak color information during RPS prediction). The known
# real reveals already fixed some of this before any reconstruction happened:
# Crimson's 7 known cards already included 5 Melee (one over his own naive
# 4-Melee derivation), matching his own memory of "only 2 ranged" better than
# the derivation did. Sky's 3 known reveals were already all-Blue, all-Ranged,
# which made his own hand-worked "2 Blue in Ranged" table impossible to hit —
# left as historical fact (Ranged 3, unchanged) rather than diluted with a
# 4th card for the sake of matching a target that was already unreachable.
CRIMSON_STATS = dict(body=4, mind=3, soul=2)
# Melee 5 / Ranged 2 / Both 2. Ranged and Both both color-mixed on purpose
# (1 Blue + 1 Red; 1 Green + 1 Blue) rather than monochrome.
CRIMSON_DECK = [
    "DEFLECT", "PROFILE", "SHARPEN",                 # 3 blue (SHARPEN: reconstructed, Both)
    "CHARGE", "REND", "TRAMPLE", "BURN BRIGHT",      # 4 red (BURN BRIGHT: reconstructed, Ranged)
    "WITNESS", "ROOTED OATH",                        # 2 green
]
SKY_STATS = dict(mind=4, body=3, soul=2)
# Ranged 3 (all Blue, unchanged from the known reveals) / Melee 3 / Both 3 —
# an even split once Ranged was left at 3 rather than grown to 4; Melee kept
# low per Drew's own memory ("only 2 melees"), the leftover slot went to Both
# instead, which is color-mixed (Blue/Red/Green) same as Melee (Red/Red/Green).
SKY_DECK = [
    "CALCULATE", "PROFILE", "AXIOM", "REALIGNMENT",  # 4 blue (REALIGNMENT: reconstructed, Both)
    "GAMBLER'S RUIN", "STRIKE", "RECOVER",            # 3 red (STRIKE: reconstructed Melee, RECOVER: reconstructed Both)
    "PATIENCE", "MIRROR STEP",                        # 2 green (both: reconstructed — Melee, Both)
]

# MOSS and GARNET — Claude's side of the same live 2v2 test. Unlike Crimson/
# Sky, both full 9-card decklists were actually recorded in the transcript
# (`playtesting/live-test-2v2.md`) — no reconstruction, no guessing, every
# card below is the real, played deck.
MOSS_STATS = dict(mind=2, body=3, soul=4)
MOSS_DECK = [
    "STILLNESS", "FOCUS",                      # 2 blue
    "GUARD", "ENDURE", "DIG IN",                # 3 red
    "PATIENCE", "RENEWAL", "WITNESS", "ROOTED OATH",  # 4 green
]
GARNET_STATS = dict(mind=3, body=4, soul=2)
GARNET_DECK = [
    "FORGET", "ANTICIPATE", "PROFILE",          # 3 blue
    "STRIKE", "BRACE", "PAIN IS FUEL", "RALLY",  # 4 red
    "TWIN STRIKE", "MOCKERY",                   # 2 green
]

# Briarwatch Jackalope (`bestiary/briarwatch-jackalope.md`) — Mind1/Body1/
# Soul3, CTR 5. Deck size = total stats = 5 (1 Blue/1 Red/3 Green). 4
# signature cards cover Blue1/Red1/Green2; FLOW (core) fills the 3rd Green,
# matching the creature's own constant-repositioning identity.
JACKALOPE_STATS = dict(mind=1, body=1, soul=3)
JACKALOPE_DECK = ["FREEZE", "NIP", "BOLT", "QUICKSTEP", "FLOW"]

# Aege, the Carrion Guide (`characters/aege.md`, `cards/aege.md`) — 2026-08-01.
# Mind5/Body3/Soul7, CTR 15, within the requested CTR 13-17 range. Deck size
# = total stats = 15 (5 Blue/3 Red/7 Green). 3 signature cards (2 Green/1
# Blue) plus core fill leaning control/information over damage, matching a
# guide who reads a fight rather than forces one.
AEGE_STATS = dict(mind=5, body=3, soul=7)
AEGE_DECK = [
    # Blue (5)
    "WHERE IT'S GATHERING", "PROFILE", "FOCUS", "ANTICIPATE", "CERTAINTY",
    # Red (3)
    "GROUNDING STANCE", "DART", "WEATHERED",
    # Green (7)
    "WATCHES FEET", "KNOWN GROUND", "READ", "FLOW", "INSTINCT", "DELAY",
    "SHADE AWAY",
]

GARRET_STATS = dict(mind=5, body=2, soul=2)
GARRET_DECK = [   # BARRIER swapped for DEFLECT, 2026-07-24 (BARRIER cut)
    "PARTITION", "DEFLECT", "SHARPEN", "SPARK OF VIOLENCE", "GORE",
    "UNDERSTANDING", "SEISMIC REDIRECT", "UNNAME", "DIG IN",
]
BRASCA_STATS = dict(mind=2, body=5, soul=2)
BRASCA_DECK = [
    "IRON GRIP", "DOUBLE DOWN", "RALLY", "IRON GRIP", "PUSH",
    "SACRIFICE STRIKE", "IRON GRIP", "ROLLOUT", "EMERGENCY REPAIRS",
]
WYN_STATS = dict(mind=2, body=2, soul=5)
WYN_DECK = [
    "DELAY", "YOU'RE NEXT", "URGENCY", "DEAD RECKONING", "VOID",
    "CHAIN", "SEED", "ACCEPTANCE", "COMMUNION",
]
TALLIS_STATS = dict(mind=3, body=3, soul=3)

# WARPER — a dedicated position-manipulation test deck, built to Drew's own
# range-distribution heuristic (2026-07-23): 4 Ranged / 3 Both / 2 Melee
# instead of the Both-heavy default most of the roster above quietly fell
# into. 6 of 9 cards directly force a reposition (self or foe): CALCULATE,
# PUSH, PULL, REPEL, MIRROR STEP, HEAVE AND HAUL. Built to answer one
# question — how often does an opponent actually have to burn a turn on the
# Move action against real, sustained position pressure?
WARPER_STATS = dict(mind=4, body=3, soul=2)
WARPER_DECK = [
    "CALCULATE", "STILLNESS", "TRACE", "FRACTURE",   # 4 Blue, all Ranged
    "PUSH", "REPEL", "PULL",                          # 3 Red — 2 Melee, 1 Both
    "MIRROR STEP", "HEAVE AND HAUL",                  # 2 Green, both Both
]
TALLIS_DECK = [
    "PAIN IS FUEL", "SEED", "FRACTURE", "STRIKE", "PREDICT",
    "BREAK", "BURN BRIGHT", "PREDICT", "RETALIATE",
]

# The Patient Host — CTR 24 boss, bespoke HP (bestiary/the-patient-host.md).
# Deck exactly as listed there: 5 signature + 19 core-fill, 8 Blue/6 Red/10 Green.
PATIENT_HOST_DECK = [
    "REGISTERED",                                                    # signature, blue
    "NO VACANCY",                                                    # signature, red
    "YOUR TURN WILL COME", "THE LEDGER NEVER CLOSES", "YOU'RE NEXT", # signature, green
    "STILLNESS", "PREDICT", "ANTICIPATE", "CALCULATE", "FOCUS", "PARTITION", "UNDERSTANDING",  # blue
    "GUARD", "ENDURE", "WEATHERED", "STARING CONTEST", "RECOVER",    # red
    "PATIENCE", "FLOW", "WITNESS", "SHADE AWAY", "URGENCY", "DELAY", "MOCKERY",  # green
]
PATIENT_HOST_STATS = dict(body=6, mind=8, soul=10, hp=66)   # formula baseline would be 21 — boss exception

# ORACLE — the full 60-card starter pool (testcampaigndecks/oracle.md), not
# a real character build. Wired in 2026-08-01 so the whole curated pool can
# actually be run through the sim (win rate, dice/keyword distribution
# checks) instead of only existing as a markdown list. Mind3/Body3/Soul3 —
# neutral, matching Frost/Steele's own baseline reference point, since the
# Oracle itself isn't tied to any one character's stats. A 60-card decklist
# is far outside the normal deck-size-matches-stats convention (same kind
# of grandfathered exception as Frost/Steele's own 10-card decks) —
# Combatant.decklist has no length constraint, confirmed directly.
ORACLE_STATS = dict(mind=3, body=3, soul=3)
ORACLE_DECK = [
    # Red (20)
    "ATTRITION", "BLINDSIDE", "BLOOD IN THE GAP", "CHARGE", "ENDURE",
    "EQUAL FOOTING", "FOOTWORK", "GAMBLER'S RUIN", "GORE", "GUARD",
    "OPEN GUARD", "PAIN IS FUEL", "PULL", "REELING", "REPEL", "RETALIATE",
    "SLIP THE BLADE", "TRAMPLE", "UNBROKEN", "WEATHERED",
    # Blue (20)
    "ANTICIPATE", "AXIOM", "CALCULATE", "CERTAINTY", "DEAD END", "DEFLECT",
    "FOCUS", "FORESEEN", "INTERRUPT", "LAST RESORT", "MARKED",
    "PHASE LOGIC", "PROFILE", "REALIGNMENT", "REBUTTAL", "REFRACT",
    "RETORT", "SHARPEN", "STUDY", "VEIL",
    # Green (20)
    "ADAPT", "BALANCE", "BIND", "BRISTLE", "COMMUNION", "DEAD RECKONING",
    "HEAVE AND HAUL", "INSTINCT", "MIRROR STEP", "MOCKERY", "OPENING",
    "RESONATE", "SHADE AWAY", "SMOKE SCREEN", "STEADFAST", "SUPPORT",
    "TWIN STRIKE", "UNTOUCHED", "URGENCY", "YOU'RE NEXT",
]

# registry so run.py can pit any two decks against each other
ROSTER = {
    "frost":  (FROST_STATS, FROST_DECK),
    "steele": (STEELE_STATS, STEELE_DECK),
    "mire":   (MIRE_STATS, MIRE_DECK),
    "volk":   (VOLK_STATS, VOLK_DECK),
    "sage":   (SAGE_STATS, SAGE_DECK),      # Mind 4 — blue archetype
    "adept":  (ADEPT_STATS, ADEPT_DECK),    # Soul 4 — green archetype
    "warden": (WARDEN_STATS, WARDEN_DECK),  # Soul 4 — green support anchor
    "vanguard": (VANGUARD_STATS, VANGUARD_DECK),  # Body 4 — tank/protection
    "tempo":    (TEMPO_STATS, TEMPO_DECK),        # Mind 4 — control/tempo
    "patient_host": (PATIENT_HOST_STATS, PATIENT_HOST_DECK),  # CTR 24 boss, bespoke HP 66
    "garret": (GARRET_STATS, GARRET_DECK),    # Oracle-drafted test player, Mind5/Body2/Soul2
    "brasca": (BRASCA_STATS, BRASCA_DECK),    # Oracle-drafted test player, Mind2/Body5/Soul2
    "wyn":    (WYN_STATS, WYN_DECK),          # Oracle-drafted test player, Mind2/Body2/Soul5
    "tallis": (TALLIS_STATS, TALLIS_DECK),    # Oracle-drafted test player, Mind3/Body3/Soul3
    "warper": (WARPER_STATS, WARPER_DECK),    # Position-manipulation test deck, Mind4/Body3/Soul2
    "crimson": (CRIMSON_STATS, CRIMSON_DECK),  # Drew's own, live 2v2 test, partial reconstruction
    "sky":     (SKY_STATS, SKY_DECK),          # Drew's own, live 2v2 test, partial reconstruction
    "moss":    (MOSS_STATS, MOSS_DECK),        # Claude's side, same live 2v2 test, fully recorded
    "garnet":  (GARNET_STATS, GARNET_DECK),    # Claude's side, same live 2v2 test, fully recorded
    "jackalope": (JACKALOPE_STATS, JACKALOPE_DECK),  # Briarwatch Jackalope, CTR 5
    "aege": (AEGE_STATS, AEGE_DECK),  # Carrion Guide, CTR 15
    "oracle": (ORACLE_STATS, ORACLE_DECK),  # full 60-card starter pool, not a real character build
}


# ============================ CARD_TAGS =======================================
# Mechanical-category tags per card (2026-07-29, Drew: "let's make new card
# buckets... build it out as tags in content.py") — supports the ongoing
# dice-balance pass by letting keyword_lab.py (or a human) pull every card
# that shares a mechanical shape, instead of eyeballing the pool by hand.
#
# A separate dict, not a Card.tags field threaded through all ~240 add()
# calls — this stays reviewable as one block, and adding a new tag category
# later means editing one dict, not touching hundreds of scattered
# registrations. Keyed by bucket, not by card (Drew's own framing was
# "a bucket for X" — this matches that shape directly: CARD_TAGS["movement"]
# is the whole bucket). Tags aren't mutually exclusive — most cards carry
# zero, some carry several (OVERDRIVE: keyword:deadly:self AND
# keyword:evade:self AND keyword:quick:self AND cost:exhaust).
#
# Vocabulary:
#   movement              — actually repositions self or foe (sets
#                            .position); a card that only READS position for
#                            a conditional check (GORE, NIP) isn't here
#   initiative             — applies Initiative Shift X
#   rps                    — alters reveal/RPS resolution itself, not just
#                            the attack that follows it — rare and load-
#                            bearing, matches Drew's own "rare RPS-changing
#                            ones like Axiom" framing. All 7 confirmed:
#                            AXIOM (axiom_ban), PARADOX (special_reveal),
#                            AFTERIMAGE (special_reveal), EQUAL FOOTING/
#                            ADAPT/CERTAINTY (wins_ties), FRAME-TRAP
#                            (hardcoded name-check in both engines)
#   keyword:<name>:self    — grants that keyword to the caster
#   keyword:<name>:ally    — grants it to an ally (dead in 1v1 Duel — see
#                            team_only below; needs keyword_lab.py --team)
#   keyword:<name>:foe     — applies it to the foe (a Debuff)
#                            (only deadly/resist/weak/vulnerable/evade/
#                            thorns/blind/ward/immune/rooted/staggered/quick
#                            are covered — the 12 keywords keyword_lab.py's
#                            own KEYWORD_GRANTS already knows how to test)
#   gated_damage           — a raw damage bonus (die or flat) on the Attack
#                            line, gated on a condition or a cost, rather
#                            than a keyword grant — doesn't fit any keyword
#                            bucket at all. Confirmed by reading each hit,
#                            not by text-matching "if" (that first pass
#                            caught a false positive — TWIN STRIKE's "if"
#                            is inside a RULING() comment string, not real
#                            conditional logic)
#   cost:hp / cost:exhaust / cost:discard
#                          — self-cost mechanism paid to cast. (Injury-as-
#                            cost checked directly, 2026-07-29 — no
#                            registered card implements it; a generic
#                            apply_injury() helper exists but nothing calls
#                            it. cost:discard corrected down hard from an
#                            initial rough-sweep guess of ~24 to a verified
#                            7 — that sweep was matching "discard" anywhere,
#                            including foe-forced-discard and Scry's own
#                            discard routing, not discard-as-a-cost
#                            specifically. Still got 3 of the 7 wrong on the
#                            first re-verification pass too (2026-07-29,
#                            during the Oracle-deck curation): STUDY
#                            ("Discard 2, draw 2"), TABLE STAKES ("Discard
#                            1 random card..."), and ACCEPTANCE ("may
#                            discard your hand...") don't match "discard a
#                            card"/"discard 1" phrasing exactly, so a
#                            pattern-based check missed them too — this
#                            list is now from a full manual read of every
#                            "discard" hit in the three core files, not a
#                            phrase pattern)
#   heal                   — heals self or an ally
#   scry                   — deck/hand manipulation (Scry, discard-then-draw)
#   glyph                  — places a persistent Mason Glyph/Object
#   ongoing                — deferred/anchored payout (me.ongoing.append)
#   status_transfer        — moves a status between combatants (steal, copy,
#                            mirror, strip, or push your own Injury/Exhaust
#                            onto a foe) rather than granting a fresh one
#   team_only              — reads "ally"/"allies" (engine.allies(...)) — a
#                            real no-op in a 1v1 Duel; needs
#                            keyword_lab.py's --team mode (2026-07-29) to
#                            test at all. Verified via actual engine.allies(
#                            calls, not a text grep — a naive "ally" search
#                            over-matches on words like "finally"/"actually"
#                            in comments
#   target_choice           — the card text says "Target" (SUPPORT's
#                            "Target ally," PARTITION's "Target enemy") —
#                            the caster genuinely picks who receives the
#                            effect, unlike Attacker/Defender (bound to
#                            whoever's in this specific RPS exchange, no
#                            choice) or "all allies"/"all enemies" (applies
#                            to everyone, also no choice). Distinction
#                            formalized in rules/cards.md, 2026-08-01, after
#                            8 new cards this session used "Target" when
#                            they meant Attacker/Defender — real code check
#                            confirmed the mismatch (foe is a plain
#                            positional parameter, zero selection logic) and
#                            a further sweep found the same error already
#                            existed on 8 older cards (ANTICIPATE, IRON
#                            GRIP, and six unregistered signature/creature
#                            cards) — all 16 fixed. This bucket is a first-
#                            pass sweep of the three core files only
#                            (cards/red-body.md, blue-mind.md,
#                            green-soul.md) — signature/creature files
#                            not swept for target_choice membership, unlike
#                            every other bucket above
#
# Coverage note: every bucket above was verified by reading the actual
# function bodies (grep the specific attribute mutation / engine call, then
# read each hit), not by trusting a rough text sweep — an early pass had
# real errors (movement's first draft included cards that only READ
# position, not moved anyone; cost:exhaust missed OVERDRIVE; a rumored
# ~7-card Injury-infliction bucket turned out to be zero cards, just the
# word "Injury" in a couple of card names; cost:discard was off by 8x on
# the first pass, then still 3 cards short even after that correction —
# see cost:discard's own note above for the full trail).
# Two more incidental findings while verifying, worth naming rather than
# quietly working around: SPIRAL CURRENT and ANALYZE both have a real
# `_..._effect` function defined in this file but no add(...) registration
# anywhere — dead code, not playable cards, excluded from every bucket
# below. And GUTTERING (`cards/duskwick.md`) is real canon text but, like
# STILL COUNTING before today, was never wired into the sim at all — also
# excluded, since there's no registered card to tag.
CARD_TAGS = {
    "movement": frozenset({
        "BOLT", "CALCULATE", "CHARGE", "DART", "DRAG", "FLOW",
        "HAUL", "HEAVE", "HEAVE AND HAUL", "KNOWN GROUND", "MIRROR STEP", "NO VACANCY",
        "PHASE LOGIC", "PULL", "PUSH", "QUICKSTEP", "REALIGNMENT", "REPEL",
        "SLIP THE BLADE", "TRAMPLE",
    }),
    "initiative": frozenset({
        "ACCEPTANCE", "DELAY", "DOUBLE DOWN", "INTERRUPT", "MOCKERY",
        "REBUTTAL", "RETALIATE", "URGENCY", "WARSONG",
        "YOUR TURN WILL COME", "YOU'RE NEXT",
    }),
    "rps": frozenset({
        "AXIOM", "PARADOX", "AFTERIMAGE", "EQUAL FOOTING", "ADAPT",
        "CERTAINTY", "FRAME-TRAP",
    }),

    "keyword:deadly:self": frozenset({
        "GAMBLER'S RUIN", "ALIGN", "SHARPEN", "STUDY", "RETALIATE",
        "ADAPTIVE BITE", "OVERDRIVE", "PATIENCE OF STONE", "COMMUNION",
        "SEED",
    }),
    "keyword:deadly:ally": frozenset({
        "RESONATE", "SUPPORT", "RALLY", "SHARPEN", "WARSONG", "COMMUNION",
        "ROOTED OATH",
    }),
    "keyword:weak:foe": frozenset({
        "ANTICIPATE", "TWIN STRIKE", "REFRACT", "DEAD RECKONING", "CONSUME",
        "WITHERING GLYPH", "ATTRITION", "WATCHES FEET",   # conditional — only if foe is Backline
    }),
    "keyword:resist:self": frozenset({
        "PAIN IS FUEL", "BRACE", "ALIGN", "INTERCEPT", "SYNCHRONY",
        "GROUNDING STANCE", "ENDURE", "NO VACANCY", "CERTAIN CONTACT",
        "RHYTHM BREAK", "STILL COUNTING", "DARK CORRIDOR", "ROLLOUT",
        "TABLE STAKES", "DIG IN", "SEED", "FORESEEN", "STEADFAST",
    }),
    "keyword:resist:ally": frozenset({"RESONATE", "GUARD", "ROOTED OATH"}),
    "keyword:vulnerable:self": frozenset({"OVERCOMMIT"}),   # deliberate exception —
        # every other real card applies Vulnerable to a foe (it's a Debuff);
        # OVERCOMMIT self-inflicts it on purpose, card text says so directly
    "keyword:vulnerable:foe": frozenset({"OPEN GUARD", "MARKED", "OPENING"}),   # new
        # 2026-08-01 (Oracle keyword-coverage pass) — the first real foe-
        # Vulnerable grants anywhere in the pool; apply_vulnerable() didn't
        # exist before these three needed it
    "keyword:evade:self": frozenset({
        "SHARED BURDEN", "SLIPSTREAM", "PHASE LOGIC", "SLIP THE BLADE",
        "SHADE AWAY", "GENETIC SAMPLE", "EXPOSED", "AFTERIMAGE", "OVERDRIVE",
        "SHED SKIN", "FREEZE", "KNOWN GROUND",
    }),
    "keyword:thorns:self": frozenset({
        "BLOOD IN THE GAP", "PAIN IS FUEL", "ADAPTIVE BITE", "BARBED GLYPH",
        "RETORT", "BRISTLE",
    }),
    "keyword:blind:foe": frozenset({
        "DEAD RECKONING", "SMOKE SCREEN", "CONSUME", "AFTERIMAGE",
        "VIBRATION LOCK", "DARK CORRIDOR", "BLINDSIDE", "VEIL",
    }),
    "keyword:blind:self": frozenset({"SMOKE SCREEN"}),   # yes, both — SMOKE
        # SCREEN blinds every enemy Frontline AND its own caster in the same effect
    "keyword:ward:self": frozenset({
        "DEFLECT", "PARADOX", "WEATHERED", "REGISTERED", "CIPHER GLYPH",
        "INSTINCT", "WHERE IT'S GATHERING",   # conditional — only if HP <= 6
    }),
    "keyword:immune:self": frozenset({"LAST RESORT", "UNBROKEN", "UNTOUCHED"}),   # all conditional: only below half HP
    "keyword:rooted:foe": frozenset({
        "BIND", "IRON GRIP", "DRAG", "COIL LATCH", "GORE", "DEAD END",
    }),
    "keyword:staggered:foe": frozenset({
        "BALANCE", "PROFILE", "REBUTTAL", "TABLE STAKES", "REELING",
    }),
    "keyword:quick:self": frozenset({"OVERDRIVE", "HEAVE AND HAUL", "FOOTWORK"}),
    "keyword:quick:ally": frozenset({"REALIGNMENT"}),

    "gated_damage": frozenset({
        "TRACE", "RHYTHM BREAK", "STILL COUNTING", "NIP", "UNDERSTANDING",
        "BURN BRIGHT", "PATIENCE",
    }),

    "cost:hp": frozenset({
        "SACRIFICE STRIKE", "BLOOD TITHE", "SHARED BURDEN", "RALLY", "ATTUNE",
    }),
    "cost:exhaust": frozenset({"OVERDRIVE", "UNMAKE"}),
    "cost:discard": frozenset({
        "ATTUNE", "BALANCE", "UNDERSTANDING", "STUDY", "TABLE STAKES",
        "ACCEPTANCE", "RENEWAL",
    }),

    "heal": frozenset({
        "BLOOD IN THE GAP", "BLOOD TITHE", "CLIFF SONG", "CONSUME",
        "DISSOLVE AND KEEP", "EMERGENCY REPAIRS", "ENDURE", "FIELD MEDICINE",
        "PARADOX", "PRESS THE INJURY", "RECOVER", "RENEWAL", "SHARED BURDEN",
        "TABLE STAKES", "WITNESS",
    }),
    "scry": frozenset({
        "ALIGN", "FOCUS", "FREEZE", "GENETIC SAMPLE", "PROFILE",
        "REGISTERED", "STILL GROUND", "UNDERSTANDING", "VIBRATION LOCK",
        "WATCHES FEET", "WHERE IT'S GATHERING",
    }),
    "glyph": frozenset({
        "BARBED GLYPH", "CIPHER GLYPH", "HONING GLYPH", "MENDING GLYPH",
        "MIRING GLYPH", "WITHERING GLYPH",
    }),
    "ongoing": frozenset({
        "ATTUNE", "CLIMB", "DIG IN", "IRON GRIP", "THE LEDGER NEVER CLOSES",
        "PATIENCE", "PATIENCE OF STONE", "ROOTED OATH", "SEED", "SLIPSTREAM",
        "SYNCHRONY",
    }),
    "status_transfer": frozenset({
        "WAITING GAME", "DRAIN", "UNMAKE", "LEVEL THE FIELD", "TRACE",
        "CARRIED INJURY",
    }),
    "team_only": frozenset({
        "ACCEPTANCE", "BLOOD TITHE", "CARRIED INJURY", "CLIFF SONG",
        "COMMUNION", "FIELD MEDICINE", "GUARD", "HEAVE AND HAUL",
        "PARTITION", "PATIENCE", "RALLY", "REALIGNMENT", "RENEWAL",
        "RESONATE", "ROOTED OATH", "SHARED BURDEN", "SHARPEN", "SUPPORT",
        "TABLE STAKES", "URGENCY", "WARSONG", "WITNESS",
    }),
    "target_choice": frozenset({
        "SHARPEN", "CALCULATE", "PARTITION", "SUPPORT", "PATIENCE",
        "WITNESS", "TWIN STRIKE", "SHARED BURDEN", "ROOTED OATH",
        "FIELD MEDICINE", "BLOOD TITHE",
    }),
}
