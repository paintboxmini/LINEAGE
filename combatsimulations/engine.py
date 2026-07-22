"""
Tales Untold — Combat Engine (PvP duel simulator)

A faithful-as-possible implementation of the Tales Untold combat loop, built to
run large numbers of 1v1 duels and surface rules gaps, balance outliers, and
emergent tactics.

Ground truth: rules/combat.md, rules/core-rules.md, rules/card-glossary.md,
rules/cards.md, and the worked example in rules/combat-example.md. Any place the
engine had to assume a ruling the rules don't state is logged via RULING() and
collected in the run report — that log IS the deliverable, not an afterthought.

Scope: implements exactly the cards in Frost's and Steele's decks
(testcampaigndecks/). Effects that only touch allies are correctly no-ops in a
duel (You Are Not Your Own Ally) — the sim will show them as dead weight.

No external dependencies. Python 3.8+.
"""

import random
from collections import Counter, defaultdict

# --- Deterministic-ruling log -------------------------------------------------
# Every assumption the engine makes beyond the written rules is recorded once,
# with a stable key, so the run report can list exactly what needs a canon call.
_RULINGS = {}


def RULING(key, note):
    if key not in _RULINGS:
        _RULINGS[key] = note


# --- Dice ---------------------------------------------------------------------
def roll(die, rng):
    return rng.randint(1, die)


def _rolled_die(die, rng, me):
    """The base damage die, modified by Deadly/Weak (rules/card-glossary.md):
    each stack adds (Deadly) or subtracts (Weak) a flat d4 from this one
    future damage roll, then consumes one stack. Flat, not proportional to
    the base die, on purpose — the old "roll twice, take higher/lower"
    version scaled with base die size (worth +0.25 on a d2, +1.65 on a
    d10), quietly favoring whichever color rolls the bigger dice regardless
    of who actually holds the stack. Deadly takes priority if both are
    somehow held at once (not a ruled case, just a defensible tie-break).
    Custom `_damage` functions (exploding dice, multi-hit cards) roll their
    own way and are NOT wrapped here — applying this generically to an
    arbitrary custom function risks doubling unrelated side effects, not
    just the die."""
    if me.deadly > 0:
        me.deadly -= 1
        return roll(die, rng) + roll(4, rng)
    if me.weak > 0:
        me.weak -= 1
        return roll(die, rng) - roll(4, rng)
    return roll(die, rng)


COLOR_TO_STAT = {'R': 'body', 'B': 'mind', 'G': 'soul'}


def _effective_color(engine, card):
    """AFTERIMAGE: colorless (card.color is None) until revealed — a color
    this genuinely doesn't have yet, not a placeholder, which is exactly
    why Axiom's ban check (comparing against a real color) can never match
    it at the point that check runs. Everywhere else color actually gets
    read or displayed, this resolves it: whoever acted immediately before
    this turn (engine._prior_turn_hit). Returns None if there's nothing to
    mirror yet (opening hand, or they Waited/Moved instead of attacking) —
    deliberately no Green fallback (Drew's correction: AFTERIMAGE stays
    genuinely colorless the same way FOLLOW-UP does). A None color is a
    real, legal state, not an error — rps() below resolves what a colorless
    reveal does against a real one. Never mutates the card itself — the
    same Card object is shared across every deck that includes it, so this
    is computed fresh at each read instead."""
    if card.special_reveal == 'mirror_color':
        return engine._prior_turn_hit.get('color')
    return card.color


def _color_label(color):
    """Display only — 'colorless' instead of a bare None in combat logs."""
    return color if color is not None else 'colorless'


def _stamp_reveal(engine, who, card):
    """FOLLOW-UP: record that `who` just revealed `card` (attack or defense),
    for the team-wide 'which ally revealed most recently' lookup below.
    Records the RESOLVED card actually shown at the table — if `card` is
    itself a FOLLOW-UP that successfully copied something, this stamps the
    thing it became, never the literal name "FOLLOW-UP" (which is never
    what's visible at reveal; a later FOLLOW-UP chains onto what was really
    shown, not onto an invisible pass-through label). Scoped deliberately to
    reveal events only (attack/defense plays), not every possible discard
    source (Scry-bin, forced hand-size trims, etc.) — those are incidental
    bookkeeping, not something an ally at the table would ever call "what I
    just did," and every one of them would need its own instrumentation
    across two engines and a dozen card effects for a case (a status card
    surfacing here) that can't happen anyway, since status cards are never
    legal attack or defense choices."""
    engine._reveal_seq += 1
    who._last_reveal_seq = engine._reveal_seq
    who._last_reveal_card = card


def _resolve_follow_up(engine, actor):
    """FOLLOW-UP: becomes a full copy of whichever ally (never `actor`
    itself — matches the established allies-only convention, e.g. WARSONG)
    most recently revealed a card this combat. No ally has revealed
    anything yet (true in an opening hand), or somehow the target is a
    status card, and it's the same no-op either way, by Drew's ruling: this
    resolution fails outright — a guaranteed loss of the reveal, not just a
    weak one, distinct from AFTERIMAGE's "default to Green" fallback."""
    candidates = [a for a in engine.allies(actor) if a._last_reveal_seq is not None]
    if not candidates:
        return None
    best = max(candidates, key=lambda a: a._last_reveal_seq)
    target = best._last_reveal_card
    if target.is_status:
        return None
    return target


# Ongoing kinds whose OWN card text says "ends if you die/collapse" (SLIPSTREAM,
# SYNCHRONY) — cleared for real on Collapse, below. Pure-Anchored kinds
# (rooted_oath, ledger) are deliberately left alone: Anchored's own glossary
# rule only ends on moving position, never mentions Collapse, and since a
# Collapsed combatant can't take turns anyway they go dormant on their own —
# explicitly removing them would be inventing a rule these cards never stated.
_ENDS_ON_COLLAPSE = {'synchrony', 'slipstream'}


def _clear_ongoing_on_collapse(target):
    """Found via Drew asking whether Collapse actually ends an Anchored/ongoing
    effect in the sim — it didn't. Nothing ever cleared `ongoing` on collapse,
    which only became a real (not just theoretical) bug once revival from
    Collapse became possible: without this, a revived combatant's old
    "ends if you collapse" effects would silently resume."""
    target.ongoing = [o for o in target.ongoing if o['kind'] not in _ENDS_ON_COLLAPSE]


