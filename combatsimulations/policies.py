"""
Decision policies — the "brains" that pilot a combatant.

The skill of Tales Untold lives in two choices: whether/what to defend, and
which color to reveal under simultaneous reveal. Swapping policies is how the
sim asks its real questions — does reading the opponent actually beat random?
does going first matter? how much dead weight does each deck carry?

A policy implements:
    choose_action(engine, me, foe)  -> ('attack', card) | ('move',) | None
    choose_defense(engine, me, foe) -> card | None      # BLIND — no sight of the
                                                         # incoming card (simultaneous
                                                         # reveal). Predict from
                                                         # foe.attack_history.
    name_axiom_color(engine, me, foe) -> 'R' | 'B' | 'G'
"""

from collections import Counter

from engine import can_attack, _effective_color

_AVG = {2: 1.5, 4: 2.5, 6: 3.5, 8: 4.5, 10: 5.5, None: 5.0}
_BEATS = {'R': 'G', 'B': 'R', 'G': 'B'}          # color -> color it beats
_BEATEN_BY = {v: k for k, v in _BEATS.items()}    # color -> color that beats it


def _most_common_real_color(history):
    """Like `history.most_common(1)[0][0]`, but skips a colorless (`None`)
    entry if it happens to be on top — a colorless reveal is now a real,
    legal thing that can land in attack_history (Drew's colorless-vs-real
    RPS rule), and `_BEATEN_BY[None]` has no answer: there's no color that
    specifically "beats colorless" to predict or ban. Returns None only if
    every recorded reveal was colorless."""
    for color, _ in history.most_common():
        if color is not None:
            return color
    return None


def est_damage(me, card):
    """Rough expected damage of playing `card` as an attack. Ally/utility = 0."""
    if card.name in ("AXIOM", "DEFLECT", "REALIGNMENT", "CLIMB",
                     "ANTICIPATE", "SPIRAL CURRENT", "RENEWAL", "FORGET"):
        base = getattr(me, card.stat) + _AVG[card.base_die]
        return base  # still a real attack, just with a utility rider
    if card.name == "TWIN STRIKE":
        return 2 * (me.soul + 1.5)
    if card.name == "GAMBLER'S RUIN":
        return me.body + 2.5 + 2.0  # explode expectation, rough
    if card.name == "BURN BRIGHT":
        return me.body + 3.5 + 2
    if card.name == "BECOMING":
        return 0   # colorless, pure utility — deals no damage of its own, ever
    if card.name in ("AFTERIMAGE", "FOLLOW-UP"):
        # Both colorless — stat isn't known here (mirrors whoever went
        # immediately before, or becomes a full copy of an ally's most
        # recent reveal), so there's no single `card.stat` to read. Rough
        # estimate either way: average of the caster's own three stats,
        # since the real answer depends on engine state this function
        # doesn't have. FOLLOW-UP is often worth less than this in practice
        # (a dead card whenever no ally has revealed yet), but a policy
        # deciding whether to play it has no cheaper way to guess that here.
        return (me.body + me.mind + me.soul) / 3 + _AVG[4]
    return getattr(me, card.stat) + _AVG[card.base_die]


def playable(hand):
    """Cards that can actually be played — status cards (Injury) cannot."""
    return [c for c in hand if not c.is_status]


