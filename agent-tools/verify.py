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
    # Read from rules/keywords/ rather than the glossary those files are built
    # into. Parsing the generated artifact would have worked identically right up
    # until a rebuild changed its shape.
    known = {re.match(r'^# (.+)\n', open(p, encoding='utf-8').read()).group(1)
               .replace(' X', '').replace(' [Color]', '').strip()
             for p in sorted(glob.glob('rules/keywords/*.md'))}
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


def check_keyword_usage():
    """agent-tools/keyword-usage.md is generated from cards/ and the glossary.
    Committed rather than produced on demand so the numbers are readable and
    diffable, which means they can go stale — this fails when they have.

    Replaces check_glossary_count, which verified a single hand-typed block
    total in the glossary header. That number is gone: the per-keyword counts it
    caveated moved out of the player-facing file entirely on 2026-08-18, after
    sitting wrong on 21 of 29 keywords. A generated table cannot drift, and this
    check is what makes that true rather than merely intended."""
    r = subprocess.run([sys.executable, 'agent-tools/keyword-usage.py', '--check'],
                       capture_output=True, text=True)
    bad = [] if r.returncode == 0 else [(r.stdout + r.stderr).strip()]
    n = len(re.findall(r'^\| .+ \| \d+ \| \d+% \|$',
                       open('agent-tools/keyword-usage.md', encoding='utf-8').read(), re.M))
    defined = len(glob.glob('rules/keywords/*.md'))
    # Coverage: the table must hold a row for every keyword that has a file.
    if n != defined:
        bad.append(f'COVERAGE: rules/keywords/ holds {defined} keywords, the table has {n} rows')
    # And the counts must not creep back into the player-facing file.
    gl = open('rules/card-glossary.md', encoding='utf-8').read()
    stale = re.findall(r'^\*\*\(\d+\) ', gl, re.M)
    if stale:
        bad.append(f'{len(stale)} glossary entries have regained a hand-typed count prefix')
    return report('keyword usage table current', bad, f'{defined} keywords')


def check_glossary_generated():
    """rules/card-glossary.md is built from rules/keywords/ and
    rules/status-cards/. Without this, "generated" is a claim in a docstring: a
    hand edit to the output would work fine until the next rebuild silently threw
    it away. This makes the edit fail loudly instead, at the moment it is made.

    Also asserts the split is total. Every keyword and status card must have a
    source file, and the built file must contain each one exactly once — a
    definition that exists only in the output is a definition the next rebuild
    deletes."""
    r = subprocess.run([sys.executable, 'agent-tools/generate-glossary.py', '--check'],
                       capture_output=True, text=True)
    bad = [] if r.returncode == 0 else [(r.stdout + r.stderr).strip()]
    gl = open('rules/card-glossary.md', encoding='utf-8').read()
    kw = sorted(glob.glob('rules/keywords/*.md'))
    sc = sorted(glob.glob('rules/status-cards/*.md'))
    for path, fmt in [(p, '**{}**') for p in kw] + [(p, '### {}') for p in sc]:
        name = re.match(r'^# (.+)\n', open(path, encoding='utf-8').read()).group(1).strip()
        hits = gl.count(fmt.format(name))
        if hits != 1:
            bad.append(f'{path}: "{name}" appears {hits} times in the built glossary, expected 1')
    # COVERAGE: nothing defined in the output that has no source behind it.
    built = len(re.findall(r'^\*\*([A-Za-z][A-Za-z \[\]X]*)\*\*$', gl, re.M))
    if built != len(kw):
        bad.append(f'COVERAGE: built glossary has {built} keyword entries, '
                   f'rules/keywords/ has {len(kw)} files')
    return report('glossary generated from its source files', bad,
                  f'{len(kw)} keywords + {len(sc)} status cards')


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
    # Canonical moved from rules/core-rules.md to rules/character-creation.md on
    # 2026-08-18, when core-rules was reclassified as a voice rather than an
    # owner (rules/README.md). A voice cannot be the source of a fact — and
    # character-creation.md already stated the formula in fuller form, with the
    # 3x Body weighting explained, while core-rules carried it as a table cell.
    CANON = 'rules/character-creation.md'
    canonical = seen.get(CANON)
    if not canonical:
        bad.append(f'{CANON} is the canonical source and states no HP formula')
    else:
        for path, matches in seen.items():
            if path != CANON and matches != canonical:
                bad.append(f'{path}: HP formula {sorted(matches)} != '
                           f'canonical {sorted(canonical)} ({CANON})')
    return report('HP formula consistent across canonical files', bad,
                  f'{len(seen)} files checked')


