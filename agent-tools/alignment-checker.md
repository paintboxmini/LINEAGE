# Alignment Checker Prompt

Use this prompt to verify that new content fits its intended context before committing.

---

```
Evaluate whether the following content belongs in its intended context.

Check:
- Does it match the location or faction identity?
- Does it reinforce existing mechanics?
- Does it introduce anything that breaks system expectations?
- Does it match the tone of surrounding files?

Output:
- Fits / Needs Adjustment / Does Not Fit

If adjustment is needed:
- Specify exactly what to change
- Keep changes minimal
```

---

## Soul Pass

Run this after confirming structural alignment.

```
After confirming structural alignment, perform a Soul Pass.

Evaluate:

1. Does this evoke a clear feeling or tension?
   - If not, identify where it feels flat

2. Does the behavior/mechanics reinforce that feeling?
   - If not, suggest a minimal adjustment

3. Is there a strong hook or memorable detail?
   - If missing, add one (no more than 1–2 lines)

4. Does this feel distinct from generic fantasy/system design?
   - If generic, sharpen wording or framing

Constraints:
- Do NOT add lore dumps
- Do NOT increase complexity
- Do NOT change core mechanics unless necessary

Goal:
Enhance tone, clarity of feeling, and memorability without breaking structure.

Return only refined additions or changes.
```

---

## Reference Files

- System tone: `CLAUDE.md`
- Location examples: `locations/briarwatch.md`, `locations/vultures-nest.md`
- Faction examples: `world/the-regency.md`
- Mechanics: `rules/card-glossary.md`, `rules/combat.md`

---

*Note: Check against `red-team.md`'s Visible Reasoning section before presenting — if design thinking is readable in the output, it didn't finish.*

*Optional: run `prompt-refinement.md` after completing this task.*
