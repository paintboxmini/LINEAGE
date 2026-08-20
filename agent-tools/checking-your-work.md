# Checking Your Work

**The tedium of hand-reading every change is the problem this file exists to replace.** Drew, 2026-08-18: *"before I tried to double check my work by always going in and hand reading every change, but my god, it's tedious... I'm taking that lesson now and trying to formalize it into agent tooling, comprehensive checks whenever we make changes."*

Hand-reading does not scale and does not repeat. A check does both. But a check is only worth having if it can fail, and most of the failures below are checks that could not.

Everything here is a mistake actually made, with the instance attached. None of it is hypothetical, and the instances are the point — a rule with no scar behind it gets rationalised away at 2am.

---

## The eight ways it goes wrong

### 1. A check reports identical whether or not it exercised anything

**Five instances in one session.** A bucket negative test removed BRACE, which was indexed elsewhere, so the invariant never broke. A `max_hp` test guarded on `hasattr(c, 'adjust_stat')` — the real method is `adjust`, so it applied no stat changes at all and reported clean. A card-conservation leak was gated on `len(self.discard) > 6`, a condition the duels never reached. A `conserve.py` fault injection raised `IndexError` before writing anything, and the check that followed passed *accurately*, because nothing had changed. And `generate-glossary.py --check` reported **current** while the generator silently dropped a keyword, because the output faithfully matched what that generator emitted.

> **A negative test must confirm the fault actually fired.** Assert the injected state exists before running the check. "I wrote a fault" and "a fault occurred" are different claims.

### 2. Coverage that counts itself

`check_decks` compared the deck lines it parsed against the deck lines *matching its own pattern* on disk. A deck written any other way was invisible to both halves: nought found, nought expected, green. Narrowing a glob to `bestiary/*/mechanics.md` dropped 6 of 37 decks from validation while every check still said PASS.

> **Count from outside the thing being checked.** If the tally and the check share a pattern, the tally cannot see the pattern's blind spot. `check_stat_block_scope` exists solely because of this.

### 3. A stated invariant that nothing enforces

`agent-tools/invariants.md` listed *"deck size equals total stats"* against `check_decks` — the flagship invariant of the deck system — and `check_decks` never checked it. Proven by moving Briarbound to Body 5, where a 9-stat creature with a 7-card deck passed clean. The same file's Confirmed section sat empty for weeks while prose candidates accumulated above it.

> **Test the claim, do not read it.** Break the thing on purpose and watch. An unenforced invariant reads exactly like an enforced one, which is worse than having neither.

### 4. Clean results are the dangerous ones

A single deck sample put a Mind-heavy build at **60.8%**, and a rule was recommended on it. Across seeds the real figure is 3–4 points and flat, with deck-draw variance comparable to the whole effect. Separately, a first simulation run produced a tidy *"no specialist configuration ever wins"* — wrong, because it ran only one ordering.

> **A result that is clean, large and actionable deserves a second sample before it becomes a rule.** Messy results get questioned. Tidy ones get published.

### 5. A sweep that reports its own tally

An equipment rewrite reported fourteen statements changed. One survived, buried in a parenthetical inside a pricing paragraph, because the sweep matched tier-example lines and that one was prose.

> **Finish a sweep by searching for what it was supposed to eliminate**, not by trusting the count it reported. `grep` for the old phrasing after you believe it is gone.

### 6. Edits that delete more than they were aimed at

A section rewrite computed its end boundary with a forward index search, matched a heading far below, and silently deleted `## Chase`, `## Fleeing Combat` and `## Initiative` — 40 content lines — while `verify.py` still reported 17 of 18 passing. A malformed reference-rewrite regex duplicated card lists across 44 files, and the same bug class recurred twice more.

> **Anchor edits on strings unique in the file, and assert the anchor count is 1 before replacing.** For anything structural, run `conserve.py snapshot` before and `check` after: it compares the multiset of content lines, so two errors that cancel in a total still show up.

### 7. Exemption lists

A first draft of `check_action_tables` matched table rows anywhere in the file, swept in the Range Matrix, and would have gone green only by naming Frontline, Melee, Ranged and the rest as exceptions. A first draft of `check_stat_block_scope` exempted `playtesting/` wholesale — which would have hidden the exact hazard it was built for.

> **Fix the discriminator, not the symptom.** An exemption list silences what it names and hides what it does not. If you are reaching for one, the rule is aimed at the wrong feature.

### 8. Absence read as evidence

Three cards were reported as unable to remove a held status because none of them said *"of your choice"*. The phrase is implied when unwritten, so they always could. A missing phrase was read as a missing capability.

> **Know the defaults before reading an absence.** Before reporting that content cannot do something, check whether the words you are missing were ever required.

---

## What to actually run

| When | Run |
|---|---|
| Before any commit | `python3 agent-tools/verify.py` — expect every check green |
| Either side of a move, rename, split or merge | `agent-tools/conserve.py snapshot` then `check` |
| After a find-and-replace sweep | `grep` for the phrasing you believe you eliminated |
| After adding a check | Break the thing it guards; confirm it fails **and** names the offender |
| After a measurement | Re-run with different seeds before quoting a number |
| Before deleting anything as unused | Search the whole repo, not the directory you are in |

## The one-line version

**Every claim you make about the repository is a hypothesis until something fails when it is false.** Not "did I check?" but **"what would have failed if I were wrong?"** If the answer is nothing, you have not checked.

## Related

- `agent-tools/verify.py` — the acceptance suite, run before every commit
- `agent-tools/conserve.py` — content conservation across a restructure
- `agent-tools/invariants.md` — what is enforced, by which check, and what is stated but unchecked
- `agent-tools/red-team.md` — reviewing *content*; this file is about reviewing *your own work on it*
