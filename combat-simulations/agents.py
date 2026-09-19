"""Who decides what a combatant does.

Three kinds: a human at the keyboard, a scripted opponent, and a random
one. All three answer the same three questions, so any mix can share a
table — a human party against scripted creatures is the normal case.
"""

import random

from engine import FRONT, BACK


class Knowledge:
    """What one combatant has been allowed to notice about another.

    **The hidden zones are hidden, and that is not negotiable by an agent
    that would play better with a peek.** A hand is hidden. A deck is
    hidden. So are HP, max HP and the stat line — an agent may not read
    them and may not decide anything on them.

    What is public is what happens in front of everyone: a card is revealed
    to be played, and after the exchange it goes to the discard where it
    stays face up. An Ongoing Effect sits on the table. A hit is announced
    with its number. Position, Down and the status tokens are all on the
    table too.

    So knowing an opponent is not a lookup, it is a slow accumulation, and
    an agent early in a fight is supposed to be ignorant. Every card they
    reveal is one more sample of a deck whose colour counts follow their
    stat line (`rules/cards.md`, Enemy decks) — which means **watching
    someone play is how you learn their stats**, the same inference the
    deck rule's side effect describes, run the legal way round.

    Memory rather than a live read of the discard pile, deliberately: a
    deck reshuffles when it runs out and the pile empties, and nobody at
    the table forgets what they watched go into it.
    """

    def __init__(self):
        self.colors = {}      # name -> Counter of colours revealed
        self._seen = {}       # name -> ids already counted

    def observe(self, other):
        """Fold in whatever of theirs is currently face up."""
        from collections import Counter
        seen = self._seen.setdefault(other.name, set())
        counts = self.colors.setdefault(other.name, Counter())
        for card in list(other.discard) + list(other.in_play):
            if id(card) in seen:
                continue
            seen.add(id(card))
            if card.color:
                counts[card.color] += 1
        return counts

    def color_odds(self, other, color):
        """(P(they play a colour this one beats), P(they play this one)).

        Laplace-smoothed toward "no idea", so the first exchange of a fight
        is a shrug and the tenth is an opinion.
        """
        from cards import BEATS
        counts = self.observe(other)
        alpha = 1.0
        n = sum(counts.values()) + 3 * alpha
        return ((counts.get(BEATS.get(color), 0) + alpha) / n,
                (counts.get(color, 0) + alpha) / n)


class Agent:
    def __init__(self, rng=None):
        self.rng = rng or random
        self.known = Knowledge()

    def choose_action(self, me, foes, allies):
        """Return ('attack', target) | ('move',) | ('cover',) | ('pass',)."""
        raise NotImplementedError

    def choose_attack(self, me, target):
        """Return a Card from me.hand that is range-legal, or None."""
        raise NotImplementedError

    def choose_defense(self, me, attacker):
        """Return a range-legal Card from me.hand, or None to take the hit."""
        raise NotImplementedError

    # ---- choices a card Effect asks for (effects.py) --------------------
    #
    # Defaults that are legal and not stupid, so a new agent only overrides
    # what it wants an opinion about.

    def choose_target(self, me, options, prompt='Target'):
        return options[0]

    def choose_option(self, me, options, prompt='Choose'):
        return options[0]

    def choose_yes_no(self, me, prompt):
        return True

    def choose_amount(self, me, low, high, prompt='How much'):
        return high

    def scry(self, who, look, opponent=None):
        """Return (keep_on_top, send_to_bottom). Top of deck is last."""
        return look, []

    # ---- the shape of a kit --------------------------------------------

    def _prefer_hand(self, me, opts):
        """A Passive is the floor, not a pick.

        **It is always the weakest thing you have**, and that is what it is
        for: it has a colour, a Range and a die and no Effect at all, where
        every card in a deck carries text. Having it means never being
        unable to act — never a turn with no legal attack, never an
        exchange with no legal block — and the price of always having it is
        that it loses to anything you could have played instead.

        So the order is: play your strong options, fall back on your weak
        one when you need to. A Passive is reached for when the hand has
        nothing legal, not when it happens to roll a bigger number.

        Scoring alone will not produce that. Chris's MIMETIC BLADE is Body
        3 + d6, which is 6.0 on expected damage and above most of what he
        is holding, so a value function ranked it first and he opened with
        it in 57% of his attacks — a Passive as a main line, which is
        backwards. The rule belongs here rather than in the weights,
        because it is a fact about what a Passive is and not a number to be
        tuned.
        """
        hand = [c for c in opts if not me.is_passive(c)]
        return hand or opts


