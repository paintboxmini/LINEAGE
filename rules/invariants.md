# Combat Invariants

An invariant is a mathematical or computational truth inside the combat simulator's engine — something that must hold regardless of how a human visualizes or tracks the same thing at the table. The visualization can vary, or be discarded entirely; the invariant is whatever survives underneath it.

This file is scoped to the simulator only. It is not a design standard for what makes a mechanic feel right, and not a keyword's rules text (that's `rules/card-glossary.md`).

**The simulator exists.** `combat-simulations/` was rebuilt from the ground up on 2026-09-06; this file was written as its specification beforehand and is now a description of what that code is checked against. Where the two disagree, one of them is a bug — see Standing gaps below for the one currently known.

---

## Confirmed

- **Derived stats are computed live, never cached.** Max HP, hand size, and initiative bonus are functions of current Body/Mind/Soul, evaluated fresh whenever needed — not stored values patched on a stat change. An implementation that caches one of these and forgets to invalidate it on a stat change has this bug specifically.
- **Card count is conserved per combatant across deck, hand, discard, and exile.** Nothing is created or destroyed by ordinary play — a card moves between piles, and the total across all of them changes only at two nameable events: a Wound/Exhaust insertion, or a permanent removal (short rest, or Exile returning to deck at combat's end). Any other change in the total is a bug.

---

## Mechanic-override reference

Not itself a list of invariants — a practical index for `combat-simulations/`: every card that overrides a specific mechanic, which one, and for how long. Useful for keeping the simulator's flag-based override system correct; check new content against it when a new card looks like it needs the same kind of override.

| Card/Effect | Mechanic overridden | Lifetime |
|---|---|---|
| Axiom | selection legality (color ban) | next reveal |
| Paradox | RPS resolution (inverts) | the exchange |
| Interrupt | defender may act (cannot-defend) | until your next turn |
| Stagger | attacker/defender may act | until recovered (self or ally action) |
| Intercept | who defends (ally substitutes) | next attack (team) |
| Initiative Shift | turn order | immediate |
| Resist | damage pipeline (reduction) | next hit |
| Protect | damage pipeline (reassignment) | next hit (team) |
| Evade | whether an attack connects | next attack (chance) |
| Ledger Weight | card selection (post-reveal redo, attacker-on-defender only) | one reveal |

---

## Standing gaps

Where `combat-simulations/` and the Confirmed section above do not currently agree.

**None.** Both Confirmed invariants are asserted by `combat-simulations/test_invariants.py`, which is the executable form of this section — a gap recorded here should get a failing check there before it gets a fix.

---

The simulator is the executable model of the Confirmed section above. If its code and this document disagree, one of them is a bug: fix the one that is wrong rather than editing this file to match the code.