def _ongoing_support_tick(engine, who):
    """Start-of-turn ticks for green ongoing support (Synchrony, Rooted Oath).
    Shared by both engines; ally-facing so it's a self-only trickle in a duel."""
    spent = []   # SEED: consumed the instant it triggers — unlike every other
                 # 'anchor' kind below, which reapplies every turn for as long
                 # as the position holds, a seed pays out once and is gone.
    for o in who.ongoing:
        if o['kind'] == 'synchrony':
            for a in [who] + engine.allies(who):
                engine.heal(a, 1, source=who)
        elif o['kind'] == 'ledger' and who.position == o.get('anchor', who.position):
            engine.heal(who, 3, source=who)   # THE LEDGER NEVER CLOSES — self-only, Anchored
        elif o['kind'] == 'dig_in' and who.position == o.get('anchor', who.position):
            who.resist += 1
        elif o['kind'] == 'rooted_oath' and who.position == o.get('anchor', who.position):
            a = o.get('target')
            if a is not None and not a.collapsed:
                a.deadly += 1
        elif o['kind'] == 'rooted_oath_def' and who.position == o.get('anchor', who.position):
            a = o.get('target')
            if a is not None and not a.collapsed:
                a.resist += 1
        elif o['kind'] == 'patience_def' and who.position == o.get('anchor', who.position):
            a = o.get('target')
            if a is not None and not a.collapsed:
                engine.heal(a, 3, source=who)
        elif o['kind'] == 'seed_deadly' and who.position == o.get('anchor', who.position):
            who.deadly += 2
            spent.append(o)
        elif o['kind'] == 'seed_resist' and who.position == o.get('anchor', who.position):
            who.resist += 2
            spent.append(o)
        elif o['kind'] == 'anchor_heal2' and who.position == o.get('anchor', who.position):
            engine.heal(who, 2, source=who)   # IRON GRIP / PATIENCE OF STONE
    if spent:
        who.ongoing = [o for o in who.ongoing if not any(o is s for s in spent)]


def _object_tick(engine, who):
    """Mason Glyphs / Objects (cards/mason-glyphs.md): trigger for free, no
    roll, no contest, for whoever occupies the matching position on their
    own turn. Ally-type objects benefit their owner's whole side, the owner
    included — a standing Object has no "self" left to exclude the way a
    per-turn ally buff (WARSONG) does, since it isn't cast by anyone
    anymore once it exists. Hazard-type objects strike the owner's
    enemies. CIPHER's "gain Obscure" is real canon text but genuinely
    unmodeled here, same footing as Reveal Hand — Obscure blocks looking at
    a hand/deck, and this sim's AI already has full internal visibility
    regardless of what any card says, so there's nothing for it to actually
    change."""
    for obj in engine.objects:
        if who.position != obj['position']:
            continue
        owner = obj['owner']
        kind = obj['kind']
        if kind == 'mending' and (who is owner or who in engine.allies(owner)):
            engine.heal(who, 1, source=owner)
        elif kind == 'honing' and (who is owner or who in engine.allies(owner)):
            who.next_attack_bonus += 1
        elif kind == 'barbed' and (who is owner or who in engine.allies(owner)):
            who.thorns += 1
        elif kind == 'withering' and who in engine.enemies(owner):
            who.weak += 1
        elif kind == 'miring' and who in engine.enemies(owner):
            engine.initiative_shift(who, -1)


def _apply_shift(engine, queue, target, amount):
    """Initiative Shift ±X (rules/card-glossary.md). `queue` IS the wheel —
    queue[0] is the marker's own slot (whoever's currently acting), queue[1] is
    next up, and so on: exactly as many slots as combatants (rules/combat.md,
    The Wheel). A positive shift travels toward index 0 (sooner), wrapping
    through the far end if it needs to go past 0; negative travels the other
    way, wrapping through 0 if it needs to go past the far end. Every slot the
    path actually crosses slides back one step along that path — a genuine
    circular rotation of the arc between old and new slot, verified against
    all of `rules/initiative-shift-examples.md`'s worked cases (including one
    whose overshoot was a full step past the minimum needed to reach the
    marker's slot — a plain linear list move only gives the right answer when
    the path doesn't wrap, which is why this walks the path explicitly).

    Boundary: a path that reaches or passes the marker's own slot can't
    literally deposit the target there and have it act "in the past," so the
    guarantee is preserved by a chip instead of by capping the move. Positive:
    the target gets an immediate bonus turn, and whoever held the marker's
    slot before this shift is skipped once — compensation for that bonus
    specifically, not a rule about the marker's slot itself (a negative shift
    reaching the same slot skips only the target, nobody else, since no bonus
    was granted to compensate for). A shift large enough to cross the
    marker's slot more than once in one application has no confirmed ruling
    and isn't modeled beyond a single crossing.

    Reshifting a token that already carries a pending skip or bonus clears it
    first. The one confirmed case of this (`rules/initiative-shift-examples.md`,
    Example 5) came out as an ordinary reposition — no bonus — which the
    general boundary-crossing formula below would NOT reproduce on its own (it
    would predict a bonus there). Rather than derive arithmetic nobody has
    confirmed, that specific case is hard-coded instead: a reshift of an
    already-pending token never re-triggers the boundary/chip logic, full
    stop — it always resolves as an ordinary reposition, whatever the raw
    distance would otherwise suggest. This is asserted as a blanket rule
    covering every variation (positive or negative new shift, prior skip or
    prior bonus), not just Example 5's exact numbers, since only the one case
    is confirmed and there's no basis to special-case the others differently.

    With 3 or fewer combatants on the wheel, X's magnitude is reduced by 1
    (toward zero) before anything else here runs — a shift of ±1 becomes a
    no-op. (Previously gated on exactly 3; Drew's correction — the dampening
    is meant to apply at 3 *or less*, not just exactly 3. This also happens
    to be what would have prevented WARSONG's +2-at-2-seats crash from ever
    reaching the exact-multiple case below in the first place — a +2 dampens
    to +1 here, which isn't a multiple of 2.)"""
    if not queue or target not in queue or amount == 0:
        return
    if len(queue) <= 3:
        amount += -1 if amount > 0 else 1
        if amount == 0:
            return
    if amount > 0:
        target._shifted_positive = True   # RHYTHM BREAK: cleared at the start
                                           # of target's own next turn
    was_pending = target._shift_skip or target in engine.pending_turns
    target._shift_skip = False
    if target in engine.pending_turns:
        engine.pending_turns.remove(target)

    i = queue.index(target)
    total = len(queue)

    if i == 0 or target is getattr(engine, '_resolving', None):
        # the current actor, still mid-turn: already at the earliest possible
        # slot, so any positive shift can only mean "sooner than right now,"
        # which becomes a bonus turn this same lap instead (ruling: a
        # positive self-shift always grants an extra turn, any magnitude).
        # `target is engine._resolving` covers this same fact during a BONUS
        # turn, where the acting character isn't at queue[0] at all (that
        # slot belongs to whoever's next in the untouched normal rotation) —
        # found via a real crash (YOU'RE NEXT chaining bonus turns into
        # itself); same rule, just no longer misdetected by queue position.
        if amount > 0 and not was_pending:
            engine.pending_turns.append(target)
        # negative: staying put (or rotating normally) already can't be
        # "sooner" than right now — no ruling asks for anything more here.
        return

    raw = i - amount
    crossed = (raw <= 0 or raw >= total) and not was_pending
    landing = raw % total
    step = -1 if amount > 0 else 1

    if landing == i:
        # |amount| is an exact multiple of the wheel size (found via a real
        # crash: WARSONG's +2 shift against a 2-seat wheel, once a team
        # battle had thinned to 2 combatants — the general case is any shift
        # that's a multiple of the current seat count, at any wheel size).
        # The target completes one or more full laps and lands back on its
        # own slot — nobody else's relative order actually changes, so there
        # is no path to walk and no one to displace. The marker was still
        # crossed along the way, though, so that consequence still lands on
        # the target itself.
        if crossed:
            if amount > 0:
                engine.pending_turns.append(target)
            else:
                target._shift_skip = True
        return

    path = [i]
    pos = i
    while pos != landing:
        pos = (pos + step) % total
        path.append(pos)
    occupants = [queue[p] for p in path]      # read before any writes below

    for k in range(len(path) - 1):
        queue[path[k]] = occupants[k + 1]
    queue[landing] = target

    if crossed:
        if amount > 0:
            displaced = occupants[path.index(0)]
            displaced._shift_skip = True
            engine.pending_turns.append(target)
        else:
            target._shift_skip = True


