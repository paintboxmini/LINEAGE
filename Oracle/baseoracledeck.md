# Oracle Deck

Cards available in the Oracle pool for this campaign. At end of session, GM draws 3 — active player picks 1.

---

## Current Pool

**Empty — intentionally, as of 2026-08-04.** Drew is building the actual pool by hand from the core sets, right before Session 1. This is not a gap to fill; do not repopulate it without being asked.

The AI-selected 63-card composition that stood here through 2026-08-03 — every pass, cut, and swap that built it — is preserved verbatim at `archives/oracle-pool-2026-08-03.md`, in case any of it is worth cribbing from.

**`combatsimulations/content.py`'s `ORACLE_DECK` and `printing/generate-cards.py`'s oracle card set still hold that same 63-card list** — they were never derived from this file, just kept in sync with it by hand, so nothing broke when this file emptied. They'll need to be rebuilt to match whatever Drew actually picks, once he picks it.

---

## Eligibility Criteria (the mechanic — this part stays)

Starter tier — simplest, lowest power/impact cards from the three core sets. Each card touches one of the three core pillars (RPS, Initiative, Position) or a standard keyword; none force the opponent to discard, inject a status (Wound/Exhaust), force a hand reveal, or presuppose a system (Anchored, an RPS auto-win/reversal, a precondition set by another card, an open-ended amount choice) the pool doesn't otherwise introduce. All core cards — `cards/red-body.md`, `cards/blue-mind.md`, `cards/green-soul.md`.

**Fixed composition target (2026-08-03, Drew): 21 per colour, split 12 / 6 / 3 along that colour's range identity.**

| | 12 | 6 | 3 |
|---|---|---|---|
| **Red** | Melee | Both | Ranged |
| **Blue** | Ranged | Melee | Both |
| **Green** | Both | Ranged | Melee |

These are exact counts, not a lean — whenever the pool is rebuilt, all nine cells should hold true.

---

## Related Documents

- `archives/oracle-pool-2026-08-03.md` — the full prior build, verbatim, with its entire reasoning trail
- `memory.md` — the 2026-08-04 threshold-log entry recording this clearing
