# NPC Encounter Generator

Use this to build short roadside or social NPC encounters — tension without combat, for early game especially. Output is repo files, not a chat block — see File Routing below.

**Scratch work:** `experimental/scratch-[task].md` (or the session scratchpad); delete before committing.

---

## Onboarding — Before Drafting

An NPC written without this context sounds like a visitor to the setting instead of a resident of it.

1. **`agent-tools/compiled-crib.md`** — Perception modes and DCs, the Function/Pressure/Hook register (Weck exemplar — see `agent-tools/exemplars.md`), status-card pressure, tone in one breath.
2. **The region** — the location file the encounter lands in. The NPC should feel produced by the place.
3. **`memory.md` — active threads** — so the NPC doesn't collide with, duplicate, or accidentally resolve an existing hook.
4. **Escalate to full canon only when needed:** full register → `world/tonal-bible.md`; more voice exemplars → Aege/Bartho/Kino in `places/vultures-nest.md`; exact status-card text → `rules/card-glossary.md`.

---

## Design Constraints

- Non-violent by default; the tension is in the terms, the silence, or the thing not explained.
- **Function / Pressure / Hook** for the NPC — what they do, what they want without saying, what they leave behind.
- 3–4 player approaches, none forced; refusing or walking on is always a complete answer.
- Delayed consequences beat immediate ones — a name in a ledger, a debt unpriced, a favor remembered.
- The NPC embodies system rules; they never explain them.
- Leave the biggest question deliberately unanswered **and say so in the file** — the answer belongs to Drew, not the generator.

## File Routing

- **Route by the Canon Gate (`CLAUDE.md`):** an NPC carrying an open world-level hook (usually what makes them good) is constitutional (Authority 3) → `experimental/[name].md`, awaiting Drew's ratification. An NPC built entirely from established canon is Authority 1 → `quests/[name].md` directly, queued for post-review.
- **A recurring, ratified NPC** graduates to `characters/[name].md` (people go in `characters/`, never `bestiary/`, even with a combat statblock) with their encounter in `quests/`.
- If the NPC has combat cards: `cards/[name].md`, source-tagged per the lineage convention (`CLAUDE.md`, card format).

## Before Presenting

1. Run `red-team.md` — check any mechanical offer for zone/timing ambiguity (where exactly does the Wound come from; when exactly does the effect happen).
2. Run `alignment-checker.md` — especially against existing NPC threads.
3. Flag the open hook explicitly as Drew's to answer.
4. Check against `red-team.md`'s Visible Reasoning section; present the encounter, the findings, and the flagged hook — nothing else.
