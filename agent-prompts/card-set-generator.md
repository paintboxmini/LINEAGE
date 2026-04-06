# Card Set Generator Prompt

Use this prompt to generate new 9-card enemy sets. Read the target creature's bestiary entry and relevant location files before running.

---

```
Create a 9-card enemy set for Tales Untold (3 Red, 3 Blue, 3 Green).

Constraints:
- Cards must share a unified identity (creature, faction, or role)
- Each color should express that identity differently
- Avoid duplicate effects across cards
- Effects should interact with positioning, deck state, or timing

System context:
- Red = pressure, force, punishment
- Blue = information, manipulation, prediction
- Green = support, stabilization, positioning
- Only use keywords from the approved list (see experimental/README.md)
- No new keywords without explicit approval

Output format:

For each card:
NAME (Color — Stat — LOCATION TAG if applicable)
Attack: Stat + die
Effect:
Defensive Bonus:
Range:
"flavor text"

Before finalizing:
1. Check for overlap or redundancy across all 9 cards
2. Ensure each card reinforces the creature's identity
3. Replace any generic effects with system-specific ones
4. Verify clarity of targeting and timing on every card
5. Confirm all keywords exist in the approved list

Return final 9 cards only.
```

---

## Loop Rules

After generating 9 cards, run the red team pass (`red-team.md`). Fix or replace failing cards, then re-red-team until all 9 pass. Present all 9 to Drew with your recommendation on the strongest. Drew decides where they land.

## Reference Files

- Keyword list: `experimental/README.md`
- Keyword definitions: `rules/card-glossary.md`
- Card examples: `cards/alignment-marshal-engine.md`, `cards/stonecoil-hollow.md`
- Loop rules: `experimental/README.md`
