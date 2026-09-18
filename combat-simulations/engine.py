"""Combat state and resolution.

Implements `rules/combat.md` and `rules/card-glossary.md` as of 2026-09-06,
including that day's changes: the always-roll Blind/Evade order and Mutual
Miss, Immunity scoped to damage inside the pipeline, Cover Evade as a
persistent dodge distinct from the Evade keyword, and Down defending
normally.

The engine resolves the structured parts — who wins, how much damage lands,
what the pipeline does to it. Card Effects are read by `effects.py` and run
from `_finish` below; a half that module cannot read is printed for whoever
is playing, which is what every card did before it existed.
"""

import math
import random

import effects as fx
from cards import Card

FRONT, BACK = 'Frontline', 'Backline'


class Pending:
    """Something a card left behind, waiting on an event.

    Two shapes share one container because they share one lifetime.

    A **reaction** carries ops and runs them when `event` fires on its
    holder — WEATHERED on being damaged, SEED on beginning a turn in the
    right place, Anchored at the start of every turn.

    A **restriction** carries no ops. The engine asks whether one is in
    force before doing something: playing a colour, moving, attacking,
    triggering a Defense Effect. It is a question the engine asks, not a
    thing that happens to a combatant.

    `owner` is whose turn the expiry is measured against, which is not
    always the holder. PARTITION reads "until *your* next turn" on the
    card that played it, so the restriction sits on the target and expires
    on the caster's turn.
    """

    __slots__ = ('event', 'ops', 'kind', 'owner', 'expires', 'uses', 'data',
                 'text', 'breaks_on_move')

    def __init__(self, event, owner, expires='combat', ops=(), kind=None,
                 uses=None, data=None, text='', breaks_on_move=False):
        self.event = event
        self.owner = owner
        self.expires = expires        # 'combat' | 'owner_next_turn' | 'once'
        self.ops = list(ops)
        self.kind = kind              # set on a restriction, None on a reaction
        self.uses = uses              # None = unlimited while it lasts
        self.data = data or {}
        self.text = text
        self.breaks_on_move = breaks_on_move

    def spend(self):
        if self.uses is not None:
            self.uses -= 1
        return self.uses is not None and self.uses <= 0

    def __repr__(self):
        return f'<Pending {self.kind or self.event}: {self.text}>'


# Restriction kinds the engine knows how to ask about.
NO_COLOR = 'no_color'            # cannot play this colour on the next reveal
NO_MOVE = 'no_move'              # cannot change position
NO_ATTACK = 'no_attack'          # cannot attack
NO_TARGET = 'no_target'          # cannot be attacked
NO_DEFENSE_EFFECT = 'no_defense_effect'
MUST_TARGET = 'must_target'      # must attack a named combatant if able
SKIP_DRAW = 'skip_draw'
IGNORE_FORCED_MOVE = 'ignore_forced_move'
WOUND_INSTEAD = 'wound_instead'  # next attack wounds rather than damages