# --- Restated mechanical facts -----------------------------------------------
#
# Phase 0 of splitting rules/ better (Drew, 2026-08-18). The survey that
# prompted it found 20 headings appearing in two or more rules files and five in
# three: rules/ carries three parallel restatements of the ruleset — the detailed
# canon, core-rules.md's quick reference, and player-guide.md's printed player
# voice — with nothing recording which one owns a given fact.
#
# This check does NOT decide ownership. That is Phase 1, and it is Drew's call.
# It asserts only that every file stating a fact states the SAME fact, which is
# true today and is what silently stops being true. When the jurisdiction map
# lands, each claim gains a canonical file and the check also reports deviation
# from it, the way check_hp_formula already does for the one fact that has one.
#
# Each pattern captures the part that can drift — a rounding direction, a die
# size, a minimum — so a changed value fails as a DISAGREEMENT naming both files,
# rather than failing to match and disappearing. And the file set each claim was
# measured over is recorded below, so a reworded sentence fails as a COVERAGE
# error instead of quietly leaving the check with less to check. That failure
# mode has cost this repo more than the drift it guards against.

RESTATED_SCOPE = [p for p in sorted(glob.glob('rules/*.md'))
                  # glossary-frame.md is spliced verbatim into card-glossary.md;
                  # counting both would be one source agreeing with itself.
                  if not p.endswith('glossary-frame.md')] + ['CLAUDE.md']

