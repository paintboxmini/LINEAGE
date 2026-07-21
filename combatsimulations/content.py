"""
Card content for the duel simulator — exactly Frost's and Steele's decks.

Each card's Effect and Defensive Bonus is implemented as faithfully as the rules
allow. Ally-only effects are deliberately no-ops in a 1v1 (You Are Not Your Own
Ally) and are marked DEAD — the sim will show how much dead weight each deck
carries into single combat. Simplifications are logged via RULING().
"""

from engine import Card, roll, RULING, COLOR_TO_STAT, _rushdown, _rolled_die


def warded(target):
    """Consume a Ward/Deflect-ward if present; True means the debuff is blocked."""
    if target.ward:
        target.ward = False
        RULING("ward-blocks-debuff",
               "Ward/DEFLECT blocks the next auxiliary debuff — status conditions, "
               "stat reductions, discard, Injury/Exhaust seeding, Positive Status "
               "Effect removal. Never RPS/Initiative/Position pillar manipulation "
               "(rules/card-glossary.md Debuff) — those callers don't route through "
               "warded() at all.")
        return True
    return False


def remove_positive_status(target):
    """Positive Status Effects (rules/card-glossary.md): Evade, Resist, Deadly,
    Fortress, Anchored, Quick. Quick is real now (OVERCOMMIT, engine.py's
    Duel.take_turn) — this docstring was stale from before that; a pending
    Quick grant is exactly as much a Positive Status Effect as the rest and
    belongs here too."""
    target.evade = 0
    target.resist = 0
    target.deadly = 0
    target._fortress = False
    target._quick = False
    target.ongoing = [o for o in target.ongoing if 'anchor' not in o]   # Anchored-flavored entries only


def _same_as_discard_top(target):
    """TRACE's condition: did the card just played match what was already
    sitting on top of the discard pile before it? discard[-1] is the just-
    played card (already appended by the time Effect/Defense fires);
    discard[-2] is whatever was on top before that."""
    return len(target.discard) >= 2 and target.discard[-1].color == target.discard[-2].color


# ============================ FROST ==========================================

def _burn_bright_dmg(engine, me, foe):
    base = me.body + roll(6, engine.rng)
    if me.hand:  # exile 1 from hand for +2 this attack
        me.exile.append(me.hand.pop(engine.rng.randrange(len(me.hand))))
        base += 2
    return base


def _burn_bright_defense(engine, me, foe):
    if me.discard:
        me.exile.append(me.discard.pop())


def _fracture_dmg(engine, me, foe):
    return me.eff('mind') + roll(4, engine.rng)


def _fracture_effect(engine, me, foe):
    top3 = me.discard[-3:]
    if len(top3) != 3 or len({c.color for c in top3}) != 3:
        return
    enemies = engine.enemies(me)
    front = [e for e in enemies if e.position == 'frontline']
    back = [e for e in enemies if e.position == 'backline']
    side = front if len(front) >= len(back) else back   # "your choice" — pick the fuller side
    for e in side:
        engine.deal(e, 3)


def _trace_dmg(engine, me, foe):
    if _same_as_discard_top(foe):
        return me.eff('mind') + max(roll(4, engine.rng), roll(4, engine.rng))   # Deadly, this roll only
    return me.eff('mind') + roll(4, engine.rng)


def _trace_defense(engine, me, foe):
    if _same_as_discard_top(foe) and not warded(foe):   # foe = attacker here
        remove_positive_status(foe)


def _twin_strike_dmg(engine, me, foe):
    RULING("twin-strike-double-roll",
           "TWIN STRIKE '(Soul + d2) x2' is read as two independent (Soul + d2) "
           "instances summed, not one roll doubled.")
    return (me.soul + roll(2, engine.rng)) + (me.soul + roll(2, engine.rng))


def _axiom_effect(engine, me, foe):
    # RPS-pillar manipulation — not a Debuff, Ward never touches it (rules/card-glossary.md).
    color = me.policy.name_axiom_color(engine, me, foe)
    foe.axiom_ban = color
    engine._say(f"    AXIOM bans {color} on {foe.name}'s next reveal")


def _sacrifice_strike_effect(engine, me, foe):
    engine.deal(me, 3, unpreventable=True)  # "Pay 3 HP" — a self-cost on win


def _sacrifice_strike_defense(engine, me, foe):
    engine.deal(me, 5, unpreventable=True)
    engine.deal(foe, me.eff('body') + roll(10, engine.rng), unpreventable=True)   # Counter Attack: this card's own damage back


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
    engine.deal(foe, me.mind + roll(4, engine.rng), unpreventable=True)  # counter, no new RPS


