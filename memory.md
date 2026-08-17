# LINEAGE — Memory

## Memory is the why

Memory preserves concise historical context for major decisions when that context materially improves future reasoning. A memory entry records the problem, the decisive reasoning or failed alternatives that explain the decision, the resulting principle/rule, and only the minimum provenance necessary to understand why it matters. It does not preserve complete deliberations, chronological work logs, implementation details, or every rejected idea. Those belong in archives.

Memory is not a transcript of how we thought. It is the smallest durable explanation of why the current design is the way it is.

---

## Branch map

**Default assumption:** `claude/general-chat-vwvr1` is the most current working branch. Agents should read and orient there unless Drew explicitly names a different branch to examine.

- `claude/general-chat-vwvr1` — working trunk (default source of truth for current work)
- `Main` — human merge target; not the daily desk
- Other named branches (`gpt/…`, snapshots, experiments) — only when Drew points at them

---

## Multi-Agent Notes

Different agents naturally specialize based on which parts of the repo they engage with. Drew is content adjudicator. Don't pre-define agent roles — the environment does that work.

The repo IS the persistent memory. This file captures what the repo can't — mid-session decisions and active threads.

New agents: read `CLAUDE.md` first, then this file. The experimental folder and archives show design process history.

Full session-by-session history archived at `archives/multi-agent-notes.md`.

---

## Resonance Is a Design Signal, Not a Population Count

How common Resonance actually is across Eclipseria isn't decided, and doesn't need to be — Drew (2026-08-14): "I haven't decided how common resonance is yet." Treating it as a population question is the wrong frame regardless. Resonance is a completion signal for design work, not a claim about how many people/places/items in the world happen to have it: once something reads as resonant, that's the marker it's been developed completely enough to hand to players, not evidence the world is thick with it.

Working consequence for the Degrees of Alignment framework (`world/resonant-people.md`, `world/resonant-items.md`, `world/resonant-places.md`): "Resonant" is expected to narrow over time to mean what's currently called Stage II — Aligned — rather than covering the full Stage I–III ladder. Stage I (instinct-level, unclassified) falls out of the term entirely. Eventual chart: Archon / Seat / Hallowed Ground at the top, Resonant People / Places / Items (= currently Aligned) below that, everything else beneath. Not executed yet — a target to write toward, not a rename to run today.

---

## One File Per Thing, Membership Recorded Separately

2026-08-17. `cards/` went from ~50 grouped set-files to **341 flat files, one per card**; `bestiary/` and `characters/` went from one file per entry to **one folder per entry, one file per section** (with `mechanics.md` grouped and `profile.md` merging appearance/behaviour). The reasoning is worth keeping because it will govern the next restructure too.

**What drove each split was different, and neither was tidiness.** Cards split because **art needs somewhere to live** — a card's image belongs in the card's own file. Entries split because a query for one thing (a deck) forced reading everything (lore, GM secrets, harvesting).

**The rule that came out of it:** content lives in exactly one file; *membership* is recorded separately and may be recorded many times. `cards/buckets/` and `cards/archetypes/` hold lists, never card text. A card has one home bucket but can be indexed in several — *defense* homes 41 cards and indexes 110, so filing by home alone would hide two-thirds of the defensive coverage in the game.

**The counterweight, learned the same day:** Drew — *"the parts of a character/creature that are repeatedly needed together for reasoning should live in the same file."* Section-per-file was too fine for appearance and behaviour, which co-occurred in 17 entries at ~400 characters each; they merged into `profile.md`. And `mechanics.md` stays grouped because deck size equals total stats and per-colour counts equal the individual stats — splitting the stat block from the deck would put two halves of one invariant in two files.

**Set membership was the hidden cost nobody predicted.** It had been carried implicitly by file grouping — `red-body.md` *was* the red core set — and had nowhere to go once the grouping went. It moved to `cards/buckets/red|blue|green|colorless.md`, which turned buckets from annotation into infrastructure: `printing/generate-cards.py` now reads the core set's membership straight out of them.

