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
    each stack applies to one future damage roll — roll twice, take the
    higher (Deadly) or lower (Weak) result, then consume one stack. Deadly
    takes priority if both are somehow held at once (not a ruled case,
    just a defensible tie-break). Custom `_damage` functions (exploding
    dice, multi-hit cards) roll their own way and are NOT wrapped here —
    applying "roll twice" generically to an arbitrary custom function risks
    doubling unrelated side effects, not just the die."""
    if me.deadly > 0:
        me.deadly -= 1
        return max(roll(die, rng), roll(die, rng))
    if me.weak > 0:
        me.weak -= 1
        return min(roll(die, rng), roll(die, rng))
    return roll(die, rng)


def _ongoing_support_tick(engine, who):
    """Start-of-turn ticks for green ongoing support (Synchrony, Rooted Oath).
    Shared by both engines; ally-facing so it's a self-only trickle in a duel."""
    for o in who.ongoing:
        if o['kind'] == 'synchrony':
            for a in [who] + engine.allies(who):
                engine.heal(a, 1, source=who)
        elif o['kind'] == 'rooted_oath' and who.position == o.get('anchor', who.position):
            allies = engine.allies(who)
            if allies:                     # ally-only: no self-fallback (green revert)
                max(allies, key=lambda a: max(a.eff('body'), a.eff('mind'), a.eff('soul'))
                    ).next_attack_bonus += 2


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

    With exactly 3 combatants on the wheel, X's magnitude is reduced by 1
    (toward zero) before anything else here runs — a shift of ±1 becomes a
    no-op."""
    if not queue or target not in queue or amount == 0:
        return
    if len(queue) == 3:
        amount += -1 if amount > 0 else 1
        if amount == 0:
            return
    was_pending = target._shift_skip or target in engine.pending_turns
    target._shift_skip = False
    if target in engine.pending_turns:
        engine.pending_turns.remove(target)

    i = queue.index(target)
    total = len(queue)

    if i == 0:
        # the current actor, still mid-turn: already at the earliest possible
        # slot, so any positive shift can only mean "sooner than right now,"
        # which becomes a bonus turn this same lap instead (ruling: a
        # positive self-shift always grants an extra turn, any magnitude).
        if amount > 0 and not was_pending:
            engine.pending_turns.append(target)
        # negative: staying put (or rotating normally) already can't be
        # "sooner" than right now — no ruling asks for anything more here.
        return

    raw = i - amount
    crossed = (raw <= 0 or raw >= total) and not was_pending
    landing = raw % total
    step = -1 if amount > 0 else 1

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
                 is_status=False):
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
    def __init__(self, name, body, mind, soul, decklist, policy):
        self.name = name
        self.body, self.mind, self.soul = body, mind, soul
        # Canon HP formula (2*Body + 9) — flattened from 3*Body+6 to decouple HP
        # from Body and cut its damage+HP double-dip. Crossover at Body 3.
        self.hp_per_body = 2
        self.max_hp = self.hp_per_body * body + 9
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
        self.team = 0                    # 0 or 1; set by the Battle in team play
        # token stacks / flags
        self.resist = 0
        self.evade = 0
        self.deadly = 0
        self.weak = 0
        self.thorns = 0
        self.staggered = False
        self.rooted = False
        self.ward = False
        self.axiom_ban = None            # color forbidden on next reveal
        self.next_attack_bonus = 0
        self.cannot_defend = False       # (unused by these decks, reserved)
        self.ongoing = []               # list of dicts: {'kind':..., ...}

        self.last_color = None           # most recent attack color (public)
        self.attack_history = Counter()  # public tally of revealed attack colors
        self.collapsed = False

        # combat-duration stat modifiers (Wither -Body, Erode -Soul)
        self.stat_mod = {'body': 0, 'mind': 0, 'soul': 0}
        self.skip_turns = 0              # lost turns (Interrupt) — these cost a turn
        self._shift_skip = False         # Initiative Shift's skip chip (card-glossary.md)
        self.must_target_frontline = False  # Partition: next turn restriction
        self._damage_floor = None        # Equal Footing def: next-attack HP floor
        self._rend_guard = False         # Rend def: next hit -> Injury, no damage
        self._last_hit = 0               # damage dealt by my most recent attack

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
        self.pending_turns = []
        self.queue = []

    def insert_injury(self, target):
        if self.injury_card is None:
            return
        target.deck.insert(0, self.injury_card)   # bottom of deck — deck.pop() draws from the end

    def initiative_shift(self, target, amount):
        _apply_shift(self, self.queue, target, amount)

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
    def deal(self, target, amount, unpreventable=False, source=None):
        if amount <= 0:
            return 0
        if not unpreventable and target.resist > 0:
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
        target.hp -= amount
        if pre > 0 and target.hp < 0 and not target.collapsed:
            RULING("single-hit-floor",
                   "A single attack cannot push a standing combatant below 0 HP "
                   "(clamped to 0 = Collapse). Matches rules/combat.md Collapse.")
            target.hp = 0
        if target.hp <= 0 and not target.collapsed:
            target.collapsed = True
            _leave_wheel(self, self.queue, target)
        return amount

    def heal(self, target, amount, source=None):
        # Collapse can be healed out of (rules/combat.md, Collapse & Death:
        # "You may be healed back into combat") — only revive on a healed total
        # that actually clears 0; anything less just softens the Collapse state.
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

    # --- one attack action ---
    def attack(self, attacker, defender, card):
        attacker.hand.remove(card)
        attacker._attacked_this = True             # for PATIENCE
        attacker._last_hit = 0  # reset; set when a hit lands (Rend reads this)

        # Evade resolves before the defender selects a card. It only reads
        # `defender.evade` (a token count), never the card's color, so it is
        # unaffected by when the reveal fields below get set.
        if defender.evade > 0:
            defender.evade -= 1
            if roll(2, self.rng) == 1:
                RULING("evade-consumes-attack",
                       "A dodged attack still consumes the attacker's played card "
                       "and its Effect does not trigger (rules/combat-example.md).")
                self._say(f"{attacker.name} plays {card.name} ({card.color})")
                self._say(f"  {defender.name} EVADES — attack misses")
                attacker.discard.append(card)
                attacker.last_color = card.color
                attacker.attack_history[card.color] += 1  # revealed = public info
                defender._damage_floor = None  # Equal Footing floor spent by any attack
                return

        # Defender chooses a defense BLIND — reveals are simultaneous, so the
        # policy never sees `card`, nor any trace of it: attacker.discard /
        # last_color / attack_history are NOT mutated until after this call
        # returns. A "blind prediction" policy can therefore only ever read
        # history from the attacker's PRIOR attacks, never the current one.
        was_staggered = defender.staggered
        def_card = None
        if not defender.collapsed and not defender.staggered and not defender.cannot_defend:
            def_card = defender.policy.choose_defense(self, defender, attacker)
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
        attacker.discard.append(card)
        attacker.last_color = card.color
        attacker.attack_history[card.color] += 1  # revealed = public info
        self._say(f"{attacker.name} plays {card.name} ({card.color})")

        if def_card is None:
            # no defense -> attacker auto-wins (full win)
            self._resolve_attacker_win(attacker, defender, card, contested=False)
            defender._damage_floor = None
            return

        defender.hand.remove(def_card)
        defender.discard.append(def_card)
        defender.last_color = def_card.color
        self._say(f"  {defender.name} defends {def_card.name} ({def_card.color})")

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
            def_card.defense(self, defender, attacker)
        defender._damage_floor = None  # Equal Footing floor spent by any attack

    def rps(self, atk_card, def_card, attacker, defender):
        base = self._rps_base(atk_card.color, def_card.color)
        # PARADOX reverses the outcome on reveal; a tie is unchanged.
        if atk_card.special_reveal == 'paradox' or def_card.special_reveal == 'paradox':
            if base != 'tie':
                base = 'defender' if base == 'attacker' else 'attacker'
        return base

    @staticmethod
    def _rps_base(atk, dfn):
        if atk == dfn:
            return 'tie'
        beats = {('B', 'R'), ('R', 'G'), ('G', 'B')}  # attacker color beats defender color
        if (atk, dfn) in beats:
            return 'attacker'
        return 'defender'

    def _resolve_attacker_win(self, attacker, defender, card, contested):
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
        dealt = self.deal(defender, dmg)
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
        who.cannot_defend = False
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
        who.draw_to_hand(self.rng)
        if who.staggered:
            who.staggered = False
            self._say(f"{who.name} is Staggered — this turn's attack is skipped")
            who.must_target_frontline = False
            return
        action = who.policy.choose_action(self, who, foe)
        if action is None:
            # Wait (rules/combat.md): forgo the action to reposition -X for a combo
            # cadence. Choosing X is a tactical, table-only call; these brains never
            # plan one, so a forced pass is just a lost turn (X=0). Tactical Wait is
            # intentionally unmodeled.
            self._say(f"{who.name} waits")
        else:
            kind = action[0]
            if kind == 'attack':
                self.attack(who, foe, action[1])
            elif kind == 'move':
                who.position = 'backline' if who.position == 'frontline' else 'frontline'
                self._say(f"{who.name} moves to {who.position}")
            elif kind == 'destroy_injury':
                for i, c in enumerate(who.hand):
                    if c.is_status and c.name == 'INJURY':
                        who.hand.pop(i)
                        self._say(f"{who.name} destroys an Injury (action)")
                        break
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
