# Oracle Eligibility — Scope

**Not built. This is a specification, not a tool.** Nothing here runs yet.

Split out from `agent-tools/card-corpus-analysis.md` on 2026-08-17 (Drew: *"Oracle eligibility is its own tool"*). The distinction is real: corpus analysis *describes a distribution* and has no correct answer to measure against. This one *measures against a stated target* and can say a card passes or fails.

---

## What It Is

A read-only pass that answers one question: **given `Oracle/baseoracledeck.md`'s stated criteria, which of the current cards are eligible for the Oracle pool, and how does the eligible set distribute against the composition target?**

This is the mechanical half of Drew's own stated approach (2026-08-16): *"the hand built Oracle deck angle — refine the card pool instead and see what falls out."* It narrows what he chooses from. It does not choose.

## The Criteria Already Exist

`Oracle/baseoracledeck.md` states them, and they are unusually checkable for a design rule:

- **Starter tier** — simplest, lowest power/impact cards from the three core sets (`cards/red-body.md`, `cards/blue-mind.md`, `cards/green-soul.md`). Core cards only.
- Each card touches one of the three core pillars (RPS, Initiative, Position) or a standard keyword.
- **None** force opponent discard, inject a status (Wound/Exhaust), force a hand reveal, or presuppose a system the pool doesn't otherwise introduce (Anchored, an RPS auto-win or reversal, a precondition set by another card, an open-ended amount choice).

**Composition target (2026-08-03, Drew): 21 per colour, split 12 / 6 / 3 along that colour's range identity.**

| | 12 | 6 | 3 |
|---|---|---|---|
| **Red** | Melee | Both | Ranged |
| **Blue** | Ranged | Melee | Both |
| **Green** | Both | Ranged | Melee |

Exact counts, not a lean. All nine cells hold or the pool is wrong.

## Output

1. **Eligible / ineligible**, per card, with the specific criterion that disqualified each rejection. A rejection without a named reason is useless — the point is to see whether the criteria are cutting what they should.
2. **The nine-cell fill.** How many eligible cards exist per colour × range cell, against the 12/6/3 target. Cells that can't be filled from the current corpus are the real finding: they say the core sets don't contain what the target asks for.
3. **Sync status.** `combatsimulations/content.py`'s `ORACLE_DECK` and `printing/generate-cards.py`'s oracle card set still hold the old 63-card list, kept in sync by hand and never derived from the pool file. Report whether they match whatever the pool currently is.

## What It Cannot Decide

**The pool itself.** `Oracle/baseoracledeck.md` says plainly: *"Drew is building the actual pool by hand from the core sets... This is not a gap to fill; do not repopulate it without being asked."* That instruction is unchanged by this tool existing. Producing an eligible list is not producing a pool, and the tool must not write to `Oracle/`.

Two judgment calls it can surface but not settle:

- **"Starter tier" and "simplest, lowest power/impact"** are not mechanically defined. A power proxy is available — `combatsimulations/` has a working engine — but a proxy ranking is evidence for the call, not the call.
- **"Presupposes a system the pool doesn't otherwise introduce"** is circular by construction: what the pool introduces depends on what's in the pool. Evaluate against the eligible set and report the cards whose status flips depending on that reading, rather than picking one silently.

## Shared Plumbing

**Same parser, same report format as `agent-tools/card-corpus-analysis.md`** (2026-08-17, Drew). Separate tool, separate criteria, identical machinery — both read the corpus through `verify.py`'s `load_canon()` and emit the same shape of report. One parser, not three; a reader who has seen one tool's output can read the other's without relearning it.

## Open Questions Before Building

1. Should the sync check against `content.py` / `generate-cards.py` live here, or become a real `verify.py` check? It's a pass/fail correctness condition, which is verify's job rather than this tool's.
