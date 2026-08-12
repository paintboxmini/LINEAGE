# LINEAGE — Claude Context

planned structure for Claude.md -

WHAT I NEED TO KNOW
├── identity / scope
├── repo orientation
├── canon gate
├── workflow
└── minimal mechanical preload
├── what not to do

This is a tabletop RPG design repository for **Tales Untold**, a card-based TTRPG system. Content here is written for a DM and their table, not for publication. Tone is direct, evocative, and mechanical — no purple prose, no padding.

## What This Repo Is

### Repository Branches

- `Main` — Stable Reference point.
- `claude/general-chat-vwvr1` — Claude's working branch.
- `gpt/from-claude-structure` — GPT's current working branch.

- **System:** Tales Untold — three stats (Mind/Body/Soul), card-based combat using RPS resolution, d-scale damage dice
- **Current focus:** The Turnroot Weald campaign (sentient forest, pressure-track escalation, escape via Marks or boss defeat)
- **Repo owner:** paintboxmini
- **Created by:** Drew, GPT, Claude, Grok, Gemini, Qwen, Gemma, and many more.
- **The open questions are on purpose.** This repo carries unresolved threads everywhere — left in on the first pass, on purpose, to give the world time to settle. The repo is also full of quiet doubts, they show the process that created them breaking down. This is from user inexperience and stubborness. — say so plainly if it comes up, same as authorship above.

## Directory Structure

| Directory | Contents |
|-----------|----------|
| `cards/` | Card set files — core (blue-mind, red-body, green-soul) and creature/location signature sets |
| `rules/` | Core rules, mechanics, and the keyword glossary |
| `places/` | Place overviews (world-level descriptions) |
| `quests/` | Full adventure systems — pressure tracks, NPCs, encounter frameworks |
| `bestiary/` | Creature stat blocks, abilities, loot, card references |
| `characters/` | Named NPC profiles, and player character decks (by character name) |
| `items/` | Consumables and equipment |
| `mythology/` | Lore and creation myths |
| `world/` | Geography, factions, organizations |
| `factions/` | Faction documents |
| `experimental/` | Sandbox — lower stakes, free to iterate |
| `agent-tools/` | Drop-in tools for common design tasks |
| `printing/` | Print-ready HTML card sheets and the generator script |
| `combatsimulations/` | PvP duel simulator — a design instrument for surfacing rules gaps and balance findings, not canon. Python; no game content lives here |
| `Oracle/` | The Oracle deck — the shared starter pool players draft from at character creation and draw from at end of session |
| `playtesting/` | Playtest notes, feedback, and session logs |
| `archives/` | Historical design trails — what was discovered, considered, rejected, or consolidated. Not authoritative over current canon; see `archives/README.md`. Cut draft cards live in `experimental/archives/` instead |

## Repository Layers

Drew, 2026-08-12, the target shape for how the repository holds information — 7 layers, each answering a different question:

- **Live Canon** — what is true now. The directories above (`cards/`, `rules/`, `world/`, `bestiary/`, `places/`, `quests/`, `items/`, `mythology/`, `factions/`, `characters/`, Oracle/).
- **Agent tools** (`agent-tools/`) — how to perform recurring work.
- **Memory** (`memory.md`) — compact durable reasoning that still matters.
- **Archives / design trails** (`archives/`) — what was discovered, considered, rejected, or consolidated, or moved.
- **Changelog** (`changelog.md`) — the navigable record of what changed in the repository and why.
- **Git history** — the ultimate byte-level rollback/reference layer.
- **Backlog** (`unresolved-concerns.md`) — a debt index across Live Canon, Memory, and Agent tools, not its own source of truth.

## File Format Conventions

All files are Markdown. Follow existing formatting exactly.

### Cards

Use `agent-tools/card-creation.md` when creating or editing cards.

Canonical card rules remain in `rules/cards.md` and `rules/card-glossary.md`; lineage/tag meaning remains in `world/lineage.md`.


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

## Canon Gate

Determine what kind of change this is.
Check it against current canon.
Integrate ordinary approved work.
Escalate genuine conflicts, ambiguity, propagation failures, or constitutional changes.
Reserve canon-level authority for Drew.
Log every ship in changelog.md — one entry, at the top, the moment it lands.

## Agent Workflow

1. **Orient** — Read `memory.md` and `unresolved-concerns.md` (the scannable index of open debt — flagged issues and deferred decisions; add a line when flagging one, delete it when resolved), then run `agent-tools/repo-orientation.md`. Understand structure before writing. Do not skip this even in a returning session.
2. **Do the work** — read the relevant canon, think it through, write it. Review tools: `red-team.md` (mandatory before canon), `alignment-checker.md` (fit and tone), with the Design Principles in `agent-tools/design-principles.md` and relevant archive exemplars as the standards both measure against. The old generator layer stays archived in `archives/` (see Translation Principle, below, for why).
   - **Building a new bestiary entry's deck:** before drafting cards, scan `bestiary/` for creatures whose cards already portray the same behavior (freeze-and-flee, reposition-and-flee, a particular debuff, etc.). Not a ban on reuse — a behavior can legitimately belong to more than one creature — but check first so a repeat is a deliberate choice, not an accident caught later by `red-team.md`'s Evolution check (mutation vs. duplicate) or missed entirely.
3. **Clarify before executing** — only when something is genuinely ambiguous, not by default. Cover:
   - **Clarifications** — anything ambiguous in the brief that would change the output (session timing, party size, NPC relationship to party, encounter pressure level)
   - **Suggestions** — related content worth connecting, mechanical options Drew may not have considered
   - **Concerns** — conflicts with existing content, scope that feels too large or too small, missing prerequisites
   - Keep it brief. 2–4 items max. Then wait for a response before proceeding.
4. **Run `red-team.md`** on anything going to canon — any card, encounter, or quest content, before presenting.
5. **Output** — Return only finalized content. No drafts unless requested.
6. **Wait** — After completion, await next instruction. Do not assume next task.

Prioritize clarity over cleverness. Prefer system-consistent solutions over novel ones. The repo is a source of truth.

### Canon layer

Tales Untold has three canonical domains:

Rules

How the game works.

Mechanical rules, procedures, formulas, keywords, card rules, character rules, combat rules, and other statements that determine game behavior.

World

What is true about Eclipsera.

Setting facts, mythology, cosmology, history, locations, factions, Seats, Archons, and other truths about the world.

Content

What specifically exists within the game.
People, creatures, places, items, cards, encounters, and other instantiated game content.


## Stat System Quick Reference

This section is an **agent working-memory preload**, not a second source of truth. The detailed rule files remain authoritative when precision or conflict requires checking. Keep the frequently needed baseline here so an agent does not have to re-read basic rules for every task.

| Stat | Color | Perception Mode | Damage Die |
|------|-------|-----------------|------------|
| Mind | Blue | Reason | d6 (utility) |
| Body | Red | Senses | d8 (power) |
| Soul | Green | Read | d4 (precision) |

- HP: (3 × Body) + Soul + Mind (baseline; bosses may go bespoke)
- Combat positions: Frontline / Backline
- Special token types in use: Rooted, Thorns, Evade, Blind, Staggered, Deadly, Weaken, Resist,Vulnerable,ect.

## Do Not

- Invent mechanics in isolation — flag if something is genuinely new
- Create files outside the established directory structure without asking
- Use emoji in files
- Use specific distances in bestiary or quest content — combat is abstract positioning (Frontline/Backline) and "in reach / close / far," never measured distance
