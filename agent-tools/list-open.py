#!/usr/bin/env python3
"""Every open question in the repo, in one place.

The repo flags unsettled things *in the file they belong to*, which is the
right place for them — the question sits next to the thing it is about, and
nobody has to keep an index in sync. The cost is that there is no way to see
all of them at once, and on 2026-09-22 there were thirty such sections across
twenty-odd files. This reads them rather than duplicating them.

**It is an inventory, not a check.** The other three scripts in this folder
exit 1 on a finding because a finding means something is wrong. An open
question is not wrong, so this always exits 0.

Two kinds, kept apart, because mixing them is what makes a list like this
useless:

  DECISIONS WAITING   `## Not Yet Set`, `## Open`, `## Still open`
                      Somebody has to choose. Usually Drew.

  HOOKS LEFT OPEN     `## Open Hooks`, `## Open Threads`
                      Deliberately unwritten, for a GM to take or ignore.
                      These are features. They are not a backlog.

    python3 agent-tools/list-open.py                # both, grouped by folder
    python3 agent-tools/list-open.py --decisions    # just the choices
    python3 agent-tools/list-open.py --hooks        # just the invitations
    python3 agent-tools/list-open.py --count        # one line per file
"""

import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {'archives', '__pycache__', '.git', 'node_modules'}

DECISION = re.compile(r'^##+\s+(not yet set|open|still open)\b', re.I)
HOOK = re.compile(r'^##+\s+(open hooks|open threads|open questions)\b', re.I)
# "## Opening Conditions" and "## Opening Scene" are different words entirely.
NOT_OPEN = re.compile(r'^##+\s+opening\b', re.I)


def walk():
    for root, dirs, files in os.walk(REPO):
        dirs[:] = sorted(d for d in dirs if d not in SKIP and not d.startswith('.'))
        for f in sorted(files):
            if f.endswith('.md'):
                yield os.path.relpath(os.path.join(root, f), REPO)


def sections(path):
    """(kind, heading, [bullet lines]) for each open section in one file."""
    with open(os.path.join(REPO, path), encoding='utf-8') as fh:
        lines = fh.read().split('\n')
    out, cur = [], None
    for ln in lines:
        if ln.startswith('#'):
            if cur:
                out.append(cur)
                cur = None
            if NOT_OPEN.match(ln):
                continue
            # HOOK first: "## Open Hooks" also matches DECISION's bare "open".
            kind = 'hook' if HOOK.match(ln) else ('decision' if DECISION.match(ln) else None)
            if kind:
                cur = (kind, ln.lstrip('#').strip(), [])
        elif cur is not None and ln.strip():
            cur[2].append(ln.rstrip())
    if cur:
        out.append(cur)
    return out


def first_sentence(text, width=104):
    """A bullet's opening claim, with the markdown emphasis stripped off."""
    t = re.sub(r'\*\*|\*|`|~~', '', text.lstrip('-* ').strip())
    t = re.sub(r'\s+', ' ', t)
    return t if len(t) <= width else t[:width - 1].rstrip() + '…'


def main():
    want_dec = '--hooks' not in sys.argv
    want_hook = '--decisions' not in sys.argv
    counts_only = '--count' in sys.argv

    found = [(p, s) for p in walk() for s in sections(p)]
    dec = [(p, s) for p, s in found if s[0] == 'decision']
    hook = [(p, s) for p, s in found if s[0] == 'hook']

    if counts_only:
        def live(bullets):
            return [b for b in bullets
                    if b.lstrip().startswith(('-', '*'))
                    and not b.lstrip().startswith(('- ~~', '* ~~'))
                    and first_sentence(b)]

        per = {}
        for p, s in found:
            per.setdefault(p, [0, 0])
            per[p][0 if s[0] == 'decision' else 1] += len(live(s[2]))
        for p in sorted(per):
            d, h = per[p]
            bits = ', '.join(x for x in (f'{d} waiting' if d else '',
                                         f'{h} hooks' if h else '') if x)
            print(f'  {p:52} {bits}')
        print(f'\n  {len(per)} files, {sum(v[0] for v in per.values())} decisions '
              f'waiting, {sum(v[1] for v in per.values())} hooks')
        return 0

    def dump(rows, title, blurb):
        print(f'\n{title}')
        print(blurb)
        folder = None
        for p, (_, heading, bullets) in rows:
            top = p.split(os.sep)[0] if os.sep in p else '(root)'
            if top != folder:
                folder = top
                print(f'\n  {folder}/')
            print(f'    {p}  —  {heading}')
            for b in bullets:
                if not b.lstrip().startswith(('-', '*')):
                    continue
                if b.lstrip().startswith('- ~~') or b.lstrip().startswith('* ~~'):
                    continue  # struck through: settled, kept as a record
                line = first_sentence(b)
                if line:
                    print(f'        · {line}')

    if want_dec and dec:
        dump(dec, 'DECISIONS WAITING', '  Somebody has to choose. These are a backlog.')
    if want_hook and hook:
        dump(hook, '\nHOOKS LEFT OPEN ON PURPOSE',
             '  Unwritten for a GM to take or ignore. These are features, not a backlog.')

    print(f'\n  {len(dec)} sections of decisions, {len(hook)} sections of hooks, '
          f'across {len({p for p, _ in found})} files.')
    print('  Inventory, not a check — always exits 0.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
