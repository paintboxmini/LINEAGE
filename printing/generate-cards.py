#!/usr/bin/env python3
"""Generate a print-ready HTML card sheet from core card files.
Cards are 60mm x 84mm (slightly under Magic card size) to fit in sleeves.
Layout: 3x3 per Letter page, exactly 9 cards per page.

Usage:
  python3 generate-cards.py              → core cards  (card-print-core.html)
  python3 generate-cards.py briarwatch  → Briarwatch encounter set
  python3 generate-cards.py items       → player item cards
  python3 generate-cards.py oracle-1     → one even third of the Oracle
  python3 generate-cards.py <set-name>  → any named set below

Print settings: Margins = None, Background graphics = On, Scale = 100%.
"""

import re
import collections
import html as html_mod
import os
import sys

# ---------------------------------------------------------------------------
# Card sets — add new encounter sets here
# ---------------------------------------------------------------------------
#
# What the Oracle deck may not contain (`rules/cards.md`, The Oracle Deck):
# nothing that reaches into an enemy's hand, deck, or stats directly. No hand
# reveal, no forcing an enemy to discard, no inserting status cards into their
# deck or hand, no manipulating their deck, no stat reduction, and nothing
# Sealed. Staggered is out too: it eats a whole attack or a whole defence,
# which is too large a swing to hand a starting deck freely. Red keeps one
# card that inflicts it, OFF BALANCE, and only on a clean win.
#
# Acting on your own hand or deck is fine, and so is control that operates
# on the board — statuses, positioning, initiative, targeting restrictions. Check a candidate against that list before adding it here; the
# starting deck is where a new player learns what the game is, and reaching
# into someone else's resources is not it.

