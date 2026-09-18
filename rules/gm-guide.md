# Running Tales Untold

This section is for the GM. None of it is mandatory. Tales Untold runs fine as a tight tactical game with minimal prep. It also supports deep, strange, atmospheric play. Both are valid.

---

## The Basic Job

Present a world that responds to what the players do, and play everything that isn't a player character honestly.

You don't need to plan every encounter. You don't need to know where the story ends. You need to know what the world is doing right now, and what happens if the players don't intervene.

---

## Running Locations

Every location in Eclipseria has its own logic. The Turnroot Weald redirects. Vulture's Nest watches. The Ashfall Wastes press. You don't have to explain this logic to your players — it's often better if you don't. Let them feel it first.

**Lead with one sensory detail.** Not a paragraph — one thing. The smell of pitch and citrus in Vulture's Nest. The way the Glasslight cliffs sing when wind passes through. One specific detail does more than five general ones.

**Let NPCs feel at home, or not.** A Glasslight local speaks gently and doesn't interrupt. A Tideward dockmaster welcomes you loudly and files you away quietly. Characters who fit their location make that location feel real. Characters who don't fit make it feel bigger.

**You don't have to describe everything.** If the players aren't looking for it, it doesn't have to exist yet. The world fills in as it's needed.

---

## Building Enemies

An enemy needs:
- **Stats** — Body, Mind, Soul (same as players, same functions)
- **HP** — use `(4 × Body) + Soul + Mind`, or pick a number that fits the fiction
- **A deck** — size = the creature's total stats, color counts = each stat; 3 themed signature cards + core fill (see `rules/cards.md`, Deck Building). Enemies draw to hand size (Mind, minimum 2) like everyone else.
- **A position** — Frontline or Backline to start
- **An intent** — what does this enemy actually want in this fight?

Intent is the part most GMs skip and most regret skipping. An enemy that wants to kill the party fights differently than one that wants to capture someone, or buy time, or protect something behind it. Intent changes which targets they prioritize, when they flee, and what happens if the party collapses.

You don't need a backstory. You need an intent.

### How many of them

**Count is the balance lever, not the creature.** A weak creature is only weak alone, and the honest way to make a fight harder is to add another one rather than to inflate the one you have.

**The number that makes a fight genuinely uncertain is:**

> **N ≈ (the party's combined total stats) ÷ (the creature's CTR)**

Three starting characters at nine stats each is 27. Against a CTR 9 creature that is three of them; against CTR 4 it is six or seven; against a CTR 13 or 14 it is two. **Take one off for a fight the party should win and still remember. Add one for a fight they will probably lose.**

Measured against the simulator at a thousand fights per row (`combat-simulations/encounter_budget.py`), and accurate to about ±1 across party sizes from two to five. It drifts at both extremes and in opposite directions: it **over-counts swarms** of very weak creatures, because a lot of small things get a lot of actions, and **under-counts heavies**, because a big party can focus one down before it spends its turns. Trust it in the middle; sanity-check the edges.

**There is a headcount cap, and below CTR 5 it binds before the formula does.** Bodies are worth more than the stats on them, because every body is another turn on the wheel. **Somewhere around twice the party's number, a fight tips regardless of how weak the individuals are** — measured at 2.0x, 2.0x and 1.8x against parties of two, three and five, and at that point the swarm is carrying only about two-thirds of the party's total stats and winning half the time anyway.

So: nine creatures at one-in-every-stat sounds like an even match against three starting characters, because nine times CTR 3 is exactly the party's 27. It is not. **Six is the even fight and eight is a guaranteed wipe.** Take the formula's answer and the headcount cap, and use whichever is smaller.

**Count alone has good resolution at the weak end and almost none at the strong end.** Against CTR 4 creatures a GM can dial four, five, six or seven and get four different fights. Against a CTR 13 creature there are three settings and only one of them is a fight: one is a formality, two is real, three is a wipe.

**Mix CTRs to get the settings back.** This is the fine-tuning lever, and it is the answer to a boss encounter that needs to be hard but survivable. One minotaur against three starting characters is a formality at 100%; two is 70%. But one minotaur plus one, two, three or four CTR-3 creatures reads 98%, 95%, 84%, 48% — four usable settings inside a gap that count alone could not divide at all.

**And note which way that cuts.** One minotaur and four small things is 26 total stats and a 48% fight. Two minotaurs is 28 total stats and a 70% fight. *Fewer stats, harder fight* — because five bodies act more often than two do. When you want pressure rather than a bigger number, add bodies.

**The real limiter on mixed encounters is fiction, not math.** What makes sense hunting together, or hired by the same person, or living in the same ruin. A GM who needs a specific difficulty and cannot justify the adds should change the terrain instead.

**There is no soft-loss band.** One creature past even, the party's win rate falls to single digits and the losses are not near-misses: a wiped three-person party averages two dead and one down, not three bloodied survivors. The step from "in doubt" to "obituary" is one creature wide the whole way up the scale. Decide before the session which side of that you meant to be on.

**Party size moves the line harder than anything else.** A fourth character shifts every threshold by a full creature and sometimes two — two Harlocks against three starting characters is a 43% win; against four it is 88%. Recompute the number when a seat fills or empties, and **never carry an encounter built for four into a session where one player didn't show up.**

