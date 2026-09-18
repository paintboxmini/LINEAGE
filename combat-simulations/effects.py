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

# Narrower shapes a card can name.
ALLIES_HERE = 'allies_here'          # allies sharing your position
FRONT_ENEMIES = 'front_enemies'      # every enemy in the Frontline
OTHER_ENEMY = 'other_enemy'          # a random enemy that is not the defender
SELF_AND_ALLY = 'self_and_ally'      # "you and target ally each ..."


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
        # One half names its target once. "Target ally heals 4 and draws 1"
        # is one ally doing both, so the choice is made on the first clause
        # and reused by the rest — otherwise a human is asked twice and can
        # answer differently, which the card does not allow.
        self._picked = {}

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
        if spec == ALLIES_HERE:
            return [a for a in self.allies if a.position == self.actor.position]
        if spec == FRONT_ENEMIES:
            from engine import FRONT
            return [e for e in self.enemies if e.position == FRONT]
        if spec == OTHER_ENEMY:
            rest = [e for e in self.enemies if e is not self.opponent]
            if not rest:
                return []
            rng = self.rng or __import__('random')
            return [rng.choice(rest)]
        if spec == SELF_AND_ALLY:
            return [self.actor] + self.resolve(ALLY, prompt)
        if spec == ALLY:
            pool = self.allies or [self.actor]
            return [self._ask(spec, pool, prompt)]
        if spec == ANY:
            pool = [self.actor] + self.allies + self.enemies
            return [self._ask(spec, pool, prompt)]
        return []

    def _ask(self, spec, pool, prompt):
        if spec in self._picked:
            return self._picked[spec]
        if len(pool) == 1 or self.agent is None:
            choice = pool[0]
        else:
            choice = self.agent.choose_target(self.actor, pool, prompt)
        self._picked[spec] = choice
        return choice


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

    SKEWER and CONSUME used to write "heal yourself for the full damage
    dealt", which contradicted the glossary and was the number the
    middle-tier ruling on this keyword was made against. Settled on
    2026-09-18 in the glossary's favour: both cards now say only
    *Lifesteal*, and the keyword is beginner-legal again.
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


class Choose(Op):
    """A card that offers a menu. The holder picks one branch and only that
    branch runs — CHANNEL, STILL POINT, HASTEN, WAIT."""

    def __init__(self, branches, labels):
        self.branches, self.labels = branches, labels

    def apply(self, ctx):
        i = 0
        if ctx.agent is not None and len(self.branches) > 1:
            pick = ctx.agent.choose_option(ctx.actor, list(self.labels), 'Choose one')
            i = self.labels.index(pick) if pick in self.labels else 0
        ctx.log(f'  chooses: {self.labels[i]}')
        for op in self.branches[i]:
            op.apply(ctx)


class MayPay(Op):
    """An optional cost with an attached rider — CONSUME's Exile. Declined
    costs nothing and grants nothing."""

    def __init__(self, cost, gain, label):
        self.cost, self.gain, self.label = cost, gain, label

    def apply(self, ctx):
        if ctx.agent is not None and not ctx.agent.choose_yes_no(ctx.actor, self.label):
            return
        if not ctx.actor.hand:
            ctx.log('  nothing in hand to pay with.')
            return
        for op in self.cost + self.gain:
            op.apply(ctx)


class Rushdown(Op):
    """`rules/combat.md`, Positioning -> Rushdown.

    Not a move behind their line and not a shove of theirs. The line of
    conflict is a relative thing — where each combatant stands in relation
    to it, not a fixed place on a map — so closing on a Backline enemy
    redraws the line to sit between the two of you. Both of you are
    Frontline afterwards because that is what the line now means.

    Which is why the target's own Rooted does not stop it: they never
    changed position. The line came to them. The mover's Rooted does stop
    it, the same as any other movement of their own.
    """

    def apply(self, ctx):
        from engine import FRONT
        target = ctx.opponent
        if target is None:
            return
        if ctx.actor.position != FRONT:
            ctx.log(f'  {ctx.actor.name} must be Frontline to Rushdown.')
            return
        if ctx.actor.rooted > 0:
            ctx.actor.rooted -= 1
            ctx.log(f'  {ctx.actor.name} is Rooted — the Rushdown is cancelled.')
            return
        if target.position == FRONT:
            return
        target._position = FRONT          # the line moved, they did not
        target.break_anchors(ctx.log, reason='the line closed on them')
        ctx.log(f'  {ctx.actor.name} closes — the Frontline is between them '
                f'and {target.name} now.')