def _rotate_current(engine, queue, who):
    """End-of-turn rotation for whoever just acted. If a shift already moved
    them (their own positive self-shift granted a bonus, handled via
    pending_turns and never touching queue position), this is a no-op —
    otherwise: ordinary rotation, off the marker's slot and onto the back."""
    if not queue or queue[0] is not who:
        return
    queue.pop(0)
    queue.append(who)


def _reposition_after(queue, me, target):
    """STARING CONTEST: move `me` to immediately follow `target` in the
    current cycle's order. Deliberately NOT routed through _apply_shift —
    the card's own text never says "Initiative Shift," just "change your
    place... the new order takes effect this cycle." No bonus turn, no
    shift-skip, a plain reorder. Safe to call even when `me` is the
    currently-resolving actor: _rotate_current already no-ops if queue[0]
    isn't who anymore by the time the turn ends, so moving the current
    actor mid-turn here doesn't fight with the normal end-of-turn rotation."""
    if me not in queue or target not in queue or me is target:
        return
    queue.remove(me)
    queue.insert(queue.index(target) + 1, me)


def _rushdown(actor, target):
    """Rushdown (rules/combat.md): move a Backline enemy to the Frontline.
    The actor must already be in the Frontline. A structural gap this whole
    session: fully defined as a table action and referenced by name in
    several bestiary cards, but never implemented anywhere — SEISMIC
    REDIRECT is the first card to actually call this. A no-op if either
    precondition fails (actor not Frontline, or target already Frontline),
    same shape as every other conditional forced-reposition effect in
    content.py — the card's own Effect just does nothing that turn rather
    than being illegal to play."""
    if actor.position == 'frontline' and target.position == 'backline':
        target.position = 'frontline'


def _discard_or_return(who, card):
    """Where a just-revealed physical card lands: discard, unless the card's
    own `returns_to_hand` says otherwise (ROLLOUT)."""
    if card.returns_to_hand:
        who.hand.append(card)
    else:
        who.discard.append(card)


def _leave_wheel(engine, queue, who):
    """A combatant who leaves the fight entirely removes their slot, and the
    wheel closes around it (rules/combat.md, Joining and leaving). Plain list
    removal already performs that close — everything after `who`'s slot
    shifts back by one, same as any other slide. Also clears any pending chip
    or bonus turn `who` was carrying, since a combatant that's gone can't be
    skipped or take a bonus turn later. Safe to call on someone not currently
    in the wheel (a no-op)."""
    if who in queue:
        queue.remove(who)
    who._shift_skip = False
    if who in engine.pending_turns:
        engine.pending_turns.remove(who)


def _join_wheel(queue, new_combatant, after=None):
    """A new combatant's token enters the wheel (rules/combat.md, Joining and
    leaving). A summon enters directly after the token of whoever summoned
    it — pass that combatant as `after`. A GM-introduced combatant enters
    when the fiction calls for it (usually the end of a full lap); the
    caller decides the timing, this just does the insertion — pass
    `after=None` to append at the back, matching "end of a lap." Now wired to
    revival from Collapse (`heal()` below, `after=` the healer) — still not
    wired to any card that summons, but the wheel's slot count is expected to
    stay accurate if one ever does."""
    if after is not None and after in queue:
        queue.insert(queue.index(after) + 1, new_combatant)
    else:
        queue.append(new_combatant)


# --- Card model ---------------------------------------------------------------
class Card:
    """A card is data plus up to three behavior hooks.

    color: 'R' | 'B' | 'G'   (Body / Mind / Soul)
    stat:  'body' | 'mind' | 'soul'
    reach: 'melee' | 'ranged' | 'both'
    base_die: the attack die (2/4/6/8), or None for custom damage.
    """

    def __init__(self, name, color, stat, reach, base_die,
                 damage=None, effect=None, defense=None, special_reveal=None,
                 is_status=False, ignores=frozenset(), returns_to_hand=False):
        self.name = name
        self.color = color
        self.stat = stat
        self.reach = reach
        self.base_die = base_die
        self._damage = damage          # fn(engine, me, foe) -> int  (pre-reduction)
        self._effect = effect          # fn(engine, me, foe)  attacker won OR tie
        self._defense = defense        # fn(engine, me, foe)  defender won OR tie
        self.special_reveal = special_reveal  # e.g. 'paradox'
        self.is_status = is_status     # Injury/Exhaust: cannot be played
        # ROLLOUT: some cards return straight to your own hand instead of
        # the discard pile once played, regardless of outcome — a Card-level
        # property (checked at every discard-append point in attack(), both
        # engines) rather than a name-specific special case, in case a
        # future card wants the same shape.
        self.returns_to_hand = returns_to_hand
        # CERTAIN CONTACT: a defense this specific attack ignores outright —
        # any subset of {'evade', 'blind', 'resist'}. Checked directly at
        # each relevant point (the Blind/Evade checks in attack(), the
        # Resist reduction in deal()) rather than a new keyword, since this
        # isn't a status granted to anyone — it's a property of the attack
        # itself, same footing as its own color/stat/range.
        self.ignores = frozenset(ignores)

    def damage(self, engine, me, foe):
        if self._damage:
            return self._damage(engine, me, foe)
        return me.eff(self.stat) + _rolled_die(self.base_die, engine.rng, me)

    def effect(self, engine, me, foe):
        if self._effect:
            self._effect(engine, me, foe)

    def defense(self, engine, me, foe):
        if self._defense:
            self._defense(engine, me, foe)


