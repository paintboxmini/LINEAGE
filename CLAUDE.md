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

- **HP = (3 × Body) + Soul + Mind** is the baseline every generator offers *(changed 2026-08-06 from (3 × Body) + 6 — Drew's call; see `memory.md`, Recently Shipped)*. Most creatures take it as-is. **Bosses may go bespoke** — a boss's HP can depart from formula when the fiction calls for it (a threshold-triggered phase, a set-piece number); mark it explicitly (`*(bespoke — boss exception; formula baseline is N)*`) so the departure is never silent.
- **Deck size = total stats**, with each color's count equal to its stat (a 1/2/3 creature runs 1 Blue / 2 Red / 3 Green — signature cards count toward their color). **This can go bespoke too** — a fixed, smaller deck paired with stats that would normally buy a bigger one (Hullback: stats for 13, deck fixed at 6, `bestiary/hullback.md`); mark it the same explicit way HP's exception is marked.
- **Creature Threat Rating = total stats.** This replaces the Early/Mid/Late tiers as the difficulty scale — precise, comparable, and self-documenting against the player baseline of 9. **That baseline scales with party size for encounter design: N players ≈ 9N as the CTR to design a standard encounter against** — confirmed 2026-08-06, 3 players = CTR 27 (`memory.md`, Recently Shipped). Wrackclaw (CTR 4) and Hullback (CTR 13, bespoke deck) are the campaign's floor, its easiest possible fights, not a mid-point — everything else scales up from there. (Future goal: compute per-card action-economy advantage and fold it into the ranking.)

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

*(Bumped +2 sides across the board, 2026-07-22 — a global combat-speed/lethality change, not just a typical-die shift. Every card's own printed die moved the same way. The `cards/*.md` sweep this note used to point to as pending was closed in the 2026-08-01 `memory.md` audit — resolved, not still open.)*

- Standard DC: 13 (DM adjusts ±2 for fiction)
- HP: (3 × Body) + Soul + Mind (baseline; bosses may go bespoke)
- Combat positions: Frontline / Backline
- Special token types in use: Rooted, Thorns, Evade, Blind, Staggered

## Agent Workflow

1. **Orient** — Read `memory.md` and `unresolved-concerns.md` (the scannable index of open debt — flagged issues and deferred decisions; add a line when flagging one, delete it when resolved), then run `agent-tools/repo-orientation.md`. Understand structure before writing. Do not skip this even in a returning session.
2. **Do the work** — read the relevant canon, think it through, write it. Review tools: `red-team.md` (mandatory before canon), `alignment-checker.md` (fit and tone, restored 2026-07-23), with `design-principles.md`/`exemplars.md` as the standard both measure against. The old generator layer stays archived in `archives/` (see Translation Principle, below, for why).
   - **Building a new bestiary entry's deck:** before drafting cards, scan `bestiary/` for creatures whose cards already portray the same behavior (freeze-and-flee, reposition-and-flee, a particular debuff, etc.). Not a ban on reuse — a behavior can legitimately belong to more than one creature — but check first so a repeat is a deliberate choice, not an accident caught later by `red-team.md`'s Evolution check (mutation vs. duplicate) or missed entirely.
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
- **Sync** — on request or at a natural pause: propagate pending changes through dependents (sim reconciliation, print regeneration, reference sweeps), clear the ledger, and clear `memory.md`'s **Recently shipped** queue once its entries have actually been looked over — that section is meant to be ephemeral, not a permanent log. Also scan **Standing Reasoning** for entries that are *closed* — fully absorbed into the canon text they explain, no longer cited as precedent by newer entries, no open follow-up thread depending on them — and move those, verbatim, to `archives/key-design-decisions.md` (the established destination for this, used since 2026-07-19). This is a per-entry judgment on material already in front of you, not a repo-wide check, so it belongs at Sync cadence rather than waiting for Release. When a Sync pass batches multiple *unrelated* pieces of new engine surface (new mechanics that don't share underlying code, just a landing date), build and verify them as separable pieces even though they ship in the same pass — batching buys one review-and-regression cycle instead of several, not a license to treat the combined diff as one thing. More surface area landing at once means more to untangle if something breaks; test each piece on its own before trusting the combination.
- **Release** — full verification: acceptance tests, print sheets regenerated, the combat simulator reconciled against current canon, ledger empty. Also the right cadence for the expensive half of the `memory.md` audit: checking whatever remains in **Active Pending Threads** and **Standing Reasoning** against live canon for drift — has something changed elsewhere in the repo that makes an old entry's claims stale or wrong, not just whether the entry is done being useful (that's Sync's job now). This is genuinely expensive (multi-pass verification against the whole repo) and doesn't belong at ordinary Sync cadence.

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

**A second failure mode, forced by a real night of it (2026-08-09), not by theory: inventing a specific, checkable detail while writing something else, and stating it with the same confidence as a quoted fact.** Not misreading Drew — misreading nothing, because nobody said it; the detail got manufactured mid-sentence to make the sentence work. Oswald's Wound stated "the myth is explicit that this cannot be done" without rechecking the Seat States table it was citing — wrong, a Contested Seat is explicitly winnable. The Pendragon Attempt's headcount was written as six with no number ever given, off by the two companions who died before anyone thought to ask how many there were. A duration, a tone, a fade-rate — same shape every time: a specific fact, invented in the moment, asserted rather than flagged.

**These usually hinge on a single word, not a whole paragraph — which is exactly why they're easy to miss.** Rewriting "Ritual bathing" for the Last Bath / custom split, one word — *"survivable, **repeatable**, not yet examined..."* — got written to keep the new text from clashing with Corren's already-existing repeat-bathing, not because anyone had said bathing could repeat. Nobody had. Drew had to say "once — not a loop" outright before it was caught, and the fix broke Corren's file, which then needed its own repair. One invented word, three follow-on corrections. **The test that actually separates a safe translation from an invented fact: does this word answer a question — how often, how many, why, since when, how long — that Drew hasn't addressed yet?** Tone, register, and imagery are safe to translate generously; that's the actual job (see the Translation Principle's opening line). Frequency, causality, quantity, and mechanism are not safe to fill in, even as a single incidental-seeming adjective buried in otherwise-fine prose. Before writing a word like that, ask whether it's actually established or just convenient — and if it's convenient, either check it against the source file first, or say plainly that it's a build choice, not a fact.

