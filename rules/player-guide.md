# Player Guide — Combat & Exploration

Your stats and your gear, then how combat and exploration actually work at the table. The rest of character creation — background, and how the starting deck gets drafted — lives in `rules/character-creation.md`.

---

# Part One: Combat

## The Stats

All characters begin with Body 2 / Mind 2 / Soul 2, then distribute 3 more points among the three — no stat above 5 at character creation.

| Stat | Colors your damage | Also drives |
|------|---------------------|-------------|
| Body | Red cards | Max HP = (3 × Body) + Soul + Mind |
| Mind | Blue cards | Hand size = Mind (minimum 2); also feeds Max HP |
| Soul | Green cards | Initiative = 1d6 + Soul; also feeds Max HP |

A card's color determines which stat powers its damage, no matter which stat is highest on your sheet. Stats also decide which mode you use for checks, saves, and perception (Part Two) — a spread built around Soul reads rooms and holds oaths, around Mind anticipates and controls, around Body endures, positions, and breaks things. Your stat spread is a statement about how your character solves problems.

---

## Positions

Every combatant is in the **Frontline** or the **Backline**. Each side of the fight has its own Frontline and Backline — the two Frontlines face off at the center; each side's Backline is its own rear position. Both are abstract zones; any number of characters can share one. Moving costs your action. Neither position gives automatic protection — the Frontline does not shield the Backline from being targeted.

**Range Matrix** — which cards you can legally play, based on where you and your target stand. You are the Attacker row:

| Attacker | Target | Melee | Ranged | Both |
|----------|--------|-------|--------|------|
| Frontline | Frontline | ✓ | ✗ | ✓ |
| Frontline | Backline | ✗ | ✓ | ✓ |
| Backline | Frontline | ✗ | ✓ | ✓ |
| Backline | Backline | ✗ | ✓ | ✓ |

Melee requires both of you in the Frontline. Everything else is Ranged range.

**Rushdown** — an action that drags a Backline *enemy* into the Frontline. Can't target allies. You must be in the Frontline yourself to use it.

**Cover** — an action, Backline only, and the fiction has to justify it (something to actually hide behind). It's **Anchored — Evade**: one the moment you take cover, one more at the start of each of your turns. It ends the instant you attack — meaning a card *you* play as the attacker; a Counter Attack or Thorns doesn't break it, since both happen while you're defending. It also ends if you Collapse, or if anything moves you out of the Backline — Rushdown included, since cover needs the Backline even though Rushdown doesn't break other Anchored effects.

**Confined spaces** — in tight terrain the GM may cap how many fit in a position, or block targeting entirely if something physically blocks the way.

---

## Turn Structure

Draw to your hand size the moment initiative is rolled, then again at the start of every one of your own turns. If your deck runs out, shuffle your discard into a fresh deck first.

Each turn: **one Action, plus one Item Action.**

| Action | What it does |
|--------|--------------|
| Play a Card | Attack with a card from your hand |
| Move Position | Frontline ↔ Backline |
| Use an Item | Activate something equipped or carried |
| Rushdown | Pull a Backline enemy to the Frontline (must be Frontline yourself) |
| Take Cover | Backline only, fiction-justified — Anchored, Evade. Ends when you attack or leave the Backline |
| Interact | Anything noncombat the fiction allows |
| Wait | See below |
| Flee | Attempt to leave the fight — see Fleeing Combat |
| Grapple | Grab, tackle or pin instead of hurting — a contested check |
| Stand Up | Get up off the ground once you're above 0 HP |
| Destroy a Wound | Get rid of 1 Wound from your hand |
| Rest in Place | Get rid of every Exhaust in your hand at once |

Your **Item Action** does exactly what its name says and nothing else. Using an Item is also legal as your regular Action — spend both that way and you use two items in one turn, at the cost of not attacking.

**Wait.** Give up your action on purpose, and in exchange, reinsert your turn token anywhere later in the initiative order — you're standing on the turn marker, so "later" is the only direction available. Land a slot or two out and you act again shortly; land far enough to lap the wheel and you sit out a stretch entirely. There's no cap on how far you can push it, since moving later is always a cost, never a reward. Its main use is coordinating with allies — sliding yourself right after a setup, or right before the ally you're setting up. You can't Wait two turns in a row; the turn after a Wait, you must take a real action.

---

## Initiative & The Wheel

At the start of combat, everyone rolls **1d6 + Soul**. Highest goes first.

**Ties** — higher Soul goes first; still tied between two players, they choose; still tied between a player and an enemy, the player goes first.

Tokens sit clockwise around a wheel in initiative order, whoever went first at 12 o'clock. A turn marker advances to the next token each turn. The wheel always has exactly as many slots as there are combatants — when someone joins or leaves, the wheel gains or closes a slot, and everyone between shifts over one.

