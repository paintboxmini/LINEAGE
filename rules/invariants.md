# Combat Invariants

An **invariant** is a resolution rule the engine holds true unless a card explicitly says otherwise. This file is the canonical list of them.

It has two uses:

- **Reviewing content** — `agent-tools/red-team.md`'s Invariant Violations pass checks a new mechanic against this list. Bending one of these must be intentional and named.
- **Building rule-benders** — a card that changes how resolution works is a *rule modifier*: it declares which invariant it swaps and reverts on expiry, rather than adding a scattered one-off exception. (See the rule-modifier direction in `memory.md`: cards temporarily patch the engine; they are not permanent special cases.)

The simulator (`combatsimulations/`) is the executable model of everything here. If this doc and the sim disagree, one of them is a bug.

---

## The exchange — the resolution loop

One attack resolves in a fixed order. Each step is an invariant; the cards that bend it are named beneath it.

1. **Declare.** The attacker plays exactly one card at one target. Its color becomes public history the instant it is played.
   - Range gates legality: melee needs both combatants frontline; ranged needs not-both-frontline; "both" is always legal.

2. **Blind, simultaneous selection.** The defender chooses at most one card to reveal *without seeing the attacker's card*. Reveals are simultaneous — the defender decides from public information only (revealed-color history, position), never the played card.
   - *Modifier — Predictable (Study):* for one marked reveal, the holder sees the attacker's card before choosing. Expires on use.
   - *Constraint — Axiom:* a named color cannot be revealed — attack or block — on the next reveal.
   - A staggered, cannot-defend, or collapsed defender skips selection (attacker wins uncontested).

3. **RPS resolution.** Blue beats Red beats Green beats Blue. Same color is a tie. No defense revealed means the attacker wins uncontested.
   - *Modifier — Paradox:* inverts win/loss for an exchange it is part of (ties unaffected).

4. **Apply the outcome.**
   - **Attacker wins:** deal damage (stat + die + any pending bonus), then the attacker's Effect triggers.
   - **Defender wins:** only the Defensive Bonus triggers; no damage.
   - **Tie:** no damage. The attacker's Effect triggers first, then the Defensive Bonus — unless the Effect cancels it. An effect that only *amplifies damage* (exploding dice, "+X damage") does nothing on a tie; there is no damage to add to (`rules/core-rules.md`).

5. **Damage pipeline — fixed order.** When damage is dealt it is reduced in this order, and each step is itself an invariant:

   redirect (Shared Burden) → volunteer shield (Fortress / Intercept, team play) → **Armour** (flat reduction) → **Resist** (halve, one stack spent per hit) → damage floor (Equal Footing) → apply to HP.

   - A single attack cannot push a *standing* combatant below 0 HP (clamped to 0 = Collapse).
   - `Unpreventable` damage skips Armour and Resist.
   - Thorns retaliates against a melee attacker after the hit lands.

---

## Standing invariants

Not tied to a single exchange, but always in force.

- **Initiative is a continuous wheel with a fixed turn marker.** There are no rounds. A combatant's position changes only via Initiative Shift; crossing the marker changes how many turns they get (see `rules/combat.md`, The turn marker, and `Initiative Shift X` in `rules/card-glossary.md`).
- **Blocking costs a card.** Every defense spends a card from hand. Hand size *is* blocking capacity between your turns — nobody blocks for free, and nobody is ever completely undefended (the hand-size floor guarantees it).
- **Derived stats.** Body → max HP (`2 × Body + 9`; only Body changes HP). Mind → hand size. Soul → initiative. Changes apply live, in both directions.
- **The deck cycles.** Decks are small and reshuffle constantly, so deck-state manipulation (scry, surveil, tracking) is near-neutral *in combat* — the deck recycles what you bury or bin. Read, tempo, and timing effects move outcomes; deck-order effects mostly do not (see `memory.md`).
- **A reveal is private until it happens, public after.** Your pending choice is hidden; your played colors are known history. Predictable is the only thing that breaks the "until it happens" half.

---

## Current rule modifiers — the registry

Every card that bends an invariant, the invariant it bends, and its lifetime. This is the seed of the future rule-modifier system (`memory.md`, architecture north star).

| Modifier | Invariant bent | Lifetime |
|---|---|---|
| Predictable (Study) | blind simultaneous selection | next reveal |
| Axiom | selection legality (color ban) | next reveal |
| Paradox | RPS resolution (inverts) | the exchange |
| Interrupt | defender may act (cannot-defend) | until your next turn |
| Stagger | defender may act (skips block) | next attack |
| Initiative Shift | wheel position | immediate |
| Armour / Resist | damage pipeline | per hit / next hit |
| Fortress / Intercept / Shared Burden | damage pipeline (redirect) | next hit (team) |
| Evade | whether an attack connects | next attack (chance) |

---

## Adding a rule-bender

Today each modifier is a per-combatant flag read inline at the one pipeline step it affects — the seam already exists. The agreed path (`memory.md`): flags → typed modifiers-with-lifetimes → policy stack. Promote a level only when adding the next bender as a flag has become painful.

Until then, a new bender should: (1) name the invariant above that it changes, (2) set a flag with a clear expiry, (3) read that flag at exactly one pipeline step, (4) revert on expiry. If a mechanic can't be expressed that way — if it needs the engine to special-case resolution in more than one place — that is the signal it wants the policy-stack architecture, and a red flag worth raising before it ships.
