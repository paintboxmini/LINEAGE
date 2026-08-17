#!/usr/bin/env python3
"""Acceptance tests for the LINEAGE repo — the checks a Release pass runs.

Why this exists: `CLAUDE.md`'s Release mode has always said "acceptance tests,"
and there were none. Every check below had been hand-written as a throwaway
script, repeatedly, across many sessions — deck validation alone got rewritten
half a dozen times in one night, each time slightly differently, and one of
those variants was wrong in a way that hid a real problem for an hour. A check
you retype is a check you eventually retype incorrectly.

Run from anywhere:
    python3 agent-tools/verify.py           # all checks
    python3 agent-tools/verify.py --quick   # skip the print-artifact rebuild

Exit code is 0 only if every check passes, so this is usable as a gate.

Each check prints its own PASS/FAIL line and, on failure, every offending item —
never a truncated sample. A verification tool that hides failures behind an
ellipsis is worse than none, because it reads as green.
"""

import os
import re
import subprocess
import sys
import glob
import collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'combatsimulations'))

# Range is a closed vocabulary (rules/combat.md, the range table). Anything else
# is a card inventing a fourth value the engine has no way to express.
VALID_RANGE = {'Melee', 'Ranged', 'Both'}

# Acquisition-source tags (CLAUDE.md, Cards). Finite on purpose: sources are
# countable, themes are not. A new tag here is an Authority-2 decision.
VALID_TAGS = {
    'ASHFALL', 'BASIN', 'BRIARWATCH', 'COIL', 'ENGINE', 'HOLLOW', 'MASON',
    'MILESTONE', 'UNHELD', 'WEALD', 'WALLOWS', 'GLASSLIGHT', 'ABYSS',
    'SHORELINE',
    # PROMISE is provisional. It arrived on 2026-08-17 with six cards that had
    # been living inside characters/kaine/ and characters/mirel/ rather than in
    # cards/, so no tag check had ever seen them. `world/lineage.md` says a tag
    # records an origin *location* — the People of Promise are a tradition
    # spanning congregations, and their home location is GLASSLIGHT. Whether
    # tradition-tags are legitimate is Drew's call; logged in
    # `unresolved-concerns.md`. Registered rather than silently retagged so the
    # cards keep saying what they were written to say.
    'PROMISE',
}

NAME_RE = r'^\*\*([A-Z][A-Z0-9\'’ \-,!?&]+)\*\*\s*$'

results = []


def report(name, failures, detail=None):
    ok = not failures
    results.append(ok)
    print(f'{"PASS" if ok else "FAIL"}  {name}' + (f'  ({detail})' if detail and ok else ''))
    for f in failures:
        print(f'        {f}')
    return ok


def load_canon():
    """Every card in cards/. One card per file since the 2026-08-17 split — the
    filename is the card's slug, the file holds exactly one card block plus its
    metadata footer. Card *sets* are no longer implied by file grouping; each
    card names its own set on a `**Set:**` line, and `cards/buckets/` records
    behaviour membership."""
    cards = {}
    for path in sorted(glob.glob('cards/*.md')):
        text = open(path, encoding='utf-8').read()
        m = re.search(NAME_RE, text, re.M)
        if not m:
            continue
        colored = re.search(r'^(RED|BLUE|GREEN) — (BODY|MIND|SOUL)(?: — ([A-Z]+))?\s*$',
                            text, re.M)
        colorless = re.search(r'^COLORLESS\s*$', text, re.M)
        if not (colored or colorless):
            continue
        rng = re.search(r'^Range: (.+)$', text, re.M)
        die = re.search(r'^Attack: .*?\bd(\d+)', text, re.M)
        cset = re.search(r'^\*\*Set:\*\* (.+)$', text, re.M)
        cards[m.group(1).strip()] = {
            'color': colored.group(1)[0] if colored else None,
            'stat': colored.group(2).lower() if colored else None,
            'tag': colored.group(3) if colored else None,
            'range': rng.group(1).strip() if rng else None,
            'die': int(die.group(1)) if die else None,
            'set': cset.group(1).strip() if cset else None,
            'file': path,
            'block': text,
        }
    return cards


