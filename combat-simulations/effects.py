"""Executing card Effects.

`cards.py` reads the structured half of a card — name, colour, stat, die,
range. This module reads the other half: the Effect and Defense Effect
prose, and turns the part of it that is regular into operations the engine
can actually run.

**The markdown stays the source of truth.** Nothing here asks a card file to
change shape, and no card carries a machine-readable annotation. The prose
is written for a person; this is a reader for it.

**A half either compiles completely or not at all.** Partial execution is
worse than none — an effect that grants the buff and silently drops the
"and draw 1" is a wrong fight reported as a right one. When any clause in a
half fails to parse, the whole half falls back to being printed for whoever
is playing, which is exactly what the engine did for every card before this
module existed. `python3 effects.py` reports how much of the pool compiles.

What is deliberately not attempted: anything needing a rules judgement a
person makes at the table (BECOMING permanently rewriting a deck, FOLLOW-UP
copying another card, PRESS THE WOUND counting status cards). Those narrate,
and they should.
"""

import re

# ---- statuses ----------------------------------------------------------

# Keyword -> Combatant attribute. Protect is handled separately: it needs a
# nominated ally, so it is not a simple counter.
STATUS_ATTR = {
    'deadly': 'deadly', 'weak': 'weak', 'evade': 'evade', 'resist': 'resist',
    'vulnerable': 'vulnerable', 'thorns': 'thorns', 'armour': 'armour',
    'armor': 'armour', 'ward': 'ward', 'quick': 'quick', 'blind': 'blind',
    'rooted': 'rooted', 'staggered': 'staggered', 'immunity': 'immunity',
}

# `rules/card-glossary.md`: the six things Ward prevents.
DEBUFFS = {'weak', 'blind', 'vulnerable', 'staggered', 'rooted'}

# `rules/card-glossary.md`: what "Positive Status Effects" names.
POSITIVE = ('evade', 'resist', 'deadly', 'protect', 'anchored', 'quick', 'immunity')

STATUS_WORDS = sorted(set(list(STATUS_ATTR) + ['protect']), key=len, reverse=True)
STATUS_RE = '|'.join(STATUS_WORDS)


# ---- targets -----------------------------------------------------------

SELF, OPPONENT, ALLY, ALL_ALLIES, ALL_ENEMIES, PARTY, ANY = (
    'self', 'opponent', 'ally', 'all_allies', 'all_enemies', 'party', 'any')

# A clause with no subject of its own inherits the last one named in the
# same half. "Target ally heals 4 and draws 1" draws for the ally, not for
# the caster; "Scry 2, then draw 1" is both the caster, because the caster
# was the subject already. Resolved at compile time, never at play time.
INHERIT = 'inherit'


class Context:
    """Everything an Op needs to resolve, for one triggering half.

    `actor` is whoever's card is resolving; `opponent` is the other side of
    the exchange. Both halves therefore use the same two names — "Defender
    gains Weak" on an attack and "Attacker gains Weak" on a defence are the
    same op with the same target.
    """

    def __init__(self, actor, opponent, allies, enemies, card, outcome,
                 damage_dealt=0, rng=None, log=print, agent=None):
        self.actor = actor
        self.opponent = opponent
        self.allies = [a for a in allies if a.alive()]
        self.enemies = [e for e in enemies if e.alive()]
        self.card = card
        self.outcome = outcome
        self.damage_dealt = damage_dealt
        self.rng = rng
        self.log = log
        self.agent = agent or getattr(actor, '_agent', None)

    def resolve(self, spec, prompt='Target'):
        """A target spec to a list of combatants."""
        if spec == SELF:
            return [self.actor]
        if spec == OPPONENT:
            return [self.opponent] if self.opponent is not None else []
        if spec == ALL_ALLIES:
            return list(self.allies)
        if spec == PARTY:
            return [self.actor] + list(self.allies)
        if spec == ALL_ENEMIES:
            return list(self.enemies)
        if spec == ALLY:
            pool = self.allies or [self.actor]
            return [self._ask(pool, prompt)]
        if spec == ANY:
            pool = [self.actor] + self.allies + self.enemies
            return [self._ask(pool, prompt)]
        return []

    def _ask(self, pool, prompt):
        if len(pool) == 1 or self.agent is None:
            return pool[0]
        return self.agent.choose_target(self.actor, pool, prompt)


