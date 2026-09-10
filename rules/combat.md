# Combat

Combat in Tales Untold is fast, positional, and decisive. Turns are short. Mistakes compound. The goal is not to outlast — it's to outread.

*(The Three Cuts run underneath this, for anyone who wants the deeper read: playing a card is Name, spending it is Price, holding a position is Distance — `experimental/the-summons.md`.)*

---

## Core Combat Philosophy

Three things decide a fight, and a build's stance toward all three, together, is what actually gets read:

- **Balance between the three stats** — Mind, Body, and Soul (`rules/character-creation.md`). Every color answers another: red overwhelms green, green outlasts blue, blue unmakes red. No stat is strongest on its own; a deck built around one alone is legible, countered risk, not a winning strategy. Mechanically, this is what **RPS** means throughout this document — the color triangle, resolved through stat balance.
- **Control distance.** Frontline and Backline. Some things only work up close; some only work at range. Moving between them costs the action you'd have spent doing something else. Shorthand: **Position.**
- **Act before your opponent does.** The initiative wheel, not a fixed turn order — shifting where you sit in it is one of the few ways to act again before the table would otherwise expect you to. Shorthand: **Initiative.**

**RPS / Initiative / Position** is the shorthand used throughout this ruleset for the three above. **A build that ignores one entirely takes on real, legible risk — fine, as long as it's intentional, not accidental.** Most real builds carry at least one tool against at least one of the three; a card or engine that looks unanswerable in a given test needs to be checked against whether that specific build had a tool for the pillar it's actually being asked to answer, before it's read as overtuned rather than matchup-specific.

**Default to telegraphed effects over hidden ones.** A hidden delayed payoff is just a surprise; a visible one is a real bet the opponent gets a turn to answer it. When a new mechanic could go either way on visibility, give the other side a chance to react — don't default to concealment for its own sake.

---

## Stealth & Ambush

To approach unseen before combat, make a check: DC = 10 + the highest Soul stat on the enemy side. Players perceive an ambush the same way — DC = 10 + the highest Soul stat on the enemy side.

**On success:** The ambusher's first attack auto-hits — no RPS, no defense. After it resolves, roll initiative for everyone involved, including the ambusher. They take their place in order normally. Combat begins.

**On failure:** Roll initiative. No advantage.

---

## Chase

When a character flees and the pursuer gives chase, set up a two-marker track instead of repeating checks.

**Set up:** Estimate how many exchanges of movement currently separate them — that's the fleeing party's starting position. The pursuer starts at 0. Standard track is 5 steps past the fleeing party's start; extend it if the head start is larger.

*Example: right on your heels = both at 0, track runs to 5. A full corridor away = fleeing party at 3, pursuer at 0, track runs to 8.*

**Each exchange (6 seconds):** Contested Soul roll (2d10 + Soul). The winner advances their marker 1 step. Discard a card whose name fits the action → Advantage.

**Caught** — The pursuer's marker reaches the fleeing party's marker.

**Escaped** — The fleeing party's marker reaches the end of the track. They've maintained enough distance to lose sight. The pursuer may attempt to follow the trail afterward (Reason check, DC set by GM based on terrain and time elapsed).

---

## Fleeing Combat

Exiting combat mid-fight is an action: **2d10 + Soul vs DC = 10 + the highest Soul stat among enemy combatants** — the ambush formula, run from the other side. Soul gets you into fights unseen and gets you out of them alive.

The formula is the baseline, not the answer. The GM adjusts it for the factors it can't see:

- **Terrain** — open road vs briar walls vs a corridor with one door
- **What stands between you and out** — an enemy in your path is not an abstraction
- **Position** — Backline is closer to gone than Frontline
- **Whether the enemy cares** — a territorial creature that just wants you off its ground may make the check trivial, or unnecessary; a hunter in its own territory pushes it up

**Success:** you leave the combat area and your participation ends. If the enemy gives chase, that's the Chase system above.

**Failure:** the action is spent and you're still in the fight, exactly where everyone can see you.

Enemies don't roll to flee — enemy disengagement is a GM call made from behavior, not a check.

---

## Initiative

At the start of combat, each participant rolls:

**1d6 + Soul**

Turn order resolves highest to lowest.

**Ties:**
- Higher Soul goes first.
- If still tied between players, they choose order among themselves.
- If still tied between a player and an enemy, the player goes first.

