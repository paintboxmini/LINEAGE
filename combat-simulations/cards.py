"""Card loading for the combat simulator.

Reads `cards/*.md` directly rather than keeping a second copy of the card
list — the markdown is the source of truth, the same way `printing/`
treats it. No dependencies, matching the rest of the repo's tooling.

A card's Effect and Defense Effect are prose written for a human, and the
engine does not attempt to parse them. What it parses is the part that is
structured: name, color, stat, attack die, and range. Effects are carried
as text and surfaced to whoever is playing, who applies them. Every one of
them, without exception — engine.py logs an Effect and a Defense Effect and
resolves neither. Mechanical recognition was once meant to live in an
effects.py; there has never been one.
"""

import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARD_DIR = os.path.join(REPO, 'cards')

COLORS = ('RED', 'BLUE', 'GREEN', 'COLORLESS')

# The RPS triangle (rules/combat.md, Attack Resolution).
BEATS = {'BLUE': 'RED', 'RED': 'GREEN', 'GREEN': 'BLUE'}


class Card:
    __slots__ = ('name', 'color', 'stat', 'attack', 'die', 'effect',
                 'defense_effect', 'special_rule', 'range', 'flavor', 'source')

    def __init__(self, **kw):
        for s in self.__slots__:
            setattr(self, s, kw.get(s))

    def beats(self, other):
        """True if this card's color wins the RPS reveal against `other`.

        Colorless auto-loses to any real color and ties another colorless
        (`cards/colorless.md`).
        """
        if self.color == 'COLORLESS':
            return False
        if other.color == 'COLORLESS':
            return True
        return BEATS.get(self.color) == other.color

    def ties(self, other):
        return self.color == other.color

    def range_ok(self, mine, theirs):
        """Range legality for the two positions (rules/combat.md, Range).

        Melee needs both Frontline. Ranged needs the two not to be in melee
        range of each other — that is, not both Frontline. Both is always
        legal.
        """
        r = (self.range or 'Both').strip().lower()
        both_front = mine == 'Frontline' and theirs == 'Frontline'
        if r.startswith('melee'):
            return both_front
        if r.startswith('ranged'):
            return not both_front
        return True

    def __repr__(self):
        return f'<{self.name} {self.color}/{self.stat} {self.attack}>'


def _die_of(attack_text):
    """Largest die named in an Attack line, as an int. 'Soul + d6' -> 6.

    Cards like TWIN STRIKE read '(Soul + d4) x 2'; the multiplier is part of
    the effect text a player applies, not something the die size captures.
    """
    dice = [int(d) for d in re.findall(r'd(\d+)', attack_text or '')]
    return max(dice) if dice else 0


def parse_file(path):
    """Parse one cards/*.md file. Mirrors printing/generate-cards.py's
    definition of a card: a `---`-delimited block carrying both a name and
    a color."""
    with open(path, encoding='utf-8') as f:
        content = f.read()

    out = []
    for block in re.split(r'\n---\n', content):
        block = block.strip()
        if not block:
            continue

        # Header lines are skipped, the block is not — a card following a
        # "## Creature" heading shares that heading's block. See the same
        # note in printing/generate-cards.py.
        kw = {'source': os.path.basename(path)}
        for line in (l.strip() for l in block.split('\n')
                     if l.strip() and not l.strip().startswith('#')):
            m = re.match(r'^\*\*(.+?)\*\*$', line)
            if m and 'name' not in kw:
                kw['name'] = m.group(1)
                continue

            m = re.match(r'^(BLUE|RED|GREEN)\s*[—\-]+\s*(.+)$', line)
            if m:
                kw['color'] = m.group(1)
                kw['stat'] = re.split(r'\s*[—\-]+\s*', m.group(2))[0].strip()
                continue

            if line == 'COLORLESS':
                kw['color'] = 'COLORLESS'
                continue

            for label, key in (('Attack:', 'attack'), ('Special Rule:', 'special_rule'),
                               ('Effect:', 'effect'), ('Defense Effect:', 'defense_effect'),
                               ('Range:', 'range')):
                if line.startswith(label):
                    kw[key] = line[len(label):].strip()
                    break
            else:
                m = re.match(r'^\*"(.+)"\*$', line)
                if m:
                    kw['flavor'] = m.group(1)

        if kw.get('name') and kw.get('color'):
            kw['die'] = _die_of(kw.get('attack'))
            out.append(Card(**kw))

    return out


def load(*filenames):
    """Load named files from cards/ (with or without the .md), or every
    card in the directory when called with no arguments."""
    if filenames:
        paths = [os.path.join(CARD_DIR, f if f.endswith('.md') else f + '.md')
                 for f in filenames]
    else:
        paths = sorted(os.path.join(CARD_DIR, f) for f in os.listdir(CARD_DIR)
                       if f.endswith('.md'))

    cards = []
    for p in paths:
        if not os.path.exists(p):
            raise FileNotFoundError(p)
        cards.extend(parse_file(p))
    return cards


def core_pool():
    """The four core lists — what a creature deck fills from
    (`rules/cards.md`, Deck Building)."""
    return load('red-body', 'blue-mind', 'green-soul', 'colorless')


def by_name(cards):
    return {c.name: c for c in cards}


if __name__ == '__main__':
    all_cards = load()
    print(f'{len(all_cards)} cards across {len(set(c.source for c in all_cards))} files')
    for color in COLORS:
        print(f'  {color:<10} {sum(1 for c in all_cards if c.color == color)}')