# --- Combatant ----------------------------------------------------------------
class Combatant:
    def __init__(self, name, body, mind, soul, decklist, policy, hp=None):
        self.name = name
        self.body, self.mind, self.soul = body, mind, soul
        # Canon HP formula (2*Body + 9) — flattened from 3*Body+6 to decouple HP
        # from Body and cut its damage+HP double-dip. Crossover at Body 3.
        self.hp_per_body = 2
        # Bosses may go bespoke on HP (CLAUDE.md, Stat Blocks) — pass `hp=` to
        # override the formula baseline; the formula is still what death_floor()
        # and Body-adjust deltas key off internally, this only overrides the
        # starting/max number itself.
        self.max_hp = hp if hp is not None else self.hp_per_body * body + 9
        self.hp = self.max_hp
        self.hand_size = max(2, mind)   # hand size = Mind, floored at 2 —
                                        # never below act-plus-one-block
        self.decklist = list(decklist)   # names, for rebuild
        self.policy = policy

        self.deck = []
        self.hand = []
        self.discard = []
        self.exile = []

        self.position = 'frontline'
        self._position_at_last_turn_start = self.position  # ROLLOUT/RHYTHM BREAK
        self._repositioned_since_last_turn = False          # tracking
        self.team = 0                    # 0 or 1; set by the Battle in team play
        # token stacks / flags
        self.resist = 0
        self.evade = 0
        self.deadly = 0
        self.weak = 0
        self.thorns = 0
        self.blind = 0
        self.staggered = False
        self.rooted = False
        self.ward = False
        self.immune = False              # Immunity (card-glossary.md): next attack against
                                          # me fails before any cards are revealed at all
        self.axiom_ban = None            # color forbidden on next reveal
        self.next_attack_bonus = 0
        self.cannot_defend = False       # (unused by these decks, reserved)
        self.ongoing = []               # list of dicts: {'kind':..., ...}
        self._anticipating = False       # ANTICIPATE: draw before defending, until my next turn
        self._no_defensive_bonus = False # UNNAME: defensive bonuses don't trigger, until my next turn
        self._partition_shield = False   # PARTITION: can't be targeted by an attack, until caster's next turn
        self._partition_shield_target = None  # PARTITION (caster side): who I shielded, to clear on my next turn
        self._bonus_action = False       # TRAMPLE: gain another action this turn (not a wheel bonus turn)
        self._weathered = False          # WEATHERED: heal 2 each time attacked, until my next turn

        self.last_color = None           # most recent attack color (public)
        self.attack_history = Counter()  # public tally of revealed attack colors
        self.collapsed = False
        self.is_dead = False             # crossed death_floor while Collapsed — permanent

        # combat-duration stat modifiers (Wither -Body, Erode -Soul)
        self.stat_mod = {'body': 0, 'mind': 0, 'soul': 0}
        self.skip_turns = 0              # lost turns (Interrupt) — these cost a turn
        self._shift_skip = False         # Initiative Shift's skip chip (card-glossary.md)
        self.must_target_frontline = False  # Partition: next turn restriction
        self._damage_floor = None        # orphaned: EQUAL FOOTING's old defense used this, no longer does (see rps()); infrastructure left in place, harmless if unused
        self._rend_guard = False         # Rend def: next hit -> Injury, no damage
        self._last_hit = 0               # damage dealt by my most recent attack
        self._tie = False                # True only while an Effect resolves during
                                          # a tie (engine.py's rps()/tie branch) — real
                                          # pre-existing gap, never initialized before
                                          # now: reading it on a normal win before any
                                          # tie had ever happened would crash
        self._last_reveal_seq = None      # FOLLOW-UP: engine._reveal_seq at my last reveal
        self._last_reveal_card = None     # FOLLOW-UP: the (resolved) card I last revealed
        self._quick = False               # Quick (card-glossary.md): a free reposition,
                                           # on top of the normal action, good for exactly
                                           # one turn — consumed at the start of that turn
                                           # regardless of whether it changes anything
        self._skip_draw_next = False      # EMERGENCY REPAIRS: no draw step, next turn only
        self._shifted_positive = False    # RHYTHM BREAK: received a + Initiative Shift,
                                           # cleared at the start of my own next turn
        self._used_wait = False           # RHYTHM BREAK: used Wait, same self-clearing shape

    def eff(self, stat):
        return max(0, getattr(self, stat) + self.stat_mod[stat])

    def adjust(self, stat, delta):
        """Change a stat for the combat by delta (negative = loss). Each stat
        drives its own derived value in real time:
          Body -> max HP (±3 per point; clamp current HP, Collapse at 0)
          Mind -> hand size (force discard if now over)
          Soul -> initiative (applies to future rolls only)
        Only Body touches HP (Drew ruling)."""
        self.stat_mod[stat] += delta
        if stat == 'body':
            self.max_hp = max(1, self.max_hp + self.hp_per_body * delta)
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            if self.hp <= 0 and not self.collapsed:
                self.collapsed = True
        elif stat == 'mind':
            while len(self.hand) > self.effective_hand_size():
                self.discard.append(self.hand.pop())  # forced discard down to size

    def injuries_visible(self):
        """Injuries a player can actually see and count — hand + discard, NOT deck
        (Drew ruling: nobody should have to track or search hidden Injuries). Press
        the Injury and Taint count these."""
        return sum(1 for c in (self.hand + self.discard)
                   if c.is_status and c.name == 'INJURY')

    # --- deck plumbing ---
    def build(self, cards, rng):
        self.deck = [cards[n] for n in self.decklist]
        rng.shuffle(self.deck)

    def draw_one(self, rng):
        if not self.deck:
            if not self.discard:
                return None
            self.deck = self.discard
            self.discard = []
            rng.shuffle(self.deck)
        return self.deck.pop()

    def draw_to_hand(self, rng):
        while len(self.hand) < self.effective_hand_size():
            c = self.draw_one(rng)
            if c is None:
                break
            self.hand.append(c)

    def effective_hand_size(self):
        bonus = sum(1 for o in self.ongoing if o['kind'] == 'handsize')
        return max(2, self.eff('mind')) + bonus  # hand size = Mind (min 2), live

    def death_floor(self):
        import math
        return -math.ceil(self.max_hp / 2)


