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
| `rules/` | Core rules quick reference |
| `locations/` | Location overviews (world-level descriptions) |
| `quests/` | Full adventure systems — pressure tracks, NPCs, encounter frameworks |
| `bestiary/` | Creature stat blocks, abilities, loot, card references |
| `items/` | Consumables and equipment |
| `mythology/` | Lore and creation myths |
| `world/` | Geography, factions, organizations |
| `factions/` | Faction documents |
| `experimental/` | Sandbox — write freely, nothing moves to canon without approval |
| `agent-prompts/` | Drop-in prompts for common design tasks |

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
- Location/set tags append after stat: `RED — BODY — WEALD`
- WEALD and similar tags indicate where a card is obtainable (Oracle deck, region-specific), not a replacement for the color system
- Separate cards with `---`

### Stat Blocks

```
**Mind X / Body X / Soul X — HP X**
```

### Bestiary Files

Open with a `Cards:` reference line if signature cards exist:
```
**Cards:** `cards/filename.md`
```

### Cross-References

Use relative paths in backticks: `` `quests/turnroot-weald-adventure.md` ``

## Branch & Commit Conventions

- Development branch: `claude/turnroot-weald-campaign-1mqjZ`
- Default branch: `claude/initial-setup-dqZCC`
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
- HP: (3 × Body) + 6
- Combat positions: Frontline / Backline
- Special token types in use: Rooted, Thorns, Evade, Rooted

## Agent Workflow

1. **Orient** — Read `memory.md`, then run `agent-prompts/repo-orientation.md`. Understand structure before writing. Do not skip this even in a returning session.
2. **Select prompt** — Use the appropriate tool from `agent-prompts/`:
   - Encounter design → `encounter-generator.md`
   - Card set design → `card-set-generator.md`
   - Content review → `red-team.md`
   - Fit check → `alignment-checker.md`
3. **Run automatic triggers** — These are not optional. See `agent-prompts/README.md` for the full table. At minimum:
   - Any card drafted → run `red-team.md` before presenting
   - Any encounter or quest content → run `red-team.md` Quest/Encounter pass
   - Any content touching an existing location, faction, or NPC → run `alignment-checker.md`
   - Any content for canon approval → run `alignment-checker.md` + Soul Pass
4. **Output** — Return only finalized content. No drafts unless requested.
5. **Wait** — After completion, await next instruction. Do not assume next task.

Prioritize clarity over cleverness. Prefer system-consistent solutions over novel ones. The repo is the source of truth.

## Do Not

- Add flavor text or lore that wasn't written or approved by the user
- Invent mechanics — adapt from existing stat blocks or ask
- Create files outside the established directory structure without asking
- Use emoji in files