# ---- ops ---------------------------------------------------------------

class Op:
    def apply(self, ctx):
        raise NotImplementedError

    def __repr__(self):
        return f'{type(self).__name__}({self.__dict__})'


def grant(who, status, n=1, log=None, source=None):
    """Apply a status, honouring Ward.

    `rules/card-glossary.md`, Ward: prevents the next Debuff applied to you,
    automatically, and expires on use. Checked here so every path that
    grants a Debuff pays it — a card, a Special Rule, or the engine.
    """
    status = status.lower()
    if status in DEBUFFS and who.ward > 0:
        who.ward -= 1
        if log:
            log(f'  {who.name} Wards off {status.title()}.')
        return False
    attr = STATUS_ATTR[status]
    setattr(who, attr, getattr(who, attr) + n)
    if log:
        amount = f' {n}' if n > 1 else ''
        log(f'  {who.name} gains {status.title()}{amount}.')
    return True


class Grant(Op):
    def __init__(self, target, status, n=1):
        self.target, self.status, self.n = target, status, n

    def apply(self, ctx):
        for who in ctx.resolve(self.target, f'Give {self.status.title()} to'):
            if self.status == 'protect':
                _grant_protect(who, ctx)
            else:
                grant(who, self.status, self.n, log=ctx.log)


def _grant_protect(who, ctx):
    """`rules/card-glossary.md`: the next time an ally would take attack
    damage, you take it instead. The holder nominates which ally."""
    mates = [c for c in ([ctx.actor] + ctx.allies + ctx.enemies)
             if c.team == who.team and c is not who and c.alive()]
    if not mates:
        ctx.log(f'  {who.name} has no ally to Protect.')
        return
    ward = mates[0] if len(mates) == 1 or ctx.agent is None else \
        ctx.agent.choose_target(who, mates, 'Protect which ally')
    who.protect_for = ward
    ward._protected_by = who
    ctx.log(f'  {who.name} will take the next hit for {ward.name} (Protect).')


class Strip(Op):
    """Remove Positive Status Effects. `all` strips every one; otherwise the
    holder picks a single kind to take or remove."""

    def __init__(self, target, mode='all', steal=False):
        self.target, self.mode, self.steal = target, mode, steal

    def apply(self, ctx):
        for who in ctx.resolve(self.target, 'Strip buffs from'):
            held = [s for s in POSITIVE
                    if s in STATUS_ATTR and getattr(who, STATUS_ATTR[s], 0) > 0]
            if who.protect_for is not None:
                held.append('protect')
            if not held:
                ctx.log(f'  {who.name} has no Positive Status Effects.')
                continue
            picks = held if self.mode == 'all' else [
                held[0] if ctx.agent is None else
                ctx.agent.choose_option(ctx.actor, held, 'Take which')]
            for s in picks:
                if s == 'protect':
                    if who.protect_for is not None:
                        who.protect_for._protected_by = None
                        who.protect_for = None
                else:
                    setattr(who, STATUS_ATTR[s], getattr(who, STATUS_ATTR[s]) - 1)
                verb = 'takes' if self.steal else 'strips'
                ctx.log(f'  {ctx.actor.name} {verb} {s.title()} from {who.name}.')
                if self.steal:
                    grant(ctx.actor, s, log=ctx.log) if s != 'protect' \
                        else _grant_protect(ctx.actor, ctx)


class Damage(Op):
    def __init__(self, target, amount, unpreventable=False):
        self.target, self.amount, self.unpreventable = target, amount, unpreventable

    def apply(self, ctx):
        for who in ctx.resolve(self.target, 'Damage'):
            who.take(self.amount, unpreventable=self.unpreventable,
                     source=ctx.actor, log=ctx.log)


class Heal(Op):
    def __init__(self, target, amount):
        self.target, self.amount = target, amount

    def apply(self, ctx):
        for who in ctx.resolve(self.target, 'Heal'):
            who.heal(self.amount, log=ctx.log)
            ctx.log(f'  {who.name} heals {self.amount} '
                    f'({who.hp}/{who.max_hp} HP).')


