#!/usr/bin/env python3
"""Generate print-ready character sheets at index-card size (3" x 5"),
4 to a Letter page.

Everything on a sheet is read out of the character's own file in campaign/ —
nothing is transcribed here. HP, hand size, initiative and maximum deck size
are recomputed from the stat table every build rather than copied from the
prose beside it, because that is exactly the pair that drifts: campaign/pat.md
and campaign/kevin.md both carried an HP figure from the old 3x Body formula
for six days after the formula changed.

Single-sided on purpose. A two-sided sheet prints wrong as often as it prints
right, and everything a player touches mid-fight fits on one face.

Usage:
  python3 generate-sheets.py            -> every character + a blank
  python3 generate-sheets.py pat chris  -> just those

Print settings: Margins = None, Background graphics = On, Scale = 100%.
"""

import html as html_mod
import os
import re
import sys

CHARACTERS = ['pat', 'chris', 'kevin']
SRC_DIR = '../campaign'
CARDS_PER_PAGE = 4

STAT_ROW = re.compile(r'^\|\s*(Mind|Body|Soul)\s*\|\s*(\d+)\s*\|', re.M)
BULLET = re.compile(r'^-\s+\*\*(.+?)\*\*\s*(?:—\s*(.*))?$', re.M)
# A Passive's printed shape, out of campaign/passives.md's own card blocks.
PASSIVE_BLOCK = re.compile(
    r'^\*\*(?P<name>[A-Z0-9\' \-]+)\*\*\s*\n'
    r'(?P<color>RED|BLUE|GREEN)\s*—\s*(?P<stat>MIND|BODY|SOUL)\s*\n'
    r'Attack:\s*(?P<attack>[^\n]+)\n'
    r'(?:(?!^\*\*)[^\n]*\n)*?'
    r'Range:\s*(?P<range>Melee|Ranged|Both)\s*$', re.M)


def passive_shapes():
    """name -> "Red · Melee · d6", read from the Passive's own card block.

    The character files also state each Passive's colour and die in prose, but
    that is a copy; this is the definition. Reading the definition means a
    sheet cannot quietly disagree with the card it is describing."""
    path = os.path.join(SRC_DIR, 'passives.md')
    out = {}
    for m in PASSIVE_BLOCK.finditer(open(path, encoding='utf-8').read()):
        die = re.search(r'(d\d+)', m.group('attack'))
        parts = [m.group('color').title(), m.group('range')]
        if die:
            parts.append(die.group(1))
        out[m.group('name').strip()] = ' · '.join(parts)
    return out


def h(t):
    return html_mod.escape(str(t))


def section(text, *names):
    """Body of the first `## ` section whose heading starts with any of names."""
    for m in re.finditer(r'^##\s+(.+?)\s*$', text, re.M):
        head = m.group(1)
        if any(head.lower().startswith(n.lower()) for n in names):
            start = m.end()
            nxt = re.search(r'^##\s+', text[start:], re.M)
            return text[start:start + nxt.start()] if nxt else text[start:]
    return ''


def find_trait(text):
    """Traits are written two ways: a heading that says Trait, or a section
    whose body declares itself one. Both are live in campaign/ right now."""
    for m in re.finditer(r'^##\s+(.+?)\s*$', text, re.M):
        head = m.group(1)
        start = m.end()
        nxt = re.search(r'^##\s+', text[start:], re.M)
        body = text[start:start + nxt.start()] if nxt else text[start:]
        if head.lower().startswith('trait'):
            return re.sub(r'^trait\s*[—-]\s*', '', head, flags=re.I).strip()
        if re.search(r'\*\*This is a Trait\*\*', body):
            return head.strip()
    return ''


def short(s, limit=58):
    """First clause of a bullet's description, trimmed to fit a card line."""
    s = re.sub(r'`[^`]*`', '', s or '')
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)
    s = re.sub(r'[*_]', '', s)
    s = s.strip().lstrip('.;,— ').strip()
    s = re.split(r'(?<=[.;])\s', s)[0].strip(' .;')
    s = re.sub(r'\s+', ' ', s)
    return s[:limit].rstrip() + '…' if len(s) > limit else s


def bullets(body, limit=2):
    out = []
    for m in BULLET.finditer(body or ''):
        out.append((m.group(1).strip(), short(m.group(2) or '')))
        if len(out) == limit:
            break
    return out


