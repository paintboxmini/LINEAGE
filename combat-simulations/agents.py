"""Who decides what a combatant does.

Three kinds: a human at the keyboard, a scripted opponent, and a random
one. All three answer the same three questions, so any mix can share a
table — a human party against scripted creatures is the normal case.
"""

import random

from engine import FRONT, BACK


class Agent:
    def choose_action(self, me, foes, allies):
        """Return ('attack', target) | ('move',) | ('cover',) | ('pass',)."""
        raise NotImplementedError

    def choose_attack(self, me, target):
        """Return a Card from me.hand that is range-legal, or None."""
        raise NotImplementedError

    def choose_defense(self, me, attacker):
        """Return a range-legal Card from me.hand, or None to take the hit."""
        raise NotImplementedError


class RandomAgent(Agent):
    """Plays legally and at random. Useful as a baseline opponent and for
    shaking out illegal states."""

    def __init__(self, rng=None):
        self.rng = rng or random

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

    def __init__(self, rng=None):
        self.rng = rng or random

    def choose_action(self, me, foes, allies):
        if me.down:
            return ('pass',)
        live = [f for f in foes if f.alive()]
        if not live:
            return ('pass',)
        reachable = [f for f in live if me.playable(f)]
        if reachable:
            return ('attack', min(reachable, key=lambda f: f.hp))
        if not me.rooted:
            return ('move',)
        return ('pass',)

    def choose_attack(self, me, target):
        opts = me.playable(target)
        if not opts:
            return None
        # Biggest expected damage, ties broken by the bigger die.
        return max(opts, key=lambda c: (me.stat(c.stat) + c.die / 2, c.die))

    def choose_defense(self, me, attacker):
        opts = me.playable(attacker)
        if not opts:
            return None
        return max(opts, key=lambda c: (me.stat(c.stat) + c.die / 2, c.die))


class HumanAgent(Agent):
    """Prompts at the terminal. Always shows the legal options and nothing
    else, so an illegal choice is not reachable from the menu."""

    def __init__(self, ask=input, show=print):
        self.ask, self.show = ask, show

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
                opts.append((f'Attack {f.name} ({f.hp}/{f.max_hp} HP, {f.position})',
                             ('attack', f)))
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