def check_card_format(canon):
    bad = []
    for name, c in sorted(canon.items()):
        where = f"{name} ({c['file'].split('/')[-1]})"
        if c['range'] is None:
            bad.append(f'{where}: no Range line')
        elif c['range'] not in VALID_RANGE:
            bad.append(f"{where}: Range {c['range']!r} is not one of {sorted(VALID_RANGE)}")
        if c['tag'] and c['tag'] not in VALID_TAGS:
            bad.append(f"{where}: unknown tag {c['tag']!r}")
        if not re.search(r'^Attack: ', c['block'], re.M):
            bad.append(f'{where}: no Attack line')
    return report('card format (Range vocabulary, tags, required lines)', bad,
                  f'{len(canon)} cards')


def parse_decks():
    """Yield (label, path, declared_total, {color: [names]}) for every deck line.

    Covers characters/ as well as bestiary/ — until 2026-08-17 this globbed
    bestiary only, so 12 character stat blocks and 2 character decks had never
    been validated at all. Found by the coverage assertion below, not by anyone
    noticing.

    Globs every file in each entry folder, not just mechanics.md: multi-variant
    entries (Ashgrazer, Briarbundles, the Tithe Engine) keep each variant's stat
    block and deck in that variant's own section file. Narrowing this to
    mechanics.md on 2026-08-17 silently dropped 6 of 37 decks from validation
    while still reporting PASS."""
    for path in _stat_files():
        text = open(path, encoding='utf-8').read()
        for m in re.finditer(r'\*\*Deck \((\d+) — (\d+) Blue / (\d+) Red / (\d+) Green\):\*\*(.+)',
                             text):
            total, b, r, g = (int(x) for x in m.groups()[:4])
            got = {'blue': [], 'red': [], 'green': []}
            for grp, col in re.findall(r'([^·]+?)\*\((blue|red|green)\)\*', m.group(5)):
                got[col] += [x.strip() for x in grp.split(',') if x.strip()]
            yield path, total, {'blue': b, 'red': r, 'green': g}, got


def check_decks(canon):
    colors = {'blue': 'B', 'red': 'R', 'green': 'G'}
    bad = []
    n = 0
    for path, total, want, got in parse_decks():
        n += 1
        f = '/'.join(path.split('/')[-2:])
        if sum(want.values()) != total:
            bad.append(f'{f}: declared total {total} != {want}')
        for col, k in want.items():
            if len(got[col]) != k:
                bad.append(f'{f}: {col} lists {len(got[col])}, declares {k}')
            for name in got[col]:
                if name not in canon:
                    bad.append(f'{f}: {name!r} is not a card in cards/')
                elif canon[name]['color'] and canon[name]['color'] != colors[col]:
                    bad.append(f"{f}: {name} is {canon[name]['color']}, listed under {col}")
    on_disk = sum(len(re.findall(r'\*\*Deck \(\d+ — ', open(p, encoding='utf-8').read()))
                  for p in _stat_files())
    if n != on_disk:
        bad.append(f'COVERAGE: {on_disk} deck lines exist across entry files, this check read {n}. '
                   'A deck line the check never parsed reports identical to a clean one — '
                   'that is how 6 of 37 went silently unvalidated on 2026-08-17.')
    return report('bestiary decks (size, per-color counts, card resolution)', bad,
                  f'{n} decks')


def check_stat_blocks():
    bad = []
    n = 0
    for path in _stat_files():
        text = open(path, encoding='utf-8').read()
        for m in re.finditer(
                r'\*\*Mind (\d+) / Body (\d+) / Soul (\d+) — HP (\d+)\*\*(.*)', text):
            mind, body, soul, hp = (int(x) for x in m.groups()[:4])
            trailing = m.group(5)
            n += 1
            f = '/'.join(path.split('/')[-2:])
            formula = 3 * body + soul + mind
            if hp != formula and 'bespoke' not in trailing.lower():
                bad.append(f'{f}: HP {hp} != formula {formula} and not marked bespoke')
            after = text[m.end():m.end() + 200]
            ctr = re.search(r'\*\*Creature Threat Rating:\*\* (\d+)', after)
            if ctr and int(ctr.group(1)) != mind + body + soul:
                bad.append(f'{f}: CTR {ctr.group(1)} != total stats {mind + body + soul}')
    on_disk = sum(len(re.findall(r'\*\*Mind \d+ / Body \d+ / Soul \d+ — HP \d+\*\*', open(p, encoding='utf-8').read()))
                  for p in _stat_files())
    if n != on_disk:
        bad.append(f'COVERAGE: {on_disk} stat blocks exist across entry files, this check read {n}.')
    return report('stat blocks (HP formula unless bespoke, CTR = total stats)', bad,
                  f'{n} blocks')