def _realignment_effect(engine, me, foe):
    me.position = 'backline' if me.position == 'frontline' else 'frontline'
# Defensive Bonus ("All allies gain Quick") left unmodeled — Quick itself has
# never been implemented anywhere in the sim (only one card, MIRROR STEP, has
# ever granted it, and its own Defensive Bonus is unmodeled for the same
# reason). Needs the mechanic built once, not per-card.


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
    # Discard ignores Ward (not a debuff). Discard a real card, not an Injury —
    # forcing away their Injury would help them.
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
    allies = engine.allies(me)     # heal the most-hurt ally 4 (dead in 1v1)
    if allies:
        engine.heal(min(allies, key=lambda a: a.hp), 4, source=me)


def _blood_tithe_defense(engine, me, foe):
    engine.deal(me, 2, unpreventable=True)   # "Pay 2 HP"
    allies = engine.allies(me)             # heal the most-hurt ally 6 (dead in 1v1)
    if allies:
        engine.heal(min(allies, key=lambda a: a.hp), 6, source=me)


def _gamblers_ruin_dmg(engine, me, foe):
    die = roll(4, engine.rng)          # the DIE result explodes, not the total
    total = me.body + die
    rerolls = 0
    while rerolls < 3 and die % 2 == 1:
        die = roll(4, engine.rng)
        total += die
        rerolls += 1
    return total


def _gamblers_ruin_defense(engine, me, foe):
    me.next_attack_bonus += roll(4, engine.rng)


def _repel_effect(engine, me, foe):
    # Position-pillar manipulation — not a Debuff, Ward never touches it (rules/card-glossary.md).
    if foe.position == 'frontline':
        foe.position = 'backline'


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
    if not warded(foe):
        foe.weak += 1


def _renewal_effect(engine, me, foe):
    for a in engine.allies(me):    # all allies heal 2 (ally-only: no self)
        engine.heal(a, 2, source=me)


def _renewal_defense(engine, me, foe):
    downed = engine.downed_allies(me)
    if downed:
        engine.heal(downed[0], 6, source=me)   # revival heal — source= places them right after me in the wheel


def _twin_strike_defense(engine, me, foe):
    foe.weak += 1   # foe = attacker here


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


# --- Green ---
def _balance_effect(engine, me, foe):
    if me.hand:
        me.discard.append(me.hand.pop(engine.rng.randrange(len(me.hand))))
        foe.staggered = True


def _balance_defense(engine, me, foe):
    if me.hand:
        me.discard.append(me.hand.pop(engine.rng.randrange(len(me.hand))))
        foe.staggered = True   # foe = attacker here


def _wither_effect(engine, me, foe):
    if not warded(foe):
        foe.adjust('body', -1)   # -1 Body AND -3 max HP; no self-Injury cost anymore


def _mockery_effect(engine, me, foe):
    engine.initiative_shift(foe, -2)


def _mockery_defense(engine, me, foe):
    foe._forced_target = me   # taunt: attacker must target me next turn (team play)


# --- Red ---
def _rend_effect(engine, me, foe):
    if me._last_hit > 0 and not warded(foe):  # Injury infliction is a debuff
        engine.insert_injury(foe)


def _rend_defense(engine, me, foe):
    me._rend_guard = True


def _press_the_injury_dmg(engine, me, foe):
    return me.eff('body') + roll(4, engine.rng) + 2 * foe.injuries_visible()


def _press_the_injury_defense(engine, me, foe):
    n = me.injuries_visible()
    if n:
        engine.heal(me, 2 * n)
        remove_injuries(me)


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
    foe._no_defensive_bonus = True   # until foe's own next turn (take_turn clears it)


def _unname_defense(engine, me, foe):
    reals = [i for i, c in enumerate(foe.hand) if not c.is_status]
    if reals:
        foe.discard.append(foe.hand.pop(engine.rng.choice(reals)))


def _taint_effect(engine, me, foe):
    if warded(foe):   # Injury infliction is a debuff
        return
    engine.insert_injury(foe)


def _taint_defense(engine, me, foe):
    if warded(foe):   # foe = attacker here; Injury infliction is a debuff either direction
        return
    engine.insert_injury(foe)


def _erode_effect(engine, me, foe):
    # Registered as both effect= and defense= below. `foe` means "the other
    # combatant" in both calling conventions — the defender during Effect,
    # the attacker during a Defensive Bonus — so this one function already
    # correctly drains whichever of them the card text calls for without
    # needing two copies.
    if not warded(foe):
        foe.adjust('soul', -1)   # -1 Soul (no HP change — Soul isn't Body); no self-cost


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
    me._fortress = True
    me.evade += 1
