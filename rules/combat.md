# Combat

Combat in Tales Untold is fast, positional, and decisive. Turns are short. Mistakes compound. The goal is not to outlast — it's to outread.

---

## Stealth & Ambush

To approach unseen before combat, make a Soul check: DC = 10 + the highest Soul stat on the side being approached. Creatures ambush the same way — when the ambusher is an NPC or creature, the GM makes its Soul check.

**On success:** The ambusher's first attack auto-hits — no RPS, no defense. After it resolves, roll initiative for everyone including the ambusher. They take their place in order normally. Combat continues.

**On failure:** Roll initiative. No advantage.

---

## Chase

When a character flees and the pursuer gives chase, set up a two-marker track instead of repeating checks.

**Set up:** Estimate how many exchanges of movement currently separate them — that's the fleeing party's starting position. The pursuer starts at 0. Standard track is 5 steps past the fleeing party's start; extend it if the head start is larger.

*Example: right on your heels = both at 0, track runs to 5. A full corridor away = fleeing party at 3, pursuer at 0, track runs to 8.*

**Each exchange (6 seconds):** Contested Soul roll (2d10 + Soul). The winner advances their marker 1 step. Discard a card whose name fits the action → Advantage.

**Caught** — The pursuer's marker reaches the fleeing party's marker.

**Escaped** — The fleeing party's marker reaches the end of the track. They've maintained enough distance to lose sight. The pursuer may attempt to follow the trail afterward (Observe check, DC set by GM based on terrain and time elapsed).

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

---

## Turn Structure

When initiative is rolled, every combatant draws to their maximum hand size — nobody enters the wheel empty-handed.

At the start of your turn, draw until you reach your maximum hand size. If your deck is empty, shuffle your discard pile into a new deck before drawing.

On your turn, you may take **one action:**

| Action | Description |
|--------|-------------|
| Play a Card | Make an attack using a card from your hand |
| Move Position | Shift between Frontline and Backline |
| Use an Item | Activate an equipped or held item |
| Rushdown | Move a Backline enemy to the Frontline. You must be in the Frontline to use this action. |
| Take Cover | Backline only; the fiction must justify it. Gain Evade until you attack. See Positioning → Cover. |
| Interact | Any noncombat action — talk, examine, activate, manipulate, or anything the fiction allows |
| Wait | Take no action; instead move yourself later in the order to a position you choose (Initiative Shift −X). Trades this turn for exact positioning. See below. Counts as "waiting." |
| Flee | Attempt to exit combat — 2d10 + Soul vs DC 10 + highest enemy Soul, GM-adjusted. See Fleeing Combat above. |

**Waiting.** To Wait is to give up your action on purpose. In exchange you reposition: choose how many seats **X** to move *later* in the order (an Initiative Shift of **−X**), and you act normally when the marker reaches your new position. You are standing on the turn marker, so you can only move later — you cannot act sooner than the turn you are already in — which is the only direction Wait ever needs.

The trade is **an action for a position.** You take one fewer action this fight — that is the whole cost; your turn count simply drops relative to everyone else — and in return you land exactly where you want in the order. Move a seat or two and you act again shortly, later this cycle. Move X far enough to **lap the wheel** and the marker passes you once per full lap before honoring your seat — a way to opt out of the tempo entirely for a stretch. There is no cap on X, because moving later is always a cost, never a reward — so Wait as little or as much as you like.