SETS = {
    'core': {
        'title': 'Core Cards',
        'files': [
            '../cards/blue-mind.md',
            '../cards/red-body.md',
            '../cards/green-soul.md',
            '../cards/colorless.md',
        ],
    },
    'briarwatch': {
        'title': 'Briarwatch Encounter Set',
        'files': [
            '../cards/briarwatch-jackalope.md',
            '../cards/tollbird.md',
            '../cards/briar-scratcher.md',
            '../cards/borrower-hollow.md',
            '../cards/stonecoil-hollow.md',
            '../cards/delve-roller-hollow.md',
        ],
    },
    'items': {
        'title': 'Items',
        'type': 'items',
        'files': [
            '../items/consumables.md',
            '../items/briarwatch-items.md',
            '../items/vultures-nest-items.md',
        ],
    },
    'items-field': {
        'title': 'Hollow and Weald Items',
        'type': 'items',
        'files': [
            '../items/hollow-and-weald-items.md',
        ],
    },
    'mason': {
        'title': 'Mason Glyphs',
        'files': [
            '../cards/mason-glyphs.md',
        ],
    },
    'washed-ashore': {
        'title': 'Washed Ashore Encounter Set',
        'files': [
            '../cards/wrackclaw.md',
            '../cards/hullback.md',
            '../cards/trisect-ashfall.md',
        ],
    },
    'oracle': {
        'title': 'Oracle Deck',
        'files': [
            '../cards/red-body.md',
            '../cards/blue-mind.md',
            '../cards/green-soul.md',
        ],
        # This list is the Oracle deck's definition. It used to be a copy of
        # one, kept in step with an Oracle/ directory and a content.py that no
        # longer exist — both were cited here until 2026-09-12, long after they
        # were gone. Nothing else defines the 63 now; edit them here.
        # Fixed composition since 2026-08-03: 21 per colour, each
        # led by that colour's own range identity. The ideal split is 12/6/3
        # and all three colours are on it; the per-colour notes below say
        # which slots each change spent.
        'cards': [
            # Red (21) — melee 12 / both 6 / ranged 3, back on the ideal
            # split after the 2026-09-06 pass. GORE swapped for INTERCEPT
            # 2026-08-03 — see content.py — and INTERCEPT has since been
            # folded into GUARD and cut.
            #   renamed: CLIFF SONG -> HEALING SONG (also Both -> Ranged),
            #            RECOVER -> SECOND WIND
            #   out:     INTERCEPT (cut), BLEED, STAUNCH
            #   in:      OFF BALANCE + CLOSE IN (melee),
            #            CERTAIN STRIKE (ranged)
            #   RATTLE out with the Staggered ban, TRAMPLE in (both melee).
            #   OFF BALANCE keeps Staggered, gated to a clean win — the one
            #   card in the deck allowed to inflict it.
            # Three in for three out: INTERCEPT's cut left the colour at 20,
            # so the two named replacements needed a third. CLOSE IN is it,
            # and it is the only Oracle card that teaches Rushdown.
            # 2026-09-07, the Deadly pass: Red had no way to raise its own
            # damage anywhere in the deck — every effect was a status, a heal,
            # a move, or a defensive gain, so the colour of raw damage
            # expressed that only through die size.
            #   out: HEALING SONG (reworked Green — see Green below),
            #        ENDURE (flat 'Gain Resist' at d8 Melee; Red still holds
            #        five Resist cards without it)
            #   in:  RETALIATE (melee, d8 — same die and range as ENDURE, so
            #        the swap is neutral on the die spread),
            #        SHARPEN (ranged — reworked Both -> Ranged to keep the
            #        3 ranged slots HEALING SONG's departure would have cost)
            'ATTRITION', 'BLINDSIDE', 'GUARD', 'OFF BALANCE', 'OPEN GUARD',
            'PAIN IS FUEL', 'PUSH', 'TRAMPLE', 'UNBROKEN', 'WEATHERED',
            'CLOSE IN', 'RETALIATE',
            'CHARGE', 'FOOTWORK', 'GROUNDING STANCE', 'PULL', 'SECOND WIND',
            'SLIP THE BLADE',
            'CERTAIN STRIKE', 'STARING CONTEST', 'SHARPEN',
            # Blue (21) — ranged 12 / melee 6 / both 3, on the ideal split.
            # 2026-09-06, in two passes. First: PREDICT (melee, cut with the
            # Sealed keyword) -> DISTRACT, and PROFILE (ranged, read the
            # attacker's hand) -> PARTITION. Then the blue balance pass:
            #   renamed: TELL -> UNDERMINE -> DOUBT -> ENFEEBLE (also
            #            Melee -> Ranged),
            #            DEAD END -> PINNED, FORESEEN -> FORESEE,
            #            SECOND GUESS -> FALTER
            #   out:     HESITATE and FALTER (both cut — FALTER with the
            #            Staggered ban), TURN, EXPOSED, RETORT,
            #            SHARPEN (moved to Red, where the card always belonged)
            #   in:      INTERRUPT + REBUTTAL + CLIMB (melee),
            #            CALLED SHOT (ranged), STILL POINT (both)
            # See the Oracle content rule above the SETS table.
            'AXIOM', 'CALCULATE', 'PINNED', 'FOCUS', 'FORESEE',
            'LAST RESORT', 'MARKED', 'PARTITION', 'CALLED SHOT', 'STILL POINT',
            'STUDY', 'VEIL', 'ANTICIPATE', 'DEFLECT', 'INTERRUPT', 'ENFEEBLE',
            'CLIMB', 'REALIGNMENT', 'REBUTTAL', 'SIDESTEP', 'DISTRACT',
            # Green (21) — both 12 / ranged 6 / melee 3, back on the ideal
            # split. OPENING moved Melee to Both on 2026-09-06, taking Green
            # off it; the green pass put it back by swapping GIVE WAY (both)
            # for TWIN STRIKE (melee).
            #   renamed: YOU'RE NEXT -> PRIORITY
            #   out:     GIVE WAY — Evade at d4 Both, the same die and range
            #            as Blue's SIDESTEP, which at least differentiates
            #            its defence half
            #   in:      TWIN STRIKE — the only damage-focused card in
            #            Green's 21, and the crossover the colour rules bless
            #   TOPPLE out with the Staggered ban, AID in (both ranged).
            # DUST renamed SMOKESCREEN 2026-08-26. SETTLE was renamed BRACE
            # the same day, onto a name Red already used; that duplicate was
            # cut 2026-09-06 as a twin of ABIDE, which takes its slot
            # here — see experimental/archives/cut-cards.md.
            # 2026-09-07, the Deadly pass: all three of Green's Deadly cards
            # handed it to someone else, two of them on the defense half, so
            # Deadly read as a Green support buff rather than a damage tool.
            # Two go, and Red picks the keyword up.
            #   out: RESONATE + SUPPORT (Deadly; COMMUNION stays because it is
            #        the deck's only Green Scry, and its Deadly is defensive),
            #        TWIN STRIKE (melee), ABIDE (flat 'Gain Resist' at
            #        d4 Both — Resist was the deck's most-represented keyword)
            #   in:  PATIENCE (Anchored — the deck had two Anchored cards and
            #        both were 'passive at start of your turn'; its attack half
            #        also backfills the damage option TWIN STRIKE took away),
            #        FLOW (Evade — Green had none, and this is Green's only d8
            #        anywhere in the 21), MEND (melee support, which Green's
            #        three melee slots had none of), HEALING SONG (reworked
            #        from Red, where the damage colour was out-healing the
            #        support colour in its own starting deck)
            # 2026-09-08, Drew's hand pass over the printed Green sheet.
            #   renamed: ACCEPTANCE -> RELEASE (it read as a state of mind
            #            rather than an action a card can take),
            #            DEAD RECKONING -> DISORIENT (the old name described
            #            what the caster does, not what the target suffers)
            #   swapped: SWAY -> SHADE AWAY. SWAY's rewrite made it the third
            #            identical 'Gain Evade' card at d4 Both; the three
            #            collapsed to one and SHADE AWAY took the slot.
            #   out:     UNTOUCHED — this is the one place the pass leaves a
            #            hole: it was Green's rung on the Immunity ladder
            #            (UNBROKEN / LAST RESORT / UNTOUCHED, `rules/cards.md`),
            #            so the Oracle now teaches Immunity in Red and Blue
            #            only. The card is untouched in the pool.
            #   in:      BRISTLE — MEND moved Melee -> Both in the same pass,
            #            which would have left Green with two melee cards and
            #            both of them control. BOLSTER held this slot from
            #            2026-09-08 until 2026-09-09, when BRISTLE took it:
            #            hackles going up fits Pat's Shunka where a thorn
            #            bush does not, and BRAMBLE covers Green's Thorns at
            #            Both range anyway.
            'RELEASE', 'BRAMBLE', 'INSTINCT', 'LEVEL THE FIELD',
            'MIRROR STEP', 'QUICKEN', 'RENEWAL', 'SHADE AWAY', 'PRIORITY',
            'OPENING', 'PATIENCE', 'MEND',
            'AID', 'COMMUNION', 'DISORIENT', 'MOCKERY', 'HEALING SONG',
            'FLOW',
            'BIND', 'SMOKESCREEN', 'BRISTLE',
        ],
    },
    # The Oracle's 63 dealt into three 21-card sheets, each an even share of
    # both colour and range. Derived from 'oracle' rather than listed by hand:
    # the composition above is edited often, and a hand-copied third would go
    # stale the first time a card was swapped without anyone noticing which
    # sheet it had been sitting on.
    #
    # Each third comes out 7 Red / 7 Blue / 7 Green AND 7 Melee / 7 Ranged /
    # 7 Both, both at once. That is not a coincidence to be proud of — it
    # falls out of the deck's own shape. Every colour is 21 at 12/6/3, so
    # every (colour, range) bucket in the deck is 12, 6 or 3, and all three
    # divide by three. Deal each bucket round-robin and both axes land even
    # together. Break the 12/6/3 ratio and the thirds stop being exact; the
    # build says so rather than printing a lopsided sheet quietly.
    'oracle-1': {
        'title': 'Oracle Deck — 1 of 3',
        'split': ('oracle', 3, 0),
    },
    'oracle-2': {
        'title': 'Oracle Deck — 2 of 3',
        'split': ('oracle', 3, 1),
    },
    'oracle-3': {
        'title': 'Oracle Deck — 3 of 3',
        'split': ('oracle', 3, 2),
    },
    'oracle-expansion': {
        'title': 'Oracle Deck — Expansion',
        'files': [
            '../cards/red-body.md',
            '../cards/blue-mind.md',
            '../cards/green-soul.md',
        ],
        # The second 21, chosen 2026-09-08. Printed on its own so the first
        # 63 don't have to be re-read to review it; together the two sets
        # are the Oracle's 84, and the content rule above covers both.
        #
        # Drawn from the core lists rather than written fresh — every card
        # here already existed on the bench. Same shape as the first 21 at
        # one third the size: 7 per colour at 4/2/1 in that colour's range
        # identity, holding each colour on the 12/6/3 ratio across all 28.
        #
        # Four cards needed rebalancing to qualify, all in `cards/`:
        #   UNNAME  — its defence half forced a random discard. Now mirrors
        #             the attack half: the attacker's Effect does not fire.
        #   FORGET  — its attack half forced a discard. Now mirrors its own
        #             legal defence half, exiling the played card on a clean
        #             win, which is what the card was always about.
        #   PROFILE — its defence half read the attacker's hand. Now a
        #             smaller version of its own attack half.
        #   CONSUME — destroying a card out of your own hand was mandatory,
        #             which is a trap in a starting deck. Now "you may".
        # The first three were barred by the content rule, and they were
        # Blue's ONLY three melee bench cards — without the rewrites Blue
        # could not have filled its two melee slots from the pool at all.
        #
        # What the 21 were chosen to fill, measured against the first set:
        #   Exile, Lifesteal and Unpreventable were all at 0 in the Oracle
        #     while living in the pool — BURN BRIGHT and FORGET, PARADOX and
        #     CONSUME, SPARK OF VIOLENCE.
        #   Scry was at 3 and three more were asked for: UNDERSTANDING,
        #     PROFILE, ALIGN. All Blue, because no Green or Red bench card
        #     has ever carried Scry.
        #   Blue had no d8 anywhere: UNDERSTANDING is the only one on the
        #     bench and it is a Scry card, so it answers both at once.
        #   Protect sat at 1 card for a mechanic with its own Damage
        #     Pipeline step: SHARED BURDEN.
        #   Immunity lost its Green rung when UNTOUCHED left the first 21.
        #     UNTOUCHED comes back here, which restores the ladder without
        #     spending a slot in the deck Drew is happy with.
        #   Green had no Weak: CONSUME. Green had one d8: SHARED BURDEN and
        #     HEAVE AND HAUL make three.
        #
        # 2026-09-09, the colour-identity pass: WAITING GAME moved Red ->
        # Blue (stealing and copying enemy buffs is enemy control), so it
        # moved from the Red block to the Blue one and took SLIPSTREAM's
        # Both slot — the expansion keeps its Positive Status Effects
        # teacher either way. PROVOKE, which moved Green -> Red the same
        # day, fills the Red Both slot it vacated.
        #   Green forced enemy movement died with SWAY: HEAVE AND HAUL.
        #   Red had no Rooted: GRAPPLE, which is also the card the glossary
        #     cites to explain Anchored holding Rooted open.
        #
        # Not fillable from the bench: Green has no Counter Attack card
        # anywhere in the core pool, so that gap survives this expansion.
        'cards': [
            # Red (7) — melee 4 / both 2 / ranged 1
            'SPARK OF VIOLENCE', 'GRAPPLE', 'DOUBLE DOWN', "GAMBLER'S RUIN",
            'BLOOD TITHE', 'PROVOKE',
            'BURN BRIGHT',
            # Blue (7) — ranged 4 / melee 2 / both 1
            'UNDERSTANDING', 'PARADOX', 'PROFILE', 'ALIGN',
            'UNNAME', 'FORGET',
            'WAITING GAME',
            # Green (7) — both 4 / ranged 2 / melee 1
            'SHARED BURDEN', 'HEAVE AND HAUL', 'ROOTED OATH', 'UNTOUCHED',
            'GUIDE', 'FIELD MEDICINE',
            'CONSUME',
        ],
    },
}

