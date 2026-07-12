# Exemplars — the Compiled Crib

A precompiled digest of the calibration the generators used to re-derive from full canon reads every run. **This file is a build artifact, not a source of truth** — every fact here has a canonical home, cited inline. When canon changes underneath it, add this file to **Pending propagation** in `memory.md` and refresh it at the next Sync.

Read this + the target's location/bestiary file + anything your specific task actually touches. Go to the full canon files only when the task bends a rule, the crib looks stale, or you're checking a keyword's exact text.

---

## Engine facts generators always need

*(sources: `rules/combat.md`, `rules/core-rules.md`, `rules/invariants.md`)*

- RPS: Blue beats Red beats Green beats Blue. Tie = no damage; attacker's Effect fires first, then Defensive Bonus (damage-amplifying effects do nothing on a tie).
- Reveals are simultaneous and blind. Defending is a prediction, not a reaction.
- **Hand size = Mind, minimum 2.** Blocking spends a card; hand is blocking capacity between turns.
- HP = (2 × Body) + 9 — Early creatures usually run *below* formula for fiction.
- Positions: Frontline / Backline. Melee needs both frontline; ranged needs not-both-frontline; "Both" always legal.
- Initiative: continuous wheel, no rounds. Shift ±X = next turn moves exactly X. **Wait** = forfeit action, choose a later seat (the party's sequencing tool).
- Standard DC 13. Perception modes: Observe (Mind) / Sense (Body) / Read (Soul).
- Status cards (Wound, Exhaust) go into decks — the delayed-consequence system.
- Approved keywords (canonical texts in `rules/card-glossary.md`; list maintained in `experimental/README.md`): Advantage, Anchored, Armour X, Blind, Counter Attack, Debuff, Disadvantage, Evade, Exile, Expose [Color], Initiative Shift X, Lifesteal X, Obscure, Predictable, Quick, Resist, Rooted, Rushdown, Scry X, Staggered, Thorns X, Unpreventable, Ward. **No new keywords without discussion.**

## Tier calibration (real anchors)

*(sources: `CLAUDE.md` Stat Blocks; the bestiary files named)*

| Tier | Means | Anchors |
|---|---|---|
| Early | one mechanic, teaches a concept, low decision overhead | Jackrabbit 1/1/3, HP 6 · Scratcher 1/1/2, HP 9 · Fencerow Shrike 1/2/3, HP 8 |
| Mid | two interacting mechanics, positioning matters | Orin Vane 5/4/2, HP 18 · Vescal 3/4/3, HP 18 |
| Late | full passive/card synergy, pressure from multiple directions | (no promoted anchor yet — calibrate against Root Heart / Tithe Engine) |

Stats read Mind/Body/Soul. If the brief doesn't state a tier, ask before building.

## Card format + two calibrated exemplars

*(sources: `CLAUDE.md` card format; `cards/green-soul.md`; `cards/fencerow-shrike.md`)*

Core card (universal — no tag; die philosophy: d6 power / d4 utility / d2 precision):

```
**SUPPORT**
GREEN — SOUL
Attack: Soul + d4
Effect: The next ally to attack deals +3 damage
Defensive Bonus: A target ally draws 1 card
Range: Ranged
*"Strength flows to those who share it."*
```

Signature card (one source tag = where it's obtained, per `world/lineage.md`; tighter identity — an effect only this creature would have; Effect ≠ Defensive Bonus):

```
**WATCHFUL PERCH**
GREEN — SOUL — BRIARWOODS
Attack: Soul + d4
Effect: Move to the Backline and gain Evade.
Defensive Bonus: Apply Initiative Shift +2 to yourself.
Range: Both
*"Still is not the same as gone."*
```

Enemy deck: 3 signature + 4–7 core, 7–10 total; core color counts lean toward the stat spread. "Ally" wording must survive **You Are Not Your Own Ally** (`rules/cards.md`; green is the exception — green counts itself among its allies).

## Stat block skeleton

```
**Mind X / Body X / Soul X — HP X**
**Difficulty:** Early / Mid / Late
```

Bestiary files open with `**Cards:** \`cards/name.md\`` when signature cards exist. Named people go in `characters/`, never `bestiary/`.

## Encounter skeleton

*(exemplars: `quests/shifting-burrow.md`, `quests/the-larder-fence.md`)*

`# Name` → *italic one-line placement note* → **Intent** (what it teaches, through play not explanation) → **Setup** (environment, positioning constraints) → **Enemies** (who + deck) → **GM notes** (behavior, triggers, when to let the lesson land) → **Win Condition** → **Related Documents**.

## NPC voice (Function / Pressure / Hook)

*(exemplars: Aege/Bartho/Kino in `locations/vultures-nest.md`; Weck in `experimental/the-man-who-buys-wounds.md`)*

Four lines of Weck, as the register to hit: *a cart that doesn't smell like animals; buys culls at fair prices, never early, never late; will buy one Wound for coin and your name in his ledger, in your own hand; answers questions honestly and unhelpfully, which is worse.* — Function (buyer), Pressure (the terms), Hook (the ledger, deliberately unanswered). Refusing is always a complete answer. NPCs embody rules; they never explain them.

## Tone in one breath

*(source: `world/tonal-bible.md`)*

Horror comes from comprehension, not confusion. Beauty and wrongness occupy the same space. The mundane and mythic coexist without the world pausing to notice. Sacrifice costs something the world doesn't refund. Not grimdark, not heroic fantasy, not whimsy — the world was never organized around you.
