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
**Strength:** N
```

Three formal rules, uniform for every combatant (players included — the trifecta spreads already obey them):

- **HP = (2 × Body) + 9** is the baseline every generator offers. Most creatures take it as-is. **Bosses may go bespoke** — a boss's HP can depart from formula when the fiction calls for it (a threshold-triggered phase, a set-piece number); mark it explicitly (`*(bespoke — boss exception; formula baseline is N)*`) so the departure is never silent.
- **Deck size = total stats**, with each color's count equal to its stat (a 1/2/3 creature runs 1 Blue / 2 Red / 3 Green — signature cards count toward their color).
- **Strength = total stats.** This replaces the Early/Mid/Late tiers as the difficulty scale — precise, comparable, and self-documenting against the player baseline of 9. (Future goal: compute per-card action-economy advantage and fold it into the ranking.)

If target Strength is not specified in a brief, ask before building.

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
- HP: (2 × Body) + 9 (baseline; bosses may go bespoke)
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
- **Release** — full verification: acceptance tests, print sheets regenerated, ledger empty. The combat simulator is a separate instrument Drew consults on his own schedule, not a checklist item, and not something used here to evaluate a change.

Batch small canon edits in Working mode; do not re-run tournaments or regenerate print sheets for every card tweak.

## Four Kinds of Canonical Content

Before asking *who may change this* (the Canon Gate, below), know *what kind of thing it is*:

1. **Rule Definitions** — vocabulary. What something *is*, mechanically and precisely. Keyword texts (`rules/card-glossary.md`), formulas (`rules/core-rules.md`), procedures (`rules/combat.md`).
2. **Invariants** (`rules/invariants.md`) — narrow, and specific to the combat simulator: a mathematical or computational fact that must hold inside the engine regardless of how a human visualizes the same thing at the table (the engine tracks a turn-count per combatant; the wheel is just how a human reads that count). Not a design standard — a computational one.
3. **Design Philosophy** (`agent-tools/design-philosophy.md`) — what makes content well-made: mechanics reflect the fantasy, ecology drives mechanics, a deck is a collection of behaviors, encounters teach through interaction. Violating one doesn't break anything the engine checks — it makes the content weaker.
4. **Exemplars** (`agent-tools/exemplars.md`) — concrete implementations chosen because they demonstrate Design Philosophy well. Extract the principle; don't copy the specifics. A creature can be a strong exemplar and still be nothing like the next one built from the same principles.

They blur because a real piece of content usually touches more than one at once — that's expected. The bug is a *file* absorbing another layer's job rather than staying narrow and pointing outward. This happened twice already, the same way: rule-definition bookkeeping quietly re-derived inside `invariants.md`, and then — even after that fix — design-craft principles ("a deck expresses behavior," "ecology drives mechanics") mislabeled as *invariant* right alongside genuinely computational facts like the turn-count-vs-wheel example, because both had been called by the same name. Both caught, both fixed. See `rules/invariants.md`'s header and `agent-tools/design-philosophy.md`'s header for the corrected, narrower scope of each.

## The Canon Gate — Authority Levels

Placement is a question of jurisdiction, not magnitude: *who is allowed to commit this kind of change?* A level-1 creature can be the best thing in the set; a level-3 wording tweak can be four words.

- **Authority 1 — Established Language** *(agent authority)*. Content that only *uses* existing canon: encounters, creatures, NPCs, cards built from existing mechanics, prose improvements. Ships to canon directories once the mandatory red-team/alignment passes are clean. One line in the post-review queue.
- **Authority 2 — Canonical Extension** *(agent authority, with audit)*. Adds something new without redefining anything: new faction behavior, a regional custom, a new map seat, a deepened NPC. Ships flagged — prominently, in the queue and in chat; Drew's review is veto-after. **An extension may extend canon but may not redirect existing themes** — if it would change what something already established means or is for, it is not an extension; it is constitutional. (Same test as the Translation Principle: *will this change the meaning of something already established?*)
- **Authority 3 — Constitutional** *(Drew's authority, permanently)*. Changes to the language itself: formulas, keywords, progression, cosmology (Seats, Archons, the Unheld, races), core Design Philosophy, anything contradicting existing canon, anything carrying an open world-level hook — anything that changes how other content is interpreted. Goes to `experimental/` or a chat proposal and waits for explicit sign-off.

Every Authority 1/2 ship gets one line under **Recently shipped** at the top of `memory.md`. Drew clears lines by blessing, or objects and the item reverts — every ship is one commit from undone, with the threshold log holding the why. The queue also gives the aggregate view: cumulative drift from many small extensions shows up there as a pattern before it becomes a fact. The gate is loose because the checks are mandatory and the history is reversible — not because review stopped.

## Translation Principle

Drew communicates through examples, metaphors, partial ideas, and observations — the fence, Gambler's Ruin, "two designers at the table." Your job is to translate, not transcribe: identify and formalize the underlying rule or principle when the evidence strongly supports it, rather than asking him to restate it in formal language. ("Invariant" here means specifically what `rules/invariants.md` means it to mean — a computational fact about the simulator. Most of what gets formalized in this section is a rule or a design-philosophy principle, not that.)

- Formalize what is strongly implied. When a recurring pattern is clearly meant but never named, propose the rule or principle yourself.
- Distinguish inferred from stated. Mark anything you derived as *inferred* so he can confirm or correct it; never present it as if he said it outright.
- **A direct statement from Drew already is the ruling — it doesn't need a second, more formal restatement to count.** If he writes out new mechanical text, even offhand or mid-illustration of something else, apply it and note the change (queue line, log entry) rather than treating it as an unconfirmed aside to check back on first. Reserve "flag and ask before applying" for the different case: *your own* inference, paraphrase, or recollection of something Drew hasn't actually re-stated. Getting this backwards adds friction the Canon Gate's reversibility already exists to make unnecessary.
- Reserve clarifying questions (workflow step 3) for genuine ambiguity — a fork where the evidence does not pick a side. A metaphor you can translate is not ambiguity.
- **Never silently redefine something already established.** When Drew's words contradict it, do not reconcile by inventing new semantics: a mechanically coherent interpretation that changes the fantasy is a bug, not a translation. If the contradiction could be a wording slip *of yours*, ask for confirmation; if Drew stated it directly, see the bullet above — apply and flag, don't ask first. The test before any interpretation: *will this require changing the meaning of something already established?* If yes, stop and name it.
- Ambiguity has levels: **(1) harmless** — wording, flavor, implementation detail: resolve silently; **(2) design choice** — pick one and log it in `memory.md`; **(3) constitutional** — formulas, keywords, cosmology, anything Authority 3 in the Canon Gate below: stop and surface. The cost of an unnecessary clarification is lower than the cost of a silently mutated design.

## Do Not

- Invent mechanics in isolation — adapt from existing stat blocks, and flag if something is genuinely new
- Create files outside the established directory structure without asking
- Use emoji in files
