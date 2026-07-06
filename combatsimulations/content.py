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


def lifesteal(engine, me, foe, x):
    dealt = engine.deal(foe, x, unpreventable=True)
    engine.heal(me, dealt)


# ============================ FROST ==========================================

def _burn_bright_dmg(engine, me, foe):
    base = me.body + roll(6, engine.rng)
    if me.hand:  # exile 1 from hand for +2 this attack
        me.exile.append(me.hand.pop(engine.rng.randrange(len(me.hand))))
        base += 2
    return base


def _fracture_dmg(engine, me, foe):
    base = me.mind + roll(4, engine.rng)
    top3 = me.discard[-3:]
    if len(top3) == 3 and len({c.color for c in top3}) == 3:
        base += 4
    return base


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
    engine.deal(me, 2, unpreventable=True)  # "Pay 2 HP" — a self-cost on win


def _sacrifice_strike_defense(engine, me, foe):
    engine.deal(me, 2, unpreventable=True)
    engine.deal(foe, roll(8, engine.rng), unpreventable=True)


def _blood_in_the_gap_effect(engine, me, foe):
    lifesteal(engine, me, foe, 1)  # "steal 1 HP from each enemy"


def _blood_in_the_gap_defense(engine, me, foe):
    me.ongoing.append({'kind': 'gap_retaliate', 'owner': me})
    RULING("gap-retaliate",
           "BLOOD IN THE GAP defense 'if damaged before your next turn, steal 2 "
           "each time' is modeled as a retaliate rider; simplified to trigger on "
           "the next damage instance only.")


def _spark_effect(engine, me, foe):
    engine.deal(foe, 2, unpreventable=True)


def _deflect_effect(engine, me, foe):
    me.ward = True


def _deflect_defense(engine, me, foe):
    engine.deal(foe, me.mind + roll(4, engine.rng), unpreventable=True)  # counter, no new RPS


def _realignment_effect(engine, me, foe):
    me.position = 'backline' if me.position == 'frontline' else 'frontline'


def _climb_defense(engine, me, foe):
    me.ongoing.append({'kind': 'handsize'})


# ============================ STEELE =========================================

def _forget_effect(engine, me, foe):
    # Discard ignores Ward (not a debuff). Discard a real card, not a Wound —
    # forcing away their Wound would help them.
    reals = [i for i, c in enumerate(foe.hand) if not c.is_status]
    if reals:
        foe.discard.append(foe.hand.pop(engine.rng.choice(reals)))


def _forget_defense(engine, me, foe):
    # exile the attacker's just-played card (top of their discard)
    if foe.discard:
        foe.exile.append(foe.discard.pop())


def _blood_tithe_effect(engine, me, foe):
    engine.deal(me, 2, unpreventable=True)
    allies = engine.allies(me)     # heal the most-hurt ally 4 (dead in 1v1)
    if allies:
        engine.heal(min(allies, key=lambda a: a.hp), 4)


def _blood_tithe_defense(engine, me, foe):
    me.ongoing.append({'kind': 'blood_tithe', 'controller': me, 'victim': foe})


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
    engine.deal(foe, 2, unpreventable=True)


def _paradox_effect(engine, me, foe):
    lifesteal(engine, me, foe, 1)


def _paradox_defense(engine, me, foe):
    lifesteal(engine, me, foe, 2)


def _spiral_current_effect(engine, me, foe):
    for c in (me, foe):
        c.position = 'backline' if c.position == 'frontline' else 'frontline'


def _align_effect(engine, me, foe):
    seen = engine.scry(me, me, 2)              # reorder own deck; then conditional draw
    if len(seen) == 2 and seen[0].color == seen[1].color and seen[0].color is not None:
        c = me.draw_one(engine.rng)
        if c:
            me.hand.append(c)


def _align_defense(engine, me, foe):
    seen = engine.scry(me, me, 2)
    if len(seen) == 2 and seen[0].color == seen[1].color and seen[0].color is not None:
        me.next_attack_bonus += 2


def _axiom_defense(engine, me, foe):
    engine.scry(me, foe, 2)                    # scry the attacker's deck (sabotage)


def _anticipate_defense(engine, me, foe):
    if not warded(foe):
        foe.next_attack_bonus -= 3  # target's next attack deals -3