def _shared_burden_defense(engine, me, foe):
    a = _most_hurt(engine.allies(me))
    if a:
        x = min(4, me.hp - 1)
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
    me._fortress = True
    me.resist += 2
_intercept_defense = _intercept_effect   # same text both sides

def _fortress_effect(engine, me, foe):
    me._fortress = True                    # I take the next hit meant for an ally
def _fortress_defense(engine, me, foe):
    for a in engine.allies(me):
        engine.heal(a, 2, source=me)

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
    engine.deal(foe, me.eff('body') + roll(4, engine.rng), unpreventable=True)   # Counter Attack: this card's own damage back

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
    a = _best_attacker(engine.allies(me)) or me   # target ally, self if no one else to pick
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
    foe.position = 'backline'
def _calculate_defense(engine, me, foe):
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
    foe.staggered = True                   # skips their next attack or defend, then clears itself

def _refract_effect(engine, me, foe):
    foe.weak += 1                          # defender gains Weak
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
    # Green card.
    prior = engine._prior_turn_hit
    if prior['hit'] and prior['actor'] in engine.allies(me):
        for a in engine.allies(me):
            a.deadly += 1
def _warsong_defense(engine, me, foe):
    a = _best_attacker(engine.allies(me)) or me
    engine.initiative_shift(a, 2)

def _rebuttal_effect(engine, me, foe):
    prior = engine._prior_turn_hit
    if prior['hit'] and prior['actor'] in engine.enemies(me):
        prior['actor'].staggered = True
def _rebuttal_defense(engine, me, foe):
    engine.initiative_shift(foe, -1)

def _communion_effect(engine, me, foe):
    for a in _team(engine, me):
        engine.scry(a, a, 1)               # party scry
def _communion_defense(engine, me, foe):
    for a in _team(engine, me):
        a.deadly += 1                      # you and allies gain Deadly

def _mirror_step_effect(engine, me, foe):
    for c in (me, foe):
        c.position = 'backline' if c.position == 'frontline' else 'frontline'

def _adapt_defense(engine, me, foe):
    me.evade += 1
# ADAPT's Effect ("instead of a tie, you win") is handled in rps() by card
# name, not here — see engine.py's Duel.rps() / team_engine.py's Battle._rps().

# VOID's Effect ("Defender gains Sealed") unmodeled — no item-usage mechanic
# exists in the sim, same treatment as PREDICT/DISTRACT.
def _void_defense(engine, me, foe):
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
    foe.weak += 1
def _dead_reckoning_defense(engine, me, foe):
    foe.blind += 1

def _patience_dmg(engine, me, foe):
    bonus = 0 if getattr(me, '_attacked_last', False) else 4   # +4 if you waited
    return me.eff('soul') + roll(4, engine.rng) + bonus
def _patience_defense(engine, me, foe):
    a = _most_hurt(engine.allies(me))
    if a:
        me.ongoing.append({'kind': 'patience_def', 'owner': me, 'anchor': me.position, 'target': a})


# ==================== Missing simple core cards (Patient Host deck-fill) =====
# None of these were ever wired to a roster deck before, so nobody caught the
# gap until building the Host's actual 24-card deck required all of them.

def _stillness_effect(engine, me, foe):
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
    if me.hand:
        me.discard.append(me.hand.pop(engine.rng.randrange(len(me.hand))))
        return me.eff('mind') + max(roll(6, engine.rng), roll(6, engine.rng))   # Deadly, this roll only
    return me.eff('mind') + roll(6, engine.rng)
def _understanding_defense(engine, me, foe):
    engine.scry(me, me, 2)   # "heal 4 if you bottom both" unmodeled — needs scry-outcome introspection the engine doesn't expose

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
    foe._forced_target = me   # taunt, same pattern as MOCKERY — "rushdown if they
                               # cannot reach you" unmodeled, matches Mockery's own gap

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
# order (Deadly > Resist > Evade > Fortress) either way, since a heuristic
# brain can't "choose" the way a real player would at the table; a real
# player picks freely among whatever's visible. Capped at however many
# statuses are actually present rather than duplicated — copying/stealing
# one Deadly twice isn't "two effects." Anchored and Quick are both skipped
# here (not by the same reasoning, though): Anchored lives in `ongoing`, not
# a simple flag; Quick is real now (OVERCOMMIT), just never asked to be
# copyable/stealable by either of these two cards specifically.
def _transfer_statuses(me, foe, count, steal):
    order = []
    if foe.deadly > 0:
        order.append('deadly')
    if foe.resist > 0:
        order.append('resist')
    if foe.evade > 0:
        order.append('evade')
    if getattr(foe, '_fortress', False):
        order.append('fortress')
    for kind in order[:count]:
        if kind == 'fortress':
            me._fortress = True
            if steal:
                foe._fortress = False
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
# _transfer_statuses (Deadly > Resist > Evade > Fortress), shared by UNMAKE
# and LEVEL THE FIELD below. Anchored/Quick skipped for the same reasons as
# _transfer_statuses.
def _strip_one_status(target, count=1):
    order = []
    if target.deadly > 0:
        order.append('deadly')
    if target.resist > 0:
        order.append('resist')
    if target.evade > 0:
        order.append('evade')
    if getattr(target, '_fortress', False):
        order.append('fortress')
    for kind in order[:count]:
        if kind == 'fortress':
            target._fortress = False
        else:
            setattr(target, kind, getattr(target, kind) - 1)

