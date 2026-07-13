# Combat Invariants

## Four layers, kept apart on purpose

This repo holds four different kinds of canonical content, and they get confused easily because a real piece of content usually touches all four at once. Keeping them in separate files is what stops the confusion from becoming drift.

1. **Rule Definitions** — vocabulary. What something *is*. Canonical, precise, mechanical: keyword texts (`rules/card-glossary.md`), the HP/hand-size/initiative formulas (`rules/core-rules.md`), the attack-resolution procedure (`rules/combat.md`). A rule definition answers "what does this do," full stop. **Keyword definitions are not invariants** — Staggered's exact text lives in the glossary; this file never restates it.
2. **Invariants** *(this file)* — constitutional. What must stay true across *every* implementation of a mechanic, not how any one implementation works. An invariant doesn't tell you the bookkeeping; it tells you the sentence the bookkeeping has to keep true. If you can point to a specific procedure and ask "why does it work this way," the invariant is the answer one level up from the procedure — the fantasy the procedure exists to protect.
3. **Exemplars** (`agent-tools/exemplars.md`) — concrete implementations chosen *because* they demonstrate an invariant well. The Fencerow Shrike is an exemplar, not an invariant: its specific stats, cards, and terrain rules are Rule Definitions; what makes it worth reading is that its design demonstrates several invariants at once (deck expresses behavior, ecology drives mechanics, encounters teach through play). You don't copy an exemplar. You extract the principle and let the next creature be a completely different organism.
4. **Heuristics** (`agent-tools/heuristics.md`) — operational. Not a truth about the world, a habit about the work: when to promote a pattern, when to escalate an architecture, when to flag instead of quietly resolve. Process, not canon.

Why they blur: an exemplar is *assembled from* rule definitions and *chosen to illustrate* invariants — genuinely two layers braided into one file, by design, because that's what a full concrete example has to be. The layering only breaks down when a file that's supposed to hold ONE layer accidentally absorbs another's job — which is exactly what happened to this file before this section existed: it had quietly become a place to re-derive rule-definition bookkeeping (Initiative Shift's seat/count mechanics, restated almost verbatim from the glossary) and to resolve ambiguity inline, instead of only stating what must stay true. Fixed below; if this file starts doing that again, that's the bug to name.

---

**The prime invariant — mechanics exist to enforce the fantasy, not to break or subvert it.** When a bookkeeping rule and the fantasy it's supposed to protect disagree, the bookkeeping is wrong. This is the first test every new resolution rule must pass.

Two worked examples of the *same* prime invariant, from two different subsystems — read them as illustrations of the pattern, not as what the prime invariant is *about*:

- *Initiative Shift:* the fantasy is "+2 means I act two turns sooner." Seats, the marker, pass-overs, and bonus turns are bookkeeping that exists only to keep that sentence true — none of it is the invariant itself. See Standing Invariants below.
- *Staggered:* the fantasy is being knocked off balance — caught mid-stumble, unable to set your feet in time to block. The mechanic (no defensive card on the next attack against you) exists to serve that fantasy, and it's *why* a rule-bender that lets an ally "catch" a staggered combatant, or that clears Staggered outright, has to reproduce the fantasy of someone steadying you — not just flip a flag back to false. (Full current mechanics: `rules/card-glossary.md`, Staggered.)

The hierarchy beneath every subsystem: **fantasy** (what should the player feel happened?) → **invariant** (what must stay true for that fantasy to cohere?) → **mechanic** (the rule definition that enforces it) → **implementation** (lists, engines, visualizations). Document the canonical layer; teach from the invariant, not from the picture.

It has two uses:

- **Reviewing content** — `agent-tools/red-team.md`'s Invariant Violations pass checks a new mechanic against this list. Bending one of these must be intentional and named.
- **Building rule-benders** — a card that changes how resolution works is a *rule modifier*: it declares which invariant it swaps and reverts on expiry, rather than adding a scattered one-off exception. Escalation path for the modifier system itself is a heuristic, not an invariant — see `agent-tools/heuristics.md`.

The simulator (`combatsimulations/`) is the executable model of everything here. If this doc and the sim disagree, one of them is a bug.

---

## Invariants of the resolution loop

Each of these is a *what must stay true*, not a *how it's implemented*. The step-by-step procedure — Declare, blind reveal, RPS, apply outcome, the damage pipeline's exact order — is a Rule Definition and lives in `rules/combat.md` (Attack Resolution, Range, Positioning, Damage Pipeline). This file states only the invariant each step protects.