def _renewal_effect(engine, me, foe):
    for a in _team(engine, me):    # you and all allies heal 2
        engine.heal(a, 2)


def _renewal_defense(engine, me, foe):
    reals = [i for i, c in enumerate(foe.hand) if not c.is_status]  # discard a real card
    if reals:
        foe.discard.append(foe.hand.pop(engine.rng.choice(reals)))


def _twin_strike_defense(engine, me, foe):
    for a in _team(engine, me):    # you or next ally +3
        a.next_attack_bonus += 3


# ==================== MIRE (Wound-attrition, 3/3/3) ==========================
# A control deck built on shuffling Wounds into the opponent's deck (Rend,
# Taint), then cashing them in (Press the Wound), plus combat-long stat erosion
# (Wither -Body, Erode -Soul). Perfectly balanced 3R/3B/3G across the RPS wheel.

def _has_color(hand, color):
    return any(c.color == color and not c.is_status for c in hand)


def _discard_one_color(engine, me, color):
    for i, c in enumerate(me.hand):
        if c.color == color and not c.is_status:
            me.discard.append(me.hand.pop(i))
            return True
    return False


def remove_wounds(target, n=None):
    """Permanently destroy up to n Wounds (all if n is None) from HAND + DISCARD
    only — never the deck (Drew: no tracking/searching hidden Wounds)."""
    removed = 0
    for pile in (target.hand, target.discard):
        i = 0
        while i < len(pile):
            if pile[i].is_status and pile[i].name == 'WOUND' and (n is None or removed < n):
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
        foe.adjust('body', -1)   # -1 Body AND -3 max HP; no self-Wound cost anymore


def _mockery_effect(engine, me, foe):
    engine.initiative_shift(foe, -2)


def _mockery_defense(engine, me, foe):
    foe._forced_target = me   # taunt: attacker must target me next turn (team play)


# --- Red ---
def _rend_effect(engine, me, foe):
    if me._last_hit > 0 and not warded(foe):  # Wound infliction is a debuff
        engine.shuffle_wound(foe)


def _rend_defense(engine, me, foe):
    me._rend_guard = True


def _equal_footing_dmg(engine, me, foe):
    base = me.eff('body') + roll(4, engine.rng)
    if foe.position == me.position:
        base += 2
    return base


def _equal_footing_defense(engine, me, foe):
    me._damage_floor = foe.hp  # next attack can't take me below attacker's HP


def _press_the_wound_dmg(engine, me, foe):
    return me.eff('body') + roll(4, engine.rng) + 2 * foe.wounds_visible()


def _press_the_wound_defense(engine, me, foe):
    n = me.wounds_visible()
    if n:
        engine.heal(me, 2 * n)
        remove_wounds(me)


# --- Blue ---
def _partition_effect(engine, me, foe):
    foe.must_target_frontline = True


def _partition_defense(engine, me, foe):
    RULING("partition-shield-dead",
           "PARTITION def 'target ally cannot be targeted' has no valid target in "
           "a 1v1 (You Are Not Your Own Ally).")


def _taint_effect(engine, me, foe):
    if warded(foe):   # Wound infliction is a debuff
        return
    if foe.wounds_visible() > 0:
        engine.shuffle_wound(foe)
        engine.shuffle_wound(foe)
    else:
        engine.shuffle_wound(foe)


def _taint_defense(engine, me, foe):
    remove_wounds(me, 1)


def _erode_effect(engine, me, foe):
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
    for a in _team(engine, me):
        a.next_attack_bonus += 2          # all allies +2 next attack
def _resonate_defense(engine, me, foe):
    for a in _team(engine, me):
        a.resist += 1                     # all allies gain Resist 1


def _support_effect(engine, me, foe):
    a = _best_attacker(_team(engine, me))
    if a:
        a.next_attack_bonus += 3          # next ally to attack +3
def _support_defense(engine, me, foe):
    allies = engine.allies(me)
    if allies:
        c = allies[0].draw_one(engine.rng)
        if c:
            allies[0].hand.append(c)      # 1 ally draws 1


def _conduct_effect(engine, me, foe):
    a = _best_attacker(_team(engine, me))
    if a:
        a.next_attack_bonus += 2
def _conduct_defense(engine, me, foe):
    a = _most_hurt(engine.allies(me))
    if a:
        c = a.draw_one(engine.rng)
        if c:
            a.hand.append(c)              # target ally draws 1


