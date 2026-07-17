# Rulings Log

Assumptions the simulator had to make because the written rules didn't fully
specify them. This is the errata queue: **RESOLVED** entries are Drew's calls
already reflected in `rules/`; **OPEN** entries are engine simplifications or
genuine gaps awaiting a decision.

Regenerate the live list any time with `python3 run.py` (it prints at the end).

---

## Resolved (canon)

- **gamblers-ruin-explode** — Every odd result, including added dice, triggers
  another d4; capped at 3 extra rolls total. Card text already matches.
- **blood-tithe-mutual-death** — If Blood Tithe's bleed collapses both parties on
  the same tick, it's a mutual result → tie. In `rules/combat.md` Simultaneous
  Effects.
- **paradox-tie** — Paradox reverses a win/loss, but a tie has no outcome to
  reverse and is unchanged. On the card.
- **simultaneous-order** — When effects resolve at once, their controller orders
  them; different controllers → the active player decides. In `rules/combat.md`.
- **single-hit-floor** — A single attack cannot push a standing combatant below 0
  (clamp to Collapse). Matches `rules/combat.md` Collapse.
- **evade-consumes-attack** — A dodged attack still spends the attacker's card and
  its Effect doesn't fire. From `rules/combat-example.md`.
- **axiom-blocks-defense** — Axiom's banned color can't be revealed to *defend*
  either; the ban is on the next reveal, attack or block. Consistent with the
  reveal-timing rules; worth a one-line confirmation on the card if you want it
  airtight.
- **twin-strike-double-roll** — `(Soul + d2) x2` is two independent (Soul + d2)
  rolls summed, not one roll doubled. Drew ruling; matches the sim.
- **blood-tithe-dead-heal** — In a duel the "heal an ally for 4" half is wasted
  (You Are Not Your Own Ally); Blood Tithe is pure self-harm in 1v1. Working as
  intended (Drew) — a party-play card, and PvP is a design instrument.
- **twin-strike-double-roll** — Two independent (Soul + d2) rolls summed. Drew.
- **balance-double / balance-knockdown** — Balance's double-hit and its knockdown
  (foe loses their next action to stand) are the intended implementation. Drew.
- **stat-change-derived** — A changed stat drives its own derived value in real
  time: **Body → max HP** (±3/point, clamps HP, can Collapse — Body ONLY touches
  HP), **Mind → hand size** (live; forces a discard if now over), **Soul →
  initiative**. Both directions. General rule in `rules/card-glossary.md` (Stat
  Change); sim in `Combatant.adjust`.
- **wound-counts-visible** — Press the Wound and Taint count Wounds in **hand +
  discard only**, never the deck — so nobody has to track or search hidden Wounds
  (Drew). Sim: `wounds_visible`.
- **wound-persists** — A Wound no longer auto-discards; it sits in the hand
  occupying a slot until an **action** discards it (to the discard pile). Short
  rest permanently **destroys** 1 Wound from hand or discard (not the deck). Drew;
  in the glossary WOUND entry, the engine, and the worked example.
- **debuff-scope** — Debuff = status conditions, status cards, stat reductions,
  forced moves (Ward blocks these). Discard and scry-your-deck are NOT debuffs and
  ignore Ward (Obscure answers those instead). Drew; in the glossary Debuff entry.
- **equal-footing-floor** — Consumed by the next attack against you regardless of
  outcome (a miss or a defended hit still spends it). Now modeled that way in the
  engine.

## Expected in 1v1 — will matter in the team sim

Not gaps: these are cards whose text needs allies or multiple enemies, so they
correctly do nothing in a duel. The full goal is a team-vs-team sim; flagged so
they aren't mistaken for bugs.

- **mockery-taunt-dead / partition-shield-dead** — "must attack you" / "ally
  can't be targeted" need more than one enemy / an ally to matter.

## Accepted simplifications (final — Drew signed off)

- **gap-retaliate** — Blood in the Gap's "steal 2 each time you're damaged"
  models a single next-damage rider, not a persistent per-instance one. Accepted
  as-is; the difference is negligible in practice.
- **stalemate-cap** — duels past the turn cap score as draws (engine safeguard,
  not a rule); effectively never triggers with attacking policies. Accepted.

## Resolved by implementation

- **scry** — Scry is now a real mechanic: `engine.scry(actor, owner, x)` lets a
  brain reorder the top of any deck (own or enemy), driven by a composable
  `ScryMixin` sub-brain every policy shares. Own-deck: surface value, bury Wounds.
  Enemy-deck: bury their threats and the color that beats your attacks, leave
  junk (and their Wounds) on top. Wired to ALIGN (own) and AXIOM's defense (enemy).
- **Initiative Shift, rewritten to match the current Wheel** — `_apply_shift`
  now walks the actual circular path between a token's old and new slot
  (`rules/combat.md`, `rules/card-glossary.md`), correctly for any wheel size,
  replacing the old count-based approximation this file used to flag as
  imprecise at 3+ combatants. Verified against all confirmed worked cases in
  `rules/initiative-shift-examples.md`. Positive shifts are fully modeled now,
  including the bonus-turn case — URGENCY's defensive +1 (was +3, rebalanced
  since) can genuinely grant an extra turn where the math calls for it in a
  2-token duel, which the old code never actually produced for this roster.
  INTERRUPT's defensive shift was reworked the same day (now -1 to the
  attacker, was +3 to self) and no longer applies a positive shift at all.
  Reshifting a token that
  already holds a pending skip/bonus chip is hard-coded rather than derived:
  the general boundary-crossing formula would predict a bonus in the one
  confirmed case, but the canon ruling says it goes normally, so a reshift of
  an already-pending token unconditionally skips the boundary/chip check —
  asserted as a blanket rule for every variation, since only that one case is
  confirmed and there's no arithmetic basis to special-case the others.

---

*This log is generated by design work, not play. It documents what an automated
engine needed to know — which is a good proxy for what a new player or AI will
trip over.*