**The Wheel.** Tokens are placed clockwise around the wheel in initiative order — whoever goes first sits at 12 o'clock. A turn marker starts at 12 o'clock. Each turn, the marker moves to the next token in line.

The wheel always has exactly as many slots as there are combatants — no empty slots. When a token shifts, each token it passes through slides over one slot toward the gap the moving token leaves behind.

**Joining and leaving.** A summoned combatant's token enters the wheel directly after the token of whoever summoned it. A GM-introduced combatant enters when the fiction calls for it — usually at the end of a full lap. Either way, the wheel gains a slot. A combatant who leaves the fight entirely removes their slot, and the wheel closes around it.

---

## Turn Structure

When initiative is rolled, every combatant draws to their maximum hand size — nobody enters the wheel empty-handed.

At the start of your turn, draw until you reach your maximum hand size. If your deck is empty, shuffle your discard pile into a new deck before drawing.

On your turn, you may take one Action, plus one free action if you have one available (see below).

| Action | Description |
|--------|-------------|
| Play a Card | Make an attack using a card from your hand |
| Move Position | Shift between Frontline and Backline — or, if you're already Frontline, close the distance on a Backline enemy yourself instead (Rushdown: you move to them, not the reverse). See Positioning → Rushdown. |
| Use an Item | Activate an equipped or held item, or use a consumable |
| Take Cover | Backline only; the fiction must justify it. Gain Cover Evade — a dodge roll that persists instead of being spent. See Positioning → Cover. |
| Interact | Any noncombat action — talk, examine, activate, manipulate, or anything the fiction allows |
| Flee | Attempt to exit combat — 2d10 + Soul vs DC 10 + highest enemy Soul, GM-adjusted. See Fleeing Combat above. |