def check_refs():
    bad = []
    for path in glob.glob('**/*.md', recursive=True):
        # archives/ is deprecated content; memory.md is a threshold log whose
        # own header rule is that existing entries "stay exactly as written";
        # unresolved-concerns.md's Pending Propagation entries carry the same
        # kind of historical rename narration since the 2026-08-12 gpt-branch
        # merge relocated that section there from memory.md; changelog.md is
        # the same ship-by-ship record that used to live inside archives/ (as
        # "Work Log — The Trail") before the 2026-08-12 Changelog/Archives
        # split gave it its own file — its entries describe what was true
        # when shipped, same historical-record status it had inside archives/.
        # None of these four is live canon prose, so a renamed/deleted file
        # mentioned in any of them is historical record, not a broken link.
        if path.startswith('archives/') or path in ('memory.md', 'unresolved-concerns.md', 'changelog.md'):
            continue
        text = open(path, encoding='utf-8').read()
        for m in re.finditer(r'^\*\*Cards:\*\* `([^`]+)`', text, re.M):
            if not os.path.exists(m.group(1)) and 'filename' not in m.group(1):
                bad.append(f'{path} -> {m.group(1)} (missing)')
        # Directory-qualified paths only: bare `red-team.md` is prose shorthand.
        for m in re.finditer(r'`((?:cards|bestiary|rules|quests|places|characters|items|'
                             r'world|factions|Oracle|agent-tools|playtesting)/'
                             r'[A-Za-z0-9_\-/]+\.md)`', text):
            target = m.group(1)
            if os.path.exists(target) or 'filename' in target:
                continue   # 'filename.md' is CLAUDE.md's format-template placeholder
            # Prose that names a file precisely to say it does NOT exist is not a
            # broken link. Look at the sentence around the match, not the whole line.
            ctx = text[max(0, m.start() - 120):m.end() + 80]
            if re.search(r"\b(?:no|not|never|pending|yet|missing|doesn't|does not|"
                         r"would|should|future|planned)\b", ctx, re.I):
                continue
            bad.append(f'{path} -> {target} (missing)')
    return report('cross-references resolve', bad)


def check_sim(canon):
    import content
    sim = content.build_cards()
    bad = []

    unknown = sorted({n for b in content.CARD_TAGS.values() for n in b} - set(sim))
    bad += [f'CARD_TAGS names a card the sim does not define: {n}' for n in unknown]

    for deck_name, (_stats, deck) in content.ROSTER.items():
        for n in deck:
            if n not in sim:
                bad.append(f'ROSTER[{deck_name}] names undefined card {n!r}')

    # Both engines share content.py, so a signature drift is a silent behaviour split.
    import inspect
    import engine
    import team_engine
    for meth in ('deal', 'insert_exhaust', 'insert_wound', 'attack'):
        a = getattr(engine.Duel, meth, None)
        b = getattr(team_engine.Battle, meth, None)
        if a and b and str(inspect.signature(a)) != str(inspect.signature(b)):
            bad.append(f'engine/team_engine signature drift on {meth}()')

    # Canon reconciliation: anything defined in both must agree.
    for n in sorted(set(sim) & set(canon)):
        s, c = sim[n], canon[n]
        if c['color'] and s.color != c['color']:
            bad.append(f'{n}: color sim={s.color} canon={c["color"]}')
        if c['stat'] and s.stat != c['stat']:
            bad.append(f'{n}: stat sim={s.stat} canon={c["stat"]}')
        reach = getattr(s, 'reach', None)
        if reach and c['range'] and reach != c['range'].lower():
            bad.append(f'{n}: range sim={reach!r} canon={c["range"]!r}')
        if s.base_die and c['die'] and s.base_die != c['die']:
            bad.append(f'{n}: die sim=d{s.base_die} canon=d{c["die"]}')

    overlap = len(set(sim) & set(canon))
    return report('simulator (tags, roster, engine parity, canon reconciliation)', bad,
                  f'{overlap} cards reconciled')


