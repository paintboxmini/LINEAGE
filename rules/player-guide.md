# Player Guide — Combat & Exploration

For players who already have a character — three stats, a nine-card deck, and gear. Building one lives in `rules/character-creation.md`; this is what you need once you're actually sitting at the table.

---

# Part One: Combat

## The Stats

| Stat | Colors your damage | Also drives |
|------|---------------------|-------------|
| Body | Red cards | Max HP = (2 × Body) + 9 |
| Mind | Blue cards | Hand size = Mind (minimum 2) |
| Soul | Green cards | Initiative = 1d6 + Soul |

A card's color determines which stat powers its damage, no matter which stat is highest on your sheet.

---

## Positions

Every combatant is in the **Frontline** or the **Backline**. Each side of the fight has its own Frontline and Backline — the two Frontlines face off at the center; each side's Backline is its own rear position. Both are abstract zones; any number of characters can share one. Moving costs your action. Neither position gives automatic protection — the Frontline does not shield the Backline from being targeted.

**Range Matrix** — which cards you can legally play, based on where you and your target stand:

| You | Target | Melee | Ranged | Both |
|-----|--------|-------|--------|------|
| Frontline | Frontline | ✓ | ✗ | ✓ |
| Frontline | Backline | ✗ | ✓ | ✓ |
| Backline | Frontline | ✗ | ✓ | ✓ |
| Backline | Backline | ✗ | ✓ | ✓ |

Melee requires both of you in the Frontline. Everything else is Ranged range.

**Rushdown** — an action that drags a Backline *enemy* into the Frontline. Can't target allies. You must be in the Frontline yourself to use it.

**Cover** — an action, Backline only, and the fiction has to justify it (something to actually hide behind). While in cover you gain Evade; attacking drops it immediately.

**Confined spaces** — in tight terrain the GM may cap how many fit in a position, or block targeting entirely if something physically blocks the way.

---

## Turn Structure

Draw to your hand size the moment initiative is rolled, then again at the start of every one of your own turns. If your deck runs out, shuffle your discard into a fresh deck first.

Each turn: **one Action, plus one Bonus Action.**

| Action | What it does |
|--------|--------------|
| Play a Card | Attack with a card from your hand |
| Move Position | Frontline ↔ Backline |
| Use an Item | Activate something equipped or carried |
| Rushdown | Pull a Backline enemy to the Frontline (must be Frontline yourself) |
| Take Cover | Backline only, fiction-justified — gain Evade until you attack |
| Interact | Anything noncombat the fiction allows |
| Wait | See below |
| Flee | Attempt to leave the fight — see Fleeing Combat |

Your **Bonus Action** can only Use an Item. Using an Item is also legal as your regular Action — spend both that way and you use two items in one turn, at the cost of not attacking.

**Wait.** Give up your action on purpose, and in exchange, reinsert your turn token anywhere later in the initiative order — you're standing on the turn marker, so "later" is the only direction available. Land a slot or two out and you act again shortly; land far enough to lap the wheel and you sit out a stretch entirely. There's no cap on how far you can push it, since moving later is always a cost, never a reward. Its main use is coordinating with allies — sliding yourself right after a setup, or right before the ally you're setting up. You can't Wait two turns in a row; the turn after a Wait, you must take a real action.

---

## Initiative & The Wheel

At the start of combat, everyone rolls **1d6 + Soul**. Highest goes first.

**Ties** — higher Soul goes first; still tied between two players, they choose; still tied between a player and an enemy, the player goes first.

Tokens sit clockwise around a wheel in initiative order, whoever went first at 12 o'clock. A turn marker advances to the next token each turn. The wheel always has exactly as many slots as there are combatants — when someone joins or leaves, the wheel gains or closes a slot, and everyone between shifts over one.

