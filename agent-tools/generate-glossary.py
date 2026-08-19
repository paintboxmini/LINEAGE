#!/usr/bin/env python3
"""Rebuild rules/card-glossary.md from the per-keyword source files.

The glossary was one 191-line file that 47 other files pointed at, holding 29
keyword definitions, 4 status cards and one shared mechanic. Editing any single
definition meant touching the file everything cites, and a keyword that outgrew
its one-line entry had nowhere to go — Initiative Shift X had already escaped
into `rules/initiative-shift-examples.md` because there was no other home for
its worked cases.

So the definitions now live one per file, in `rules/keywords/` and
`rules/status-cards/`, and this rebuilds the printed glossary from them. The
file keeps its path — 105 references across the repo resolve to it, and every
one still works.

    python3 agent-tools/generate-glossary.py           # rebuild
    python3 agent-tools/generate-glossary.py --check    # exit 1 if stale

`verify.py`'s `check_glossary_generated` runs the second form, which is what
makes "generated" true rather than merely intended: hand-edit the output and the
build fails instead of quietly losing the edit on the next rebuild.

**Order is alphabetical.** It used to be descending usage count — a designer's
ordering in a file whose own header says it is meant to be printed and handed to
players. A player looking up Sealed mid-turn wants it where the S's are.

`rules/glossary-frame.md` holds everything that is not a definition: the
preamble, the section headings, the at-the-table token note, and Stat Change,
which is explicitly not a keyword. Two marker lines say where the generated
blocks go. The frame is hand-written; only what sits at the markers is built.
"""

import os
import re
import sys
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

FRAME = 'rules/glossary-frame.md'
OUTPUT = 'rules/card-glossary.md'
KEYWORDS = 'rules/keywords/*.md'
STATUS = 'rules/status-cards/*.md'


def entries(pattern):
    """(name, body) per source file, alphabetical by name."""
    out = []
    for path in sorted(glob.glob(pattern)):
        text = open(path, encoding='utf-8').read()
        m = re.match(r'^# (.+)\n', text)
        if not m:
            raise SystemExit(f'{path}: no "# NAME" heading on the first line')
        out.append((m.group(1).strip(), text[m.end():].strip()))
    return sorted(out, key=lambda e: e[0].lower())


def render():
    frame = open(FRAME, encoding='utf-8').read()
    for marker in ('<!-- KEYWORDS -->', '<!-- STATUS CARDS -->'):
        if frame.count(marker) != 1:
            raise SystemExit(f'{FRAME}: expected exactly one {marker}')

    kw = '\n\n'.join(f'**{name}**\n{body}' for name, body in entries(KEYWORDS))
    sc = '\n\n---\n\n'.join(f'### {name}\n{body}' for name, body in entries(STATUS))

    out = frame.replace('<!-- KEYWORDS -->', kw).replace('<!-- STATUS CARDS -->', sc)
    note = ('*Generated from `rules/keywords/` and `rules/status-cards/` by '
            '`agent-tools/generate-glossary.py`. Edit those, not this file — '
            '`verify.py` fails if the two disagree.*')
    # Placed under the title so anyone opening the file to edit it is told first.
    lines = out.split('\n')
    lines.insert(1, '\n' + note)
    return '\n'.join(lines).rstrip() + '\n'


def main():
    text = render()
    if '--check' in sys.argv:
        current = open(OUTPUT, encoding='utf-8').read() if os.path.exists(OUTPUT) else ''
        if current != text:
            print(f'STALE  {OUTPUT} — run `python3 agent-tools/generate-glossary.py`')
            return 1
        print(f'current  {OUTPUT}')
        return 0
    open(OUTPUT, 'w', encoding='utf-8').write(text)
    print(f'wrote {OUTPUT} '
          f'({len(entries(KEYWORDS))} keywords, {len(entries(STATUS))} status cards)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
