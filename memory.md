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

## A Status Belongs to Its Target, Not Its Source

Drew, 2026-08-18: *"once a status is applied, it leaves the caster and becomes attached to the target. so removing the caster doesn't remove a resolved status. I think that's how it should stay too."*

The reason is snowballing. If dropping a combatant also stripped every status they had applied, the first collapse in a fight would pay out twice — once by removing an actor, again by refunding all their pressure. The team already winning would win harder for the same action, and fights would decide themselves earlier than the cards did.

Worth keeping because it is the kind of rule that gets reintroduced by accident rather than on purpose. It was: the first draft of the status-tracking rule said *"the card and the effect end together"* while also placing the card in front of the caster, which reads as caster removal ending their effects. Nobody designed that; it fell out of describing the physical tracker as though its location meant ownership.

**The engine was already right.** Statuses are plain counters on the combatant holding them, with no reference to who applied them, so caster removal cannot reach them — confirmed empirically, not just read. The only collapse-time cleanup is `_clear_ongoing_on_collapse`, and it clears Anchored-type effects on the collapsing combatant's *own* list, which is Anchored's own rule about its holder rather than anything about casters.

## Rushdown Is Closing Distance, Not a Shove

Drew, 2026-08-18: *"forced movement breaks a stance in the player fantasy correctly. but in the player fantasy rushdown is not a forced movement option. it's in the name rushdown. that's a combatant moving in quickly towards another combatant... a combatant moving towards an anchored combatant doesn't break the stance."*

So Rushdown is the one movement that does not end Anchored. Every other forced reposition — HAUL, HEAVE, REPEL, SYSTEM PURGE, THE ROOM LEANS IN, CENSURE's and ROLLING THUNDER's pushes — still does, and correctly.

Worth keeping because the exception is not derivable from the mechanic. Mechanically Rushdown relocates the *target* from Backline to Frontline, which reads as forced movement and is why the rule needed stating explicitly rather than following from anything. The justification lives in what the name depicts, not in what the card does to the board.

**Cover is the sub-case that goes the other way.** Cover is an Anchored effect, so the Rushdown exception would carry — except cover states the Backline as a requirement of its own, so being pulled out of it ends cover regardless. Drew ruled the Rushdown/Anchored interaction; the Cover consequence is an inference from cover's own stated requirement, flagged as such when written.

**The related engine bug, fixed the same day.** The tick gated every Anchored payout on `who.position == o['anchor']`, which *suspended* a stance while its holder was displaced and silently resumed it if they came back. The written rule had always said "ends immediately." Drew: *"suspending anchored is a bug."* Fixed by making `Combatant.position` a property whose setter ends anchored effects on a real change — one place instead of the thirty-odd call sites that move people, the same reasoning that made `max_hp` computed rather than patched.

## Any Stat, If the Table Agrees

Drew, 2026-08-18: *"the roll can be made using any stat that the player or GM can argue for that makes sense in the narrative, the table must agree. this is a blanket rule that applies to any check or save."*

It supersedes `rules/out-of-combat.md`'s previous closing line, *"When multiple stats could apply, the player may make their case. The GM decides."* — the adjudicator moved from the GM to the table.

The consequence worth remembering: **every stat named in a rule is now the obvious choice, not the only one.** Stealth says Soul, the flee check says Soul, the chase says Soul; each still names its stat, and each is now an example rather than a constraint. It also retroactively legitimises creature entries that already deviated — the Briarbound's ambush asks the party for Senses or Reason where the general rule says Soul, which was a conflict before this ruling and is an ordinary application of it after.

## Equipment Provides, It Does Not Grant at a Moment

Drew, 2026-08-18: *"equipment provide effects while worn not only granted at combat start. statuses still work normally (evade leaves after it triggers). at the end of combat equipment effects that expired, get reapplied."*

Fourteen items and pricing examples had said *"start combat with X."* Drew's note that this *"was a simplifier for the repo I used that was never the real way it worked at the table"* is the useful part: the written rule had been a convenience, and the table had been playing the fuller version all along.

Inside one fight the two are identical, so nothing rebalances. What changes is that the effect is true out of combat as well, and the rule now says *why* you have it rather than *when* you got it. The wording needs both halves — provision plus an end-of-combat refresh — because "while worn" alone would imply Evade regenerating the instant it triggers, which is not the intent.

It also separates the two kinds cleanly, which the old phrasing did not: **Armour X and Thorns are persistent** and never expire, so refresh never applies to them; Evade, Resist, Protect, Ward and Deadly are consumable and do.

## A Chase Tracks the Gap, and Contact Decides Nothing