class Combatant:
    def __init__(self, name, body, mind, soul, deck, position=FRONT, team='party',
                 rng=None):
        self.name = name
        self.body, self.mind, self.soul = body, mind, soul
        self.team = team
        self._position = position

        # Everything waiting on an event: Anchored, reactions, restrictions.
        self.pending = []

        self.hp = self.max_hp

        # Every shuffle this combatant ever makes comes from here. Using the
        # module-level random instead made --seed a lie: the deck order and
        # every reshuffle were outside the seeded stream, so the same seed
        # gave a different fight.
        self.rng = rng or random
        self.deck = list(deck)
        self.rng.shuffle(self.deck)
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

    # ---- position ------------------------------------------------------

    @property
    def position(self):
        return self._position

    def set_position(self, dest, log=None, forced=False):
        """The one way position changes, so Rooted and Anchored are paid
        wherever the movement came from.

        `rules/card-glossary.md`, Rooted: the next movement is cancelled and
        the charge is spent, forced movement included. Anchored: if you move,
        voluntarily or by an enemy effect, it ends immediately.
        """
        if dest == self._position:
            return False

        # CORNER and friends: a restriction that simply forbids it.
        locked = self.restriction(NO_MOVE)
        if locked is not None:
            if log:
                log(f'  {self.name} cannot change position right now.')
            return False

        if forced:
            # GROUNDING STANCE: ignore the next ability that forces a move.
            ignore = self.restriction(IGNORE_FORCED_MOVE)
            if ignore is not None:
                self.spend_restriction(ignore, log=log)
                if log:
                    log(f'  {self.name} plants — the forced movement is ignored.')
                return False

        if self.rooted > 0:
            self.rooted -= 1
            if log:
                log(f'  {self.name} is Rooted — the move is cancelled.')
            return False
        self._position = dest
        if log:
            log(f'  {self.name} moves to the {dest}.')
        self.break_anchors(log=log, reason='moved')
        return True

    def break_anchors(self, log=None, reason='moved'):
        """`rules/card-glossary.md`, Anchored: moving ends it immediately.
        Only the Anchored reactions go — a restriction placed on you is not
        something your own movement clears."""
        gone = [p for p in self.pending if p.breaks_on_move]
        if gone:
            if log:
                log(f'  {self.name} {reason} — Anchored ends.')
            self.pending = [p for p in self.pending if not p.breaks_on_move]

    # ---- pending effects ------------------------------------------------

    def add_pending(self, p, log=None):
        self.pending.append(p)
        if log and p.text:
            log(f'  {self.name}: {p.text}')

    def restriction(self, kind, **match):
        """The first restriction of this kind in force, or None. `match`
        narrows it — restriction(NO_COLOR, color='RED')."""
        for p in self.pending:
            if p.kind != kind:
                continue
            if all(p.data.get(k) == v for k, v in match.items()):
                return p
        return None

    def spend_restriction(self, p, log=None):
        if p.spend():
            self.pending.remove(p)
        if log and p.text:
            log(f'  {self.name}: {p.text}')

    def fire(self, event, opponent, allies, enemies, rng, log, **data):
        """Run every reaction waiting on `event`."""
        import effects as _fx
        for p in list(self.pending):
            if p.kind is not None or p.event != event or p not in self.pending:
                continue
            if p.data.get('position') and p.data['position'] != self.position:
                continue
            if p.text:
                log(f'  {self.name}: {p.text}')
            ctx = _fx.Context(self, opponent, allies, enemies, None, event,
                              rng=rng, log=log)
            ctx.wheel = data.get('wheel')
            for op in p.ops:
                op.apply(ctx)
            if p.spend() and p in self.pending:
                self.pending.remove(p)

    def expire_pending(self, log=None):
        """Called at the start of this combatant's turn. Anything measured
        against *their* next turn ends here, whoever is holding it — which
        is why this sweeps the whole table rather than just self."""
        for c in _TABLE or [self]:
            gone = [p for p in c.pending
                    if p.expires == 'owner_next_turn' and p.owner is self]
            for p in gone:
                c.pending.remove(p)
                if log and p.text:
                    log(f'  {c.name}: {p.text} — ends.')

    def tick_anchors(self, opponent_default, allies, enemies, rng, log):
        """Start-of-turn triggers. `rules/card-glossary.md`: the benefit
        triggers at the start of each of your turns for as long as you hold
        position — never on the turn it was played."""
        self.fire('turn_start', opponent_default, allies, enemies, rng, log)

    @property
    def max_hp(self):
        """rules/character-creation.md: max HP = (4 x Body) + Mind + Soul.

        Derived on read, never stored. rules/invariants.md, Confirmed:
        caching this and failing to invalidate it on a stat change is the
        named bug, so there is nothing here to invalidate.
        """
        return 4 * self.body + self.mind + self.soul

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
                self.rng.shuffle(self.deck)
                if log:
                    log(f'{self.name} reshuffles their discard into a new deck.')
            self.hand.append(self.deck.pop())
            drawn += 1
        return drawn

    def playable(self, opponent):
        """Cards in hand whose Range is legal for the current positions."""
        banned = {p.data.get('color') for p in self.pending if p.kind == NO_COLOR}
        return [c for c in self.hand
                if c.is_playable()
                and c.color not in banned
                and c.range_ok(self.position, opponent.position)]

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
            target.break_anchors(log=log, reason='Collapsed')
        if target.hp <= target.death_threshold:
            target.dead = True
            if log:
                log(f'{target.name} dies.')

        # WEATHERED, PAIN IS FUEL: "when you are damaged".
        if dealt > 0 and target.alive() and any(
                p.kind is None and p.event == 'damaged' for p in target.pending):
            allies = [c for c in _TABLE if c.team == target.team and c is not target]
            enemies = [c for c in _TABLE if c.team != target.team]
            target.fire('damaged', source, allies, enemies, None, log or (lambda *a: None))
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
    # A Colorless card has no stat to add — it is the flat die and nothing
    # else (`cards/colorless.md`).
    base = attacker.stat(card.stat) if card.stat else 0
    total = base + (d(card.die, rng) if card.die else 0)

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