- **A reveal is private until it happens, public after.** Your pending choice is hidden from the attacker; your played colors are known history the instant they're played. Nothing breaks the blind — the defender chooses from public information only, never from the card actually in play. Reveal simultaneity is absolute.
- **An effect that only amplifies damage needs damage to amplify.** Exploding dice, "+X damage," and similar have nothing to act on when an attack deals none — so they do nothing on a tie or a miss. Effects independent of damage (status, stat shifts, repositioning) trigger normally regardless of outcome. (Full outcome table: `rules/combat.md`, Attack Resolution.)
- **Attack-damage defenses only defend against attacks.** Armour, Resist, damage floors, and redirects all exist to answer *an attack* — so none of them touch Thorns, status damage, or HP costs, which aren't attacks. Unpreventable damage isn't a special case bypassing the pipeline; it was never in the pipeline's jurisdiction to begin with. (Pipeline order: `rules/combat.md`, Damage Pipeline.)
- **A single attack cannot end a standing combatant.** It clamps at 0 HP (Collapse); only damage taken *after* Collapse can push further. (Full Collapse/Death rules: `rules/combat.md`.)

---

## Standing invariants

Not tied to a single exchange, but always in force.

- **Initiative Shift ±X means exactly: the target's next turn arrives X turns sooner or later, and nothing else may vary.** The full seat/count/pass-over bookkeeping that keeps this sentence true under every edge case lives in `rules/card-glossary.md`, Initiative Shift X — that bookkeeping is a rule definition, not restated here. What's invariant is narrower and stricter than the bookkeeping: whatever the implementation, the target's count changes by exactly X and nothing about anyone else's relative order does.
- **The linear turn order is the canonical state; the wheel is its visualization.** Turns-until-action is *derived* from a position in a list (position − 1, current actor normalized to position 1); the wheel is circular only because turns repeat forever, and exists to make one awkward list property (after the last actor, play continues with the first) easy to read at the table. A shift is a list operation — remove, reinsert X positions away, slide the gap closed. One state, three altitudes: the rules are linear, the wheel is circular, the count is arithmetic. This is the invariant a reimplementation has to preserve even if it throws out every other visualization.
- **Blocking costs a card, and hand size at rest is exactly your blocking capacity between turns.** Nobody blocks for free; a stat floor exists so no one is ever reduced below act-plus-one-block, and beyond that floor there is no cushion — a low-Mind combatant must compensate through the rest of the system (Resist, draw, ally support, equipment), and that pressure is intended. (The actual hand-size formula: `rules/core-rules.md`, Stats.)
- **Stat changes apply live, in both directions, the instant the stat changes.** Nothing about a combatant is fixed at creation — a drain or a boost immediately cascades to whatever it governs. (The formulas themselves — Body→HP, Mind→hand size, Soul→initiative, total stats→deck size and Strength: `rules/core-rules.md` and `rules/card-glossary.md`, Stat Change.)
- **The deck reshuffles from discard; cards don't leave the game by default.** Because decks are small and recycle constantly, deck-state manipulation (scry, surveil) is near-neutral in combat, while read/tempo/timing effects are what actually move outcomes. This is a consequence of the invariant, not a separate rule.

---

## Current rule modifiers — the registry

Every card that bends an invariant, the invariant it bends, and its lifetime. This is the seed of the future rule-modifier system (`memory.md`, architecture north star; escalation heuristic in `agent-tools/heuristics.md`).

| Modifier | Invariant bent | Lifetime |
|---|---|---|
| Axiom | selection legality (color ban) | next reveal |
| Paradox | RPS resolution (inverts) | the exchange |
| Interrupt | defender may act (cannot-defend) | until your next turn |
| Stagger | defender may act (skips block) | next attack |
| Intercept | who defends (ally substitutes) | next attack (team) |
| Initiative Shift | wheel position | immediate |
| Armour / Resist | damage pipeline (reduction) | per hit / next hit |
| Fortress / Shared Burden | damage pipeline (reassignment) | next hit (team) |
| Evade | whether an attack connects | next attack (chance) |

---

## Adding a rule-bender

Name the invariant above that the new mechanic changes, set a flag with a clear expiry, read that flag at exactly one pipeline step, revert on expiry. If a mechanic can't be expressed that way, that's a signal worth raising before it ships — see `agent-tools/heuristics.md` for the escalation path.
