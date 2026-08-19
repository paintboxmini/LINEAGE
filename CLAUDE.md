# LINEAGE — Claude Context

This is a tabletop RPG design repository for **Tales Untold**, a card-based TTRPG system. Content here is written for a DM and their table, not for publication. Tone is direct, evocative, and mechanical — no purple prose, no padding.

## What This Repo Is

### Repository Branches

- `Main` — Stable Reference point.
- `claude/general-chat-vwvr1` — Claude's working branch.
- `character-design-inspection` — GPT's current working branch. (Was `gpt/from-claude-structure`; that branch no longer exists on the remote.)

- **System:** Tales Untold — three stats (Mind/Body/Soul), card-based combat using RPS resolution, d-scale damage dice
- **Current focus:** The Turnroot Weald campaign (sentient forest, pressure-track escalation, escape via Marks or boss defeat)
- **Repo owner:** paintboxmini
- **Created by:** Drew, GPT, Claude, Grok, Gemini, Qwen, Gemma, and many more.
- **The open questions are on purpose.** This repo carries unresolved threads everywhere — left in on the first pass, on purpose, to give the world time to settle. The repo is also full of quiet doubts, they show the process that created them breaking down. This is from user inexperience and stubborness. — say so plainly if it comes up, same as authorship above.

## Directory Structure

| Directory | Contents |
|-----------|----------|
| `cards/` | **One file per card**, flat — the filename is the card's slug, and card art lives in the card's own file. Membership lives in `cards/buckets/` (behaviour buckets plus the `red`/`blue`/`green`/`colorless` colour sets) and `cards/archetypes/`; neither holds card text |
| `rules/` | Core rules and mechanics; `rules/README.md` records **which file owns which topic**. **One file per keyword** in `rules/keywords/`, one per status card in `rules/status-cards/`; `rules/card-glossary.md` is **generated** from those plus `rules/glossary-frame.md` — edit the sources, never the built file |
| `places/` | Place overviews (world-level descriptions) |
| `quests/` | Full adventure systems — pressure tracks, NPCs, encounter frameworks |
| `bestiary/` | **One folder per creature.** `mechanics.md` holds the stat block, deck, passives, abilities and loot together; `profile.md` holds appearance and behaviour; other sections get their own file; `README.md` is the front door |
| `characters/` | **One folder per character**, same shape as `bestiary/` — `mechanics.md`, `profile.md`, `README.md`, plus any other sections |
| `items/` | Consumables and equipment |
| `world/` | Geography, factions, organizations, lore and creation myths, cosmology (Seats, Archons, Resonance) |
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

- **Live Canon** — what is true now. The directories above (`cards/`, `rules/`, `world/`, `bestiary/`, `places/`, `quests/`, `items/`, `factions/`, `characters/`, Oracle/).
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

### Bestiary and Character Entries

One folder per entry. `README.md` carries the title, subtitle, a Contents list and Related Documents. `mechanics.md` carries the stat block, Creature Threat Rating, Deck line, passives, abilities, loot and combat identity — the stat block and deck stay in the same file because deck size equals total stats and per-colour counts equal the individual stats, so they are one invariant. `profile.md` carries appearance and behaviour. Anything else gets its own file.

**A section earns its own file when it is substantial enough to read alone, or common enough across entries that the filename is predictable.** One-off *and* small fails both — that is a heading, not a file. Corrected 2026-08-17 after the first split produced 19 one-off sections under 300 characters, including a 143-character one.

