# HP and Stat-Derived Values — Design Trail

This is a historical design trail explaining the evolution of HP and stat-derived values. It is not a current rules reference; current mechanics live in the canonical rules files.

## The problem

Early Tales Untold balance tied survivability heavily to Body. Body already governed Red-card damage, so increasing Body improved both offense and durability. That created a double-dip: a high-Body build hit harder while also taking more punishment.

Balance work therefore treated the HP formula as a possible lever for separating those roles without abandoning the three-stat structure.

## What the balance work established

Simulation showed that flattening or decoupling HP from Body could reduce the damage-plus-survivability coupling, but it was only a **secondary balance lever**. The larger balance behavior came from game length, damage variance, defensive economy, and the relationship between raw stat bonuses and card dice.

This mattered because it prevented a tempting but misleading conclusion: if a high-stat build was winning too often, changing HP alone was not necessarily addressing the real cause.

The broader combat simulations eventually showed that longer games gave RPS reads, card advantage, and defensive decisions more room to matter. That made game length a more consequential balance variable than small individual HP adjustments.

## Stat-derived values

A second thread concerned what happens when a stat itself changes during combat.

The durable rule is that a stat is not an isolated number. Its derived functions move with it. A temporary change to a stat therefore affects the things that stat governs for the duration of the change, then those values return when the change ends.

The system subsequently generalized this relationship beyond the original Body-only HP interpretation. Body, Mind, and Soul each participate in the current derived-value model alongside their primary combat functions.

The important design lesson is therefore:

> **When a stat changes, reason from the stat's current derived functions rather than inventing a separate ad hoc modifier for each card.**

This keeps stat-changing effects coherent across current and future mechanics.

## What this history prevents

The old archive contains several obsolete snapshots, including a Body-only HP model and earlier formulas. Those are historical evidence, not alternatives to the current rules.

Future design work should not resurrect an earlier HP formula merely because it appears in an old decision record. The useful historical information is **why HP was changed and what the experiments demonstrated about its leverage**, not the obsolete numbers themselves.

## Provenance

The historical record includes balance simulations comparing HP changes, card-dice changes, game length, stat effects, and defensive economy. The key-design archive preserves those findings in their original historical context. Current derived-value rules are authoritative in `rules/card-glossary.md` and `rules/combat.md`.