def resolve_attack(attacker, defender, atk_card, def_card, rng=random,
                   log=print, wheel=None):
    """One exchange, following `rules/combat.md` Attack Resolution.

    `def_card` may be None — the defender cannot or chooses not to defend.
    Returns an Outcome.
    """
    log(f'{attacker.name} attacks {defender.name}.')

    # PARTITION: the target is out of the exchange entirely, either side.
    # The cards were already committed, so they still go to the discard —
    # an exchange that does not happen must not eat them.
    for who, kind in ((attacker, NO_ATTACK), (defender, NO_TARGET)):
        if who.restriction(kind) is not None:
            log(f'  {who.name} is partitioned — the attack does not happen.')
            attacker.discard.append(atk_card)
            if def_card is not None:
                defender.discard.append(def_card)
            return Outcome.MUTUAL_MISS

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
        return _finish(Outcome.DEFENDER, attacker, defender, atk_card, def_card, log, rng, wheel)
    if atk_blind_miss and def_blind_miss:
        log('Both miss — Mutual Miss. No damage, no Effect, no Defense Effect.')
        return _finish(Outcome.MUTUAL_MISS, attacker, defender, atk_card, def_card, log, rng, wheel)
    if atk_blind_miss:
        log(f'{attacker.name} misses (Blind).')
        return _finish(Outcome.DEFENDER, attacker, defender, atk_card, def_card, log, rng, wheel)
    if def_blind_miss:
        log(f'{defender.name} misses their block (Blind).')
        return _finish(Outcome.ATTACKER, attacker, defender, atk_card, def_card, log, rng, wheel)
    if def_card is None:
        log(f'{defender.name} has no legal defense.')
        return _finish(Outcome.ATTACKER, attacker, defender, atk_card, def_card, log, rng, wheel)

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
    return _finish(outcome, attacker, defender, atk_card, def_card, log,
                   rng, wheel)