class ReturnToHand(Op):
    """FOCUS: the card comes back instead of going to the discard. _finish
    discards it after the Effect runs, so it is marked and skipped there."""

    def apply(self, ctx):
        if ctx.card is not None:
            ctx.return_card = True
            ctx.log(f'  {ctx.card.name} returns to hand.')


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
    'they': INHERIT, 'all allies in your position': ALLIES_HERE,
    'all frontline enemies': FRONT_ENEMIES,
    'a random enemy other than the defender': OTHER_ENEMY,
    'you and target ally': SELF_AND_ALLY,
    'target ally in your position': ALLY, 'an enemy': OPPONENT,
}


def _who(word):
    return WHO.get((word or '').strip().lower().rstrip('.'))


RULES = []
MENU_RULES = []


def rule(pattern):
    def wrap(fn):
        RULES.append((re.compile(pattern, re.I), fn))
        return fn
    return wrap


def menu(pattern):
    """Checked before RULES. A menu must be read whole — otherwise an
    ordinary rule consumes its first branch and the rest fails to parse,
    which is how STILL POINT and HASTEN were being lost."""
    def wrap(fn):
        MENU_RULES.append((re.compile(pattern, re.I), fn))
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


@rule(r'^lifesteal')
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
    gate_subject = None
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
            if 'ally' in label:
                gate_subject = ALLY
            break

    ops = []
    while s:
        sep = SEP.match(s)
        if sep and sep.end():
            s = s[sep.end():]
            if not s:
                break
        for pattern, fn in MENU_RULES + RULES:
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

    subject = gate_subject or SELF
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
      r'(?:the\s+)?(backline|other position|position of your choice)')
def _r_push(m):
    """"To the backline" is a destination. "The other position" is a flip,
    which is not the same thing when they are already in the Backline."""
    from engine import BACK
    who = _who(m.group(1))
    if not who:
        return None
    dest = BACK if m.group(2).lower() == 'backline' else None
    return [Move(who, dest)]


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


# -- third pass: the cheap tail ------------------------------------------

@rule(rf'^(?:and\s+)?(?:they\s+)?gains?\s+((?:{STATUS_RE})(?:[\s,]+(?:and\s+)?(?:{STATUS_RE})(?:\s+\d+|\s+twice)?)*(?:\s+\d+|\s+twice)?)')
def _r_gain_inherit(m):
    return [Grant(INHERIT, s_, n) for s_, n in (_statuses(m.group(1)) or [])] or None


@rule(rf'^all allies in your position gains?\s+({STATUS_RE})')
def _r_gain_here(m):
    return [Grant(ALLIES_HERE, m.group(1).lower())]


@rule(rf'^apply ({STATUS_RE}) to all frontline enemies, and to yourself')
def _r_smokescreen(m):
    return [Grant(FRONT_ENEMIES, m.group(1).lower()), Grant(SELF, m.group(1).lower())]


@rule(rf'^apply ({STATUS_RE}) to (any target|target ally|all allies)')
def _r_apply_to(m):
    who = _who(m.group(2))
    return [Grant(who, m.group(1).lower())] if who else None


@rule(r'^deal\s+(\d+)\s+unpreventable damage to a random enemy other than the defender')
def _r_splash(m):
    return [Damage(OTHER_ENEMY, int(m.group(1)), unpreventable=True)]


@rule(r'^(?:and\s+)?may change positions?')
def _r_may_move_inherit(m):
    return [Move(INHERIT, optional=True)]


