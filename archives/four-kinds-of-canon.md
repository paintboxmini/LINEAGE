## Four Kinds of Canonical Content

Before asking *who may change this* (the Canon Gate, below), know *what kind of thing it is*:

1. **Rule Definitions** — vocabulary. What something *is*, mechanically and precisely. Keyword texts (`rules/card-glossary.md`), formulas (`rules/core-rules.md`), procedures (`rules/combat.md`).
2. **Invariants** (`rules/invariants.md`) — narrow, and specific to the combat simulator: a mathematical or computational fact that must hold inside the engine regardless of how a human visualizes the same thing at the table (e.g., total card count is conserved across a combatant's deck, hand, discard, and exile no matter how a human pictures the shuffle). Not a design standard — a computational one.
3. **Design Principles** and **Exemplars** — living doctrine. Design Principles live in `agent-tools/design-principles.md`; concrete exemplars are identified in the content itself or in relevant archives. What something *is* mechanically stays in Rule Definitions; what makes it *well-made* lives in Design Principles.

They blur because a real piece of content usually touches more than one at once — that's expected. The bug is a *file* absorbing another layer's job rather than staying narrow and pointing outward. Rule-definition bookkeeping belongs in Rule Definitions; computational invariants belong in `rules/invariants.md`; design-craft principles belong in `agent-tools/design-principles.md`.