# UNMAKE (Blue) — the biggest buff-removal in the game: wipes every
# Positive Status Effect from the target in one go, via the existing
# `remove_positive_status` helper (already used by TRACE) — and, Drew's
# explicit call, ignores Ward entirely. A real, deliberate exception to the
# established Debuff/Ward rule, same category as AFTERIMAGE bypassing Axiom
# or FRAME-TRAP bypassing RPS — flagged here, not incidental, since
# normally a Positive-Status-Effect removal is exactly the kind of thing
# Ward is supposed to stop (`warded()`'s own ruling text). Paid for with a
# steep Exhaust cost — 3, heavier than OVERCOMMIT's 2, since this both
# breaks a standing rule and wipes an opponent's entire buff set at once.
def _unmake_effect(engine, me, foe):
    remove_positive_status(foe)
    engine.insert_exhaust(me, 3)
def _unmake_defense(engine, me, foe):
    remove_positive_status(foe)
    engine.insert_exhaust(me, 3)

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
    base = me.eff('mind') + _rolled_die(2, engine.rng, me)
    if foe.staggered:
        base *= 2
    return base
def _exposed_defense(engine, me, foe):
    me.evade += 1

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
        foe.weak += 1
        foe.blind += 1

def _consume_effect(engine, me, foe):
    engine.heal(me, me._last_hit)   # Lifesteal: full damage just dealt
    _consume_destroy(engine, me, foe)

def _consume_defense(engine, me, foe):
    dmg = me.eff('soul') + roll(4, engine.rng)
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
    color = engine._prior_turn_hit.get('color')
    if color is None:
        return roll(4, engine.rng)
    stat = COLOR_TO_STAT[color]
    return me.eff(stat) + roll(4, engine.rng)

def _afterimage_effect(engine, me, foe):
    foe.blind += 1
def _afterimage_defense(engine, me, foe):
    me.evade += 1


# ==================== The Patient Host — boss signature cards ================

def _your_turn_will_come_effect(engine, me, foe):
    engine.initiative_shift(foe, -2)
def _your_turn_will_come_defense(engine, me, foe):
    engine.initiative_shift(foe, -2)   # foe = the attacker, from a defense call

def _registered_effect(engine, me, foe):
    engine.scry(me, foe, 2)   # the Host reads and rearranges the target's own top 2 — "the ledger already knew"
def _registered_defense(engine, me, foe):
    me.ward = True

def _no_vacancy_effect(engine, me, foe):
    foe.position = 'backline'
def _no_vacancy_defense(engine, me, foe):
    me.resist += 2

def _ledger_effect(engine, me, foe):
    me.ongoing.append({'kind': 'ledger', 'owner': me, 'anchor': me.position})
def _ledger_defense(engine, me, foe):
    c = me.draw_one(engine.rng)
    if c:
        me.hand.append(c)

# STAKE (Cultivator) — renamed from SEED: same mechanic, a less plant-locked
# name so the card can fit a Construct or Mason deck without the fantasy
# forcing a growth metaphor. Tempo-as-a-resource, the first card in this
# shape: telegraphed, invests now for a bigger payoff later, no counter to
# track — plants at the caster's current position and pays out the next
# time THEY begin a turn still standing there (engine._ongoing_support_tick),
# however many turns that takes. Moving off the position (or being forced
# off it) just delays the payout, doesn't cancel it — Position is a real
# lever against this card, not just killing/Warding the caster first (Ward
# is irrelevant here regardless: this is a positive self-buff, never a
# debuff, and never applied by anyone else, so it was never in Ward's scope
# at all). Effect and Defensive Bonus stake the same way, different payoff
# each — "stake" is flavor, not a fictional action that needs the Effect
# side's exclusive timing; nothing stops narrating the Defensive Bonus as
# driving it in as part of the block itself.
def _stake_effect(engine, me, foe):
    me.ongoing.append({'kind': 'stake_deadly', 'owner': me, 'anchor': me.position})