**Initiative Shift X** (a card effect) moves a token X slots around the wheel — positive shifts it sooner, negative shifts it later. Full mechanics: `rules/card-glossary.md` (Initiative Shift X) and `rules/initiative-shift-examples.md`.

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

When attack damage lands, it passes through, in order: **redirect** (e.g. Shared Burden) → **volunteer shield** (Protect) → **Armour** (flat reduction) → **Resist / Vulnerable** (one stack of each cancels the other first; otherwise Resist halves, Vulnerable adds 50%, rounded down) → HP.

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

(d10 shows up on a handful of cards as a genuine outlier above this scale — rare, and usually paired with an extra cost or condition.)

Some cards carry a **Special Rule** line instead of — or alongside — an Effect and Defensive Bonus. It overrides normal resolution exactly as printed.

**"Attacker"/"Defender" vs. "Target"** — two different things on card text:
- **Attacker/Defender** means whoever you're resolving *this specific exchange* against. No choice involved.
- **Target** means you genuinely choose — an ally among several, or a specific enemy when more than one is present.

### An Example — STRIKE

```
STRIKE
RED — BODY
Attack: Body + d10
Effect: None
Defensive Bonus: Deal 3 damage to attacker, unpreventable.
Range: Melee
"Sometimes the direct path is the wisest path."
```