# ---------------------------------------------------------------------------

COLOR_HEX = {
    'BLUE':      '#2C5F9E',
    'RED':       '#9E2C2C',
    'GREEN':     '#2A7A3E',
    'COLORLESS': '#5A5A5A',
}

COLOR_BG = {
    'BLUE':      '#F0F4FA',
    'RED':       '#FAF0F0',
    'GREEN':     '#F0F7F2',
    'COLORLESS': '#F2F2F2',
}

COLOR_LABEL = {
    'BLUE':      'Mind',
    'RED':       'Body',
    'GREEN':     'Soul',
    'COLORLESS': 'Colorless',
}

ITEM_HEX = '#7A5C10'
ITEM_BG  = '#FBF8F0'

CARDS_PER_PAGE = 9


def parse_cards(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    cards = []
    blocks = re.split(r'\n---\n', content)

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # Header LINES are skipped below, but the block is not: a card that
        # follows a "## Creature" heading with no --- between them shares the
        # heading's block, and skipping the whole block silently dropped it
        # from the sheet. That is how four briarbundles cards went unprinted.
        # A block with no name-and-colour is rejected at the end anyway, so
        # the file's own title block still costs nothing.
        card = {}
        lines = [l.strip() for l in block.split('\n')
                 if l.strip() and not l.strip().startswith('#')]

        for line in lines:
            m = re.match(r'^\*\*(.+?)\*\*$', line)
            if m and 'name' not in card:
                card['name'] = m.group(1)
                continue

            m = re.match(r'^(BLUE|RED|GREEN)\s*[—\-]+\s*(.+)$', line)
            if m:
                card['color'] = m.group(1)
                stat_part = re.split(r'\s*[—\-]+\s*', m.group(2))[0]
                card['stat'] = stat_part.strip()
                continue

            if line == 'COLORLESS':
                card['color'] = 'COLORLESS'
                continue

            if line.startswith('Attack:'):
                card['attack'] = line[7:].strip()
            elif line.startswith('Special Rule:'):
                card['special_rule'] = line[13:].strip()
            elif line.startswith('Effect:'):
                card['effect'] = line[7:].strip()
            elif line.startswith('Defense Effect:'):
                card['defense_effect'] = line[15:].strip()
            elif line.startswith('Range:'):
                card['range'] = line[6:].strip()
            else:
                m = re.match(r'^\*"(.+)"\*$', line)
                if m:
                    card['flavor'] = m.group(1)

        if card.get('name') and card.get('color'):
            cards.append(card)

    return cards


def parse_items(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    items = []
    blocks = re.split(r'\n---\n', content)

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        item = {'_type': 'item'}
        lines = [l.strip() for l in block.split('\n') if l.strip()]

        for line in lines:
            # Skip markdown section headers
            if line.startswith('#'):
                continue

            # Name: **ITEM NAME**
            m = re.match(r'^\*\*(.+?)\*\*$', line)
            if m and 'name' not in item:
                item['name'] = m.group(1)
                continue

            # Only process further once we have a name
            if 'name' not in item:
                continue

            # Italic lines: type descriptor or source (skip source)
            m = re.match(r'^\*(.+)\*$', line)
            if m:
                inner = m.group(1)
                if inner.startswith('Source:'):
                    continue
                if 'type' not in item:
                    item['type'] = inner
                continue

            # Everything else is effect text
            item.setdefault('effect_lines', []).append(line)

        if item.get('name'):
            items.append(item)

    return items


def split_evenly(cards, parts, index):
    """Deal `cards` into `parts` shares even on colour and range at once,
    and return share number `index`.

    Dealing bucket by bucket is what makes both axes come out even together.
    Balancing colour and then balancing range inside it is the obvious
    approach and it fights itself; bucketing on the pair and dealing each
    bucket round-robin means every share takes a proportional slice of each
    (colour, range) combination, and the colour totals and range totals fall
    out of that rather than being negotiated against each other.

    A bucket that does not divide by `parts` splits as evenly as it can —
    the remainder lands in the low-numbered shares. Callers report the
    residue rather than hiding it: an uneven sheet is a fine thing to print
    and a bad thing to be surprised by.

    Original order is preserved within each share, so a part keeps the
    parent's colour grouping and reads the same way down the page.
    """
    buckets = {}
    for i, card in enumerate(cards):
        buckets.setdefault((card['color'], card['range']), []).append(i)
    keep = set()
    for idxs in buckets.values():
        keep.update(idxs[index::parts])
    return [c for i, c in enumerate(cards) if i in keep]


def split_residue(cards, parts):
    """(colour, range) buckets of `cards` that don't divide by `parts`, as
    a list of 'RED Melee 13' strings. Empty means every share is exact."""
    buckets = {}
    for card in cards:
        key = (card['color'], card['range'])
        buckets[key] = buckets.get(key, 0) + 1
    return [f'{col} {rng} {n}' for (col, rng), n in sorted(buckets.items())
            if n % parts]


def load_set(set_name):
    cfg = SETS[set_name]

    # A split set has no files of its own — it is a share of another set.
    if 'split' in cfg:
        parent, parts, index = cfg['split']
        return split_evenly(load_set(parent), parts, index)

    is_items = cfg.get('type') == 'items'
    parser = parse_items if is_items else parse_cards

    seen = set()
    by_name = {}
    all_cards = []
    for f in cfg['files']:
        for card in parser(f):
            if card['name'] not in seen:
                seen.add(card['name'])
                all_cards.append(card)
                by_name[card['name']] = card

    # Optional explicit whitelist (e.g. a specific character's deck) — filters
    # and reorders to match the list exactly, instead of every card in `files`.
    if 'cards' in cfg:
        missing = [n for n in cfg['cards'] if n not in by_name]
        if missing:
            raise SystemExit(f"generate-cards.py: card(s) not found for set "
                              f"'{set_name}': {', '.join(missing)}")
        return [by_name[n] for n in cfg['cards']]

    return all_cards


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

    de = card.get('defense_effect', 'None')
    rows += f'<tr><td class="lbl">Defense</td><td>{h(de)}</td></tr>'

    if card.get('range'):
        rows += f'<tr><td class="lbl">Range</td><td>{h(card["range"])}</td></tr>'

    flavor = ''
    if card.get('flavor'):
        flavor = f'<div class="flavor">&#8220;{h(card["flavor"])}&#8221;</div>'

    # Body text is set large by default, because most cards are short — median
    # is ~140 characters. A handful run 300+ and would overflow a fixed 84mm
    # card at that size, so those step down instead of clipping. Better a
    # slightly smaller wordy card than a truncated one.
    weight = sum(len(str(card.get(k, ''))) for k in
                 ('attack', 'special_rule', 'effect', 'defense_effect', 'range', 'flavor'))
    density = ' denser' if weight > 285 else (' dense' if weight > 195 else '')

    return f'''<div class="card{density}" style="background:{bg_color};border-color:{hex_color}99">
  <div class="card-top">
    <div class="card-name">{h(card["name"])}</div>
    <div class="dot" style="background:{hex_color}"></div>
  </div>
  <div class="card-sub" style="color:{hex_color}">{h(stat_label)}</div>
  <div class="divider" style="background:{hex_color}44"></div>
  <table class="tbl">{rows}</table>
  {flavor}
</div>'''


def item_to_html(item):
    type_line = ''
    if item.get('type'):
        type_line = f'<div class="card-sub" style="color:{ITEM_HEX}">{h(item["type"])}</div>'

    effect = '<br>'.join(h(l) for l in item.get('effect_lines', []))

    return f'''<div class="card" style="background:{ITEM_BG};border-color:{ITEM_HEX}99">
  <div class="card-top">
    <div class="card-name">{h(item["name"])}</div>
  </div>
  {type_line}
  <div class="divider" style="background:{ITEM_HEX}44"></div>
  <div class="item-effect">{effect}</div>
</div>'''


def render_card(card):
    if card.get('_type') == 'item':
        return item_to_html(card)
    return card_to_html(card)


def chunk(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def generate_html(all_cards, title):
    page_divs = []
    for page_cards in chunk(all_cards, CARDS_PER_PAGE):
        cards_html = '\n'.join(render_card(c) for c in page_cards)
        page_divs.append(f'<div class="page">\n{cards_html}\n</div>')

    pages_html = '\n'.join(page_divs)
    total = len(all_cards)
    total_pages = -(-total // CARDS_PER_PAGE)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Tales Untold — {h(title)} ({total} cards, {total_pages} pages)</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}

@page {{
  size: letter;
  margin: 10mm;
}}

body {{
  font-family: Georgia, "Times New Roman", serif;
  background: #bbb;
}}

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

.page:last-child {{
  break-after: auto;
  page-break-after: auto;
}}

@media screen {{
  body {{ padding: 12mm; }}
  .page {{
    margin-bottom: 12mm;
    box-shadow: 0 2px 12px rgba(0,0,0,0.3);
  }}
}}

.card {{
  width: 60mm;
  height: 84mm;
  border: 1.5px solid;
  border-radius: 7px;
  padding: 2.5mm 3mm 2mm;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}}

.card-top {{
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 1.5px;
}}

.card-name {{
  font-size: 12pt;
  font-weight: bold;
  line-height: 1.12;
  flex: 1;
  letter-spacing: 0.01em;
}}

.dot {{
  width: 11px;
  height: 11px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-left: 5px;
  margin-top: 2px;
}}

.card-sub {{
  font-size: 7.5pt;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 3px;
  font-style: italic;
}}

.divider {{
  height: 1px;
  margin-bottom: 3px;
}}

.tbl {{
  width: 100%;
  border-collapse: collapse;
  flex: 1;
}}

.tbl td {{
  font-size: 9.5pt;
  line-height: 1.28;
  vertical-align: top;
  padding: 1.5px 0;
}}

.tbl .lbl {{
  font-size: 7pt;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #555;
  white-space: nowrap;
  padding-right: 4px;
  width: 1px;
  padding-top: 2px;
}}

.card.dense .tbl td {{ font-size: 8.2pt; line-height: 1.22; }}
.card.dense .flavor {{ font-size: 8pt; }}
.card.dense .card-name {{ font-size: 11pt; }}

.card.denser .tbl td {{ font-size: 7pt; line-height: 1.18; }}
.card.denser .flavor {{ font-size: 7pt; }}
.card.denser .card-name {{ font-size: 10pt; }}
.card.denser .tbl .lbl {{ font-size: 6pt; }}

.flavor {{
  font-style: italic;
  font-size: 9pt;
  color: #555;
  line-height: 1.3;
  margin-top: auto;
  padding-top: 3px;
  border-top: 1px solid rgba(0,0,0,0.12);
}}

.item-effect {{
  font-size: 9.5pt;
  line-height: 1.35;
  flex: 1;
}}
</style>
</head>
<body>
{pages_html}
</body>
</html>'''


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    set_name = sys.argv[1] if len(sys.argv) > 1 else 'core'

    if set_name not in SETS:
        print(f'Unknown set: {set_name}')
        print(f'Available sets: {", ".join(SETS)}')
        sys.exit(1)

    cfg = SETS[set_name]
    print(f'Generating: {cfg["title"]}')

    all_cards = load_set(set_name)
    total_pages = -(-len(all_cards) // CARDS_PER_PAGE)
    output = f'card-print-{set_name}.html'

    with open(output, 'w', encoding='utf-8') as f:
        f.write(generate_html(all_cards, cfg['title']))

    print(f'  {len(all_cards)} items across {total_pages} pages → {output}')
    last = len(all_cards) % CARDS_PER_PAGE or CARDS_PER_PAGE
    if last < CARDS_PER_PAGE:
        print(f'  (last page has {last})')

    # For a share of another set, say what the share actually came out as.
    # The whole point of a split is the balance, so print it every time
    # rather than trusting the comment in the SETS table to stay true.
    if 'split' in cfg:
        parent, parts, _ = cfg['split']
        by_color = collections.Counter(c['color'] for c in all_cards)
        by_range = collections.Counter(c['range'] for c in all_cards)
        fmt = lambda t: '  '.join(f'{k} {v}' for k, v in sorted(t.items()))
        print(f'  colour: {fmt(by_color)}')
        print(f'  range:  {fmt(by_range)}')
        residue = split_residue(load_set(parent), parts)
        if residue:
            print(f'  ! uneven — {parts} does not divide: {", ".join(residue)}')
            print(f'    the shares differ by one card in each; '
                  f'see the SETS note on the 12/6/3 ratio')
    print('\nPrint settings: Margins = None, Background graphics = On, Scale = 100%')
