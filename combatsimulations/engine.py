"""Combat state and resolution.

Implements `rules/combat.md` and `rules/card-glossary.md` as of 2026-09-06,
including that day's changes: the always-roll Blind/Evade order and Mutual
Miss, Immunity scoped to damage inside the pipeline, Cover Evade as a
persistent dodge distinct from the Evade keyword, and Down defending
normally.

Card Effects are prose and are not executed here — see cards.py. The engine
resolves the structured parts (who wins, how much damage lands, what the
pipeline does to it) and hands the Effect text to whoever is playing.
"""

import math
import random

from cards import Card

FRONT, BACK = 'Frontline', 'Backline'


class Combatant:
    def __init__(self, name, body, mind, soul, deck, position=FRONT, team='party'):
        self.name = name
        self.body, self.mind, self.soul = body, mind, soul
        self.team = team
        self.position = position

        # rules/character-creation.md: max HP = (3 x Body) + Soul + Mind
        self.max_hp = 3 * body + soul + mind
        self.hp = self.max_hp

        self.deck = list(deck)
        random.shuffle(self.deck)
        self.hand = []
        self.discard = []
        self.exiled = []

        # Stacking statuses, held as counts.
        self.deadly = 0
        self.weak = 0
        self.evade = 0
        self.resist = 0
        self.vulnerable = 0
        self.thorns = 0
        self.armour = 0
        self.ward = 0
        self.quick = 0            # banked free Move Positions
        self.blind = 0
        self.rooted = 0
        self.staggered = 0
        self.immunity = 0
        self.protect_for = None   # ally whose next hit this combatant takes
        self._protected_by = None  # set on the ally being shielded

        self.in_cover = False     # Cover Evade: persistent, never spent
        self.down = False
        self.dead = False
        self.acted_last_turn = False

    # ---- derived --------------------------------------------------------

    @property
    def hand_size(self):
        """rules/character-creation.md: hand size is Mind, minimum 2."""
        return max(2, self.mind)

    @property
    def death_threshold(self):
        """"If you reach negative half your Max HP (rounded up), you die.\""""
        return -math.ceil(self.max_hp / 2)

    def stat(self, name):
        return {'body': self.body, 'mind': self.mind, 'soul': self.soul}[name.lower()]

    def alive(self):
        return not self.dead

    # ---- deck ----------------------------------------------------------

    def draw_up(self, log=None):
        """"At the start of your turn, draw until you reach your maximum hand
        size. If your deck is empty, shuffle your discard pile into a new
        deck before drawing.\""""
        drawn = 0
        while len(self.hand) < self.hand_size:
            if not self.deck:
                if not self.discard:
                    break
                self.deck = self.discard
                self.discard = []
                random.shuffle(self.deck)
                if log:
                    log(f'{self.name} reshuffles their discard into a new deck.')
            self.hand.append(self.deck.pop())
            drawn += 1
        return drawn

    def playable(self, opponent):
        """Cards in hand whose Range is legal for the current positions."""
        return [c for c in self.hand if c.range_ok(self.position, opponent.position)]

    # ---- damage --------------------------------------------------------

    def take(self, amount, unpreventable=False, source=None, log=None):
        """Apply damage through the pipeline (`rules/combat.md`).

        reassignment -> Immunity -> Armour -> Resist/Vulnerable -> HP.

        Unpreventable damage bypasses the pipeline entirely: it was never
        attack damage, so none of the steps apply.
        """
        target = self

        if not unpreventable:
            # reassignment — the damage lands on someone else instead, in
            # full, before anything reduces it.
            guard = self._protected_by
            if guard is not None and guard.alive():
                if log:
                    log(f'{guard.name} takes the hit for {self.name} (Protect).')
                target = guard
                guard._protected_by = None
                self._protected_by = None

            # Immunity, held by whoever is actually receiving the damage.
            if target.immunity > 0 and amount > 0:
                target.immunity -= 1
                if log:
                    log(f'{target.name} is Immune — the damage is reduced to 0.')
                return 0

            if target.armour:
                amount = max(0, amount - target.armour)

            # One stack of each cancels the other first.
            r, v = target.resist, target.vulnerable
            cancel = min(r, v)
            r, v = r - cancel, v - cancel
            if r > 0:
                amount = amount // 2
                target.resist -= 1
            elif v > 0:
                amount = int(amount * 1.5)
                target.vulnerable -= 1

        before = target.hp
        target.hp -= amount

        # "A single attack cannot push a standing combatant below 0 HP."
        if not target.down and target.hp < 0:
            target.hp = 0

        dealt = before - target.hp
        if log and dealt:
            log(f'{target.name} takes {dealt} ({target.hp}/{target.max_hp} HP).')

        if target.hp <= 0 and not target.down:
            target.down = True
            if log:
                log(f'{target.name} Collapses.')
        if target.hp <= target.death_threshold:
            target.dead = True
            if log:
                log(f'{target.name} dies.')
        return dealt

    def heal(self, amount, log=None):
        was_down = self.down
        self.hp = min(self.max_hp, self.hp + amount)
        if was_down and self.hp > 0:
            self.down = False   # healing ends the Collapse; it does not stand you up
            if log:
                log(f'{self.name} is healed above 0 — still Down until they stand.')
        return amount

    def __str__(self):
        return self.name


