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

from engine import can_attack

_AVG = {2: 1.5, 4: 2.5, 6: 3.5, 8: 4.5, None: 5.0}
_BEATS = {'R': 'G', 'B': 'R', 'G': 'B'}          # color -> color it beats
_BEATEN_BY = {v: k for k, v in _BEATS.items()}    # color -> color that beats it


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
    return getattr(me, card.stat) + _AVG[card.base_die]


def playable(hand):
    """Cards that can actually be played — status cards (Wound) cannot."""
    return [c for c in hand if not c.is_status]


def legal_attacks(engine, me, foe):
    if me.must_target_frontline and foe.position != 'frontline':
        return []  # Partition: no legal frontline target
    return [c for c in me.hand if not c.is_status and can_attack(me, foe, c)]


class RandomPolicy:
    name = "random"

    def choose_action(self, engine, me, foe):
        atks = legal_attacks(engine, me, foe)
        if atks:
            return ('attack', engine.rng.choice(atks))
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


class GreedyPolicy:
    """Maximize damage; defend only when it can win the reveal."""
    name = "greedy"

    def choose_action(self, engine, me, foe):
        atks = legal_attacks(engine, me, foe)
        if atks:
            return ('attack', max(atks, key=lambda c: est_damage(me, c)))
        # no legal attack — a move may open ranged/melee lines
        if me.hand:
            return ('move',)
        return None

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
        # ban the color the foe reveals most often
        if foe.attack_history:
            return foe.attack_history.most_common(1)[0][0]
        return foe.last_color or 'B'


class ReaderPolicy:
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
            if me.hand:
                return ('move',)
            return None
        pred = self._predict(foe)
        if pred is not None:
            # the foe (if also a reader) tends to defend with the color that beats
            # OUR most common attack. Break damage ties toward the color that would
            # beat that expected defense.
            expected_def = _BEATEN_BY[me.attack_history.most_common(1)[0][0]] \
                if me.attack_history else None
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


class TacticianPolicy:
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

    def _value(self, me, foe, card):
        v = est_damage(me, card)
        if card.name == "AXIOM":
            v += 2 + 3 * self._foe_skew(foe)         # ban bites a predictable foe
        elif card.name == "SPARK OF VIOLENCE" and foe.hp <= 4:
            v += 4                                    # unpreventable finisher
        return v

    def choose_action(self, engine, me, foe):
        atks = legal_attacks(engine, me, foe)
        if not atks:
            return ('move',) if me.hand else None
        return ('attack', max(atks, key=lambda c: self._value(me, foe, c)))

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
        return foe.last_color or (foe.attack_history.most_common(1)[0][0]
                                  if foe.attack_history else 'B')


POLICIES = {p.name: p for p in
            [RandomPolicy(), GreedyPolicy(), ReaderPolicy(), TacticianPolicy()]}


def make_policy(name):
    """Fresh instance (stateful policies must never be shared)."""
    return {'random': RandomPolicy, 'greedy': GreedyPolicy,
            'reader': ReaderPolicy, 'tactician': TacticianPolicy}[name]()
