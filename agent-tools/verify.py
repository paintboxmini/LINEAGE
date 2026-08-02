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
            formula = 2 * body + 9
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
        if path.startswith('archives/'):
            continue
        text = open(path, encoding='utf-8').read()
        for m in re.finditer(r'^\*\*Cards:\*\* `([^`]+)`', text, re.M):
            if not os.path.exists(m.group(1)) and 'filename' not in m.group(1):
                bad.append(f'{path} -> {m.group(1)} (missing)')
        # Directory-qualified paths only: bare `red-team.md` is prose shorthand.
        for m in re.finditer(r'`((?:cards|bestiary|rules|quests|locations|characters|items|'
                             r'world|mythology|factions|Oracle|agent-tools|playtesting)/'
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
    for meth in ('deal', 'insert_exhaust', 'insert_wound'):
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
