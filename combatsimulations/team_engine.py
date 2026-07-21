"""
Tales Untold — Team Battle engine (N-vs-N).

Extends the duel engine to team combat, which is where the mechanics the 1v1 sim
can't see come alive: ally-support effects (green's whole kit), taunts/redirects,
and hand-size-as-blocking-capacity (multiple enemies attack you between your
turns; every block costs a card).

Design: reuses engine.Combatant / Card / roll / RULING unchanged, and exposes the
SAME effect-facing API as engine.Duel (deal, heal, insert_injury, allies,
enemies, _say, rng, cards). So one set of card effects in content.py serves both
engines — ally effects route through engine.allies(me), which is empty in a duel
(no behavior change there) and populated here.

Policies for teams implement:
    choose_action(battle, me) -> ('attack', card, target) | ('move',)
                                 | ('destroy_injury',) | None
    choose_defense(battle, me, attacker) -> card | None
    name_axiom_color(battle, me, foe) -> 'R'|'B'|'G'
"""

import random

from engine import (roll, RULING, can_attack, _ongoing_support_tick,
                    _apply_shift, _reposition_after, _rotate_current, _leave_wheel,
                    _join_wheel, _clear_ongoing_on_collapse)


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
        self.injury_card = cards.get('INJURY')
        self.pending_turns = []
        self.queue = []
        self.team_target = {0: None, 1: None}   # each side's shared focus-fire pick (team_policies.py, _pick_target)
        self._resolving = None   # whoever's turn is currently resolving (see engine._apply_shift)
        # RETALIATE/WARSONG/REBUTTAL: "the turn immediately before yours" — see the
        # matching comment in engine.py's Duel.__init__ for the full mechanism.
        self._prior_turn_hit = {'actor': None, 'target': None, 'hit': False}
        self._this_turn_hit = {'actor': None, 'target': None, 'hit': False}

    # --- team API (shared shape with Duel) ---
    def living(self, team):
        return [c for c in self.teams[team] if not c.collapsed]

    def allies(self, me):
        return [c for c in self.teams[me.team] if c is not me and not c.collapsed]

    def downed_allies(self, me):
        """Collapsed-but-not-dead allies — for RENEWAL's revival heal. A
        separate pool from allies() deliberately, same reasoning as
        targetable(): ordinary ally-targeting should never see a Collapsed
        teammate, but a card written specifically to revive one needs to."""
        return [c for c in self.teams[me.team] if c is not me and c.collapsed and not c.is_dead]

    def enemies(self, me):
        return [c for c in self.teams[1 - me.team] if not c.collapsed]

    def targetable(self, me):
        """Everyone on the enemy side still worth aiming at — living or
        Collapsed, just not dead. A separate pool from enemies() deliberately:
        normal support-card/ally logic should never see a Collapsed character,
        but target *selection* (team_policies.py, _pick_target) draws from
        this wider pool — a downed enemy is back in play for a fresh random
        pick, not specially hunted or specially spared."""
        return [c for c in self.teams[1 - me.team] if not c.is_dead]

    def _say(self, msg):
        self.log.append(msg)

    # --- damage / heal (identical semantics to Duel) ---
    def deal(self, target, amount, unpreventable=False, source=None):
        if amount <= 0:
            return 0
        # Redirect and shield are ATTACK-damage defenses — unpreventable damage
        # (bleed, thorns, status, HP costs) is not an attack, so it is neither
        # redirected nor tanked; it lands on the original target, full.
        if not unpreventable:
            # Shared Burden: a queued redirect sends this ally's next hit to the tank.
            rt = getattr(target, '_damage_redirect', None)
            if rt is not None and not rt.collapsed and rt is not target:
                target._damage_redirect = None
                self._say(f"    SHARED BURDEN: {target.name}'s damage -> {rt.name}")
                return self.deal(rt, amount, unpreventable, source)
            # Fortress Stance: a standing ally has volunteered to eat the next hit.
            for f in self.allies(target):
                if getattr(f, '_fortress', False):
                    f._fortress = False
                    self._say(f"    FORTRESS: {f.name} takes the hit for {target.name}")
                    return self.deal(f, amount, unpreventable, source)
        if not unpreventable and target.resist > 0:
            amount = amount // 2
            target.resist -= 1
        if not unpreventable and target._damage_floor is not None:
            cap = max(0, target.hp - target._damage_floor)
            amount = min(amount, cap)
        pre = target.hp
        was_collapsed = target.collapsed
        target.hp -= amount
        if pre > 0 and target.hp < 0 and not was_collapsed:
            target.hp = 0
        if target.hp <= 0 and not target.collapsed:
            target.collapsed = True
            _clear_ongoing_on_collapse(target)
            self._say(f"    {target.name} COLLAPSES")
            _leave_wheel(self, self.queue, target)
        elif was_collapsed and not target.is_dead and target.hp <= target.death_floor():
            # Only reachable already-Collapsed — a standing combatant is
            # protected from dying on the hit that drops them. Permanent —
            # heal() refuses to revive a dead combatant.
            target.is_dead = True
            self._say(f"    {target.name} DIES")
        return amount

    def heal(self, target, amount, source=None):
        # Death is permanent (rules/combat.md, Collapse & Death) — unlike
        # Collapse, nothing heals it. A dead combatant just doesn't respond.
        if target.is_dead:
            return
        # Collapse can be healed out of ("You may be healed back into combat")
        # — only revive on a healed total that actually clears 0; anything
        # less just softens the Collapse state.
        target.hp = min(target.max_hp, target.hp + amount)
        if target.collapsed and target.hp > 0:
            target.collapsed = False
            # Revived one slot after whoever healed them, not straight into the
            # live rotation — the marker has to complete a full lap before it
            # reaches them again (Drew: they shouldn't get to act until it does).
            _join_wheel(self.queue, target, after=source)

    def insert_injury(self, target):
        if self.injury_card is None:
            return
        target.deck.insert(0, self.injury_card)   # bottom of deck — deck.pop() draws from the end

    def scry(self, actor, owner, x):
        seen = [owner.deck.pop() for _ in range(min(x, len(owner.deck)))]
        if not seen:
            return seen
        plan = actor.policy.scry_plan(self, actor, owner, seen)
        top, bottom = plan[0], plan[1]
        binned = plan[2] if len(plan) > 2 else []
        for c in binned:
            owner.discard.append(c)
        for c in bottom:
            owner.deck.insert(0, c)
        for c in top:
            owner.deck.append(c)
        return seen

    def initiative_shift(self, target, amount):
        _apply_shift(self, self.queue, target, amount)

    def reposition_after(self, me, target):
        _reposition_after(self.queue, me, target)

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
        _ongoing_support_tick(self, who)

    # --- one attack, at a chosen target ---
    def attack(self, attacker, defender, card):
        attacker.hand.remove(card)
        attacker._attacked_this = True
        attacker._last_hit = 0

        if defender._weathered:   # WEATHERED: heal 2 each time attacked, whatever the outcome
            self.heal(defender, 2)

        # Blind resolves before Evade (rules/card-glossary.md, Blind) — see
        # engine.py's Duel.attack() for the full reasoning and the noted
        # simplification (stack consumed on next attack, no wall-clock expiry).
        if attacker.blind > 0:
            attacker.blind -= 1
            if roll(2, self.rng) == 1:
                self._say(f"{attacker.name} plays {card.name} ({card.color}) at {defender.name}")
                self._say(f"  {attacker.name} is BLIND — attack fails entirely")
                attacker.discard.append(card)
                attacker.last_color = card.color
                attacker.attack_history[card.color] += 1
                return

        was_staggered = defender.staggered
        # Evade resolves before the defender selects a card. It only reads
        # `defender.evade` (a token count), never the card's color, so it is
        # unaffected by when the reveal fields below get set.
        if defender.evade > 0:
            defender.evade -= 1
            if roll(2, self.rng) == 1:
                self._say(f"{attacker.name} plays {card.name} ({card.color}) at {defender.name}")
                self._say(f"  {defender.name} EVADES")
                attacker.discard.append(card)
                attacker.last_color = card.color
                attacker.attack_history[card.color] += 1
                defender._damage_floor = None
                return

        def_card = None
        if not defender.collapsed and not defender.staggered and not defender.cannot_defend:
            if defender._anticipating:   # ANTICIPATE: draw before defending, every qualifying attack
                c = defender.draw_one(self.rng)
                if c:
                    defender.hand.append(c)
            def_card = defender.policy.choose_defense(self, defender, attacker)
            if def_card is not None and defender.axiom_ban and def_card.color == defender.axiom_ban:
                def_card = None
        if was_staggered:
            defender.staggered = False
            self._say(f"    {defender.name} was Staggered — this attack goes undefended, then it clears")

        # Reveal: both cards flip face-up "simultaneously," in code terms right
        # here, before anything (including FORGET, later) looks at them.
        attacker.discard.append(card)
        attacker.last_color = card.color
        attacker.attack_history[card.color] += 1
        self._say(f"{attacker.name} plays {card.name} ({card.color}) at {defender.name}")

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
            # see engine.py's Duel.attack() for why this is rolled here
            attacker._redirect_dmg = card.damage(self, attacker, defender)
            if not defender._no_defensive_bonus:   # UNNAME
                def_card.defense(self, defender, attacker)
            attacker._redirect_dmg = None
        else:  # tie
            card.effect(self, attacker, defender)
            if not defender._no_defensive_bonus:   # UNNAME
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
        # "Instead of a tie, you win" — see engine.py's Duel.rps() for the full
        # reasoning. EQUAL FOOTING works either side; ADAPT is Effect-only, so
        # it only ever counts on the attacker side. Both-sided claims cancel out.
        if base == 'tie':
            atk_wins_tie = atk_card.name in ('EQUAL FOOTING', 'ADAPT')
            def_wins_tie = def_card.name == 'EQUAL FOOTING'
            if atk_wins_tie and not def_wins_tie:
                base = 'attacker'
            elif def_wins_tie and not atk_wins_tie:
                base = 'defender'
        return base

    def _resolve_attacker_win(self, attacker, defender, card):
        self._this_turn_hit = {'actor': attacker, 'target': defender, 'hit': True}
        dmg = card.damage(self, attacker, defender) + attacker.next_attack_bonus
        attacker.next_attack_bonus = 0
        if defender._rend_guard:
            defender._rend_guard = False
            self.insert_injury(defender)
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
        self.queue = list(self.order)   # queue[0] = next to act; rotates each turn
        self.pending_turns = []
        while self.turn_count < self.max_turns:
            if not self.queue:      # defensive: shouldn't happen, win-check fires first
                return self._finish(bool(self.living(0)), bool(self.living(1)))
            who = self.queue[0]
            if not who.collapsed:
                self.take_turn(who)
            a, b = bool(self.living(0)), bool(self.living(1))
            if not a or not b:
                return self._finish(a, b)
            _rotate_current(self, self.queue, who)
            self.turn_count += 1
            while self.pending_turns and self.turn_count < self.max_turns:
                extra = self.pending_turns.pop(0)
                if not extra.collapsed:
                    self.take_turn(extra)
                a, b = bool(self.living(0)), bool(self.living(1))
                if not a or not b:
                    return self._finish(a, b)
                if extra in self.queue:
                    self.queue.remove(extra)
                    self.queue.append(extra)
                self.turn_count += 1
        return self._finish(bool(self.living(0)), bool(self.living(1)))

    def take_turn(self, who):
        self._resolving = who   # see engine._apply_shift — covers bonus turns, not just queue[0]
        self._prior_turn_hit = self._this_turn_hit   # freeze last turn's result before this turn can overwrite it
        self._this_turn_hit = {'actor': who, 'target': None, 'hit': False}
        who.cannot_defend = False
        who._anticipating = False        # ANTICIPATE, UNNAME, WEATHERED: self-clearing, "until my next turn"
        who._no_defensive_bonus = False
        who._weathered = False
        shielded = who._partition_shield_target   # PARTITION: caster clears the shield they granted
        if shielded is not None:
            shielded._partition_shield = False
            who._partition_shield_target = None
        who._attacked_last = getattr(who, '_attacked_this', False)
        who._attacked_this = False
        if who._shift_skip or who.skip_turns > 0:
            who._shift_skip = False
            if who.skip_turns > 0:
                who.skip_turns -= 1
            return
        self.start_of_turn(who)
        if who.collapsed:
            return
        who.draw_to_hand(self.rng)
        if who.staggered:
            who.staggered = False
            self._say(f"{who.name} is Staggered — this turn's attack is skipped")
            who.must_target_frontline = False
            who._forced_target = None
            return
        extra_actions = 0
        while True:
            action = who.policy.choose_action(self, who)
            if action is None:
                # Wait (rules/combat.md): forgo the action to reposition -X for a
                # combo cadence. Choosing X is a tactical, table-only call; these
                # brains never plan one, so a forced pass is just a lost turn
                # (X=0). Tactical Wait is intentionally unmodeled.
                self._say(f"{who.name} waits")
            elif action[0] == 'attack':
                _, card, target = action
                # Targeting a Collapsed-but-not-dead enemy is a deliberate,
                # policy-level choice (team_policies.py, _pick_target's random
                # pile-on) — not redirected away from here. A Collapsed target
                # auto-hits (rules/combat.md, Collapse & Death), which attack()
                # already handles via its own `not defender.collapsed` gate.
                self.attack(who, target, card)
            elif action[0] == 'move':
                who.position = 'backline' if who.position == 'frontline' else 'frontline'
            elif action[0] == 'destroy_injury':
                for i, c in enumerate(who.hand):
                    if c.is_status and c.name == 'INJURY':
                        who.hand.pop(i)
                        break
            who.must_target_frontline = False
            who._forced_target = None   # taunt is one-shot: consumed by this turn
            # TRAMPLE: an extra action within THIS turn, not a wheel bonus turn —
            # capped so a bug can't hang the sim, though nothing should ever
            # realistically chain that far.
            if not who._bonus_action or who.collapsed or extra_actions >= 5:
                break
            who._bonus_action = False
            extra_actions += 1
            self._say(f"{who.name} gained another action (TRAMPLE)")

    def _finish(self, a_alive, b_alive):
        if a_alive and not b_alive:
            self.result = 0
        elif b_alive and not a_alive:
            self.result = 1
        else:
            self.result = 'TIE'
        return self.result
