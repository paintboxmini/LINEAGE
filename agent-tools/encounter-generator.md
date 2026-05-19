# Encounter Generator Prompt

Use this prompt to generate new Tales Untold encounters. Paste it into a new agent session along with relevant repo context (bestiary entries, card files, current keyword list from `experimental/README.md`).

**Before starting:** Create `experimental/scratch-[task].md` for all reasoning, math, and mechanical tradeoffs. Delete it before committing. Nothing from the scratch file goes into the content file.

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
- Defensive bonuses trigger only on successful defense

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
