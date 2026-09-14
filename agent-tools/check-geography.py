#!/usr/bin/env python3
"""Checks that directional claims about places agree with the map.

One job. `world/geography-overview.md`, Bearing Table, owns where every place
sits relative to every other. This reads that table and then reads every
directional claim in the repo back against it.

Why it exists: on 2026-09-11 a line read "the forest advances north — up the
ground between it and the Kings Road, along the spoke that runs from Turnroot
Weald to Eclipseria." The Capital is northeast of the Weald, so the sentence
contradicted itself inside one clause, and nothing mechanical could see it.
The reference checker only proves that names resolve, never that claims hold.

Two severities, because they are worth very different amounts:

  CONFLICT   — the claim names a subject, a bearing and a reference, and the
               table says a different bearing. This is a real error and the
               only thing that fails the run. A table row marked "conflict"
               is never adjudicated against — claims about a place the map
               itself hasn't settled drop to UNVERIFIED instead.
  UNVERIFIED — a directional claim the table can't adjudicate, because the
               subject isn't in it, or the sentence doesn't name one. Mostly
               fine, occasionally a place quietly acquiring a position nobody
               wrote down. Shown with --unverified; never fails the run.

A claim is read as `<bearing> of|from <Place>`. The subject is the nearest
known place named earlier in the same line; failing that, in a `places/X.md`  # link-check: ignore
file, the place that file is about — which is what makes opening lines like
"Farmland a day's travel west of Vulture's Nest" checkable.

Usage:
    python3 agent-tools/check-geography.py               # conflicts, exit 1 on any
    python3 agent-tools/check-geography.py --strict      # also flag approximations
    python3 agent-tools/check-geography.py --unverified  # also list the soft ones
    python3 agent-tools/check-geography.py --table       # print the parsed map and stop

Default tolerance is deliberate: adjacent bearings agree. Saying north when
the map says northeast is imprecise, not wrong, and flagging it by default
would bury the real errors. `--strict` flags it, and is the setting to run
when an approximation has had time to drift into a load-bearing fact.

A line carrying `<!-- geo-check: ignore -->` is skipped, for prose where a
compass word isn't a claim ("the northernmost water", a card's flavour text).

What this does NOT do, stated plainly because the limits matter more than the
coverage: distances, travel times, and whether a route is walkable in the days
a file gives it. Building the table is what exposed the Briarwatch conflict —
a day west of Vulture's Nest and also on the Weald's edge, ~13 days apart —
but a person had to read the two claims together to see it; no bearing row
contradicted another. And it only sees claims written as
`<bearing> of|from <Place>`. The sentence that prompted this tool —
"advances north ... along the spoke that runs from Turnroot Weald to
Eclipseria" — has no such phrase in it, so this would not have caught it. What
would have is the table itself existing: the map now lives in one place, so
writing that sentence means opening the file that would have contradicted it.
"""

import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEO = os.path.join('world', 'geography-overview.md')
SKIP_DIRS = ('printing', 'agent-tools', 'combat-simulations', '.git', 'archives')

BEARINGS = {
    'north': (0, 1), 'south': (0, -1), 'east': (1, 0), 'west': (-1, 0),
    'northeast': (1, 1), 'northwest': (-1, 1),
    'southeast': (1, -1), 'southwest': (-1, -1),
}

# Aliases the world actually uses in prose, mapped to the table's canonical name.
ALIASES = {
    'eclipseria': 'Eclipseria', 'the capital': 'Eclipseria', 'the citadel': 'Eclipseria',
    "vulture's nest": "Vulture's Nest", 'vultures nest': "Vulture's Nest",
    'the nest': "Vulture's Nest",
    'glasslight reach': 'Glasslight Reach', 'glasslight': 'Glasslight Reach',
    'the reach': 'Glasslight Reach',
    'turnroot weald': 'Turnroot Weald', 'turnroot': 'Turnroot Weald',
    'the weald': 'Turnroot Weald',
    'ashfall wastes': 'Ashfall Wastes', 'the wastes': 'Ashfall Wastes',
    'ashfall': 'Ashfall Wastes',
    'abyssal ruins': 'Abyssal Ruins', 'the ruins': 'Abyssal Ruins',
    'briarwatch': 'Briarwatch', 'canille': 'Canille', 'pneum': 'Pneum',
    'apnea': 'Apnea', 'the coil': 'The Coil', 'the roadhouse': 'The Roadhouse',
}

# places/<file>.md → the place that file is about, for subject fallback.
FILE_SUBJECT = {
    'briarwatch': 'Briarwatch', 'canille': 'Canille', 'pneum': 'Pneum',
    'apnea': 'Apnea', 'the-coil': 'The Coil', 'vultures-nest': "Vulture's Nest",
    'glasslight-reach': 'Glasslight Reach', 'turnroot-weald': 'Turnroot Weald',
    'ashfall-wastes': 'Ashfall Wastes', 'abyssal-ruins': 'Abyssal Ruins',
    'roadhouse': 'The Roadhouse',
}

BEARING_RE = re.compile(
    r'\b(north|south|east|west|northeast|north-east|northwest|north-west'
    r'|southeast|south-east|southwest|south-west)\b'
    r'(?:ern|erly)?\s+(?:of|from)\s+(?:the\s+)?([A-Z][A-Za-z\'’]*(?:\s+[A-Z][A-Za-z\'’]*)?)',
    re.I)

