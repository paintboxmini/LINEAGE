#!/usr/bin/env python3
"""Generate a print-ready HTML card sheet from core card files.
Cards are 60mm x 84mm (slightly under Magic card size) to fit in sleeves.
Layout: 3x3 per Letter page, exactly 9 cards per page.

Usage:
  python3 generate-cards.py              → core cards  (card-print-core.html)
  python3 generate-cards.py briarwatch  → Briarwatch encounter set
  python3 generate-cards.py items       → player item cards
  python3 generate-cards.py <set-name>  → any named set below

Print settings: Margins = None, Background graphics = On, Scale = 100%.
"""

import re
import html as html_mod
import os
import sys

# ---------------------------------------------------------------------------
# Card sets — add new encounter sets here
# ---------------------------------------------------------------------------

SETS = {
    'core': {
        'title': 'Core Cards',
        'files': [
            '../cards/blue-mind.md',
            '../cards/red-body.md',
            '../cards/green-soul.md',
            '../cards/colorless.md',
        ],
    },
    'briarwatch': {
        'title': 'Briarwatch Encounter Set',
        'files': [
            '../cards/briarwatch-jackalope.md',
            '../cards/tollbird.md',
            '../cards/briar-scratcher.md',
            '../cards/borrower-hollow.md',
            '../cards/stonecoil-hollow.md',
            '../cards/delve-roller-hollow.md',
        ],
    },
    'items': {
        'title': 'Items',
        'type': 'items',
        'files': [
            '../items/consumables.md',
            '../items/briarwatch-items.md',
            '../items/vultures-nest-items.md',
        ],
    },
    'items-field': {
        'title': 'Hollow and Weald Items',
        'type': 'items',
        'files': [
            '../items/hollow-and-weald-items.md',
        ],
    },
    'mason': {
        'title': 'Mason Glyphs',
        'files': [
            '../cards/mason-glyphs.md',
        ],
    },
    'frost': {
        'title': "Frost's Deck",
        'files': [
            '../cards/red-body.md',
            '../cards/blue-mind.md',
            '../cards/green-soul.md',
        ],
        # `../characters/frost.md` — order matches that file's own
        # Red/Blue/Green grouping, not registration order in the core files.
        'cards': [
            'SACRIFICE STRIKE', 'BLOOD IN THE GAP', 'BURN BRIGHT', 'SPARK OF VIOLENCE',
            'AXIOM', 'DEFLECT', 'REALIGNMENT', 'CLIMB', 'FRACTURE',
            'TWIN STRIKE',
        ],
    },
    'steele': {
        'title': "Steele's Deck",
        'files': [
            '../cards/red-body.md',
            '../cards/blue-mind.md',
            '../cards/green-soul.md',
        ],
        # `../characters/steele.md`
        'cards': [
            'BLOOD TITHE', "GAMBLER'S RUIN", 'PAIN IS FUEL', 'REPEL',
            'FORGET', 'PARADOX', 'ALIGN', 'ANTICIPATE',
            'MIRROR STEP', 'RENEWAL',
        ],
    },
    'oracle': {
        'title': 'Oracle Deck',
        'files': [
            '../cards/red-body.md',
            '../cards/blue-mind.md',
            '../cards/green-soul.md',
        ],
        # `../Oracle/baseoracledeck.md` — matches `content.py`'s ORACLE_DECK
        # verbatim. Fixed composition since 2026-08-03: 21 per colour, split
        # 12/6/3 along each colour's range identity.
        'cards': [
            # Red (21) — melee 12 / both 6 / ranged 3
            # GORE swapped for INTERCEPT 2026-08-03 — see content.py.
            'ATTRITION', 'BLINDSIDE', 'CHARGE', 'ENDURE', 'GUARD', 'INTERCEPT',
            'OPEN GUARD', 'PAIN IS FUEL', 'PUSH', 'REELING', 'UNBROKEN',
            'WEATHERED', 'CLIFF SONG', 'FOOTWORK', 'GROUNDING STANCE', 'PULL',
            'RECOVER', 'SLIP THE BLADE', 'BLOOD IN THE GAP',
            'EMERGENCY REPAIRS', 'STARING CONTEST',
            # Blue (21) — ranged 12 / melee 6 / both 3
            'AXIOM', 'CALCULATE', 'DEAD END', 'FOCUS', 'FORESEEN',
            'LAST RESORT', 'MARKED', 'PROFILE', 'REFRACT', 'RETORT', 'STUDY',
            'VEIL', 'ANTICIPATE', 'DEFLECT', 'PREDICT', 'HESITATE', 'TELL',
            'SECOND GUESS', 'REALIGNMENT', 'SHARPEN', 'SIDESTEP',
            # Green (21) — both 12 / ranged 6 / melee 3
            'ACCEPTANCE', 'BRAMBLE', 'GIVE WAY', 'INSTINCT',
            'LEVEL THE FIELD', 'MIRROR STEP', 'QUICKEN', 'RENEWAL', 'SETTLE',
            'SWAY', 'UNTOUCHED', "YOU'RE NEXT", 'BALANCE', 'COMMUNION',
            'DEAD RECKONING', 'MOCKERY', 'RESONATE', 'SUPPORT', 'BIND',
            'DUST', 'OPENING',
        ],
    },
}

