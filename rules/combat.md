# Combat

Combat in Tales Untold is fast, positional, and decisive. Turns are short. Mistakes compound. The goal is not to outlast — it's to outread.

---

## Stealth & Ambush

To approach unseen before combat, make a Soul check: DC = 10 + the highest Soul stat among enemy combatants. The GM rolls for that creature.

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

There are no rounds. Initiative is a continuous wheel — once the last position has acted, the order cycles back to 1st and keeps going. Card effects referencing timing anchor to a combatant's own next turn, not a table-wide round.

Card effects cannot modify initiative unless the card explicitly states otherwise. See **Initiative Shift X** in `rules/card-glossary.md`.

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
| Interact | Any noncombat action — talk, examine, activate, manipulate, or anything the fiction allows |
| Flee | Attempt to exit combat — 2d10 + Soul vs DC 10 + highest enemy Soul, GM-adjusted. See Fleeing Combat above. |

---

## Attack Resolution

1. Attacker plays and discards 1 card.
2. Defender may reveal and discard 1 card to defend.
3. If the defender cannot or chooses not to defend, the attacker wins automatically.
4. If both reveal cards simultaneously, resolve using Rock-Paper-Scissors:

```
Blue (Mind)   beats  Red   (Body)
Red  (Body)   beats  Green (Soul)
Green (Soul)  beats  Blue  (Mind)
```

**Attacker wins** → deal damage + apply the card's Effect  
**Defender wins** → no damage + defender triggers Defensive Bonus  
**Tie** → no damage. Attacker's Effect still triggers, then Defender's Defensive Bonus triggers. If the attacker's Effect cancels the Defensive Bonus, the Defensive Bonus does not trigger.

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

### Confined Spaces

In tight environments (narrow tunnels, low passages, cramped rooms), the GM may limit how many characters fit in either position. If a creature physically blocks a passage, characters behind them cannot be targeted unless the fiction clearly allows it (e.g., ranged attack with line of sight). Rushdown in confined spaces may represent forcing an enemy into unstable terrain rather than a clean positional shift.

---

## Ongoing Effects

Some cards produce **Ongoing Effects.** These cards remain face up in front of the player after use. The effect persists until its stated condition is met, at which point the card is discarded.

Multiple ongoing effects can be active simultaneously unless a card specifies otherwise.

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