def _finish(outcome, attacker, defender, atk_card, def_card, log,
            rng=random, wheel=None):
    """Apply the outcome, run whatever of each half is executable, then
    discard both cards."""
    dealt = 0
    returned_atk = returned_def = False
    gone_atk = gone_def = False   # a card exiled out of the exchange itself
    if outcome == Outcome.ATTACKER:
        swap = defender.restriction(WOUND_INSTEAD)
        if swap is not None:
            from cards import status_card
            defender.deck.insert(0, status_card('Wound'))
            defender.spend_restriction(swap, log=log)
            log(f'  The hit lands as a Wound in {defender.name}\'s deck '
                f'instead of damage.')
            dmg = dealt = 0
        else:
            dmg = roll_damage(attacker, atk_card, rng)
            dealt = defender.take(dmg, source=attacker, log=log)
        if dealt and defender.thorns and (atk_card.range or '').strip().lower().startswith('melee'):
            log(f'{defender.name}\'s Thorns bites back.')
            attacker.take(defender.thorns, unpreventable=True, log=log)
        returned_atk, gone_def = _run(atk_card, 'effect', attacker, defender,
                                      outcome, dealt, log, rng, wheel, def_card)
    elif outcome == Outcome.DEFENDER:
        log('  No damage.')
        returned_def, gone_atk = _run(def_card, 'defense_effect', defender,
                                      attacker, outcome, 0, log, rng, wheel,
                                      atk_card)
    elif outcome == Outcome.TIE:
        log('  Tie — no damage.')
        returned_atk, gone_def = _run(atk_card, 'effect', attacker, defender,
                                      outcome, 0, log, rng, wheel, def_card)
        returned_def, gone_atk = _run(def_card, 'defense_effect', defender,
                                      attacker, outcome, 0, log, rng, wheel,
                                      atk_card)

    # FOCUS returns itself to hand instead of discarding. Tracked here, not
    # on the Card: build_deck draws from a shared pool, so one Card object is
    # in several decks at once and must never carry per-fight state.
    if not returned_atk and not gone_atk:
        attacker.discard.append(atk_card)
    if def_card is not None and not returned_def and not gone_def:
        defender.discard.append(def_card)
    return outcome


# Compiled halves, keyed by the text itself — the same wording on two cards
# compiles once, and a card file edited between runs is re-read by cards.py
# and lands here as new text.
_COMPILED = {}


def compiled(card, half):
    text = getattr(card, half, None)
    if not text or text.strip().lower() in ('none.', 'none'):
        return None
    if text not in _COMPILED:
        _COMPILED[text] = fx.compile_half(text)
    return _COMPILED[text]


def _run(card, half, actor, opponent, outcome, dealt, log, rng, wheel,
         opponent_card=None):
    """Run one half. Anything that did not compile is read out instead,
    which is what every card did before effects.py existed.

    Returns True when the card returned itself to hand instead of being
    discarded.
    """
    if card is None:
        return False, False
    text = getattr(card, half, None)
    if not text or text.strip().lower() in ('none.', 'none'):
        return False, False
    label = 'Effect' if half == 'effect' else 'Defense Effect'
    if half == 'defense_effect':
        gagged = actor.restriction(NO_DEFENSE_EFFECT)
        if gagged is not None:
            log(f'  {actor.name} cannot trigger Defense Effects — {label} '
                f'does not fire.')
            return False, False
    ops = compiled(card, half)
    if ops is None:
        log(f'  {label}: {text}')
        return False, False
    log(f'  {label}: {text}')
    ctx = fx.Context(actor, opponent,
                     allies=[c for c in _TABLE if c.team == actor.team and c is not actor],
                     enemies=[c for c in _TABLE if c.team != actor.team],
                     card=card, outcome=outcome, damage_dealt=dealt,
                     rng=rng, log=log)
    ctx.wheel = wheel
    ctx.opponent_card = opponent_card
    ctx.return_card = False
    ctx.exiled_opponent_card = False
    for op in ops:
        op.apply(ctx)
    if ctx.return_card:
        actor.hand.append(card)
    return ctx.return_card, ctx.exiled_opponent_card


# Everyone in the current fight. Set by play.py before the first exchange so
# that "all allies" and "any enemy" have something to resolve against; an
# exchange run outside a fight simply sees the two combatants in it.
_TABLE = []


def set_table(combatants):
    """Called by play.run at the start of every fight. Anything resolving
    "all allies" or "any enemy" reads this, so it must describe the fight in
    progress — see the note there."""
    global _TABLE
    _TABLE = list(combatants)
