"""Card loading for the combat simulator.

Reads `cards/*.md` directly rather than keeping a second copy of the card
list — the markdown is the source of truth, the same way `printing/`
treats it. No dependencies, matching the rest of the repo's tooling.

What this module parses is the structured part of a card: name, color,
stat, attack die, and range. Effect and Defense Effect are carried as text.
Reading that text is `effects.py`, which compiles the regular part of it
into operations the engine runs and leaves the rest to be read out at the
table.
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
                 'defense_effect', 'special_rule', 'range', 'flavor', 'source',
                 'applies_when')

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

    def is_playable(self):
        """Status cards (Wound, Exhaust) have no Attack line and can never
        be played — taking up a slot is the whole mechanic. Every written
        card has one, so the absence is what marks a status card."""
        return self.attack is not None

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
                               ('Applies When:', 'applies_when'),
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


PASSIVE_FILE = os.path.join(REPO, 'campaign', 'passives.md')


def load_passives():
    """The written Passives, keyed by name.

    `campaign/passives.md` is not under `cards/` and must not be — it is
    not a deck, and the two parsers that glob that directory would read it
    as one (`CLAUDE.md`, Conventions). It is read here by name instead, the
    same way `core_pool` names its four files.

    A Passive is card-shaped but is not a card in a deck: printed colour,
    Range, die, and an **Applies When** in place of the Effect
    (`rules/character-creation.md`, Passives and Traits). It sits face up
    in its own zone, is never drawn and never discarded.
    """
    return {c.name: c for c in parse_file(PASSIVE_FILE)}


KEVIN_FILE = os.path.join(REPO, 'campaign', 'kevin.md')


def _md_table(text, first_header):
    """Rows of the first markdown table whose header starts with a column
    named `first_header`, as lists of stripped cells."""
    rows, inside = [], False
    for line in text.split('\n'):
        line = line.strip()
        if not line.startswith('|'):
            if inside:
                break
            continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        first = re.sub(r'[*_`]', '', cells[0]).strip().lower()
        if not inside:
            if first == first_header.lower():
                inside = True
            continue
        if set(''.join(cells)) <= set('-: '):
            continue
        rows.append([re.sub(r'\*\*', '', c).strip() for c in cells])
    return rows


def load_grinder_rounds():
    """Kevin's prepared rounds, read out of his own file.

    `campaign/kevin.md`, The Ingredients, is the source of truth for what a
    load does — the markdown is the card (`CLAUDE.md`). Read rather than
    copied so the two cannot drift: the cells are ordinary card prose and
    go through the same reader every Effect line does.

    Returns {name: (effect, defense_effect)}. A dash means no effect.
    """
    with open(KEVIN_FILE, encoding='utf-8') as f:
        rows = _md_table(f.read(), 'Load')
    out = {}
    for r in rows:
        if len(r) < 3:
            continue
        name = r[0]
        eff = None if r[1] in ('', '—', '-') else r[1]
        dfn = None if r[2] in ('', '—', '-') else r[2]
        out[name.lower()] = (eff, dfn)
    return out


def load_drinks():
    """Kevin's prepared drinks, same arrangement — `campaign/kevin.md`,
    The beverages. Returns {name: effect on the drinker}."""
    with open(KEVIN_FILE, encoding='utf-8') as f:
        rows = _md_table(f.read(), 'Drink')
    return {r[0].lower(): r[1] for r in rows if len(r) >= 2}


def core_pool():
    """The four core lists — what a creature deck fills from
    (`rules/cards.md`, Deck Building)."""
    return load('red-body', 'blue-mind', 'green-soul', 'colorless')


_STATUS_TEXT = {
    'Wound': 'Unplayable. Clogs the hand until it is removed.',
    'Exhaust': 'Unplayable. Clogs the hand until it is removed.',
}


def status_card(kind):
    """A Wound or an Exhaust as a real card (`rules/card-glossary.md`,
    Status Cards). It is Colorless with no attack, so it can never be
    played — it takes up a slot, which is the whole mechanic."""
    return Card(name=kind.upper(), color='COLORLESS', stat=None, attack=None,
                die=0, effect=None, defense_effect=None,
                special_rule=_STATUS_TEXT.get(kind), range='Both',
                flavor=None, source='status')


def by_name(cards):
    return {c.name: c for c in cards}


if __name__ == '__main__':
    all_cards = load()
    print(f'{len(all_cards)} cards across {len(set(c.source for c in all_cards))} files')
    for color in COLORS:
        print(f'  {color:<10} {sum(1 for c in all_cards if c.color == color)}')
