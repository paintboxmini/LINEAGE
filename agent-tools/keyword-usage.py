#!/usr/bin/env python3
"""Recount how many cards use each glossary keyword, and write the result.

Why this exists: `rules/card-glossary.md` used to carry a hand-maintained
`(55)` in front of every keyword. Those numbers were a snapshot, they drifted,
and on 2026-08-03 a recount disagreed with the header on 16 keywords in both
directions — including decreases, which adding cards cannot cause. That sat
open in `unresolved-concerns.md` for two weeks and got worse, not better: by
2026-08-18 the disagreement was 21 of 29.

The root cause was never a bad regex. The counting rule itself was ambiguous in
three places, and Drew settled all three on 2026-08-18:

  1. **A conditional grant is a use.** LAST RESORT's "If your HP is 6 or less,
     gain Immunity" counts. What does *not* count is a presence *test* — "if the
     defender is Rooted" reacts to a keyword rather than applying it — or a
     negation, "ignores Evade". The old rule excluded every conditional and so
     counted Immunity at zero.
  2. **An umbrella counts its members.** Debuff and Positive Status Effects are
     defined in the glossary as lists of other keywords. A card granting Deadly
     is a card the Positive Status Effects entry covers, whether or not it says
     the words. Membership is parsed from those two definitions, so the counts
     cannot drift away from the text that defines them.
  3. **Once per card.** A keyword named on both the Effect and the Defensive
     Bonus is one card using it, not two.

The counts also left the glossary entirely. That file states it is meant to be
printed and handed to players, and a player does not need to know Evade is on 57
cards — that number is for the designer. It lives here now, generated, where
being recomputed is normal and drift is impossible.

    python3 agent-tools/keyword-usage.py            # rewrite keyword-usage.md
    python3 agent-tools/keyword-usage.py --check     # exit 1 if it is stale

`verify.py`'s `check_keyword_usage` runs the second form.
"""

import os
import re
import sys
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

KEYWORD_DIR = 'rules/keywords'
OUTPUT = 'agent-tools/keyword-usage.md'

# The lines on a card that can actually do something. Flavor text and the Range
# line cannot grant a keyword.
RULE_LINES = ('Effect:', 'Defensive Bonus:', 'Special Rule:', 'Attack:')

# Kept identical to verify.py's NAME_RE on purpose — see tally().
NAME_RE = r'^\*\*([A-Z][A-Z0-9\'’ \-,!?&]+)\*\*\s*$'

# A presence test reads the keyword off someone; it does not apply it. The verb
# cannot tell them apart — EXPOSED's "this attack has Critical" grants, while
# "if the defender has Evade" tests, and both read "has X". Scope can: a test
# lives inside an *open* conditional clause. Once that clause closes at its
# comma, what follows is the card doing something.
#   "If the defender is Staggered, this attack has Critical."
#    ^ Staggered: clause still open -> test   ^ Critical: past the comma -> grant
# Keying on the verb instead let four cases through, each a different verb the
# list would have had to grow to cover: "if target has Blind or Staggered"
# (second item in a list), "if target is already Staggered" (an adverb), "if the
# attacker received a positive Initiative Shift" (a verb not on any list). Scope
# catches all four without enumerating anything. The one exception is an
# explicit grant inside a condition, which stays a grant.
COND_OPEN = re.compile(r'\b(if|unless|while)\b[^,]*$', re.I)
GRANT = re.compile(r'\b(gain|gains|apply|applies|applied|inflict|inflicts|grant|grants|'
                   r'give|gives|add|adds|becomes?)\s+(a\s+|an\s+|the\s+)?$', re.I)


def is_test(pre):
    """Inside an open conditional, a keyword is being read unless it is being given."""
    return bool(COND_OPEN.search(pre)) and not GRANT.search(pre)


# A negation cancels or ignores the keyword rather than granting it.
NEG = re.compile(r"\b(ignores?|ignoring|cannot|can't|prevents?|instead of|does not|do not|no longer)\b[^,.;]*$", re.I)

# Stat reduction is a Debuff member with no keyword of its own — the three cards
# say "loses 1 Mind this combat" rather than naming a mechanic.
STAT_REDUCTION = re.compile(r'\bloses?\s+\d+\s+(Mind|Body|Soul)\b', re.I)


def keywords():
    """Every keyword, read from the per-keyword source files rather than the
    glossary they are built into — a tool that parses a generated artifact is one
    rebuild away from disagreeing with the thing that defines it."""
    out = []
    for path in sorted(glob.glob('rules/keywords/*.md')):
        m = re.match(r'^# (.+)\n', open(path, encoding='utf-8').read())
        if not m:
            raise SystemExit(f'{path}: no "# NAME" heading on the first line')
        out.append(m.group(1).strip())
    return out


