# Build Archetypes

A design compass, not canon. These names never appear at the table and never surface to players — Drew's explicit call: "at the table archetypes aren't revealed, they are naturally discovered." They exist here to check design space against (what's been explored, what hasn't) and to give a new card a lineage to check itself against, the same way `rules/card-glossary.md` gives a mechanic one. Nothing below is a Rule Definition, an Invariant, or a promise to players — see CLAUDE.md's Four Kinds of Canonical Content for why this needed its own, fourth kind of home instead of living in any of those three, or in `memory.md`.

Status marks what's actually shipped, not what's just named. A named-but-unbuilt archetype is a real, open gap — not a mistake.

---

**The Escalator** — named, not yet fleshed out.

**The Opportunist** — named, not yet fleshed out.

**The Gambler** — embraces variance; wagers now for a bigger (or worse) outcome later. GAMBLER'S RUIN (existing core card) is the dice-variance seed. Berserker's Price (`cards/red-body.md`) is a close cousin in shape, not archetype-tagged to it specifically. In progress: a card trading an upfront benefit for Exhaust cards seeded into hand.

**The Builder** — Mason philosophy: "I changed the battlefield, deal with it." Zones/Beacons/Hazards as persistent, position-tied area effects. Shipped: MENDING GLYPH, HONING GLYPH, BARBED GLYPH, CIPHER GLYPH (`cards/mason-glyphs.md`) — the first targetable, non-combatant battlefield entities in the game. Combat-simulator support still pending (queued for Sync).

**The Parasite** — predation: drains, hijacks, steals; takes from the opponent rather than copying or inventing. Distinguished from Mirror in the same conversation that named both: Mirror imitates and takes nothing, Parasite predates. Shipped: DRAIN, CONSUME (`cards/red-body.md`, `cards/green-soul.md`). Still unbuilt: HIJACK (name locked, steals a random card from an opponent's hand, returns it at combat's end — needs new cross-hand-transfer and combat-end-return engine infrastructure, neither exists yet). Also flagged, not built: "attack using the opponent's own stat" would be a genuine simulator first — nothing currently reads a different combatant's stat for its own damage roll.

**The Collector** — named, not yet fleshed out.

**The Coward** — confirmed as Rasp's own kit (`characters/rasp.md`), generalized into a reusable template rather than being personal to her specifically. Untargetable-while-Backline as the thesis (OUT OF REACH), chip damage over commitment.

**The Judge** — "very Tales Untold" (Drew). Punishes symmetry/pattern — e.g., both Frontlines occupied. Not yet built.

**The Teacher** — an antagonist whose cruelty is *improving* the player mid-fight: rewards reading, punishes sloppy play. A genuinely distinct emotional register from every other archetype here — not yet built.

**The Mirror** — imitation: copies actions/buffs, takes nothing (the line drawn against Parasite, above). Shipped: STARING CONTEST (Initiative reposition), WAITING GAME (copies up to two Positive Status Effects), AFTERIMAGE (mirrors color+stat of whoever acted before you), FOLLOW-UP (fully becomes a copy of an ally's last reveal) — all in `cards/colorless.md` and `cards/red-body.md`. Still unbuilt: a card that copies the *actual color* of whoever went before, distinct from Afterimage's stat-mirroring (discussed, not built).

**The Cultivator** — "plants delayed effects, improves cards instead of immediately benefiting, invests now for larger future turns... likes Builders because both create persistent state." Question: *what can I nurture?* Grew out of a real gap check — nothing spent a player's own future turn as a cost or an investment before this. Shipped: SEED (`cards/green-soul.md`) — plant now, telegraphed, pays out the next time you begin a turn back at the same position; no counter tracked, Position itself is the gate.

**The Weaver** — "makes unrelated mechanics interact... turns two average cards into one powerful interaction" (example: AXIOM + PARADOX). Question: *what can I connect?* Not yet built toward.

---

## Standing principles that came out of building these

- **A keyword should never be a card's whole idea — only where the idea lands**, after everything else about the card (a trigger condition, a cost, a pillar interaction) has already made it distinct. Reusing Deadly/Resist/Weak across many cards is fine; a card whose entire identity is "grants Deadly" is under-designed regardless of which keyword.
- **Telegraph, don't conceal, when a mechanic could go either way.** "The game's about interaction. It's no fun if the opponent doesn't have a chance to interact." (Drew) — the standing tiebreaker for any new mechanic with a visibility question.
- **A build should touch all three pillars (RPS, Initiative, Position) or have a stated reason not to** — not a hard rule, but the check worth running before calling an archetype's first card finished.