def _witness_effect(engine, me, foe):
    a = _most_hurt(_team(engine, me))
    if a:
        engine.heal(a, 3)
def _witness_defense(engine, me, foe):
    a = _most_hurt(_team(engine, me))
    if a:
        engine.heal(a, 3)


def _shared_burden_effect(engine, me, foe):
    a = _most_hurt(engine.allies(me))
    if a:
        a._damage_redirect = me           # next hit on that ally lands on me instead
def _shared_burden_defense(engine, me, foe):
    a = _most_hurt(engine.allies(me))
    if a:
        x = min(4, me.hp - 1)
        if x > 0:
            engine.heal(a, x)
            engine.deal(me, x, unpreventable=True)   # transfer HP to the ally


# ==================== EXPANDED SET (team-combat variety) =====================
# ~20 more cards covering tanks, team buffs, AoE, tempo denial, positioning,
# ongoing heals, and control. Ally effects route through engine.allies / _team so
# they're live in a Battle and inert in a duel.

# --- Red: front-line, protection, AoE ---
def _strike_defense(engine, me, foe):
    engine.deal(foe, 2, unpreventable=True)

def _guard_effect(engine, me, foe):
    for a in engine.allies(me):
        a.armour = max(a.armour, 2)        # allies take -2 from attacks until your next turn
def _guard_defense(engine, me, foe):
    for a in engine.allies(me):
        a.armour = max(a.armour, 2)        # allies gain Armour 2

def _intercept_setup(engine, me, foe):
    me._intercept = True                   # next time an ally is attacked, I defend

def _fortress_effect(engine, me, foe):
    me._fortress = True                    # I take the next hit meant for an ally
def _fortress_defense(engine, me, foe):
    for a in engine.allies(me):
        engine.heal(a, 2)

def _rally_effect(engine, me, foe):
    for a in engine.allies(me):
        if a.position == 'frontline':
            a.next_attack_bonus += 2
def _rally_defense(engine, me, foe):
    for a in engine.allies(me):
        if a.position == 'backline':
            a.next_attack_bonus += 2

def _trample_effect(engine, me, foe):
    if foe.collapsed:                      # this attack defeated the defender
        others = [x for x in engine.enemies(me) if x is not foe and x.position == 'frontline']
        if others:
            engine.deal(others[0], 3)
def _trample_defense(engine, me, foe):
    foe.position = 'backline'              # push the attacker back

def _charge_move(engine, me, foe):
    me.position = 'frontline'
    foe.position = 'frontline'

# --- Blue: tempo, control, AoE ---
def _interrupt_effect(engine, me, foe):
    foe.skip_turns += 1                    # target loses their next turn
    me.cannot_defend = True                # you can't defend until your next turn
def _interrupt_defense(engine, me, foe):
    engine.initiative_shift(me, 3)         # Initiative Shift +3 (positive: minimal in sim)

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
    wounds = [c for c in me.hand if c.is_status and c.name == 'WOUND']
    drop = wounds[0] if wounds else next((c for c in me.hand if not c.is_status), None)
    if drop is not None:
        me.hand.remove(drop); me.discard.append(drop)
        c = me.draw_one(engine.rng)
        if c:
            me.hand.append(c)              # discard 1 (a Wound if held), draw 1
def _study_defense(engine, me, foe):
    foe._predictable_to = me               # Predictable: I read this foe's next reveal

def _profile_effect(engine, me, foe):
    engine.scry(me, me, 2)
def _profile_defense(engine, me, foe):
    foe.staggered = True                   # attacker can't defend the next hit

def _refract_effect(engine, me, foe):
    foe.next_attack_bonus -= 3             # defender's next attack deals -3
def _refract_defense(engine, me, foe):
    foe.next_attack_bonus -= 3

# --- Green: ongoing support, tempo, position ---
def _synchrony_effect(engine, me, foe):
    me.ongoing.append({'kind': 'synchrony', 'owner': me})
def _synchrony_defense(engine, me, foe):
    me.resist += 1

def _rooted_oath_effect(engine, me, foe):
    me.ongoing.append({'kind': 'rooted_oath', 'owner': me, 'anchor': me.position})
def _rooted_oath_defense(engine, me, foe):
    pool = [a for a in engine.allies(me) if a.position == me.position] or [me]
    engine.heal(min(pool, key=lambda a: a.hp), 3)

