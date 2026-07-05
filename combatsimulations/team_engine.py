"""
Tales Untold — Team Battle engine (N-vs-N).

Extends the duel engine to team combat, which is where the mechanics the 1v1 sim
can't see come alive: ally-support effects (green's whole kit), taunts/redirects,
and hand-size-as-blocking-capacity (multiple enemies attack you between your
turns; every block costs a card).

Design: reuses engine.Combatant / Card / roll / RULING unchanged, and exposes the
SAME effect-facing API as engine.Duel (deal, heal, shuffle_wound, allies,
enemies, _say, rng, cards). So one set of card effects in content.py serves both
engines — ally effects route through engine.allies(me), which is empty in a duel
(no behavior change there) and populated here.

Policies for teams implement:
    choose_action(battle, me) -> ('attack', card, target) | ('move',)
                                 | ('discard_wound',) | None
    choose_defense(battle, me, attacker) -> card | None
    name_axiom_color(battle, me, foe) -> 'R'|'B'|'G'
"""

import random

from engine import roll, RULING, can_attack


class Battle:
    def __init__(self, team_a, team_b, cards, seed=None, max_turns=600, log=None):
        self.rng = random.Random(seed)
        self.cards = cards
        self.teams = [list(team_a), list(team_b)]
        for t, team in enumerate(self.teams):
            for c in team:
                c.team = t
        self.all = self.teams[0] + self.teams[1]
        self.max_turns = max_turns
        self.log = log if log is not None else []
        self.turn_count = 0
        self.wound = cards.get('WOUND')

    # --- team API (shared shape with Duel) ---
    def living(self, team):
        return [c for c in self.teams[team] if not c.collapsed]

    def allies(self, me):
        return [c for c in self.teams[me.team] if c is not me and not c.collapsed]

    def enemies(self, me):
        return [c for c in self.teams[1 - me.team] if not c.collapsed]

    def _say(self, msg):
        self.log.append(msg)

    # --- damage / heal (identical semantics to Duel) ---
    def deal(self, target, amount, unpreventable=False, source=None):
        if amount <= 0:
            return 0
        if not unpreventable and target.resist > 0:
            amount = amount // 2
            target.resist -= 1
        if target._damage_floor is not None:
            cap = max(0, target.hp - target._damage_floor)
            amount = min(amount, cap)
        pre = target.hp
        target.hp -= amount
        if pre > 0 and target.hp < 0 and not target.collapsed:
            target.hp = 0
        if target.hp <= 0 and not target.collapsed:
            target.collapsed = True
            self._say(f"    {target.name} COLLAPSES")
        return amount

    def heal(self, target, amount):
        if target.collapsed:
            return
        target.hp = min(target.max_hp, target.hp + amount)

    def shuffle_wound(self, target):
        if self.wound is None:
            return
        target.deck.insert(self.rng.randint(0, len(target.deck)), self.wound)

    def initiative_shift(self, target, amount):
        n = len(self.all)
        skips = abs(amount) // n
        if amount < 0:
            target.skip_turns += skips

    # --- setup: one interleaved initiative wheel over everyone ---
    def setup(self):
        for c in self.all:
            c.build(self.cards, self.rng)
        rolls = {c: roll(6, self.rng) + c.soul for c in self.all}
        self.rng.shuffle(self.all)
        # highest first; ties -> higher Soul -> players... here just coin
        self.order = sorted(self.all, key=lambda c: (rolls[c], c.soul, self.rng.random()),
                            reverse=True)
        for c in self.all:
            c.draw_to_hand(self.rng)

    # --- start-of-turn ongoing ticks (Blood Tithe bleed, etc.) ---
    def start_of_turn(self, who):
        for o in [o for o in who.ongoing if o['kind'] == 'blood_tithe']:
            self.deal(o['controller'], 1, unpreventable=True)
            self.deal(o['victim'], 1, unpreventable=True)

    # --- one attack, at a chosen target ---
    def attack(self, attacker, defender, card):
        attacker.hand.remove(card)
        attacker.discard.append(card)
        attacker.last_color = card.color
        attacker.attack_history[card.color] += 1
        attacker._last_hit = 0
        self._say(f"{attacker.name} plays {card.name} ({card.color}) at {defender.name}")

        if defender.evade > 0:
            defender.evade -= 1
            if roll(2, self.rng) == 1:
                self._say(f"  {defender.name} EVADES")
                defender._damage_floor = None
                return

        def_card = None
        if not defender.collapsed and not defender.staggered:
            def_card = defender.policy.choose_defense(self, defender, attacker)
            if def_card is not None and defender.axiom_ban and def_card.color == defender.axiom_ban:
                def_card = None
        defender.staggered = False

        if def_card is None:
            self._resolve_attacker_win(attacker, defender, card)
            defender._damage_floor = None
            return

        defender.hand.remove(def_card)
        defender.discard.append(def_card)
        defender.last_color = def_card.color

        outcome = self._rps(card, def_card)
        if outcome == 'attacker':
            self._resolve_attacker_win(attacker, defender, card)
        elif outcome == 'defender':
            def_card.defense(self, defender, attacker)
        else:  # tie
            card.effect(self, attacker, defender)
            def_card.defense(self, defender, attacker)
        defender._damage_floor = None

    @staticmethod
    def _rps_base(atk, dfn):
        if atk == dfn:
            return 'tie'
        return 'attacker' if (atk, dfn) in {('B', 'R'), ('R', 'G'), ('G', 'B')} else 'defender'

    def _rps(self, atk_card, def_card):
        base = self._rps_base(atk_card.color, def_card.color)
        if (atk_card.special_reveal == 'paradox' or def_card.special_reveal == 'paradox') \
                and base != 'tie':
            base = 'defender' if base == 'attacker' else 'attacker'
        return base

    def _resolve_attacker_win(self, attacker, defender, card):
        dmg = card.damage(self, attacker, defender) + attacker.next_attack_bonus
        attacker.next_attack_bonus = 0
        if defender._rend_guard:
            defender._rend_guard = False
            self.shuffle_wound(defender)
            attacker._last_hit = 0
            card.effect(self, attacker, defender)
            return
        dealt = self.deal(defender, dmg)
        attacker._last_hit = dealt
        if defender.thorns > 0 and card.reach == 'melee':
            self.deal(attacker, defender.thorns, unpreventable=True)
        card.effect(self, attacker, defender)

    # --- main loop ---
    def run(self):
        self.setup()
        idx = 0
        n = len(self.order)
        while self.turn_count < self.max_turns:
            who = self.order[idx % n]
            if not who.collapsed:
                self.take_turn(who)
            a, b = bool(self.living(0)), bool(self.living(1))
            if not a or not b:
                return self._finish(a, b)
            idx += 1
            self.turn_count += 1
        return self._finish(bool(self.living(0)), bool(self.living(1)))

    def take_turn(self, who):
        if who.skip_turns > 0:
            who.skip_turns -= 1
            return
        self.start_of_turn(who)
        if who.collapsed:
            return
        who.draw_to_hand(self.rng)
        action = who.policy.choose_action(self, who)
        if action is None:
            pass
        elif action[0] == 'attack':
            _, card, target = action
            if target.collapsed:
                alt = self.enemies(who)
                if not alt:
                    return
                target = alt[0]
            self.attack(who, target, card)
        elif action[0] == 'move':
            who.position = 'backline' if who.position == 'frontline' else 'frontline'
        elif action[0] == 'discard_wound':
            for i, c in enumerate(who.hand):
                if c.is_status and c.name == 'WOUND':
                    who.discard.append(who.hand.pop(i))
                    break
        who.must_target_frontline = False
        who._forced_target = None   # taunt is one-shot: consumed by this turn

    def _finish(self, a_alive, b_alive):
        if a_alive and not b_alive:
            self.result = 0
        elif b_alive and not a_alive:
            self.result = 1
        else:
            self.result = 'TIE'
        return self.result
