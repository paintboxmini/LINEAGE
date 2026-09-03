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

On your turn, you may take one Action

| Action | Description |
|--------|-------------|
| Play a Card | Make an attack using a card from your hand |
| Move Position | Shift between Frontline and Backline. |
| Use an Item | Activate an equipped or held item 
| Rushdown | A Backline enemy is repositioned to the Frontline. You must be in the Frontline to use this action. This doesn't count as the enemy moving, it counts as you moving toward it; shifting the line of engagement. |
| Take Cover | Backline only; the fiction must justify it. Gain Evade until you attack. See Positioning → Cover. |
| Interact | Any noncombat action — talk, examine, activate, manipulate, or anything the fiction allows |
| Flee | Attempt to exit combat — 2d10 + Soul vs DC 10 + highest enemy Soul, GM-adjusted. See Fleeing Combat above. |

## Reading a Card

Every card carries: **Name / Color + Stat / Attack (Stat + die) / Effect / Defensive Bonus / Range / Flavor text.**

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

Full canonical wording for every keyword and status card: `rules/card-glossary.md`.

A Passive resolves exactly like a card from hand once concealment is settled — what it is, its fixed shape, and how it's concealed beforehand: `rules/character-creation.md`, Passives.

---

## Attack Resolution

1. Attacker plays 1 card, face down — committed, not yet public.
2. Defender may choose 1 card to defend with, face down — **The chosen card must satisfy its own Range requirement for the current positions, exactly as if the defender were attacking the attacker** — a Melee card cannot defend unless both combatants are Frontline; Ranged and Both are unaffected.
3. **Blind, then Evade, resolve next** — Blind checks the attacker's own stack; Blind and Evade checks the defender's.

**A mistaken illegal pick** (wrong Range for the current positions) is fixed differently depending on when it's caught. Caught before the attacker's card is known: swap freely, no penalty — nothing about the attacker's choice has leaked, so the pick is still genuinely blind. Caught only after the attacker's card is already revealed: too late for a free redo, since that knowledge can't be un-known and picking again now would mean picking with information blind defense is supposed to deny you. Resolve it as no legal defense — but the illegal card itself returns to hand, not the discard pile, since it was never actually, legally played. The attacker still learns what it was (a real cost, already paid), but the mistake doesn't also cost a card on top of the auto-loss.
4. If the defender cannot or chooses not to defend, the attacker wins automatically.
5. Both cards reveal simultaneously — only now do they become public and move to their owners' discard piles — and resolve using Rock-Paper-Scissors:

```
Blue (Mind)   beats  Red   (Body)
Red  (Body)   beats  Green (Soul)
Green (Soul)  beats  Blue  (Mind)
```

**Attacker wins** → deal damage, then apply the card's Effect  
**Defender wins** → no damage + defender triggers Defense Effect  
**Tie** → no damage. Attacker's Effect still triggers, then Defender's Defense Effect triggers. If the attacker's Effect cancels the Defense Effect, the Defense Effect does not trigger.

An Effect that only *adds to or amplifies this attack's damage* has nothing to act on when the attack deals no damage — so it does nothing on a tie (or any miss). Exploding dice, "+2 damage this attack," "deal +2 for each Wound," and the like all need a landed hit. Effects that do something independent of attack damage — apply a status, shift a stat, move a card — still trigger normally.

A standing bonus or penalty like "your next attack deals +X" is consumed by a miss.

## Damage Pipeline

The base roll is **Stat + die, with Deadly/Weak folded in** — a Deadly stack adds a d6, a Weak stack subtracts one, and one of each cancels before either applies. That total is what enters the pipeline below.

When *attack* damage is dealt, it passes through this pipeline in fixed order:

**redirect** (Shared Burden) → **volunteer shield** (Protect, team play) → **Armour** (flat reduction) → **Resist / Vulnerable** (one stack of each cancels the other first; otherwise Resist halves or Vulnerable multiplies by 1.5, rounded down) → apply to HP.

A single attack cannot push a *standing* combatant below 0 HP (clamped to 0 = Collapse; see Collapse & Death below).

**Unpreventable damage bypasses this pipeline entirely** — not as an exception carved out of it, but because the pipeline only ever governed *attack* damage in the first place. Thorns, status damage, and HP costs are not attacks, so none of the steps above apply: they cannot be reduced (Resist) or reassigned (Shared Burden/Protect). They land on the original target, in full. Thorns specifically retaliates against a melee attacker after the hit lands, and is itself unpreventable.

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

Each side has its own Frontline and Backline. The two Frontlines face each other at the center of combat — that contact point is where Melee range exists. Each side's Backline is their own rear position, on the opposite end of the field from the enemy's Backline.

Both positions are abstract zones — any number of characters may share either position. Moving costs your action for the turn. Position provides no automatic protection. The Frontline does not shield the Backline from being targeted.

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

Repositions a Backline **enemy** to the Frontline. Cannot target allies. The user must be in the Frontline. See the action table above.

### Interact & Position

Position determines what's within reach. A character can only interact with objects that the fiction places near them. The GM calls it based on where things are — a lever at the center of the room favors Frontline characters, a mechanism on the back wall favors Backline. Neither position has a blanket advantage; the environment decides.

### Cover

Taking cover is an action. You must be in the Backline, and the fiction must justify it — there must be something to take cover behind.

While in cover, you gain **Evade**. Making an attack drops cover immediately.

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

- You cannot attack.
- You cannot defend, so any attack targeting you lands automatically.
- You cannot change position.
- You may be healed back into combat.
- Every **3 in-game hours** spent Collapsed, recover **1d4 HP**.

### Standing Up

Once you are above 0 HP, **standing costs your action** on your turn. You are Down until you spend it, and you act normally from your next turn onward.

A revived ally is not immediately back in the fight. They are alive, on the ground, and one turn away from being useful — which is the real cost of going down, and the reason healing someone before they Collapse is worth more than healing them after.

### If the Entire Party Collapses

The enemy determines the outcome based on their intent, nature, and what the fiction demands. Death is possible — but it is not automatic. Captivity, humiliation, forced retreat, and stranger fates are all on the table.

The world does not guarantee fairness. It only guarantees consequence.

### GM Override

The GM may declare instant death at any point if the fiction demands it — a beheading, a fall into the void, a creature that does not leave survivors. The collapse rules exist to create dramatic space, not to protect players from a world that can genuinely kill them. Use this power with intention, not frequency.