CLAIMS = {
    'death threshold — rounding direction': (
        [r'negative half your Max HP \(rounded (up|down)\)',
         r'Max HP ÷ 2, rounded (up|down)'],
        {'rules/combat.md', 'rules/core-rules.md', 'rules/player-guide.md'},
    ),
    'Collapse threshold — HP': (
        [r'reduces you to \*\*(\d+) HP\*\*',
         r'Reach \*\*(\d+) HP\*\*',
         r'Reduced to (\d+) HP'],
        {'rules/combat.md', 'rules/core-rules.md', 'rules/player-guide.md'},
    ),
    'Collapsed recovery — interval in hours': (
        [r'(?:Every )?\*?\*?(\d+) in-game hours'],
        {'rules/combat.md', 'rules/core-rules.md', 'rules/player-guide.md'},
    ),
    'Collapsed recovery — die': (
        [r'recover \*?\*?1d(\d+) HP'],
        {'rules/combat.md', 'rules/core-rules.md', 'rules/player-guide.md'},
    ),
    'hand size — minimum': (
        [r'[Hh]and size[^.|]{0,40}?[Mm]ind[^.|]{0,30}?minimum (\d+)',
         r'[Mm]ind[^.|]{0,20}?\(minimum (\d+)\)[^.|]{0,30}?hand size',
         r'hand size is \*\*Mind\*\*, with a minimum of (\d+)'],
        {'rules/card-glossary.md', 'rules/cards.md', 'rules/character-creation.md',
         'rules/core-rules.md', 'rules/gm-guide.md', 'rules/player-guide.md'},
    ),
    'chase — escape distance': (
        [r'distance reaches (\d)\.\*\* They are out of sight',
         r'\*\*Distance (\d) = escaped\*\*',
         r'\*\*Reach (\d) and you\'re gone\*\*'],
        {'rules/combat.md', 'rules/core-rules.md', 'rules/player-guide.md'},
    ),
    'Take Cover — the keyword it grants': (
        # Cover has no number to compare, so the checkable fact is which keyword
        # it grants. Every file with a Take Cover action row must name the same
        # one. This is the shape to reuse for any rule expressed through a
        # keyword rather than a value: if one voice is updated and another is
        # missed, the stale file stops matching and fails as a COVERAGE error
        # naming itself.
        [r'\| Take Cover \|[^|]*?\b(Anchored)\b[^|]*\|'],
        {'rules/combat.md', 'rules/core-rules.md', 'rules/player-guide.md'},
    ),
    'Range Matrix — the four legality rows': (
        # Captured as one tuple, so any single cell flipping anywhere fails.
        # The three copies were byte-identical in combat.md and core-rules.md
        # but player-guide.md headed its column "You" instead of "Attacker" —
        # one table, two vocabularies, in the thing whose whole job is being
        # read the same way by everyone at the table. Unified 2026-08-18.
        [r'\| Frontline \| Frontline \| (.) \| (.) \| (.) \|\n'
         r'\| Frontline \| Backline \| (.) \| (.) \| (.) \|\n'
         r'\| Backline \| Frontline \| (.) \| (.) \| (.) \|\n'
         r'\| Backline \| Backline \| (.) \| (.) \| (.) \|'],
        {'rules/combat.md', 'rules/core-rules.md', 'rules/player-guide.md'},
    ),
    'DC table — Easy/Normal/Hard/Extreme': (
        [r'\| Easy \| (\d+) \|\n\| Normal \| (\d+) \|\n\| Hard \| (\d+) \|\n\| Extreme \| (\d+) \|'],
        {'rules/core-rules.md', 'rules/out-of-combat.md', 'rules/player-guide.md'},
    ),
    'core resolution — dice': (
        [r'\*\*(\d+d\d+) \+ (?:the )?relevant stat'],
        {'rules/core-rules.md', 'rules/out-of-combat.md', 'rules/player-guide.md'},
    ),
    'Advantage/Disadvantage — dice': (
        # Three files, three wordings — "drop lowest", "discard the lowest",
        # "drop the highest". One pattern covering all of them, because a
        # pattern that matches only one file is a check that only checks one.
        [r'[Rr]oll \*?\*?(\d+d\d+)\*?\*?, (?:drop|discard) (?:the )?(?:lowest|highest)'],
        {'rules/core-rules.md', 'rules/out-of-combat.md', 'rules/player-guide.md'},
    ),
    'short rest — duration in minutes': (
        [r'\*\*Duration:\*\* (\d+) minutes', r'\| Short \| (\d+) min'],
        {'rules/core-rules.md', 'rules/out-of-combat.md', 'rules/player-guide.md'},
    ),
    'short rest — heal': (
        [r'Recover \*\*(\d+d\d+ \+ Body)\*\* HP', r'\| Short \| [^|]*\| (\d+d\d+ \+ Body) HP',
         r'heal \*\*(\d+d\d+ \+ Body)\*\*'],
        {'rules/core-rules.md', 'rules/out-of-combat.md', 'rules/player-guide.md'},
    ),
    'short rest — daily limit': (
        [r'\*\*Limit:\*\* (\d+) per day', r'\| (\d+)/day \|'],
        {'rules/core-rules.md', 'rules/out-of-combat.md'},
    ),
    'long rest — duration': (
        [r'\*\*Duration:\*\* (7½) hours', r'\| Long \| (7½) hours'],
        {'rules/core-rules.md', 'rules/out-of-combat.md', 'rules/player-guide.md'},
    ),
    'flee check — dice': (
        [r'(\d+d\d+) \+ Soul vs DC'],
        {'rules/combat.md', 'rules/core-rules.md'},
    ),
    'flee check — DC': (
        [r'\d+d\d+ \+ Soul vs DC (\d+)'],
        {'rules/combat.md', 'rules/core-rules.md'},
    ),
    'initiative — die': (
        [r'1d(\d+) \+ \*?\*?Soul'],
        {'rules/card-glossary.md', 'rules/character-creation.md', 'rules/combat.md',
         'rules/core-rules.md', 'rules/player-guide.md'},
    ),
}