class PayHP(Op):
    """An HP cost. `rules/card-glossary.md`, Unpreventable: HP costs land in
    full and cannot be reduced or reassigned."""

    def __init__(self, amount):
        self.amount = amount

    def apply(self, ctx):
        ctx.actor.take(self.amount, unpreventable=True, log=ctx.log)


class Lifesteal(Op):
    """Heal for half the damage this attack actually dealt to HP, rounded
    down — after every reduction, since that is what landed.

    SKEWER and CONSUME both write "heal yourself for the full damage dealt",
    which contradicts the glossary. `rules/card-glossary.md` opens by saying
    card text that contradicts it is an error, so the half is what runs here.
    Flagged rather than silently reconciled: if full is the intent, the
    glossary is what should move.
    """

    def apply(self, ctx):
        if ctx.damage_dealt > 0:
            healed = ctx.damage_dealt // 2
            ctx.actor.heal(healed, log=ctx.log)
            ctx.log(f'  {ctx.actor.name} Lifesteals {healed}.')


class Draw(Op):
    def __init__(self, target, n):
        self.target, self.n = target, n

    def apply(self, ctx):
        for who in ctx.resolve(self.target, 'Draw'):
            got = 0
            for _ in range(self.n):
                if not who.deck:
                    if not who.discard:
                        break
                    who.deck, who.discard = who.discard, []
                    (ctx.rng or __import__('random')).shuffle(who.deck)
                who.hand.append(who.deck.pop())
                got += 1
            if got:
                ctx.log(f'  {who.name} draws {got}.')


class Discard(Op):
    def __init__(self, target, n, at_random=False):
        self.target, self.n, self.at_random = target, n, at_random

    def apply(self, ctx):
        rng = ctx.rng or __import__('random')
        for who in ctx.resolve(self.target, 'Discard'):
            for _ in range(min(self.n, len(who.hand))):
                card = rng.choice(who.hand) if self.at_random else who.hand[-1]
                who.hand.remove(card)
                who.discard.append(card)
            ctx.log(f'  {who.name} discards {min(self.n, len(who.hand) + self.n)}.')


class Exile(Op):
    """`rules/card-glossary.md`: removed from play for the rest of combat,
    not to the discard, and it comes back to the discard when combat ends."""

    def __init__(self, target, n, zone='hand'):
        self.target, self.n, self.zone = target, n, zone

    def apply(self, ctx):
        for who in ctx.resolve(self.target, 'Exile from'):
            pile = who.hand if self.zone == 'hand' else who.discard
            for _ in range(min(self.n, len(pile))):
                who.exiled.append(pile.pop())
            ctx.log(f'  {who.name} exiles {min(self.n, len(pile) + self.n)} '
                    f'from their {self.zone}.')


class Scry(Op):
    """Look at the top X of a deck and place each on top, on the bottom, or
    in the discard. The engine's stand-in for the judgement: keep what the
    holder can use now, bottom the rest."""

    def __init__(self, target, n):
        self.target, self.n = target, n

    def apply(self, ctx):
        for who in ctx.resolve(self.target, 'Scry'):
            look = [who.deck.pop() for _ in range(min(self.n, len(who.deck)))]
            if not look:
                continue
            if ctx.agent is not None and hasattr(ctx.agent, 'scry'):
                keep, bottom = ctx.agent.scry(who, look, ctx.opponent)
            else:
                keep, bottom = look, []
            for c in reversed(bottom):
                who.deck.insert(0, c)
            for c in keep:
                who.deck.append(c)
            ctx.log(f'  {who.name} Scrys {len(look)}'
                    + (f', bottoming {len(bottom)}.' if bottom else '.'))


class Move(Op):
    """Change position. Rooted and Anchored are handled by the position
    setter in engine.py, so forced and chosen movement pay the same price."""

    def __init__(self, target, to=None, optional=False):
        self.target, self.to, self.optional = target, to, optional

    def apply(self, ctx):
        from engine import FRONT, BACK
        for who in ctx.resolve(self.target, 'Move'):
            dest = self.to
            if dest is None:
                if self.optional and ctx.agent is not None:
                    if not ctx.agent.choose_yes_no(
                            ctx.actor, f'Move {who.name} to the other position'):
                        continue
                dest = BACK if who.position == FRONT else FRONT
            if who.position == dest:
                continue
            who.set_position(dest, log=ctx.log)