**Free Actions.** Once per turn, on top of your Action above, you get one free action — it costs nothing from your turn, so you still take your normal Action as well. Spending a banked Quick to Move Position (Rushdown included), activating a piece of your own gear (turning something on, and similar minor personal gestures — not the world around you; that's still Interact), and eating or drinking all count. Capped at one per turn regardless of how many you'd otherwise have available — a second banked Quick just waits for next turn.

**Actually using a consumable or piece of gear for its mechanical effect is never free — that's Use an Item, above, and costs your Action.** Kevin throwing an incendiary orange is Use an Item: the throw's whole point is the effect it produces, not a minor gesture.

---

## Reading a Card

Every card carries: **Name / Color + Stat / Attack (Stat + die) / Effect / Defense Effect / Range / Flavor text.**

The die tells you the card's philosophy:

| Die | Personality |
|-----|-------------|
| d8 | Raw power — high ceiling, less control |
| d6 | Utility — moderate damage, strong effects |
| d4 | Precision — low damage, high control and information |

(d10 shows up on a handful of cards as a genuine outlier above this scale — rare, and usually paired with an extra cost or condition.)

Some cards carry a **Special Rule** line instead of — or alongside — an Effect and a Defense Effect. It overrides normal resolution exactly as printed.

**"Attacker"/"Defender" vs. "Target"** — two different things on card text:
- **Attacker/Defender** means whoever you're resolving *this specific exchange* against. No choice involved.
- **Target** means you genuinely choose — an ally among several, or a specific enemy when more than one is present.

### An Example — STRIKE

```
STRIKE
RED — BODY
Attack: Body + d10
Effect: None
Defense Effect: Deal 3 damage to attacker, unpreventable.
Range: Melee
"Sometimes the direct path is the wisest path."
```

- **Name** — STRIKE.
- **Color + Stat** — Red, Body. A Red card beats Green and loses to Blue in RPS, and its damage comes off your Body stat.
- **Attack: Body + d10** — your Body stat plus a d10 roll. The fourth tier, and the rarest: Red alone holds it, on cards that pay for it somewhere else on the card (STRIKE has no Effect at all, REPAY costs 3 HP up front, OVERCOMMIT hands you Vulnerable for the privilege).
- **Effect: None** — nothing happens beyond the damage when you win as the attacker. This is what STRIKE actually trades for that big die: every other d10 card in the game still does something extra — bonus damage under a condition, a reposition, a resource interaction — STRIKE's whole design is spent on the number alone.
- **Defense Effect: Deal 3 damage to attacker, unpreventable** — win *or tie* as the defender and you deal a flat 3 back (STRIKE's own Effect is None, so it never cancels the Defense Effect on a tie). "Unpreventable" means it skips the Damage Pipeline entirely — Resist, Protect, none of it applies.
- **Range: Melee** — you and your target must both be in the Frontline to play this card.
- **Flavor text** — *"Sometimes the direct path is the wisest path."* Not a rule. Just the world's own read on a card built with nothing to hide.

Full canonical wording for every keyword and status card: `rules/card-glossary.md`.

A Passive resolves exactly like a card from hand once concealment is settled — what it is, its fixed shape, and how it's concealed beforehand: `rules/character-creation.md`, Passives.

---

## Attack Resolution

1. Attacker plays 1 card, face down — committed, not yet public.
2. Defender may choose 1 card to defend with, face down — **The chosen card must satisfy its own Range requirement for the current positions, exactly as if the defender were attacking the attacker** — a Melee card cannot defend unless both combatants are Frontline; Ranged and Both are unaffected.
3. **Blind and Evade resolve now, before either card is revealed.** Both cards are already committed at this point. Every check that applies actually rolls — being attacked is what triggers a defender's Evade and Blind, not whether the attack would land, so a stack gets spent, or a defender's own block-miss gets rolled, even when it turns out not to have mattered:
   - **Attacker's Blind:** roll 1d2 if the attacker holds it.
   - **Defender's Evade:** roll 1d2 if the defender holds it.
   - **Defender's Blind:** roll 1d2 if the defender holds it and is actually defending.

   **Resolving the rolls, in this order:**
   1. **Defender's Evade succeeds** → the defender auto-wins the resolution (step 5's Defender wins outcome). A clean dodge — nothing else in this step changes that.
   2. **Otherwise, attacker's Blind misses *and* defender's Blind misses** → **Mutual Miss** (see step 5): the attack failed and the block attempted against it also failed. Not a win for either side, and not a Tie — a Tie still needs two cards that actually did something; this is two that didn't.
   3. **Otherwise, attacker's Blind misses alone** (the defender's own block, if any, didn't also miss) → the defender auto-wins the resolution.
   4. **Otherwise, defender's Blind misses alone** (the attacker's own attack, above, didn't also miss) → the attacker wins automatically, exactly like no legal defense, below.
   5. **Otherwise** (none of the above fired) → proceed to the reveal.

**A mistaken illegal pick** (wrong Range for the current positions) is fixed differently depending on when it's caught. Caught before the attacker's card is known: swap freely, no penalty — nothing about the attacker's choice has leaked, so the pick is still genuinely blind. Caught only after the attacker's card is already revealed: too late for a free redo, since that knowledge can't be un-known and picking again now would mean picking with information blind defense is supposed to deny you. Resolve it as no legal defense — but the illegal card itself returns to hand, not the discard pile, since it was never actually, legally played. The attacker still learns what it was (a real cost, already paid), but the mistake doesn't also cost a card on top of the auto-loss.
4. If the defender cannot or chooses not to defend, the attacker wins automatically — same outcome as a defender Blind-miss, above.
5. Both cards reveal simultaneously — only now do they become public and move to their owners' discard piles — and resolve using Rock-Paper-Scissors:

```
Blue (Mind)   beats  Red   (Body)
Red  (Body)   beats  Green (Soul)
Green (Soul)  beats  Blue  (Mind)
```

**Attacker wins** → deal damage, then apply the card's Effect  
**Defender wins** → no damage + defender triggers Defense Effect  
**Tie** → no damage. Attacker's Effect still triggers, then Defender's Defense Effect triggers. If the attacker's Effect cancels the Defense Effect, the Defense Effect does not trigger.  
**Mutual Miss** → no damage, no Effect, no Defense Effect. Both cards are still discarded as normal — they were played, they just both failed. Only reachable via the attacker's Blind and the defender's Blind both missing in the same exchange (step 3, above); it never comes up during a normal reveal.

An Effect that only *adds to or amplifies this attack's damage* has nothing to act on when the attack deals no damage — so it does nothing on a tie (or any miss). Exploding dice, "+2 damage this attack," "deal +2 for each Wound," and the like all need a landed hit. Effects that do something independent of attack damage — apply a status, shift a stat, move a card — still trigger normally.

A standing bonus or penalty like "your next attack deals +X" is consumed by a miss.

---

## Damage Pipeline

The base roll is **Stat + die, with Deadly/Weak folded in** — a Deadly stack adds a d6, a Weak stack subtracts one, and one of each cancels before either applies. That total is what enters the pipeline below.

When *attack* damage is dealt, it passes through this pipeline in fixed order:

**reassignment** (the damage lands on someone else instead, in full, before anything reduces it — Protect volunteers you for an ally's hit; TURN sends an attack you're defending against at a target of your choice) → **Immunity** (held by whoever is actually receiving the damage — reduces it to 0, leaving the rest of the pipeline nothing to act on) → **Armour** (flat reduction) → **Resist / Vulnerable** (one stack of each cancels the other first; otherwise Resist halves or Vulnerable multiplies by 1.5, rounded down) → apply to HP.

A single attack cannot push a *standing* combatant below 0 HP (clamped to 0 = Collapse; see Collapse & Death below).

**Unpreventable damage bypasses this pipeline entirely** — not as an exception carved out of it, but because the pipeline only ever governed *attack* damage in the first place. Thorns, status damage, and HP costs are not attacks, so none of the steps above apply: they cannot be reduced (Resist) or reassigned (Protect). They land on the original target, in full. Thorns specifically retaliates against a melee attacker after the hit lands, and is itself unpreventable.

---

## Range

Every card lists a range requirement. If you don't meet it, you cannot play that card as an attack this turn.

| Term | Meaning |
|------|---------|
| Melee | You and the target must be in the Frontline |
| Ranged | Works only while not in Melee range with the target |
| Both | Either position is valid |

---

## Positioning

Every combatant occupies one of two positions: **Frontline** or **Backline**.

Frontline isn't a fixed place on the field — it's wherever two sides have actually closed the distance and are fighting face to face. Whoever's caught up in that is Frontline, on both sides of it, for as long as it's happening there; that contact point is where Melee range exists. Backline is everyone else: still in the fight, just not closed with anyone yet. Nothing pins the Frontline to one spot — it's wherever the fighting actually is, and it moves when the fighting does.

Both positions are abstract zones, and any number of characters may occupy either one. What occupying the same position *means* depends on whose side they're on.

**Allies in the same position are together** — close enough to hand something over, step in front of each other, pass a drink. **Opponents in the same position are only together in the Frontline.** Two enemies both in the Backline are on opposite sides of the field, each simply not closed with anyone; the Frontline is the one position where opposing sides are actually in contact, which is why it is the one position Melee works from. "Both in the Backline" is not proximity — it is two people who have each disengaged.

This is why a card can hand a drink to an ally in your position and a Melee card cannot reach an enemy in yours: the ally is beside you, the enemy is across the field.

Moving costs your action for the turn. Position provides no automatic protection. The Frontline does not shield the Backline from being targeted.

### Range Matrix

Position determines which cards can be played. Use this table to resolve any targeting question:

| Attacker | Target | Melee | Ranged | Both |
|----------|--------|-------|--------|------|
| Frontline | Frontline | ✓ | ✗ | ✓ |
| Frontline | Backline | ✗ | ✓ | ✓ |
| Backline | Frontline | ✗ | ✓ | ✓ |
| Backline | Backline | ✗ | ✓ | ✓ |

Melee requires both characters to be in the Frontline. Any other combination is not Melee range.

### Rushdown

The Move Position action's other shape, not a separate action of its own: closing the distance on a Backline **enemy** yourself, instead of shifting between Frontline and Backline — not moving them, moving toward them. Wherever you land, that's Frontline now, for both of you: the fighting bent to include them, not a teleport. Cannot target allies. You must already be in the Frontline yourself — Rushdown extends a fight you're already inside, not a first step into one from nothing. See Move Position in the action table, above.

### Interact & Position

Position determines what's within reach. A character can only interact with objects that the fiction places near them. The GM calls it based on where things are — a lever at the center of the room favors Frontline characters, a mechanism on the back wall favors Backline. Neither position has a blanket advantage; the environment decides.

### Cover

Taking cover is an action. You must be in the Backline, and the fiction must justify it — there must be something to take cover behind.

While in cover you have **Cover Evade** — its own thing, not the Evade keyword, though it rolls identically. The same 1d2 dodge at the same point in Attack Resolution (step 3), succeeding the same way, with the one difference that matters: **it is not a stack and is never spent.** Every attack against you rolls it, however many come, for as long as you hold cover.

Cover ends the instant you attack. It also ends if you leave the Backline, or if the fiction takes the cover away — a wall comes down, the thing you were behind moves. Cover Evade goes with it.

**Cover Evade and held Evade stacks are separate.** Only one dodge roll happens per attack, so if you have both, the cover roll is the one that happens and your stacks stay banked for after cover breaks. That is the point of paying an Action for cover rather than a card: the stacks you were holding survive it.

### Confined Spaces

In tight environments (narrow tunnels, low passages, cramped rooms), the GM may limit how many characters fit in either position. If a creature physically blocks a passage, characters behind them cannot be targeted unless the fiction clearly allows it (e.g., ranged attack with line of sight). Rushdown in confined spaces may represent forcing an enemy into unstable terrain rather than a clean positional shift.

---

## Ongoing Effects

Some cards produce **Ongoing Effects.** These cards remain face up in front of the player after use. The effect persists until its stated condition is met, at which point the card is discarded.

Multiple ongoing effects can be active simultaneously unless a card specifies otherwise.

---

## Simultaneous Effects

When two or more effects would resolve at the same moment — several "start of your turn" triggers, two tokens landing at once — the **controller of those effects chooses the order** they resolve in. If the simultaneous effects have different controllers, the player whose turn it is decides the order.

Order can matter: two ticks that commute end at the same number, but a heal that arrives after a lethal tick arrives too late. If two effects would each reduce a combatant to death at the same instant and neither is clearly first, the exchange is a **mutual result** — resolve it as a tie.

**This does not apply to Attack Resolution.** An attacker's Effect and a defender's Defense Effect are not a controller's choice to order — Attack Resolution (above) already fixes it: Effect before Defense Effect, always, on every tie. Nobody, including the attacker, chooses that order.

---

## You Are Not Your Own Ally

Card effects that say "allies" or "enemies" never include yourself. You can't target yourself with an ally effect, and you can't accidentally trigger an enemy effect on yourself. "All allies in your position" means everyone else sharing it — not you. The only exception is a card that explicitly names *yourself* as the target.

---

## Collapse & Death

If an attack reduces you to **0 HP**, you Collapse.

- A single attack cannot push you below 0.
- Additional damage taken while Collapsed *can* reduce you below 0.
- If you reach **negative half your Max HP (rounded up)**, you die.

You are on the ground. That is literal, and it stays true until you spend an action getting up.

### While Down

You are Down from the moment you Collapse until you stand. Healing above 0 HP ends the Collapse — it does not stand you up.

**Down is not unconscious.** You are on the ground and finished as an attacker, but you are awake, aware, and still covering yourself.

- You cannot attack.
- You cannot change position.
- **You defend normally.** Choose a card face down and resolve the exchange exactly as a standing combatant would, Defense Effect and all. Attack Resolution runs against you in full — including the attacker's Blind check — so an attack on a Down character can still miss.
- **You keep your one free action each turn** (Free Actions, above). Eating, drinking, and activating your own gear all work from the ground. Moving does not: a banked Quick has no Move Position to spend itself on while you're Down, so it simply holds.
- Your Action is unavailable while you're Down, with one exception — standing up, once you have the HP for it (Standing Up, below).
- You may be healed back into combat.
- Every **3 in-game hours** spent Collapsed, recover **1d4 HP**.

### Standing Up

Once you are above 0 HP, **standing costs your action** on your turn. You are Down until you spend it, and you act normally from your next turn onward.

A revived ally is not immediately back on offense. They were covering themselves the whole time they were down, but they are still on the ground and one turn away from being useful — which is the real cost of going down, and the reason healing someone before they Collapse is worth more than healing them after.

### If the Entire Party Collapses

The enemy determines the outcome based on their intent, nature, and what the fiction demands. Death is possible — but it is not automatic. Captivity, humiliation, forced retreat, and stranger fates are all on the table.

The world does not guarantee fairness. It only guarantees consequence.

### GM Override

The GM may declare instant death at any point if the fiction demands it — a beheading, a fall into the void, a creature that does not leave survivors. The collapse rules exist to create dramatic space, not to protect players from a world that can genuinely kill them. Use this power with intention, not frequency.
