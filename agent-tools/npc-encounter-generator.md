# NPC Encounter Generator

Use this to build short roadside or social NPC encounters — tension without combat, for early game especially. Output is repo files, not a chat block — see File Routing below.

**Scratch work:** `experimental/scratch-[task].md` (or the session scratchpad); delete before committing.

---

## Onboarding — Required Reading Before Drafting

An NPC written without this context sounds like a visitor to the setting instead of a resident of it.

1. **`world/tonal-bible.md`** — the register. Warmth containing something wrong; no heroic-fantasy framing; the world is not organized around the party.
2. **`rules/resolution.md` and the DC table in `rules/core-rules.md`** — the three Perception modes (Observe / Sense / Read). Noncombat tension runs on these; know which mode a moment calls for.
3. **Existing NPCs** — `locations/vultures-nest.md` (Aege, Bartho, Kino) and `experimental/the-man-who-buys-wounds.md` (Weck) for how this repo does **Function / Pressure / Hook** without exposition.
4. **The region** — the location file the encounter lands in. The NPC should feel produced by the place.
5. **`memory.md` — active threads and the branch map** — so the NPC doesn't collide with, duplicate, or accidentally resolve an existing hook.
6. **Status cards** (`rules/card-glossary.md` — Wound, Exhaust) — if the encounter has mechanical teeth, use the existing pressure systems, not invented ones. A bargain that touches the Wound economy is strong precisely because the economy is real.

---

## Design Constraints

- Non-violent by default; the tension is in the terms, the silence, or the thing not explained.
- **Function / Pressure / Hook** for the NPC — what they do, what they want without saying, what they leave behind.
- 3–4 player approaches, none forced; refusing or walking on is always a complete answer.
- Delayed consequences beat immediate ones — a name in a ledger, a debt unpriced, a favor remembered.
- The NPC embodies system rules; they never explain them.
- Leave the biggest question deliberately unanswered **and say so in the file** — the answer belongs to Drew, not the generator.

## File Routing

- **The encounter** → `experimental/[name].md` by default. A new NPC almost always carries an open hook (that is what makes them good), and open hooks are Drew's to ratify — canon placement comes with promotion, not authorship.
- **A recurring, ratified NPC** graduates to `characters/[name].md` (people go in `characters/`, never `bestiary/`, even with a combat statblock) with their encounter in `quests/`.
- If the NPC has combat cards: `cards/[name].md`, source-tagged per the lineage convention (`CLAUDE.md`, card format).

## Before Presenting

1. Run `red-team.md` — check any mechanical offer for zone/timing ambiguity (where exactly does the Wound come from; when exactly does the effect happen).
2. Run `alignment-checker.md` — especially against existing NPC threads.
3. Flag the open hook explicitly as Drew's to answer.
4. Remove visible reasoning; present the encounter, the findings, and the flagged hook — nothing else.
