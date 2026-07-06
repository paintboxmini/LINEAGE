"""
Team-battle policies. Same brains, but now they must choose a TARGET, and their
defense naturally models blocking capacity (a combatant attacked several times
between its turns spends a card each block, so hands run dry — the thing the 1v1
sim couldn't show).

    choose_action(battle, me) -> ('attack', card, target) | ('move',)
                                 | ('discard_wound',) | None
    choose_defense(battle, me, attacker) -> card | None
"""

from policies import est_damage, _BEATEN_BY, playable, ScryMixin


def legal_attacks_team(battle, me, target):
    if me.must_target_frontline and target.position != 'frontline':
        return []
    return [c for c in me.hand if not c.is_status and can_attack_t(me, target, c)]


def can_attack_t(attacker, target, card):
    if card.reach == 'both':
        return True
    both_front = attacker.position == 'frontline' and target.position == 'frontline'
    return both_front if card.reach == 'melee' else (not both_front)


class TeamTactician(ScryMixin):
    """Focus-fire the weakest reachable enemy; attack for max value; defend by
    recency read. Respects taunts (forced target). Composes with the shared
    ScryMixin for deck-manipulation decisions. Team analogue of the duel tactician."""
    name = "team_tactician"

    def _pick_target(self, battle, me):
        forced = getattr(me, '_forced_target', None)
        if forced is not None and not forced.collapsed:
            return forced
        foes = battle.enemies(me)
        if not foes:
            return None
        # focus fire: lowest effective HP first (secure kills, concentrate)
        return min(foes, key=lambda e: (e.hp, e.max_hp))

    def choose_action(self, battle, me):
        target = self._pick_target(battle, me)
        if target is not None:
            atks = legal_attacks_team(battle, me, target)
            if atks:
                # value = damage + a nudge for effects that matter in teams
                return ('attack', max(atks, key=lambda c: self._value(battle, me, target, c)), target)
        # no legal attack: clear a Wound if stuck, else reposition
        if any(c.is_status and c.name == 'WOUND' for c in me.hand):
            return ('discard_wound',)
        if me.hand:
            return ('move',)
        return None

    def _value(self, battle, me, target, card):
        # A support-aware valuation: play green's team cards when the team can use
        # them, not just when they beat max-damage. This is what lets green be
        # piloted as an anchor instead of a bad attacker.
        v = est_damage(me, card)
        allies = battle.allies(me)
        if not allies:
            return v + (2 if card.name == "AXIOM" else 0)
        hurt = [a for a in allies if a.hp < a.max_hp * 0.5]
        lowest = min(allies, key=lambda a: a.hp)
        big_threat = lowest.hp <= 6
        if card.name in ("WITNESS", "RENEWAL"):
            v += 7 if hurt else 1               # heals — huge when someone's low
        elif card.name == "SHARED BURDEN":
            v += 6 if big_threat else 1         # tank a dying ally's next hit
        elif card.name in ("RESONATE", "SUPPORT", "CONDUCT"):
            v += 4                              # team buffs / card advantage
        elif card.name == "TWIN STRIKE":
            v += 2
        elif card.name == "MOCKERY":
            v += 3 if big_threat else 1         # taunt heat off a dying ally
        elif card.name == "AXIOM":
            v += 2
        return v

    def choose_defense(self, battle, me, attacker):
        pred = attacker.last_color
        if pred is None:
            return None
        winners = [c for c in me.hand if not c.is_status and c.color == _BEATEN_BY[pred]]
        if winners:
            return min(winners, key=lambda c: est_damage(me, c))
        return None

    def name_axiom_color(self, battle, me, foe):
        return foe.last_color or 'B'


def make_team_policy(name="team_tactician"):
    return {"team_tactician": TeamTactician}[name]()
