# NPC Encounter Generator Prompt

Use this prompt to generate short roadside or social NPC encounters. Designed for early game — tension without combat.

**Before starting:** Create `experimental/scratch-[task].md` for all reasoning, math, and mechanical tradeoffs. Delete it before committing. Nothing from the scratch file goes into the content file.

---

## Onboarding — Required Reading Before Drafting

Do not draft until all of this is done. An NPC written without this context sounds like a visitor to the setting instead of a resident of it.

1. **`world/tonal-bible.md`** — the register everything here is written in. Beauty and wrongness in the same space; no heroic-fantasy framing.
2. **`rules/resolution.md` and the DC table in `rules/core-rules.md`** — including the three Perception modes (Observe / Sense / Read). Noncombat tension runs on these checks; know which mode a moment calls for.
3. **Existing NPCs** — `locations/vultures-nest.md` (Aege, Bartho, Kino) for how this repo does function, pressure, and hook without exposition.
4. **The region the encounter lands in** — e.g., `locations/briarwoods.md`, `locations/roadhouse.md` for road encounters. The NPC should feel produced by the place.
5. **`memory.md` — Active Pending Threads** — so the NPC doesn't collide with, duplicate, or accidentally resolve an existing hook. Touching an established location, faction, or NPC also triggers `alignment-checker.md`.
6. **Status cards in `rules/card-glossary.md`** (Wound, Exhaust) — if the delayed consequence is mechanical, use the existing pressure systems, not invented ones.

---

```
Create a short roadside NPC encounter for Tales Untold.

Constraints:
- Early game
- Non-violent by default, but tension must be present
- Must allow multiple player approaches (ignore, engage, exploit)
- Must reinforce system themes (movement, consequence, observation, or tradeoffs)
- Keep it short, clean, and immediately playable

System context:
- Positioning and movement matter
- Consequences can be delayed (deck effects like Wound/Exhaust)
- NPCs should embody system rules, not explain them
- Avoid long dialogue or lore dumps

Output format:

ENCOUNTER NAME

Intent:
(What this interaction teaches)

Setup:
(Where and how players encounter it)

NPC:
(Name + Function / Pressure / Hook)

Interaction Options:
- 3–4 ways players might engage (no forced outcomes)

Outcomes:
(What changes based on player behavior)

Optional Mechanic:
(If applicable, include a light mechanical interaction)

Before finalizing:
1. Ensure NPC behavior reflects system rules
2. Remove any unnecessary exposition
3. Ensure at least one outcome has delayed consequences
4. Keep everything concise
5. Remove any visible reasoning — if design thinking is readable in the output, it didn't finish

Return final version only.
```

---

## Reference Files

- NPC examples: `locations/vultures-nest.md` (Aege, Bartho, Kino)
- Tone reference: `locations/briarwatch.md`, `locations/roadhouse.md`
- Delayed consequence examples: `bestiary/briar-scratcher.md`, `quests/shifting-burrow.md`

---

*Optional: run `prompt-refinement.md` after completing this task.*