**Initiative Shift X** (a card effect) moves a token X slots — positive = counterclockwise (sooner), negative = clockwise (later). A positive shift can never make its target act later than they already would; a negative shift can never make them act sooner. At exactly 3 combatants, shift magnitude is reduced by 1 toward zero before applying — the wheel is most sensitive there. Large enough shifts turn into a skipped turn or an immediate bonus turn rather than breaking those rules. Full mechanics and worked cases: `rules/card-glossary.md` (Initiative Shift X) and `rules/initiative-shift-examples.md`.

---

## Attack Resolution

1. **Attacker plays a card, face down.** Committed, not yet public.
2. **Blind, then Evade check.** Blind checks the attacker's own stack; Evade checks the defender's. Both resolve here, before the defender picks anything.
3. **Defender chooses a card to defend with, face down — blind.** No peeking at the attacker's card. The chosen card must satisfy its own Range for the current positions, same as if the defender were attacking. No legal card in hand means no legal defense.
4. **No defense → attacker wins automatically.**
5. **Both reveal simultaneously.** Only now do the cards become public and move to discard. Resolve Rock-Paper-Scissors:

```
Blue (Mind)   beats  Red   (Body)
Red  (Body)   beats  Green (Soul)
Green (Soul)  beats  Blue  (Mind)
```

- **Attacker wins** → deals damage, then the card's Effect triggers.
- **Defender wins** → no damage; the defender's Defensive Bonus triggers.
- **Tie** → no damage. The attacker's Effect still triggers first, then the Defensive Bonus — unless the Effect cancels it.

An Effect that only adds to *this attack's* damage does nothing on a miss or a tie — there's no hit to add to. Effects that do something else (apply a status, reposition, shift a stat) trigger normally regardless.

---

## Damage Pipeline

When attack damage lands, it passes through, in order: **redirect** (e.g. Shared Burden) → **volunteer shield** (Protect) → **Resist / Vulnerable** (one stack of each cancels the other first; otherwise Resist halves, Vulnerable adds 50%, rounded down) → HP.

A single attack can never push a standing combatant below 0 HP — that's a Collapse, not a kill.

**Unpreventable** damage skips this pipeline entirely — Thorns, status damage, and HP costs aren't attacks, so nothing above applies to them. They land in full.

---

## Reading Your Cards

Every card has: **Name / Color + Stat / Attack (Stat + die) / Effect / Defensive Bonus / Range / Flavor text.**

The die tells you the card's philosophy:

| Die | Personality |
|-----|-------------|
| d8 | Raw power — high ceiling, less control |
| d6 | Utility — moderate damage, strong effects |
| d4 | Precision — low damage, high control and information |

(d10 shows up on a handful of cards as a genuine outlier above this scale — rare, always paired with a real cost.)

Some cards carry a **Special Rule** line instead of — or alongside — an Effect and Defensive Bonus. It overrides normal resolution exactly as printed.

**"Attacker"/"Defender" vs. "Target"** — two different things on card text:
- **Attacker/Defender** means whoever you're resolving *this specific exchange* against. No choice involved.
- **Target** means you genuinely choose — an ally among several, or a specific enemy when more than one is present.

---

## Keywords Quick Reference

*Initiative Shift X is covered above, under Initiative & The Wheel — not repeated here.*

