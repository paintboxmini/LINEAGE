#!/usr/bin/env python3
"""Content conservation across a restructure — the snapshot half of an invariant.

`agent-tools/invariants.md` states: *a pure move loses no content line and
duplicates none.* That held on 2026-08-17's entry-sorting pass, but it was
verified by counting lines in a throwaway script, which proves only that the
totals matched — not that the same lines came out the other side. Two bugs that
cancel are invisible to a total.

This is the standing tool that version replaced. It cannot live in `verify.py`,
because conservation is a property of a *transition*: it needs a before state.
So it is two commands, run either side of a move:

    python3 agent-tools/conserve.py snapshot 'bestiary/**/*.md' 'characters/**/*.md'
    ... do the restructure ...
    python3 agent-tools/conserve.py check

Snapshot defaults to `.conserve-snapshot.json` at the repo root (gitignored) and
remembers its own scope, so `check` takes no arguments in the normal case.

What it compares: the multiset of normalized content lines. Normalization strips
indentation and collapses internal whitespace, so reflowing a list or changing a
bullet's nesting is not a loss. Pure structure carries no content and is dropped
entirely — horizontal rules, table separator rows, code fences.

Three outcomes, and only two of them fail:

  LOST        a line present before and gone after, or present fewer times.
              Always a failure. This is the one that matters.
  DUPLICATED  a non-heading line that now appears more times than it did.
              Always a failure. Three separate times in one session a
              reference-rewrite regex silently duplicated a block, and a
              line-count check would have caught none of them, because the
              duplicate arrived in the same pass that moved the original.
  ADDED       a line that did not exist before. Never a failure — a restructure
              legitimately writes new navigation. Reported so it can be read.

On a deliberate edit rather than a pure move, LOST is expected — read the list and
confirm every entry was meant to go. Stripping the hand-typed counts out of the
glossary reported 30 lost and 29 added: the 29 renamed headers plus the one
deleted paragraph, and no definition body line among them. That is the check
earning its keep on an edit, not just on a move.

Headings are exempt from DUPLICATED on purpose. Splitting one file into four
legitimately repeats `## Contents` four times, and duplicate headings *within* a
file are already `verify.py`'s `check_entry_structure`. Cross-file repetition is
the expected shape, not a defect.

    python3 agent-tools/conserve.py --selftest

runs the negative test: it injects one deletion and one duplication into a real
snapshot and asserts both are caught. A negative test that does not confirm it
actually triggered the fault is the fourth-most-common bug in this repo's
history — see `agent-tools/invariants.md`.
"""

import argparse
import collections
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_SNAPSHOT = os.path.join(ROOT, '.conserve-snapshot.json')

# Lines that are pure structure. They carry no content, and a restructure moves
# them around freely, so counting them would produce noise that buries the real
# signal.
STRUCTURAL = (
    lambda s: set(s) <= set('-*_ ') and len(s.replace(' ', '')) >= 3,   # --- *** ___
    lambda s: s.startswith('|') and set(s) <= set('|-: '),              # table rule
    lambda s: s.startswith('```'),                                      # code fence
)

MAX_ORIGINS = 5


def normalize(line):
    """Collapse a raw line to its content, or None if it carries none."""
    s = ' '.join(line.split())
    if not s:
        return None
    for is_structural in STRUCTURAL:
        if is_structural(s):
            return None
    return s


def is_heading(s):
    return s.startswith('#')


def collect(patterns):
    """Return (Counter of normalized lines, {line: [origin files]}, files read)."""
    counts = collections.Counter()
    origins = collections.defaultdict(list)
    files = []
    for pattern in patterns:
        for path in sorted(glob.glob(os.path.join(ROOT, pattern), recursive=True)):
            if not os.path.isfile(path):
                continue
            rel = os.path.relpath(path, ROOT)
            files.append(rel)
            with open(path, encoding='utf-8') as fh:
                for raw in fh:
                    s = normalize(raw)
                    if s is None:
                        continue
                    counts[s] += 1
                    if len(origins[s]) < MAX_ORIGINS and rel not in origins[s]:
                        origins[s].append(rel)
    return counts, origins, files


def cmd_snapshot(args):
    counts, origins, files = collect(args.patterns)
    if not files:
        print(f'no files matched: {" ".join(args.patterns)}', file=sys.stderr)
        return 1
    payload = {
        'scope': args.patterns,
        'files': files,
        'lines': {s: [n, origins[s]] for s, n in counts.items()},
    }
    with open(args.snapshot, 'w', encoding='utf-8') as fh:
        json.dump(payload, fh)
    print(f'snapshot  {len(files)} files, {sum(counts.values())} content lines '
          f'({len(counts)} distinct)  ->  {os.path.relpath(args.snapshot, ROOT)}')
    return 0


def compare(before_lines, before_origins, after_counts):
    """Return (lost, duplicated, added) as lists of (line, detail)."""
    lost, duplicated, added = [], [], []
    for s, n in before_lines.items():
        m = after_counts.get(s, 0)
        if m < n:
            where = ', '.join(before_origins.get(s, [])) or 'unknown'
            gone = 'gone' if m == 0 else f'{n} -> {m}'
            lost.append((s, f'{gone}   was in: {where}'))
        elif m > n and not is_heading(s):
            duplicated.append((s, f'{n} -> {m}'))
    for s, m in after_counts.items():
        if s not in before_lines:
            added.append((s, ''))
    return lost, duplicated, added