Drew, 2026-08-18: *"no explicit track length needed. all that needs tracked is relative distance. the fiction determines the starting distance apart... a chase where they have no space between them is 'captured'. but captured isn't automatic."*

The old two-marker track was broken in a way its own example demonstrated: *"right on your heels = both at 0"* satisfied the catch condition (*"the pursuer's marker reaches the fleeing party's marker"*) before a single roll, and a pursuer winning from a gap of zero moved *past* the fleeing marker into a state the rule gave no meaning to. Simulated at even odds it also ran 86% / 75% / 39% in the pursuer's favour at the three documented starting gaps — a chase was mostly a formality.

Tracking only the gap fixes both and makes the odds legible: with absorbing ends at 0 and 4, **escape probability is simply the starting gap over 4.** One step apart is 25%, two is even, three is 75%. The GM sets difficulty by setting distance, and can read the number off without a table.

**Contact grants the initiative, not a free attack.** Drew, 2026-08-18, on the alternative offered: *"giving the pursuer the first turn makes sense."* The reasoning behind refusing the free attack still stands and is why the lighter lever was the right one: Drew asked whether the chaser should get an ambush-style attack before initiative. No: Ambush and Unguarded both pay out for *arriving unseen*, and a fleeing character knows exactly who is behind them — granting the ambush package here would make the word cover two different mechanics, in the same session that split Unguarded off so it wouldn't. It would also collapse the choice the rule exists to create: if the free hit is automatic, *fight or subdue* stops being a decision. The lighter lever, if contact ever needs to feel more decisive, is giving the pursuer the first turn rather than a free hit.

## Reactions Need Awareness; Properties Do Not

The line that settles how an opening interacts with every defensive keyword, and the reason the earlier attempts felt wrong. Drew, 2026-08-18: *"ambush and unguarded still don't interact right with evade or immunity. I'm not sure what solution best matches the intended play experience."*

- **Reactions** — Evade is a dodge, Protect is throwing yourself in front of an ally. Neither can happen against a blow nobody saw. An **ambush** beats both.
- **Properties** — Armour, Resist, Thorns and Immunity are what you are made of. They apply to anything, always.

So an ambush makes you easier to **hit**, never easier to **survive**. **Unguarded** beats neither category — the target can see you fine and simply is not swinging back, so all it takes is the defense card and the reveal. The attacker's own Blind still rolls either way: it is their failing, not the defender's reaction.

**Immunity's fiction is what makes this obvious.** It comes only from LAST RESORT, UNBROKEN and UNTOUCHED, all gated on *"if your HP is 6 or less"* — it is not a dodge or a block, it is a refusal to fall. Deleting it for an ambush removed it in precisely the situation it exists for.

**Removing the carve-out cost nothing, which was checked rather than assumed.** Those three cards are Immunity's only sources — no item grants it — and all three are played *during* combat. A target being ambushed pre-combat is at full HP with no cards played, so **they can never hold Immunity when the auto-hit lands.** The exception had never been able to fire; it existed only to make Immunity's own text false.

If an ambush should ever feel more lethal, the lever is damage or a Deadly stack on the auto-hit — not stripping defenses, which is what tangled it in the first place.

## Unguarded Is an Opening, Not Helplessness

Drew, 2026-08-18: *"the fantasy isn't a creature or character who is willing to be hit. they are non aggressive, allowing an opening for the first strike. but they will defend if shown a threat."*

The first draft gave Unguarded an ambush's auto-hit, which said the wrong thing: it made the target unable to protect itself at all. Corrected, the two states pay for different things and therefore buy different things.

- **Ambush** pays for arriving unseen. Its auto-hit beats Evade and Immunity, because the target never knew.
- **Unguarded** pays for the target not fighting yet. The attack is **unblocked** — no defense played, no reveal resolved — but **Evade and Immunity still apply**, because they can see you coming and are simply not swinging back.

The other half is a real choice rather than a free lunch: a side facing an Unguarded target may **strike** and take the unblocked attack, or **ready** visibly and drop the state with no attack at all. Both end it, and you cannot do both — readying is visible, and visibility is exactly what closes the opening.

**GRAPPLE and SUBDUE were named backwards** (Drew, same day): grapple is the general action — a contested check to grab, tackle or pin — and `cards/subdue.md` is its specialised card embodiment. The card was renamed; the action now carries the plain word.

## Maxing a Stat Is Priced, Except Mind

Drew, 2026-08-18, on whether Advancement needs a numeric stat cap: *"I still think that maxing a single stat already has a built in flaw in rps."* Measured rather than argued, with `combatsimulations/stat_spread_lab.py`. **The intuition holds for two stats out of three, and the exception is the useful part.**