def load(name, shapes):
    path = os.path.join(SRC_DIR, f'{name}.md')
    text = open(path, encoding='utf-8').read()

    stats = {k: int(v) for k, v in STAT_ROW.findall(text)}
    for k in ('Mind', 'Body', 'Soul'):
        if k not in stats:
            raise SystemExit(f'generate-sheets.py: no {k} row in {path}')

    heading = re.search(r'^#\s+(.+?)\s*$', text, re.M)
    stat_head = re.search(r'^##\s+(Stats.*?)\s*$', text, re.M)

    return {
        'name': heading.group(1).strip() if heading else name.title(),
        'stats': stats,
        # Derived here, every build. Never read off the page.
        'hp': 4 * stats['Body'] + stats['Soul'] + stats['Mind'],
        'hand': max(2, stats['Mind']),
        'init': stats['Soul'],
        'deck': sum(stats.values()),
        'provisional': 'unconfirmed' in (stat_head.group(1).lower() if stat_head else ''),
        'passives': [(n, shapes.get(n, '(not in passives.md)'))
                     for n, _ in bullets(section(text, 'Passives'))],
        'skills': bullets(section(text, 'Skills')),
        'trait': find_trait(text),
    }


BLANK = {
    'name': '', 'stats': {'Body': '', 'Mind': '', 'Soul': ''},
    'hp': '', 'hand': '', 'init': '', 'deck': '', 'provisional': False,
    'passives': [], 'skills': [], 'trait': '',
}


def rule(n=1):
    return '<div class="rule"></div>' * n


def slot(label, filled, note=''):
    if filled:
        body = f'<span class="fill">{h(filled)}</span>'
        if note:
            body += f' <span class="note">{h(note)}</span>'
    else:
        body = '<span class="blank"></span>'
    return f'<div class="row"><span class="lbl">{h(label)}</span>{body}</div>'


def sheet_html(c):
    s = c['stats']
    init = f"1d6 + {c['init']}" if c['init'] != '' else ''

    passives = c['passives'] or [('', ''), ('', '')]
    passives = (passives + [('', ''), ('', '')])[:2]
    skills = c['skills'] or [('', ''), ('', '')]
    skills = (skills + [('', ''), ('', '')])[:2]

    name = h(c['name']) if c['name'] else '<span class="blank wide"></span>'
    flag = '<span class="prov">provisional</span>' if c['provisional'] else ''

    stat_cells = ''.join(
        f'<div class="stat"><div class="sv">{h(v) if v != "" else "&nbsp;"}</div>'
        f'<div class="sn">{k}</div></div>'
        for k, v in (('Body', s['Body']), ('Mind', s['Mind']), ('Soul', s['Soul'])))

    derived = ''.join(
        f'<div class="d"><span class="dl">{lbl}</span>'
        f'<span class="dv">{h(val) if val != "" else "&nbsp;"}</span></div>'
        for lbl, val in (('Max HP', c['hp']), ('Hand', c['hand']),
                         ('Init', init), ('Deck Max', c['deck'])))

    return f'''<div class="sheet">
  <div class="head"><span class="nm">{name}</span>{flag}</div>
  <div class="stats">{stat_cells}</div>
  <div class="derived">{derived}</div>

  <div class="hp"><span class="lbl">Current HP</span><span class="hpbox"></span>
    <span class="lbl">Position</span><span class="pos">Front &nbsp;/&nbsp; Back</span></div>

  <div class="sec">Passives</div>
  {slot('1', passives[0][0], passives[0][1])}
  {slot('2', passives[1][0], passives[1][1])}

  <div class="sec">Trait</div>
  {slot('', c['trait'])}

  <div class="sec">Skills</div>
  {slot('1', skills[0][0])}
  {slot('2', skills[1][0])}

  <div class="sec">Equipment</div>
  {slot('Weapon', '')}
  {slot('Armor', '')}
  {slot('Artifact', '')}

  <div class="sec">Price <span class="hint">I never / I must / I always / I cannot / Once I / Whenever</span></div>
  {rule(2)}

  <div class="sec">Statuses &amp; Bank</div>
  {rule(2)}
</div>'''