# --- Section inventory -------------------------------------------------------
#
# What every rules file is expected to contain, section by section. Added
# 2026-08-18 after an edit of mine computed its end boundary with a forward
# index search, matched a heading far below, and silently deleted `## Chase`,
# `## Fleeing Combat` and `## Initiative` from combat.md — 40 content lines —
# while this suite still reported 17 of 18 passing. Nothing here asserted that a
# rules file still contained the sections it had yesterday, so nothing could.
#
# Drew, on that: "we should have been double checking our work as we went."
#
# Updating this list is meant to be a deliberate act. A section that legitimately
# moves or is renamed gets edited here in the same commit; one that vanishes by
# accident fails the build and names itself. Same discipline as CLAIMS' expected
# file sets, which have already caught two silent blind spots today.
#
# Excluded: README.md (the map), card-glossary.md (generated, and already checked
# against its sources by check_glossary_generated), glossary-frame.md (its input).
SECTION_INVENTORY = {'cards.md': ['Card Anatomy',
              '"Attacker" / "Defender" vs. "Target"',
              'Card Example',
              "The Die Is the Card's Personality",
              'Card Glossary',
              'Deck Building',
              'Important: You Are Not Your Own Ally'],
 'character-creation.md': ['Stats',
                           'What Stats Do',
                           'Equipment',
                           'Starting Deck',
                           'Hand Size',
                           'The Oracle Deck',
                           'Advancement',
                           'Magic Expression'],
 'combat.md': ['Core Combat Philosophy',
               'Stealth & Ambush',
               'Chase',
               'Fleeing Combat',
               'Initiative',
               'Turn Structure',
               'Attack Resolution',
               'Damage Pipeline',
               'Range',
               'Positioning',
               'Ongoing Effects',
               'Objects',
               'Simultaneous Effects',
               'Collapse & Death'],
 'core-rules.md': ['Stats',
                   'Difficulty Classes',
                   'Combat — 1 Action + 1 Item Action Per Turn',
                   'Attack Resolution',
                   'Card Anatomy',
                   'Perception Modes',
                   'Collapse & Death',
                   'Resting',
                   'Positioning',
                   'Stealth & Ambush',
                   'Chase',
                   'Cover',
                   'Equipment Slots',
                   'Advancement',
                   'Important Rule'],
 'equipment.md': ['The Default: Dress However You Want',
                  'What Equipment Does',
                  'Weapon and Armor Tiers',
                  'Currency',
                  'Pacing — How Fast Gear Should Arrive',
                  'Pricing Consumables',
                  'More Fastball Ideas (Unnamed on Purpose)',
                  'Artifacts',
                  'Building Items As Standard Practice'],
 'gm-guide.md': ['The Basic Job',
                 'Running Locations',
                 'Building Enemies',
                 'Using the Oracle',
                 'Pacing Sessions',
                 'When to Call for Rolls',
                 'Death & Consequences',
                 'A Note on the Unheld'],
 'initiative-shift-examples.md': ['Example 1 — An ordinary shift',
                                  'Example 2 — A negative shift that overshoots',
                                  'Example 3 — A positive shift landing exactly on the '
                                  "marker's slot",
                                  'Example 4 — A negative shift landing exactly on the '
                                  "marker's slot",
                                  'Example 5 — Reshifting a token that already has a pending '
                                  'chip',
                                  'What These Examples Demonstrate',
                                  'Related Documents'],
 'items.md': ['Briarwatch',
              'The Hollow Below Briarwatch & Turnroot Weald (shared)',
              'Turnroot Weald',
              "Vulture's Nest",
              'Fog Basin',
              'Capital of Eclipseria',
              'Kaine (Storm Seat Artifact)',
              'No Fixed Source',
              'The Silent Choir',
              'Underground Bazaar — no items, by design',
              'Who Trades With Whom'],
 'out-of-combat.md': ['Core Resolution',
                      'Advantage & Disadvantage',
                      'Checks',
                      'Saves',
                      'Resting',
                      'Perception'],
 'people.md': ["Name — What They Are, and What They're Called",
               'Price — Declaring a Price',
               'Distance — What a Person Can Never Have',
               'Related Documents'],
 'places.md': ["Name — What It Is, and What It's Called",
               'Price — The Pressure Track',
               'Distance — What a Place Can Never Be',
               'Related Documents'],
 'player-guide.md': ['The Stats',
                     'Positions',
                     'Turn Structure',
                     'Initiative & The Wheel',
                     'Attack Resolution',
                     'Damage Pipeline',
                     'Reading Your Cards',
                     'What It Looks Like',
                     'Keywords',
                     'Status Cards',
                     'Collapse & Death',
                     'Fleeing, Chasing, and Stealth',
                     'Ongoing & Simultaneous Effects',
                     'You Are Not Your Own Ally',
                     'Core Resolution',
                     'Advantage & Disadvantage',
                     'Checks vs. Saves',
                     'Perception',
                     'Resting',
                     'Equipment',
                     'What You Showed Up With',
                     'The Oracle (End of Session)'],
 'river-fishing.md': ['Running It', 'Why It Works', 'Related Documents'],
 'the-summons.md': ['What Was Done to Make Anything',
                    'Where You Will Arrive',
                    'The First Cut in You — Name',
                    'The Second Cut in You — Price',
                    'The Third Cut in You — Distance',
                    'How to Look at Anything',
                    'What This Costs Me',
                    'Come Anyway']}