class Shift(Op):
    """Initiative Shift X. The wheel lives on the context when the caller
    supplies one; without it the shift is reported and not applied."""

    def __init__(self, target, amount):
        self.target, self.amount = target, amount

    def apply(self, ctx):
        wheel = getattr(ctx, 'wheel', None)
        for who in ctx.resolve(self.target, 'Initiative Shift'):
            if wheel is None:
                ctx.log(f'  Initiative Shift {self.amount:+} on {who.name} '
                        f'(no wheel in this context).')
                continue
            wheel.shift(who, self.amount)
            ctx.log(f'  {who.name} takes Initiative Shift {self.amount:+}.')


class StatLoss(Op):
    """`rules/card-glossary.md`, Stat Change — for the rest of the combat."""

    def __init__(self, target, stat, n=1):
        self.target, self.stat, self.n = target, stat, n

    def apply(self, ctx):
        for who in ctx.resolve(self.target, f'Drain {self.stat.title()}'):
            if who.ward > 0:
                who.ward -= 1
                ctx.log(f'  {who.name} Wards off the stat loss.')
                continue
            before = who.max_hp
            setattr(who, self.stat, max(0, getattr(who, self.stat) - self.n))
            who.hp = min(who.hp, who.max_hp)
            ctx.log(f'  {who.name} loses {self.n} {self.stat.title()} '
                    f'(Max HP {before} -> {who.max_hp}).')


class CounterAttack(Op):
    """"Deal this card's Attack damage back to the attacker, works with
    effects like deadly." """

    def apply(self, ctx):
        if ctx.opponent is None or ctx.card is None:
            return
        from engine import roll_damage
        dmg = roll_damage(ctx.actor, ctx.card, ctx.rng or __import__('random'))
        ctx.log(f'  {ctx.actor.name} Counter Attacks.')
        ctx.opponent.take(dmg, source=ctx.actor, log=ctx.log)


class Anchored(Op):
    """`rules/card-glossary.md`: the benefit triggers at the start of each of
    your turns for as long as you hold position. It does not pay on the turn
    it is played — the first trigger is your next turn — and it ends the
    moment you move, voluntarily or not, or Collapse.
    """

    def __init__(self, ops, text):
        self.ops, self.text = ops, text

    def apply(self, ctx):
        ctx.actor.anchored.append((self.ops, self.text, ctx.opponent))
        ctx.log(f'  {ctx.actor.name} is Anchored: {self.text}')


class Gated(Op):
    """A clause that only fires when a condition holds."""

    def __init__(self, test, ops, label):
        self.test, self.ops, self.label = test, ops, label

    def apply(self, ctx):
        if self.test(ctx):
            for op in self.ops:
                op.apply(ctx)
        else:
            ctx.log(f'  ({self.label} — no effect.)')


class Narrate(Op):
    """The fallback, and the behaviour every card had before this module:
    print the text and let the table apply it."""

    def __init__(self, text):
        self.text = text

    def apply(self, ctx):
        ctx.log(f'  {self.text}')


class AddStatusCard(Op):
    """`rules/card-glossary.md`, Status Cards. A Wound or an Exhaust is a
    real card that goes into a real pile, so it thickens the deck it lands
    in — which is why Exile is the only permanent answer to one."""

    def __init__(self, target, kind, n=1, where='deck_bottom'):
        self.target, self.kind, self.n, self.where = target, kind, n, where

    def apply(self, ctx):
        from cards import status_card
        for who in ctx.resolve(self.target, f'Add {self.kind}'):
            for _ in range(self.n):
                card = status_card(self.kind)
                if self.where == 'hand':
                    who.hand.append(card)
                else:
                    who.deck.insert(0, card)
            where = 'hand' if self.where == 'hand' else 'the bottom of their deck'
            ctx.log(f'  {self.n} {self.kind} to {who.name}\'s {where}.')


class RemoveStatusCards(Op):
    """Wounds cleared out of a hand and discard pile. Removed from play, not
    discarded — a status card that leaves is destroyed."""

    def __init__(self, target, kind='Wound'):
        self.target, self.kind = target, kind

    def apply(self, ctx):
        for who in ctx.resolve(self.target, f'Clear {self.kind}s from'):
            gone = 0
            for pile in (who.hand, who.discard):
                keep = [c for c in pile if c.name != self.kind.upper()]
                gone += len(pile) - len(keep)
                pile[:] = keep
            ctx.log(f'  {gone} {self.kind}(s) removed from {who.name}.')


