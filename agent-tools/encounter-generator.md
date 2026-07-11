# Encounter Generator

Use this to build new Tales Untold encounters. The output is repo files, not a chat block — see File Routing below.

**Scratch work:** reasoning, math, and tradeoffs go in `experimental/scratch-[task].md` (or the session scratchpad), never in the content files. Delete scratch files before committing.

---

## Onboarding — Required Reading Before Drafting

Encounters built without calibration end up the wrong weight for their tier and fight the engine instead of using it.

1. **`rules/combat.md` and `rules/core-rules.md`** — attack resolution, the tie rule, positioning, the range matrix, the initiative wheel, and the **Wait action** (turn-order repositioning is a player tool now; encounters can teach or test it).
2. **`rules/invariants.md`** — the resolution contract. An encounter mechanic that bends an invariant must say so explicitly and is a red-team flag, not a house rule.
3. **`rules/combat-example.md`** — a full fight beat by beat. This is the table texture you're designing for.
4. **`rules/card-glossary.md`** + the approved keyword list in `experimental/README.md` — exact keyword phrasing only. Hand size is **Mind, minimum 2**; nobody is ever reduced below act-plus-one-block.
5. **Difficulty tiers** (`CLAUDE.md`, Stat Blocks) — Early / Mid / Late. If the brief doesn't state a tier, ask before building.
6. **Two or three bestiary entries near the target tier** — e.g. `bestiary/briar-scratcher.md`, `bestiary/briarwatch-jackrabbit.md`, `bestiary/fencerow-shrike.md` for Early. Calibrate against them; HP defaults to (2 × Body) + 9, and Early creatures usually run below formula for fiction.
7. **The enemy deck convention** (`rules/cards.md`) — 3 signature cards + 4–7 core cards, 7–10 total; core picks lean toward the creature's stat spread.
8. **The tag convention** (`CLAUDE.md`, card format; `world/lineage.md`) — signature cards carry one source tag (the location or creature they're obtained from): `RED — BODY — BRIARWOODS`.
9. **Encounter exemplars** — `quests/shifting-burrow.md`, `quests/the-larder-fence.md` — for structure, tone, and how a lesson is taught through play rather than explanation.
10. **The location the encounter lands in** — its file in `locations/`. The best hooks are usually already there; listen before inventing.

---

## Design Constraints

- State the tier. Teach one mechanic (Early) or one interaction (Mid) **through play**, never through explanation.
- Run on the engine, not around it: positioning, the wheel, hand economy, and status-card pressure are your materials. The strongest twists are the ones the rules enforce for you.
- Simple, clean effects; no generic damage-only enemies; no new keywords without discussion.
- Effect and Defensive Bonus on a card should not be near-duplicates.
- Multiple viable player approaches where the fiction allows it; walking away can be a valid answer.

## File Routing

- **Encounter** → `quests/[name].md` (intent, setup, enemies, GM notes, win condition, related docs).
- **New creature** → `bestiary/[name].md` (stat block, `**Difficulty:**` line, behavior, `Cards:` reference) + `cards/[name].md` (signature cards, source-tagged).
- **Named NPC** (a person, even one with a combat statblock) → `characters/[name].md`, never `bestiary/`.
- **Anything carrying an open world-level hook** (an unexplained entity, a new faction behavior, a mystery whose answer isn't written) → **`experimental/` first.** Drew promotes to canon. Content that only uses established canon may land in canon directories directly.
- New cards make a print sheet stale — record it under **Pending propagation** in `memory.md` (Work Modes); do not regenerate mid-task.

## Before Presenting

1. Run `red-team.md` (Quest/Encounter pass) — invariants first.
2. Run `alignment-checker.md` if the encounter touches an existing location, faction, or NPC.
3. Surface anything that extends canon (new faction behavior, new truth about a place) as an explicit item for Drew's ruling — never let it ride in silently.
4. Remove visible reasoning. Present the encounters, the review findings, and the flagged rulings — nothing else.