## The Canon Gate — Authority Levels

Placement is a question of jurisdiction, not magnitude: *who is allowed to commit this kind of change?* A level-1 creature can be the best thing in the set; a level-3 wording tweak can be four words. This is a different axis from how confident you are in reading what Drew means — that's Translation Principle, above.

- **Authority 1 — Established Language** *(agent authority)*. Content that only *uses* existing canon: encounters, creatures, NPCs, cards built from existing mechanics, prose improvements. Ships to canon directories once the mandatory `red-team.md` pass is clean. One line in the post-review queue.
- **Authority 2 — Canonical Extension** *(agent authority, with audit)*. Adds something new without redefining anything: new faction behavior, a regional custom, a new map seat, a deepened NPC. Ships flagged — prominently, in the queue and in chat; Drew's review is veto-after. **An extension may extend canon but may not redirect existing themes** — apply Translation Principle's redefinition test, above; if it says yes, this isn't an extension, it's constitutional.
- **Authority 3 — Constitutional** *(Drew's authority, permanently)*. Changes to the language itself: formulas, keywords, progression, cosmology (Seats, Archons, the Unheld, races), core Design Principles, anything contradicting existing canon, anything carrying an open world-level hook — anything that changes how other content is interpreted. Goes to `experimental/` or a chat proposal and waits for explicit sign-off.

**Reviewing `experimental/` before it ships.** Content that arrives there — especially material drafted elsewhere (another AI conversation, a brainstorm dropped in whole) — gets read against current canon, not just against itself, before any Authority 1/2/3 ship. A same-file read catches internal inconsistency; only a read against the rest of the repo catches a closed thread being reopened, an established identity being mutated, or an invented fact duplicating one that already exists. This is what "Canon Gate" means in practice, not just the authority-level bookkeeping above. *(Drew, `experimental/The Unheld`, 2026-08-04: "it's more important than ever that you give anything found in experimental a thorough review." First run on the Aege/Holdfast landing, confirmed again on the Weavers/Waterworks ship — see `memory.md`, Standing Reasoning, for both.)* A 2026-08-06 proposal (`archives/harness-brainstorm-2026-08-06.md`) to skip this full read whenever a cheap pass finds no conflict, defaulting to integrate rather than evaluate, was tested against that same week's actual ships rather than judged in the abstract — two of the five files in flight at the time each carried a real, non-syntactic contradiction with established canon that only the full read caught. Rejected on that evidence. Full review stays mandatory; don't re-propose the shortcut without accounting for those two counterexamples.

Every Authority 1/2 ship gets one line under **Recently shipped** at the top of `memory.md`. Drew clears lines by blessing, or objects and the item reverts — every ship is one commit from undone, with the threshold log holding the why. The queue also gives the aggregate view: cumulative drift from many small extensions shows up there as a pattern before it becomes a fact. The gate is loose because the checks are mandatory and the history is reversible — not because review stopped.

**Write-up length follows decision difficulty, not ship count.** A deterministic fix — a duration bug, a renamed term propagated across files, a typo — gets its one line in Recently shipped and stops there. `memory.md`'s **Standing Reasoning** section is reserved for ships that actually required reconciling a conflict or making a judgment call the repo didn't already answer, not for restating a Recently-shipped paragraph a second time at greater length. Writing the same reasoning twice, once compressed and once expanded, is duplication, not diligence.

## Do Not

- Invent mechanics in isolation — adapt from existing stat blocks, and flag if something is genuinely new
- Create files outside the established directory structure without asking
- Use emoji in files
- Write a fact's own justification into canon text. A location or creature file states what is — geography, behavior, appearance — not why it must be that way. Reasoning belongs in `memory.md`'s threshold log, where the before-state and the "why" are the whole point; a content file explaining itself is reasoning that leaked out of process and into product
- Use specific distances in bestiary or quest content — combat is abstract positioning (Frontline/Backline) and "in reach / close / far," never measured distance
