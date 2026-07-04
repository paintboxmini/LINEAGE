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
    if foe.hand and not warded(foe):
        foe.discard.append(foe.hand.pop(engine.rng.randrange(len(foe.hand))))


def _forget_defense(engine, me, foe):
    # exile the attacker's just-played card (top of their discard)
    if foe.discard:
        foe.exile.append(foe.discard.pop())


def _blood_tithe_effect(engine, me, foe):
    engine.deal(me, 2, unpreventable=True)
    RULING("blood-tithe-dead-heal",
           "BLOOD TITHE effect 'heal an ally for 4' has no legal target in a duel "
           "(You Are Not Your Own Ally) — the 4 HP is wasted; only the 2 self-"
           "damage applies.")


def _blood_tithe_defense(engine, me, foe):
    me.ongoing.append({'kind': 'blood_tithe', 'controller': me, 'victim': foe})


def _gamblers_ruin_dmg(engine, me, foe):
    total = me.body + roll(4, engine.rng)
    rerolls = 0
    last = total
    while rerolls < 3 and (last % 2 == 1):
        last = roll(4, engine.rng)
        total += last
        rerolls += 1
    RULING("gamblers-ruin-explode",
           "GAMBLER'S RUIN: every odd result (including added dice) triggers "
           "another d4, capped at 3 extra rolls total (Drew ruling).")
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
    if len(me.hand) < me.effective_hand_size():
        c = me.draw_one(engine.rng)
        if c:
            me.hand.append(c)
    RULING("align-scry-simplified",
           "ALIGN's scry-2 information step is simplified: the conditional draw is "
           "modeled, the scry ordering is not (no hidden-info policy consumes it).")


def _align_defense(engine, me, foe):
    me.next_attack_bonus += 2


def _anticipate_defense(engine, me, foe):
    if not warded(foe):
        foe.next_attack_bonus -= 3  # target's next attack deals -3


def _renewal_defense(engine, me, foe):
    if foe.hand:
        foe.discard.append(foe.hand.pop(engine.rng.randrange(len(foe.hand))))


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
    add("AXIOM", 'B', 'mind', 'both', 2, effect=_axiom_effect)
    add("DEFLECT", 'B', 'mind', 'melee', 4,
        effect=_deflect_effect, defense=_deflect_defense)
    add("REALIGNMENT", 'B', 'mind', 'both', 4, effect=_realignment_effect)  # def DEAD (allies)
    add("CLIMB", 'B', 'mind', 'both', 4, defense=_climb_defense)            # effect ~ deck-order, DEAD
    add("FRACTURE", 'B', 'mind', 'ranged', 4, damage=_fracture_dmg)
    # Frost — Green
    add("TWIN STRIKE", 'G', 'soul', 'melee', None, damage=_twin_strike_dmg)  # def DEAD (allies)

    # Steele — Red
    add("BLOOD TITHE", 'R', 'body', 'both', 4,
        effect=_blood_tithe_effect, defense=_blood_tithe_defense)
    add("GAMBLER'S RUIN", 'R', 'body', 'melee', None,
        damage=_gamblers_ruin_dmg, defense=_gamblers_ruin_defense)
    add("REPEL", 'R', 'body', 'melee', 2,
        effect=_repel_effect, defense=_repel_effect)
    add("PAIN IS FUEL", 'R', 'body', 'both', 6,
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
    add("RENEWAL", 'G', 'soul', 'both', 4, defense=_renewal_defense)              # effect DEAD (allies)

    return C


FROST_DECK = [
    "SACRIFICE STRIKE", "BLOOD IN THE GAP", "BURN BRIGHT", "SPARK OF VIOLENCE",
    "AXIOM", "DEFLECT", "REALIGNMENT", "CLIMB", "FRACTURE", "TWIN STRIKE",
]

STEELE_DECK = [
    "FORGET", "BLOOD TITHE", "GAMBLER'S RUIN", "REPEL", "PAIN IS FUEL",
    "PARADOX", "SPIRAL CURRENT", "ALIGN", "ANTICIPATE", "RENEWAL",
]

FROST_STATS = dict(body=3, mind=3, soul=3)
STEELE_STATS = dict(body=4, mind=3, soul=2)
