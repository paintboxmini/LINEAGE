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

## Reference Files

- System tone: `CLAUDE.md`
- Location examples: `locations/briarwatch.md`, `locations/vultures-nest.md`
- Faction examples: `world/the-regency.md`
- Mechanics: `rules/card-glossary.md`, `rules/combat.md`