*These numbers were first measured as a structural floor — dice, HP, range, the reveal, positioning and the wheel — back when the simulator did not execute card Effects, with the reasoning that Effects raise both sides. **The simulator runs most of them now, and the both-sides argument mostly held.** Re-measured on 2026-09-18 at three thousand fights a row with roughly seven in eight Effect halves modelled: the heavy end did not move at all — one and two minotaurs read 94.5% and 65.0% against 94.5% and 64.6% before. **The swarm end moved, and it moved the way this section already warned it would.** Six wrackclaws were a 48% fight on the structural floor and are a 54–56% fight with Effects running: the formula over-counts swarms, and executing Effects widens that gap by about half a creature rather than closing it. At the weak end, take the formula's answer, take the headcount cap, and lean on the cap. Still read the 50% line as "a real fight" rather than a precise coin flip — an eighth of the pool is still narrated, and a party built around those cards will drift from this.*

**Signature cards double as loot.** When a memorable enemy is defeated, its signature cards can enter the Oracle after the fight. They're a good way to make an enemy leave a permanent mark on the campaign.

**Old card printings are a free source of enemy variance.** Cards get revised — a die size changes, an Effect gets rewritten, a Defense Effect starts doing something else entirely. Don't treat your old printouts as obsolete once the canon text moves on. Deploy them, unchanged, in enemy decks.

The same logic that says two members of the same species shouldn't share identical HP applies to their cards: a player who's fought MOCKERY before and thinks they know what it does is a different tactical situation than a player seeing it fresh, and an old printing that reads differently from the current one recreates that uncertainty honestly — no homebrew mechanic required, just an actual older piece of paper with actual different text on it.

Reserve this for **enemy decks only, never player decks.** A player's own cards have to mean what they say, every time — that's a fairness floor. An enemy's deck is already the GM's secret information, same territory as anything else the party doesn't get to see coming.

Not every old printing is worth the bother. A card that only changed by a die size won't register as a surprise. Look for printings where the Effect or Defense Effect itself changed — those are the ones a player's memory will actively mislead them on, which is the whole point.

---

## Using the Oracle

The Oracle is your main tool for making the world feel responsive.

After encounters, add cards that fit what just happened. The party fought something from the Abyssal Ruins — add a card that smells like that. They befriended someone in Vulture's Nest — maybe a card from that relationship enters the pool. They survived something they shouldn't have — maybe something unusual shows up.

You don't have to justify every addition. Trust your instincts about what the world would offer next.

Players can propose custom cards. Take the proposals seriously, adjust anything that needs adjusting, and add them when the timing feels right.

---

## Pacing Sessions

A session in Tales Untold typically has:
- One or two combat encounters
- Several noncombat moments (exploration, conversation, investigation)
- One thing that doesn't resolve cleanly

That last one is important. Not every question needs an answer by session's end. Not every threat needs to be addressed. The world has things happening in it that aren't about the players — and occasionally reminding them of that makes the world feel much larger.

End of session, each player runs the Oracle ritual — a question answered, a card glimpsed and buried, a pick from three. That's the mechanical heartbeat. Everything else is negotiable. The Price step is worth running with intention: the buried card stays in the pool, and what a player glimpses and doesn't get is often what they start playing toward.

The very first time this ritual runs — Session 0, character creation — deserves its own tone: see `quests/washed-ashore.md`, which is where Session 0 actually happens.

---

## When to Call for Rolls

Not every action needs a roll. If success is guaranteed, describe it and move on. If failure has no interesting consequence, don't roll. Rolls are for moments where both success and failure would change something worth changing.

The Perception modes are your friend here. When players are poking at something, ask yourself which mode applies before you ask for a roll. *What are they actually trying to notice?* The answer shapes what they find — and what they miss.

**Good roleplay should move the difficulty, not remove it.** A scene played well enough that success feels inevitable is still worth a roll — just an easy one. Drop the DC to 5 or 7 instead of skipping the check outright. The dice still matter this way: a bad roll on an easy check is a real, rare stumble worth playing honestly, not a guaranteed miss wearing tension as a costume. This also keeps the reward proportional — the roleplay earned the low DC, not automatic success, so an exceptional roll on top of it can still mean *more* than the baseline outcome, not just the same outcome with extra steps.

**Mechanical detail is earned by a roll, not handed over before one.** When a player looks at something before committing to an action — the top of a rubble pile, the far side of a chasm, a locked door — resist naming the trap's trigger conditions, its DC, or its failure state up front. Let the look be its own free, safe action (an Easy Perception check, gated to what that mode would actually reveal), and answer the question they actually asked before assuming which mechanic they're walking into. A room can define a loud/forceful action that trips a hazard and *also* define a quiet way to learn about it first — both belong in the text, and the quiet option goes first at the table.

---

## Death & Consequences

The GM Override on Collapse exists for a reason. Use it when the fiction demands it, not to punish. There's a difference between a world that can kill players and a GM who's trying to.

That said — don't protect players from consequences they earned. The Ashfall Wastes are draining. The Abyssal Ruins carry risk. If the players walk into something dangerous and something dangerous happens, that's the world working correctly.

Consequences don't have to be death. Lost equipment, forced position changes, curse cards added to a deck, relationships strained, paths closed — the world has more ways to respond than killing someone.

---

## A Note on the Unheld

You don't have to explain it. You don't have to know what it wants. Drop hints when they feel right. Let some of them point toward something. Let others be noise. The distinction between signal and noise is part of what players are navigating — don't resolve it for them prematurely.

If something strange happens and you don't know why, you don't have to know why. Sometimes that's the world.
