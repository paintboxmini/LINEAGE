#!/usr/bin/env python3
"""Generate a print-ready HTML/PDF rendering of a rules/*.md document —
a normal flowing document, not the 3x3 sleeve-card grid generate-cards.py
produces. No external Markdown library (same "no dependencies" convention
as generate-cards.py and the combat simulator itself) — a small, targeted
converter for exactly the Markdown constructs these docs actually use:
# / ## headers, tables, fenced code blocks, horizontal rules,
bold/italic/inline-code, plain bullet/numbered lists, and blockquotes
(used for the Oracle's voice in the summons packet — styled with an
amber left border to read as a distinct register from the rules text).
No nesting, no images, no real hyperlinks (backtick file paths render
as inline code, not anchors).

Usage:
  python3 generate-rules-pdf.py                    → rules/player-guide.md
  python3 generate-rules-pdf.py gm-guide.md         → any rules/*.md file

Print settings: Margins = None, Background graphics = On, Scale = 100%.
"""

import re
import html as html_mod
import os
import sys


def h(text):
    return html_mod.escape(text)


def inline(text):
    """Bold, italic, inline code — order matters: bold (**) before italic (*)
    so a run of four asterisks doesn't get mis-split, then code last so
    escaped angle brackets inside backticks survive untouched."""
    text = h(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`([^`]+?)`', r'<code>\1</code>', text)
    return text


def parse_table(lines):
    """lines: consecutive '|...|' rows, including the '|---|---|' separator
    on row 2. Returns (html, rows_consumed)."""
    rows = [l.strip().strip('|').split('|') for l in lines]
    header = [c.strip() for c in rows[0]]
    body = [[c.strip() for c in r] for r in rows[2:]]  # skip the --- separator row
    out = ['<table class="doc-table">', '<thead><tr>']
    for c in header:
        out.append(f'<th>{inline(c)}</th>')
    out.append('</tr></thead><tbody>')
    for r in body:
        out.append('<tr>')
        for c in r:
            out.append(f'<td>{inline(c)}</td>')
        out.append('</tr>')
    out.append('</tbody></table>')
    return '\n'.join(out)


def convert(md_text, title):
    lines = md_text.split('\n')
    out = []
    i = 0
    n = len(lines)
    first_h1 = True

    while i < n:
        line = lines[i]

        if line.strip() == '':
            i += 1
            continue

        # Fenced code block
        if line.startswith('```'):
            i += 1
            block = []
            while i < n and not lines[i].startswith('```'):
                block.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            out.append(f'<pre>{h(chr(10).join(block))}</pre>')
            continue

        # Horizontal rule
        if line.strip() == '---':
            out.append('<hr>')
            i += 1
            continue

        # Headers
        if line.startswith('# '):
            if first_h1:
                out.append(f'<h1 class="doc-title">{inline(line[2:])}</h1>')
                first_h1 = False
            else:
                out.append(f'<h1 class="section-break">{inline(line[2:])}</h1>')
            i += 1
            continue
        if line.startswith('## '):
            out.append(f'<h2>{inline(line[3:])}</h2>')
            i += 1
            continue

        # Table
        if line.startswith('|'):
            block = []
            while i < n and lines[i].startswith('|'):
                block.append(lines[i])
                i += 1
            out.append(parse_table(block))
            continue

        # Blockquote — the Oracle's own voice in the summons packet. Blank
        # lines inside a quote start a new paragraph within the same block.
        if line.startswith('>'):
            paras = [[]]
            while i < n and (lines[i].startswith('>') or
                             (lines[i].strip() == '' and i + 1 < n and lines[i + 1].startswith('>'))):
                # A bare '>' (or a truly blank line between quoted blocks) breaks
                # the paragraph without ending the quote.
                content = lines[i].lstrip('>').strip()
                if content == '':
                    if paras[-1]:
                        paras.append([])
                else:
                    paras[-1].append(content)
                i += 1
            inner = ''.join(f'<p>{inline(" ".join(p))}</p>' for p in paras if p)
            out.append(f'<blockquote>{inner}</blockquote>')
            continue

        # Bullet list
        if line.startswith('- '):
            block = []
            while i < n and lines[i].startswith('- '):
                block.append(lines[i][2:])
                i += 1
            items = ''.join(f'<li>{inline(it)}</li>' for it in block)
            out.append(f'<ul>{items}</ul>')
            continue

        # Numbered list
        if re.match(r'^\d+\.\s', line):
            block = []
            while i < n and re.match(r'^\d+\.\s', lines[i]):
                block.append(re.sub(r'^\d+\.\s', '', lines[i]))
                i += 1
            items = ''.join(f'<li>{inline(it)}</li>' for it in block)
            out.append(f'<ol>{items}</ol>')
            continue

        # Paragraph (collect until blank line, table, header, hr, or list start)
        block = [line]
        i += 1
        while i < n and lines[i].strip() != '' and not (
            lines[i].startswith('#') or lines[i].startswith('|') or
            lines[i].startswith('```') or lines[i].strip() == '---' or
            lines[i].startswith('- ') or lines[i].startswith('>') or
            re.match(r'^\d+\.\s', lines[i])
        ):
            block.append(lines[i])
            i += 1
        out.append(f'<p>{inline(" ".join(block))}</p>')

    body = '\n'.join(out)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Tales Untold — {h(title)}</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}