class Reveal(Op):
    """Information. The engine knows the hand, so it simply says it."""

    def __init__(self, target):
        self.target = target

    def apply(self, ctx):
        for who in ctx.resolve(self.target, 'Reveal'):
            ctx.log(f'  {who.name}\'s hand: '
                    + (', '.join(c.name for c in who.hand) or '(empty)'))


class ExileCardInPlay(Op):
    """FORGET: the card the other side just played leaves for the fight."""

    def apply(self, ctx):
        card = getattr(ctx, 'opponent_card', None)
        if ctx.opponent is None or card is None:
            return
        if card in ctx.opponent.discard:
            ctx.opponent.discard.remove(card)
        ctx.opponent.exiled.append(card)
        ctx.log(f'  {card.name} is Exiled for the rest of combat.')


class HealByStat(Op):
    def __init__(self, target, stat, mult):
        self.target, self.stat, self.mult = target, stat, mult

    def apply(self, ctx):
        for who in ctx.resolve(self.target, 'Heal'):
            amount = self.mult * ctx.actor.stat(self.stat)
            who.heal(amount, log=ctx.log)
            ctx.log(f'  {who.name} heals {amount} ({who.hp}/{who.max_hp} HP).')


# ---- the reader --------------------------------------------------------
#
# A half is read left to right. Each rule below consumes a prefix of the
# remaining text and yields ops; when nothing matches what is left, the
# half has not been understood and the whole thing narrates instead.

def _statuses(text):
    """'Protect and Resist' -> [('protect',1),('resist',1)];
    'Thorns 4' -> [('thorns',4)]; 'Deadly twice' -> [('deadly',2)]."""
    out = []
    for part in re.split(r',\s*(?:and\s+)?|\s+and\s+', text.strip()):
        part = part.strip().rstrip('.')
        if not part:
            continue
        m = re.match(rf'^({STATUS_RE})(?:\s+(\d+)|\s+(twice))?$', part, re.I)
        if not m:
            return None
        n = int(m.group(2)) if m.group(2) else (2 if m.group(3) else 1)
        out.append((m.group(1).lower(), n))
    return out or None


def _grants(target, text):
    parsed = _statuses(text)
    if parsed is None:
        return None
    return [Grant(target, s, n) for s, n in parsed]


WHO = {
    'you': SELF, 'yourself': SELF, 'self': SELF,
    'defender': OPPONENT, 'the defender': OPPONENT, 'them': OPPONENT,
    'attacker': OPPONENT, 'the attacker': OPPONENT,
    'target ally': ALLY, 'an ally': ALLY, 'a target ally': ALLY,
    'all allies': ALL_ALLIES, 'your party': PARTY,
    'you and all allies': PARTY, 'any target': ANY,
    # Bare "target" is the other side of this exchange — PUSH moves the
    # defender, SUNDER drains them. Only "any target" is a free choice.
    'target': OPPONENT,
    'each enemy': ALL_ENEMIES, 'every enemy': ALL_ENEMIES,
    'all enemies': ALL_ENEMIES, 'target enemy': OPPONENT,
    'target ally in your position': ALLY, 'an enemy': OPPONENT,
}


def _who(word):
    return WHO.get((word or '').strip().lower().rstrip('.'))


RULES = []


def rule(pattern):
    def wrap(fn):
        RULES.append((re.compile(pattern, re.I), fn))
        return fn
    return wrap


# -- grants ------------------------------------------------------------

@rule(rf'^(?:you\s+)?gains?\s+((?:{STATUS_RE})(?:[\s,]+(?:and\s+)?(?:{STATUS_RE})(?:\s+\d+|\s+twice)?)*(?:\s+\d+|\s+twice)?)')
def _r_gain_self(m):
    return _grants(SELF, m.group(1))


@rule(rf'^(you|the defender|defender|the attacker|attacker|target ally in your position|target ally|target enemy|all allies|target)\s+gains?\s+((?:{STATUS_RE})(?:[\s,]+(?:and\s+)?(?:{STATUS_RE})(?:\s+\d+|\s+twice)?)*(?:\s+\d+|\s+twice)?)')
def _r_gain_other(m):
    who = _who(m.group(1))
    return _grants(who, m.group(2)) if who else None


