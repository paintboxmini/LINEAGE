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

## When the Soul Pass Fails — Finding the Angle

The Soul Pass detects flatness; it doesn't fix it. When something comes back flat, generic, or like it could exist in any TTRPG, dig with these — one good answer is enough to find the angle. *(Folded in from the archived `inspiration-guide.md`, 2026-07-23 — the generative half the Soul Pass never covered. Read `world/tonal-bible.md` first if you haven't.)*

**The core questions:**
- What is this thing's own logic, independent of what the party will do with it? A creature, location, or NPC that exists only in relation to the party is set dressing.
- What was here before? What will still be here after? The party is passing through. The world isn't.
- What's the beautiful version of this? What's the horrifying version? Are they the same thing? If they're not even close, it isn't deep enough yet.
- What rule does this follow so consistently it becomes its own kind of law? The Cenobites aren't scary because they're random — they're scary because they're not.
- If a child who grew up here described this, what would they call it? Children in this world use mythic logic; their vocabulary for strangeness is often more accurate than the adult rationalist framing.
- What does this want on its own terms? Not what the party wants from it. Not what the story needs it to do.

**Stuck on a location:** start from what it was before people arrived; find the one thing that doesn't fit the rest (that's usually the truth of the place); ask what the locals have stopped noticing; ask what the place takes from you over time — not combat cost, cost.

**Stuck on a creature:** ecology before combat role — what does it eat, where does it sleep, what avoids it? What does it do when there's nobody to fight? Find the beautiful version and the wrong version and build toward the overlap.

**Stuck on an NPC:** what have they seen that the party hasn't (their edge)? What have they decided to stop thinking about (their flaw)? What do they do when nobody is watching (their truth)? Warm and wrong, or cold and right — both are interesting, neither is safe. For the fuller, generative version of this — belief, wound, and what a person says when that belief is actually challenged — see `agent-tools/finding-a-voice.md`.

**The last check:** does it feel like it belongs to *this* world, or could it exist in any TTRPG? If it could exist anywhere, find the thing that makes it only possible here — under this sky, against the Unheld, with these rules. That thing is usually already in the content somewhere; it just needs to be moved to the front.

---

## Reference Files

- System tone: `CLAUDE.md`
- Location examples: `places/briarwatch.md`, `places/vultures-nest.md`
- Faction examples: `world/the-regency.md`
- Mechanics: `rules/card-glossary.md`, `rules/combat.md`

---

*Note: Check against `red-team.md`'s Visible Reasoning section before presenting — if design thinking is readable in the output, it didn't finish.*