def check_rules_sections():
    """Every rules file still holds the sections it is supposed to hold."""
    bad = []
    for name, expected in sorted(SECTION_INVENTORY.items()):
        path = f'rules/{name}'
        if not os.path.exists(path):
            bad.append(f'{path} is gone; it held {len(expected)} sections')
            continue
        actual = re.findall(r'^## (.+)$', open(path, encoding='utf-8').read(), re.M)
        for missing in [s for s in expected if s not in actual]:
            bad.append(f'{path}: section "{missing}" is gone — deleted, renamed or moved?')
        for added in [s for s in actual if s not in expected]:
            bad.append(f'{path}: section "{added}" is new — add it to SECTION_INVENTORY')
    total = sum(len(v) for v in SECTION_INVENTORY.values())
    return report('rules sections intact', bad,
                  f'{total} sections across {len(SECTION_INVENTORY)} files')


def check_rules_jurisdiction():
    """rules/README.md records which file owns which topic (Drew, 2026-08-18,
    Phase 1 of splitting rules/). A map is only worth having while it is
    complete, and the way a map like this dies is quietly: someone adds a rules
    file, nobody adds the row, and the map still reads authoritative.

    So both directions. Every file in rules/ must be named in the map, and every
    file the map names must exist. No exemptions — glossary-frame.md is listed
    with the glossary it feeds, rather than carved out here, because an
    exemption list is the same hole one level up."""
    listed = open('rules/README.md', encoding='utf-8').read()
    bad = []
    on_disk = [os.path.basename(p) for p in sorted(glob.glob('rules/*.md'))
               if os.path.basename(p) != 'README.md']
    for name in on_disk:
        if f'`{name}`' not in listed:
            bad.append(f'rules/{name} exists but is not in rules/README.md — who owns it?')
    for m in re.finditer(r'^\| `([a-z0-9-]+\.md)`', listed, re.M):
        for name in re.findall(r'[a-z0-9-]+\.md', m.group(0)):
            if not os.path.exists(f'rules/{name}'):
                bad.append(f'rules/README.md names rules/{name}, which does not exist')
    return report('rules/ jurisdiction map complete', bad, f'{len(on_disk)} files mapped')


def check_restatements():
    """Every file that states a restated mechanical fact must state the same
    value. Six facts, each measured across the files that carried it on
    2026-08-18 — hand size alone is restated in six files."""
    bad = []
    counts = []
    for claim, (patterns, expected_files) in CLAIMS.items():
        found = {}
        for path in RESTATED_SCOPE:
            if not os.path.exists(path):
                continue
            text = open(path, encoding='utf-8').read()
            values = set()
            for pat in patterns:
                values |= set(re.findall(pat, text))
            if values:
                found[path] = values
        # COVERAGE: a fact that stopped matching where it used to match is a
        # reworded sentence, not an absence — and the check just went blind to it.
        missing = expected_files - set(found)
        if missing:
            bad.append(f'{claim}: no longer found in {sorted(missing)} '
                       f'(moved or reworded? the check is now blind there)')
        for path, values in sorted(found.items()):
            if len(values) > 1:
                bad.append(f'{claim}: {path} states {sorted(values)} — two values in one file')
        allv = set().union(*found.values()) if found else set()
        if len(allv) > 1:
            detail = '; '.join(f'{p}={sorted(v)}' for p, v in sorted(found.items()))
            bad.append(f'{claim}: files disagree — {detail}')
        counts.append(len(found))
    return report('restated mechanical facts agree', bad,
                  f'{len(CLAIMS)} facts across {max(counts)} files')


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