class ScryMixin:
    """A composable sub-brain: every action-brain mixes this in and shares one
    Scry strategy. The engine hands scry_plan the cards seen on top of a deck and
    it returns (to_top, to_bottom) — to_top[-1] is drawn next.

    Two modes, per Drew's logic:
      • Your own (or an ally's) deck — set up good draws: surface your best cards,
        bury Injuries so you don't draw dead.
      • An enemy's deck — sabotage draws: bury their biggest threats AND the color
        that would beat your usual attack (so the card that normally answers you
        is delayed), and leave their junk (and any Injuries!) on top to draw.

    Override scry_plan on a specific brain for card-specific cleverness (e.g.
    keep a threat on top when you already hold the answer). This default is the
    "make my attacks safer" line.
    """
    def scry_plan(self, engine, actor, owner, seen):
        own = (owner is actor) or (owner in engine.allies(actor))
        if own:
            real = sorted([c for c in seen if not c.is_status],
                          key=lambda c: est_damage(actor, c))   # best ends last -> drawn first
            injuries = [c for c in seen if c.is_status]
            # Bottom Injuries, don't bin them: in a single combat, binning to discard
            # just recycles them faster on the next reshuffle. (Scry CAN bin — the
            # engine supports it — but that's a rest/Press-the-Injury play, which
            # lives outside a no-rest duel. See memory.md.)
            return real, injuries
        # enemy deck
        my = actor.attack_history.most_common(1)[0][0] if actor.attack_history else None
        counter = _BEATEN_BY[my] if my else None    # color that beats my attacks
        def threat(c):
            if c.is_status:
                return -10                          # an Injury of theirs: leave it on top!
            return est_damage(owner, c) + (5 if (counter and c.color == counter) else 0)
        ranked = sorted(seen, key=threat)           # weakest first
        half = max(1, len(ranked) // 2)
        junk = ranked[:half][::-1]                  # low threat, weakest last -> drawn next
        bury = ranked[half:]                        # threats + counter color -> bottom
        return junk, bury


def legal_attacks(engine, me, foe):
    if me.must_target_frontline and foe.position != 'frontline':
        return []  # Partition: no legal frontline target
    return [c for c in me.hand if not c.is_status and can_attack(me, foe, c)]


def idle_recovery(engine, me, foe):
    """What to do with a forced-idle turn (no legal attack): clear an Injury or
    Exhaust if one's stuck in hand (Injury checked first — same conservative
    "never trade a real attacking turn for it" policy either way). Staggered no
    longer routes through here — the engine skips that turn's action itself,
    before a policy ever gets asked to choose one."""
    if legal_attacks(engine, me, foe):
        return None
    if any(c.is_status and c.name == 'INJURY' for c in me.hand):
        return ('destroy_injury',)
    if any(c.is_status and c.name == 'EXHAUST' for c in me.hand):
        return ('destroy_exhaust',)
    return None


class RandomPolicy(ScryMixin):
    name = "random"

    def choose_action(self, engine, me, foe):
        atks = legal_attacks(engine, me, foe)
        if atks:
            return ('attack', engine.rng.choice(atks))
        w = idle_recovery(engine, me, foe)
        if w:
            return w
        if me.hand and engine.rng.random() < 0.5:
            return ('move',)
        return None

    def choose_defense(self, engine, me, foe):
        hand = playable(me.hand)
        if not hand:
            return None
        if engine.rng.random() < 0.7:
            return engine.rng.choice(hand)
        return None

    def name_axiom_color(self, engine, me, foe):
        return engine.rng.choice(['R', 'B', 'G'])


class GreedyPolicy(ScryMixin):
    """Maximize damage; defend only when it can win the reveal."""
    name = "greedy"

    def choose_action(self, engine, me, foe):
        atks = legal_attacks(engine, me, foe)
        if atks:
            return ('attack', max(atks, key=lambda c: est_damage(me, c)))
        # no legal attack — clear an Injury if idle, else a move may open lines
        return idle_recovery(engine, me, foe) or (('move',) if me.hand else None)

    def choose_defense(self, engine, me, foe):
        # blind: predict the foe repeats their last attack color; hold the color
        # that would beat that prediction.
        pred = foe.last_color
        if pred is None:
            return None  # nothing to go on — decline, keep cards
        winners = [c for c in me.hand if c.color == _BEATEN_BY[pred]]
        if winners:
            return min(winners, key=lambda c: est_damage(me, c))  # save big cards
        return None

    def name_axiom_color(self, engine, me, foe):
        # ban the color the foe reveals most often — "colorless" isn't a
        # real ban target (Axiom names R/B/G), so skip a colorless top entry
        # rather than naming a color that can never actually match anything.
        return _most_common_real_color(foe.attack_history) or foe.last_color or 'B'


class ReaderPolicy(ScryMixin):
    """Punish the opponent's most frequent attack color (from public history)."""
    name = "reader"

    @staticmethod
    def _predict(foe):
        if foe.attack_history:
            return foe.attack_history.most_common(1)[0][0]
        return foe.last_color

    def choose_action(self, engine, me, foe):
        atks = legal_attacks(engine, me, foe)
        if not atks:
            return idle_recovery(engine, me, foe) or (('move',) if me.hand else None)
        pred = self._predict(foe)
        if pred is not None:
            # the foe (if also a reader) tends to defend with the color that beats
            # OUR most common attack. Break damage ties toward the color that would
            # beat that expected defense.
            my_top = _most_common_real_color(me.attack_history) if me.attack_history else None
            expected_def = _BEATEN_BY[my_top] if my_top else None
            def key(c):
                anti = 1 if (expected_def and c.color == _BEATEN_BY[expected_def]) else 0
                return (est_damage(me, c), anti)
            return ('attack', max(atks, key=key))
        return ('attack', max(atks, key=lambda c: est_damage(me, c)))

    def choose_defense(self, engine, me, foe):
        # blind: predict the foe's most frequent attack color and hold its counter
        pred = self._predict(foe)
        if pred is None:
            return None
        winners = [c for c in me.hand if c.color == _BEATEN_BY[pred]]
        if winners:
            return min(winners, key=lambda c: est_damage(me, c))
        return None

    def name_axiom_color(self, engine, me, foe):
        return self._predict(foe) or 'B'


class TacticianPolicy(ScryMixin):
    """Built on GREEDY, not reader — the tournament's verdict.

    The sim overturned the intuition that tracking an opponent's lifetime color
    frequency (reader) is smart. It isn't: recency wins. Greedy — which predicts
    the foe's NEXT reveal from their LAST one and otherwise maximizes damage —
    beats reader decisively (up to 90/10 in the Mire mirror). So the tactician
    inherits greedy's recency-read and aggressive offense, and adds only the one
    upgrade that helped without hurting any deck: valuing Axiom's color ban (and
    an unpreventable Spark to finish a low foe).

    Anti-read color flattening was tried and cut — it only helps a deck whose
    off-colors are as strong as its main color, and loses for everyone else.
    """
    name = "tactician"

    @staticmethod
    def _foe_skew(foe):
        h = foe.attack_history
        if not h:
            return 0.0
        return h.most_common(1)[0][1] / sum(h.values())

    @staticmethod
    def _color_exhausted(engine, foe, color):
        """True if every copy of `color` in the foe's decklist is visible in their
        discard — so none is live in their deck or hand. This is the SITUATIONAL
        use of deck-tracking Drew flagged: not a predictor, a safety check. It's
        cheap and only ever helps, because it only fires on certainty."""
        full = sum(1 for n in foe.decklist
                   if not engine.cards[n].is_status and engine.cards[n].color == color)
        if full == 0:
            return False
        seen = sum(1 for c in foe.discard if not c.is_status and c.color == color)
        return seen >= full

    def _value(self, engine, me, foe, card):
        v = est_damage(me, card)
        if card.name == "AXIOM":
            v += 2 + 3 * self._foe_skew(foe)         # ban bites a predictable foe
        elif card.name == "SPARK OF VIOLENCE" and foe.hp <= 4:
            v += 4                                    # unpreventable finisher
        # Risk-free read: if the color that beats this attack (as a defender) is
        # exhausted from the foe's live cards, this attack cannot lose the reveal.
        # AFTERIMAGE mirrors whoever went immediately before it — colorless on its
        # face, but that mirrored color is already fixed engine-side by the time
        # this decision is made (the prior turn already resolved and revealed), so
        # a real read just looks it up via _effective_color instead of the None
        # printed on the card — same check every other card gets, one extra step.
        atk_color = _effective_color(engine, card)
        if atk_color is not None and self._color_exhausted(engine, foe, _BEATEN_BY[atk_color]):
            v += 2
        return v

    def choose_action(self, engine, me, foe):
        atks = legal_attacks(engine, me, foe)
        if not atks:
            return idle_recovery(engine, me, foe) or (('move',) if me.hand else None)
        return ('attack', max(atks, key=lambda c: self._value(engine, me, foe, c)))

    def choose_defense(self, engine, me, foe):
        # recency read: expect the foe to repeat their last attack color
        pred = foe.last_color
        if pred is None:
            return None
        winners = [c for c in me.hand if not c.is_status and c.color == _BEATEN_BY[pred]]
        if winners:
            return min(winners, key=lambda c: est_damage(me, c))
        return None

    def name_axiom_color(self, engine, me, foe):
        return foe.last_color or _most_common_real_color(foe.attack_history) or 'B'


class PunisherPolicy(TacticianPolicy):
    """The anti-stat-max brain. Everything the tactician does, plus the piece the
    tactician lacks: CARD CONSERVATION against a color-reliant opponent.

    When the foe leans hard on one attack color, the counter to that color is
    precious — it wins the reveal every time the foe attacks. The tactician
    happily spends its counters as attacks; the punisher hoards them. If the foe
    is mono-reliant and I'm down to my last counter-color card, I won't fire it as
    an attack — I hold it to block. That's the maximal legal punishment for
    over-relying on one stat/color.
    """
    name = "punisher"
    RELIANCE = 0.55  # foe counts as "color-reliant" above this share of one color

    def _dominant(self, foe):
        h = foe.attack_history
        if not h:
            return None
        color, n = h.most_common(1)[0]
        return color if n / sum(h.values()) >= self.RELIANCE else None

    def choose_action(self, engine, me, foe):
        atks = legal_attacks(engine, me, foe)
        if not atks:
            return idle_recovery(engine, me, foe) or (('move',) if me.hand else None)
        dom = self._dominant(foe)
        if dom:
            counter = _BEATEN_BY[dom]                      # color I defend dom with
            held = [c for c in me.hand if not c.is_status and c.color == counter]
            non_counter = [c for c in atks if c.color != counter]
            # if firing a counter would leave me unable to block the dominant
            # color next turn, attack with something else instead
            if non_counter and len(held) <= 1:
                atks = non_counter
        return ('attack', max(atks, key=lambda c: self._value(engine, me, foe, c)))


# Note: a standalone "tracker" brain that PREDICTED from deck state (decklist
# minus discard) was tried and removed. It lost ~85% to the tactician — in tiny
# reshuffling decks, "what's left in the deck" barely predicts the next draw, and
# a heavily-played color depletes fastest, fooling availability-based prediction
# right before a reshuffle. Deck-tracking's real value is narrow and certain, not
# predictive: the exhaustion safety-check now lives inside the tactician
# (_color_exhausted). Situational, as Drew put it — never the whole strategy.

POLICIES = {p.name: p for p in
            [RandomPolicy(), GreedyPolicy(), ReaderPolicy(),
             TacticianPolicy(), PunisherPolicy()]}


def make_policy(name):
    """Fresh instance (stateful policies must never be shared)."""
    return {'random': RandomPolicy, 'greedy': GreedyPolicy,
            'reader': ReaderPolicy, 'tactician': TacticianPolicy,
            'punisher': PunisherPolicy}[name]()
