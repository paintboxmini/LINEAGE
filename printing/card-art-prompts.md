# Card — Art Prompts

Blank card plates in the same hand as the character sheet, and a text pass
to go over them. Same two-step method: the face prompts make a card with no
lettering on it at all, the fields prompt lays the card's labels over a
finished face.

**Five prompts.** One face per colour — Red, Blue, Green and Neutral for the
colourless cards — then the fields pass, run once on each of the four
finished faces. Every prompt is complete on its own, including its
negatives, so any one of them can be pasted whole into an image model that
knows nothing about this world without reading anything else here.

**The four faces are word-for-word identical apart from three lines**, and
that is deliberate rather than lazy: the pigment disc, the mineral veining,
and the tint in the chiselled groove. Those three carry the colour; nothing
else changes, so the four print as one set rather than four designs that
happen to share a size. If you edit one face, make the same edit to the
other three.

| | Disc | Carries |
|---|---|---|
| Red | `#9E2C2C` deep oxblood | self-buffs and raw damage, the biggest dice |
| Blue | `#2C5F9E` deep ink | enemy control — debuffs, repositioning, taking options away |
| Green | `#2A7A3E` deep forest | flexibility and support — healing, allies, movement |
| Neutral | `#5A5A5A` slate grey | the colourless cards |

**Canvas:** 5:7 portrait, which is the printed card exactly (60 × 84 mm).
Render at least 1000 × 1400.

**Generate one card, then tile it.** Nine cards asked for as a single image
come back nine slightly different sizes, slightly rotated, with drifting
colour and edges that line up with no cut grid. Make one face at high
resolution per colour and lay it out with `generate-blanks.py`, which tiles
3x3 on Letter using the exact grid real cards print on: 60 x 84 mm cells,
8 mm between columns, 3.5 mm between rows, inside a 10 mm page margin. A
blank sheet and a printed sheet then cut identically.

```
python3 generate-blanks.py art/card-red.png              # 9 of one
python3 generate-blanks.py art/red.png art/blue.png      # cycles them
python3 generate-blanks.py --pages 4 art/card-red.png    # four pages
```

---

## Two things that make this different from the sheet

**A card is dense with print; the sheet was mostly blank lines.** The median
card carries about 140 characters of rules text and some run past 300, set
around 8pt on a 60 mm card. Ornament that looks restrained on an index card
will bury this. The plate has to be quieter than the sheet by a wide margin
— the same materials, a fraction of the incident.

**Cards get cut and sleeved, so the edge must be clean.** No torn deckle, no
burnt corners, no pins, no lifting paper. Those were right on a page and are
wrong on something that has to sit square in a sleeve and match 53 siblings
on a cut grid.

---

## 1. Red Card Face — art only, no text

> A blank playing-card face, portrait 5:7, in the style of an antique
> survey-atlas plate. **Clean rectangular edges, perfectly square corners,
> full bleed to the edge** — no torn paper, no deckle, no burn marks, no
> pins, no tape, no lifted corners, no drop shadow, no frame around a frame.
>
> **The surface is pale grey-white quartz stone**, finely worked flat: a
> smooth slab with faint mineral veining, a hairline crack or two, and the
> soft tonal unevenness of real stone. Weathered and matte, like something
> handled for years. Bone, chalk and weathered parchment throughout. Flat
> overcast light, no sun anywhere, no shadow direction, no gloss.
>
> **A single circular disc of solid matte pigment sits in the upper right
> corner**, inset into the stone like a cake of dry pigment set into a slab.
> Colour: **deep oxblood red, `#9E2C2C`**. Strong, full, unmistakable colour —
> not pale, not pastel, not washed out, not translucent. Dead flat and
> chalk-matte: no gloss, no glass, no enamel, no varnish, no specular
> highlight, no reflection, no gemstone. A clean pale rim of bare stone runs
> around it. It is the only saturated thing on the card and it is **empty —
> no symbol, no numeral, no mark inside it**.
>
> **The mineral veins running through the quartz carry the faintest trace of
> that same red** — a whisper of it in the stone, at perhaps 10%
> strength, nothing like the disc. The rest of the slab stays grey-white.
>
> **A single fine chiselled groove runs horizontally across the card below
> the top zone**, a divider rule cut into the stone rather than drawn on it —
> V-grooved, catching light along one edge, with faint chalk setting-out
> marks still visible under the cut and slightly out of true with it. One
> line only, tinted very faintly red where pigment has worked into
> the cut.
>
> **A narrow chiselled border line** runs just inside the card edge on all
> four sides, the same cut character, thin and even, framing the face without
> decorating it.
>
> **The centre and lower two-thirds of the card are open, flat, undecorated
> stone** — clean enough to print twelve lines of small text on. Keep this
> area almost entirely empty. Permitted here, and only whisper-faint at
> 8–12% contrast: a ghost of survey linework, a fragment of a bearing arc, a
> trace of contour hatching, a pale water-stain. Nothing with an edge hard
> enough to be mistaken for a letter.
>
> Style: hand-drafted antique cartography crossed with architectural stone
> rubbing. Restrained, precise, austere, and mostly empty by design. Matte,
> printable, high detail, flat lighting.

