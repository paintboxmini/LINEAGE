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

## The gradient trap — and the faint grid it draws

The first styled sheet came back with very faint vertical and horizontal
lines across it, almost imperceptible, on a regular grid. The cause was not
the texture, which was the obvious suspect and was innocent. It was the
**`radial-gradient` colour wash.**

Chrome cannot emit a CSS gradient as a plain fill. It builds a **PDF tiling
pattern**, and most viewers draw a hairline at every pattern cell boundary.
Isolated by elimination on one 9-card page:

| Page contains | Tiling patterns | Shadings |
|---|---|---|
| grain and wash | 9 | 18 |
| grain only, wash removed | **0** | **0** |
| wash only, grain removed | 9 | 18 |

`background-repeat` does the same thing for the same reason, and so does
`mix-blend-mode`. Any of the three puts a pattern in the PDF.

**The fix is to bake the wash into the texture image.** One RGBA PNG per
colour carries the paper grain in its alpha and the colour falloff in its
RGB, drawn once per card at `background-size: 100% 100%` with
`background-repeat: no-repeat`. No gradient, no repeat, no blend mode
anywhere in the card CSS. Verified on a real 21-card build: **0 tiling
patterns, 0 shadings**, all four typefaces embedded and subset.

So the rule for this pipeline is narrower than "avoid feTurbulence":

> Anything that makes Chrome emit a pattern will draw a grid on the page.
> Gradients, repeats and blend modes all do. Bake them into an image
> instead, and draw that image exactly once per element.

---

## What this changed in the pipeline

Nothing structural. `generate-cards.py` still emits HTML that Chrome prints,
and the 3×3 grid, the card data, the set definitions and `generate-all.sh`
are untouched. What was added: four vendored typefaces under
`printing/assets/fonts/`, and `printing/make-grain.py`, which writes one
stock texture per card colour into `printing/assets/`.

Fonts are vendored rather than fetched, because a build that needs the
network is a build that breaks. All four are SIL Open Font License.
