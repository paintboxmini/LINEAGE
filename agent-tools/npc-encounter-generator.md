# NPC Encounter Generator Prompt

Use this prompt to generate short roadside or social NPC encounters. Designed for early game — tension without combat.

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
