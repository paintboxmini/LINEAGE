#!/usr/bin/env python3
"""Cards written down twice, saying two different things.

A signature card is drafted in `campaign/` — where the reasoning for it
lives — and then lands in `cards/`, which is what the parsers read
(`combat-simulations/cards.py`, `printing/generate-cards.py`). Both copies
are worth having: one is the argument, the other is the card. What is not
worth having is the two of them quietly disagreeing.

`check-references.py` cannot see this. It loads `cards/` only, so a card
named once in each directory is not a duplicate to it, and nothing else in
the repo reads a fenced card block in a campaign file at all. This is the
`agent-tools/README.md` gap, for the one class of it that is mechanical:
same card name, two files, compare the fields.

    python3 agent-tools/check-card-drift.py

Exits 1 on a finding. A card that exists in only one place is not a
finding — a draft that has not landed yet is the normal state.
"""

import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'combat-simulations'))

import cards as C  # noqa: E402

# What a difference actually changes at the table. Flavour and the card's
# quote are deliberately not here: a campaign file may carry a working
# quote that the printed card improves on, and that is not drift.
FIELDS = ('color', 'stat', 'attack', 'effect', 'defense_effect',
          'range', 'special_rule')

FENCE = re.compile(r'```\n(.*?)\n```', re.S)
FIELD = re.compile(r'^(Attack|Effect|Defense Effect|Range|Special Rule)\s*:\s*(.*)$')
COLOR = re.compile(r'^(BLUE|RED|GREEN)\s*[—\-]+\s*(\w+)\s*$')


def norm(v):
    """Whitespace and emphasis are layout, not content — a campaign file
    wraps its card blocks by hand and bolds the clause it is arguing about;
    `cards/` does neither."""
    if v is None:
        return None
    v = re.sub(r'[*_`]', '', str(v))
    return ' '.join(v.split()).rstrip('.').lower()


def from_fence(text, source):
    """Card blocks as a campaign file writes them: a fenced block whose
    first line is the card's name in caps."""
    out = []
    for block in FENCE.findall(text):
        lines = [l.rstrip() for l in block.split('\n') if l.strip()]
        if not lines:
            continue
        name = lines[0].strip()
        if not re.fullmatch(r"[A-Z][A-Z0-9 '\-]{2,}", name):
            continue
        card = {'name': name, 'source': source}
        body = None
        for line in lines[1:]:
            m = COLOR.match(line.strip())
            if m:
                card['color'], card['stat'] = m.group(1), m.group(2)
                body = None
                continue
            m = FIELD.match(line.strip())
            if m:
                key = m.group(1).lower().replace(' ', '_')
                card[key] = m.group(2)
                body = key
                continue
            # A wrapped continuation of the field above it.
            if body and not line.strip().startswith('"'):
                card[body] = card.get(body, '') + ' ' + line.strip()
        if 'attack' in card:
            out.append(card)
    return out


def drafts():
    found = []
    for root, _, files in os.walk(os.path.join(REPO, 'campaign')):
        for f in sorted(files):
            if not f.endswith('.md'):
                continue
            path = os.path.join(root, f)
            rel = os.path.relpath(path, REPO)
            with open(path, encoding='utf-8', errors='ignore') as fh:
                found.extend(from_fence(fh.read(), rel))
    return found


def main():
    landed = {}
    for c in C.load():
        landed.setdefault(c.name.upper(), c)

    findings = []
    checked = 0
    for draft in drafts():
        card = landed.get(draft['name'].upper())
        if card is None:
            continue
        checked += 1
        for field in FIELDS:
            mine = norm(draft.get(field))
            theirs = norm(getattr(card, field, None))
            if mine is None:
                continue
            if mine != theirs:
                findings.append((draft['name'], field, draft['source'],
                                 draft.get(field), card.source,
                                 getattr(card, field, None)))

    if findings:
        print(f'\nCARDS THAT DISAGREE WITH THEMSELVES ({len(findings)}):')
        for name, field, src, mine, dst, theirs in findings:
            print(f'\n  {name} — {field}')
            print(f'    {src}: {mine}')
            print(f'    cards/{dst}: {theirs}')
        print()
        raise SystemExit(1)

    print(f'Clean — {checked} drafted cards match the copy in cards/.')


if __name__ == '__main__':
    main()
