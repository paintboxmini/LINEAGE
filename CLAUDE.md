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

- **HP = (3 × Body) + Soul + Mind** is the baseline every generator offers *(changed 2026-08-06 from (3 × Body) + 6 — Drew's call; see `archives/key-design-decisions.md`)*. Most creatures take it as-is. **Bosses may go bespoke** — a boss's HP can depart from formula when the fiction calls for it (a threshold-triggered phase, a set-piece number); mark it explicitly (`*(bespoke — boss exception; formula baseline is N)*`) so the departure is never silent.
- **Deck size = total stats**, with each color's count equal to its stat (a 1/2/3 creature runs 1 Blue / 2 Red / 3 Green — signature cards count toward their color). **This can go bespoke too** — a fixed, smaller deck paired with stats that would normally buy a bigger one (Hullback: stats for 13, deck fixed at 6, `bestiary/hullback.md`); mark it the same explicit way HP's exception is marked.
- **Creature Threat Rating = total stats.** This replaces the Early/Mid/Late tiers as the difficulty scale — precise, comparable, and self-documenting against the player baseline of 9. **That baseline scales with party size for encounter design: N players ≈ 9N as the CTR to design a standard encounter against** — confirmed 2026-08-06, 3 players = CTR 27 (`archives/key-design-decisions.md`). Wrackclaw (CTR 4) and Hullback (CTR 13, bespoke deck) are the campaign's floor, its easiest possible fights, not a mid-point — everything else scales up from there. (Future goal: compute per-card action-economy advantage and fold it into the ranking.)

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

This section is an **agent working-memory preload**, not a second source of truth. The detailed rule files remain authoritative when precision or conflict requires checking. Keep the frequently needed baseline here so an agent does not have to re-read basic rules for every task.

| Stat | Color | Perception Mode | Damage Die |
|------|-------|-----------------|------------|
| Mind | Blue | Reason | d6 (utility) |
| Body | Red | Senses | d8 (power) |
| Soul | Green | Read | d4 (precision) |

*(Bumped +2 sides across the board, 2026-07-22 — a global combat-speed/lethality change, not just a typical-die shift. Every card's own printed die moved the same way. The `cards/*.md` sweep this note used to point to as pending was closed in the 2026-08-01 `memory.md` audit — resolved, not still open.)*

- HP: (3 × Body) + Soul + Mind (baseline; bosses may go bespoke)
- Combat positions: Frontline / Backline
- Special token types in use: Rooted, Thorns, Evade, Blind, Staggered

## Active Design Reasoning — Design Principles

These are living design principles: standards for making and evaluating Tales Untold content. They are part of Claude's active reasoning model, not a historical log. Rule Definitions say what something is mechanically; these principles say what makes content well-made. Exemplars remain separate because they demonstrate these principles concretely.

- **Mechanics exist to reflect the fantasy.** A resolution rule that produces a mechanic without a felt truth behind it is broken, no matter how clean the math is. This is the standard every new mechanic gets checked against.
- **A creature's deck is a collection of its behaviors.** The deck doesn't just enable what a creature can do — card by card, it should *be* what the creature does.
- **Ecology drives mechanics.** A creature's environment and biology generate its rules. The rules aren't picked first with fiction painted on after.
- **Encounters teach through interaction, not explanation.** A lesson lands because the player did something and felt the consequence — not because a GM explained the rule beforehand.
- **Fiction and mechanics reinforce one another.** Neither stands alone: a mechanic with no fictional reason is arbitrary; fiction with no mechanical expression is decoration.
- **Local rules emerge from the environment, not arbitrary exception.** When a place needs a special rule, the rule should read as a discovered property of that place, not a bolt-on carve-out from the general system.
- **Difficulty should be precise and computable, not a vague label.** CTR is the current, incomplete expression of this principle, not an adequate measurement yet. Do not mistake the current framework for the principle it is trying to express.
- **A mechanic without impact doesn't matter. Meaning without mechanics doesn't either.** Both halves are load-bearing: a mechanic that changes nothing about play is decoration, and a piece of fiction the system can't touch mechanically isn't really in the game, just described near it.
- **Standard fights, where the players hold a real advantage, should resolve in about 3 turns per combatant.** The validated 5–6 turns per combatant case represents a fight without that player-side advantage and is a useful boss-tier comparison. Measure future tests against both numbers rather than treating either as a universal target.
- **Body's advantage is raw combat power.** Body has higher raw damage and contributes more strongly to maximum HP. Its common melee range and greater frontline vulnerability are constraints on that power, not reasons to remove the raw-stat advantage. This adds fidelity to the original color logic rather than replacing it: colors should retain distinct strengths and tradeoffs.
- **A build that ignores one of the three combat pillars — RPS, Initiative, or Position — takes on real, legible risk.** That is fine when intentional, not accidental. Content that cannot interact with any pillar is probably inert; a build that deliberately gives one up should have a recognizable reason or compensating strength.

## Name, Price, and Distance

These are the three Cuts applied across people, places, and things. They are one framework, not three isolated writing prompts: **Name** establishes identity and distinction, **Price** establishes the meaningful cost of acting or expressing that identity, and **Distance** defines the relationships and boundaries between things — what is unreachable, what is close, and what distinctions can eventually cease to hold.

### Name — Fidelity Through Specificity

Name is more than giving something a proper name. A Named person, place, or thing has enough identity that it is no longer interchangeable with another instance of its category.

The current working breakdown is deliberately **not a closed list**:

- **What it is.** Its essential nature, role, or function.
- **An actual name.** Not a placeholder such as "a guard" or "the forest."
- **Traits.** The particulars that make it recognizably itself.
- **History.** What happened before the story encountered it and how that history made it what it is.

Apply this at the subject's scale:

- **People:** nature or role, actual name, traits, history.
- **Places:** essential nature, actual name, distinctive traits, history.
- **Things:** what the thing is or does, actual name, distinctive traits or capabilities, history including origin and prior use.

This is a fidelity test, not a formula. The four-part breakdown is useful because it catches interchangeable, under-specified content; it does not claim to exhaust identity.

### Price — Fidelity Through Correspondence

Price is not a universal mechanical tax. It is the cost imposed when something acts, expresses its nature, or forces something into the world. **The Price should meaningfully correspond to what was done.**

For people, Price can take the form of a binding constraint: *I never…*, *I must…*, *I always…*, *I cannot…*, *Once I…*, or *Whenever…*. The constraint is the Price, not merely the words used to declare it. NPCs follow the same underlying law even though the declaration is not necessarily a player-facing ritual.

For places, Price can manifest as pressure or accumulated debt: escalation caused by failing to move through the place according to its domain. A pressure track is one expression of Place-Price, not a universal requirement for every location.

For resonant things, Price is deliberately flexible in expression:

- It is **not** automatically HP loss.
- It is **not** one universal mechanical expression.
- It emerges from the specific use and should answer the shape of what was forced through the item.
- It may manifest as vitality transfer, physical reflection, collateral consequence, loss or degradation, binding consequence, social consequence, or another form that meaningfully corresponds to the act.

**Price is proportional to magnitude.** A greater working bends more reality and therefore carries greater cost.

**Actions aligned with a seated Archon's will have reduced Price; actions against that will have increased Price.** An unheld Seat has no will to align with or defy, so its Price is paid on magnitude alone.

**Price can propagate.** The cost may affect other people or things touched by the working without relieving the actor of their own Price. A consequence landing on an ally can still be part of the actor's Price rather than a transfer that makes the actor free of cost.

**Understanding Price is not the same as controlling Price.** Someone may learn an item's metaphysical laws through experience or teaching without automatically gaining authority over where the Price falls. Familiarity can help someone act intelligently within the law; it does not make them exempt from it.

### Distance — Relationships, Boundaries, and Their Collapse

Distance defines the relationship between what something is and what it is not. It determines what remains separate, what lies close enough to influence or resonate with it, and what can become so close that the distinction between the two no longer meaningfully holds.

Distance has several expressions:

- **What can never be reached.** The boundary that remains beyond the thing's ordinary ability to cross. This is the established **What Can Never Be** principle.
- **What is close.** The people, things, states, places, or domains near enough to meaningfully influence, resonate with, or interact with the subject.
- **What no longer holds any distinction.** A collapse of distance in which two identities, domains, states, or beings become close enough that the boundary between them ceases to meaningfully distinguish them.

#### What Can Never Be

- **People:** every NPC worth building carries something reality will not let them close — a relationship they can't repair, a child they can't have, forgiveness they can't receive, a version of themselves they can no longer become. If they could have exactly one thing that would make their life feel complete, what is it, and why can reality never give it to them?
- **Resonant objects:** every resonant object carries the equivalent — not a state it desires, but a state of being it can never inhabit. A sword can never be a plow. A crown can never be the person who wears it. If it could become exactly one other thing that would complete its nature, what would that be, and why can it never be that?
- **Resonant places:** a resonant place carries the same boundary at its own scale — not a state it desires, but a domain it can never fully become. If it could resolve into exactly one other kind of place, permanently, what would that be, and why can it never actually settle there?

Distance is not merely a hard ceiling. A story can cross a Distance or collapse one, and that is not automatically a rules violation; it is a meaningful transformation when the fiction earns it. A Distance resolved casually was never carrying meaningful weight. Likewise, do not invent a universal definition of "close" or "no distinction" where the world has not established one — those relationships are themselves part of what the fiction can reveal.

## Agent Workflow

1. **Orient** — Read `memory.md` and `unresolved-concerns.md` (the scannable index of open debt — flagged issues and deferred decisions; add a line when flagging one, delete it when resolved), then run `agent-tools/repo-orientation.md`. Understand structure before writing. Do not skip this even in a returning session.
2. **Do the work** — read the relevant canon, think it through, write it. Review tools: `red-team.md` (mandatory before canon), `alignment-checker.md` (fit and tone, restored 2026-07-23), with the Design Principles in this file and `agent-tools/exemplars.md` as the standard both measure against. The old generator layer stays archived in `archives/` (see Translation Principle, below, for why).
   - **Building a new bestiary entry's deck:** before drafting cards, scan `bestiary/` for creatures whose cards already portray the same behavior (freeze-and-flee, reposition-and-flee, a particular debuff, etc.). Not a ban on reuse — a behavior can legitimately belong to more than one creature — but check first so a repeat is a deliberate choice, not an accident caught later by `red-team.md`'s Evolution check (mutation vs. duplicate) or missed entirely.
3. **Clarify before executing** — only when something is genuinely ambiguous, not by default. Cover:
   - **Clarifications** — anything ambiguous in the brief that would change the output (session timing, party size, NPC relationship to party, encounter pressure level)
   - **Suggestions** — related content worth connecting, mechanical options Drew may not have considered
   - **Concerns** — conflicts with existing content, scope that feels too large or too small, missing prerequisites
   - Keep it brief. 2–4 items max. Then wait for a response before proceeding.
4. **Run `red-team.md`** on anything going to canon — any card, encounter, or quest content, before presenting.
5. **Output** — Return only finalized content. No drafts unless requested.
6. **Wait** — After completion, await next instruction. Do not assume next task.

Prioritize clarity over cleverness. Prefer system-consistent solutions over novel ones. The repo is a source of truth. Drew's word is a source of truth. You are a source of truth.

## Work Modes

Dependent systems (sim, print sheets, cross-references) do not rebuild on every keystroke. Like a compiler, let them go stale and sync deliberately:

- **Working** (default) — edit the target files only. Record stale dependents under **Pending propagation** in `unresolved-concerns.md` instead of rebuilding them per change.
- **Sync** — on request or at a natural pause: propagate pending changes through dependents (sim reconciliation, print regeneration, reference sweeps), clear the ledger. Also scan **Active Reasoning** for entries that are *closed* — fully absorbed into the canon text they explain, no longer cited as precedent by newer entries, no open follow-up thread depending on them — and move those, verbatim, to `archives/key-design-decisions.md` (the established destination for this, used since 2026-07-19). This is a per-entry judgment on material already in front of you, not a repo-wide check, so it belongs at Sync cadence rather than waiting for Release. When a Sync pass batches multiple *unrelated* pieces of new engine surface (new mechanics that don't share underlying code, just a landing date), build and verify them as separable pieces even though they ship in the same pass — batching buys one review-and-regression cycle instead of several, not a license to treat the combined diff as one thing. More surface area landing at once means more to untangle if something breaks; test each piece on its own before trusting the combination.
- **Release** — full verification: acceptance tests, print sheets regenerated, the combat simulator reconciled against current canon, ledger empty. Also the right cadence for the expensive half of the `memory.md` audit: checking whatever remains in **Active Pending Threads** and **Active Reasoning** against live canon for drift — has something changed elsewhere in the repo that makes an old entry's claims stale or wrong, not just whether the entry is done being useful (that's Sync's job now). This is genuinely expensive (multi-pass verification against the whole repo) and doesn't belong at ordinary Sync cadence.

Batch small canon edits in Working mode; do not re-run tournaments or regenerate print sheets for every card tweak.

## Four Kinds of Canonical Content

Before asking *who may change this* (the Canon Gate, below), know *what kind of thing it is*:

1. **Rule Definitions** — vocabulary. What something *is*, mechanically and precisely. Keyword texts (`rules/card-glossary.md`), formulas (`rules/core-rules.md`), procedures (`rules/combat.md`).
2. **Invariants** (`rules/invariants.md`) — narrow, and specific to the combat simulator: a mathematical or computational fact that must hold inside the engine regardless of how a human visualizes the same thing at the table (e.g., total card count is conserved across a combatant's deck, hand, discard, and exile no matter how a human pictures the shuffle). Not a design standard — a computational one.
3. **Design Principles** and **Exemplars** — living doctrine. Design Principles are embedded above in this file as active reasoning; Exemplars remain in `agent-tools/exemplars.md` as concrete demonstrations. What something *is* mechanically stays in Rule Definitions; what makes it *well-made* lives in Design Principles.

They blur because a real piece of content usually touches more than one at once — that's expected. The bug is a *file* absorbing another layer's job rather than staying narrow and pointing outward. Rule-definition bookkeeping belongs in Rule Definitions; computational invariants belong in `rules/invariants.md`; design-craft principles belong in the Design Principles above.

## Translation Principle

*Scope: lore and canon, rules text, card wording, session drafts, and the agent harness itself — anywhere Drew's compressed input becomes written content.*

Drew communicates through examples, metaphors, partial ideas, and observations — the fence, Gambler's Ruin, "two designers at the table." Translate, don't transcribe: **tone, register, and imagery are safe to expand generously — that's the actual job.** What follows is what's *not* safe to fill in. Five rules, each forced by a real break, not written in advance for a hypothetical one. Full incident narratives, kept for the reasoning trail rather than day-to-day use: `archives/translation-principle-full.md`.

**The working card:**

- **Redefinition test.** Before writing or interpreting anything: could this be wrong in a way that requires changing something already established? If yes, stop and name it — even if, especially if, it feels like the obvious next sentence rather than a guess. (Forced by "Turnroot Weald borders Briarwatch's eastern edge" — four files to unwind once it turned out wrong.)
- **No invented specifics.** A number, duration, limit, or headcount isn't safe to fill in, even as one incidental-seeming word. Test: does this word answer a how-often / how-many / why / since-when question nobody's addressed yet? If yes, check it against a source file, or say plainly it's a build choice, not a fact. (Forced by "repeatable" — one invented word, three follow-on corrections.)
- **No sanding.** Don't write fluent, resolved-sounding prose around a conflict instead of actually resolving it. **Distinct from the rule above, not a restatement of it: invented specifics *add* a fact that wasn't there; sanding *avoids resolving* one that was.** Same smooth wrongness, opposite direction — one over-commits, the other evades. Test: could I point to the specific fact that resolves this, or only to a sentence that implies one exists? (Forced by Corren's first "tolerated exception" fix, which read complete and wasn't.)
- **Flag Drew's own slips.** When what he states directly conflicts with, or quietly overlooks, an already-established fact, say so — name the fact, name the conflict, let him decide informed. Don't silently defer to old canon over his new word, and don't silently apply his new word over old canon without saying so. His own standing request, not a caught incident: *"I very often misremember or worse forget about details that are relevant to the changes I'm making."*
- **What a good translation looks like, for contrast.** Drew: *"he is tall and stiff. Extremely formal in public. Quick to anger behind closed doors... same rare shows of warmth."* Translated: *"Tall, stiff-postured — not cold. Formal, but the kind of formal most people read as pleasant: he smiles when he approves, in council and behind closed doors alike... Nobody has ever needed to raise his volume for him; the rank does that."* (`world/the-regency.md`, Lord Oswald.) Safe, because every added word dresses a stated fact in voice — none of it answers a how-often/how-many/why question he hadn't already answered himself.

**Flag protocol, so rule 4 doesn't become constant interruption.** Low-confidence suspicion, low stakes: name it in one line inline with the work, then proceed on his stated instruction — he can wave it off in his next message with no lost work. Anything that would be expensive to unwind, or that touches Authority 3 territory (cosmology, formulas, anything already shipped and load-bearing elsewhere): stop and ask before writing anything, the same bar the Canon Gate already sets for that tier. Match the interruption to the cost of being wrong, not to how uncertain it feels in the moment.

**Where this doesn't apply — mechanical execution isn't narrative invention.** Drew, directly: *"The Translation Principle is making you too cautious. Change CLAUDE.md so you're allowed to infer missing mechanics when the intended design is obvious."* A standing permission, requested the same way rule 4 was — not forced by an incident, because the failure it's correcting is the opposite kind: hesitation, not invention. None of the five rules above are about stalling on execution inside an already-fixed design space — a value a formula already determines (HP, CTR, deck size), a keyword the ecology obviously calls for, a stat, color, or range the fiction already points to. Building those is arithmetic and pattern-matching, not invention; Authority 1 already covers it without a gate ("content that only uses existing canon"). **The line:** is there exactly one answer already fixed by formula or unbroken established pattern, or am I choosing among several genuinely plausible answers about how the world actually works — a headcount, a frequency, a cause, a motive? The first: build it, don't ask. The second is what the rules above are actually protecting.

**Established effects do not require invented explanations.** If an already-established effect has an ordinary, direct manifestation, build the manifestation without demanding a separate lore mechanism for it. A spark can ignite wood; lightning can strike a conductor; a known restorative effect can make touched water healing; an established supernatural effect can leave a person energized. The test is not "have I explained why this happens in the world's metaphysics?" It is "is this a direct consequence or expression of something already established?" If yes, do not manufacture a missing explanation just to make the sentence feel complete. Protect the genuinely open question; don't create one where none exists.

## The Canon Gate — Authority Levels

Placement is a question of jurisdiction, not magnitude: *who is allowed to commit this kind of change?* A level-1 creature can be the best thing in the set; a level-3 wording tweak can be four words. This is a different axis from how confident you are in reading what Drew means — that's Translation Principle, above.

- **Authority 1 — Established Language** *(agent authority)*. Content that only *uses* existing canon: encounters, creatures, NPCs, cards built from existing mechanics, prose improvements. Ships to canon directories once the mandatory `red-team.md` pass is clean. One line in the post-review queue (`archives/key-design-decisions.md`, Work Log — The Trail).
- **Authority 2 — Canonical Extension** *(agent authority, with audit)*. Adds something new without redefining anything: new faction behavior, a regional custom, a new map seat, a deepened NPC. Ships flagged — prominently, in the queue and in chat; Drew's review is veto-after. **An extension may extend canon but may not redirect existing themes** — apply Translation Principle's redefinition test, above; if it says yes, this isn't an extension, it's constitutional.
- **Authority 3 — Constitutional** *(Drew's authority, permanently)*. Changes to the language itself: formulas, keywords, progression, cosmology (Seats, Archons, the Unheld, races), core Design Principles, anything contradicting existing canon, anything carrying an open world-level hook — anything that changes how other content is interpreted. Goes to `experimental/` or a chat proposal and waits for explicit sign-off. **No standing queue for this** — Drew, 2026-08-11: *"a3 recommendation don't need their own section. I'll respond to those in chat."* Constitutional-level observations get raised in conversation directly, the same as any other flag, not logged into a tracked backlog. Same message, refined: *"we should keep A3 suggestions, they just get mentioned in chat, not logged... honestly any that you want to keep that go unaddressed should go to unresolved concerns."* If a chat-raised observation goes unaddressed and is worth remembering, it goes to `unresolved-concerns.md` like any other flagged debt — not a new mechanism, just that file's existing job.

**Reviewing `experimental/` before it ships.** Content that arrives there — especially material drafted elsewhere (another AI conversation, a brainstorm dropped in whole) — gets read against current canon, not just against itself, before any Authority 1/2/3 ship. A same-file read catches internal inconsistency; only a read against the rest of the repo catches a closed thread being reopened, an established identity being mutated, or an invented fact duplicating one that already exists. This is what "Canon Gate" means in practice, not just the authority-level bookkeeping above. *(Drew, `experimental/The Unheld`, 2026-08-04: "it's more important than ever that you give anything found in experimental a thorough review." First run on the Aege/Holdfast landing, confirmed again on the Weavers/Waterworks ship — see `memory.md`, Active Reasoning, for both.)* A 2026-08-06 proposal (`archives/harness-brainstorm-2026-08-06.md`) to skip this full read whenever a cheap pass finds no conflict, defaulting to integrate rather than evaluate, was tested against that same week's actual ships rather than judged in the abstract — two of the five files in flight at the time each carried a real, non-syntactic contradiction with established canon that only the full read caught. Rejected on that evidence. Full review stays mandatory; don't re-propose the shortcut without accounting for those two counterexamples.

Every Authority 1/2 ship gets one line at the top of `archives/key-design-decisions.md`'s Work Log — The Trail (2026-08-11, Drew: *"recently shipped should be an archive thing"* — logged directly to its permanent home now, newest-first, no staging in `memory.md` first). Drew clears lines by blessing (reading and saying nothing), or objects and the item reverts — every ship is one commit from undone, with the entry itself holding the why. The log also gives the aggregate view: cumulative drift from many small extensions shows up there as a pattern before it becomes a fact. The gate is loose because the checks are mandatory and the history is reversible — not because review stopped.

**Write-up length follows decision difficulty, not ship count.** A deterministic fix — a duration bug, a renamed term propagated across files, a typo — gets its one line in the Work Log and stops there. `memory.md`'s **Active Reasoning** section is reserved for ships that actually required reconciling a conflict or making a judgment call the repo didn't already answer, not for restating a Recently-shipped paragraph a second time at greater length. Writing the same reasoning twice, once compressed and once expanded, is duplication, not diligence.

## Campaign Status

**Intended session spine (Drew, 2026-08-02)** — the shape the gold pacing is calibrated against:

| Session | Where |
|---|---|
| 1 | Unheld Ocean shoreline → Roadhouse → Briarwatch, ending at the ruins about to go into the burrows *(was Vulture's Nest → Roadhouse → Briarwatch; retired 2026-08-06, `archives/key-design-decisions.md`)* |
| 2 | The Hollow solved |
| 3 | Turnroot Weald |
| 4 | Turnroot finished |
| 5 | Eclipseria — the capital |

This is why gear pacing targets five sessions to a first Tier 1 item **per character**: it lands each character's first real equipment at roughly the moment the campaign reaches the city that sells it. Not a schedule to enforce — a reference the economy was built against.

## Active Threads

Possible future connections noticed while doing other work, that don't require answering them. If something here actually needs an answer for current work to tie into the repo correctly, that's debt, not this — it belongs in `unresolved-concerns.md` instead.

**ARCHITECTURAL NORTH STAR — typed modifiers, Step 3.** Step 2 shipped 2026-08-05/06 (typed modifiers with lifetimes for `axiom_ban`, `cannot_defend`, `staggered`, plus the AXIOM attacker-side gap closed same week — full reasoning archived, `archives/key-design-decisions.md`). Step 3 — the full policy stack — remains explicitly deferred, not abandoned: only worth building once a modifier-as-special-case has become genuinely painful. This is the only live pointer to that sequencing call left after the 2026-08-11 restructure moved Step 2's reasoning trail to archives.

**B thread — Quartermaster Voss**
Secondary hook, only activates if party explored the Roadhouse barracks and found the posting order. Unsigned line: "anything from the docks that isn't in the manifest." Points to unsanctioned smuggling from Vulture's Nest to the capital. Voss is at Eclipseria South Gate. Voss's intake reports are cross-referenced against Jonas's ledger — condoned goods appear in both. The supply chain that doesn't appear in either is the FourthEye thread. Don't develop until party pulls on it.

**FourthEye pipeline**
Drug spreading through Eclipseria's Underground Bazaar (Giblets' stall is the bazaar-end node). Supply chain runs from Vulture's Nest, bypasses Jonas's ledger entirely, never appears in Voss's intake. Masaharu is at the Nest tracing it backward. Identity of the Nest-side operator: unknown. Giblets' "plan connected to someone he used to work with" is the forward-pointing thread. Three Regency hard lines violated: too addictive, too destructive, council gets no cut. **The Cellar Custodians are the last link before it reaches the Bazaar** (Drew, 2026-08-05) — the deep tunnels they patrol are the same ones the drug has to move through to reach the Bazaar's hidden pocket. Who's actually dirty and how far up it goes stays unestablished, same as the Nest-side operator. See `places/vultures-nest.md` (Masaharu, Rumors), `places/capital/underground-bazaar.md` (Giblets), `factions/the-cellar-custodians.md` (GM Secret).

**Bazaar uprising thread** (future)
Kess is positioned as a future organizer: Cartographers Guild network, grandmother's intelligence cache, personal grievance, methodical temperament. Moth as wildcard (nothing to lose). FourthEye pipeline crossing Regency hard lines as potential lever. Don't develop without Drew — flag as long thread.

## Do Not

- Invent mechanics in isolation — adapt from existing stat blocks, and flag if something is genuinely new
- Create files outside the established directory structure without asking
- Use emoji in files
- Write a fact's own justification into canon text. A location or creature file states what is — geography, behavior, appearance — not why it must be that way. Reasoning belongs in `memory.md`'s threshold log, where the before-state and the "why" are the whole point; a content file explaining itself is reasoning that leaked out of process and into product
- Use specific distances in bestiary or quest content — combat is abstract positioning (Frontline/Backline) and "in reach / close / far," never measured distance
