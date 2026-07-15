# Card Set Generator Prompt

Use this prompt to generate new 9-card enemy sets. Read the target creature's bestiary entry and relevant location files before running.

**Before starting:** Create `experimental/scratch-[task].md` for all reasoning, math, and mechanical tradeoffs. Nothing from the scratch file goes into the content file.

---

## Onboarding — Before Drafting

Cards written without calibration read fine in isolation and wrong next to everything else.

1. **`agent-tools/compiled-crib.md`** — keyword list, card formats with calibrated core + signature examples, die philosophy, deck and tag conventions, ally-wording rules.
2. **The color's core file for your target colors** (`cards/red-body.md` / `blue-mind.md` / `green-soul.md`) — duplication check: if your effect already exists on a core card, it isn't a signature effect.
3. **`experimental/archives/cut-cards.md`** — do not re-draft a cut card without addressing why it was cut.
4. **Escalate to full canon only when needed:** a keyword used in a novel way → its exact text in `rules/card-glossary.md`; a design-quality check → `agent-tools/design-principles.md`; touching the simulator's own resolution logic → `rules/invariants.md`; one comparable signature set for identity texture (e.g. `cards/tollbird.md`).

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
6. Check against `red-team.md`'s Visible Reasoning section — if design thinking is readable in the output, it didn't finish

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