Piling three advancement points into one stat (total 12) against a spread 4/4/4, both sides on balanced decks and both orderings run:

| Piled | HP | tactician | punisher |
|---|---|---|---|
| Body 8/2/2 | 28 | 41.2% | 44.6% |
| **Mind 2/8/2** | 16 | **60.8%** | **60.8%** |
| Soul 2/2/8 | 16 | 31.7% | 27.9% |

**Body loses while holding 28 HP against 24, which is the clearest evidence the pricing is real.** Soul loses hardest. **Mind wins, and wins more as it grows** — 55–60% at the starting total of 9, 60.8% at 12.

**The mechanism is hand size, and it is the one thing the RPS pillar cannot read.** A defender chooses blind from revealed-colour history, so every other advantage a specialist buys is a colour, and a colour is legible. Mind buys *options*: at Mind 8 you hold eight cards to your opponent's four, so you almost always have the counter colour available. Prediction cannot punish a player who holds every answer.

So the built-in flaw Drew described is real, and it is specifically a flaw in **damage** specialisation. Mind is not a damage stat in the same way — it is an information stat wearing a damage stat's clothes.

**The numbers above are wrong, and the correction matters.** Re-run on 2026-08-18 across ten deck-sampling seeds at 600 duels each, the mirror baseline (4/4/4 against itself) is **49.2% ± 1.7**, a legal Mind 3/6/3 is **52.9%** with a range of 46.8–62.3, and an illegal Mind 2/8/2 is **54.6%** with a range of 47.7–59.8. The 60.8% reported earlier was a single deck draw sitting near the top of that range, not a representative figure.

Two things follow. **Mind is advantaged, but by roughly four points rather than ten** — real, much smaller than claimed. And **the spread cap does not fix it**: 3/6/3 and 2/8/2 differ by 1.7 points, inside one standard deviation. Mind at 6 is very nearly Mind at 8.

**The largest single factor is which cards you drew.** Deck-draw variance (sd 3.4–3.8) is comparable to the entire stat effect. A conclusion from one deck sample is a conclusion about that sample.

The cap still stands on its own terms — it is character creation's own limit, it is one rule instead of two, and it stops builds nobody intended. It just is not the answer to Mind, and it was partly recommended as one.

**Resolved by capping the spread, 2026-08-18** (Drew: *"lets cap the stat spread"*). The lab picked the number: Mind-heavy builds at total 12 against a spread 4/4/4 run 50.9% at gap 2, ~54% at gaps 3–4, 56% at gap 5 and **60.8% at gap 6**, against a mirror baseline of 50.8–52.5% that sets the noise floor. **No stat may exceed another by more than 3** — which is not a new number: base 2 plus three points to spend already makes 5/2/2 the widest legal build at creation, so the cap is creation's own limit extended past creation, and it *replaces* the old "no single stat may exceed 5" rather than joining it. It cuts the 60.8% outlier to roughly 54%, inside the range the other stats already occupy. **Scoped to player characters only** — five existing stat blocks exceed a spread of 3 (Aege, Fermata, the Gluttony Abomination, Hullback, the Patient Host) and none of them are wrong: creatures and named NPCs are designed rather than budgeted. Temporary combat drains (Sunder, Wither, Erode) are also unbound.

**The separate finding, from the same lab:** leaning your *deck* into your maxed colour is punished far harder than the stat itself. Body/Red mono runs 37.9–41.7% against 45.4–48.8% for the same stats on a balanced deck. The trap is the deck the max tempts you to build, not the max.

**Caveats, because the numbers are only as good as the model.** The simulator has no equipment or items, decks here are constructed rather than Oracle-grown, and the policies are heuristics — a bot holding eight cards may exploit them harder than a person would, which would inflate the Mind result specifically. An earlier run of this same question reported a cleaner "no specialist ever wins" result; it was wrong because it ran only one ordering for the balanced condition. Both orderings are summed now.

## Wounds Are Reachable in Hand and Discard, Never in Deck

Drew, 2026-08-18: the gap between what clears a Wound and where Wounds live is deliberate. Cards and actions reach your hand and discard pile; only a rest reaches your deck. A Wound shuffled into your deck is a cost you carry out of the fight, and nothing in combat can reach in and take it back.

Recorded here rather than in `rules/status-cards/wound.md`, where I originally put it. That file is printed and handed to players, and its own preamble says to state the rule and stop — *"no why it's shaped that way... if it's a live design question worth remembering, it goes in `memory.md`, not here."* I wrote the reasoning into the handout specifically so a later pass would not "fix" the gap, which was the right worry and the wrong location.