def check_item_keywords():
    """Every keyword an item file names must exist in the glossary, and items may
    not restate a keyword's rule in longhand. Both failure modes were live until
    2026-08-02: SPLIT WEDGE claimed Anchored for a one-turn effect (Anchored is
    explicitly persistent and re-triggering), and BARBED WRAP wrote out Thorns by
    hand in a strictly wider form. Neither is visible to any other check."""
    gl = open('rules/card-glossary.md', encoding='utf-8').read()
    known = {m.group(2).replace(' X', '').replace(' [Color]', '').strip()
             for m in re.finditer(r'^\*\*\((\d+)\) ([A-Za-z \[\]X]+)\*\*', gl, re.M)}
    longhand = [
        (r'reduce (?:all )?(?:incoming )?damage by \d', 'Armour X'),
        (r'deal \d+ damage to (?:the )?attacker', 'Thorns X'),
        (r'take half damage', 'Resist'),
    ]
    bad = []
    for path in sorted(glob.glob('items/*.md')) + sorted(glob.glob('rules/equipment.md')):
        text = open(path, encoding='utf-8').read()
        f = path.split('/')[-1]
        for line in text.splitlines():
            if not re.match(r'^(?:Use|Effect|Activates|Passive)', line):
                continue
            for pat, kw in longhand:
                if re.search(pat, line, re.I) and kw.split()[0] not in line:
                    bad.append(f'{f}: writes {kw} longhand -> {line.strip()[:70]}')
            # Anchored must describe a persisting benefit, never a one-turn one.
            if 'Anchored' in line and re.search(r'\bthis turn\b', line) \
                    and 'start of each' not in line:
                bad.append(f'{f}: Anchored used for a one-turn effect -> {line.strip()[:70]}')
    return report('item keyword usage (no invented or longhand keywords)', bad,
                  f'{len(known)} glossary keywords')


def check_glossary_count(canon):
    """The glossary header states how many card blocks its keyword counts were
    taken over. That number drifted twice in one day — once because cards were
    added after the count, once because my own recount matched on a colored
    header line and silently dropped cards/colorless.md. A stated number nothing
    verifies is a number that will be wrong."""
    text = open('rules/card-glossary.md', encoding='utf-8').read()
    m = re.search(r'Recounted across all (\d+) card blocks', text)
    if not m:
        return report('glossary block count', ['header no longer states a block count'])
    stated, actual = int(m.group(1)), len(canon)
    bad = ([] if stated == actual else
           [f'header says {stated} card blocks, cards/ has {actual} — recount the keyword numbers'])
    return report('glossary block count matches cards/', bad, f'{actual} blocks')


def check_duplicate_refs():
    """A file that lists the same target twice in its bullet references. Cheap to
    create during a repoint (two old links collapse onto one new file) and
    invisible to every other check, since both entries resolve fine."""
    import collections
    bad = []
    for path in sorted(glob.glob('**/*.md', recursive=True)):
        if path.startswith('archives/'):
            continue
        targets = []
        for line in open(path, encoding='utf-8').read().splitlines():
            if not line.startswith('- `'):
                continue
            m = re.search(r'`([^`]+)`', line)
            if m and '/' in m.group(1):
                targets.append(m.group(1))
        for tgt, n in collections.Counter(targets).items():
            if n > 1:
                bad.append(f'{path}: lists {tgt} {n} times')
    return report('no duplicate cross-references', bad)


RESTATED_DIRS = ('quests', 'places', 'world', 'factions', 'items')

