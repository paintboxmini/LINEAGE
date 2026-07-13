# Combat Invariants

An invariant is not a rule and not an example — it's the standard a mechanic is checked against. The prime invariant states that standard once, in the abstract. It needs no worked example to be understood; if you find yourself reaching for a specific keyword to explain it, that keyword's mechanics belong in `rules/card-glossary.md`, not here. See `CLAUDE.md`, Four Kinds of Canonical Content, for how this file relates to Rule Definitions, Exemplars, and Heuristics.

---

**The prime invariant — mechanics exist to ensure that they reflect the fantasy of the TTRPG, not to break or subvert it.** When a mechanic and the fantasy it's supposed to produce disagree, the mechanic is wrong. This is the test every resolution rule has to pass.

It has two uses:

- **Reviewing content** — `agent-tools/red-team.md`'s Invariant Violations pass checks a new mechanic against this test.
- **Judging a mechanic override** — see below.

---

## What a mechanic-overriding card actually does

A card that changes how resolution works does not bend an invariant — invariants don't bend; that's what makes them invariant. It overrides a specific **mechanic**, for a scoped duration, and the prime invariant is the standard that override gets checked against: does the fantasy still hold while it's active? Paradox inverting RPS win/loss doesn't touch the prime invariant. It changes a mechanic. The prime invariant is what you hold that new mechanic up to.

## Current mechanic overrides — the registry

Every card that overrides a mechanic, which one, and for how long.

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

## Adding a mechanic override

Name the mechanic the new card overrides, set a flag with a clear expiry, read that flag at exactly one point in the relevant procedure, revert on expiry — then check the result against the prime invariant. If a mechanic can't be expressed that way, that's a signal worth raising before it ships. Escalation path: `agent-tools/heuristics.md`.

---

## Standing invariants

Fantasy-level truths that must survive any implementation. Not a specific mechanic's bookkeeping — that's `rules/card-glossary.md`, `rules/combat.md`, `rules/core-rules.md`.

- **Your hand is your stamina to react.** Every defense spends a card; when your hand is thin, you are exposed, and nothing restores that but time, support, or the rest of your kit. This is what makes a low-Mind combatant feel fragile between turns, not just on paper.
- **A stat change lands the instant it happens.** Nothing about a combatant is fixed for the fight — a drain or a boost is felt immediately, in whatever it governs, not on some later beat.
- **Nothing you own leaves a fight for good.** A deck empties and reshuffles from its own discard; what you drew is not gone, only spent for now.

---

The simulator (`combatsimulations/`) is the executable model of this document's mechanics. Keeping its code faithful to canon is a maintenance concern, not an evaluative one — the simulator is a separate instrument for surfacing findings when asked, not a step in judging whether a ruling is sound. See `agent-tools/heuristics.md`.
