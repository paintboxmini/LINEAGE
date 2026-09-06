"""The initiative wheel and Initiative Shift.

Model: a fixed ring of slots, one per combatant, indexed clockwise. Index 0
is the marker's slot. A shift moves a token between slots and the tokens it
travels through slide one slot toward the gap it left — which is why this is
a ring of slots rather than a list you remove from and insert into. The two
give different answers whenever a shift wraps past the marker, and the
wraparound cases are exactly the ones the rules care about.

Verified against every worked case in `rules/initiative-shift-examples.md`;
see test_wheel.py, which runs them as assertions.

Sign convention (`rules/card-glossary.md`, Initiative Shift X): a positive
shift moves counterclockwise, toward the marker, and makes its target act
sooner. A negative shift moves clockwise and makes it act later.
"""

SKIP = 'skip'
BONUS = 'bonus'


class Wheel:
    def __init__(self, tokens):
        """tokens: in initiative order, first to act first. That combatant
        starts on the marker's slot."""
        self.slots = list(tokens)
        self.chips = {}          # token -> SKIP | BONUS
        self.pending_bonus = []  # tokens owed an immediate extra turn

    # ---- geometry -------------------------------------------------------

    def __len__(self):
        return len(self.slots)

    def index(self, token):
        return self.slots.index(token)

    def order(self):
        """Tokens clockwise from the marker's slot."""
        return list(self.slots)

    def _move(self, frm, to, clockwise):
        """Move the token at slot `frm` to slot `to`, sliding everything it
        travels through one slot back toward the gap."""
        n = len(self.slots)
        token = self.slots[frm]
        step = 1 if clockwise else -1
        i = frm
        while i != to:
            nxt = (i + step) % n
            self.slots[i] = self.slots[nxt]   # passed token slides back
            i = nxt
        self.slots[to] = token

    # ---- Initiative Shift ----------------------------------------------

    def shift(self, token, amount):
        """Apply Initiative Shift `amount` to `token`. Returns a short
        description of what happened, for the log.

        Callers should sum simultaneous shifts on the same token first —
        "multiple shifts applied to the same token at once sum into one net
        shift before it applies."
        """
        n = len(self.slots)

        # "With exactly 3 combatants on the wheel, reduce X's magnitude by 1
        # (toward zero) before applying the shift."
        if n == 3 and amount:
            amount = amount - 1 if amount > 0 else amount + 1
            if amount == 0:
                return f'{token} — shift reduced to 0 (3 on the wheel)'

        if amount == 0:
            return f'{token} — no shift'

        # "Reshifting a token that already carries a pending skip or bonus
        # chip removes the pending chip."
        had = self.chips.pop(token, None)
        if had == BONUS and token in self.pending_bonus:
            self.pending_bonus.remove(token)

        s = self.index(token)
        note = ''

        if amount > 0:
            raw = s - amount
            if raw <= 0:
                # Lands on the marker's own slot, or past it: there is no
                # slot before "now", so the target takes an immediate extra
                # turn instead, and whoever it displaced off the marker's
                # slot is skipped in compensation.
                displaced = self.slots[0]
                self._move(s, 0, clockwise=False)
                self.chips[token] = BONUS
                self.pending_bonus.append(token)
                if displaced is not token:
                    self.chips[displaced] = SKIP
                    note = f'; {displaced} skipped in compensation'
                return f'{token} +{amount} → bonus turn{note}'
            self._move(s, raw, clockwise=False)
            return f'{token} +{amount} → slot {raw}'

        k = -amount
        raw = s + k
        if raw >= n:
            # Wrapped at or past the marker's slot, which would land it
            # sooner than it started. The shift and slide still happen in
            # full; a skip chip preserves "negative never sooner". No
            # compensation skip here: nothing earned a bonus turn.
            to = raw % n
            self._move(s, to, clockwise=True)
            self.chips[token] = SKIP
            return f'{token} {amount} → slot {to}, skipped'
        self._move(s, raw, clockwise=True)
        return f'{token} {amount} → slot {raw}'

    # ---- turn order -----------------------------------------------------

    def take_bonus(self):
        """Pop a token owed an immediate extra turn, if any."""
        while self.pending_bonus:
            t = self.pending_bonus.pop(0)
            if self.chips.get(t) == BONUS:
                del self.chips[t]
                return t
        return None

    def advance(self, actor):
        """Move the marker past `actor` and re-anchor so the marker's slot is
        index 0 again. Returns the token whose turn it now is, or None if it
        holds a skip chip (the chip is spent either way).

        The marker advances to the slot after wherever the acting token
        ended up — a token that slid can carry the marker with it. See the
        note in README.md on Example 3, the one worked case this does not
        reproduce turn-for-turn.
        """
        n = len(self.slots)
        nxt = (self.index(actor) + 1) % n
        self.slots = self.slots[nxt:] + self.slots[:nxt]
        up = self.slots[0]
        if self.chips.get(up) == SKIP:
            del self.chips[up]
            return None
        return up

    # ---- joining and leaving -------------------------------------------

    def add_after(self, token, after):
        """A summoned combatant enters directly after whoever summoned it."""
        self.slots.insert(self.index(after) + 1, token)

    def remove(self, token):
        """A combatant leaving the fight; the wheel closes around the slot."""
        self.slots.remove(token)
        self.chips.pop(token, None)
        if token in self.pending_bonus:
            self.pending_bonus.remove(token)

    def __repr__(self):
        marks = {SKIP: '(skip)', BONUS: '(bonus)'}
        return ', '.join(str(t) + marks.get(self.chips.get(t), '')
                         for t in self.slots)