# ---- attack resolution -------------------------------------------------

class Outcome:
    ATTACKER = 'attacker wins'
    DEFENDER = 'defender wins'
    TIE = 'tie'
    MUTUAL_MISS = 'mutual miss'


def d(sides, rng=random):
    return rng.randint(1, sides)


def roll_damage(attacker, card, rng=random):
    """Stat + die, with Deadly/Weak folded in. One stack of each cancels
    before either applies."""
    total = attacker.stat(card.stat) + (d(card.die, rng) if card.die else 0)

    deadly, weak = attacker.deadly, attacker.weak
    cancel = min(deadly, weak)
    deadly, weak = deadly - cancel, weak - cancel
    attacker.deadly = max(0, attacker.deadly - cancel - (1 if deadly else 0))
    attacker.weak = max(0, attacker.weak - cancel - (1 if weak else 0))
    if deadly:
        total += d(6, rng)
    elif weak:
        total -= d(6, rng)
    return max(0, total)


def resolve_attack(attacker, defender, atk_card, def_card, rng=random, log=print):
    """One exchange, following `rules/combat.md` Attack Resolution.

    `def_card` may be None — the defender cannot or chooses not to defend.
    Returns an Outcome.
    """
    log(f'{attacker.name} attacks {defender.name}.')

    # Step 3. Every check that applies actually rolls, whether or not it
    # ends up mattering: being attacked is what triggers them.
    atk_blind_miss = attacker.blind > 0 and d(2, rng) == 1
    if attacker.blind:
        attacker.blind -= 1

    evaded = False
    if defender.in_cover:
        # Cover Evade — rolls the same, but is never spent, and stands in
        # for held stacks while it lasts.
        evaded = d(2, rng) == 1
        if evaded:
            log(f'{defender.name} dodges from cover.')
    elif defender.evade > 0:
        defender.evade -= 1
        evaded = d(2, rng) == 1
        if evaded:
            log(f'{defender.name} evades.')

    def_blind_miss = False
    if defender.blind > 0 and def_card is not None:
        def_blind_miss = d(2, rng) == 1
        defender.blind -= 1

    # Resolution priority.
    if evaded:
        return _finish(Outcome.DEFENDER, attacker, defender, atk_card, def_card, log)
    if atk_blind_miss and def_blind_miss:
        log('Both miss — Mutual Miss. No damage, no Effect, no Defense Effect.')
        return _finish(Outcome.MUTUAL_MISS, attacker, defender, atk_card, def_card, log)
    if atk_blind_miss:
        log(f'{attacker.name} misses (Blind).')
        return _finish(Outcome.DEFENDER, attacker, defender, atk_card, def_card, log)
    if def_blind_miss:
        log(f'{defender.name} misses their block (Blind).')
        return _finish(Outcome.ATTACKER, attacker, defender, atk_card, def_card, log)
    if def_card is None:
        log(f'{defender.name} has no legal defense.')
        return _finish(Outcome.ATTACKER, attacker, defender, atk_card, def_card, log)

    # Step 5. Reveal.
    log(f'  {atk_card.name} ({atk_card.color}) vs {def_card.name} ({def_card.color})')
    if atk_card.ties(def_card):
        outcome = Outcome.TIE
    elif atk_card.beats(def_card):
        outcome = Outcome.ATTACKER
    elif def_card.beats(atk_card):
        outcome = Outcome.DEFENDER
    else:
        outcome = Outcome.TIE
    return _finish(outcome, attacker, defender, atk_card, def_card, log)


def _finish(outcome, attacker, defender, atk_card, def_card, log):
    """Apply the outcome, then discard both cards."""
    if outcome == Outcome.ATTACKER:
        dmg = roll_damage(attacker, atk_card)
        defender.take(dmg, source=attacker, log=log)
        if defender.thorns and (atk_card.range or '').strip().lower().startswith('melee'):
            log(f'{defender.name}\'s Thorns bites back.')
            attacker.take(defender.thorns, unpreventable=True, log=log)
        if atk_card.effect and atk_card.effect.lower() != 'none.':
            log(f'  Effect: {atk_card.effect}')
    elif outcome == Outcome.DEFENDER:
        log('  No damage.')
        if def_card and def_card.defense_effect and def_card.defense_effect.lower() != 'none.':
            log(f'  Defense Effect: {def_card.defense_effect}')
    elif outcome == Outcome.TIE:
        log('  Tie — no damage.')
        if atk_card.effect and atk_card.effect.lower() != 'none.':
            log(f'  Effect: {atk_card.effect}')
        if def_card and def_card.defense_effect and def_card.defense_effect.lower() != 'none.':
            log(f'  Defense Effect: {def_card.defense_effect}')

    attacker.discard.append(atk_card)
    if def_card is not None:
        defender.discard.append(def_card)
    return outcome
