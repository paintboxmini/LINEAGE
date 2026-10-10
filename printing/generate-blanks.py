#!/usr/bin/env python3
"""Lay generated card art out 3x3 on a Letter page, ready to print and cut.

Why this exists rather than a prompt asking for a 3x3 sheet: nine cards
generated as one image come back nine slightly different sizes, slightly
rotated, with drifting colour and edges that do not line up with any cut
grid. Generate one card face at high resolution and tile it here instead.
The tiling is exact because it is the same grid generate-cards.py prints
real cards on — 60 x 84mm cells, 8mm column gaps, 3.5mm row gaps, inside
Letter's 10mm margin — so a blank sheet and a printed sheet cut identically.

Usage:
  python3 generate-blanks.py art/card-red.png            -> 9 of that one
  python3 generate-blanks.py art/red.png art/blue.png    -> cycles them
  python3 generate-blanks.py --pages 4 art/card-red.png  -> 4 pages of it

Print settings: Margins = None, Background graphics = On, Scale = 100%.
"""

import html as html_mod
import os
import sys

CARDS_PER_PAGE = 9


def build(images, pages):
    cells = []
    for i in range(pages * CARDS_PER_PAGE):
        src = html_mod.escape(images[i % len(images)])
        cells.append(f'<div class="slot"><img src="{src}" alt=""></div>')

    page_html = '\n'.join(
        f'<div class="page">{"".join(cells[p * CARDS_PER_PAGE:(p + 1) * CARDS_PER_PAGE])}</div>'
        for p in range(pages))

    return f'''<title>Tales Untold — Blank Cards</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
@page {{ size: letter; margin: 10mm; }}
body {{ background: #bbb; }}

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
.page:last-child {{ break-after: auto; page-break-after: auto; }}

@media screen {{
  body {{ padding: 12mm; }}
  .page {{ margin-bottom: 12mm; box-shadow: 0 2px 12px rgba(0,0,0,.3); }}
}}

/* The art is 5:7 and the cell is 60x84mm, which is also 5:7, so it fills
   the cell exactly. object-fit guards against art that came back a few
   pixels off — it crops rather than letterboxing or stretching, because a
   white sliver at a card edge is worse than losing a hairline of stone. */
.slot {{ width: 60mm; height: 84mm; overflow: hidden; }}
.slot img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
</style>
{page_html}'''


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    args = sys.argv[1:]
    pages = 1
    if '--pages' in args:
        i = args.index('--pages')
        pages = int(args[i + 1])
        del args[i:i + 2]

    if not args:
        raise SystemExit(__doc__.strip())

    missing = [a for a in args if not os.path.exists(a)]
    if missing:
        raise SystemExit('generate-blanks.py: not found: ' + ', '.join(missing))

    out = 'card-blanks.html'
    with open(out, 'w', encoding='utf-8') as f:
        f.write(build(args, pages))

    total = pages * CARDS_PER_PAGE
    print(f'Generating: Blank Cards')
    print(f'  {total} cards across {pages} page(s) -> {out}')
    for a in args:
        print(f'    {a}')
    print('\nPrint settings: Margins = None, Background graphics = On, Scale = 100%')