| Keyword | What it does |
|---------|---------------|
| Deadly | Next damage roll, add a d6. Stacks; cancels 1-for-1 with Weak. |
| Weak | Next damage roll, subtract a d6. Stacks; cancels 1-for-1 with Deadly. |
| Resist | Next successful attack against you, take half damage. Cancels 1-for-1 with Vulnerable. |
| Vulnerable | Next successful attack against you, take 50% more damage. Cancels 1-for-1 with Resist. |
| Evade | 50% chance the next attack against you misses outright, checked before you choose a defense. |
| Blind | Attacker's own 50% miss chance, checked before the defender even picks a card. |
| Staggered | Your next attack or defend — whichever comes first — is skipped instead. |
| Rooted | Can't voluntarily change position until your next turn. Forced movement (Rushdown, Pull) still works on you. |
| Anchored | A stated benefit that keeps triggering each of your turns as long as you don't move. Ends immediately on moving or Collapsing. |
| Quick | Change position for free — doesn't cost your action. |
| Ward | Blocks the next Debuff (Weak, Blind, Vulnerable, Staggered, Rooted, or a stat reduction) applied to you. One use. |
| Immunity | The next attack against you fails completely, before any card is even revealed. One use. |
| Protect | The next time an ally would take attack damage, you take it instead. |
| Thorns X | Deal X damage back to any enemy that lands a melee hit on you. |
| Counter Attack | Deal this card's Attack damage back to the attacker. |
| Lifesteal | Heal half the damage this attack actually landed, rounded down. |
| Critical | This attack's base damage (stat + die, Deadly/Weak included) is doubled. Each card that grants it states its own trigger. |
| Scry X | Look at the top X cards of a deck (yours, unless stated otherwise). Sort each to top, bottom, or discard, in any order. |
| Exile | Removed from play for the rest of combat — doesn't go to discard, can't be retrieved. Returns to discard when combat ends. |
| Expose [Color] | Blindly pick a card from the target's hand; if it's the named color, the stated effect applies. |
| Locked | That card can't be played, until end of combat unless stated otherwise. |
| Sealed | Can't Use an Item — action, bonus action, or passive — until end of your next turn unless stated otherwise. |
| Obscure | Enemies can't look at or manipulate your hand or deck (doesn't stop status cards being added). |
| Reveal Hand | At the table: state your color counts in hand ("2 Red, 1 Blue"). |
| Rushdown | Move a target enemy from Backline to Frontline. You must be Frontline; can't target allies. |
| Unpreventable | Ignores every defense that applies to attacks — lands in full. |
| Positive Status Effects | Shorthand for Evade, Resist, Deadly, Protect, Anchored, Quick, and Immunity all at once. |
| Debuff | Shorthand for Weak, Blind, Vulnerable, Staggered, Rooted, and stat reductions — the six things Ward and Deflect can prevent. |

Full canonical wording for all of these: `rules/card-glossary.md`.

---

## Status Cards

**Injury** — enters your deck as a consequence. Can't be played; sits in your hand occupying a slot until removed. In combat, spend your action to destroy one from your hand. Once per short rest, destroy one from hand, discard, or deck. A long rest destroys all of them.

**Exhaust** — goes straight into your hand (not your deck) when applied — the slot cost is immediate, not something you have to draw into. Spend your action to destroy all Exhaust in your hand at once. Any rest, short or long, clears all of it.

---

## Collapse & Death

Reduced to 0 HP → **Collapse.** You cannot act, cannot defend, and are automatically hit by anything targeting you. A single attack can't push a standing combatant below 0, but further damage while already Collapsed can. Reach **negative half your Max HP (rounded up)** → death.

While Collapsed, you can still be healed back into the fight, and recover 1d4 HP every 3 in-game hours if left alone.

If the whole party goes down, the GM decides the outcome from the enemy's own nature and intent — death is possible, not automatic. Captivity, humiliation, forced retreat, and stranger fates are all real options. The GM can also declare instant death outright when the fiction genuinely demands it (a beheading, a fall into the void) — a rare override, not a default.

---

## Fleeing, Chasing, and Stealth

**Flee (mid-fight)** — an action: **2d10 + Soul vs. DC = 10 + the highest Soul among enemies**, adjusted by the GM for terrain, position, and whether the enemy actually cares. Success ends your participation in the fight (the enemy may give chase — see Chase below). Failure costs the action; you're still there.

**Chase** — a two-marker track instead of repeated rolls. The fleeing side starts however many exchanges ahead they already are; the pursuer starts at 0. Standard track is 5 steps past the fleeing side's start. Each exchange, contested Soul (2d10 + Soul) — winner advances one step. Caught = pursuer's marker reaches the fleeing side's. Escaped = the fleeing side reaches the end of the track.

**Stealth & Ambush** — a Soul check, DC = 10 + the highest Soul on the side being approached (creatures ambush the same way, GM rolling for them). Success: the ambusher's first attack auto-hits, no RPS, no defense — then everyone rolls initiative as normal, ambusher included, and the fight proceeds.