# ---------------------------------------------------------------------------

COLOR_HEX = {
    'BLUE':      '#2C5F9E',
    'RED':       '#9E2C2C',
    'GREEN':     '#2A7A3E',
    'COLORLESS': '#5A5A5A',
}

COLOR_BG = {
    'BLUE':      '#F0F4FA',
    'RED':       '#FAF0F0',
    'GREEN':     '#F0F7F2',
    'COLORLESS': '#F2F2F2',
}

COLOR_LABEL = {
    'BLUE':      'Mind',
    'RED':       'Body',
    'GREEN':     'Soul',
    'COLORLESS': 'Colorless',
}

ITEM_HEX = '#7A5C10'
ITEM_BG  = '#FBF8F0'

CARDS_PER_PAGE = 9


def parse_cards(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    cards = []
    blocks = re.split(r'\n---\n', content)

    for block in blocks:
        block = block.strip()
        if not block or block.startswith('#'):
            continue

        card = {}
        lines = [l.strip() for l in block.split('\n') if l.strip()]

        for line in lines:
            m = re.match(r'^\*\*(.+?)\*\*$', line)
            if m and 'name' not in card:
                card['name'] = m.group(1)
                continue

            m = re.match(r'^(BLUE|RED|GREEN)\s*[—\-]+\s*(.+)$', line)
            if m:
                card['color'] = m.group(1)
                stat_part = re.split(r'\s*[—\-]+\s*', m.group(2))[0]
                card['stat'] = stat_part.strip()
                continue

            if line == 'COLORLESS':
                card['color'] = 'COLORLESS'
                continue

            if line.startswith('Attack:'):
                card['attack'] = line[7:].strip()
            elif line.startswith('Special Rule:'):
                card['special_rule'] = line[13:].strip()
            elif line.startswith('Effect:'):
                card['effect'] = line[7:].strip()
            elif line.startswith('Defensive Bonus:'):
                card['defensive_bonus'] = line[16:].strip()
            elif line.startswith('Range:'):
                card['range'] = line[6:].strip()
            else:
                m = re.match(r'^\*"(.+)"\*$', line)
                if m:
                    card['flavor'] = m.group(1)

        if card.get('name') and card.get('color'):
            cards.append(card)

    return cards


def parse_items(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    items = []
    blocks = re.split(r'\n---\n', content)

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        item = {'_type': 'item'}
        lines = [l.strip() for l in block.split('\n') if l.strip()]

        for line in lines:
            # Skip markdown section headers
            if line.startswith('#'):
                continue

            # Name: **ITEM NAME**
            m = re.match(r'^\*\*(.+?)\*\*$', line)
            if m and 'name' not in item:
                item['name'] = m.group(1)
                continue

            # Only process further once we have a name
            if 'name' not in item:
                continue

            # Italic lines: type descriptor or source (skip source)
            m = re.match(r'^\*(.+)\*$', line)
            if m:
                inner = m.group(1)
                if inner.startswith('Source:'):
                    continue
                if 'type' not in item:
                    item['type'] = inner
                continue

            # Everything else is effect text
            item.setdefault('effect_lines', []).append(line)

        if item.get('name'):
            items.append(item)

    return items


def load_set(set_name):
    cfg = SETS[set_name]
    is_items = cfg.get('type') == 'items'
    parser = parse_items if is_items else parse_cards

    seen = set()
    by_name = {}
    all_cards = []
    for f in cfg['files']:
        for card in parser(f):
            if card['name'] not in seen:
                seen.add(card['name'])
                all_cards.append(card)
                by_name[card['name']] = card

    # Optional explicit whitelist (e.g. a specific character's deck) — filters
    # and reorders to match the list exactly, instead of every card in `files`.
    if 'cards' in cfg:
        missing = [n for n in cfg['cards'] if n not in by_name]
        if missing:
            raise SystemExit(f"generate-cards.py: card(s) not found for set "
                              f"'{set_name}': {', '.join(missing)}")
        return [by_name[n] for n in cfg['cards']]

    return all_cards


def h(text):
    return html_mod.escape(str(text))


def card_to_html(card):
    color = card.get('color', 'BLUE')
    hex_color = COLOR_HEX[color]
    bg_color = COLOR_BG[color]
    stat_label = COLOR_LABEL[color]

    rows = ''

    if card.get('attack'):
        rows += f'<tr><td class="lbl">Attack</td><td>{h(card["attack"])}</td></tr>'

    if card.get('special_rule'):
        rows += f'<tr><td class="lbl">Special</td><td>{h(card["special_rule"])}</td></tr>'

    effect = card.get('effect', 'None')
    rows += f'<tr><td class="lbl">Effect</td><td>{h(effect)}</td></tr>'

    db = card.get('defensive_bonus', 'None')
    rows += f'<tr><td class="lbl">Defense</td><td>{h(db)}</td></tr>'

    if card.get('range'):
        rows += f'<tr><td class="lbl">Range</td><td>{h(card["range"])}</td></tr>'

    flavor = ''
    if card.get('flavor'):
        flavor = f'<div class="flavor">&#8220;{h(card["flavor"])}&#8221;</div>'

    # Body text is set large by default, because most cards are short — median
    # is ~140 characters. A handful run 300+ and would overflow a fixed 84mm
    # card at that size, so those step down instead of clipping. Better a
    # slightly smaller wordy card than a truncated one.
    weight = sum(len(str(card.get(k, ''))) for k in
                 ('attack', 'special_rule', 'effect', 'defensive_bonus', 'range', 'flavor'))
    density = ' denser' if weight > 285 else (' dense' if weight > 195 else '')

    return f'''<div class="card{density}" style="background:{bg_color};border-color:{hex_color}99">
  <div class="card-top">
    <div class="card-name">{h(card["name"])}</div>
    <div class="dot" style="background:{hex_color}"></div>
  </div>
  <div class="card-sub" style="color:{hex_color}">{h(stat_label)}</div>
  <div class="divider" style="background:{hex_color}44"></div>
  <table class="tbl">{rows}</table>
  {flavor}
</div>'''


def item_to_html(item):
    type_line = ''
    if item.get('type'):
        type_line = f'<div class="card-sub" style="color:{ITEM_HEX}">{h(item["type"])}</div>'

    effect = '<br>'.join(h(l) for l in item.get('effect_lines', []))

    return f'''<div class="card" style="background:{ITEM_BG};border-color:{ITEM_HEX}99">
  <div class="card-top">
    <div class="card-name">{h(item["name"])}</div>
  </div>
  {type_line}
  <div class="divider" style="background:{ITEM_HEX}44"></div>
  <div class="item-effect">{effect}</div>
</div>'''


def render_card(card):
    if card.get('_type') == 'item':
        return item_to_html(card)
    return card_to_html(card)


def chunk(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def generate_html(all_cards, title):
    page_divs = []
    for page_cards in chunk(all_cards, CARDS_PER_PAGE):
        cards_html = '\n'.join(render_card(c) for c in page_cards)
        page_divs.append(f'<div class="page">\n{cards_html}\n</div>')

    pages_html = '\n'.join(page_divs)
    total = len(all_cards)
    total_pages = -(-total // CARDS_PER_PAGE)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Tales Untold — {h(title)} ({total} cards, {total_pages} pages)</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}

@page {{
  size: letter;
  margin: 10mm;
}}

body {{
  font-family: Georgia, "Times New Roman", serif;
  background: #bbb;
}}

.page {{
  width: 196mm;
  height: 259mm;
  display: grid;
  grid-template-columns: repeat(3, 60mm);
  grid-template-rows: repeat(3, 84mm);
  column-gap: calc((196mm - 3 * 60mm) / 2);
  row-gap: calc((259mm - 3 * 84mm) / 2);
  break-after: page;
  page-break-after: always;
  background: white;
}}

.page:last-child {{
  break-after: auto;
  page-break-after: auto;
}}

@media screen {{
  body {{ padding: 12mm; }}
  .page {{
    margin-bottom: 12mm;
    box-shadow: 0 2px 12px rgba(0,0,0,0.3);
  }}
}}

.card {{
  width: 60mm;
  height: 84mm;
  border: 1.5px solid;
  border-radius: 7px;
  padding: 2.5mm 3mm 2mm;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}}

.card-top {{
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 1.5px;
}}

.card-name {{
  font-size: 12pt;
  font-weight: bold;
  line-height: 1.12;
  flex: 1;
  letter-spacing: 0.01em;
}}

.dot {{
  width: 11px;
  height: 11px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-left: 5px;
  margin-top: 2px;
}}

.card-sub {{
  font-size: 7.5pt;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 3px;
  font-style: italic;
}}

.divider {{
  height: 1px;
  margin-bottom: 3px;
}}

.tbl {{
  width: 100%;
  border-collapse: collapse;
  flex: 1;
}}

.tbl td {{
  font-size: 9.5pt;
  line-height: 1.28;
  vertical-align: top;
  padding: 1.5px 0;
}}

.tbl .lbl {{
  font-size: 7pt;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #555;
  white-space: nowrap;
  padding-right: 4px;
  width: 1px;
  padding-top: 2px;
}}

.card.dense .tbl td {{ font-size: 8.2pt; line-height: 1.22; }}
.card.dense .flavor {{ font-size: 8pt; }}
.card.dense .card-name {{ font-size: 11pt; }}

.card.denser .tbl td {{ font-size: 7pt; line-height: 1.18; }}
.card.denser .flavor {{ font-size: 7pt; }}
.card.denser .card-name {{ font-size: 10pt; }}
.card.denser .tbl .lbl {{ font-size: 6pt; }}

.flavor {{
  font-style: italic;
  font-size: 9pt;
  color: #555;
  line-height: 1.3;
  margin-top: auto;
  padding-top: 3px;
  border-top: 1px solid rgba(0,0,0,0.12);
}}

.item-effect {{
  font-size: 9.5pt;
  line-height: 1.35;
  flex: 1;
}}
</style>
</head>
<body>
{pages_html}
</body>
</html>'''


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    set_name = sys.argv[1] if len(sys.argv) > 1 else 'core'

    if set_name not in SETS:
        print(f'Unknown set: {set_name}')
        print(f'Available sets: {", ".join(SETS)}')
        sys.exit(1)

    cfg = SETS[set_name]
    print(f'Generating: {cfg["title"]}')

    all_cards = load_set(set_name)
    total_pages = -(-len(all_cards) // CARDS_PER_PAGE)
    output = f'card-print-{set_name}.html'

    with open(output, 'w', encoding='utf-8') as f:
        f.write(generate_html(all_cards, cfg['title']))

    print(f'  {len(all_cards)} items across {total_pages} pages → {output}')
    last = len(all_cards) % CARDS_PER_PAGE or CARDS_PER_PAGE
    if last < CARDS_PER_PAGE:
        print(f'  (last page has {last})')
    print('\nPrint settings: Margins = None, Background graphics = On, Scale = 100%')