**Negative / must not appear:**

> no text, no letters, no numerals, no words, no runes, no readable script,
> no calligraphy, no labels, no signature, no watermark, no gibberish
> lettering anywhere; nothing inside the coloured disc; no second disc; no
> people, no faces, no creatures, no weapons, no armour; no landscape, no
> scenery, no sky, no water, no trees, no buildings; no torn or deckled
> edge, no pins, no tape; no ornate border, no scrollwork, no filigree, no
> corner flourishes, no card frame, no banner or ribbon shapes; no
> illustration window or art box; no glow, no sparkle, no gradient wash; no
> clutter anywhere in the lower two-thirds.

---

## 2. Blue Card Face — art only, no text

> A blank playing-card face, portrait 5:7, in the style of an antique
> survey-atlas plate. **Clean rectangular edges, perfectly square corners,
> full bleed to the edge** — no torn paper, no deckle, no burn marks, no
> pins, no tape, no lifted corners, no drop shadow, no frame around a frame.
>
> **The surface is pale grey-white quartz stone**, finely worked flat: a
> smooth slab with faint mineral veining, a hairline crack or two, and the
> soft tonal unevenness of real stone. Weathered and matte, like something
> handled for years. Bone, chalk and weathered parchment throughout. Flat
> overcast light, no sun anywhere, no shadow direction, no gloss.
>
> **A single circular disc of solid matte pigment sits in the upper right
> corner**, inset into the stone like a cake of dry pigment set into a slab.
> Colour: **deep ink blue, `#2C5F9E`**. Strong, full, unmistakable colour —
> not pale, not pastel, not washed out, not translucent. Dead flat and
> chalk-matte: no gloss, no glass, no enamel, no varnish, no specular
> highlight, no reflection, no gemstone. A clean pale rim of bare stone runs
> around it. It is the only saturated thing on the card and it is **empty —
> no symbol, no numeral, no mark inside it**.
>
> **The mineral veins running through the quartz carry the faintest trace of
> that same blue** — a whisper of it in the stone, at perhaps 10%
> strength, nothing like the disc. The rest of the slab stays grey-white.
>
> **A single fine chiselled groove runs horizontally across the card below
> the top zone**, a divider rule cut into the stone rather than drawn on it —
> V-grooved, catching light along one edge, with faint chalk setting-out
> marks still visible under the cut and slightly out of true with it. One
> line only, tinted very faintly blue where pigment has worked into
> the cut.
>
> **A narrow chiselled border line** runs just inside the card edge on all
> four sides, the same cut character, thin and even, framing the face without
> decorating it.
>
> **The centre and lower two-thirds of the card are open, flat, undecorated
> stone** — clean enough to print twelve lines of small text on. Keep this
> area almost entirely empty. Permitted here, and only whisper-faint at
> 8–12% contrast: a ghost of survey linework, a fragment of a bearing arc, a
> trace of contour hatching, a pale water-stain. Nothing with an edge hard
> enough to be mistaken for a letter.
>
> Style: hand-drafted antique cartography crossed with architectural stone
> rubbing. Restrained, precise, austere, and mostly empty by design. Matte,
> printable, high detail, flat lighting.

**Negative / must not appear:**

> no text, no letters, no numerals, no words, no runes, no readable script,
> no calligraphy, no labels, no signature, no watermark, no gibberish
> lettering anywhere; nothing inside the coloured disc; no second disc; no
> people, no faces, no creatures, no weapons, no armour; no landscape, no
> scenery, no sky, no water, no trees, no buildings; no torn or deckled
> edge, no pins, no tape; no ornate border, no scrollwork, no filigree, no
> corner flourishes, no card frame, no banner or ribbon shapes; no
> illustration window or art box; no glow, no sparkle, no gradient wash; no
> clutter anywhere in the lower two-thirds.