In any of these, discarding a card whose name meaningfully fits the action grants **Advantage** (roll 3d10, drop the lowest).

---

## Ongoing & Simultaneous Effects

**Ongoing Effects** stay face-up in front of you after use until their stated condition is met, then discard. Multiple can be active at once unless a card says otherwise.

**Simultaneous Effects** — when two or more things would resolve at the same instant, the controller of those effects chooses the order (the acting player decides if the controllers differ). This does *not* apply to Attack Resolution — Effect always resolves before Defensive Bonus on a tie, no one chooses that order.

---

## You Are Not Your Own Ally

Card effects that say "allies" or "enemies" never include yourself. You can't target yourself with an ally effect, and you can't accidentally trigger an enemy effect on yourself. "All allies in your position" means everyone else sharing it — not you. The only exception is a card that explicitly names *yourself* as the target.

---

# Part Two: Exploration

## Core Resolution

Attempting something risky outside combat: roll **2d10 + the relevant stat**, compare to a Difficulty Class the GM sets.

| Difficulty | DC |
|------------|----|
| Easy | 11 |
| Normal | 13 |
| Hard | 16 |
| Extreme | 19 |

Meet or beat it to succeed. The fiction decides which stat applies — Body for physical exertion, Mind for reasoning and interpretation, Soul for bonds, will, and spiritual pressure. If more than one could plausibly apply, make your case; the GM decides.

---

## Advantage & Disadvantage

If a card in your hand has a name that genuinely fits what you're attempting, discard it for **Advantage** — roll 3d10, drop the lowest. (**Disadvantage** is the mirror: roll 3d10, drop the highest.) The table has to agree the connection is real — ask yourself whether a reasonable person would look at the card name and see it.

This is a separate system from Deadly/Weak, which only ever apply to combat damage rolls — the naming is deliberate so the two never collide.

---

## Checks vs. Saves

**Checks** are active — you're trying to accomplish something. Body overcomes a physical obstacle; Mind obtains or interprets information; Soul creates or maintains a bond, or resists spiritual pressure.

**Saves** are reactive — something is happening *to* you. Body against fatigue, falls, cold, forced movement; Mind against illusion, manipulation, memory interference; Soul against fear, corruption, possession, despair.

The difference matters for what failure means: fail a check and you didn't accomplish what you set out to do; fail a save and you suffer something you couldn't fully prevent.

---

## Perception

Not one roll — the GM reads what kind of signal is actually present and assigns the matching mode. You can propose a different mode if the fiction genuinely supports it.

| Mode | Stat | Notices |
|------|------|---------|
| Reason | Mind | *What* something is — hidden mechanisms, symbols, inconsistencies, tracking, puzzle clues |
| Senses | Body | *When or where* something happens — movement, vibration, ambushes, unstable footing |
| Read | Soul | *What something intends or signifies* — lies, fear, confidence, corruption, hostile tension |

**The one table rule:** when a player says "I look around" or "I try to get a read on this," ask one question — *what are you actually trying to notice?* That answer picks the mode. A player who names what they're looking for, and picks the right mode, gets a sharper result on success than a vague search ever would.

---

# Between Fights

## Resting

| Rest | Duration | Heals | Also clears | Limit |
|------|----------|-------|--------------|-------|
| Short | 20 minutes | 1d6 + Body HP | All Exhaust; may destroy 1 Injury from hand, discard, or deck | 3/day, can be chained |
| Long | 7½ hours | Full heal | All Injuries and all Exhaust | Once/day, requires genuine safety |

Either length reshuffles your discard into your deck and refreshes your hand to full.

---

## Equipment

Three slots: **Weapon, Armor, Artifact.** Only what's actually equipped carries a permanent passive effect — everything else about how you look or what you're carrying is free, unrestricted fiction. Carried items (equipped or not) are used via the Interact action, or the Use an Item action/bonus action in combat. Artifacts are resonant items aligned with a Seat's domain.

Full tier system and the world's item catalog: `rules/equipment.md` and `rules/items.md`.