@page {{
  size: letter;
  margin: 20mm 18mm;
}}

body {{
  font-family: Georgia, "Times New Roman", serif;
  color: #1a1a1a;
  line-height: 1.5;
  font-size: 10.5pt;
}}

h1 {{
  font-size: 20pt;
  margin: 0 0 8mm 0;
  color: #1a1a1a;
  border-bottom: 2px solid #333;
  padding-bottom: 3mm;
}}

h1.section-break {{
  break-before: page;
  page-break-before: always;
  padding-top: 2mm;
}}

h1.doc-title {{
  break-before: auto;
  page-break-before: avoid;
}}

h2 {{
  font-size: 13pt;
  margin: 7mm 0 3mm 0;
  color: #2C5F9E;
  border-bottom: 1px solid #ccc;
  padding-bottom: 1.5mm;
}}

p {{
  margin: 0 0 3mm 0;
  text-align: left;
}}

hr {{
  border: none;
  border-top: 1px solid #ddd;
  margin: 4mm 0;
}}

ul, ol {{
  margin: 0 0 3mm 6mm;
}}

li {{
  margin-bottom: 1mm;
}}

code {{
  font-family: "Courier New", monospace;
  font-size: 9.5pt;
  background: #f2f2f2;
  padding: 0.5px 3px;
  border-radius: 2px;
}}

pre {{
  font-family: "Courier New", monospace;
  font-size: 9.5pt;
  background: #f7f7f7;
  border: 1px solid #ddd;
  border-radius: 3px;
  padding: 3mm 4mm;
  margin: 0 0 3mm 0;
  white-space: pre;
}}

table.doc-table {{
  width: 100%;
  border-collapse: collapse;
  margin: 0 0 4mm 0;
  font-size: 9.5pt;
}}

table.doc-table th {{
  background: #2C5F9E;
  color: white;
  text-align: left;
  padding: 1.5mm 3mm;
  font-size: 8.5pt;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}}

table.doc-table td {{
  padding: 1.5mm 3mm;
  border-bottom: 1px solid #e0e0e0;
  vertical-align: top;
}}

table.doc-table tr:nth-child(even) td {{
  background: #f7f9fc;
}}

blockquote {{
  margin: 0 0 4mm 0;
  padding: 2mm 0 2mm 5mm;
  border-left: 2px solid #9a7b2f;
  color: #3a3226;
  font-style: italic;
}}

blockquote p {{
  margin: 0 0 2mm 0;
}}

blockquote p:last-child {{
  margin-bottom: 0;
}}

strong {{
  font-weight: bold;
}}

em {{
  font-style: italic;
}}

@media screen {{
  body {{
    max-width: 210mm;
    margin: 12mm auto;
    padding: 15mm;
    background: white;
    box-shadow: 0 2px 12px rgba(0,0,0,0.15);
  }}
}}
</style>
</head>
<body>
{body}
</body>
</html>'''


# Named multi-document builds. `packet` is the thing that actually goes out
# to players: the Oracle's summons, then the plain mechanical guide behind it.
PACKETS = {
    'packet': {
        'title': 'A Summons to Eclipseria',
        'files': ['the-summons.md', 'player-guide.md'],
    },
}


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    arg = sys.argv[1] if len(sys.argv) > 1 else 'player-guide.md'

    if arg in PACKETS:
        cfg = PACKETS[arg]
        parts = []
        for fname in cfg['files']:
            src = f'../rules/{fname}'
            if not os.path.exists(src):
                print(f'Not found: {src}')
                sys.exit(1)
            with open(src, encoding='utf-8') as f:
                parts.append(f.read().strip())
        md_text = '\n\n'.join(parts)
        title = cfg['title']
        output = f'{arg}.html'
        srclabel = ' + '.join(cfg['files'])
    else:
        fname = arg
        src = f'../rules/{fname}'
        if not os.path.exists(src):
            print(f'Not found: {src}')
            sys.exit(1)
        with open(src, encoding='utf-8') as f:
            md_text = f.read()
        title_match = re.match(r'^#\s+(.+)$', md_text.split('\n', 1)[0])
        title = title_match.group(1) if title_match else fname
        output = f'{fname[:-3] if fname.endswith(".md") else fname}.html'
        srclabel = src

    with open(output, 'w', encoding='utf-8') as f:
        f.write(convert(md_text, title))

    print(f'{srclabel} → {output}')
    print('\nPrint settings: Margins = None, Background graphics = On, Scale = 100%')