---

## 3. Green Card Face — art only, no text

> A blank playing-card face, portrait 5:7, in the style of an antique
> survey-atlas plate. **Clean rectangular edges, perfectly square corners,
> full bleed to the edge** — no torn paper, no deckle, no burn marks, no
> pins, no tape, no lifted corners, no drop shadow, no frame around a frame.
>
> **The surface is pale grey-white quartz stone**, finely worked flat: a
> smooth slab with faint mineral veining, a hairline crack or two, and the
> soft tonal unevenness of real stone. Weathered and matte, like something
> handled for years. Bone, chalk and weathered parchment throughout. Flat
> overcast light, no sun anywhere, no shadow direction, no gloss.
>
> **A single circular disc of solid matte pigment sits in the upper right
> corner**, inset into the stone like a cake of dry pigment set into a slab.
> Colour: **deep forest green, `#2A7A3E`**. Strong, full, unmistakable colour —
> not pale, not pastel, not washed out, not translucent. Dead flat and
> chalk-matte: no gloss, no glass, no enamel, no varnish, no specular
> highlight, no reflection, no gemstone. A clean pale rim of bare stone runs
> around it. It is the only saturated thing on the card and it is **empty —
> no symbol, no numeral, no mark inside it**.
>
> **The mineral veins running through the quartz carry the faintest trace of
> that same green** — a whisper of it in the stone, at perhaps 10%
> strength, nothing like the disc. The rest of the slab stays grey-white.
>
> **A single fine chiselled groove runs horizontally across the card below
> the top zone**, a divider rule cut into the stone rather than drawn on it —
> V-grooved, catching light along one edge, with faint chalk setting-out
> marks still visible under the cut and slightly out of true with it. One
> line only, tinted very faintly green where pigment has worked into
> the cut.
>
> **A narrow chiselled border line** runs just inside the card edge on all
> four sides, the same cut character, thin and even, framing the face without
> decorating it.
>
> **The centre and lower two-thirds of the card are open, flat, undecorated
> stone** — clean enough to print twelve lines of small text on. Keep this
> area almost entirely empty. Permitted here, and only whisper-faint at
> 8–12% contrast: a ghost of survey linework, a fragment of a bearing arc, a
> trace of contour hatching, a pale water-stain. Nothing with an edge hard
> enough to be mistaken for a letter.
>
> Style: hand-drafted antique cartography crossed with architectural stone
> rubbing. Restrained, precise, austere, and mostly empty by design. Matte,
> printable, high detail, flat lighting.

**Negative / must not appear:**

> no text, no letters, no numerals, no words, no runes, no readable script,
> no calligraphy, no labels, no signature, no watermark, no gibberish
> lettering anywhere; nothing inside the coloured disc; no second disc; no
> people, no faces, no creatures, no weapons, no armour; no landscape, no
> scenery, no sky, no water, no trees, no buildings; no torn or deckled
> edge, no pins, no tape; no ornate border, no scrollwork, no filigree, no
> corner flourishes, no card frame, no banner or ribbon shapes; no
> illustration window or art box; no glow, no sparkle, no gradient wash; no
> clutter anywhere in the lower two-thirds.

---

## 4. Neutral Card Face — art only, no text

