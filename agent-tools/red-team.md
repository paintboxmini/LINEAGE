# Red Team Prompt

Use this prompt to review cards, encounters, or any game content before it goes to canon.

---

```
Analyze the following content for Tales Untold.

Focus on:
- Ambiguity (unclear targeting or timing)
- Redundancy (duplicate or overlapping effects)
- Tone mismatch (does it fit the system identity?)
- Mechanical weakness (effects that don't matter in play)
- Keyword compliance (only approved keywords in use)
- Visible reasoning (unfinished thinking left in the output)

Steps:
1. List at least 3 issues
2. Explain why each is a problem
3. Provide corrected versions

Do not rewrite everything — only fix what is necessary.
```

---

## Additional Pass: Quest / Encounter Review

If the content involves a quest, location, or narrative sequence, also evaluate:

```
1. Player Agency
   - Are there multiple ways players can approach this?
   - Is any outcome forced or overly linear?

2. Pressure & Tension
   - What pressures the player to act?
   - Is there a meaningful cost to delay, ignore, or rush?

3. Clarity Through Play
   - Are mechanics taught through interaction rather than explanation?
   - Would a player understand what matters by experiencing it?

4. Consequence
   - Do player choices create immediate or delayed consequences?
   - Are outcomes meaningfully different based on behavior?

5. Friction Points
   - Where might players get confused or stall?
   - Where might they disengage?

6. System Integration
   - Does this reinforce core systems (positioning, deck state, timing)?
   - Or does it feel disconnected from gameplay?

Steps:
- Identify at least 2 issues in the above areas
- Explain why they matter
- Suggest minimal fixes

Do not add new content unless necessary — refine what exists.
```

---

## Visible Reasoning — What to Look For

Unfinished reasoning leaves marks. Flag any of the following:

- **Mechanical scaffolding** — action lists, design intent notes, or structural placeholders that belong in a scratch file
- **Self-explaining content** — text that tells you what a mechanic is supposed to do instead of just doing it ("this passive is intended to teach X")
- **Designer hedging** — conditional language that reflects uncertainty rather than fiction ("this could also work as...")
- **Justification text** — narrative reasons for why a mechanic exists, written as if convincing someone rather than describing the world
- **Orphaned details** — specifics that were there to help the agent reason but serve no purpose in play

If removing flagged text breaks the content, the content isn't finished. Send it back.

---

## What to Check Against

- Keyword list: `experimental/README.md`
- Keyword definitions: `rules/card-glossary.md`
- Tone reference: `cards/alignment-marshal-engine.md`
- Existing cards for redundancy: `cards/red-body.md`, `cards/blue-mind.md`, `cards/green-soul.md`

---

*Optional: run `prompt-refinement.md` after completing this task.*
