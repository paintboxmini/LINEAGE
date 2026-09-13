# What This Environment Can Actually Do to Cards

Measured on 2026-09-13, not estimated. The question was whether cards can be
made properly artistic here without hand-generating art per card, whether PDF
is the right format, and whether fonts, borders and texture are available.

Short answer: **yes to all of it, PDF is right, and it costs about 0.6 MB for
a 63-card deck** — provided the texture is done one specific way.

---

## Is PDF the right format?

Yes, and for a reason worth knowing: a Chrome-printed PDF is **mixed**. Text
stays live vector with the typeface embedded and subset, so it is razor sharp
at any size and prints at the printer's own resolution. Only the things that
genuinely need pixels — texture, blends — get rasterized, and Chrome does that
at **300 dpi**, measured.

That is the best of both. A PNG export would flatten the type to pixels; an
SVG would not embed reliably for a print shop. Keep PDF.

---

## Fonts

`fc-list` shows 59 installed faces here and they are all generic — DejaVu,
Liberation, FreeSerif, Bitstream Charter. **Georgia is not among them**, which
matters because `generate-cards.py` currently asks for Georgia and silently
falls back to Liberation Serif in every PDF this environment has produced.

Google Fonts is reachable from here (the CSS endpoint and the `.ttf` files both
return 200), so real typefaces can be downloaded, base64-embedded in the CSS,
and they subset into the PDF correctly. Verified with three:

| Face | Role | Why |
|---|---|---|
| Cinzel SemiBold | card names | Roman inscriptional capitals — literally letters cut in stone |
| EB Garamond | rules text | Old-style serif, holds up small, high legibility at 9 pt |
| IM Fell English Italic | flavour text | Antique press italic, clearly a different voice from the rules |

**Vendor them rather than fetching at build time.** Roughly 630 KB of TTF for
the three. A build that needs the network is a build that breaks.

---

## Borders, washes, texture

All of it is plain CSS and SVG, no image assets and no AI:

- **Borders** — a coloured card edge plus an inset hairline rule a millimetre
  and a half in, tinted from the card's own colour. Two lines of CSS.
- **Colour wash** — `radial-gradient` in the card's hue, strongest at the top
  and fading out, so the card reads as tinted stock rather than a white
  rectangle with a coloured line around it.
- **Texture** — procedural grain, covered below, and it is the one with a trap
  in it.

---

## The texture trap — 87 MB against 0.6 MB

Two ways to get paper grain. They look nearly identical and differ in size by
**135×**.

| Method | Per page | 63-card deck | Image objects |
|---|---|---|---|
| SVG `feTurbulence` across the whole page | 12,723 KB | **87.0 MB** | 2 × 2317×3063 px |
| A 160×160 PNG noise tile, repeated | 94 KB | **0.6 MB** | 1 × 160×160 px |

`feTurbulence` is the obvious choice and it is the wrong one. Chrome cannot
keep an SVG filter as vector, so it rasterizes the entire painted area at
300 dpi and embeds that — per page, twice over. `mix-blend-mode` forces the
same flattening wherever it is used.

A small noise tile set to `background-repeat` stays **one small image object**
that the PDF references over and over. Generate the tile procedurally at build
time (a few lines of zlib and struct — no image library needed, and there is
no Pillow here) so nothing binary has to be committed.

Put the grain on the **page**, not on each card. The cards are cut out of the
page anyway, so the texture runs continuously underneath them and each card
takes its own slice — which is also what printing on textured stock actually
does.

---

## What this would change in the pipeline

Nothing structural. `generate-cards.py` already emits HTML that Chrome prints;
this is all CSS and one embedded tile. The 3×3 grid, the card data, the set
definitions and `generate-all.sh` stay exactly as they are.

Not yet done — this file records the investigation, not a decision.
