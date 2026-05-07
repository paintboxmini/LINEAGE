#!/usr/bin/env python3
"""Generate a print-ready HTML card sheet from core card files.
Open the output in Chrome/Firefox and print → Save as PDF.
"""

import re
import html as html_mod
import os

COLOR_HEX = {
    'BLUE':  '#2C5F9E',
    'RED':   '#9E2C2C',
    'GREEN': '#2A7A3E',
}

COLOR_BG = {
    'BLUE':  '#F0F4FA',
    'RED':   '#FAF0F0',
    'GREEN': '#F0F7F2',
}

COLOR_LABEL = {
    'BLUE':  'Mind',
    'RED':   'Body',
    'GREEN': 'Soul',
}


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
            # Card name: **NAME**
            m = re.match(r'^\*\*(.+?)\*\*$', line)
            if m and 'name' not in card:
                card['name'] = m.group(1)
                continue

            # Color line: BLUE — MIND or BLUE — MIND — TAG
            m = re.match(r'^(BLUE|RED|GREEN)\s*[—\-]+\s*(.+)$', line)
            if m:
                card['color'] = m.group(1)
                stat_part = re.split(r'\s*[—\-]+\s*', m.group(2))[0]
                card['stat'] = stat_part.strip()
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

    return f'''<div class="card" style="background:{bg_color};border-color:{hex_color}88">
  <div class="card-top">
    <div class="card-name">{h(card["name"])}</div>
    <div class="dot" style="background:{hex_color}"></div>
  </div>
  <div class="card-sub" style="color:{hex_color}">{h(stat_label)}</div>
  <div class="divider" style="background:{hex_color}44"></div>
  <table class="tbl">{rows}</table>
  {flavor}
</div>'''


def generate_html(all_cards):
    cards_html = '\n'.join(card_to_html(c) for c in all_cards)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Tales Untold — Core Cards</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}

body {{
  font-family: Georgia, "Times New Roman", serif;
  background: #ccc;
  padding: 0.4in;
}}

.sheet {{
  display: flex;
  flex-wrap: wrap;
  gap: 0.15in;
}}

.card {{
  width: 2.75in;
  min-height: 3.85in;
  border: 1.5px solid;
  border-radius: 10px;
  padding: 0.14in 0.16in 0.12in;
  display: flex;
  flex-direction: column;
  break-inside: avoid;
  page-break-inside: avoid;
}}

.card-top {{
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 2px;
}}

.card-name {{
  font-size: 14pt;
  font-weight: bold;
  line-height: 1.15;
  flex: 1;
  letter-spacing: 0.01em;
}}

.dot {{
  width: 20px;
  height: 20px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-left: 8px;
  margin-top: 3px;
}}

.card-sub {{
  font-size: 8pt;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 5px;
  font-style: italic;
}}

.divider {{
  height: 1px;
  margin-bottom: 6px;
}}

.tbl {{
  width: 100%;
  border-collapse: collapse;
  flex: 1;
}}

.tbl td {{
  font-size: 10pt;
  line-height: 1.35;
  vertical-align: top;
  padding: 2px 0;
}}

.tbl .lbl {{
  font-size: 7.5pt;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #555;
  white-space: nowrap;
  padding-right: 7px;
  width: 1px;
  padding-top: 3px;
}}

.flavor {{
  font-style: italic;
  font-size: 8pt;
  color: #555;
  line-height: 1.35;
  margin-top: auto;
  padding-top: 6px;
  border-top: 1px solid rgba(0,0,0,0.1);
}}

@media print {{
  body {{
    background: white;
    padding: 0.25in;
  }}
  .sheet {{
    gap: 0.12in;
  }}
}}
</style>
</head>
<body>
<div class="sheet">
{cards_html}
</div>
</body>
</html>'''


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    files = [
        'cards/blue-mind.md',
        'cards/red-body.md',
        'cards/green-soul.md',
    ]

    all_cards = []
    for f in files:
        batch = parse_cards(f)
        all_cards.extend(batch)
        print(f'  {f}: {len(batch)} cards')

    output = 'card-print.html'
    with open(output, 'w', encoding='utf-8') as f:
        f.write(generate_html(all_cards))

    print(f'\nGenerated {output} ({len(all_cards)} cards total)')
    print('Open in Chrome/Firefox → Print → Save as PDF')
    print('Set margins to Minimum, enable Background graphics')