def chunk(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def page_html(sheets):
    pages = []
    for group in chunk(sheets, CARDS_PER_PAGE):
        cells = ''.join(group)
        cells += '<div class="sheet empty"></div>' * (CARDS_PER_PAGE - len(group))
        pages.append(f'<div class="page">{cells}</div>')
    return '\n'.join(pages)


def document(sheets, title):
    return f'''<title>Tales Untold — {h(title)}</title>
<style>
@page {{ size: Letter; margin: 0; }}
body {{ font-family: "Iowan Old Style", Georgia, serif; background: #888; }}

.page {{
  width: 216mm; height: 279mm;
  padding: 12.5mm 25.4mm;
  display: grid;
  grid-template-columns: repeat(2, 76.2mm);
  grid-template-rows: repeat(2, 127mm);
  column-gap: 12.4mm;
  row-gap: 0;
  break-after: page; page-break-after: always;
  background: white;
}}
.page:last-child {{ break-after: auto; page-break-after: auto; }}

@media screen {{
  body {{ padding: 12mm; }}
  .page {{ margin-bottom: 12mm; box-shadow: 0 2px 12px rgba(0,0,0,.35); }}
}}

.sheet {{
  width: 76.2mm; height: 127mm;
  border: 1.2px solid #333; border-radius: 6px;
  padding: 3mm 3.4mm 2.6mm;
  display: flex; flex-direction: column;
  overflow: hidden; background: #FDFCF8;
}}
.sheet.empty {{ border: 1px dashed #CCC; background: transparent; }}

.head {{ display: flex; align-items: baseline; justify-content: space-between;
         border-bottom: 1.5px solid #333; padding-bottom: 1.2mm; margin-bottom: 1.6mm; }}
.nm {{ font-size: 13pt; font-weight: bold; letter-spacing: .01em; }}
.prov {{ font-size: 6pt; text-transform: uppercase; letter-spacing: .09em;
         color: #8A6A20; border: .8px solid #C7A65A; border-radius: 2px; padding: .3mm 1mm; }}

.stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.6mm; margin-bottom: 1.6mm; }}
.stat {{ border: 1px solid #999; border-radius: 3px; text-align: center; padding: .8mm 0 .5mm; }}
.sv {{ font-size: 15pt; font-weight: bold; line-height: 1; }}
.sn {{ font-size: 6pt; text-transform: uppercase; letter-spacing: .1em; color: #555; }}

.derived {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 1mm; margin-bottom: 1.8mm; }}
.d {{ text-align: center; }}
.dl {{ display: block; font-size: 5.6pt; text-transform: uppercase; letter-spacing: .07em; color: #666; }}
.dv {{ display: block; font-size: 8.5pt; font-weight: bold; }}

.hp {{ display: flex; align-items: center; gap: 1.4mm; margin-bottom: 1.8mm; }}
.hpbox {{ flex: 1; border: 1px solid #666; border-radius: 2px; height: 5.2mm; background: #fff; }}
.pos {{ font-size: 7pt; white-space: nowrap; }}

.sec {{ font-size: 6.2pt; font-weight: bold; text-transform: uppercase;
        letter-spacing: .1em; color: #444;
        border-bottom: .7px solid #BBB; margin: 1.2mm 0 .9mm; padding-bottom: .4mm; }}
.hint {{ font-weight: normal; text-transform: none; letter-spacing: 0;
         color: #888; font-size: 5.6pt; font-style: italic; }}

.row {{ display: flex; align-items: baseline; gap: 1.2mm; margin-bottom: .9mm; min-height: 3.6mm; }}
.lbl {{ font-size: 6pt; text-transform: uppercase; letter-spacing: .06em;
        color: #777; min-width: 8mm; }}
.fill {{ font-size: 8.5pt; font-weight: bold; }}
.note {{ font-size: 6.4pt; color: #666; font-style: italic; }}
.blank {{ flex: 1; border-bottom: .7px solid #AAA; height: 3.2mm; }}
.blank.wide {{ min-width: 34mm; display: inline-block; }}

.rule {{ border-bottom: .7px solid #AAA; height: 4mm; margin-bottom: .6mm; }}
</style>
{page_html(sheets)}'''


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    wanted = sys.argv[1:] or CHARACTERS
    unknown = [w for w in wanted if w not in CHARACTERS]
    if unknown:
        raise SystemExit(f'Unknown character(s): {", ".join(unknown)}. '
                         f'Known: {", ".join(CHARACTERS)}')

    shapes = passive_shapes()
    sheets, loaded = [], []
    for n in wanted:
        c = load(n, shapes)
        loaded.append(c)
        sheets.append(sheet_html(c))
    sheets.append(sheet_html(BLANK))

    out = 'character-sheets.html'
    with open(out, 'w', encoding='utf-8') as f:
        f.write(document(sheets, 'Character Sheets'))

    pages = -(-len(sheets) // CARDS_PER_PAGE)
    print(f'Generating: Character Sheets')
    print(f'  {len(sheets)} sheets ({len(loaded)} characters + 1 blank) '
          f'across {pages} pages -> {out}')
    for c in loaded:
        s = c['stats']
        flag = '  [provisional]' if c['provisional'] else ''
        print(f"    {c['name']:<8} B{s['Body']} M{s['Mind']} S{s['Soul']}  "
              f"HP {c['hp']}  hand {c['hand']}  init 1d6+{c['init']}  "
              f"deck {c['deck']}{flag}")
    print('\nPrint settings: Margins = None, Background graphics = On, Scale = 100%')