class RandomAgent(Agent):
    """Plays legally and at random. Useful as a baseline opponent and for
    shaking out illegal states."""

    def choose_action(self, me, foes, allies):
        live = [f for f in foes if f.alive()]
        if not live:
            return ('pass',)
        if me.down:
            return ('pass',)
        if me.playable(live[0]) or len(live) > 1:
            for f in self.rng.sample(live, len(live)):
                if me.playable(f):
                    return ('attack', f)
        if not me.rooted:
            return ('move',)
        return ('pass',)

    def choose_attack(self, me, target):
        opts = me.playable(target)
        return self.rng.choice(opts) if opts else None

    def choose_defense(self, me, attacker):
        opts = me.playable(attacker)
        return self.rng.choice(opts) if opts else None


class SimpleAI(Agent):
    """A creature that plays to type rather than at random: closes when it
    can attack, hits the weakest reachable target, defends with the colour
    that beats what it has most often seen. Not clever — just not random."""

    def choose_action(self, me, foes, allies):
        if me.down:
            return ('pass',)
        live = [f for f in foes if f.alive()]
        if not live:
            return ('pass',)
        reachable = [f for f in live if me.playable(f)]
        if reachable:
            return ('attack', self._weakest(reachable))
        if not me.rooted:
            return ('move',)
        return ('pass',)

    def _weakest(self, options):
        """Whoever the table has watched absorb the most, ties at random.

        **Not HP, and not a fraction of it.** Neither is public
        (`Knowledge`). What is public is the damage announced as it lands,
        so the most anyone can honestly say is "I have put more into that
        one than into this one" — never how much is left, which would need
        a max HP nobody was shown. It is a cruder signal than HP on
        purpose, and it costs the agent something: a big creature that has
        soaked a lot still reads as the hurt one.

        Ties break at random, which is not a detail. `min` breaks a tie by
        list order, and list order is the same on every turn of every
        fight: with two party members level, every creature in the
        encounter picked the same one, forever. Measured over 250 fights,
        whoever was listed first of two 18 HP characters took ~1600 attacks
        and went down 62-71% of the time while the other took ~700 and went
        down under 30% — and they swapped when the list was reordered. It
        read as a finding about a character and was a finding about a list.
        """
        worst = max(f.seen_damage for f in options)
        tied = [f for f in options if f.seen_damage >= worst]
        return self.rng.choice(tied) if len(tied) > 1 else tied[0]

    def choose_attack(self, me, target):
        opts = self._prefer_hand(me, me.playable(target))
        if not opts:
            return None
        # Biggest expected damage, ties broken by the bigger die.
        return max(opts, key=lambda c: (me.stat(c.stat) + c.die / 2, c.die))

    def choose_defense(self, me, attacker):
        opts = self._prefer_hand(me, me.playable(attacker))
        if not opts:
            return None
        return max(opts, key=lambda c: (me.stat(c.stat) + c.die / 2, c.die))

    def choose_target(self, me, options, prompt='Target'):
        """Help the ally who has taken the most; hurt the enemy who has.
        Which way round is decided by whose side they are on.

        Both read `seen_damage` rather than HP, for the reason in
        `_weakest` — and note it is the same measure on both sides now,
        where this class once used raw HP in one method and the fraction in
        the other, one method apart.
        """
        friends = [o for o in options if o.team == me.team]
        if friends and any(w in prompt.lower() for w in
                           ('heal', 'give', 'protect', 'draw', 'ally')):
            return self._weakest(friends)
        foes = [o for o in options if o.team != me.team]
        return self._weakest(foes or options)

    def choose_option(self, me, options, prompt='Choose'):
        return options[0]

    def choose_yes_no(self, me, prompt):
        return True

    def choose_amount(self, me, low, high, prompt='How much'):
        """Give what can be spared rather than everything: half the room,
        so a transfer never leaves the giver on the floor."""
        return max(low, min(high, (low + high) // 2))

    def scry(self, who, look, opponent=None):
        """Bottom the cards that cannot be played from here, keep the rest.
        A Wound or an Exhaust is always worth bottoming."""
        keep, bottom = [], []
        for c in look:
            playable = opponent is None or c.range_ok(who.position, opponent.position)
            (keep if playable and c.color != 'COLORLESS' else bottom).append(c)
        return keep, bottom


class HumanAgent(Agent):
    """Prompts at the terminal. Always shows the legal options and nothing
    else, so an illegal choice is not reachable from the menu."""

    def __init__(self, ask=input, show=print):
        super().__init__()
        self.ask, self.show = ask, show

    def _health(self, me, other):
        """What this player is entitled to see about someone's condition.

        Their own sheet, or a teammate's, is theirs to read. An opponent's
        is not: `Knowledge` makes HP and max HP hidden for agents, and a
        human reading them off the prompt would be the same leak with a
        person in the loop. What everyone can see is the damage that has
        been announced as it landed, and whether they are still standing.
        """
        if other is me or other.team == me.team:
            return f'{other.hp}/{other.max_hp} HP'
        return (f'{other.seen_damage} damage taken'
                + (', DOWN' if other.down else ''))

    def _pick(self, prompt, options, allow_none=False):
        if not options:
            return None
        for i, (label, _) in enumerate(options, 1):
            self.show(f'   {i}. {label}')
        if allow_none:
            self.show('   0. (none)')
        while True:
            raw = self.ask(f'{prompt} > ').strip()
            if raw == '0' and allow_none:
                return None
            if raw.isdigit() and 1 <= int(raw) <= len(options):
                return options[int(raw) - 1][1]
            self.show('   — pick one of the listed numbers.')

    def choose_action(self, me, foes, allies):
        live = [f for f in foes if f.alive()]
        opts = []
        for f in live:
            legal = me.playable(f)
            if legal and not me.down:
                opts.append((f'Attack {f.name} ({self._health(me, f)}, '
                             f'{f.position})', ('attack', f)))
        if not me.down and not me.rooted:
            other = BACK if me.position == FRONT else FRONT
            opts.append((f'Move Position → {other}', ('move',)))
            if me.position == BACK:
                opts.append(('Take Cover (persistent dodge until you attack)', ('cover',)))
        opts.append(('Pass', ('pass',)))
        self.show(f'\n {me.name} — {me.hp}/{me.max_hp} HP, {me.position}'
                  + (' [DOWN]' if me.down else ''))
        self.show(f' Hand: ' + ', '.join(f'{c.name}({c.color[0]})' for c in me.hand))
        return self._pick('Action', opts)

    def choose_attack(self, me, target):
        legal = me.playable(target)
        opts = [(f'{c.name} — {c.color}, {c.attack}, {c.range}', c) for c in legal]
        self.show(f'\n Attacking {target.name}:')
        return self._pick('Card', opts)

    def choose_defense(self, me, attacker):
        legal = me.playable(attacker)
        if not legal:
            self.show(f'\n {me.name} has no legal defense against '
                      f'{attacker.name}.')
            return None
        opts = [(f'{c.name} — {c.color}, def: {c.defense_effect or "None."}', c)
                for c in legal]
        self.show(f'\n {attacker.name} attacks {me.name} '
                  f'({me.hp}/{me.max_hp} HP). Defend with:')
        return self._pick('Defense', opts, allow_none=True)

    # ---- Effect choices -------------------------------------------------

    def choose_target(self, me, options, prompt='Target'):
        opts = [(f'{c.name} ({self._health(me, c)}, {c.position})', c)
                for c in options]
        self.show(f'\n {prompt}:')
        return self._pick('Target', opts)

    def choose_option(self, me, options, prompt='Choose'):
        self.show(f'\n {prompt}:')
        return self._pick('Option', [(str(o).title(), o) for o in options])

    def choose_yes_no(self, me, prompt):
        while True:
            raw = self.ask(f' {prompt}? [y/n] > ').strip().lower()
            if raw in ('y', 'yes'):
                return True
            if raw in ('n', 'no'):
                return False

    def scry(self, who, look, opponent=None):
        keep, bottom = [], []
        self.show(f'\n Scrying {len(look)}:')
        for c in look:
            where = self._pick(f'{c.name} ({c.color})',
                               [('Top', 'top'), ('Bottom', 'bottom')])
            (keep if where == 'top' else bottom).append(c)
        return keep, bottom

    def choose_amount(self, me, low, high, prompt='How much'):
        while True:
            raw = self.ask(f' {prompt} ({low}-{high}) > ').strip()
            if raw.isdigit() and low <= int(raw) <= high:
                return int(raw)
            self.show(f'   — a number from {low} to {high}.')


class KitAI(SimpleAI):
    """Plays a character's kit rather than maximising one damage roll.

    `SimpleAI` picks the biggest expected number, on attack and on defence
    alike, and that is the right baseline for a creature — it is also why
    the structural encounter figures in `rules/gm-guide.md` are built on it
    and should stay built on it. **This is the agent for a player
    character**, where "the biggest number" is often the wrong play and
    sometimes actively throws the kit away.

    Four things it knows that SimpleAI does not:

    1. **A defence is won on colour, not on damage.** A defender who wins
       deals nothing, so scoring a block by its Attack line is scoring the
       wrong thing entirely. This scores it by the odds of actually winning
       the reveal, read off what colours the attacker's deck is made of.
    2. **Some cards cannot deal damage at all.** HOLD THE LINE mirrors its
       opponent's colour and therefore always ties, so attacking with it is
       a guaranteed nothing — and blocking with it is a guaranteed stop.
       Same card, opposite value, depending on which side of the exchange.
    3. **A colour played twice running can cost you a stance.** KILLSWITCH
       ends on the same colour two attacks in a row, so while it is up, a
       repeat is not free.
    4. **Some effects are worth more than the damage on the card.** Setting
       a stance that is not up, putting a totem on the table that buffs the
       whole party, banking a tie-win.

    Everything here is a heuristic about card *properties* the engine can
    already see — a gated colour change, a stance that ends on a repeat, a
    summon — rather than a list of card names.

    **Measured, and the result is not what it looks like at first.**

    In a **duel** this is worth nothing. Mirror matches — the same kit on
    both sides, one agent each — put it at parity with SimpleAI at best,
    and an early version lost 60/40. A duel is a pure damage race with no
    allies and no time, and in one of those "play the biggest card" is very
    nearly the correct strategy. Ablated a method at a time, the duel gives
    50.0% for every part of this class on every character — which is to say
    the benchmark cannot see any of it, and a weight tuned against it is a
    weight tuned against nothing.

    In a **party fight** it is worth a great deal:

        party of three, 300 fights each      SimpleAI    KitAI
        vs 4 wrackclaws                        86.3%     88.3%
        vs 5 wrackclaws                        80.0%     83.7%

        who goes down, vs 5 wrackclaws       SimpleAI    KitAI
        Chris                                    31%       25%
        Kevin                                    27%       20%
        Pat                                      26%       21%

    It is ahead of `SimpleAI` on win rate and on down rate against every
    foe shape tried — 2/1/1, 1/2/1, 1/1/2, 2/2/2, 3/1/1, 1/3/1 — and the
    margin is widest against the shape that punishes a bad read: 80.0%
    against 89.6% at 1/3/1.

    That gap is the whole point of the class. Setup plays — a totem that
    buffs everyone, a drink handed to somebody else, a stance held across a
    long fight — pay back over time and across people, and neither of those
    things exists in a duel. **So judge an agent on the fight the character
    was built for, not on the convenient benchmark.**

    The weights are swept against the party fight rather than chosen by
    eye, and the honest reading is that **most of them do not matter**:

    - `_REPEAT_PENALTY` earns its keep, by about a point of win rate at
      both encounter sizes. Turning it off is the only single change in the
      grid that costs anything. Anywhere from -1.0 down is the same.
    - `_EFFECT_VALUE` is flat from 0.25 to 1.5 and costs about a point at
      0.0. It stays at 0.5, which is the middle of the flat part.
    - `_SETUP_BONUS`, `_STANCE_REPLAY` and `_BANK_TIE_WIN` move nothing
      measurable across their whole range. `_STANCE_REPLAY` in particular
      cannot fire at all: no deck runs a card twice, so once KILLSWITCH is
      face up there is no second copy to replay over it. They are kept
      because they are correct, not because they have been shown to pay.

    **A caution, because this sweep has now been wrong once.** An earlier
    reading of it concluded that `_SETUP_BONUS` was inert because "Chris
    never sets his stance" — KILLSWITCH legal 2232 times and chosen twice
    — and wrote that up as a finding about the card being priced out. It
    was not about the card. It was `_prefer_hand` missing: his MIMETIC
    BLADE Passive was competing on its number and crowding the stance out.
    With a Passive back in its place as the fallback, KILLSWITCH is chosen
    149 times of 698 and a stance is up on 597 turns of 2676. **A weight
    that reads as inert is as likely to mean the agent never reaches the
    situation as it is to mean the weight does not matter**, and the two
    look identical in the sweep.
    """

    # Weights, in damage-equivalents. Swept against the party fight rather
    # than chosen by eye — and mostly they do not matter. See the note on
    # tuning in the class docstring for which of them has been shown to.
    _EFFECT_VALUE = 0.5
    _SETUP_BONUS = 1.0      # a stance not yet up, or a totem not yet out
    _STANCE_REPLAY = -2.0   # the same stance again
    _REPEAT_PENALTY = -2.0  # a colour that would end a stance
    _BANK_TIE_WIN = 1.0

    # ---- shared scoring -------------------------------------------------

    def _expected(self, me, card):
        """Expected damage before any effect."""
        return me.stat(card.stat) + (card.die or 0) / 2

    def _ops(self, card, half):
        import engine
        try:
            return engine.compiled(card, half) or []
        except Exception:
            return []

    def _mirrors(self, card):
        """A card that takes its opponent's colour can never win the reveal
        on colour, so it always ties — HOLD THE LINE."""
        import effects as fx
        return fx.traits(card, 'attack').mirrors_color

    def _wins_ties_on_defence(self, card):
        import effects as fx
        return fx.traits(card, 'defense').wins_ties

    # ---- attacking ------------------------------------------------------

    def choose_attack(self, me, target):
        opts = self._prefer_hand(me, me.playable(target))
        if not opts:
            return None
        return max(opts, key=lambda c: (self._attack_value(me, c, target),
                                        c.die or 0))

    def _attack_value(self, me, card, target):
        import effects as fx
        value = self._expected(me, card)

        # A card that always ties and carries no Effect does nothing at all
        # as an attack. Hold it for the block it is actually good at.
        if self._mirrors(card):
            text = (card.effect or '').strip().lower()
            if text in ('', 'none', 'none.'):
                return -1.0

        ops = self._ops(card, 'effect')

        # A stance is worth setting if one is not already up, and worth
        # very little if the same one is. This returns rather than falling
        # through, which exempts the stance card from the colour-repeat
        # penalty below — deliberately: replaying KILLSWITCH replaces the
        # choice rather than ending it (`campaign/chris.md`), so green into
        # green is not a repeat that costs him anything.
        for op in ops:
            if isinstance(op, fx.Stance):
                return (value + self._SETUP_BONUS if op.key not in me.stances
                        else value + self._STANCE_REPLAY)

        # A totem that buffs the party is worth more than its own damage,
        # and worth nothing extra once one is standing.
        if any(isinstance(op, fx.Summon) for op in ops):
            import engine
            already = any(c.is_object and c.summoner is me
                          for c in engine.table())
            value += 0.0 if already else self._SETUP_BONUS

        # A held tie-win is worth banking, once.
        if any(isinstance(op, fx.WinsNextTie) for op in ops) \
                and not me.wins_next_tie:
            value += self._BANK_TIE_WIN

        # An Effect gated on "the card you played last turn was a different
        # colour" only pays when it is true, so only count it then.
        for op in ops:
            if isinstance(op, fx.Gated) and op.label == 'the colour changed':
                if me.last_color and me.last_color != card.color:
                    value += self._EFFECT_VALUE
                    for inner in op.ops:
                        if isinstance(inner, fx.DamageBonus):
                            value += inner.amount
                break
        else:
            if ops:
                value += self._EFFECT_VALUE

        # The load is the card, so score GRIND SHOT with what is in it.
        if any(isinstance(op, fx.AsLoadedRound) for op in ops):
            value += self._load_value(me)

        # Repeating a colour ends a stance that says it does.
        if me.last_attack_color == card.color:
            for key, held in me.stances.items():
                if held.get('ends_on_repeat'):
                    value += self._REPEAT_PENALTY
                    break
        return value

    def _load_value(self, me):
        import effects as fx
        if not me.load:
            return 0.0
        row = fx._rounds().get(me.load.lower())
        if not row or not row[0]:
            return 0.0
        ops = fx.compile_half(row[0]) or []
        return sum(op.amount if isinstance(op, fx.DamageBonus)
                   else self._EFFECT_VALUE for op in ops)

    # ---- defending ------------------------------------------------------

    def choose_defense(self, me, attacker):
        opts = self._prefer_hand(me, me.playable(attacker))
        if not opts:
            return None
        return max(opts, key=lambda c: (self._defence_value(me, c, attacker),
                                        c.die or 0))

    def _defence_value(self, me, card, attacker):
        """What a block is actually worth: the odds of winning the reveal.

        Winning means no damage *and* the Defense Effect. A tie means no
        damage and both effects. Losing means taking the hit. Damage on the
        card itself never happens on defence at all, so it is not counted.
        """
        from cards import BEATS
        beat, tie = self._odds(card, attacker)
        value = beat * 3.0 + tie * 1.5
        if self._ops(card, 'defense_effect'):
            value += self._EFFECT_VALUE * (beat + tie)
        return value

    def _odds(self, card, attacker):
        """(P(this colour beats theirs), P(it ties)), from what this
        attacker has been *seen* to play.

        A mirroring card ties with certainty, and one that also wins ties on
        defence is therefore a guaranteed block.

        Everything else is inference, because nothing else is available.
        Hands, decks and stat lines are hidden (`Knowledge`), so the only
        evidence about what colour is coming is the colours that have
        already come. Early in a fight the smoothing makes this very close
        to a shrug, and it should be: an agent that has seen two cards does
        not know anything yet. It sharpens as the discard fills.

        **Two earlier versions of this were wrong, and the second was wrong
        in a way worth remembering.**

        It first counted `attacker.hand + attacker.deck` — hidden zones, and
        on top of that the one set of cards guaranteed not to hold the
        attack being answered, because `play.py` pulls the attack card out
        of hand before it asks the defender to block. Measured over 1950
        defences the prior was not noisy but inverted: a colour holding none
        of that pool was the colour played 62% of the time, one holding 70%
        of it was played 0% of the time, and where the model predicted no
        damage with certainty, damage got through 65% of the time.

        It was then replaced by the attacker's stat line, which is exact —
        deck size is total stats and each colour's count equals its matching
        stat (`rules/cards.md`, Enemy decks) — and still not allowed, for
        the same reason the hand is not. A stat block is a sheet the
        defender was never shown. The legitimate version of that same
        inference is this one: watch the cards, and the stat line is what
        you converge on.
        """
        if self._mirrors(card):
            return (1.0, 0.0) if self._wins_ties_on_defence(card) else (0.0, 1.0)
        return self.known.color_odds(attacker, card.color)

    # ---- the free action ------------------------------------------------

    def choose_free_action(self, me, foes, allies):
        """One per turn (`rules/combat.md`, Free Actions), so this is a real
        choice rather than a checklist: reload, drink, or throw."""
        import engine
        hurt = me.hp <= me.max_hp * 0.5
        if me.drinks and hurt:
            return ('drink', me.drinks[0])
        if me.load is None and me.rounds:
            return ('reload', self._best_round(me))
        if me.oranges > 0:
            live = [f for f in foes if f.alive() and not f.is_object]
            if len(live) >= 2:
                where = max((engine.FRONT, engine.BACK),
                            key=lambda p: sum(1 for f in live if f.position == p))
                if sum(1 for f in live if f.position == where) >= 2:
                    return ('orange', where)
        if me.load is None and me.rounds:
            return ('reload', self._best_round(me))
        return None

    def _best_round(self, me):
        import effects as fx
        rows = fx._rounds()

        def worth(name):
            row = rows.get(name.lower())
            if not row or not row[0]:
                return 0.0
            ops = fx.compile_half(row[0]) or []
            return sum(op.amount if isinstance(op, fx.DamageBonus)
                       else self._EFFECT_VALUE for op in ops)
        return max(me.rounds, key=worth)

    # ---- choices a card Effect asks for ---------------------------------

    def choose_option(self, me, options, prompt='Choose'):
        """Prefer a mode that is actually doing something. Armour is worth
        more when the fight is going badly, damage when it is not."""
        low = me.hp <= me.max_hp * 0.4
        for opt in options:
            text = opt.lower()
            if low and 'armour' in text:
                return opt
            if not low and 'damage' in text:
                return opt
        return options[0]