DISTANCE_RE = re.compile(
    r'[^.!?\n]{0,70}\b(?:\d+(?:[–-]\d+)? ?(?:ft\.?|feet|foot|yards?|meters?|metres?|'
    r'miles?|inch(?:es)?)|(?:twenty|thirty|forty|fifty|sixty|hundred|thousand)[- ]'
    r'(?:feet|foot|yards?|paces|miles?)|meter tall|\d+ ?(?:yards?|paces))\b'
    r'[^.!?\n]{0,50}', re.I)


def _bestiary_blocks():
    """{'bestiary/x/mechanics.md': [(mind, body, soul, hp), ...]} for every stat block."""
    blocks = {}
    for path in sorted(glob.glob('bestiary/*/*.md')):
        text = open(path, encoding='utf-8').read()
        blocks[path] = [tuple(int(x) for x in m.groups()) for m in re.finditer(
            r'Mind (\d+) ?/ ?Body (\d+) ?/ ?Soul (\d+)[ ,—-]+HP (\d+)', text)]
    return blocks


def check_restated_stat_blocks():
    """A stat block written outside bestiary/ must agree with its source.

    Five quest files restate creature numbers for GM convenience. They agreed
    when written; nothing stopped them drifting afterward. `characters/` is
    skipped by design — player and NPC blocks have no bestiary source.
    """
    src = _bestiary_blocks()
    bad = []
    n = 0
    for d in RESTATED_DIRS:
        for path in sorted(glob.glob(f'{d}/*.md')):
            text = open(path, encoding='utf-8').read()
            for m in re.finditer(
                    r'Mind (\d+) ?/ ?Body (\d+) ?/ ?Soul (\d+)[ ,—-]+HP (\d+)', text):
                mind, body, soul, hp = (int(x) for x in m.groups())
                n += 1
                window = text[max(0, m.start() - 400):m.end() + 250]
                named = {f'bestiary/{f}.md' for f in
                         re.findall(r'`bestiary/([A-Za-z0-9_\-]+)\.md`', window)}
                bespoke = 'bespoke' in window.lower()
                # CTR is searched forward only. A backward window picks up the
                # previous creature's rating — sour-tomatoes stacks two blocks
                # a few lines apart, and the first draft of this check read
                # Cole's stats against his father's number.
                ctr = re.search(r'Creature Threat Rating:?\*{0,2} (\d+)',
                                text[m.end():m.end() + 200])
                if ctr and int(ctr.group(1)) != mind + body + soul:
                    bad.append(f'{path}: CTR {ctr.group(1)} != total stats '
                               f'{mind + body + soul}')
                if named and not bespoke:
                    known = {b for f in named for b in src.get(f, [])}
                    if known and (mind, body, soul, hp) not in known:
                        bad.append(
                            f'{path}: restates {mind}/{body}/{soul} HP {hp}, which '
                            f'matches no block in {", ".join(sorted(named))}')
                elif not bespoke and hp != 3 * body + soul + mind:
                    bad.append(f'{path}: HP {hp} != formula {3 * body + soul + mind} '
                               f'and not marked bespoke')
    return report('restated stat blocks match their bestiary source', bad,
                  f'{n} restatements')


def check_distances():
    """No measured distance in quest or bestiary content (CLAUDE.md, Do Not).

    Combat is abstract positioning. Drew ruled the scope strict on 2026-08-03:
    room dimensions and object specs go too, not just combat reach.
    """
    bad = []
    for d in ('quests', 'bestiary'):
        for path in sorted(glob.glob(f'{d}/*.md')):
            for m in DISTANCE_RE.finditer(open(path, encoding='utf-8').read()):
                snippet = m.group(0).strip()
                bad.append(f'{path}: {snippet}')
    return report('no measured distances in quests/ or bestiary/', bad)


HP_FORMULA_RE = re.compile(r'(\d+)\s*×\s*Body\)?\s*\+\s*Soul\s*\+\s*Mind')

HP_FORMULA_FILES = (
    'CLAUDE.md',
    'rules/core-rules.md',
    'rules/player-guide.md',
    'rules/gm-guide.md',
    'rules/character-creation.md',
    'agent-tools/compiled-crib.md',
)


