# The Compiled Crib

A practical efficiency tool, not one of the four canonical kinds (`CLAUDE.md`, Four Kinds of Canonical Content) — it's a precompiled digest of facts the generators would otherwise re-derive from full canon reads every run: engine facts, calibration numbers, format templates. It cuts across Rule Definitions, Invariants, and Design Principles for speed; it doesn't hold canon of its own. **This file is a build artifact, not a source of truth** — every fact here has a canonical home, cited inline. When canon changes underneath it, add this file to **Pending propagation** in `memory.md` and refresh it at the next Sync. If a pattern gets retrieved repeatedly to rediscover it, that's the signal to promote it into this file rather than re-deriving it next time.

For actual best-in-class Tales Untold content — the pieces worth reading to calibrate what excellent looks like — see `agent-tools/exemplars.md` instead. That file is curated content; this one is a cheat-sheet.

Read this + the target's location/bestiary file + anything your specific task actually touches. Go to the full canon files only when the task bends a rule, the crib looks stale, or you're checking a keyword's exact text.

---

## Engine facts generators always need

*(sources: `rules/combat.md`, `rules/core-rules.md`, `rules/card-glossary.md`)*

- RPS: Blue beats Red beats Green beats Blue. Tie = no damage; attacker's Effect fires first, then Defensive Bonus (damage-amplifying effects do nothing on a tie).
- Reveals are simultaneous and blind. Defending is a prediction, not a reaction.
- **Hand size = Mind, minimum 2.** Blocking spends a card; hand is blocking capacity between turns.
- HP = (2 × Body) + 9 is the baseline every generator offers; bosses may go bespoke, marked explicitly. **Deck size = total stats** (color counts = each stat; signatures count toward their color). **Creature Threat Rating = total stats** — the difficulty scale; player baseline is 9.
- **Range counts derive from the same stat numbers as color counts, reassigned to range buckets**: Mind → Ranged, Body → Melee, Soul → Both. Within each range bucket, color mix should approximate the deck's overall color percentages rather than concentrating one color into one bucket (e.g. every Ranged card also being Blue) — that leaks color from publicly-known range legality during RPS prediction. Default starting point, not a hard constraint — real decks may deviate for a stated reason (Crimson/Sky, `combatsimulations/content.py`, lean into Frontline/Backline specialization on purpose rather than following this default). Worked example, Mind4/Body3/Soul2 (colors Blue4/Red3/Green2): ranges Ranged4/Melee3/Both2, each internally ~4/9 Blue, ~3/9 Red, ~2/9 Green. *(Drew's heuristic, 2026-07-28.)*
- Positions: Frontline / Backline. Melee needs both frontline; ranged needs not-both-frontline; "Both" always legal.
- Initiative: tokens placed clockwise in initiative order; a turn marker starts at 12 o'clock and advances one token per turn. **Wait** = forfeit action, choose a later slot (the party's sequencing tool). **Initiative Shift X** always moves the token the full distance — positive counterclockwise (never later), negative clockwise (never sooner); when that would violate the guarantee, a skip or bonus chip preserves it instead of altering the move. Full mechanic: `rules/combat.md`, `rules/card-glossary.md`; worked cases: `rules/initiative-shift-examples.md`.
- Standard DC 13. Perception modes: Reason (Mind) / Senses (Body) / Read (Soul).
- Status cards (Wound, Exhaust) go into decks — the delayed-consequence system.
- Approved keywords (canonical texts in `rules/card-glossary.md`; list maintained in `experimental/README.md`): Anchored, Blind, Counter Attack, Deadly, Debuff, Evade, Exile, Expose [Color], Protect, Initiative Shift X, Lifesteal, Locked, Obscure, Quick, Resist, Rooted, Rushdown, Scry X, Sealed, Staggered, Thorns X, Unpreventable, Ward, Weak. **No new keywords without discussion.**

## Creature Threat Rating calibration (real anchors)

*(sources: `CLAUDE.md` Stat Blocks; the bestiary files named. Creature Threat Rating = total stats; player baseline 9.)*

| Creature Threat Rating | Reads as | Anchors |
|---|---|---|
| 4–6 | teaching creatures: one lesson, simple loop, often disengages | Scratcher 4 · Jackalope 5 · Borrower 6 |
| 8–10 | a real fight: defining passive, interacting cards | Stonecoil 8 · Fogcaller 9 · Tollbird 9 · Vescal 10 |
| 11+ | above a player: named threats and bosses; toughness comes from stats | Orin Vane 11 · Root Heart 11 · Masaharu 12 · Minotaur 14 · Trisect 15 |

Stats read Mind/Body/Soul. If the brief doesn't state a target Creature Threat Rating, ask before building.

## Card format + two calibrated exemplars

*(sources: `CLAUDE.md` card format; `cards/green-soul.md`; `cards/tollbird.md`)*

Core card (universal — no tag; die philosophy: d8 power / d6 utility / d4 precision):

```
**SUPPORT**
GREEN — SOUL
Attack: Soul + d4
Effect: Target ally gains Deadly
Defensive Bonus: Target ally draws 2
Range: Ranged
*"Strength flows to those who share it."*
```

Signature card (one source tag = where it's obtained, per `world/lineage.md`; tighter identity — an effect only this creature would have; Effect ≠ Defensive Bonus):

```
**WATCHFUL PERCH**
GREEN — SOUL — BRIARWATCH
Attack: Soul + d6
Effect: Move to the Backline and gain Evade.
Defensive Bonus: Apply Initiative Shift +2 to yourself.
Range: Both
*"Still is not the same as gone."*
```

Enemy deck: **size = total stats, color counts = each stat** (signatures count toward their color); 3 signature + core to fill. Range counts derive the same way — see Engine Facts above. "Ally" wording must survive **You Are Not Your Own Ally** (`rules/cards.md`) — no color is exempt.

## Stat block skeleton

```
**Mind X / Body X / Soul X — HP X**
**Creature Threat Rating:** N
```

Bestiary files open with `**Cards:** \`cards/name.md\`` when signature cards exist, and should list a **recommended full deck** (3 signature + core picks, sized and colored to the stat line — see `bestiary/tollbird.md` for the full pattern; backfilling older entries is queued work). Named people go in `characters/`, never `bestiary/`.

## Encounter skeleton

*(exemplars: `quests/shifting-burrow.md`, `quests/the-larder-fence.md`)*

`# Name` → *italic one-line placement note* → **Intent** (what it teaches, through play not explanation) → **Setup** (environment, positioning constraints) → **Enemies** (who + deck) → **GM notes** (behavior, triggers, when to let the lesson land) → **Win Condition** → **Related Documents**.

## NPC voice (Function / Pressure / Hook)

*(exemplars: Aege/Bartho/Kino in `locations/vultures-nest.md`; Weck in `characters/weck.md`)*

Four lines of Weck, as the register to hit: *a cart that doesn't smell like animals; buys culls at fair prices, never early, never late; will buy one Wound for coin and your name in his ledger, in your own hand; answers questions honestly and unhelpfully, which is worse.* — Function (buyer), Pressure (the terms), Hook (the ledger, deliberately unanswered). Refusing is always a complete answer. NPCs embody rules; they never explain them.

## Tone in one breath

*(source: `world/tonal-bible.md`)*

Horror comes from comprehension, not confusion. Beauty and wrongness occupy the same space. The mundane and mythic coexist without the world pausing to notice. Sacrifice costs something the world doesn't refund. Not grimdark, not heroic fantasy, not whimsy — the world was never organized around you.