ROW_RE = re.compile(r'^\|\s*([^|]+?)\s*\|\s*([a-z\-]+)\s*\|\s*([^|]+?)\s*\|')


def norm_bearing(word):
    return word.lower().replace('-', '')


def canon(name):
    return ALIASES.get(name.strip().lower().rstrip('.,;:'))


def load_table():
    """Parse the Bearing Table rows out of the geography file."""
    path = os.path.join(REPO, GEO)
    text = open(path, encoding='utf-8').read()
    start = text.find('## Bearing Table')
    if start < 0:
        sys.exit(f'{GEO} has no "## Bearing Table" section — nothing to check against.')
    end = text.find('\n### ', start)
    body = text[start:end if end > 0 else len(text)]

    table, conflicted = {}, set()
    for line in body.split('\n'):
        m = ROW_RE.match(line)
        if not m:
            continue
        place, bearing, ref = m.group(1), norm_bearing(m.group(2)), m.group(3)
        if bearing not in BEARINGS:
            continue
        ref_c = canon(ref) or ref.strip()
        place_c = canon(place) or place.strip()
        table[(place_c, ref_c)] = bearing
        if 'conflict' in line.lower():
            conflicted.add((place_c, ref_c))
    return table, conflicted


def markdown_files():
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        for f in sorted(files):
            if f.endswith('.md'):
                yield os.path.relpath(os.path.join(root, f), REPO)


def subject_for(line, upto, path):
    """Nearest known place named before the bearing; else the file's own place."""
    best = None
    for alias, name in ALIASES.items():
        i = line.lower().rfind(alias, 0, upto)
        if i >= 0 and (best is None or i > best[0]):
            best = (i, name)
    if best:
        return best[1]
    if path.startswith('places' + os.sep):
        return FILE_SUBJECT.get(os.path.basename(path)[:-3])
    return None


def opposed(a, b):
    """True when two bearings point in contradictory directions.

    North vs northeast is not opposed — the table is rough compass sense, and
    adjacent bearings are the same gesture. North vs south, or northeast vs
    southwest, is a real contradiction. --strict treats any mismatch at all as
    one, which is the setting that catches an approximation drifting.
    """
    ax, ay = BEARINGS[a]
    bx, by = BEARINGS[b]
    return (ax * bx + ay * by) < 0 or (ax == -bx and ay == -by)


REVERSE = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east',
           'northeast': 'southwest', 'southwest': 'northeast',
           'northwest': 'southeast', 'southeast': 'northwest'}


def expected(table, subj, ref):
    """The map's bearing for subj-from-ref, direct or by flipping the stored row.

    The table stores each pair once. "Turnroot Weald is southwest of
    Eclipseria" also settles "Eclipseria is northeast of Turnroot Weald", and
    a claim written the second way has to be checked against the first.
    """
    if (subj, ref) in table:
        return table[(subj, ref)], (subj, ref)
    if (ref, subj) in table:
        return REVERSE[table[(ref, subj)]], (ref, subj)
    return None, None


def main():
    show_unverified = '--unverified' in sys.argv
    strict = '--strict' in sys.argv
    table, conflicted = load_table()

    if '--table' in sys.argv:
        for (place, ref), bearing in sorted(table.items()):
            mark = '  (CONFLICTED)' if (place, ref) in conflicted else ''
            print(f'  {place} is {bearing} of {ref}{mark}')
        return 0

    conflicts, unverified = [], []
    for path in markdown_files():
        if path == GEO:
            continue
        for n, line in enumerate(open(os.path.join(REPO, path), encoding='utf-8'), 1):
            if 'geo-check: ignore' in line:
                continue
            for m in BEARING_RE.finditer(line):
                bearing = norm_bearing(m.group(1))
                ref = canon(m.group(2))
                if not ref:
                    continue
                subj = subject_for(line, m.start(), path)
                if subj is None or subj == ref:
                    unverified.append((path, n, subj, bearing, ref))
                    continue
                actual, key = expected(table, subj, ref)
                if actual is None or key in conflicted:
                    unverified.append((path, n, subj, bearing, ref))
                    continue
                wrong = bearing != actual if strict else opposed(bearing, actual)
                if wrong:
                    conflicts.append((path, n, subj, bearing, ref, actual))

    if conflicts:
        print(f'DIRECTIONAL CLAIMS THAT CONTRADICT THE MAP ({len(conflicts)}):')
        for path, n, subj, said, ref, actual in conflicts:
            print(f'  {path}:{n} -> says {subj} is {said} of {ref}; map says {actual}')
    if show_unverified and unverified:
        print(f'\nUNVERIFIED DIRECTIONAL CLAIMS ({len(unverified)}):')
        for path, n, subj, bearing, ref in unverified:
            who = subj or '(no subject in line)'
            print(f'  {path}:{n} -> {who}, {bearing} of {ref}')
    if not conflicts:
        extra = '' if show_unverified else f', {len(unverified)} unverified (--unverified)'
        print(f'Clean — {len(table)} bearings on the map, no contradictions{extra}.')
    return 1 if conflicts else 0


if __name__ == '__main__':
    sys.exit(main())