def umbrellas(known):
    """Parse Debuff and Positive Status Effects membership from their own text,
    so a change to either definition moves the counts with it."""
    out = {}
    for name in ('Debuff', 'Positive Status Effects'):
        path = f"rules/keywords/{re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')}.md"
        if not os.path.exists(path):
            continue
        m = re.match(r'^# .+\n\n(.+)$', open(path, encoding='utf-8').read(), re.M)
        if not m:
            continue
        head = re.split(r'[—.]', m.group(1))[0]
        members = [k for k in known if k != name and re.search(rf'\b{re.escape(k)}\b', head)]
        out[name] = (members, 'stat reduction' in head)
    return out


def uses(card_text, keyword):
    """Does this card apply this keyword? Once per card, never twice."""
    base = re.sub(r'( X| \[Color\])$', '', keyword)
    for line in card_text.split('\n'):
        if not line.startswith(RULE_LINES):
            continue
        for m in re.finditer(rf'\b{re.escape(base)}\b', line, re.I):
            pre = line[:m.start()]
            if is_test(pre) or NEG.search(pre):
                continue
            return True
    return False


def reduces_stat(card_text):
    return any(STAT_REDUCTION.search(l) for l in card_text.split('\n')
               if l.startswith(RULE_LINES))


def name_of(path):
    m = re.search(r'^\*\*(.+?)\*\*', open(path, encoding='utf-8').read(), re.M)
    return m.group(1) if m else os.path.basename(path)[:-3].upper()


def tally():
    known = keywords()
    umb = umbrellas(known)
    # cards/README.md sits in the same directory and is not a card. This is
    # verify.py's own NAME_RE, searched rather than matched, so this tool and
    # load_canon() always agree on what counts as a card — four Briarbundles
    # files still open with a stray "## Haywight" variant heading left over from
    # the split, and anchoring to the first character silently dropped them.
    cards = [p for p in sorted(glob.glob('cards/*.md'))
             if re.search(NAME_RE, open(p, encoding='utf-8').read(), re.M)]
    direct = {k: [] for k in known}
    reducers = []
    for path in cards:
        text = open(path, encoding='utf-8').read()
        for k in known:
            if uses(text, k):
                direct[k].append(name_of(path))
        if reduces_stat(text):
            reducers.append(name_of(path))

    final = {k: set(v) for k, v in direct.items()}
    for name, (members, includes_stat) in umb.items():
        for m in members:
            final[name] |= final[m]
        if includes_stat:
            final[name] |= set(reducers)
    return known, umb, {k: sorted(v) for k, v in final.items()}, len(cards)


def render():
    known, umb, final, total = tally()
    L = []
    L.append('# Keyword Usage')
    L.append('')
    L.append(f'**Generated — do not edit by hand.** `python3 agent-tools/keyword-usage.py` '
             f'rewrites this file; `verify.py` fails if it is stale.')
    L.append('')
    L.append(f'How many of the {total} cards in `cards/` apply each keyword defined in '
             f'`{KEYWORD_DIR}/`. Counting rule, settled by Drew 2026-08-18: **a conditional grant '
             f'counts, a presence test or negation does not; an umbrella counts its members; '
             f'once per card.** Full reasoning in the script.')
    L.append('')
    L.append('| Keyword | Cards | Share |')
    L.append('|---|---:|---:|')
    for k in sorted(known, key=lambda k: (-len(final[k]), k)):
        n = len(final[k])
        mark = ' *(umbrella)*' if k in umb else ''
        L.append(f'| {k}{mark} | {n} | {100*n/total:.0f}% |')
    L.append('')
    for name, (members, includes_stat) in umb.items():
        extra = ' + stat reduction' if includes_stat else ''
        L.append(f'**{name}** covers {", ".join(members)}{extra} — membership parsed from '
                 f'its own glossary definition, so the count moves when the definition does.')
    L.append('')
    L.append('## Rare keywords')
    L.append('')
    L.append('Eight cards or fewer — the thin parts of the design space, listed by name '
             'because that is the number worth knowing when placing a new card.')
    L.append('')
    for k in sorted(known, key=lambda k: (len(final[k]), k)):
        if len(final[k]) <= 8:
            names = ', '.join(final[k]) if final[k] else '*no cards*'
            L.append(f'- **{k}** ({len(final[k])}) — {names}')
    L.append('')
    return '\n'.join(L)


def main():
    text = render()
    if '--check' in sys.argv:
        current = open(OUTPUT, encoding='utf-8').read() if os.path.exists(OUTPUT) else ''
        if current != text:
            print(f'STALE  {OUTPUT} — run `python3 agent-tools/keyword-usage.py`')
            return 1
        print(f'current  {OUTPUT}')
        return 0
    open(OUTPUT, 'w', encoding='utf-8').write(text)
    print(f'wrote {OUTPUT}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