> A blank playing-card face, portrait 5:7, in the style of an antique
> survey-atlas plate. **Clean rectangular edges, perfectly square corners,
> full bleed to the edge** — no torn paper, no deckle, no burn marks, no
> pins, no tape, no lifted corners, no drop shadow, no frame around a frame.
>
> **The surface is pale grey-white quartz stone**, finely worked flat: a
> smooth slab with faint mineral veining, a hairline crack or two, and the
> soft tonal unevenness of real stone. Weathered and matte, like something
> handled for years. Bone, chalk and weathered parchment throughout. Flat
> overcast light, no sun anywhere, no shadow direction, no gloss.
>
> **A single circular disc of solid matte pigment sits in the upper right
> corner**, inset into the stone like a cake of dry pigment set into a slab.
> Colour: **neutral slate grey, `#5A5A5A`**. Strong, full, unmistakable colour —
> not pale, not pastel, not washed out, not translucent. Dead flat and
> chalk-matte: no gloss, no glass, no enamel, no varnish, no specular
> highlight, no reflection, no gemstone. A clean pale rim of bare stone runs
> around it. It is the only saturated thing on the card and it is **empty —
> no symbol, no numeral, no mark inside it**.
>
> **The mineral veins running through the quartz carry the faintest trace of
> that same grey** — a whisper of it in the stone, at perhaps 10%
> strength, nothing like the disc. The rest of the slab stays grey-white.
>
> **A single fine chiselled groove runs horizontally across the card below
> the top zone**, a divider rule cut into the stone rather than drawn on it —
> V-grooved, catching light along one edge, with faint chalk setting-out
> marks still visible under the cut and slightly out of true with it. One
> line only, tinted very faintly grey where pigment has worked into
> the cut.
>
> **A narrow chiselled border line** runs just inside the card edge on all
> four sides, the same cut character, thin and even, framing the face without
> decorating it.
>
> **The centre and lower two-thirds of the card are open, flat, undecorated
> stone** — clean enough to print twelve lines of small text on. Keep this
> area almost entirely empty. Permitted here, and only whisper-faint at
> 8–12% contrast: a ghost of survey linework, a fragment of a bearing arc, a
> trace of contour hatching, a pale water-stain. Nothing with an edge hard
> enough to be mistaken for a letter.
>
> Style: hand-drafted antique cartography crossed with architectural stone
> rubbing. Restrained, precise, austere, and mostly empty by design. Matte,
> printable, high detail, flat lighting.

**Negative / must not appear:**

> no text, no letters, no numerals, no words, no runes, no readable script,
> no calligraphy, no labels, no signature, no watermark, no gibberish
> lettering anywhere; nothing inside the coloured disc; no second disc; no
> people, no faces, no creatures, no weapons, no armour; no landscape, no
> scenery, no sky, no water, no trees, no buildings; no torn or deckled
> edge, no pins, no tape; no ornate border, no scrollwork, no filigree, no
> corner flourishes, no card frame, no banner or ribbon shapes; no
> illustration window or art box; no glow, no sparkle, no gradient wash; no
> clutter anywhere in the lower two-thirds.

---

## 5. The Card Fields (text pass over the finished face)

Run this on the output of any of the four face prompts, once each. Nothing here is a real card — this pass
produces an **empty template**, with the field labels printed and the value
beside each one left blank for typesetting later.

> Take the supplied card face and add printed annotation in fine sepia-black
> ink, in the style of an engraved atlas plate. Type sits *on* the stone with
> the faint background showing through unchanged. Nothing is boxed or
> panelled, and the coloured disc stays completely empty.
>
> **Top zone, above the chiselled divider, left-aligned, clear of the disc:**
> a wide empty ruled line for the card's name, set large — this is the
> biggest text zone on the card. Directly beneath it, a second much smaller
> empty ruled line, about half the width.
>
> **Below the divider, a column of four label rows**, evenly spaced, each a
> small label in spaced capitals at the left with a generous blank area
> beside and below it for text to be set into. Top to bottom the labels read:
> `ATTACK`, `EFFECT`, `DEFENSE`, `RANGE`. Leave the largest blank space after
> EFFECT and DEFENSE, which carry the most text. (A handful of cards also
> carry a SPECIAL row; it is rare enough that the blank template does not
> reserve one, and it gets set in when a card needs it.) Labels are small, muted and
> secondary — they should sit quieter than the blank space they introduce.
>
> **At the very bottom, a narrow band** set apart by a little extra space
> above it, holding two short empty ruled lines for a line of quoted italic
> text.
>
> Keep the labels crisp, plain and readable — **an engraved small-capital
> serif, sober and legible, not calligraphic.** No swash capitals, no
> spiralling flourishes, no scrollwork. This is a printed card, not a
> hand-lettered page, and everything on it has to stay readable at thumbnail
> size in a player's hand.

**Must not appear in the text pass:**

> no numerals, digits or numbers anywhere; no sample or placeholder card
> name, rules text or flavour text — every value area is blank; no swash
> capitals, no flourishes, no scrollwork, no calligraphy; no keyword names,
> no stat names, no colour names; no mana symbols, no icons, no pips, no set
> symbol, no rarity mark, no collector number; no illustration; no change to
> the coloured disc.

---

<!-- Maintenance only — not part of either prompt, do not paste. -->
<!-- 5:7 is the printed card at 60 x 84mm; the 3x3 page grid, field order, -->
<!-- labels and the four colour hexes all come from generate-cards.py. -->