def show(label, items, limit=None):
    print(f'\n{label}  ({len(items)})')
    shown = items if limit is None else items[:limit]
    for s, detail in shown:
        text = s if len(s) <= 110 else s[:107] + '...'
        print(f'    {text}')
        if detail:
            print(f'        {detail}')
    if limit is not None and len(items) > limit:
        print(f'    ... and {len(items) - limit} more')


def cmd_check(args):
    if not os.path.exists(args.snapshot):
        print(f'no snapshot at {args.snapshot} — run `snapshot` first', file=sys.stderr)
        return 1
    with open(args.snapshot, encoding='utf-8') as fh:
        payload = json.load(fh)
    patterns = args.patterns or payload['scope']
    before_lines = {s: v[0] for s, v in payload['lines'].items()}
    before_origins = {s: v[1] for s, v in payload['lines'].items()}
    after_counts, _, after_files = collect(patterns)

    lost, duplicated, added = compare(before_lines, before_origins, after_counts)

    print(f'before: {len(payload["files"])} files, {sum(before_lines.values())} content lines')
    print(f'after:  {len(after_files)} files, {sum(after_counts.values())} content lines')

    # Every lost line, in full, always. A conservation tool that truncates its
    # failure list is telling you the thing you most need to read is elsewhere.
    if lost:
        show('LOST', lost)
    if duplicated:
        show('DUPLICATED', duplicated)
    if added:
        show('ADDED (informational)', added, limit=None if args.verbose else 20)

    print()
    if lost or duplicated:
        print(f'FAIL  content not conserved  ({len(lost)} lost, {len(duplicated)} duplicated)')
        return 1
    print(f'PASS  content conserved  ({len(added)} new lines added, 0 lost, 0 duplicated)')
    return 0


def cmd_selftest(args):
    """Prove the check fires. Both faults are injected into a real snapshot."""
    patterns = ['agent-tools/*.md']
    counts, origins, files = collect(patterns)
    if not files:
        print('selftest: no files matched', file=sys.stderr)
        return 1
    before = dict(counts)

    # Pick two real, distinct, non-heading lines from the actual corpus so the
    # faults are the shape the real thing would take, not synthetic strings.
    candidates = [s for s in sorted(before) if not is_heading(s) and before[s] == 1]
    if len(candidates) < 2:
        print('selftest: corpus too small to inject both faults', file=sys.stderr)
        return 1
    victim, twin = candidates[0], candidates[-1]

    after = collections.Counter(before)
    del after[victim]      # a line vanishes
    after[twin] += 1       # a line is copied

    lost, duplicated, added = compare(before, origins, after)

    ok = True
    if not any(s == victim for s, _ in lost):
        print(f'selftest FAIL: deletion of {victim!r} was not reported as LOST')
        ok = False
    if not any(s == twin for s, _ in duplicated):
        print(f'selftest FAIL: duplication of {twin!r} was not reported as DUPLICATED')
        ok = False

    # And the inverse: an untouched corpus must report clean, or a passing
    # result means nothing.
    clean_lost, clean_dup, _ = compare(before, origins, collections.Counter(before))
    if clean_lost or clean_dup:
        print(f'selftest FAIL: unchanged corpus reported {len(clean_lost)} lost, '
              f'{len(clean_dup)} duplicated')
        ok = False

    # A heading duplicated is deliberately not a failure. Assert that too, so
    # the exemption is tested rather than merely written down.
    headings = [s for s in sorted(before) if is_heading(s)]
    if headings:
        h_after = collections.Counter(before)
        h_after[headings[0]] += 1
        _, h_dup, _ = compare(before, origins, h_after)
        if any(s == headings[0] for s, _ in h_dup):
            print(f'selftest FAIL: heading {headings[0]!r} was flagged as DUPLICATED')
            ok = False

    if ok:
        print(f'selftest PASS  ({len(files)} files, {sum(before.values())} lines) — '
              f'deletion caught, duplication caught, heading exemption honored, '
              f'unchanged corpus clean')
    return 0 if ok else 1


def main():
    p = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    p.add_argument('--snapshot', default=DEFAULT_SNAPSHOT)
    p.add_argument('--selftest', action='store_true')
    sub = p.add_subparsers(dest='cmd')

    s = sub.add_parser('snapshot', help='record content lines before a restructure')
    s.add_argument('patterns', nargs='+')

    c = sub.add_parser('check', help='compare the tree against the snapshot')
    c.add_argument('patterns', nargs='*')
    c.add_argument('-v', '--verbose', action='store_true', help='list every added line')

    args = p.parse_args()
    if args.selftest:
        return cmd_selftest(args)
    if args.cmd == 'snapshot':
        return cmd_snapshot(args)
    if args.cmd == 'check':
        args.verbose = getattr(args, 'verbose', False)
        return cmd_check(args)
    p.print_help()
    return 1


if __name__ == '__main__':
    sys.exit(main())
