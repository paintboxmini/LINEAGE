# Encounter Generator Prompt

Use this prompt to generate new Tales Untold encounters. Paste it into a new agent session along with relevant repo context (bestiary entries, card files, current keyword list from `experimental/README.md`).

**Before starting:** Create `experimental/scratch-[task].md` for all reasoning, math, and mechanical tradeoffs. Delete it before committing. Nothing from the scratch file goes into the content file.

---

## Onboarding — Required Reading Before Drafting

Do not draft until all of this is done. Encounters built without calibration end up the wrong weight for their tier and fight the engine instead of using it.

1. **`rules/combat.md` and `rules/core-rules.md`** — attack resolution, the tie rule, positioning, the range matrix, and the initiative wheel. Encounter mechanics must run on these, not around them.
2. **`rules/combat-example.md`** — a full fight played out beat by beat. This is what your encounter will feel like at the table; design for that texture.
3. **`rules/card-glossary.md`** plus the approved keyword list in `experimental/README.md` — exact keyword phrasing only, nothing pending, nothing new without approval.
4. **Difficulty tier conventions** (`CLAUDE.md`, Stat Blocks) — Early / Mid / Late definitions. If the brief doesn't state a tier, ask before building.
5. **Two or three bestiary entries near the target tier** — e.g., `bestiary/briar-scratcher.md` and `bestiary/delve-roller.md` for Early. Calibrate stats against them; HP is always (3 × Body) + 6.
6. **The enemy deck convention** (`rules/cards.md`, Deck Building) — 3 signature cards + 4–7 core cards; enemies draw to hand size like everyone else.
7. **Encounter examples** — `quests/shifting-burrow.md`, `quests/hollow-below-briarwatch.md` — for structure, tone, and how a lesson gets taught through play.

---

```
Create a full encounter for Tales Untold.

Constraints:
- Early or mid game (state which)
- Must teach a mechanic through play (not explanation)
- Use simple, clean effects
- Avoid generic damage-only actions
- Keep complexity appropriate to tier

System context:
- Positioning matters (Frontline / Backline)
- Movement can trigger consequences
- Status cards (Wound, Exhaust, etc.) go into decks
- Defensive Bonuses trigger when the defender wins the RPS, and on ties (unless the attacker's Effect cancels them)

Output format:

ENCOUNTER NAME

Intent:
(What this encounter teaches)

Setup:
(Environment, positioning constraints)

Enemies:
(Name + short behavioral identity)

Enemy Cards (3):
- Name (Color — Stat)
- Attack: Stat + die
- Effect:
- Defensive Bonus:
- Range:

Behavior Notes:
(How enemies act and what triggers them)

Win Condition:

Before finalizing:
1. Compare with repo patterns (naming, tone, structure)
2. Identify at least 2 weaknesses or inconsistencies
3. Fix them
4. Ensure no ambiguous targeting, no redundancy with existing cards,
   and the encounter teaches its intended lesson through mechanics
5. Remove any visible reasoning — if design thinking is readable in the output, it didn't finish

Return final version only.
```

---

## Reference Files

- Keyword list: `experimental/README.md`
- Keyword definitions: `rules/card-glossary.md`
- Encounter examples: `quests/shifting-burrow.md`, `quests/hollow-below-briarwatch.md`
- Tone reference: `cards/alignment-marshal-engine.md`

---

*Optional: run `prompt-refinement.md` after completing this task.*
