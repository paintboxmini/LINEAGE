#!/usr/bin/env python3
"""Generate the card stock textures — one RGBA PNG per card colour.

Both the paper grain and the colour wash are baked into a single image on
purpose, and that is not an optimisation. A CSS gradient becomes a PDF
tiling pattern when Chrome prints it, and most PDF viewers draw a hairline
at every pattern cell boundary — which is exactly the faint vertical and
horizontal lines that showed up across the first styled card sheet.
Measured on one 9-card page: with the radial-gradient wash, 9 tiling
patterns and 18 shadings; with the wash baked into this image instead,
zero and zero.

The grain must not be a repeating CSS background either, for the same
reason: background-repeat is a tiling pattern too. One image per card,
drawn once, stretched to the card. No repeat, no gradient, no blend mode.

Output is ~150 dpi at 60x84mm, which is plenty for noise — the type stays
live vector at full printer resolution regardless.

Usage: python3 make-grain.py        (writes assets/grain-<colour>.png)
"""

import math
import os
import random
import struct
import zlib

W, H = 360, 504          # 5:7, the card's own ratio
WASH = 0.42              # colour strength at the top of the card
REACH = 0.72             # how far down the card the colour carries
COLOURS = {
    'red':       ((158, 44, 44), 5),
    'blue':      ((44, 95, 158), 6),
    'green':     ((42, 122, 62), 7),
    'colorless': ((90, 90, 90), 8),
}


def chunk(tag, data):
    c = tag + data
    return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c))


def stock(rgb, seed):
    random.seed(seed)
    noise = [[random.randint(0, 255) for _ in range(W)] for _ in range(H)]
    r, g, b = rgb
    rows = bytearray()
    for y in range(H):
        rows.append(0)                       # PNG filter byte: none
        for x in range(W):
            # a 3-tap blur so it reads as paper fibre rather than static
            v = (noise[y][x] + noise[y][(x + 1) % W] + noise[(y + 1) % H][x]) // 3
            # Colour falloff from the top centre, strongest at the title.
            # WASH and REACH were picked by rendering .17/.62, .30/.62,
            # .42/.72 and .55/.80 side by side across all three hues: .17 was
            # too faint to read as tinted stock, and at .55 the small-caps
            # stat label starts losing contrast against its own ground on
            # blue and green. .42 is as strong as this can go while the body
            # text still sits on light paper.
            dx = (x - W / 2) / (W * REACH)
            dy = y / (H * REACH * 1.29)
            wash = max(0.0, 1.0 - math.sqrt(dx * dx + dy * dy)) ** 1.5
            grain = (v / 255) * 0.10
            alpha = int(255 * min(0.95, wash * WASH + grain))
            # where the wash dominates use the card hue; where the grain
            # dominates use a neutral warm grey, so texture never tints
            m = wash * WASH / (wash * WASH + grain + 1e-6)
            rows += bytes((int(r * m + 90 * (1 - m)),
                           int(g * m + 80 * (1 - m)),
                           int(b * m + 70 * (1 - m)),
                           alpha))
    return (b'\x89PNG\r\n\x1a\n'
            + chunk(b'IHDR', struct.pack('>IIBBBBB', W, H, 8, 6, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(bytes(rows), 9))
            + chunk(b'IEND', b''))


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.makedirs('assets', exist_ok=True)
    print('Generating card stock textures...')
    for name, (rgb, seed) in COLOURS.items():
        png = stock(rgb, seed)
        path = f'assets/grain-{name}.png'
        with open(path, 'wb') as f:
            f.write(png)
        print(f'  {path}  {len(png) / 1024:.0f} KB  ({W}x{H})')