@rule(rf'^give (any target|target ally)\s+({STATUS_RE})')
def _r_give(m):
    who = _who(m.group(1))
    return [Grant(who, m.group(2).lower())] if who else None


# -- healing and HP ----------------------------------------------------

@rule(r'^(?:you and all allies|your party|all allies)\s+heals?\s+(\d+)(?:\s*HP)?')
def _r_heal_party(m):
    return [Heal(PARTY, int(m.group(1)))]


@rule(r'^target ally(?: in your position)?\s+heals?\s+(\d+)(?:\s*HP)?')
def _r_heal_ally(m):
    return [Heal(ALLY, int(m.group(1)))]


@rule(r'^heals?\s+(\d+)(?:\s*HP)?')
def _r_heal_self(m):
    return [Heal(INHERIT, int(m.group(1)))]


@rule(r'^pay\s+(\d+)\s*HP')
def _r_pay(m):
    return [PayHP(int(m.group(1)))]


@rule(r'^lose\s+(\d+)\s*HP')
def _r_lose(m):
    return [PayHP(int(m.group(1)))]


@rule(r'^lifesteal(?:\s*[—-]+\s*heal yourself for the full damage dealt)?')
def _r_lifesteal(m):
    return [Lifesteal()]


# -- damage ------------------------------------------------------------

@rule(r'^deal\s+(\d+)\s+(unpreventable\s+)?damage to (?:the\s+)?(attacker|defender)'
      r'(,\s*unpreventable)?')
def _r_damage(m):
    unp = bool(m.group(2) or m.group(3))
    return [Damage(OPPONENT, int(m.group(1)), unpreventable=unp)]


@rule(r'^deal\s+(\d+)\s+unpreventable damage to any enemy')
def _r_damage_any(m):
    return [Damage(ANY, int(m.group(1)), unpreventable=True)]


@rule(r'^counter attack')
def _r_counter(m):
    return [CounterAttack()]


# -- cards -------------------------------------------------------------

@rule(r'^target ally draws?\s+(\d+)')
def _r_draw_ally(m):
    return [Draw(ALLY, int(m.group(1)))]


@rule(r'^(?:and\s+)?draws?\s+(\d+)(?:\s+cards?)?')
def _r_draw(m):
    return [Draw(INHERIT, int(m.group(1)))]


@rule(r'^(defender|attacker) discards?\s+(\d+) card at random')
def _r_discard_them(m):
    return [Discard(OPPONENT, int(m.group(2)), at_random=True)]


@rule(r'^discard\s+(\d+)(?:\s+random)?(?:\s+cards?)?(?:\s+from your hand)?')
def _r_discard(m):
    return [Discard(SELF, int(m.group(1)))]


@rule(r'^exile\s+(\d+) cards? from your (hand|discard pile)')
def _r_exile(m):
    zone = 'hand' if m.group(2).lower() == 'hand' else 'discard'
    return [Exile(SELF, int(m.group(1)), zone)]


@rule(r'^(?:you and target ally each\s+)?scry\s+(\d+)')
def _r_scry(m):
    return [Scry(SELF, int(m.group(1)))]


# -- movement ----------------------------------------------------------

@rule(r'^move to the (backline|frontline)')
def _r_move_self_to(m):
    from engine import FRONT, BACK
    return [Move(SELF, BACK if m.group(1).lower() == 'backline' else FRONT)]


@rule(r'^move (?:the\s+)?(target|defender|attacker) to (?:the\s+)?(backline|frontline)')
def _r_move_them(m):
    from engine import FRONT, BACK
    who = _who(m.group(1))
    dest = BACK if m.group(2).lower() == 'backline' else FRONT
    return [Move(who, dest)] if who else None


@rule(r'^pull (defender|attacker) to (?:the\s+)?frontline')
def _r_pull(m):
    from engine import FRONT
    return [Move(OPPONENT, FRONT)]


@rule(r'^you may change positions?')
def _r_may_move(m):
    return [Move(SELF, optional=True)]