def _urgency_effect(engine, me, foe):
    a = _best_attacker(engine.allies(me))
    if a:
        engine.initiative_shift(a, 3)      # positive: minimal in sim
def _urgency_defense(engine, me, foe):
    engine.initiative_shift(me, 3)

def _delay_effect(engine, me, foe):
    engine.initiative_shift(foe, -3)       # defender skips (negative shift)
def _delay_defense(engine, me, foe):
    engine.initiative_shift(foe, -3)

def _communion_effect(engine, me, foe):
    for a in _team(engine, me):
        engine.scry(a, a, 1)               # party scry
def _communion_defense(engine, me, foe):
    for a in _team(engine, me):
        a.next_attack_bonus += 2           # you and allies +2 damage next attack

def _mirror_step_effect(engine, me, foe):
    for c in (me, foe):
        c.position = 'backline' if c.position == 'frontline' else 'frontline'

def _patience_dmg(engine, me, foe):
    bonus = 0 if getattr(me, '_attacked_last', False) else 4   # +4 if you waited
    return me.eff('soul') + roll(4, engine.rng) + bonus
def _patience_defense(engine, me, foe):
    me.position = 'backline' if me.position == 'frontline' else 'frontline'


# ============================ REGISTRY =======================================

def build_cards():
    C = {}

    def add(*a, **k):
        c = Card(*a, **k)
        C[c.name] = c

    # Frost — Red
    add("SACRIFICE STRIKE", 'R', 'body', 'melee', 8,
        effect=_sacrifice_strike_effect, defense=_sacrifice_strike_defense)
    add("BLOOD IN THE GAP", 'R', 'body', 'ranged', 2,
        effect=_blood_in_the_gap_effect, defense=_blood_in_the_gap_defense)
    add("BURN BRIGHT", 'R', 'body', 'ranged', 6, damage=_burn_bright_dmg)
    add("SPARK OF VIOLENCE", 'R', 'body', 'both', 4,
        effect=_spark_effect, defense=_spark_effect)
    # Frost — Blue
    add("AXIOM", 'B', 'mind', 'both', 2, effect=_axiom_effect, defense=_axiom_defense)
    add("DEFLECT", 'B', 'mind', 'melee', 4,
        effect=_deflect_effect, defense=_deflect_defense)
    add("REALIGNMENT", 'B', 'mind', 'both', 4, effect=_realignment_effect)  # def DEAD (allies)
    add("CLIMB", 'B', 'mind', 'both', 4, defense=_climb_defense)            # effect ~ deck-order, DEAD
    add("FRACTURE", 'B', 'mind', 'ranged', 4, damage=_fracture_dmg)
    # Frost — Green
    add("TWIN STRIKE", 'G', 'soul', 'melee', None, damage=_twin_strike_dmg,
        defense=_twin_strike_defense)   # def buffs next ally (team play)

    # Steele — Red
    add("BLOOD TITHE", 'R', 'body', 'both', 4,
        effect=_blood_tithe_effect, defense=_blood_tithe_defense)
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
    add("ANTICIPATE", 'B', 'mind', 'melee', 4, defense=_anticipate_defense)   # effect DEAD (info)
    # Steele — Green
    add("SPIRAL CURRENT", 'G', 'soul', 'both', 4, effect=_spiral_current_effect)  # def DEAD
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
    add("EQUAL FOOTING", 'R', 'body', 'both', 4,
        damage=_equal_footing_dmg, defense=_equal_footing_defense)
    add("PRESS THE WOUND", 'R', 'body', 'melee', 4,
        damage=_press_the_wound_dmg, defense=_press_the_wound_defense)
    # Mire — Blue
    add("PARTITION", 'B', 'mind', 'both', 2,
        effect=_partition_effect, defense=_partition_defense)
    add("TAINT", 'B', 'mind', 'ranged', 2,
        effect=_taint_effect, defense=_taint_defense)
    add("ERODE", 'B', 'mind', 'both', 4,
        effect=_erode_effect, defense=_erode_effect)

    # Green support kit (team play)
    add("RESONATE", 'G', 'soul', 'ranged', 4,
        effect=_resonate_effect, defense=_resonate_defense)
    add("SUPPORT", 'G', 'soul', 'ranged', 4,
        effect=_support_effect, defense=_support_defense)
    add("CONDUCT", 'G', 'soul', 'both', 6,
        effect=_conduct_effect, defense=_conduct_defense)
    add("WITNESS", 'G', 'soul', 'melee', 4,
        effect=_witness_effect, defense=_witness_defense)
    add("SHARED BURDEN", 'G', 'soul', 'both', 6,
        effect=_shared_burden_effect, defense=_shared_burden_defense)

    # --- Expanded set: Red ---
    add("STRIKE", 'R', 'body', 'melee', 8, defense=_strike_defense)
    add("GUARD", 'R', 'body', 'melee', 4, effect=_guard_effect, defense=_guard_defense)
    add("INTERCEPT", 'R', 'body', 'melee', 4,
        effect=_intercept_setup, defense=_intercept_setup)
    add("FORTRESS STANCE", 'R', 'body', 'melee', 4,
        effect=_fortress_effect, defense=_fortress_defense)
    add("RALLY", 'R', 'body', 'both', 4, effect=_rally_effect, defense=_rally_defense)
    add("TRAMPLE", 'R', 'body', 'melee', 6,
        effect=_trample_effect, defense=_trample_defense)
    add("CHARGE", 'R', 'body', 'both', 4, effect=_charge_move, defense=_charge_move)
    # --- Expanded set: Blue ---
    add("INTERRUPT", 'B', 'mind', 'both', 2,
        effect=_interrupt_effect, defense=_interrupt_defense)
    add("CHAIN", 'B', 'mind', 'both', 2, effect=_chain_effect, defense=_chain_defense)
    add("CALCULATE", 'B', 'mind', 'ranged', 4,
        effect=_calculate_effect, defense=_calculate_defense)
    add("ANALYZE", 'B', 'mind', 'both', 2, effect=_analyze_effect)
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

    # Status card
    add("WOUND", None, None, None, None, is_status=True)

    return C


