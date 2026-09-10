#!/usr/bin/env python3
"""Cross-reference checks for the repo's prose and card data.

Three kinds of rot this catches, all of which have actually happened:

  1. Broken document references. A `path/to/file.md` in backticks pointing at
     a file that isn't there. Usually the target was deliberately deleted and
     the citations were left behind — 43 of these had accumulated by
     2026-09-10, across 17 targets, invisible until something looked.

  2. Decklist references to cards that don't exist. Renaming a card breaks
     every creature that ran it, silently, because nothing reads those lists
     but a human. This is the check that caught RECOVER, FORESEEN, YOU'RE
     NEXT and SEISMIC REDIRECT after renames.

  3. Duplicate card names. `printing/generate-cards.py` resolves a set's
     fixed card list by name into a first-wins dict, so two cards sharing a
     name means one of them silently prints in the other's place. The Red and
     Green BRACE did exactly that to the Oracle deck.

Usage:
    python3 agent_tools/check-repo.py            # report, exit 1 if anything is wrong
    python3 agent_tools/check-repo.py --quiet    # only print problems

A line carrying `<!-- link-check: ignore -->` is skipped by check 1, for the
rare case where a path is the subject of a sentence rather than a citation.
"""

import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'combatsimulations'))
import cards as C  # noqa: E402

SKIP_DIRS = ('printing', 'agent_tools', '.git')
DOC_REF = re.compile(r'`([A-Za-z0-9_\-/. ]+\.md)`')
DECK = re.compile(r'Deck\s*\(([^)]*)\)', re.S)


def markdown_files():
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        for name in sorted(files):
            if name.endswith('.md'):
                yield os.path.relpath(os.path.join(root, name), REPO)


def check_links():
    out = []
    for f in markdown_files():
        with open(os.path.join(REPO, f), encoding='utf-8', errors='ignore') as fh:
            for i, line in enumerate(fh, 1):
                if 'link-check: ignore' in line:
                    continue
                for m in DOC_REF.finditer(line):
                    target = m.group(1).strip()
                    if not os.path.exists(os.path.join(REPO, target)):
                        out.append((f, i, target))
    return out


def check_decklists(names):
    out = []
    for f in markdown_files():
        text = open(os.path.join(REPO, f), encoding='utf-8', errors='ignore').read()
        for m in DECK.finditer(text):
            body = re.sub(r'\*\(\s*\w+\s*\)\*', '', m.group(1))
            for raw in re.split(r'[,·]', body):
                n = re.sub(r'[*_`]', '', raw).strip()
                n = re.sub(r'^\d+\s*[x×]\s*', '', n).strip()
                if not n or n[0].isdigit():
                    continue
                if n.upper() not in names:
                    out.append((f, n))
    return out


def check_duplicate_names(all_cards):
    seen = {}
    for c in all_cards:
        seen.setdefault(c.name, []).append(c.source)
    return {n: v for n, v in seen.items() if len(v) > 1}


def main():
    quiet = '--quiet' in sys.argv
    all_cards = C.load()
    names = {c.name.upper() for c in all_cards}

    links = check_links()
    decks = check_decklists(names)
    dupes = check_duplicate_names(all_cards)
    problems = len(links) + len(decks) + len(dupes)

    if links:
        print(f"\nBROKEN DOCUMENT REFERENCES ({len(links)}):")
        for f, i, t in links:
            print(f"  {f}:{i} -> {t}")
    if decks:
        print(f"\nDECKLISTS NAMING CARDS THAT DON'T EXIST ({len(decks)}):")
        for f, n in decks:
            print(f"  {f} -> {n}")
    if dupes:
        print(f"\nDUPLICATE CARD NAMES ({len(dupes)}):")
        for n, srcs in dupes.items():
            print(f"  {n} -> {', '.join(srcs)}")

    if problems == 0 and not quiet:
        print(f"Clean — {len(all_cards)} cards, "
              f"{sum(1 for _ in markdown_files())} documents, no broken references.")
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