def _stake_defense(engine, me, foe):
    me.ongoing.append({'kind': 'stake_resist', 'owner': me, 'anchor': me.position})

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

# OVERCOMMIT (Gambler) — the archetype's actual thesis: a huge upfront
# swing (all four Positive Status Effects at once) paid for with Exhaust,
# which costs a full future action to ever clear (rules/card-glossary.md,
# EXHAUST) rather than costing HP or a single hand card the way every
# other cost mechanic shipped this session does. First card ever to grant
# Quick — see engine.py's Duel.take_turn for how the free reposition
# actually resolves.
def _overcommit_payout(engine, me, foe):
    me.deadly += 1
    me.resist += 1
    me._quick = True
    me.evade += 1
    engine.insert_exhaust(me, 2)

def _overcommit_effect(engine, me, foe):
    _overcommit_payout(engine, me, foe)
def _overcommit_defense(engine, me, foe):
    _overcommit_payout(engine, me, foe)

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

# TELLS (was YOU CHANGED WALLS, Wall-Reader) — reworked on promotion,
# not just renamed. Effect uses "moved" (Drew's own call, the cleaner
# phrasing) via the new `_repositioned_since_last_turn` tracker (built for
# this and ROLLOUT below — first time "did X reposition since their last
# turn" has ever been tracked in the sim). Defensive Bonus is a genuinely
# new condition: gain Resist if the ATTACKER received a positive Initiative
# Shift or used Wait since their own last turn. Implementation note, flagged
# rather than silently assumed: "since your last turn" reads most literally
# as bound to the DEFENDER's own timeline, but the two new flags
# (`_shifted_positive`, `_used_wait`) are self-clearing on the AFFECTED
# combatant's own next turn (same shape as `_anticipating`/`_weathered`) —
# a materially simpler, self-contained approximation of the same intent,
# not a literal cross-combatant timeline comparison.
def _tells_effect(engine, me, foe):
    if foe._repositioned_since_last_turn:
        me.deadly += 1
def _tells_defense(engine, me, foe):
    if foe._shifted_positive or foe._used_wait:
        me.resist += 1

# IRON GRIP (was CORRECTION GRIP, Alignment Marshal) — unchanged mechanically.
def _iron_grip_effect(engine, me, foe):
    foe.rooted = True
def _iron_grip_defense(engine, me, foe):
    me.ongoing.append({'kind': 'anchor_heal2', 'owner': me, 'anchor': me.position})

# PATIENCE OF STONE (Delve Roller / Stonecoil, identical in both files —
# proven twice already) — unchanged, Defensive Bonus stays an unconditional
# Deadly grant per Drew ("maybe that's okay though").
def _patience_of_stone_effect(engine, me, foe):
    me.ongoing.append({'kind': 'anchor_heal2', 'owner': me, 'anchor': me.position})
def _patience_of_stone_defense(engine, me, foe):
    me.deadly += 1

# ROLLOUT (Delve Roller) — the Pokemon reference, made real: returns
# straight to hand after use (`returns_to_hand=True` on the Card itself),
# regardless of outcome, instead of ever sitting in discard. Needs its own
# damage function since the +4 bonus is conditional; reuses the same
# `_repositioned_since_last_turn` tracker as TELLS, just checking
# yourself instead of the target.
def _rollout_damage(engine, me, foe):
    base = me.eff('body') + roll(2, engine.rng)
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
    engine.deal(foe, me.eff('body') + roll(4, engine.rng), unpreventable=True)

# GORE (Minotaur) — unchanged.
def _gore_damage(engine, me, foe):
    base = me.eff('body') + roll(6, engine.rng)
    if foe.position == 'frontline':
        base += roll(4, engine.rng)
    return base
def _gore_defense(engine, me, foe):
    foe.rooted = True

def _youre_next_effect(engine, me, foe):
    # Promoted to core: Drew's tweak — only a clean win, not a tie
    # (`attacker._tie` is set True only while an Effect resolves during a
    # tie, engine.py's rps()/tie branch).
    if me._tie:
        return
    engine.initiative_shift(me, 2)
def _youre_next_defense(engine, me, foe):
    engine.deal(foe, 3, unpreventable=True)


# ============================ REGISTRY =======================================