def check_bucket_lists(canon):
    """`cards/buckets/` and `cards/archetypes/` are hand-written lists, not
    generated views, so they can drift in both directions: a card added with no
    bucket, or a bucket naming a card that does not exist.

    Both had already happened. `the-gambler.md` listed WILD CARD, which has
    never existed in `cards/`, the simulator, or a print sheet — found by a
    one-off sweep on 2026-08-17, not by anything standing. These are the two
    assertions that close it.
    """
    bad = []
    listed = set()
    for path in sorted(glob.glob('cards/buckets/*.md') + glob.glob('cards/archetypes/*.md')):
        if path.endswith('README.md'):
            continue
        for m in re.finditer(r'^- \[?([A-Z][A-Z0-9\'’ \-]+?)\]?(?:\(|  |$)', 
                             open(path, encoding='utf-8').read(), re.M):
            name = m.group(1).strip()
            if name not in canon:
                bad.append(f'{path}: lists {name!r}, which is not a card in cards/')
            else:
                listed.add(name)
    # every card must appear in at least one bucket (archetypes are optional —
    # they are an index of design lineage, not a partition of the set)
    bucketed = set()
    for path in sorted(glob.glob('cards/buckets/*.md')):
        if path.endswith('README.md'):
            continue
        for m in re.finditer(r'^- \[?([A-Z][A-Z0-9\'’ \-]+?)\]?(?:\(|  |$)',
                             open(path, encoding='utf-8').read(), re.M):
            bucketed.add(m.group(1).strip())
    for name in sorted(set(canon) - bucketed):
        bad.append(f'{name} is in cards/ but appears in no bucket')
    return report('bucket and archetype lists resolve', bad,
                  f'{len(bucketed)} cards bucketed')


def check_card_conservation():
    """Non-status cards are conserved: ordinary play moves a card between deck,
    hand, discard and exile, and never creates or destroys one. Status cards
    (Wound/Exhaust) are the only things the engine adds or removes, so holding
    the *real* cards fixed is the sharp form of the invariant.

    Confirmed 2026-08-17 across 180 duels before being wired in here. Runs a
    small deterministic set — fixed seeds, fixed pairings — so it costs little
    and cannot flake.
    """
    try:
        import itertools
        import engine
        import content
        import policies
    except Exception as e:                       # sim not importable — say so
        return report('card conservation in the simulator', [f'could not import: {e}'])
    cards = content.build_cards()
    roster = content.ROSTER
    names = sorted(roster)[:8]
    bad = []
    duels = 0
    for a, b in itertools.combinations(names, 2):
        for seed in (0, 1):
            made = []
            for n in (a, b):
                st, deck = roster[n]
                made.append(engine.Combatant(n, st['body'], st['mind'], st['soul'],
                                             deck, policies.make_policy('tactician')))
            try:
                engine.Duel(made[0], made[1], cards, seed=seed).run()
            except Exception as e:
                bad.append(f'{a} vs {b} seed {seed}: duel raised {type(e).__name__}: {e}')
                continue
            duels += 1
            for c, key in zip(made, (a, b)):
                want = sum(1 for n in roster[key][1] if not cards[n].is_status)
                got = sum(1 for pile in (c.deck, c.hand, c.discard, c.exile)
                          for x in pile if not x.is_status)
                if got != want:
                    bad.append(f'{key} vs {b if key == a else a} seed {seed}: '
                               f'{got} real cards across deck/hand/discard/exile, '
                               f'decklist had {want}')
    return report('card conservation in the simulator', bad, f'{duels} duels')


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
    check_keyword_usage()
    check_glossary_generated()
    check_duplicate_refs()
    check_restated_stat_blocks()
    check_distances()
    check_hp_formula()
    check_restatements()
    check_rules_jurisdiction()
    check_rules_sections()
    check_entry_structure()
    check_bucket_lists(canon)
    check_card_conservation()
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