@rule(r'^you and (?:the\s+)?(?:defender|attacker) both move positions?')
def _r_both_move(m):
    return [Move(SELF), Move(OPPONENT)]


@rule(r'^you and the (?:defender|attacker) move into frontline')
def _r_both_front(m):
    from engine import FRONT
    return [Move(SELF, FRONT), Move(OPPONENT, FRONT)]


# -- initiative --------------------------------------------------------

@rule(r'^apply initiative shift\s+([+-]?\d+) to '
      r'(yourself|an ally|all allies|the attacker|attacker|defender|the defender|any target|them)')
def _r_shift(m):
    who = _who(m.group(2))
    return [Shift(who, int(m.group(1)))] if who else None


# -- stats and buff removal -------------------------------------------

@rule(r'^(target|defender|attacker) loses 1 (mind|body|soul) this combat')
def _r_statloss(m):
    who = _who(m.group(1))
    return [StatLoss(who, m.group(2).lower())] if who else None


@rule(r'^remove every positive status effect from the (defender|attacker)')
def _r_strip_all(m):
    return [Strip(OPPONENT, 'all')]


@rule(r'^remove one positive status effect of your choice from each enemy')
def _r_strip_each(m):
    return [Strip(ALL_ENEMIES, 'one')]


@rule(r"^steal one positive status effect of your choice that the (?:defender|attacker) "
      r"currently has\s*[—-]+\s*it'?s removed from them, not just copied")
def _r_steal(m):
    return [Strip(OPPONENT, 'one', steal=True)]


@rule(r'^take 1 stack of a positive status effect the defender has\.?\s*it moves to you')
def _r_steal_stack(m):
    return [Strip(OPPONENT, 'one', steal=True)]


# ---- gates -------------------------------------------------------------

GATES = [
    (re.compile(r'^only on a clean win\s*[—-]*\s*(?:not a tie)?[.,]?\s*', re.I),
     lambda ctx: ctx.outcome == 'attacker wins', 'clean win only'),
    (re.compile(r'^on a clean win only[.,]?\s*', re.I),
     lambda ctx: ctx.outcome == 'attacker wins', 'clean win only'),
    (re.compile(r'^on a clean win,\s*', re.I),
     lambda ctx: ctx.outcome == 'attacker wins', 'clean win only'),
    (re.compile(r'^only on a tie[.,]?\s*', re.I),
     lambda ctx: ctx.outcome == 'tie', 'tie only'),
    (re.compile(r'^if your HP is (\d+) or less,\s*', re.I),
     None, 'HP threshold'),
    (re.compile(r'^if this attack deals damage,\s*', re.I),
     lambda ctx: ctx.damage_dealt > 0, 'damage dealt'),
    (re.compile(r'^if target ally\'s HP is (\d+) or less,\s*', re.I),
     None, 'ally HP threshold'),
]

SEP = re.compile(r'^\s*(?:[.,;]|\s+and\b|\s+then\b)+\s*', re.I)


def compile_half(text):
    """Prose to ops, or None when any part of it is not understood."""
    if not text:
        return None
    s = ' '.join(text.split()).strip()
    if s.lower() in ('none.', 'none', ''):
        return None

    # A trailing gate reads the same as a leading one (FORGET puts it last).
    trailing = re.search(
        r'\.\s*((?:only on a clean win\s*[—-]*\s*not a tie|on a clean win only)\.?)$',
        s, re.I)
    if trailing:
        s = s[:trailing.start()] + '.'
        s = trailing.group(1) + ' ' + s

    # Anchored wraps everything after it.
    m = re.match(r'^anchored\s*[—-]+\s*(.+)$', s, re.I)
    if m:
        # "at the start of each of your turns" restates Anchored's own
        # definition; the op already fires then.
        body = re.sub(r'(?:,\s*)?at the start of each of your turns[,]?\s*',
                      '', m.group(1), flags=re.I).strip()
        inner = compile_half(body)
        return [Anchored(inner, body)] if inner else None

    gate = None
    for pattern, test, label in GATES:
        g = pattern.match(s)
        if g:
            s = s[g.end():]
            if test is None:
                n = int(g.group(1))
                who = 'ally' if 'ally' in label else 'self'
                test = (lambda n, who: (lambda ctx: (
                    (ctx.resolve(ALLY)[0] if who == 'ally' else ctx.actor).hp <= n
                )))(n, who)
            gate = (test, label)
            break

    ops = []
    while s:
        sep = SEP.match(s)
        if sep and sep.end():
            s = s[sep.end():]
            if not s:
                break
        for pattern, fn in RULES:
            m = pattern.match(s)
            if not m:
                continue
            built = fn(m)
            if built is None:
                continue
            ops.extend(built)
            s = s[m.end():]
            break
        else:
            return None

    if not ops:
        return None

    subject = SELF
    for op in ops:
        target = getattr(op, 'target', None)
        if target == INHERIT:
            op.target = subject
        elif target in (SELF, OPPONENT, ALLY, ALL_ALLIES, ALL_ENEMIES, PARTY, ANY):
            subject = target

    if gate:
        return [Gated(gate[0], ops, gate[1])]
    return ops


