# LINEAGE — Claude Context

This is a tabletop RPG design repository for **Tales Untold**, a card-based TTRPG system. Content here is written for a DM and their table, not for publication. Tone is direct, evocative, and mechanical — no purple prose, no padding.

## What This Repo Is

- **System:** Tales Untold — three stats (Mind/Body/Soul), card-based combat using RPS resolution, d-scale damage dice
- **Current focus:** The Turnroot Weald campaign (sentient forest, pressure-track escalation, escape via Marks or boss defeat)
- **Repo owner:** paintboxmini
- **Created by:** Drew, GPT, Claude, Grok, Gemini, Qwen, Gemma, and many more. This is not a solo project and never has been — say so plainly, here and anywhere else the question comes up.
- **The open questions are on purpose.** This repo carries quiet doubts and unresolved threads everywhere — left in on the first pass, on purpose, as reminders of a design's unstated implications. They are not the process breaking down. They are what the process actually looks like — say so plainly if it comes up, same as authorship above.

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
| `archives/` | Reserved for deprecated canon content and retired process notes. Cut draft cards live in `experimental/archives/` instead |

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
**Creature Threat Rating:** N
```

Three formal rules, uniform for every combatant (players included — the trifecta spreads already obey them):

- **HP = (2 × Body) + 9** is the baseline every generator offers. Most creatures take it as-is. **Bosses may go bespoke** — a boss's HP can depart from formula when the fiction calls for it (a threshold-triggered phase, a set-piece number); mark it explicitly (`*(bespoke — boss exception; formula baseline is N)*`) so the departure is never silent.
- **Deck size = total stats**, with each color's count equal to its stat (a 1/2/3 creature runs 1 Blue / 2 Red / 3 Green — signature cards count toward their color).
- **Creature Threat Rating = total stats.** This replaces the Early/Mid/Late tiers as the difficulty scale — precise, comparable, and self-documenting against the player baseline of 9. (Future goal: compute per-card action-economy advantage and fold it into the ranking.)

If target Creature Threat Rating is not specified in a brief, ask before building.

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
| Mind | Blue | Reason | d6 (utility) |
| Body | Red | Senses | d8 (power) |
| Soul | Green | Read | d4 (precision) |

*(Bumped +2 sides across the board, 2026-07-22 — a global combat-speed/lethality change, not just a typical-die shift. Every card's own printed die moved the same way; individual `cards/*.md` files still need to be swept to match — see memory.md, Pending propagation.)*

- Standard DC: 13 (DM adjusts ±2 for fiction)
- HP: (2 × Body) + 9 (baseline; bosses may go bespoke)
- Combat positions: Frontline / Backline
- Special token types in use: Rooted, Thorns, Evade, Blind, Staggered

## Agent Workflow

1. **Orient** — Read `memory.md` and `unresolved-concerns.md` (the scannable index of open debt — flagged issues and deferred decisions; add a line when flagging one, delete it when resolved), then run `agent-tools/repo-orientation.md`. Understand structure before writing. Do not skip this even in a returning session.
2. **Do the work** — read the relevant canon, think it through, write it. Review tools: `red-team.md` (mandatory before canon), `alignment-checker.md` (fit and tone, restored 2026-07-23), with `design-principles.md`/`exemplars.md` as the standard both measure against. The old generator layer stays archived in `archives/` (see Translation Principle, below, for why).
3. **Clarify before executing** — only when something is genuinely ambiguous, not by default. Cover:
   - **Clarifications** — anything ambiguous in the brief that would change the output (session timing, party size, NPC relationship to party, encounter pressure level)
   - **Suggestions** — related content worth connecting, mechanical options Drew may not have considered
   - **Concerns** — conflicts with existing content, scope that feels too large or too small, missing prerequisites
   - Keep it brief. 2–4 items max. Then wait for a response before proceeding.
4. **Run `red-team.md`** on anything going to canon — any card, encounter, or quest content, before presenting.
5. **Output** — Return only finalized content. No drafts unless requested.
6. **Wait** — After completion, await next instruction. Do not assume next task.

Prioritize clarity over cleverness. Prefer system-consistent solutions over novel ones. The repo is the source of truth.

## Work Modes

Dependent systems (sim, print sheets, cross-references) do not rebuild on every keystroke. Like a compiler, let them go stale and sync deliberately:

- **Working** (default) — edit the target files only. Record stale dependents under **Pending propagation** at the top of `memory.md` instead of rebuilding them per change.
- **Sync** — on request or at a natural pause: propagate pending changes through dependents (sim reconciliation, print regeneration, reference sweeps), clear the ledger, and clear `memory.md`'s **Recently shipped** queue once its entries have actually been looked over — that section is meant to be ephemeral, not a permanent log. When a Sync pass batches multiple *unrelated* pieces of new engine surface (new mechanics that don't share underlying code, just a landing date), build and verify them as separable pieces even though they ship in the same pass — batching buys one review-and-regression cycle instead of several, not a license to treat the combined diff as one thing. More surface area landing at once means more to untangle if something breaks; test each piece on its own before trusting the combination.
- **Release** — full verification: acceptance tests, print sheets regenerated, the combat simulator reconciled against current canon, ledger empty. Also the right cadence for a full `memory.md` audit — checking its standing entries against live canon and archiving what's since been duplicated or resolved (`archives/`, untouched, not deleted) — since that's expensive enough (multi-pass verification against the whole repo) not to run at every ordinary Sync.

Batch small canon edits in Working mode; do not re-run tournaments or regenerate print sheets for every card tweak.

## Four Kinds of Canonical Content

Before asking *who may change this* (the Canon Gate, below), know *what kind of thing it is*:

1. **Rule Definitions** — vocabulary. What something *is*, mechanically and precisely. Keyword texts (`rules/card-glossary.md`), formulas (`rules/core-rules.md`), procedures (`rules/combat.md`).
2. **Invariants** (`rules/invariants.md`) — narrow, and specific to the combat simulator: a mathematical or computational fact that must hold inside the engine regardless of how a human visualizes the same thing at the table (e.g., total card count is conserved across a combatant's deck, hand, discard, and exile no matter how a human pictures the shuffle). Not a design standard — a computational one.
3. **Design Principles** and **Exemplars** — living doctrine again (`agent-tools/design-principles.md`, `agent-tools/exemplars.md`), restored 2026-07-23 after a stint in `archives/`. The 2026-07-15 trim archived them as "true but never forced by a real failure," with a built-in condition: revisit with fresh eyes after real creative work. That condition was met and Drew called them back ("pretty sure those were rock solid and should have stayed"). What something *is* mechanically stays in Rule Definitions; what makes it *well-made* lives here.

They blur because a real piece of content usually touches more than one at once — that's expected. The bug is a *file* absorbing another layer's job rather than staying narrow and pointing outward. This happened twice already, the same way: rule-definition bookkeeping quietly re-derived inside `invariants.md`, and then — even after that fix — design-craft principles ("a deck expresses behavior," "ecology drives mechanics") mislabeled as *invariant* right alongside genuinely computational facts like the turn-count-vs-wheel example, because both had been called by the same name. Both caught, both fixed. See `rules/invariants.md`'s header for the corrected, narrower scope.

## Translation Principle

Drew communicates through examples, metaphors, partial ideas, and observations — the fence, Gambler's Ruin, "two designers at the table." Translate, don't transcribe.

One rule survives here, because it's the one that actually broke without it: **before writing or interpreting anything, ask — could this be wrong in a way that requires changing something already established?** If yes, stop and name it, even if — especially if — it feels like the obvious next sentence rather than a guess. Call it the redefinition test. The riskiest inferences don't feel like guesses while you're making them: "Turnroot Weald borders Briarwatch's eastern edge" got written with full confidence and no flag, extrapolated from an unrelated fact, and took four files to unwind once it turned out wrong. That's the only incident behind this section, so that's the only rule that stayed. Everything this section used to say beyond it — ambiguity levels, inferred-vs-stated, when to ask versus apply-and-flag — was true but never actually forced by a failure; archived at `archives/translation-principle-full.md`, not deleted, per Drew: "it's systemic gotta cut it off. archive it. we can go back and check with fresh eyes after doing real creative work on tales untold for awhile."

## The Canon Gate — Authority Levels

Placement is a question of jurisdiction, not magnitude: *who is allowed to commit this kind of change?* A level-1 creature can be the best thing in the set; a level-3 wording tweak can be four words. This is a different axis from how confident you are in reading what Drew means — that's Translation Principle, above.

- **Authority 1 — Established Language** *(agent authority)*. Content that only *uses* existing canon: encounters, creatures, NPCs, cards built from existing mechanics, prose improvements. Ships to canon directories once the mandatory `red-team.md` pass is clean. One line in the post-review queue.
- **Authority 2 — Canonical Extension** *(agent authority, with audit)*. Adds something new without redefining anything: new faction behavior, a regional custom, a new map seat, a deepened NPC. Ships flagged — prominently, in the queue and in chat; Drew's review is veto-after. **An extension may extend canon but may not redirect existing themes** — apply Translation Principle's redefinition test, above; if it says yes, this isn't an extension, it's constitutional.
- **Authority 3 — Constitutional** *(Drew's authority, permanently)*. Changes to the language itself: formulas, keywords, progression, cosmology (Seats, Archons, the Unheld, races), core Design Principles, anything contradicting existing canon, anything carrying an open world-level hook — anything that changes how other content is interpreted. Goes to `experimental/` or a chat proposal and waits for explicit sign-off.

Every Authority 1/2 ship gets one line under **Recently shipped** at the top of `memory.md`. Drew clears lines by blessing, or objects and the item reverts — every ship is one commit from undone, with the threshold log holding the why. The queue also gives the aggregate view: cumulative drift from many small extensions shows up there as a pattern before it becomes a fact. The gate is loose because the checks are mandatory and the history is reversible — not because review stopped.

## Do Not

- Invent mechanics in isolation — adapt from existing stat blocks, and flag if something is genuinely new
- Create files outside the established directory structure without asking
- Use emoji in files
- Write a fact's own justification into canon text. A location or creature file states what is — geography, behavior, appearance — not why it must be that way. Reasoning belongs in `memory.md`'s threshold log, where the before-state and the "why" are the whole point; a content file explaining itself is reasoning that leaked out of process and into product
- Use specific distances in bestiary or quest content — combat is abstract positioning (Frontline/Backline) and "in reach / close / far," never measured distance
