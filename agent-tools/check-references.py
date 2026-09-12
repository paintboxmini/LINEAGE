#!/usr/bin/env python3
"""Checks that every name in this repo resolves to the thing it should.

One job, four checks. All four catch silent failures — nothing errors, nothing
looks wrong, the reference just quietly points at nothing or at the wrong
thing. All four have actually happened here.

  1. Broken document references. A backticked path pointing at a file that
     isn't there. Usually the target was deliberately deleted and
     the citations were left behind — 43 of these had accumulated by
     2026-09-10, across 17 targets, invisible until something looked.

  2. Decklist references to cards that don't exist. Renaming a card breaks
     every creature that ran it, silently, because nothing reads those lists
     but a human. This is the check that caught RECOVER, FORESEEN, YOU'RE
     NEXT and SEISMIC REDIRECT after renames.

  3. Section citations. The repo cites sections constantly — `rules/combat.md`,
     Range Matrix — and a file surviving a rename while its headings change
     leaves the path resolving and the section not. Six of these had drifted
     by 2026-09-10, including two in rules/ pointing at a section renamed
     from "Card Trading" to "The Card Economy".

  4. Duplicate card names. Not a reference itself — a uniqueness constraint —
     but it is the precondition that makes checks 2 and 3 possible to satisfy.
     `printing/generate-cards.py` resolves a set's fixed card list by name into
     a first-wins dict, so two cards sharing a name means one silently prints
     in the other's place. The Red and Green BRACE did exactly that to the
     Oracle deck.

Usage:
    python3 agent-tools/check-references.py            # report, exit 1 on problems
    python3 agent-tools/check-references.py --quiet    # only print problems

A line carrying `link-check: ignore` (in an HTML comment in Markdown, a `#`
comment in a script) is skipped by checks 1 and 3, for
the rare case where a path is the subject of a sentence rather than a citation.
"""

import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'combat-simulations'))
import cards as C  # noqa: E402

# Nothing is skipped but .git. printing/ and agent-tools/ used to be, and that
# was the hole: `../characters/frost.md` sat in a generate-cards.py comment  # link-check: ignore  # link-check: ignore
# citing a file that had never existed, and a comment is exactly where a dead
# citation survives longest, because nothing executes it.
SKIP_DIRS = ('.git',)
SOURCE_EXT = ('.md', '.py', '.sh')
DOC_REF = re.compile(r'`([A-Za-z0-9_\-/. ]+\.(?:md|py|sh))`')
# A citation is sometimes written as the command that runs the file.
CMD_PREFIX = re.compile(r'^(?:python3?|bash|sh|\./)\s+')
# A backticked path, then a section name — stop at sentence punctuation.
SECTION_REF = re.compile(r'`([A-Za-z0-9_\-/. ]+\.md)`,\s+([A-Z][A-Za-z0-9 &\'’\-]{2,44}?)(?=[.,;:—\n)]|$)')
# A heading, or the bold lead-in the repo uses for named sub-rules.
HEADING = re.compile(r'^#+\s*(.+?)\s*$|^\*\*(.+?)\*\*', re.M)
DECK = re.compile(r'Deck\s*\(([^)]*)\)', re.S)


def repo_files(exts=SOURCE_EXT):
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        for name in sorted(files):
            if name.endswith(exts):
                yield os.path.relpath(os.path.join(root, name), REPO)


def markdown_files():
    return repo_files(('.md',))


def resolve_ref(citing, target):
    """Where a cited path actually lives, or None.

    Two conventions are in use and both are correct. Prose cites from the repo
    root (`rules/combat.md` reads the same wherever it is quoted); the build
    scripts cite from their own directory (`../cards/red-body.md`, because
    that is the string they pass to open()). Try root first, then relative —
    root first so a repo-root path is never shadowed by a same-named file
    sitting beside the citation."""
    target = CMD_PREFIX.sub('', target).strip()
    if not target:
        return None
    here = os.path.dirname(citing)
    for cand in (target, os.path.normpath(os.path.join(here, target))):
        if os.path.exists(os.path.join(REPO, cand)):
            return cand
    return None


def check_links():
    out = []
    for f in repo_files():
        with open(os.path.join(REPO, f), encoding='utf-8', errors='ignore') as fh:
            for i, line in enumerate(fh, 1):
                if 'link-check: ignore' in line:
                    continue
                for m in DOC_REF.finditer(line):
                    target = m.group(1).strip()
                    if resolve_ref(f, target) is None:
                        out.append((f, i, target))
    return out


def sections_of(path):
    """Every heading and bold lead-in in a file, lowercased."""
    out = set()
    with open(path, encoding='utf-8', errors='ignore') as fh:
        for m in HEADING.finditer(fh.read()):
            head = (m.group(1) or m.group(2) or '').strip().strip('*').strip()
            if head:
                out.add(head.lower())
    return out


# "CTR 4" and the like are stat citations, not section names.
STAT_SHAPED = re.compile(r'^[A-Z]{2,}\s+\d+$')


def check_sections():
    """A cited section must exist in the file cited. A heading routinely carries
    more than the citation does — "The Boy Who Won't Calm" lives under
    "Encounter Hook — The Boy Who Won't Calm" — so containment counts, not just
    a prefix."""
    cache = {}
    out = []
    for f in repo_files():
        with open(os.path.join(REPO, f), encoding='utf-8', errors='ignore') as fh:
            for i, line in enumerate(fh, 1):
                if 'link-check: ignore' in line:
                    continue
                for m in SECTION_REF.finditer(line):
                    target, sec = m.group(1).strip(), m.group(2).strip()
                    if STAT_SHAPED.match(sec):
                        continue
                    resolved = resolve_ref(f, target)
                    if resolved is None:
                        continue          # check 1 already owns this one
                    if resolved not in cache:
                        cache[resolved] = sections_of(os.path.join(REPO, resolved))
                    cache[target] = cache[resolved]
                    low = sec.lower()
                    if not any(low in h for h in cache[target]):
                        out.append((f, i, target, sec))
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
    secs = check_sections()
    decks = check_decklists(names)
    dupes = check_duplicate_names(all_cards)
    problems = len(links) + len(secs) + len(decks) + len(dupes)

    if links:
        print(f"\nBROKEN DOCUMENT REFERENCES ({len(links)}):")
        for f, i, t in links:
            print(f"  {f}:{i} -> {t}")
    if secs:
        print(f"\nCITED SECTIONS THAT DON'T EXIST IN THE FILE CITED ({len(secs)}):")
        for f, i, t, sec in secs:
            print(f"  {f}:{i} -> {t}, {sec!r}")
    if decks:
        print(f"\nDECKLISTS NAMING CARDS THAT DON'T EXIST ({len(decks)}):")
        for f, n in decks:
            print(f"  {f} -> {n}")
    if dupes:
        print(f"\nDUPLICATE CARD NAMES ({len(dupes)}):")
        for n, srcs in dupes.items():
            print(f"  {n} -> {', '.join(srcs)}")

    if problems == 0 and not quiet:
        docs = sum(1 for _ in markdown_files())
        scripts = sum(1 for _ in repo_files(('.py', '.sh')))
        print(f"Clean — {len(all_cards)} cards, {docs} documents, "
              f"{scripts} scripts, no broken references.")
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