def build_cards():
    C = {}

    def add(*a, **k):
        c = Card(*a, **k)
        C[c.name] = c

    # Frost — Red
    add("SACRIFICE STRIKE", 'R', 'body', 'melee', 10,
        effect=_sacrifice_strike_effect, defense=_sacrifice_strike_defense)
    add("BLOOD IN THE GAP", 'R', 'body', 'ranged', 2,
        effect=_blood_in_the_gap_effect, defense=_blood_in_the_gap_defense)
    add("BURN BRIGHT", 'R', 'body', 'ranged', 6, damage=_burn_bright_dmg, defense=_burn_bright_defense)
    add("SPARK OF VIOLENCE", 'R', 'body', 'both', 4,
        effect=_spark_effect, defense=_spark_effect)
    # Frost — Blue
    add("AXIOM", 'B', 'mind', 'both', 2, effect=_axiom_effect, defense=_axiom_defense)
    add("DEFLECT", 'B', 'mind', 'melee', 4,
        effect=_deflect_effect, defense=_deflect_defense)
    add("REALIGNMENT", 'B', 'mind', 'both', 4, effect=_realignment_effect)  # def DEAD (Quick unmodeled)
    add("CLIMB", 'B', 'mind', 'both', 4, effect=_climb_effect, defense=_climb_defense)
    add("FRACTURE", 'B', 'mind', 'ranged', 4, damage=_fracture_dmg, effect=_fracture_effect)
    add("TRACE", 'B', 'mind', 'ranged', 4, damage=_trace_dmg, defense=_trace_defense)
    # Frost — Green
    add("TWIN STRIKE", 'G', 'soul', 'melee', None, damage=_twin_strike_dmg,
        defense=_twin_strike_defense)

    # Steele — Red
    add("BLOOD TITHE", 'R', 'body', 'both', 4,
        effect=_blood_tithe_effect, defense=_blood_tithe_defense)
    add("BRACE", 'R', 'body', 'melee', 2, effect=_brace_effect, defense=_brace_defense)
    add("GAMBLER'S RUIN", 'R', 'body', 'melee', None,
        damage=_gamblers_ruin_dmg, defense=_gamblers_ruin_defense)
    add("REPEL", 'R', 'body', 'melee', 2,
        effect=_repel_effect, defense=_repel_effect)
    add("PAIN IS FUEL", 'R', 'body', 'both', 4,   # d6 -> d4 rebalance
        effect=_pain_is_fuel_effect, defense=_pain_is_fuel_defense)
    # Steele — Blue
    add("FORGET", 'B', 'mind', 'ranged', 2,
        effect=_forget_effect, defense=_forget_defense)
    add("PARADOX", 'B', 'mind', 'both', 4,
        effect=_paradox_effect, defense=_paradox_defense, special_reveal='paradox')
    add("ALIGN", 'B', 'mind', 'ranged', 4,
        effect=_align_effect, defense=_align_defense)
    add("ANTICIPATE", 'B', 'mind', 'melee', 4, effect=_anticipate_effect, defense=_anticipate_defense)
    # Steele — Green
    add("RENEWAL", 'G', 'soul', 'both', 2,
        effect=_renewal_effect, defense=_renewal_defense)

    # Mire — Green
    add("BALANCE", 'G', 'soul', 'ranged', 2,
        effect=_balance_effect, defense=_balance_defense)
    add("WITHER", 'G', 'soul', 'both', 4,
        effect=_wither_effect, defense=_wither_effect)
    add("MOCKERY", 'G', 'soul', 'both', 4,
        effect=_mockery_effect, defense=_mockery_defense)
    # Mire — Red
    add("REND", 'R', 'body', 'melee', 4,
        effect=_rend_effect, defense=_rend_defense)
    add("EQUAL FOOTING", 'R', 'body', 'both', 2)   # "instead of a tie, you win" — handled in rps(), no effect/defense function needed
    add("PRESS THE INJURY", 'R', 'body', 'melee', 4,
        damage=_press_the_injury_dmg, defense=_press_the_injury_defense)
    add("DIG IN", 'R', 'body', 'melee', 2, effect=_dig_in_effect, defense=_dig_in_defense)
    # Mire — Blue
    add("PARTITION", 'B', 'mind', 'both', 2,
        effect=_partition_effect, defense=_partition_defense)
    add("UNNAME", 'B', 'mind', 'both', 2, effect=_unname_effect, defense=_unname_defense)
    add("SLIPSTREAM", 'B', 'mind', 'both', 2, effect=_slipstream_effect, defense=_slipstream_defense)
    add("TAINT", 'B', 'mind', 'ranged', 2,
        effect=_taint_effect, defense=_taint_defense)
    add("ERODE", 'B', 'mind', 'both', 4,
        effect=_erode_effect, defense=_erode_effect)

    # Green support kit (team play)
    add("RESONATE", 'G', 'soul', 'ranged', 4,
        effect=_resonate_effect, defense=_resonate_defense)
    add("SUPPORT", 'G', 'soul', 'ranged', 4,
        effect=_support_effect, defense=_support_defense)
    add("WITNESS", 'G', 'soul', 'melee', 2,
        effect=_witness_effect, defense=_witness_defense)
    add("SHARED BURDEN", 'G', 'soul', 'both', 6,
        effect=_shared_burden_effect, defense=_shared_burden_defense)

    # --- Expanded set: Red ---
    add("STRIKE", 'R', 'body', 'melee', 8, defense=_strike_defense)
    add("GUARD", 'R', 'body', 'melee', 2, effect=_guard_effect, defense=_guard_defense)
    add("INTERCEPT", 'R', 'body', 'melee', 2,
        effect=_intercept_effect, defense=_intercept_defense)
    add("RALLY", 'R', 'body', 'both', 2, effect=_rally_effect, defense=_rally_defense)
    add("TRAMPLE", 'R', 'body', 'melee', 4,
        effect=_trample_effect, defense=_trample_defense)
    add("BREAK", 'R', 'body', 'melee', 4, defense=_break_defense)
    add("CHARGE", 'R', 'body', 'both', 4, effect=_charge_move, defense=_charge_move)
    # --- Expanded set: Blue ---
    add("INTERRUPT", 'B', 'mind', 'both', 2,
        effect=_interrupt_effect, defense=_interrupt_defense)
    add("SHARPEN", 'B', 'mind', 'both', 4, effect=_sharpen_effect, defense=_sharpen_defense)
    add("CHAIN", 'B', 'mind', 'both', 2, effect=_chain_effect, defense=_chain_defense)
    add("CALCULATE", 'B', 'mind', 'ranged', 4,
        effect=_calculate_effect, defense=_calculate_defense)
    add("STUDY", 'B', 'mind', 'ranged', 6, effect=_study_effect, defense=_study_defense)
    add("PROFILE", 'B', 'mind', 'both', 4, effect=_profile_effect, defense=_profile_defense)
    add("REFRACT", 'B', 'mind', 'ranged', 4,
        effect=_refract_effect, defense=_refract_defense)
    # --- Expanded set: Green ---
    add("SYNCHRONY", 'G', 'soul', 'both', 2,
        effect=_synchrony_effect, defense=_synchrony_defense)
    add("ROOTED OATH", 'G', 'soul', 'both', 4,
        effect=_rooted_oath_effect, defense=_rooted_oath_defense)
    add("URGENCY", 'G', 'soul', 'melee', 4,
        effect=_urgency_effect, defense=_urgency_defense)
    add("DELAY", 'G', 'soul', 'both', 6, effect=_delay_effect, defense=_delay_defense)
    add("COMMUNION", 'G', 'soul', 'both', 4,
        effect=_communion_effect, defense=_communion_defense)
    add("MIRROR STEP", 'G', 'soul', 'both', 4, effect=_mirror_step_effect)
    add("PATIENCE", 'G', 'soul', 'melee', None,
        damage=_patience_dmg, defense=_patience_defense)

    # Missing simple core cards (Patient Host deck-fill)
    add("STILLNESS", 'B', 'mind', 'ranged', 4,
        effect=_stillness_effect, defense=_stillness_defense)
    add("PREDICT", 'B', 'mind', 'melee', 6)   # Sealed unmodeled — no item-usage mechanic exists in the sim
    add("FOCUS", 'B', 'mind', 'both', 4, effect=_focus_effect, defense=_focus_defense)
    add("UNDERSTANDING", 'B', 'mind', 'both', 6,
        damage=_understanding_dmg, defense=_understanding_defense)
    add("ENDURE", 'R', 'body', 'both', 2, effect=_endure_effect, defense=_endure_defense)
    add("WEATHERED", 'R', 'body', 'both', 4, effect=_weathered_effect, defense=_weathered_defense)
    add("STARING CONTEST", 'R', 'body', 'both', 2,
        effect=_staring_contest_effect, defense=_staring_contest_defense)
    add("WAITING GAME", 'R', 'body', 'both', 2,
        effect=_waiting_game_effect, defense=_waiting_game_defense)
    add("AFTERIMAGE", None, None, 'both', None,
        damage=_afterimage_damage, effect=_afterimage_effect, defense=_afterimage_defense,
        special_reveal='mirror_color')
    add("DRAIN", 'R', 'body', 'both', 2, effect=_drain_effect, defense=_drain_defense)
    add("CONSUME", 'G', 'soul', 'both', 4, effect=_consume_effect, defense=_consume_defense)
    add("FOLLOW-UP", None, None, 'both', None, damage=_follow_up_damage)
    add("BECOMING", None, None, 'both', None, damage=_becoming_damage)
    add("STAKE", 'G', 'soul', 'both', 4, effect=_stake_effect, defense=_stake_defense)
    add("EMERGENCY REPAIRS", 'R', 'body', 'ranged', 4,
        effect=_emergency_repairs_effect, defense=_emergency_repairs_defense)
    add("OVERCOMMIT", 'R', 'body', 'both', 4,
        effect=_overcommit_effect, defense=_overcommit_defense)
    # Bestiary promotions
    add("CERTAIN CONTACT", 'R', 'body', 'melee', 6,
        defense=_certain_contact_defense, ignores=frozenset({'evade', 'resist', 'blind'}))
    add("HEAVE AND HAUL", 'G', 'soul', 'both', 4,
        effect=_heave_and_haul_effect, defense=_heave_and_haul_defense)
    add("TELLS", 'R', 'body', 'melee', 6,
        effect=_tells_effect, defense=_tells_defense)
    add("IRON GRIP", 'R', 'body', 'melee', 6,
        effect=_iron_grip_effect, defense=_iron_grip_defense)
    add("PATIENCE OF STONE", 'G', 'soul', 'melee', 4,
        effect=_patience_of_stone_effect, defense=_patience_of_stone_defense)
    add("ROLLOUT", 'R', 'body', 'melee', 2,
        damage=_rollout_damage, defense=_rollout_defense, returns_to_hand=True)
    add("SEISMIC REDIRECT", 'R', 'body', 'both', 4,
        effect=_seismic_redirect_effect, defense=_seismic_redirect_defense)
    add("GORE", 'R', 'body', 'melee', 6, damage=_gore_damage, defense=_gore_defense)
    # FRAME-TRAP: the auto-win-and-negate-defense special case lives in
    # attack() (both engines, checked by card.name), and the tie-win lives
    # in rps() (also by name) -- nothing for content.py to register beyond
    # the card's base stats. "Effect: none" and "Defensive Bonus: wins ties"
    # (which structurally already means the attacker's Effect never fires
    # on that tie, since a won tie IS a clean defender win) are both fully
    # satisfied with no functions of their own.
    add("FRAME-TRAP", 'B', 'mind', 'both', 2)
    add("EXPOSED", 'B', 'mind', 'both', None, damage=_exposed_damage, defense=_exposed_defense)
    add("UNMAKE", 'B', 'mind', 'both', 2, effect=_unmake_effect, defense=_unmake_defense)
    add("LEVEL THE FIELD", 'G', 'soul', 'both', 4,
        effect=_level_the_field_effect, defense=_level_the_field_defense)
    add("RECOVER", 'R', 'body', 'both', 2, effect=_recover_effect, defense=_recover_defense)
    add("FLOW", 'G', 'soul', 'melee', 4, effect=_flow_effect, defense=_flow_defense)
    add("ADAPT", 'G', 'soul', 'both', 6, defense=_adapt_defense)
    add("VOID", 'G', 'soul', 'melee', 4, defense=_void_defense)
    add("ACCEPTANCE", 'G', 'soul', 'both', 4, effect=_acceptance_effect, defense=_acceptance_defense)
    add("SHADE AWAY", 'G', 'soul', 'melee', 2,
        effect=_shade_away_effect, defense=_shade_away_defense)
    add("DEAD RECKONING", 'G', 'soul', 'both', 4,
        effect=_dead_reckoning_effect, defense=_dead_reckoning_defense)
    add("RETALIATE", 'R', 'body', 'both', 4,
        effect=_retaliate_effect, defense=_retaliate_defense)
    add("WARSONG", 'G', 'soul', 'both', 4,
        effect=_warsong_effect, defense=_warsong_defense)
    add("REBUTTAL", 'B', 'mind', 'ranged', 4,
        effect=_rebuttal_effect, defense=_rebuttal_defense)
    add("FIELD MEDICINE", 'G', 'soul', 'ranged', 2,
        effect=_field_medicine_effect, defense=_field_medicine_defense)

    # The Patient Host — boss signature cards
    add("YOUR TURN WILL COME", 'G', 'soul', 'ranged', 4,
        effect=_your_turn_will_come_effect, defense=_your_turn_will_come_defense)
    add("REGISTERED", 'B', 'mind', 'both', 4,
        effect=_registered_effect, defense=_registered_defense)
    add("NO VACANCY", 'R', 'body', 'melee', 6,
        effect=_no_vacancy_effect, defense=_no_vacancy_defense)
    add("THE LEDGER NEVER CLOSES", 'G', 'soul', 'both', 4,
        effect=_ledger_effect, defense=_ledger_defense)
    add("YOU'RE NEXT", 'G', 'soul', 'both', 4,
        effect=_youre_next_effect, defense=_youre_next_defense)

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
}