## The Deck Cap Is What Keeps Status Cards Heavy

Drew, 2026-08-18, on why the cap beats the plan it replaced: *"my previous plan was more convoluted — managing player decks by forcing periodic removals, bazaar trading to reduce deck size, and status cards to dilute larger decks. the bank and max deck size handles it better, without losing any of the interesting mechanics. plus it keeps status card impact more meaningful. larger decks care less about status cards."*

That last line is the part worth keeping. **A Wound in a 9-card deck is one draw in nine; the same Wound in a 20-card deck is one in twenty.** An uncapped deck quietly defuses every consequence the game can hand out, so the longer a campaign ran the less anything stuck. Capping the deck holds the denominator still and keeps a Wound costing what it cost on day one.

It also retires three mechanisms that existed to fight the same problem from different directions — forced periodic removal, bazaar trading as deck-shrinking, and status cards as deliberate dilution. None of them are lost: trading is still trading, removal is still available, and status cards still do what they do. They simply stopped having to also serve as deck-size management.

**The 10-card playtest decks are not evidence against the cap.** Kevin's and Drew's daughter's session ran before either the bank or the cap existed, which is exactly why both decks sit one card over.

## A Deck Is As Big As You Are

Drew, 2026-08-18: *"decks don't grow forever, instead a new card from the oracle replaces an old card the player chooses. the maximum is equal to total stats."*

**I had argued the opposite and been wrong about the evidence.** A character starts with 2/2/2 plus three points — nine total stats — and a nine-card deck. I read that match as a coincidence and used it to argue *against* a cap, on the grounds that capping would make the Oracle ritual illegal from session two. It does not: it makes the ritual a **replacement** rather than an addition, which is a better ritual. The match was the rule, not a coincidence, and it also unifies players with creatures, whose decks have always equalled their stat lines.

The consequence is that a deck stops being an accumulation and becomes a **shape**. Growth still happens — a stat increase widens the deck by one — but the ordinary session asks what you are willing to put down, not what you would like to add. **This is what makes the bank necessary rather than optional:** something has to hold what comes out, or every Oracle card is also a small funeral.

**Evidence the old behaviour was real:** both archived playtest decks are exactly one card over — nine total stats, ten cards, one Oracle pick each from Session 1. Left as they are; archives record what happened.

## Cards Are Not Objects in Eclipseria

Drew, 2026-08-18: *"cards and the bank exist outside of the world. they aren't physically present in the world."*

Nobody in the world holds a card, drops one, or finds one in a drawer. A card is a way of acting that somebody learned (`world/lineage.md`: *"every technique, every card, every way of surviving a fight was learned from something"*), and the deck is how that is handled at the table. The bank is the same — real, yours, and nowhere.

It explains two things that were already true and previously unexplained: why the Underground Bazaar trades a card for a memory or a secret, and why nothing there is ever bought with coin. What changes hands is the experience. There was never a piece of card to hand over.

## Value Is Demand for a Lineage, Not Rarity

Drew, 2026-08-18: *"we have no rarity tiers, which I don't think we should... a card trader evaluates the value of the card, but they may also have a desire for cards with specific tags that they are willing to trade more for."*

Cards sit at roughly one power level, so price cannot come from power. It comes from **tags** — a tag names the tradition a card still comes from, and a trader assembling MASON work has no use for a WEALD card at any price and every use for a common MASON one.

That gives the soul economy a denomination it lacked: untagged commons are small change, a wanted tag settles a trade on its own. It also keeps the bazaar's existing character intact — *"a party with money and no leverage will find nothing worth having"* was already describing exactly this, without a mechanism behind it.

## Hold Off on Unheld Lore During Story-Crafting

Drew (2026-08-15): "I want to make an explicit design note to not touch unheld lore when story crafting." The People of Promise's larger arc (their "final current," and Kaine's own thread) is genuinely a ways out — not near-term work. Past that, Unheld-focused story content generally, and *especially* `world/creation-myth-the-three-cuts.md`, are the campaign's endgame material, tied to the council/Pendragon Attempt payoff (`world/the-regency.md`). Don't reach for either early just because a scene brushes up against the coastline or a funeral.

**One deliberate exception, not a contradiction of the above:** seed an early scene of the "orthodox" death rite — releasing the deceased into the Unheld at the coastline — several sessions before the party ever reaches Glasslight Reach. Ordinary custom, not deep lore or Promise theology specifically; the point is quiet foreshadowing so Glasslight's own Unheld-adjacent content doesn't land from nowhere later. Keep it that light — a witnessed tradition, not a hook into cosmology.