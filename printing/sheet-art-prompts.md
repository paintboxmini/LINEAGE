# Character Sheet — Art Prompts

Two prompts, run in order. The first makes the plate with no lettering on it
at all; the second lays type over the finished plate. Splitting them is a
working method for AI art, and it happens to be how the world already works:
*"An atlas page is one recorded image with writing around it… The image is the
observation. The margins are the argument about what it means. The images fade.
The writing doesn't."* (`factions-and-races/the-cartographers-guild.md`, Methods.)
An atlas plate and its marginalia are made in two passes by two different hands.
So is this.

**Canvas:** 3:5 portrait, to match the printed sheet
(`printing/generate-sheets.py`, 76.2 × 127 mm). Render at least 1200 × 2000.

**The three colours are fixed** — they are the card colours, so a sheet and a
hand of cards have to agree: deep red `#9E2C2C`, deep blue `#2C5F9E`, deep
green `#2A7A3E` (`printing/generate-cards.py`, COLOR_HEX).

---

## Prompt 1 — The Plate (art only, no text)

> A vertical parchment plate in the style of an old survey atlas, portrait
> 3:5. The upper two-thirds is dominated by a single large equilateral
> triangle, point up, drawn as if **chiselled into pale grey-white quartz
> stone** — cut, not painted. The cut lines are V-grooved and catch light
> along one edge the way real chisel work does. Faint chalk-and-string
> setting-out marks are still visible under the cut, slightly out of true
> with it, as though the mark was laid first and the chisel followed. Some
> stretches of the groove are cut wide and shallow, others thin and deep, and
> the thin deep passages look older and sharper while the wide ones look worn
> and nearly faded out. Recut lines overlap older faded lines.
>
> At each of the three corners of the triangle sits a **filled circular well**,
> like a shallow bowl ground into the stone and flooded with pigment. Three
> colours, one per corner, unlabelled and unmarked: deep blood red `#9E2C2C`
> at the top corner, deep ink blue `#2C5F9E` at the bottom-left corner, deep
> forest green `#2A7A3E` at the bottom-right corner. Each well has a clean
> pale rim of bare stone around it, is flat and even in the centre with a
> soft inner shadow, and is **empty — no symbol, no numeral, no mark of any
> kind inside it**. The wells are the brightest, most saturated things in the
> picture; everything else is desaturated.
>
> The triangle's interior is **open, flat, undecorated stone** — clean enough
> to write four short lines on. Only the faintest surface texture: a hairline
> vein or two of mineral colour in the quartz, nothing that competes.
>
> Behind and around the triangle, a **grey sea occupies the outer margins** —
> flat, hazy, colourless water without horizon, waves without insistence,
> fading at the very edges of the plate into an unresolved blur where detail
> stops being detail. It is not stormy and not threatening. It is simply
> unmeaning, and the stone is holding it off. Where the grey comes nearest to
> the chiselled lines it thins out and recedes.
>
> The **lower third of the plate is a broad open field of the same pale
> stone** for writing on — a worked flat surface, lightly toned, with subtle
> background art living *underneath* it at low contrast: ghosted survey
> linework, faint bearing arcs and a fragment of a compass rose, contour
> hatching, a squared mason's post or two standing along the bottom edge, a
> pale water-stain and a fold crease. All of it whisper-faint, 10–15%
> contrast against the stone, so type laid on top stays perfectly legible.
> Leave the horizontal centre band of this lower field the cleanest.
>
> Palette: bone, chalk, wet slate, weathered parchment, cold grey-green sea.
> Light is flat and overcast with no sun anywhere — the world has no sun.
> Feels like a page from a surveyor's field atlas that has been carried in a
> satchel for twenty years: handled, creased, slightly foxed at the corners.
>
> Style: hand-drafted antique cartography crossed with architectural stone
> rubbing. Fine ink linework, restrained, precise, a little austere. Muted
> and weathered except for the three colour wells. Matte, printable, high
> detail, flat lighting, no gloss, no glow, no magic sparkle, no fantasy
> kitsch.

**Negative / must not appear:**

