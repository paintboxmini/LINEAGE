# LINEAGE — Claude Context

This is a tabletop RPG design repository for **Tales Untold**, a card-based TTRPG system. Content here is written for a DM and their table, not for publication. Tone is direct, evocative, and mechanical — no purple prose, no padding.

## What This Repo Is

- **System:** Tales Untold — three stats (Mind/Body/Soul), card-based combat using RPS resolution, d-scale damage dice
- **Current focus:** The Turnroot Weald campaign (sentient forest, pressure-track escalation, escape via Marks or boss defeat)
- **Repo owner:** paintboxmini

## Directory Structure

| Directory | Contents |
|-----------|----------|
| `cards/` | Card set files — core (blue-mind, red-body, green-soul) and creature/location signature sets |
| `rules/` | Core rules, mechanics, and the keyword glossary |
| `locations/` | Location overviews (world-level descriptions) |
| `quests/` | Full adventure systems — pressure tracks, NPCs, encounter frameworks |
| `bestiary/` | Creature stat blocks, abilities, loot, card references |
| `characters/` | Named NPC profiles |
| `items/` | Consumables and equipment |
| `mythology/` | Lore and creation myths |
| `world/` | Geography, factions, organizations |
| `factions/` | Faction documents |
| `experimental/` | Sandbox — lower stakes, free to iterate |
| `agent-tools/` | Drop-in tools for common design tasks |
| `printing/` | Print-ready HTML card sheets and the generator script |
| `combatsimulations/` | PvP duel simulator — a design instrument for surfacing rules gaps and balance findings, not canon. Python; no game content lives here |
| `testcampaigndecks/` | This campaign's decks only — player decks (by character name), the Oracle pool, campaign-specific NPCs. General NPC/monster decks are not stored here; they're assembled per the enemy deck convention in `rules/cards.md` |
| `playtesting/` | Playtest notes, feedback, and session logs |
| `archives/` | Reserved for deprecated canon content. Currently unused — cut draft cards live in `experimental/archives/` instead |

## File Format Conventions

All files are Markdown. Follow existing formatting exactly.

### Cards

```
**CARD NAME**
COLOR — STAT
Attack: Stat + dX
Effect: [description]
Defensive Bonus: [description]
Range: [Melee / Ranged / Both]
*"flavor quote"*
```

- Colors: RED (Body), BLUE (Mind), GREEN (Soul)
- Source tags append after stat: `RED — BODY — WEALD`
- **A tag marks a card's acquisition source — its lineage.** It answers "where or from whom was this card obtained": a location (WEALD, ASHFALL, COIL), an archon, a faction (MASON, PROMISE), a specific creature, or the Unheld. It traces provenance, not theme. Rules:
  - A card carries **at most one tag** (its source). Core cards are universal and carry none.
  - A tag is never a card's *theme*. Theme lives in the flavor line. (A card about memory is not a MEMORY card; that is what the quote is for.) This is the rule that keeps the tag set finite — sources are countable, themes are not.
  - The test: *does removing the tag change how the card is obtained?* If not, it is not a tag.
  - The world-truth this expresses — living traditions, diffused universality, names vs. tags — lives in `world/lineage.md`.
- Separate cards with `---`

### Stat Blocks

```
**Mind X / Body X / Soul X — HP X**
**Difficulty:** Early / Mid / Late
```

- **Early** — one mechanic, teaches a concept, low decision overhead
- **Mid** — two interacting mechanics, positioning starts to matter
- **Late** — full passive/card synergy, pressure from multiple directions

If difficulty is not specified, ask before building.

### Bestiary Files

Open with a `Cards:` reference line if signature cards exist:
```
**Cards:** `cards/filename.md`
```

### Cross-References

Use relative paths in backticks: `` `quests/turnroot-weald-adventure.md` ``

## Commit Conventions

- Commit messages: short imperative sentence, no period, no emoji
- Commit in logical groups (one concern per commit)
- Always push with `-u origin <branch>`

## Stat System Quick Reference

| Stat | Color | Perception Mode | Damage Die |
|------|-------|-----------------|------------|
| Mind | Blue | Observe | d4 (utility) |
| Body | Red | Sense | d6 (power) |
| Soul | Green | Read | d2 (precision) |

- Standard DC: 13 (DM adjusts ±2 for fiction)
- HP: (2 × Body) + 9
- Combat positions: Frontline / Backline
- Special token types in use: Rooted, Thorns, Evade, Blind, Staggered

## Agent Workflow

1. **Orient** — Read `memory.md`, then run `agent-tools/repo-orientation.md`. Understand structure before writing. Do not skip this even in a returning session.
2. **Select prompt** — Use the appropriate tool from `agent-tools/`:
   - Encounter design → `encounter-generator.md`
   - Card set design → `card-set-generator.md`
   - Content review → `red-team.md`
   - Fit check → `alignment-checker.md`