Waiting sets your count to your new seat's natural arrival: the marker honors your seat the first time it reaches it. You are never passed over for having Waited — you never spent this lap's action; the forfeited action *was* the payment. (This is the difference between Waiting there and being *shifted* there: a shifted combatant's count is written by the shift, and the marker enforces it.)

Its main use is **team coordination** — chaining turns into the right sequence. Move yourself to act right after an ally's setup, or right before the ally you are setting up, so a combo resolves without an enemy acting in between. The reposition persists, so one Wait fixes a combo cadence for the rest of the fight. Waiting and "passing" are the same choice, and it is what effects that reward holding back — such as Patience — key off.

---

## Attack Resolution

1. Attacker plays 1 card, face down — committed, not yet public.
2. Defender may choose 1 card to defend with, face down — **blind.** The defender chooses without seeing the attacker's card, deciding from public information only (revealed-color history, position). This is a prediction, not a reaction. **The chosen card must satisfy its own Range requirement for the current positions, exactly as if the defender were attacking the attacker** — a Melee card cannot defend unless both combatants are Frontline; Ranged and Both are unaffected. A defender with no card in hand that meets the requirement has no legal defense against this attack.
3. If the defender cannot or chooses not to defend, the attacker wins automatically.
4. Both cards reveal simultaneously — only now do they become public and move to their owners' discard piles — and resolve using Rock-Paper-Scissors:

```
Blue (Mind)   beats  Red   (Body)
Red  (Body)   beats  Green (Soul)
Green (Soul)  beats  Blue  (Mind)
```

**Attacker wins** → deal damage + apply the card's Effect  
**Defender wins** → no damage + defender triggers Defensive Bonus  
**Tie** → no damage. Attacker's Effect still triggers, then Defender's Defensive Bonus triggers. If the attacker's Effect cancels the Defensive Bonus, the Defensive Bonus does not trigger.

An Effect that only *adds to or amplifies this attack's damage* has nothing to act on when the attack deals no damage — so it does nothing on a tie (or any miss). Exploding dice, "+2 damage this attack," "deal +2 for each Wound," and the like all need a landed hit. Effects that do something independent of damage — apply a status, shift a stat, move a card — still trigger normally.

---

## Damage Pipeline

When *attack* damage is dealt, it passes through this pipeline in fixed order:

**redirect** (Shared Burden) → **volunteer shield** (Fortress, team play) → **Armour** (flat reduction) → **Resist** (halve, one stack spent per hit) → **damage floor** (Equal Footing) → apply to HP.

A single attack cannot push a *standing* combatant below 0 HP (clamped to 0 = Collapse; see Collapse & Death below).

**Unpreventable damage bypasses this pipeline entirely** — not as an exception carved out of it, but because the pipeline only ever governed *attack* damage in the first place. Thorns, status damage, and HP costs are not attacks, so none of the steps above apply: they cannot be reduced (Armour/Resist), reassigned (Shared Burden/Fortress), or capped (Equal Footing). They land on the original target, in full. Thorns specifically retaliates against a melee attacker after the hit lands, and is itself unpreventable.

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

Moves a Backline **enemy** to the Frontline. Cannot target allies. The user must be in the Frontline. See the action table above.

### Interact & Position

Position determines what's within reach. A character can only interact with objects that the fiction places near them. The GM calls it based on where things are — a lever at the center of the room favors Frontline characters, a mechanism on the back wall favors Backline. Neither position has a blanket advantage; the environment decides.

### Cover

Taking cover is an action. You must be in the Backline, and the fiction must justify it — there must be something to take cover behind.

While in cover, you gain **Evade** (`rules/card-glossary.md`). Making an attack drops cover immediately.

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

---

## Collapse & Death

If an attack reduces you to **0 HP**, you Collapse.

- A single attack cannot push you below 0.
- Additional damage taken while Collapsed *can* reduce you below 0.
- If you reach **negative half your Max HP (rounded up)**, you die.

### While Collapsed

- You cannot act.
- You cannot defend.
- You are automatically hit by any attack targeting you.
- You may be healed back into combat.
- Every **3 in-game hours** spent Collapsed, recover **1d4 HP**.

### If the Entire Party Collapses

The enemy determines the outcome based on their intent, nature, and what the fiction demands. Death is possible — but it is not automatic. Captivity, humiliation, forced retreat, and stranger fates are all on the table.

The world does not guarantee fairness. It only guarantees consequence.

### GM Override

The GM may declare instant death at any point if the fiction demands it — a beheading, a fall into the void, a creature that does not leave survivors. The collapse rules exist to create dramatic space, not to protect players from a world that can genuinely kill them. Use this power with intention, not frequency.
