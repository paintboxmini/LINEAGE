# Card Set Generator Prompt

Use this prompt to generate new 9-card enemy sets. Read the target creature's bestiary entry and relevant location files before running.

**Before starting:** Create `experimental/scratch-[task].md` for all reasoning, math, and mechanical tradeoffs. Delete it before committing. Nothing from the scratch file goes into the content file.

---

## Onboarding — Required Reading Before Drafting

Do not draft a single card until all of this is done. Cards written without calibration read fine in isolation and wrong next to everything else.

1. **`rules/card-glossary.md`** — full read. When a card uses a keyword, its text must match the canonical definition exactly. If your effect needs a keyword that isn't here, stop — no new keywords without approval.
2. **Approved keyword list** (`experimental/README.md`) — includes anything pending canon approval. Pending keywords are not usable.
3. **All three core files** — `cards/red-body.md`, `cards/blue-mind.md`, `cards/green-soul.md`. This is the power baseline: damage dice, effect strength, defensive bonus weight, flavor voice. Also a duplication check — if your effect already exists on a core card, it isn't a signature effect.
4. **At least two signature sets** — e.g., `cards/alignment-marshal-engine.md`, `cards/stonecoil-hollow.md`, `cards/briar-scratcher.md`. Note how signature cards differ from core: tighter identity, effects that only make sense coming from this creature.
5. **`rules/cards.md`** — card anatomy, die philosophy (d6 power / d4 utility / d2 precision), deck-building conventions, and You Are Not Your Own Ally. Every "ally"/"enemy" wording must survive that rule.
6. **`experimental/archives/cut-cards.md`** — what has already been drafted and cut, and why. Do not re-draft a cut card without addressing the reason it was cut.

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
6. Remove any visible reasoning — if design thinking is readable in the output, it didn't finish

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

---

*Optional: run `prompt-refinement.md` after completing this task.*