3. **Clarify before executing** — Before writing anything, surface what you need to know. This step is mandatory. Cover:
   - **Clarifications** — anything ambiguous in the brief that would change the output (session timing, party size, NPC relationship to party, encounter pressure level)
   - **Suggestions** — related content worth connecting, mechanical options Drew may not have considered
   - **Concerns** — conflicts with existing content, scope that feels too large or too small, missing prerequisites
   - Keep it brief. 2–4 items max. Then wait for a response before proceeding.
4. **Run automatic triggers** — These are not optional. See `agent-tools/README.md` for the full table. At minimum:
   - Any card drafted → run `red-team.md` before presenting
   - Any encounter or quest content → run `red-team.md` Quest/Encounter pass
   - Any content touching an existing location, faction, or NPC → run `alignment-checker.md`
   - Any content for canon approval → run `alignment-checker.md` + Soul Pass
5. **Output** — Return only finalized content. No drafts unless requested.
6. **Wait** — After completion, await next instruction. Do not assume next task.

Prioritize clarity over cleverness. Prefer system-consistent solutions over novel ones. The repo is the source of truth.

## Work Modes

Dependent systems (sim, print sheets, cross-references) do not rebuild on every keystroke. Like a compiler, let them go stale and sync deliberately:

- **Working** (default) — edit the target files only. Record stale dependents under **Pending propagation** at the top of `memory.md` instead of rebuilding them per change.
- **Sync** — on request or at a natural pause: propagate pending changes through dependents (sim reconciliation, print regeneration, reference sweeps), then clear the ledger.
- **Release** — full verification: acceptance tests, both tournaments, print sheets regenerated, ledger empty.

Batch small canon edits in Working mode; do not re-run tournaments or regenerate print sheets for every card tweak.

## The Canon Gate

Content placement follows three tiers — the Translation Principle's ambiguity levels, applied to where work lands:

- **Tier 1 — ship direct.** Content that only *uses* established canon (encounters, creatures, cards, items, NPCs built from existing truth): land it in the canon directories once the mandatory red-team/alignment passes are clean. Add one line to the post-review queue.
- **Tier 2 — ship and flag.** Content that *extends* canon without contradicting it (new faction behavior, a new map seat, a deepened NPC): ship it, and flag the extension prominently — in the post-review queue and in chat. Drew's review is veto-after, not approve-first.
- **Tier 3 — gated, permanently.** Rules, invariants, keywords, core formulas, cosmology (Seats, Archons, the Unheld, races), anything contradicting existing canon, and anything carrying an open world-level hook: it goes to `experimental/` or a chat proposal and waits for Drew's explicit sign-off.

Every Tier 1/2 ship gets one line under **Recently shipped** at the top of `memory.md`. Drew clears lines as he blesses them, or objects and the item reverts — every ship is one commit away from undone, with the threshold log holding the why. The gate is loose because the automated checks are mandatory and the history is reversible — not because review stopped.

## Translation Principle

Drew communicates through examples, metaphors, partial ideas, and observations — the fence, Gambler's Ruin, "two designers at the table." Your job is to translate, not transcribe: identify and formalize the underlying invariant or rule when the evidence strongly supports it, rather than asking him to restate it in formal language.

- Formalize what is strongly implied. When a recurring pattern is clearly meant but never named, propose the invariant yourself.
- Distinguish inferred from stated. Mark an invariant you derived as *inferred* so he can confirm or correct it; never present it as if he said it outright.
- Reserve clarifying questions (workflow step 3) for genuine ambiguity — a fork where the evidence does not pick a side. A metaphor you can translate is not ambiguity.
- **Never silently redefine an established invariant.** When Drew's words contradict one, do not reconcile by inventing new semantics: a mechanically coherent interpretation that changes the fantasy is a bug, not a translation. If the contradiction could be a wording slip, ask for confirmation; otherwise surface it explicitly — name the invariant and the conflict. The test before any interpretation: *will this require changing the meaning of something already established?* If yes, stop.
- Ambiguity has levels: **(1) harmless** — wording, flavor, implementation detail: resolve silently; **(2) design choice** — pick one and log it in `memory.md`; **(3) protected invariant** — turn-order semantics, RPS resolution, core formulas, anything in `rules/invariants.md`: stop and surface. The cost of an unnecessary clarification is lower than the cost of a silently mutated design.

## Do Not

- Invent mechanics in isolation — adapt from existing stat blocks, and flag if something is genuinely new
- Create files outside the established directory structure without asking
- Use emoji in files