> no text, no letters, no numerals, no words, no runes, no readable script,
> no calligraphy, no labels, no signatures, no watermark, no title, no
> gibberish lettering anywhere in the image; nothing written inside the
> coloured circles; no fourth circle; no people, no faces, no creatures, no
> weapons, no armour, no shields; no sun, no moon, no stars, no bright sky;
> no glow, no neon, no lens flare, no rainbow; no borders made of type; no
> UI elements, no icons, no arrows; no clutter in the lower third.

**Why these pieces:** the triangle is chiselled rather than drawn because
Masons cut glyphs with chisels and never draw them, and the chalk-and-string
marks are the step before the chisel touches stone; the wide-shallow versus
thin-deep grooves are the order's real tradeoff, strong-and-fading against
lasting-and-weaker; the recut-over-faded lines are the maintenance rotation,
which is the whole job (`factions-and-races/the-masons.md`). The three
triangle edges are the three sustained wounds that hold a thing in
existence — Name, Price, Distance — which is why the grooves must read as
*cut and still open*, never as healed or decorative
(`world/creation-myth-the-three-cuts.md`). The grey margin sea is the Unheld:
not chaos and not malice, just unmeaning pressing on the edge of anything held
(`world/the-unheld.md`). And the whole plate is an atlas page — image in the
middle, room for the argument around it.

---

## Prompt 2 — The Marginalia (text pass over the finished plate)

Run this on the output of Prompt 1. Every value below is **written by the
player at the table**, so the type pass places *labels and ruled lines*,
never sample values — the only exception is the small hint text under Price.

> Take the supplied plate and add hand-lettered annotation in the style of a
> surveyor's field atlas: fine sepia-black ink, an antique engraved serif for
> labels, small caps for the label words, slightly irregular baselines as if
> written by hand with a steel nib. Type sits *on* the stone, following its
> surface, with the faint background art showing through unchanged beneath.
> Nothing is boxed or panelled. No new artwork, no new symbols, no change to
> the triangle or the three coloured circles.
>
> **Across the very top, above the triangle:** two ruled write-in lines, one
> under the other, full width. The first is labelled `NAME` in small caps at
> its left end; the second is labelled `RACE`. Labels are small and grey; the
> ruled lines are thin, long and empty.
>
> **Inside the triangle, centred in its open interior:** four short labelled
> slots stacked as two rows of two, small and evenly spaced, each a tiny
> label in small caps above a short blank rule. They read `MAX HP`, `HAND`,
> `INIT`, `DECK MAX`. Keep them well clear of the three corner circles and
> well inside the cut edges. These are the only marks allowed inside the
> triangle.
>
> **The three coloured circles stay completely empty** — no label, no number,
> no outline change. A number gets written into each by hand later.
>
> **In the lower field, below the triangle, in this order, top to bottom:**
> a section heading `TRAIT` in small caps with a thin rule under the heading,
> then one long empty write-in line beneath it;
> a section heading `SKILLS`, then two long empty write-in lines beneath it,
> each with a small numeral `1` and `2` at its left end;
> a section heading `PRICE`, followed immediately on the same line by small
> italic hint text reading exactly
> `I never / I must / I always / I cannot / Once I / Whenever`,
> then six long empty ruled lines filling the remaining space to the bottom
> margin.
>
> Keep generous even spacing. Leave a clear margin all around. The written
> lines must be long, unbroken and genuinely empty — this is a form to be
> filled in with a pen, not a finished page.

**Must not appear in the text pass:**

> no equipment, weapon, armour or artifact section; no inventory; no stat
> names anywhere — never write Body, Mind or Soul, and never label the
> circles; no sample or placeholder values in any field; no numbers except
> the small `1` and `2` beside the two skill lines; no extra sections, no
> flavour text, no page number, no title, no signature, no logo.

**Why no equipment:** gear lives on cards, not on the sheet
(`rules/character-creation.md`, Equipment — only equipped items grant
mechanical effects, and the items themselves are their own objects).

**Why the stats are unlabelled:** the three colours already say it. Red is
Body, blue is Mind, green is Soul everywhere else in the game, and a player
holding a red card learns the mapping in one hand of play
(`rules/cards.md`, What Each Colour Tends Toward).