@rule(r'^all allies may change positions?')
def _r_allies_may_move(m):
    return [Move(ALL_ALLIES, optional=True)]


@rule(r'^you and target ally each scry\s+(\d+)')
def _r_pair_scry(m):
    return [Scry(SELF_AND_ALLY, int(m.group(1)))]


@rule(r'^(?:each\s+)?draws?\s+(\d+)')
def _r_pair_draw(m):
    return [Draw(INHERIT, int(m.group(1)))]


@rule(r'^rushdown')
def _r_rushdown(m):
    return [Rushdown()]


@rule(r'^return this card to your hand')
def _r_return(m):
    return [ReturnToHand()]


@rule(r'^move with them')
def _r_move_along(m):
    return [Move(SELF)]


@rule(r'^if this is a tie, deal\s+(\d+) instead')
def _r_tie_instead(m):
    """DEAD HEAT: the tie branch replaces the flat damage above it rather
    than adding to it, so it undoes the difference."""
    return [Gated(lambda ctx: ctx.outcome == 'tie',
                  [Damage(OPPONENT, int(m.group(1)) - 2, unpreventable=False)],
                  'tie tops it up')]


# -- modal cards: a menu where only the chosen branch runs ---------------

def _branches(text, sep=r',\s*or\s+|\s+or\s+|,\s*'):
    """Split a menu into branches, compiling each. All or nothing: a menu
    with one unreadable option is not a menu this can offer."""
    parts = [p.strip().rstrip('.') for p in re.split(sep, text) if p.strip()]
    out, labels = [], []
    for part in parts:
        ops = compile_half(part)
        if ops is None:
            return None, None
        out.append(ops)
        labels.append(part)
    return (out, labels) if len(out) > 1 else (None, None)


@menu(r'^choose one for target ally\s*[—-]+\s*(.+?)\.?$')
def _r_channel(m):
    """CHANNEL — the menu is for the ally, so each branch is read as theirs."""
    body = m.group(1)
    parts = [p.strip() for p in re.split(r',\s*or\s+|,\s*', body) if p.strip()]
    branches, labels = [], []
    for part in parts:
        ops = compile_half(part)
        if ops is None:
            return None
        for op in ops:
            if getattr(op, 'target', None) in (SELF, INHERIT):
                op.target = ALLY
        branches.append(ops)
        labels.append(part)
    return [Choose(branches, labels)] if len(branches) > 1 else None


@menu(r'^scry 1, gain ward, or apply weak to any target')
def _r_still_point(m):
    return [Choose([[Scry(SELF, 1)], [Grant(SELF, 'ward')], [Grant(ANY, 'weak')]],
                   ['Scry 1', 'gain Ward', 'apply Weak to any target'])]


@menu(r'^apply initiative shift \+1 to yourself, or -1 to the attacker \(choose\)')
def _r_hasten(m):
    return [Choose([[Shift(SELF, 1)], [Shift(OPPONENT, -1)]],
                   ['Initiative Shift +1 to yourself',
                    'Initiative Shift -1 to the attacker'])]


@menu(r'^apply initiative shift -1, -2, or -3 to yourself \(choose\)')
def _r_wait(m):
    return [Choose([[Shift(SELF, -1)], [Shift(SELF, -2)], [Shift(SELF, -3)]],
                   ['-1', '-2', '-3'])]


@menu(r'^you may exile one card from your own hand to give the (?:defender|attacker) '
      r'weak and blind')
def _r_consume_cost(m):
    return [MayPay([Exile(SELF, 1, 'hand')],
                   [Grant(OPPONENT, 'weak'), Grant(OPPONENT, 'blind')],
                   'Exile a card to apply Weak and Blind')]


# ---- coverage ------------------------------------------------------
#
# Keep this block last. @rule registers at import time, so a rule
# defined below the __main__ guard is not registered when this file is
# run as a script — it silently does not count.
# ---- ----------------------------------------------------------

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