**All mechanical content goes in `mechanics.md`, including per-variant stat blocks.** A multi-variant creature (Ashgrazer's Alpha and Pack) keeps every variant's block there rather than in per-variant section files. Where variants each carry a full stat block, deck and passives of their own, they are separate creatures and earn separate entries instead — Briarwatch's four Briarbundles were promoted that way on 2026-08-18, leaving `bestiary/briarbundles/` holding the folklore they share. Splitting them out once left three `mechanics.md` files holding no mechanics at all, and silently dropped 6 of 37 decks from `verify.py`'s validation while every check still reported PASS.

`mechanics.md` opens with a `Cards:` line naming the specific card files, if signature cards exist:
```
**Cards:** `cards/out-of-reach.md`, `cards/slow-hands.md`
```

### Cross-References

Use relative paths in backticks: `` `quests/turnroot-weald-adventure.md` ``

## Commit Conventions

- Commit messages: short imperative sentence, no period, no emoji
- Commit in logical groups (one concern per commit)
- Always push with `-u origin <branch>`

## Translation Principle

Scope: lore and canon, rules text, card wording, session drafts, and the agent harness itself — anywhere Drew's compressed input becomes written content.

- **Translate compressed input into explicit form when the evidence supports it.** Tone, register, imagery, examples, metaphors, and partial ideas can be expanded when the underlying meaning is strongly supported.
- **Distinguish direct rulings from agent inference.** Drew's explicit statements are rulings. Your own conclusions are inferences; do not present them as if Drew stated them.
- **Never silently redefine established meaning.** If an interpretation would change something already established, stop and surface the conflict rather than reconciling it invisibly.
- **Surface genuine design forks instead of choosing invisibly.** If multiple plausible interpretations would materially change the design, expose the fork and let Drew decide.
- **Leave genuinely unspecified details unspecified.** Do not manufacture missing facts merely to make prose or a design feel complete.
- **Do not invent specific facts to make prose complete.** Do not fill in unprovided numbers, durations, frequencies, causes, motives, headcounts, or mechanisms as incidental details.
- **Do not sand over unresolved conflicts with fluent prose.** If the underlying conflict has no actual resolution, don't hide it behind language that merely sounds resolved.
- **Flag apparent conflicts when Drew's own new statement may contradict established material.** Name the established fact and the apparent conflict; let Drew decide rather than silently privileging either one.

Full reasoning trail and incident history: `archives/consolidated/translation-principle.md` and `archives/translation-principle-full.md`. This section is the operational form only.

## Canon Gate

Talk it through first (Agent Workflow, step 3) — once we're both on the same page, it's safe to write. (2026-08-12, Drew: the old Authority 1/2/3 tiers were excessive.)
Check it against current canon before writing.
Escalate genuine conflicts, ambiguity, or propagation failures rather than resolving them silently.
Log every ship in changelog.md — one entry, at the top, the moment it lands.

## Agent Workflow

1. **Orient** — Read `memory.md` and `unresolved-concerns.md` (the scannable index of open debt — flagged issues and deferred decisions; add a line when flagging one, delete it when resolved), then run `agent-tools/repo-orientation.md`. Understand structure before writing. Do not skip this even in a returning session.
2. **Do the work** — read the relevant canon, think it through, write it. Review tools: `red-team.md` (mandatory before canon), `alignment-checker.md` (fit and tone), with the Design Principles in `agent-tools/design-principles.md` and relevant archive exemplars as the standards both measure against. The old generator layer stays archived in `archives/`.
   - **Building a new bestiary entry's deck:** before drafting cards, scan `bestiary/` for creatures whose cards already portray the same behavior (freeze-and-flee, reposition-and-flee, a particular debuff, etc.). Not a ban on reuse — a behavior can legitimately belong to more than one creature — but check first so a repeat is a deliberate choice, not an accident caught later by `red-team.md`'s Evolution check (mutation vs. duplicate) or missed entirely.
   - **Staleness check, roughly every 5 substantial canon changes:** a session doing rapid iterative worldbuilding — retcons, portfolio splits, renames — accumulates stale cross-references and leftover facts fast, cheaper to catch in batches than to let it compound. Run a consistency sweep (a background `Explore`-type Agent works well for this) checking recent changes against the rest of the repo. Track the count across the session; don't wait for it to be requested. (2026-08-15, Drew.)
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
- Special token types in use: Rooted, Thorns, Evade, Blind, Staggered, Deadly, Weaken, Resist, Vulnerable, Protect, and Immunity.

## Do Not

- Invent mechanics in isolation — flag if something is genuinely new
- Create files outside the established directory structure without asking
- Use emoji in files
- Use specific distances in bestiary or quest content — combat is abstract positioning (Frontline/Backline) and "in reach / close / far," never measured distance
