"""
Card content for the duel simulator — exactly Frost's and Steele's decks.

Each card's Effect and Defensive Bonus is implemented as faithfully as the rules
allow. Ally-only effects are deliberately no-ops in a 1v1 (You Are Not Your Own
Ally) and are marked DEAD — the sim will show how much dead weight each deck
carries into single combat. Simplifications are logged via RULING().
"""

from engine import Card, roll, RULING


def warded(target):
    """Consume a Ward/Deflect-ward if present; True means the debuff is blocked."""
    if target.ward:
        target.ward = False
        RULING("ward-blocks-debuff",
               "Ward/DEFLECT blocks the next debuff: forced move, discard, or a "
               "damage penalty all count as debuffs (rules/card-glossary.md Debuff).")
        return True
    return False


def remove_positive_status(target):
    """Positive Status Effects (rules/card-glossary.md): Evade, Resist, Deadly,
    Fortress, Anchored, Quick. Quick isn't implemented anywhere in the sim yet
    (see REALIGNMENT), so there's nothing to clear for it here."""
    target.evade = 0
    target.resist = 0
    target.deadly = 0
    target._fortress = False
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
    color = me.policy.name_axiom_color(engine, me, foe)
    if not warded(foe):
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
    engine.deal(foe, 2, unpreventable=True)


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
    if foe.position == 'frontline' and not warded(foe):
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
    color = me.policy.name_axiom_color(engine, me, foe)   # mirror-ban the attacker
    if not warded(foe):
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
    reals = [i for i, c in enumerate(foe.hand) if not c.is_status]  # discard a real card
    if reals:
        foe.discard.append(foe.hand.pop(engine.rng.choice(reals)))


def _twin_strike_defense(engine, me, foe):
    for a in engine.allies(me):    # next ally gains Deadly (ally-only: no self)
        a.deadly += 1


# ==================== MIRE (Injury-attrition, 3/3/3) ==========================
# A control deck built on shuffling Injuries into the opponent's deck (Rend,
# Taint), then cashing them in (Press the Injury), plus combat-long stat erosion
# (Wither -Body, Erode -Soul). Perfectly balanced 3R/3B/3G across the RPS wheel.

def _has_color(hand, color):
    return any(c.color == color and not c.is_status for c in hand)


def _discard_one_color(engine, me, color):
    for i, c in enumerate(me.hand):
        if c.color == color and not c.is_status:
            me.discard.append(me.hand.pop(i))
            return True
    return False


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
    if _has_color(me.hand, 'B') and _has_color(me.hand, 'R'):
        _discard_one_color(engine, me, 'B')
        _discard_one_color(engine, me, 'R')
        engine.deal(foe, me.eff('soul') + roll(4, engine.rng))  # second hit
        engine._say(f"    BALANCE triggers twice")


def _balance_defense(engine, me, foe):
    if _has_color(me.hand, 'B') and _has_color(me.hand, 'R'):
        _discard_one_color(engine, me, 'B')
        _discard_one_color(engine, me, 'R')
        foe.skip_turns += 1  # knocked down: must spend an action to stand
        RULING("balance-knockdown",
               "BALANCE def 'knock down (requires an Action to stand)' is modeled "
               "as the foe losing their next action to stand up.")


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
        a.deadly += 1                     # next ally to attack gains Deadly
def _support_defense(engine, me, foe):
    allies = engine.allies(me)
    if allies:
        c = allies[0].draw_one(engine.rng)
        if c:
            allies[0].hand.append(c)      # 1 ally draws 1




def _witness_effect(engine, me, foe):
    a = _most_hurt(engine.allies(me))
    if a:
        engine.heal(a, 3, source=me)
def _witness_defense(engine, me, foe):
    a = _most_hurt(engine.allies(me))
    if a:
        engine.heal(a, 3, source=me)


def _shared_burden_effect(engine, me, foe):
    a = _most_hurt(engine.allies(me))
    if a:
        a._damage_redirect = me           # next hit on that ally lands on me instead
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
    # Only on a clean win, never a tie (same `_redirect_dmg` signal pattern).
    if getattr(foe, '_redirect_dmg', None) is None:
        return
    engine.deal(foe, 2, unpreventable=True)

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

def _rooted_oath_effect(engine, me, foe):
    me.ongoing.append({'kind': 'rooted_oath', 'owner': me, 'anchor': me.position})
def _rooted_oath_defense(engine, me, foe):
    pool = [a for a in engine.allies(me) if a.position == me.position] or [me]
    engine.heal(min(pool, key=lambda a: a.hp), 3, source=me)

def _urgency_effect(engine, me, foe):
    a = _best_attacker(engine.allies(me))
    if a:
        engine.initiative_shift(a, 1)
def _urgency_defense(engine, me, foe):
    engine.initiative_shift(me, 1)          # the "-1 to the attacker" choice is unmodeled

def _delay_effect(engine, me, foe):
    engine.initiative_shift(foe, -1)       # defender skips (negative shift)
def _delay_defense(engine, me, foe):
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

def _patience_dmg(engine, me, foe):
    bonus = 0 if getattr(me, '_attacked_last', False) else 4   # +4 if you waited
    return me.eff('soul') + roll(4, engine.rng) + bonus
def _patience_defense(engine, me, foe):
    me.position = 'backline' if me.position == 'frontline' else 'frontline'


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

# STARING CONTEST (Red) — "move to immediately follow a chosen token in
# initiative order" is a direct requeue, not a numeric shift; no engine hook
# for it distinct from Initiative Shift X. Left fully unmodeled, registered
# with no effect/defense, same treatment as Tactical Wait.


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

def _youre_next_effect(engine, me, foe):
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
        defense=_twin_strike_defense)   # def buffs next ally (team play)

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
    add("RENEWAL", 'G', 'soul', 'both', 4,
        effect=_renewal_effect, defense=_renewal_defense)   # effect heals allies (team play)

    # Mire — Green
    add("BALANCE", 'G', 'soul', 'ranged', 4,
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
    add("WITNESS", 'G', 'soul', 'melee', 4,
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
    add("STARING CONTEST", 'R', 'body', 'both', 2)   # fully unmodeled — see note above
    add("RECOVER", 'R', 'body', 'both', 2, effect=_recover_effect, defense=_recover_defense)
    add("FLOW", 'G', 'soul', 'melee', 4, effect=_flow_effect, defense=_flow_defense)
    add("SHADE AWAY", 'G', 'soul', 'melee', 2,
        effect=_shade_away_effect, defense=_shade_away_defense)

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
