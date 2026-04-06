# Encounter Generator Prompt

Use this prompt to generate new Tales Untold encounters. Paste it into a new agent session along with relevant repo context (bestiary entries, card files, current keyword list).

---

```
Create a full encounter for Tales Untold.

Constraints:
- Early game difficulty
- Must teach a mechanic through play (not explanation)
- Use simple, clean effects
- Avoid generic damage-only actions
- Keep complexity low

System context:
- Positioning matters (Frontline / Backline)
- Movement can trigger consequences
- Status cards (like Wound, Exhaust) exist and go into decks
- Defensive bonuses only trigger on successful defense

Output format:

ENCOUNTER NAME

Intent:
(What this encounter teaches)

Setup:
(Environment, positioning constraints)

Enemies:
(Name and short behavior description)

Enemy Cards (3):
- Name (Color — Stat)
- Attack: Stat + die
- Effect:
- Defensive Bonus:
- Range:

Behavior Notes:
(How enemies act / what triggers them)

Win Condition:
(How players resolve encounter)

Keep everything consistent with the system.

Before finalizing:

1. Compare your output against existing repo files for consistency in:
   - wording
   - mechanics
   - tone

2. Perform one red-team pass:
   - Identify at least 2 weaknesses or inconsistencies
   - Fix them

3. Ensure:
   - No ambiguous targeting
   - Effects are not redundant with existing cards
   - The encounter teaches its intended lesson through mechanics

Then present the final version only.
```

---

## Notes

- Always cross-reference the current keyword list in `experimental/README.md` before writing card effects
- Check `rules/card-glossary.md` for keyword definitions
- Existing encounter examples: `quests/shifting-burrow.md`, `quests/hollow-below-briarwatch.md`
- Tone reference: terse, mechanical, present tense — see `cards/alignment-marshal-engine.md`
