# Combat Invariants

An **invariant** is a resolution rule the engine holds true unless a card explicitly says otherwise. This file is the canonical list of them.

**The prime invariant — mechanics exist to enforce the fantasy, not to break or subvert it.** Every entry below formalizes a sentence a player believes ("+2 means I act two turns sooner"). When a bookkeeping rule and the believed sentence disagree, the bookkeeping is wrong. This is the first test every new resolution rule must pass.

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
   - *Modifier — Intercept (team):* a standing ally reveals in the target's place, taking over this defense before RPS.
   - A staggered, cannot-defend, or collapsed defender skips selection (attacker wins uncontested).

3. **RPS resolution.** Blue beats Red beats Green beats Blue. Same color is a tie. No defense revealed means the attacker wins uncontested.
   - *Modifier — Paradox:* inverts win/loss for an exchange it is part of (ties unaffected).

4. **Apply the outcome.**
   - **Attacker wins:** deal damage (stat + die + any pending bonus), then the attacker's Effect triggers.
   - **Defender wins:** only the Defensive Bonus triggers; no damage.
   - **Tie:** no damage. The attacker's Effect triggers first, then the Defensive Bonus — unless the Effect cancels it. An effect that only *amplifies damage* (exploding dice, "+X damage") does nothing on a tie; there is no damage to add to (`rules/core-rules.md`).

5. **Damage pipeline — fixed order.** When *attack* damage is dealt it passes through this pipeline, and each step is itself an invariant:

   redirect (Shared Burden) → volunteer shield (Fortress, team play) → **Armour** (flat reduction) → **Resist** (halve, one stack spent per hit) → damage floor (Equal Footing) → apply to HP.

   - A single attack cannot push a *standing* combatant below 0 HP (clamped to 0 = Collapse).
   - **Unpreventable damage bypasses the whole pipeline.** Every step above is an *attack-damage* defense; bleed, thorns, status damage, and HP costs are not attacks, so they cannot be reduced (Armour/Resist), reassigned (Shared Burden/Fortress), or capped (Equal Footing). They land on the original target, in full.
   - Thorns retaliates against a melee attacker after the hit lands (and is itself unpreventable).

---

## Standing invariants

Not tied to a single exchange, but always in force.

- **Initiative Shift ±X means exactly: the target's next turn arrives X turns sooner or later.** There are no rounds. Seats, the marker, pass-overs, and bonus turns are bookkeeping that enforces this sentence; when seat and count disagree, the count wins. The marker sits on a position, not a person; sliding (displacement from someone's cut-in) never changes anyone's count; Waiting sets your count to your chosen seat (the forfeited action is the payment). See `rules/card-glossary.md`, Initiative Shift X.
- **Blocking costs a card.** Every defense spends a card from hand. Hand size *is* blocking capacity between your turns — nobody blocks for free. The hand-size floor keeps you from *starting* a turn defenseless, but focus-fire between your turns can still empty your hand.
- **Derived stats.** Body → max HP (`2 × Body + 9`; only Body changes HP). Mind → hand size. Soul → initiative. Changes apply live, in both directions.
- **The deck reshuffles from discard.** When a deck runs out it is rebuilt from its discard pile — cards do not leave the game by default. (Consequence, not a rule: because decks are small and recycle constantly, deck-state manipulation like scry/surveil is near-neutral in combat, while read/tempo/timing effects move outcomes.)
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
| Intercept | who defends (ally substitutes) | next attack (team) |
| Initiative Shift | wheel position | immediate |
| Armour / Resist | damage pipeline (reduction) | per hit / next hit |
| Fortress / Shared Burden | damage pipeline (reassignment) | next hit (team) |
| Evade | whether an attack connects | next attack (chance) |

---

## Adding a rule-bender

Today each modifier is a per-combatant flag read inline at the one pipeline step it affects — the seam already exists. The agreed path (`memory.md`): flags → typed modifiers-with-lifetimes → policy stack. Promote a level only when adding the next bender as a flag has become painful.

Until then, a new bender should: (1) name the invariant above that it changes, (2) set a flag with a clear expiry, (3) read that flag at exactly one pipeline step, (4) revert on expiry. If a mechanic can't be expressed that way — if it needs the engine to special-case resolution in more than one place — that is the signal it wants the policy-stack architecture, and a red flag worth raising before it ships.