# --- The engine ---------------------------------------------------------------
class Duel:
    def __init__(self, a, b, cards, seed=None, max_turns=300, log=None):
        self.rng = random.Random(seed)
        self.cards = cards
        self.combatants = [a, b]
        self.max_turns = max_turns
        self.log = log if log is not None else []
        self.turn_count = 0
        self.injury_card = cards.get('INJURY')
        self.exhaust_card = cards.get('EXHAUST')
        self.pending_turns = []
        self.queue = []
        self._resolving = None   # whoever's turn is currently resolving (see _apply_shift)
        # RETALIATE/WARSONG/REBUTTAL/AFTERIMAGE: "the turn immediately before
        # yours" — frozen snapshot of the last completed turn, promoted from
        # _this_turn_hit at the top of take_turn (before that turn's own
        # actions can overwrite it), so a card's Effect always reads the
        # PRIOR combatant's result, never its own. 'color' is set at every
        # reveal regardless of outcome (win, tie, or loss) — AFTERIMAGE cares
        # what was shown, not who won; 'hit'/'target' stay clean-win-only.
        self._prior_turn_hit = {'actor': None, 'target': None, 'hit': False, 'color': None}
        self._this_turn_hit = {'actor': None, 'target': None, 'hit': False, 'color': None}
        self._reveal_seq = 0   # FOLLOW-UP: monotonic clock, stamped on each real reveal
        self.objects = []   # Mason Glyphs / Objects (cards/mason-glyphs.md): list of
                             # {'kind', 'owner', 'position'} dicts, engine-level, not
                             # tied to any Combatant's own state — they outlast their
                             # creator and exist independently on the battlefield.

    def create_object(self, owner, kind):
        """Mason Glyphs / Objects: a persistent, position-anchored battlefield
        entity, created at the owner's current position. No unique ID needed —
        destruction removes the exact dict by identity."""
        self.objects.append({'kind': kind, 'owner': owner, 'position': owner.position})

    def attack_object(self, attacker, card, obj):
        """Attacking an Object instead of a combatant: never rolls for damage,
        never triggers the attacking card's own Effect — it just destroys the
        Object outright, and the card is discarded as normal. Fortress
        intercepts this exactly like it intercepts real attack damage: if
        anyone on the Object's own side currently holds Fortress, this
        becomes a genuine attack against THEM instead (full RPS/damage/Effect
        resolution — the genuine article, not a stand-in), and the Object
        survives untouched. Not yet reachable by any policy in this sim
        (no AI decision logic exists for "is destroying this worth it") —
        a real, deliberate scope limit, same shape as every other "no policy
        decision infrastructure yet" gap this session. Real players and
        future smarter policies can call this directly."""
        owner = obj['owner']
        guard = next((f for f in [owner] + self.allies(owner) if getattr(f, '_fortress', False)), None)
        if guard is not None:
            guard._fortress = False
            self._say(f"    FORTRESS: {guard.name} takes the hit meant for {obj['kind']}")
            self.attack(attacker, guard, card)
            return
        attacker.hand.remove(card)
        _discard_or_return(attacker, card)
        self.objects.remove(obj)
        self._say(f"{attacker.name} destroys {obj['kind']} at {obj['position']}")

    def insert_injury(self, target):
        if self.injury_card is None:
            return
        target.deck.insert(0, self.injury_card)   # bottom of deck — deck.pop() draws from the end

    def insert_exhaust(self, target, n=1):
        """Exhaust (card-glossary.md): goes directly into the target's HAND, not the
        deck — the difference from an Injury, which has to be drawn before it costs
        anything. Can legitimately push hand size above the normal draw cap for a
        turn or more; nothing truncates it back down on its own (same as Mind-loss
        forcing a discard is the only thing that ever rebalances hand size — see
        Combatant.adjust) — only a full destroy_exhaust action clears it."""
        if self.exhaust_card is None:
            return
        for _ in range(n):
            target.hand.append(self.exhaust_card)

    def initiative_shift(self, target, amount):
        _apply_shift(self, self.queue, target, amount)

    def reposition_after(self, me, target):
        _reposition_after(self.queue, me, target)

    def scry(self, actor, owner, x):
        """Look at the top x of owner's deck; the actor's policy decides which go
        back on top and which to the bottom. Returns the cards seen (some cards,
        e.g. ALIGN, care what they were). to_top[-1] ends up drawn next."""
        seen = [owner.deck.pop() for _ in range(min(x, len(owner.deck)))]
        if not seen:
            return seen
        plan = actor.policy.scry_plan(self, actor, owner, seen)
        top, bottom = plan[0], plan[1]
        binned = plan[2] if len(plan) > 2 else []   # Scry can now bin to discard
        for c in binned:
            owner.discard.append(c)
        for c in bottom:
            owner.deck.insert(0, c)
        for c in top:
            owner.deck.append(c)
        return seen

    def _say(self, msg):
        self.log.append(msg)

    def other(self, who):
        return self.combatants[1] if who is self.combatants[0] else self.combatants[0]

    # Team API shared with the Battle engine, so one set of card effects serves
    # both. In a 1v1 there are no allies (ally effects stay no-ops, exactly as
    # before) and exactly one enemy.
    def allies(self, me):
        return []

    def downed_allies(self, me):
        return []   # no allies in a 1v1 — RENEWAL's revival heal stays a no-op here too

    def enemies(self, me):
        foe = self.other(me)
        return [] if foe.collapsed else [foe]

    # --- setup: opening hands drawn when initiative is rolled ---
    def setup(self):
        for c in self.combatants:
            c.build(self.cards, self.rng)
        inits = []
        for c in self.combatants:
            inits.append((roll(6, self.rng) + c.soul, c.soul, c))
        # highest total first; tie -> higher soul; still tied -> coin
        self.rng.shuffle(self.combatants)  # random baseline before stable sort
        order = sorted(self.combatants,
                       key=lambda c: (next(i[0] for i in inits if i[2] is c),
                                      c.soul, self.rng.random()),
                       reverse=True)
        self.order = order
        for c in self.combatants:
            c.draw_to_hand(self.rng)

    # --- damage application ---
    def deal(self, target, amount, unpreventable=False, source=None, bypass_resist=False):
        if amount <= 0:
            return 0
        if not unpreventable and not bypass_resist and target.resist > 0:
            amount = amount // 2
            target.resist -= 1  # one stack per attack
        if not unpreventable and target._damage_floor is not None:
            # Equal Footing floors ATTACK damage only — unpreventable damage (bleed,
            # thorns, status, HP costs) is not an attack and ignores the floor.
            cap = max(0, target.hp - target._damage_floor)
            amount = min(amount, cap)
            # floor is cleared in attack() after the exchange, so it is removed by
            # the next attack whether or not that attack dealt damage.
        # a single normal attack cannot push below 0 (clamp); extra damage while
        # collapsed can. We treat any single application atomically.
        pre = target.hp
        was_collapsed = target.collapsed
        target.hp -= amount
        if pre > 0 and target.hp < 0 and not was_collapsed:
            RULING("single-hit-floor",
                   "A single attack cannot push a standing combatant below 0 HP "
                   "(clamped to 0 = Collapse). Matches rules/combat.md Collapse.")
            target.hp = 0
        if target.hp <= 0 and not target.collapsed:
            target.collapsed = True
            _clear_ongoing_on_collapse(target)
            _leave_wheel(self, self.queue, target)
        elif was_collapsed and not target.is_dead and target.hp <= target.death_floor():
            # Only reachable already-Collapsed — the single-hit-floor above
            # protects a standing combatant from dying on the hit that drops
            # them (rules/combat.md, Collapse & Death: "a single attack cannot
            # push you below 0"). Death is permanent — no further heal call
            # can undo it (see heal()).
            target.is_dead = True
            RULING("death-floor",
                   "Collapsed and reduced to or below -ceil(max_hp/2): dead "
                   "(rules/combat.md, Collapse & Death). Permanent.")
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

    # --- start-of-turn ongoing ticks (BLOOD TITHE etc.) ---
    def start_of_turn(self, who):
        _ongoing_support_tick(self, who)
        _object_tick(self, who)

    # --- one attack action ---
    def attack(self, attacker, defender, card):
        attacker.hand.remove(card)
        attacker._attacked_this = True             # for PATIENCE
        attacker._last_hit = 0  # reset; set when a hit lands (Rend reads this)

        # Immunity (card-glossary.md, BARRIER/LAST RESORT): the attack fails
        # completely before anything else — no FOLLOW-UP resolution, no color
        # read, no reveal bookkeeping. Stronger than Blind/Evade, both of
        # which still reveal the attacker's card and log it to attack_history
        # even on a miss; Immunity means none of that ever happened at all,
        # so it's checked first, ahead of everything below.
        if defender.immune:
            defender.immune = False
            self._say(f"{defender.name}'s Immunity stops the attack cold")
            _discard_or_return(attacker, card)
            return

        # FOLLOW-UP: fully BECOMES a copy of whichever ally most recently
        # revealed a card (before RPS resolution, per Drew's spec) — a
        # stronger transformation than AFTERIMAGE's color-only mirroring, so
        # `card` itself is swapped to the copied Card object for everything
        # below (color, effect, damage, the Axiom-ban check — deliberately
        # NOT exempt the way AFTERIMAGE is, since this fully becomes the real
        # card, name and all). `physical_card` keeps the true identity for
        # hand/discard bookkeeping: FOLLOW-UP itself is what returns to the
        # copier's own discard, never the copied card's name. No target ->
        # `card` stays FOLLOW-UP itself: genuinely colorless (native color
        # None), same footing as AFTERIMAGE with nothing to mirror — resolved
        # by rps() below, not treated as an automatic whiff (Drew's rule:
        # "colorless cards auto lose to any color... it only loses when it's
        # challenged by a card with an actual color" — a colorless card still
        # wins fully if there's no real defense to challenge it at all).
        physical_card = card
        if card.name == "FOLLOW-UP":
            target = _resolve_follow_up(self, attacker)
            if target is not None:
                card = target
        # AFTERIMAGE: resolved once, used everywhere color is read or shown
        # below EXCEPT the Axiom-ban check further down, which deliberately
        # keeps reading card.color directly — that check has to see the
        # genuine colorless state to be bypassed by it at all. May be None
        # (colorless, nothing to mirror/copy) — rps() handles that case on
        # its own; no early return here.
        atk_color = _effective_color(self, card)

        if defender._weathered:   # WEATHERED: heal 2 each time attacked, whatever the outcome
            self.heal(defender, 2)

        # Blind resolves before Evade (rules/card-glossary.md, Blind) — it's
        # the ATTACKER's own stack, checked on their own attack, before the
        # defender's Evade ever gets a say. Simplification, noted: modeled as
        # a stack consumed on the next attack, same shape as Evade; the "or
        # expires at the end of your next turn even if unused" wall-clock
        # nuance isn't tracked.
        if attacker.blind > 0 and 'blind' not in card.ignores:
            attacker.blind -= 1
            if roll(2, self.rng) == 1:
                self._say(f"{attacker.name} plays {card.name} ({_color_label(atk_color)})")
                self._say(f"  {attacker.name} is BLIND — attack fails entirely")
                _discard_or_return(attacker, physical_card)
                attacker.last_color = atk_color
                attacker.attack_history[atk_color] += 1
                self._this_turn_hit['color'] = atk_color
                _stamp_reveal(self, attacker, card)
                return

        # Evade resolves before the defender selects a card. It only reads
        # `defender.evade` (a token count), never the card's color, so it is
        # unaffected by when the reveal fields below get set.
        if defender.evade > 0 and 'evade' not in card.ignores:
            defender.evade -= 1
            if roll(2, self.rng) == 1:
                RULING("evade-consumes-attack",
                       "A dodged attack still consumes the attacker's played card "
                       "and its Effect does not trigger (rules/combat-example.md).")
                self._say(f"{attacker.name} plays {card.name} ({_color_label(atk_color)})")
                self._say(f"  {defender.name} EVADES — attack misses")
                _discard_or_return(attacker, physical_card)
                attacker.last_color = atk_color
                attacker.attack_history[atk_color] += 1  # revealed = public info
                self._this_turn_hit['color'] = atk_color
                _stamp_reveal(self, attacker, card)
                defender._damage_floor = None  # Equal Footing floor spent by any attack
                return

        # Defender chooses a defense BLIND — reveals are simultaneous, so the
        # policy never sees `card`, nor any trace of it: attacker.discard /
        # last_color / attack_history are NOT mutated until after this call
        # returns. A "blind prediction" policy can therefore only ever read
        # history from the attacker's PRIOR attacks, never the current one.
        was_staggered = defender.staggered
        def_card = None
        physical_def_card = None
        if not defender.collapsed and not defender.staggered and not defender.cannot_defend:
            if defender._anticipating:   # ANTICIPATE: draw before defending, every qualifying attack
                c = defender.draw_one(self.rng)
                if c:
                    defender.hand.append(c)
            chosen = defender.policy.choose_defense(self, defender, attacker)
            if chosen is not None:
                physical_def_card = chosen
                def_card = chosen
                if chosen.name == "FOLLOW-UP":
                    target = _resolve_follow_up(self, defender)
                    if target is not None:
                        def_card = target
                    # else: def_card stays FOLLOW-UP itself, genuinely
                    # colorless (native color None) — a legitimate defense
                    # choice, resolved by rps() below like any other card,
                    # not an automatic "no legal defense."
                if def_card is not None:
                    # enforce Axiom ban on the reveal
                    if defender.axiom_ban and def_card.color == defender.axiom_ban:
                        RULING("axiom-blocks-defense",
                               "AXIOM's named color cannot be revealed to defend either "
                               "— the ban is on the next reveal, attack or block "
                               "(rules/card-glossary.md Axiom + reveal timing).")
                        def_card = None
        if was_staggered:
            defender.staggered = False
            self._say(f"  {defender.name} was Staggered — this attack goes undefended, then it clears")

        # Reveal: both cards flip face-up "simultaneously," in code terms right
        # here, immediately before anything looks at them. The attacker's card
        # lands in discard now (before RPS/outcome application), so effects
        # like FORGET that read `foe.discard` after RPS resolves still see it.
        _discard_or_return(attacker, physical_card)
        attacker.last_color = atk_color
        attacker.attack_history[atk_color] += 1  # revealed = public info
        self._this_turn_hit['color'] = atk_color
        _stamp_reveal(self, attacker, card)
        self._say(f"{attacker.name} plays {card.name} ({_color_label(atk_color)})")

        if def_card is None:
            # no defense -> attacker auto-wins (full win); a colorless
            # attacker still gets the same clean, uncontested win here —
            # "colorless auto loses to any color... it only loses when it's
            # challenged by a card with an actual color" (Drew's rule) — no
            # challenge at all means no loss.
            self._resolve_attacker_win(attacker, defender, card, contested=False)
            defender._damage_floor = None
            return

        def_color = _effective_color(self, def_card)   # resolved AFTER the Axiom check above
        defender.hand.remove(physical_def_card)
        _discard_or_return(defender, physical_def_card)
        defender.last_color = def_color
        _stamp_reveal(self, defender, def_card)
        self._say(f"  {defender.name} defends {def_card.name} ({_color_label(def_color)})")

        # FRAME-TRAP: if the defender was hit by an attack on the turn
        # immediately before this one, this attack auto-wins outright — no
        # RPS at all. The defender's card is already committed and revealed
        # above (matches the card's own text: it isn't a "no legal defense"
        # case, the defender genuinely chose and revealed a real card, it's
        # specifically negated after the fact — no Defensive Bonus, no
        # damage roll for it, nothing). "Took damage" means a landed
        # attack specifically (`_prior_turn_hit['hit']`), never Thorns or
        # any other damage source (Drew's confirmed scope).
        if card.name == 'FRAME-TRAP' and self._prior_turn_hit['hit'] \
                and self._prior_turn_hit['target'] is defender:
            self._say(f"  FRAME-TRAP: {defender.name} was hit last turn — {def_card.name} is negated")
            self._resolve_attacker_win(attacker, defender, card, contested=True)
            defender._damage_floor = None
            return

        outcome = self.rps(card, def_card, attacker, defender)
        if outcome == 'attacker':
            self._resolve_attacker_win(attacker, defender, card, contested=True)
        elif outcome == 'defender':
            self._say(f"  -> {defender.name} wins the reveal")
            # A clean win means no damage was ever computed (the attacker's
            # card never resolves). Some Defensive Bonuses need that number
            # anyway (REFRACT's full-damage redirect) -- roll it here, once,
            # for their benefit only; it never applies to the attacker's own
            # turn (their next_attack_bonus/Deadly/Weak stay untouched --
            # rules/combat.md) and is unset again right after so it can't
            # leak into a later attack that doesn't ask for it.
            attacker._redirect_dmg = card.damage(self, attacker, defender)
            if not defender._no_defensive_bonus:   # UNNAME
                def_card.defense(self, defender, attacker)
            attacker._redirect_dmg = None
        else:  # tie
            self._say("  -> tie")
            # attacker Effect first, then defender Defensive Bonus, unless the
            # Effect cancels it. None of these two decks cancel, but DEAD HEAT-style
            # cancels are honored via a flag if present.
            attacker._tie = True
            card.effect(self, attacker, defender)
            attacker._tie = False
            if not defender._no_defensive_bonus:   # UNNAME
                def_card.defense(self, defender, attacker)
        defender._damage_floor = None  # Equal Footing floor spent by any attack

    def rps(self, atk_card, def_card, attacker, defender):
        base = self._rps_base(_effective_color(self, atk_card), _effective_color(self, def_card))
        # PARADOX reverses the outcome on reveal; a tie is unchanged.
        if atk_card.special_reveal == 'paradox' or def_card.special_reveal == 'paradox':
            if base != 'tie':
                base = 'defender' if base == 'attacker' else 'attacker'
        # "Instead of a tie, you win" — checked by name, not a keyword, since
        # only these cards do it. EQUAL FOOTING works from either side; ADAPT's
        # is Effect-only (Drew: "ADAPT effect: win on ties" — its Defensive
        # Bonus stays Gain Evade), so it only ever counts on the attacker side.
        # If both sides have a live claim, neither wins out — stays a tie, same
        # logic as rules/combat.md's Simultaneous Effects (no clear order).
        if base == 'tie':
            atk_wins_tie = atk_card.name in ('EQUAL FOOTING', 'ADAPT')
            # FRAME-TRAP's tie-win is Defensive-Bonus-only per its own card
            # text (unlike EQUAL FOOTING, which works from either side) —
            # same asymmetric shape as ADAPT's attacker-only claim, just on
            # the other side.
            def_wins_tie = def_card.name in ('EQUAL FOOTING', 'FRAME-TRAP')
            if atk_wins_tie and not def_wins_tie:
                base = 'attacker'
            elif def_wins_tie and not atk_wins_tie:
                base = 'defender'
        return base

    @staticmethod
    def _rps_base(atk, dfn):
        if atk == dfn:
            return 'tie'   # includes colorless vs colorless (None == None)
        # Colorless auto-loses to any real color, whichever side it's on —
        # Drew's rule: "colorless cards auto lose to any color... it only
        # loses when it's challenged by a card with an actual color." A
        # colorless card facing no challenge at all never reaches this
        # function (attack() short-circuits to an uncontested win first).
        if atk is None:
            return 'defender'
        if dfn is None:
            return 'attacker'
        beats = {('B', 'R'), ('R', 'G'), ('G', 'B')}  # attacker color beats defender color
        if (atk, dfn) in beats:
            return 'attacker'
        return 'defender'

    def _resolve_attacker_win(self, attacker, defender, card, contested):
        # Preserve 'color', set earlier in attack() at the reveal point —
        # replacing the whole dict here would silently drop it on every
        # clean win, a real bug caught building AFTERIMAGE.
        self._this_turn_hit = {'actor': attacker, 'target': defender, 'hit': True,
                                'color': self._this_turn_hit.get('color')}
        dmg = card.damage(self, attacker, defender) + attacker.next_attack_bonus
        attacker.next_attack_bonus = 0
        # Rend's defensive guard: the next hit deals no damage and instead
        # shuffles an Injury into the struck combatant.
        if defender._rend_guard:
            defender._rend_guard = False
            self.insert_injury(defender)
            attacker._last_hit = 0
            self._say(f"  -> REND guard: no damage, Injury into {defender.name}")
            card.effect(self, attacker, defender)
            return
        dealt = self.deal(defender, dmg, bypass_resist=('resist' in card.ignores))
        attacker._last_hit = dealt
        self._say(f"  -> {attacker.name} hits for {dealt} "
                  f"({defender.name} {defender.hp}/{defender.max_hp})")
        # Thorns: only on a successful MELEE hit against a thorned defender.
        if defender.thorns > 0 and card.reach in ('melee',):
            self.deal(attacker, defender.thorns, unpreventable=True)
        card.effect(self, attacker, defender)

    def _win_result(self, who, foe):
        if foe.collapsed and not who.collapsed:
            return self._finish(who)
        if who.collapsed and not foe.collapsed:
            return self._finish(foe)
        if who.collapsed and foe.collapsed:
            return self._finish(None)
        return None

    # --- main loop ---
    def run(self):
        self.setup()
        self.queue = list(self.order)   # queue[0] = next to act; rotates each turn
        self.pending_turns = []
        while self.turn_count < self.max_turns:
            if not self.queue:      # defensive: shouldn't happen, win-check fires first
                return self._finish(None)
            who = self.queue[0]
            if not who.collapsed:
                self.take_turn(who, self.other(who))
            r = self._win_result(who, self.other(who))
            if r is not None:
                return r
            # current actor rotates to the back, honoring any shift aimed at it
            _rotate_current(self, self.queue, who)
            self.turn_count += 1
            # bonus turns from a positive shift crossing the marker: right after
            while self.pending_turns and self.turn_count < self.max_turns:
                extra = self.pending_turns.pop(0)
                if not extra.collapsed:
                    self.take_turn(extra, self.other(extra))
                r = self._win_result(extra, self.other(extra))
                if r is not None:
                    return r
                # the bonus recipient still needs to vacate the marker's slot
                # afterward, exactly like an ordinary turn would
                if extra in self.queue:
                    self.queue.remove(extra)
                    self.queue.append(extra)
                self.turn_count += 1
        RULING("stalemate-cap",
               "Duels exceeding max_turns are scored as draws (engine safeguard, "
               "not a game rule).")
        return self._finish(None)

    def take_turn(self, who, foe):
        self._resolving = who   # see _apply_shift — covers bonus turns, not just queue[0]
        self._prior_turn_hit = self._this_turn_hit   # freeze last turn's result before this turn can overwrite it
        self._this_turn_hit = {'actor': who, 'target': None, 'hit': False, 'color': None}
        # ROLLOUT/RHYTHM BREAK: did my position change at any point since my
        # own last turn began (my own Move, forced repositioning by anyone,
        # Quick, Rushdown as a victim — anything)? Computed once, right here,
        # before this turn's own actions can touch position — stays readable
        # (by myself or anyone else) until my next turn recomputes it.
        who._repositioned_since_last_turn = (who.position != who._position_at_last_turn_start)
        who._position_at_last_turn_start = who.position
        who.cannot_defend = False
        who._anticipating = False        # ANTICIPATE, UNNAME, WEATHERED: self-clearing, "until my next turn"
        who._no_defensive_bonus = False
        who._weathered = False
        who._shifted_positive = False    # RHYTHM BREAK: same self-clearing shape
        who._used_wait = False
        shielded = who._partition_shield_target   # PARTITION: caster clears the shield they granted
        if shielded is not None:
            shielded._partition_shield = False
            who._partition_shield_target = None
        who._attacked_last = getattr(who, '_attacked_this', False)  # PATIENCE
        who._attacked_this = False
        if who._shift_skip or who.skip_turns > 0:
            who._shift_skip = False
            if who.skip_turns > 0:
                who.skip_turns -= 1
            self._say(f"{who.name} loses their turn")
            return
        self.start_of_turn(who)
        if who.collapsed:
            return
        if who._quick:
            # Quick (card-glossary.md): a free repositioning action on top of
            # the normal action, good for exactly this one turn — either a
            # normal Move or Rushdown (Drew's correction: Rushdown isn't a
            # granted keyword, it's one of the normal movement options, same
            # as Move Position itself). "You may" in the glossary text is a
            # real table choice; the bots here have no position-optimizing
            # logic to make that choice with, so a simple, deterministic
            # default stands in rather than adding a new decision axis to
            # every policy for one small utility grant — flagged, not
            # silently assumed: Rushdown if already Frontline with a
            # Backline enemy to drag in (the more aggressive option),
            # otherwise a plain self-flip. Applies even on a Staggered turn
            # below: Quick only ever promises the reposition, never the
            # attack that Staggered skips.
            who._quick = False
            if who.position == 'frontline' and foe.position == 'backline':
                _rushdown(who, foe)
                self._say(f"{who.name} uses Rushdown for free (Quick), dragging {foe.name} to Frontline")
            else:
                who.position = 'backline' if who.position == 'frontline' else 'frontline'
                self._say(f"{who.name} repositions for free (Quick)")
        if who._skip_draw_next:
            who._skip_draw_next = False
            self._say(f"{who.name} skips their draw step (Emergency Repairs)")
        else:
            who.draw_to_hand(self.rng)
        if who.staggered:
            who.staggered = False
            self._say(f"{who.name} is Staggered — this turn's attack is skipped")
            who.must_target_frontline = False
            return
        extra_actions = 0
        while True:
            action = who.policy.choose_action(self, who, foe)
            if action is None:
                # Wait (rules/combat.md): forgo the action to reposition -X for a
                # combo cadence. Choosing X is a tactical, table-only call; these
                # brains never plan one, so a forced pass is just a lost turn
                # (X=0). Tactical Wait is intentionally unmodeled.
                who._used_wait = True   # RHYTHM BREAK
                self._say(f"{who.name} waits")
            else:
                kind = action[0]
                if kind == 'attack':
                    self.attack(who, foe, action[1])
                elif kind == 'attack_object':
                    self.attack_object(who, action[1], action[2])
                elif kind == 'move':
                    who.position = 'backline' if who.position == 'frontline' else 'frontline'
                    self._say(f"{who.name} moves to {who.position}")
                elif kind == 'destroy_exhaust':
                    removed = sum(1 for c in who.hand if c.is_status and c.name == 'EXHAUST')
                    who.hand = [c for c in who.hand if not (c.is_status and c.name == 'EXHAUST')]
                    self._say(f"{who.name} destroys all Exhaust cards ({removed}) (action)")
                elif kind == 'destroy_injury':
                    for i, c in enumerate(who.hand):
                        if c.is_status and c.name == 'INJURY':
                            who.hand.pop(i)
                            self._say(f"{who.name} destroys an Injury (action)")
                            break
            # TRAMPLE: an extra action within THIS turn, not a wheel bonus turn —
            # capped so a bug can't hang the sim, though nothing should ever
            # realistically chain that far.
            if not who._bonus_action or who.collapsed or extra_actions >= 5:
                break
            who._bonus_action = False
            extra_actions += 1
            self._say(f"{who.name} gained another action (TRAMPLE)")
        # Injuries no longer leave on their own — they sit until an action or rest
        # clears them. Only per-turn restrictions reset here.
        who.must_target_frontline = False

    def _finish(self, winner):
        self.result = winner.name if winner else 'TIE'
        return self.result


# --- range legality -----------------------------------------------------------
def can_attack(attacker, defender, card):
    if card.reach == 'both':
        return True
    both_front = attacker.position == 'frontline' and defender.position == 'frontline'
    if card.reach == 'melee':
        return both_front
    if card.reach == 'ranged':
        return not both_front
    return False