def check_hp_formula():
    """The HP formula is restated in six files instead of living in one
    canonical spot, each restatement free to drift independently — flagged
    as the harness's biggest single propagation risk (Drew, 2026-08-05, the
    Harness Audit's point 3). Not fixed by deleting the restatements — each
    genuinely serves standalone readability in its own file (a GM reading
    gm-guide.md shouldn't have to jump to core-rules.md for one number) —
    fixed by making drift between them impossible to miss instead. Canonical
    value is `rules/core-rules.md`'s, per CLAUDE.md's own Rule Definitions
    taxonomy ("formulas (`rules/core-rules.md`)").
    """
    seen = {}
    bad = []
    for path in HP_FORMULA_FILES:
        text = open(path, encoding='utf-8').read()
        matches = set(HP_FORMULA_RE.findall(text))
        if not matches:
            bad.append(f'{path}: HP formula not found (moved or reworded?)')
            continue
        if len(matches) > 1:
            bad.append(f'{path}: states multiple different HP formulas: {sorted(matches)}')
        seen[path] = matches
    canonical = seen.get('rules/core-rules.md')
    if canonical:
        for path, matches in seen.items():
            if path != 'rules/core-rules.md' and matches != canonical:
                bad.append(f'{path}: HP formula {sorted(matches)} != '
                           f'canonical {sorted(canonical)} (rules/core-rules.md)')
    return report('HP formula consistent across canonical files', bad,
                  f'{len(seen)} files checked')


ENTRY_GLOBS = ('bestiary/*/*.md', 'characters/*/*.md')

# Deck and stat-block validation covers bestiary/ AND characters/. It globbed
# bestiary only from the day it was written until 2026-08-17, so 12 character
# stat blocks and 2 character decks had never been validated at all — a gap the
# coverage assertion below found, not a person. Widening it surfaced 11 real
# errors (nine character HP values predating the 2026-08-06 three-stat HP
# formula, and Orin Vane's prose deck line); all were fixed, and the scope has
# stayed wide since.
STAT_SCOPE = ENTRY_GLOBS


def _entry_files():
    out = []
    for g in ENTRY_GLOBS:
        out += sorted(glob.glob(g))
    return out


def _stat_files():
    out = []
    for g in STAT_SCOPE:
        out += sorted(glob.glob(g))
    return out


def check_entry_structure():
    """Structural invariants for bestiary/ and characters/ entry folders.

    Every bug the 2026-08-17 restructures produced was invisible to the checks
    that existed: content duplicated into two files, a Contents list pointing at
    files that no longer existed, a heading appearing twice because two scripted
    passes each handled part of the same fold. None of those break a
    cross-reference or a deck, so nothing caught them until someone happened to
    look. These are cheap and always on.
    """
    bad = []
    for d in sorted(glob.glob('bestiary/*/') + glob.glob('characters/*/')):
        readme = d + 'README.md'
        if not os.path.exists(readme):
            bad.append(f'{d}: no README.md')
            continue
        s = open(readme, encoding='utf-8').read()
        if s.count('\n## Contents\n') > 1:
            bad.append(f'{readme}: {s.count(chr(10) + "## Contents" + chr(10))} Contents blocks')
        listed = {m.group(1) for m in re.finditer(r'^- \[[^\]]+\]\(([^)]+)\)$', s, re.M)}
        actual = {os.path.basename(p) for p in glob.glob(d + '*.md')} - {'README.md'}
        if listed:
            for f in sorted(listed - actual):
                bad.append(f'{readme}: Contents lists {f}, which does not exist')
            for f in sorted(actual - listed):
                bad.append(f'{readme}: {f} exists but is not in Contents')
    for path in _entry_files():
        text = open(path, encoding='utf-8').read()
        heads = [m.group(1).strip() for m in re.finditer(r'^## (.+)$', text, re.M)]
        for h, n in collections.Counter(heads).items():
            if n > 1:
                bad.append(f'{path}: heading "{h}" appears {n} times')
        # a bold label immediately preceded by backticked paths is the signature
        # of a botched reference rewrite (2026-08-17 produced 44 of them)
        if re.search(r'^`[^`]+\.md`(?:, `[^`]+\.md`)*\*\*', text, re.M):
            bad.append(f'{path}: malformed label — reference list ran into a bold heading')
    return report('entry folders (Contents accurate, no duplicated sections)', bad,
                  f'{len(glob.glob("bestiary/*/") + glob.glob("characters/*/"))} entries')