FROST_DECK = [
    "SACRIFICE STRIKE", "BLOOD IN THE GAP", "BURN BRIGHT", "SPARK OF VIOLENCE",
    "AXIOM", "DEFLECT", "REALIGNMENT", "CLIMB", "FRACTURE", "TWIN STRIKE",
]

STEELE_DECK = [
    "FORGET", "BLOOD TITHE", "GAMBLER'S RUIN", "REPEL", "PAIN IS FUEL",
    "PARADOX", "SPIRAL CURRENT", "ALIGN", "ANTICIPATE", "RENEWAL",
]

MIRE_DECK = [
    "BALANCE", "WITHER", "MOCKERY", "REND", "EQUAL FOOTING",
    "PRESS THE WOUND", "PARTITION", "TAINT", "ERODE",
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
    "TWIN STRIKE", "SPIRAL CURRENT", "MOCKERY",      # 3 green
    "PAIN IS FUEL", "GAMBLER'S RUIN",                # 2 red
]
ADEPT_DECK = [
    "TWIN STRIKE", "SPIRAL CURRENT", "BALANCE", "MOCKERY",  # 4 green
    "PAIN IS FUEL", "GAMBLER'S RUIN", "BLOOD TITHE",        # 3 red
    "PARADOX", "ALIGN",                                     # 2 blue
]

# WARDEN — a dedicated green-support build (Soul 4), to test whether green's real
# support kit + a support-piloting brain makes it the team anchor its identity
# claims. 7 green (5 support + attacker + taunt), 1 red, 1 blue.
WARDEN_DECK = [
    "RESONATE", "SUPPORT", "CONDUCT", "WITNESS", "SHARED BURDEN",
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
VANGUARD_DECK = [   # Body 4 — front-line tank/protection + a little sustain
    "STRIKE", "GUARD", "INTERCEPT", "FORTRESS STANCE", "RALLY", "TRAMPLE",
    "WITNESS", "RENEWAL", "PARADOX",
]
VANGUARD_STATS = dict(body=4, soul=3, mind=2)
TEMPO_DECK = [      # Mind 4 — control/tempo denial
    "INTERRUPT", "CHAIN", "CALCULATE", "PROFILE", "REFRACT", "AXIOM",
    "DELAY", "PARADOX", "PAIN IS FUEL",
]
TEMPO_STATS = dict(mind=4, soul=3, body=2)

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
}
