# Encounter Generator

Use this to build new Tales Untold encounters. The output is repo files, not a chat block — see File Routing below.

**Scratch work:** reasoning, math, and tradeoffs go in `experimental/scratch-[task].md` (or the session scratchpad), never in the content files. Delete scratch files before committing.

---

## Onboarding — Before Drafting

Encounters built without calibration end up the wrong weight for their tier and fight the engine instead of using it.

1. **`agent-tools/exemplars.md`** — the compiled crib: engine facts, tier anchors, formats, deck and tag conventions, skeletons, tone. This replaces the old full-canon read list for routine work.
2. **The location the encounter lands in** — its file in `locations/`. The best hooks are usually already there; listen before inventing.
3. **Escalate to full canon only when needed:** bending or brushing a rule → `rules/invariants.md` + the relevant rules file; using a keyword in a novel way → its exact text in `rules/card-glossary.md`; designing off an existing creature → its bestiary entry. If the crib looks stale against canon, flag it for the Pending-propagation ledger.
4. Tier not stated in the brief? Ask before building.

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