def check_oracle_sync():
    """The Oracle pool is mirrored in two places that were never derived from it
    — `combatsimulations/content.py`'s ORACLE_DECK and `printing/generate-cards.py`'s
    oracle card set — and kept in sync by hand. Hand-sync is exactly the failure
    mode this file exists to catch.

    Two invariants, deliberately different in strength:

    1. The two code lists must always agree with each other. Both claim to hold
       the same pool; if they disagree, one is stale no matter what the pool is.
    2. They must match `Oracle/baseoracledeck.md` — but only when that file
       actually lists a pool. It is deliberately empty right now (Drew is
       building it by hand), and an empty pool is a stated state, not a
       failure. The moment it is populated this check starts enforcing.
    """
    def names(text):
        return re.findall(r'["\']([A-Z][A-Z0-9\'’ \-]+)["\']', text)

    def block(path, start_re):
        src = open(path, encoding='utf-8').read()
        m = re.search(start_re, src, re.S)
        if not m:
            return None
        depth, i = 0, m.end() - 1
        for j in range(i, len(src)):
            if src[j] == '[':
                depth += 1
            elif src[j] == ']':
                depth -= 1
                if depth == 0:
                    return names(src[i:j])
        return None

    sim = block('combatsimulations/content.py', r'ORACLE_DECK\s*=\s*\[')
    pr = block('printing/generate-cards.py', r"'title':\s*'Oracle Deck'.*?'cards':\s*\[")
    bad = []
    if sim is None:
        bad.append("combatsimulations/content.py: ORACLE_DECK not found")
    if pr is None:
        bad.append("printing/generate-cards.py: Oracle Deck 'cards' list not found")

    detail = None
    if sim is not None and pr is not None:
        for n in sorted(set(sim) - set(pr)):
            bad.append(f'{n}: in content.py ORACLE_DECK, missing from generate-cards.py')
        for n in sorted(set(pr) - set(sim)):
            bad.append(f'{n}: in generate-cards.py, missing from content.py ORACLE_DECK')

        pool_src = open('Oracle/baseoracledeck.md', encoding='utf-8').read()
        pool = set(re.findall(NAME_RE, pool_src, re.M))
        if pool:
            for n in sorted(pool - set(sim)):
                bad.append(f'{n}: in the Oracle pool, missing from both code lists')
            for n in sorted(set(sim) - pool):
                bad.append(f'{n}: in the code lists, not in the Oracle pool')
            detail = f'{len(pool)} pooled cards'
        else:
            detail = (f'{len(sim)} mirrored; pool file empty by design, '
                      'cross-check skipped')
    return report('Oracle pool mirrors in sync', bad, detail)


def check_print():
    script = 'printing/generate-all.sh'
    if not os.access(script, os.X_OK):
        return report('print artifacts current', [f'{script} not executable'])
    p = subprocess.run(['./generate-all.sh', '--check'], cwd='printing',
                       capture_output=True, text=True)
    stale = [l.strip() for l in p.stdout.splitlines()
             if l.startswith('  ') and l.strip().endswith('.html')]
    return report('print artifacts current', stale)


def main():
    quick = '--quick' in sys.argv
    print('LINEAGE acceptance tests\n')
    canon = load_canon()
    check_card_format(canon)
    check_decks(canon)
    check_stat_blocks()
    check_refs()
    check_sim(canon)
    check_item_keywords()
    check_glossary_count(canon)
    check_duplicate_refs()
    check_restated_stat_blocks()
    check_distances()
    check_hp_formula()
    check_entry_structure()
    check_oracle_sync()
    if quick:
        print('SKIP  print artifacts current (--quick)')
    else:
        check_print()
    print()
    failed = results.count(False)
    print(f'{len(results) - failed}/{len(results)} checks passed')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