# -- second pass: shapes the first pass left narrated --------------------

@rule(r'^(?:apply\s+)?initiative shift\s+([+-]?\d+) to '
      r'(yourself|an ally|all allies|the attacker|attacker|defender|the defender|any target|them)')
def _r_shift2(m):
    who = _who(m.group(2))
    return [Shift(who, int(m.group(1)))] if who else None


@rule(r'^(?:move|push) (?:the\s+)?(target|defender|attacker|any target) to '
      r'(?:the\s+)?(?:backline|other position|position of your choice)')
def _r_push(m):
    from engine import BACK
    who = _who(m.group(1))
    return [Move(who, BACK)] if who else None


@rule(r'^move self to any position')
def _r_move_any(m):
    return [Move(SELF, optional=True)]


@rule(r'^all enemies must move to backline if possible')
def _r_repel(m):
    from engine import BACK
    return [Move(ALL_ENEMIES, BACK)]


@rule(r'^add (\d+) exhaust cards? to your hand')
def _r_exhaust(m):
    return [AddStatusCard(SELF, 'Exhaust', int(m.group(1)), where='hand')]


@rule(r"^add (\d+) wound to the bottom of (?:the\s+)?(defender|attacker)'?s? deck")
def _r_wound(m):
    return [AddStatusCard(OPPONENT, 'Wound', int(m.group(1)))]


@rule(r"^remove all wounds (?:from target ally'?s? hand and discard pile|"
      r"in your hand and discard pile)")
def _r_dewound(m):
    return [RemoveStatusCards(ALLY if 'target ally' in m.group(0).lower() else SELF)]


@rule(r"^(?:they\s+)?heals?\s+(\d+)\s*HP")
def _r_heal_they(m):
    return [Heal(INHERIT, int(m.group(1)))]


@rule(r'^heal\s+(\d+)\s*[x×]\s*your (soul|body|mind)')
def _r_heal_stat(m):
    return [HealByStat(SELF, m.group(2).lower(), int(m.group(1)))]


@rule(r'^target collapsed ally heals?\s+(\d+)(?:\s*HP)?')
def _r_heal_collapsed(m):
    return [Heal(ALLY, int(m.group(1)))]


@rule(r"^(?:look at the (defender|attacker)'?s hand|(defender|attacker) reveals hand)")
def _r_reveal(m):
    return [Reveal(OPPONENT)]


@rule(r"^exile the (?:defender|attacker)'?s card until end of combat")
def _r_forget(m):
    return [ExileCardInPlay()]


# ---- coverage ----------------------------------------------------------

def coverage(pool):
    """(compiled, narrated) halves, for `python3 effects.py`."""
    done, left = [], []
    for c in pool:
        for half, text in (('E', c.effect), ('D', c.defense_effect)):
            if not text or text.strip().lower() in ('none.', 'none'):
                continue
            (done if compile_half(text) else left).append((c.name, half, text.strip()))
    return done, left


if __name__ == '__main__':
    import sys
    import cards as cardlib

    pool = cardlib.core_pool()
    done, left = coverage(pool)
    total = len(done) + len(left)
    print(f'{len(done)}/{total} effect halves compile '
          f'({100 * len(done) / total:.0f}%), {len(left)} narrate.\n')

    if '-v' in sys.argv:
        print('Narrated:')
        for name, half, text in sorted(left):
            print(f'  {name:<18} {half}  {text[:96]}')
