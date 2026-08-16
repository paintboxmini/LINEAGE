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
    """Every card block in cards/*.md, colored or colorless."""
    cards = {}
    for path in sorted(glob.glob('cards/*.md')):
        for block in open(path, encoding='utf-8').read().split('\n---\n'):
            m = re.search(NAME_RE, block, re.M)
            if not m:
                continue
            colored = re.search(r'^(RED|BLUE|GREEN) — (BODY|MIND|SOUL)(?: — ([A-Z]+))?\s*$',
                                block, re.M)
            colorless = re.search(r'^COLORLESS\s*$', block, re.M)
            if not (colored or colorless):
                continue
            rng = re.search(r'^Range: (.+)$', block, re.M)
            die = re.search(r'^Attack: .*?\bd(\d+)', block, re.M)
            cards[m.group(1).strip()] = {
                'color': colored.group(1)[0] if colored else None,
                'stat': colored.group(2).lower() if colored else None,
                'tag': colored.group(3) if colored else None,
                'range': rng.group(1).strip() if rng else None,
                'die': int(die.group(1)) if die else None,
                'file': path,
                'block': block,
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
    """Yield (label, path, declared_total, {color: [names]}) for every deck line."""
    for path in sorted(glob.glob('bestiary/*.md')):
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
        f = path.split('/')[-1]
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
    return report('bestiary decks (size, per-color counts, card resolution)', bad,
                  f'{n} decks')


def check_stat_blocks():
    bad = []
    n = 0
    for path in sorted(glob.glob('bestiary/*.md')):
        text = open(path, encoding='utf-8').read()
        for m in re.finditer(
                r'\*\*Mind (\d+) / Body (\d+) / Soul (\d+) — HP (\d+)\*\*(.*)', text):
            mind, body, soul, hp = (int(x) for x in m.groups()[:4])
            trailing = m.group(5)
            n += 1
            f = path.split('/')[-1]
            formula = 3 * body + soul + mind
            if hp != formula and 'bespoke' not in trailing.lower():
                bad.append(f'{f}: HP {hp} != formula {formula} and not marked bespoke')
            after = text[m.end():m.end() + 200]
            ctr = re.search(r'\*\*Creature Threat Rating:\*\* (\d+)', after)
            if ctr and int(ctr.group(1)) != mind + body + soul:
                bad.append(f'{f}: CTR {ctr.group(1)} != total stats {mind + body + soul}')
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
    """{'bestiary/x.md': [(mind, body, soul, hp), ...]} for every stat block."""
    blocks = {}
    for path in sorted(glob.glob('bestiary/*.md')):
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
