"""
Team-battle policies. Same brains, but now they must choose a TARGET, and their
defense naturally models blocking capacity (a combatant attacked several times
between its turns spends a card each block, so hands run dry — the thing the 1v1
sim couldn't show).

    choose_action(battle, me) -> ('attack', card, target) | ('move',)
                                 | ('destroy_injury',) | None
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
        if forced is not None and not forced.collapsed and not forced._partition_shield:
            return forced
        # Team plan (Drew): pick a target at random and pile on — stay locked
        # while they're still standing. The instant they collapse, the lock
        # drops and the next pick is random again, over everyone still alive
        # in play (including the one who just went down — they're back in
        # the pool, not specially hunted or specially spared).
        cur = battle.team_target.get(me.team)
        if cur is not None and not cur.collapsed and not cur.is_dead and not cur._partition_shield:
            return cur
        pool = [c for c in battle.targetable(me) if not c._partition_shield]
        if not pool:
            pool = battle.targetable(me)   # everyone shielded somehow — fall back rather than stall
        if not pool:
            return None
        # Retaliation heuristic (experiment, Drew): an instinct-driven creature
        # shouldn't re-roll a fresh random target the instant its current one
        # collapses — it should go after whoever's actually been hurting it.
        # This also has a real side effect on the death-rate problem: a random
        # re-lock can land right back on the character who just went down
        # (they're still in the pool), which is the only way Death actually
        # triggers (a second hit while already Collapsed); retaliating against
        # the last live attacker instead means the just-downed character isn't
        # the default next target, giving them real room to be revived before
        # anything can finish them off. Deliberately an explicit opt-in flag
        # (`me.retaliates`), not inferred from a low Mind stat — several real
        # ROSTER player archetypes (volk/adept/warden/vanguard) have Mind 2 for
        # unrelated reasons, and inferring from the stat silently changed their
        # established behavior and broke the regression suite the first time
        # this was tried.
        if getattr(me, 'retaliates', False):
            last = getattr(me, '_last_attacked_by', None)
            if last is not None and last in pool and not last.collapsed:
                battle.team_target[me.team] = last
                return last
            # No valid retaliation target (opening turn, or the last attacker
            # is themselves down) — still avoid defaulting onto someone
            # already Collapsed if a standing target exists. Same reasoning
            # as the retaliation branch: a Collapsed character shouldn't be
            # the instinctive next target just because they're in the pool.
            standing = [c for c in pool if not c.collapsed]
            if standing:
                pick = battle.rng.choice(standing)
                battle.team_target[me.team] = pick
                return pick
        pick = battle.rng.choice(pool)
        battle.team_target[me.team] = pick if not pick.collapsed else None
        return pick

    def choose_action(self, battle, me):
        # Staggered no longer routes through here — the engine skips that
        # turn's action itself, before this is ever called.
        target = self._pick_target(battle, me)
        if target is not None:
            atks = legal_attacks_team(battle, me, target)
            if atks:
                # value = damage + a nudge for effects that matter in teams
                return ('attack', max(atks, key=lambda c: self._value(battle, me, target, c)), target)
        # no legal attack: clear an Injury, then an Exhaust, or move
        if any(c.is_status and c.name == 'INJURY' for c in me.hand):
            return ('destroy_injury',)
        if any(c.is_status and c.name == 'EXHAUST' for c in me.hand):
            return ('destroy_exhaust',)
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
        elif card.name in ("SHARED BURDEN", "INTERCEPT", "FORTRESS STANCE"):
            v += 6 if big_threat else 1         # tank/redirect a dying ally's hit
        elif card.name in ("RESONATE", "SUPPORT", "CONDUCT", "COMMUNION"):
            v += 4                              # green team buffs / card advantage
        elif card.name in ("GUARD", "RALLY"):
            v += 3 if hurt else 0              # protection only when an ally's in danger
        elif card.name in ("INTERRUPT", "DELAY"):
            v += 4                              # tempo denial — skip an enemy
        elif card.name == "CHAIN":
            v += 3 if len(battle.enemies(me)) > 1 else 0   # AoE splash
        elif card.name == "TRAMPLE":
            v += 3 if target.hp <= 8 else 0     # finisher that carries over
        elif card.name in ("TWIN STRIKE", "SYNCHRONY", "ROOTED OATH"):
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
