# Initiative — Slots, Not Seats (working draft)

**Status: NOT CANON.** Drew: "we still aren't quite there yet." This is a live design thread, not a ruling — `rules/card-glossary.md`'s Initiative Shift X entry and `rules/combat.md`'s fence/marker text are unchanged and still govern actual play until this resolves.

---

## The problem this is solving

Initiative Shift X's old wraparound math — "For shifts of X ≥ N (N = combatants), resolve one bonus turn (positive) or one full-lap pass-over (negative) per revolution" — was flagged earlier this session as unresolved: *"the freaking math for cyclic ordered list permutations is insane. let's leave it for now. I'm praying to the muse."*

Drew came back to it starting from a full rebuild, then found a much smaller fix. Both are recorded here — the rejected direction, because the reasoning that ruled it out is worth keeping, and the current direction, because it isn't finished yet.

---

## Rejected direction: a linear track (Patchwork-inspired)

First pass: replace the wheel entirely with a bounded linear track. Length = number of combatants. Whoever holds the lowest occupied slot acts, then moves to the back. Multiple combatants could stack on the same slot, resolved **last in, first out**. Floor/ceiling clamps: a shift can't push anyone past the track's current trailing or leading edge.

This would have worked, and it directly named where the old wheel's complexity actually lived: **the fence** (`rules/combat.md`) — the "marker sits on a position, not a person" rule — only had to exist because a wheel has no edges. A fixed reference point was needed to keep "right now" meaningful on a structure that loops forever. Remove the loop, and the fence has nothing left to do.

**Why it was set aside**, not because it was wrong: once the actual diagnosis landed (see below), it turned out the wheel didn't need to be replaced to get the same benefit — it just needed one boundary condition. Rebuilding the whole turn-order structure to fix one clause would have been solving it twice.

---

## Current direction: keep the wheel, clamp the shift

**The actual fix: a shift can never move a target's count past the marker.**

Worked example (4 combatants, marker at slot 1): someone at count 2 gets shifted −2 (later by 2). Naively their new count is 4 — in a 4-slot wheel, count 4 means "a full lap, back to acting immediately," which is exactly the case the old rule needed special wraparound handling for. Under the clamp, this shift simply caps at count 3 (the slot right before the marker comes back around) instead of wrapping. No revolutions, no modular arithmetic, no bonus-turn-per-lap bookkeeping.

**This eliminates:** the entire "shifts of X ≥ N... one bonus turn or full-lap pass-over per revolution" clause. That was the actual cyclic-permutation math causing the trouble — it's gone, not simplified.

**This does NOT eliminate** (confirmed still needed, not yet re-verified against every edge case):
- **Sliding** — no piece-stacking in this version (explicitly rejected: "we don't need piece stacking"). Shifting into an occupied slot still displaces everyone between by one slot, same as before.
- **Ordinary same-lap pass-overs** — the existing example ("someone who has just acted is shifted backward into a coming slot: the marker's first visit waves past them") isn't a wraparound case. It's a normal seat/count disagreement within a single lap, and the clamp doesn't touch it.

## Terminology, confirmed

- **Seat → Slot.** "Position" was already claimed by Frontline/Backline (`rules/combat.md`); "seat" is being retired in favor of **slot** for a wheel position, to keep the wheel's own vocabulary from colliding with anything else while we're in here anyway.
- **Sliding** stays the term for displacing neighbors when a shift lands on an occupied slot. Distinct from **shifting**.
- **Initiative Shift X** keeps "Shift" in its name — the keyword itself doesn't change.

## Not yet resolved

- Full re-verification of ordinary (non-wraparound) pass-overs under the new clamp — worked through once in chat reasoning, not yet pressure-tested against a full multi-shift combat sequence.
- Whether "count" and "slot" terminology both need adjustment now that "seat" → "slot," or whether "count" stays as-is.
- The actual rewritten `rules/card-glossary.md` Initiative Shift X entry and `rules/combat.md` fence text — not drafted yet, waiting on the above.

## Related Documents

- `rules/card-glossary.md` — Initiative Shift X, current (unchanged) canonical text
- `rules/combat.md` — the turn marker / fence, current (unchanged) canonical text