- **Name** — STRIKE.
- **Color + Stat** — Red, Body. A Red card beats Green and loses to Blue in RPS, and its damage comes off your Body stat.
- **Attack: Body + d10** — your Body stat plus a d10 roll. The rare outlier die, not a fourth named tier.
- **Effect: None** — nothing happens beyond the damage when you win as the attacker. This is what STRIKE actually trades for that big die: every other d10 card in the game still does something extra — bonus damage under a condition, a reposition, a resource interaction — STRIKE's whole design is spent on the number alone.
- **Defensive Bonus: Deal 3 damage to attacker, unpreventable** — win *or tie* as the defender and you deal a flat 3 back (STRIKE's own Effect is None, so it never cancels the Defensive Bonus on a tie). "Unpreventable" means it skips the Damage Pipeline entirely — Resist, Protect, none of it applies.
- **Range: Melee** — you and your target must both be in the Frontline to play this card.
- **Flavor text** — *"Sometimes the direct path is the wisest path."* Not a rule. Just the world's own read on a card built with nothing to hide.

---

## What It Looks Like

When you play a card, **you choose what it looks like.**

The card tells you the mechanical outcome — the stat, the damage die, the effect. What it doesn't tell you is how your character gets there. That part is yours.

A Body card might be a punch, a shove, the ground shifting underfoot; a Mind card a feint or a command that lands exactly right; a Soul card a ward or a held breath. See `rules/character-creation.md`, Magic Expression, for the full statement of this.

None of it is wrong as long as it fits your character. The cards are a frame. You're the one making it mean something.

You don't have to explain the metaphysics. Neither does your character.

---

## Keywords

Every keyword is defined once, in `rules/card-glossary.md`. Print it and keep it on the table beside this guide — it is meant to be handed to players, and it is the ruling wherever anything disagrees with it.

*Initiative Shift X is the exception, covered above under Initiative & The Wheel — it needs the Wheel to make sense and doesn't read alone.*

---

## Status Cards

Some consequences become cards. A status card can't be played, and it doesn't leave your hand or deck on its own — it has to be managed.

---

## Collapse & Death

Reduced to 0 HP → **Collapse.** You go to the ground, and you are **Down** until you get up. A single attack can't push a standing combatant below 0, but further damage while already Collapsed can. Reach **negative half your Max HP (rounded up)** → death.

While Down you cannot attack, cannot change position, and cannot defend — so attacks against you land automatically. You can still be healed back into the fight, and recover 1d4 HP every 3 in-game hours if left alone.

**Healing does not stand you up.** It ends the Collapse; getting off the ground costs your action on your turn, and you act normally from the turn after that. A revived ally is alive and still a turn away from being useful — which is why catching someone *before* they go down is worth more than picking them up after.

If the whole party goes down, the GM decides the outcome from the enemy's own nature and intent — death is possible, not automatic. Captivity, humiliation, forced retreat, and stranger fates are all real options. The GM can also declare instant death outright when the fiction genuinely demands it (a beheading, a fall into the void) — a rare override, not a default.

---

## Fleeing, Chasing, and Stealth

**Flee (mid-fight)** — an action: **2d10 + Soul vs. DC = 10 + the highest Soul among enemies**, adjusted by the GM for terrain, position, and whether the enemy actually cares. Success ends your participation in the fight (the enemy may give chase — see Chase below). Failure costs the action; you're still there.

**Chase** — only the distance between you is tracked, starting wherever the fiction puts it. Each exchange, a contested roll (Soul is obvious, any stat you can argue for works); the winner moves the distance one step their way. **Reach 4 and you're gone** — they may still try to follow your trail. **Reach 0 and they've caught you:** the chase ends there. They get no free attack for it, but they do act first, and they choose — fight, grapple you with a contested check, or whatever they were chasing you for.

**Stealth & Ambush** — a check against DC = 10 + the highest Soul on the side you're approaching. You roll your own; the GM rolls for creatures. Soul is the obvious stat, but any stat you can argue for and the table agrees to works. Success: the ambusher's first attack auto-hits — no RPS, no defense, and no Evade or Protect, because you can't react to what you didn't see. What you're made of still counts: Armour, Resist, Thorns and Immunity all apply. An ambush makes you easier to hit, not easier to kill. **Your side gets one auto-hit, not one each**, and there's no window for a second before initiative. Then everyone rolls initiative as normal, ambusher included.

**Unguarded** — some creatures and people don't fight until they're fought. They take no turns and play no cards, which leaves you an opening. You get one of two things, never both: **strike**, and one attack lands unblocked (no defense, no reveal — but everything else still applies, Evade and Protect included, since they can see you), or **ready** yourself visibly, which drops Unguarded with no attack. Either way initiative follows. This isn't an ambush and doesn't stack with one: an ambush pays for not being seen and beats Evade and Protect; this beats only the defense card.

In any of these, discarding a card whose name meaningfully fits the action grants **Advantage** (roll 3d10, drop the lowest).

---

## Ongoing & Simultaneous Effects

**Ongoing Effects** stay face-up in front of you after use until their stated condition is met, then discard. Multiple can be active at once unless a card says otherwise.

**Tracking a status — the card is the marker.** When a card gives someone a temporary status, don't discard it. Set it face-up in front of whoever it's affecting, and discard it for real when the effect ends. That card is out of your rotation the whole time, so it isn't coming back on a reshuffle — the status costs you the card, not just the turn.

**Status tokens fill the gaps the card can't.** Take tokens when the card alone can't show the state: when one card hits several combatants (the card stays in front of you, each of them takes a token), when a numbered status is being spent down (the card keeps showing its printed number, the tokens carry what's left), or when nothing was played at all — a creature's passive, an item, the terrain. Tokens never replace the card. A status belongs to whoever it landed on — once it resolves it's theirs, and it stays put even if the person who played the card Collapses or leaves the fight. The effect ends on its own stated condition, and only then does the card go to the discard; you can't take a card back to cancel one early. Full rule: `rules/combat.md`, Ongoing Effects.

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
| Short | 20 minutes | 2d6 + Body HP | All Exhaust (hand, deck, and discard); may destroy 1 Wound from hand, discard, or deck | 3/day, can be chained |
| Long | 7½ hours | Full heal | All Wounds, and all Exhaust (hand, deck, and discard) | Once/day, requires genuine safety |

Either length reshuffles your discard into your deck and refreshes your hand to full.

---

## Equipment

Three slots: **Weapon, Armor, Artifact.** Only what's actually equipped carries a permanent passive effect — everything else about how you look or what you're carrying is free, unrestricted fiction. Carried items (equipped or not) are used via the Interact action, or the Use an Item Action / Item Action in combat. Artifacts are resonant items aligned with a Seat's domain.

Full tier system and the world's item catalog: `rules/equipment.md` and `rules/items.md`.

---

## What You Showed Up With

You choose what your character wears and what they carry. A sword, a bow, a walking stick, a good coat, a set of tools, whatever fits the person you made.

**None of it has stats. None of it has a gold value.** Your starting garb and weapon are not equipment in the mechanical sense — they grant no bonus, occupy no slot, and cannot be sold. Nobody is going to ask you what your sword's damage is. The cards are your damage. The gear is who you are.

**It still matters, constantly.** Not in a fight — out of one. What you happen to be carrying is a standing answer to problems the world puts in front of you, and the GM will take it seriously:

- A sword can dig. It can pry, wedge a door, cut a rope at arm's length, and reach something you'd rather not reach with your hand.
- A bow can shoot out a light across a room you don't want to cross.
- A heavy coat is a rope, a sack, a way to carry something too hot to hold, or the reason the cold doesn't get a check out of you.

So choose it as fiction, then use it as leverage. The character who thought about what they brought will find more doors open than the one who wrote "sword" and stopped thinking about it. That is the whole design: no numbers on it, real consequences from it.

---

## The Oracle (End of Session)

At the close of every session, each player meets the Oracle alone. She speaks in three frames — **Name, Price, Distance** — and you'll hear the GM use those words at the table. She asks you something real and you answer it. She shows you a piece of what growth could look like, and you don't get to keep it — not yet. Then she offers you a genuine choice among a few real options, and whatever you choose becomes a permanent part of your deck.

Growth is never handed over whole. Where this actually happens, and what it's like to sit across from her, is worth meeting for yourself rather than reading about in advance.