**What restructuring is actually good for.** Every pass surfaced content drift nothing else had caught: a card file containing no cards, Rasp's prose describing two cards retired hours earlier, 3,700 characters of duplicated card text in seven character files, Delve Roller's mangled card line, and a verify glob that silently stopped validating 6 of 37 decks while still reporting PASS. **Moving things forces you to look at them.** Expect a restructure to find bugs unrelated to the restructure, and budget for fixing them.

---

## Card Creation Is Reasoning, Not a Pipeline

Drew (2026-08-17): *"card creation is design and reasoning. An established workflow helps but can easily become too restrictive if it gets over defined."* This came out of a live case where the tool got over-defined in a single session and had to be walked back.

**What happened.** `agent-tools/card-creation.md` was read as forcing every effect into an existing keyword. It wasn't — the corpus already uses plain longhand freely (CALCULATE, STUDY, FOREST MEMORY) and `verify.py` only enforces keyword canonicity on `items/`, never `cards/`. But the tool had a prohibition with no matching permission: it said don't mint keywords for convenience, and never said plain text was legitimate or what to do when a card needs genuinely new mechanical space. Fixed by stating both, plus a **compression rule** — a keyword is earned when the set has already written the same mechanic longhand enough times that it has become vocabulary. Flag the candidate; don't mint it mid-card. No repeat threshold was set on purpose; Drew said "repeated" and "eventually" without a number.

**Then it overcorrected.** A convergence check was added on top — align a new card to how the set already expresses a similar move unless the difference is load-bearing — and Drew cut it: *"Convergence step is premature. It causes card individuality to collapse early."* Two separate defects, worth keeping distinct:

- **The altitude was wrong.** Convergence is a judgment about the corpus, made across many cards at once. Applied to one card mid-authoring, it sands off individuality before the card has established what it is. It isn't a bad question; it's a question for a different layer.
- **It authorized silent rewrites.** Compression escalates ("flag, don't mint"); convergence just said "align it." An agent would have quietly restated a card's mechanic and the fork would never have reached Drew — a direct violation of the Canon Gate. Caught on self-review, fixed, then removed with the rest.

**The standing rule:** where guidance in `card-creation.md` would flatten what makes a specific card worth having, the card wins and the guidance yields. Compression stayed because it only ever flags. Anything that would resolve a design question inside a rewrite doesn't belong in an authoring tool.

**The ratchet problem, since resolved.** Compression plus convergence formed a one-way pull toward keyword coverage with nothing pushing back — run far enough, every effect becomes a keyword and cards collapse toward *"Attack: X + die. Effect: [Keyword]"*, which is the condition Drew objected to in the first place. Removing convergence took out half of it. Drew supplied the other half on 2026-08-17, ruling that conditional triggers stay uncompressed: *"it would work but would require more memorization/table lookup for players."*

That gives the compression rule its missing counter-pressure, and it generalizes past the one case. **A keyword's real cost is paid by the player, in lookup.** Repetition is necessary but not sufficient — compress what is intricate or opaque in longhand, leave what is already self-explanatory however often it recurs. The largest repeated pattern in the set is a family of conditional triggers across at least seven cards, and it is correctly staying exactly as it is.

**Still open:** no path exists for retiring a keyword that stopped earning its place. The glossary only grows.

---

## Hold Off on Unheld Lore During Story-Crafting

Drew (2026-08-15): "I want to make an explicit design note to not touch unheld lore when story crafting." The People of Promise's larger arc (their "final current," and Kaine's own thread) is genuinely a ways out — not near-term work. Past that, Unheld-focused story content generally, and *especially* `world/creation-myth-the-three-cuts.md`, are the campaign's endgame material, tied to the council/Pendragon Attempt payoff (`world/the-regency.md`). Don't reach for either early just because a scene brushes up against the coastline or a funeral.

**One deliberate exception, not a contradiction of the above:** seed an early scene of the "orthodox" death rite — releasing the deceased into the Unheld at the coastline — several sessions before the party ever reaches Glasslight Reach. Ordinary custom, not deep lore or Promise theology specifically; the point is quiet foreshadowing so Glasslight's own Unheld-adjacent content doesn't land from nowhere later. Keep it that light — a witnessed tradition, not a hook into cosmology.