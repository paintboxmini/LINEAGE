# Combat Invariants

An invariant is a mathematical or computational truth inside the combat simulator's engine — something that must hold regardless of how a human visualizes or tracks the same thing at the table. The visualization can vary, or be discarded entirely; the invariant is whatever survives underneath it.

This file is scoped to the simulator only. It is not a design standard for what makes a mechanic feel right (that's `agent-tools/design-philosophy.md`) and not a keyword's rules text (that's `rules/card-glossary.md`).

---

## Confirmed

**The engine tracks a turn-count per combatant, not a position on a wheel.** A human at the table pictures a wheel — a marker moving around a loop of seats — because it's an easy way to see whose turn is coming. The engine doesn't need seats at all. What has to be correct is: for every combatant, how many turns away is their next turn. The wheel is one way to make that count legible to a human; it is not what gets computed. Initiative Shift ±X means: recompute that count by exactly X for the target. Any implementation is correct exactly when it preserves that number — wheel, list, or nothing visual at all. (Table-facing bookkeeping — seats, passes, bonus turns: `rules/card-glossary.md`, Initiative Shift X.)

## Candidates — proposed, not yet confirmed

Only the entry above has actually been confirmed against this definition. These two are offered in the same style, not asserted as settled:

- **Derived stats are computed live, never cached.** Max HP, hand size, and initiative bonus are functions of current Body/Mind/Soul, evaluated fresh whenever needed — not stored values patched on a stat change. An implementation that caches one of these and forgets to invalidate it on a stat change has this bug specifically.
- **Card count is conserved per combatant across deck, hand, discard, and exile.** Nothing is created or destroyed by ordinary play — a card moves between piles, and the total across all of them changes only at two nameable events: a Wound/Exhaust insertion, or a permanent removal (short rest, or Exile returning to deck at combat's end). Any other change in the total is a bug.

---

## Mechanic-override reference

Not itself a list of invariants — a practical index for `combatsimulations/`: every card that overrides a specific mechanic, which one, and for how long. Useful for keeping the simulator's flag-based override system correct; check new content against it when a new card looks like it needs the same kind of override.

| Card/Effect | Mechanic overridden | Lifetime |
|---|---|---|
| Axiom | selection legality (color ban) | next reveal |
| Paradox | RPS resolution (inverts) | the exchange |
| Interrupt | defender may act (cannot-defend) | until your next turn |
| Stagger | attacker/defender may act | until recovered (self or ally action) |
| Intercept | who defends (ally substitutes) | next attack (team) |
| Initiative Shift | turn order | immediate |
| Armour / Resist | damage pipeline (reduction) | per hit / next hit |
| Fortress / Shared Burden | damage pipeline (reassignment) | next hit (team) |
| Evade | whether an attack connects | next attack (chance) |

Adding a new override: name the mechanic it changes, set a flag with a clear expiry, read that flag at exactly one point in the relevant procedure, revert on expiry. Escalating the override system itself beyond flags (to typed modifiers, to a policy stack) is engineering judgment, not an invariant — see `memory.md`'s architecture north star for that path.

---

The simulator is the executable model of the Confirmed section above. If its code and this document disagree on those, one of them is a bug.
