# Combat

Combat in Tales Untold is fast, positional, and decisive. Turns are short. Mistakes compound. The goal is not to outlast — it's to outread.

*(The Three Cuts run underneath this, for anyone who wants the deeper read: playing a card is Name, spending it is Price, holding a position is Distance — `rules/the-summons.md`.)*

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

To approach unseen before combat, make a check against **DC = 10 + the highest Soul on the side being approached**. Players attempting an ambush roll for themselves; the GM rolls for an ambushing creature or NPC. Soul is the obvious stat and not the required one — any stat someone can argue for and the table agrees to works, same as every check (`rules/out-of-combat.md`).

**On success:** the ambusher's first attack **auto-hits — no RPS, no defense, and no Evade or Protect.** Then roll initiative for everyone including the ambusher, who takes their place in order normally.

**Reactions need awareness; properties do not.** That is the whole line, and it settles every case. Evade is a dodge and Protect is throwing yourself in front of someone — neither can happen against a blow nobody saw. Armour, Resist, Thorns and Immunity are what you are made of, and they apply to anything. An ambush makes you easier to **hit**, never easier to **survive**. The attacker's own Blind still rolls: it is their failing, not your reaction.

**One attack, not one each.** A side that ambushes together still gets a single auto-hit; there is no window for a second before initiative is rolled. If more than one of them could take it, that side picks who.

**On failure:** roll initiative. No advantage.

A creature whose own entry defines an ambush uses that instead — several do, with their own trigger, stat and DC.

### Unguarded

Some creatures and people do not fight until they are fought. One who is **Unguarded** is not in combat: it takes no turns, plays no cards, and does nothing against the other side.

This is not willingness to be hit. It is a lack of aggression, and it leaves an opening for a first strike — but they will defend themselves the moment they are shown a threat.

While it lasts, a side in sight of an Unguarded target chooses one of two things. **Both end the state, and it cannot be had twice.**

- **Strike.** One attack lands **unblocked** — no defense is played and no reveal is resolved. **Every reaction and property still applies**, Evade and Protect included; they can see you coming and simply are not swinging back. Then roll initiative and fight.
- **Ready.** Visibly prepare for a fight — weapons drawn, aim taken, ground closed with obvious intent. Unguarded drops with no attack made, and initiative is rolled.

You cannot do both. Readying is visible, and visibility is exactly what closes the opening.

**Unguarded is not an ambush and does not stack with one.** An ambush pays for arriving unseen, so it beats the reactions — Evade and Protect. This pays only for the target not fighting yet, so it beats nothing but the defense card and the reveal.

A creature's own entry says whether it is Unguarded and what else ends it.

---

## Chase

When someone flees and someone else gives chase, track one thing: **the distance between them.** The fiction sets where it starts — right on their heels, a corridor away, a roof apart. There is no board and no fixed length; only the gap matters.

**Each exchange:** a contested roll. Soul is the obvious stat and any arguable one works (`rules/out-of-combat.md`). The winner moves the distance one step their way. Discard a card whose name fits the action → Advantage.

**Escaped — the distance reaches 4.** They are out of sight. The pursuer may try to follow the trail afterward: a check, DC set by the GM for terrain and time elapsed.

**Contact — the distance reaches 0.** The chase ends, and nothing else is decided by it. Contact grants no free attack; what it grants is the initiative. **The pursuer takes the first turn**, and chooses what they were chasing for:

- **Fight.** Roll initiative and resolve normally, pursuer first.
- **Grapple.** A contested check to grab, tackle or pin rather than harm. Available to anyone; `cards/subdue.md` is the card that does it deliberately.
- **Anything else.** An item, a skill, a word — whatever they actually wanted.

**The starting distance is the whole difficulty dial.** A chase run at even odds escapes about as often as the starting gap is large: one step apart and the pursuer wins three times in four, two steps is even, three steps and the runner gets away three times in four.

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

On your turn, you may take **one Action**, plus **one Item Action:**

| Action | Description |
|--------|-------------|
| Play a Card | Make an attack using a card from your hand |
| Move Position | Shift between Frontline and Backline |
| Use an Item | Activate an equipped or held item |
| Rushdown | Move a Backline enemy to the Frontline. You must be in the Frontline to use this action. |
| Take Cover | Backline only; the fiction must justify it. Anchored — Evade. Ends when you attack or leave the Backline. See Positioning → Cover. |
| Interact | Any noncombat action — talk, examine, activate, manipulate, or anything the fiction allows |
| Wait | Take no action; instead reinsert yourself anywhere later in the order. Trades this turn for exact positioning. Can't be used two turns in a row. See below. Counts as "waiting." |
| Flee | Attempt to exit combat — 2d10 + Soul vs DC 10 + highest enemy Soul, GM-adjusted. See Fleeing Combat above. |
| Grapple | Grab and hold an adjacent enemy — a contested check. Holds you both. See Grappling below. `cards/subdue.md` is the card that does it deliberately. |
| Stand Up | Get off the ground while Down. Only available once you are above 0 HP. See Collapse & Death below. |
| Destroy a Wound | Destroy 1 Wound from your hand (`rules/status-cards/wound.md`). |
| Rest in Place | Destroy every Exhaust in your hand, all at once (`rules/status-cards/exhaust.md`). |

**Item Action.** It does exactly what its name says and nothing else — it cannot be spent on any other option in the table above. Using an Item is also still legal as your regular Action, so a combatant who spends both this way uses 2 items in a single turn, at the cost of not attacking (or taking any other action) that turn.

**Waiting.** To Wait is to give up your action on purpose. In exchange you reposition: pick any slot later in the order and reinsert yourself there directly, and you act normally when the marker reaches it. You are standing on the turn marker, so you can only move later — you cannot act sooner than the turn you are already in — which is the only direction Wait ever needs.

The trade is **an action for a position.** You take one fewer action this fight — that is the whole cost; your turn count simply drops relative to everyone else — and in return you land exactly where you want in the order. Land a slot or two out and you act again shortly, later this cycle. Land far enough out to **lap the wheel** and the marker passes you once per full lap before honoring your slot — a way to opt out of the tempo entirely for a stretch. There is no cap on how far out you can reinsert, because moving later is always a cost, never a reward — so Wait as little or as much as you like.

Waiting sets your count to your new slot's natural arrival: the marker honors your slot the first time it reaches it. You are never passed over for having Waited — you never spent this lap's action; the forfeited action *was* the payment. (This is the difference between Waiting there and being *shifted* there: a shifted combatant's count is written by the shift, and the marker enforces it.)

Its main use is **team coordination** — chaining turns into the right sequence. Move yourself to act right after an ally's setup, or right before the ally you are setting up, so a combo resolves without an enemy acting in between. The reposition persists, so one Wait fixes a combo cadence for the rest of the fight. Waiting and "passing" are the same choice, and it is what effects that reward holding back — such as Patience — key off.

**Can't Wait twice in a row.** Waiting marks your token; the turn immediately after, you must take a real action — Wait is off the table until that turn resolves, then the mark clears. This is a distinct marker from Staggered's skip, with one job: closing the one real degenerate line in the system, where two combatants trade Waits back and forth forever and neither ever actually acts. Now the worst case is one mutual dodge before someone has to move.

---

## Attack Resolution

**Table rule:** when declaring a target, announce the range you're attacking from too — a quick checkpoint that keeps position and legality fresh in everyone's mind before any card gets committed, not after.

1. Attacker plays 1 card, face down — committed, not yet public.
2. **Blind, then Evade, resolve next** — Blind checks the attacker's own stack; Evade checks the defender's. See `rules/card-glossary.md` (Blind, Evade) for each's exact trigger and odds. Both resolve here, before the defender ever picks a card.
3. Defender may choose 1 card to defend with, face down — **blind.** The defender chooses without seeing the attacker's card, deciding from public information only (revealed-color history, position). This is a prediction, not a reaction. **The chosen card must satisfy its own Range requirement for the current positions, exactly as if the defender were attacking the attacker** — a Melee card cannot defend unless both combatants are Frontline; Ranged and Both are unaffected. A defender with no card in hand that meets the requirement has no legal defense against this attack.

**A mistaken illegal pick** (wrong Range for the current positions) is fixed differently depending on when it's caught. Caught before the attacker's card is known: swap freely, no penalty — nothing about the attacker's choice has leaked, so the pick is still genuinely blind. Caught only after the attacker's card is already revealed: too late for a free redo, since that knowledge can't be un-known and picking again now would mean picking with information blind defense is supposed to deny you. Resolve it as no legal defense — but the illegal card itself returns to hand, not the discard pile, since it was never actually, legally played. The attacker still learns what it was (a real cost, already paid), but the mistake doesn't also cost a card on top of the auto-loss.
4. If the defender cannot or chooses not to defend, the attacker wins automatically.
5. Both cards reveal simultaneously — only now do they become public and move to their owners' discard piles — and resolve using Rock-Paper-Scissors:

```
Blue (Mind)   beats  Red   (Body)
Red  (Body)   beats  Green (Soul)
Green (Soul)  beats  Blue  (Mind)
```

**Attacker wins** → deal damage, then apply the card's Effect  
**Defender wins** → no damage + defender triggers Defensive Bonus  
**Tie** → no damage. Attacker's Effect still triggers, then Defender's Defensive Bonus triggers. If the attacker's Effect cancels the Defensive Bonus, the Defensive Bonus does not trigger.

An Effect that only *adds to or amplifies this attack's damage* has nothing to act on when the attack deals no damage — so it does nothing on a tie (or any miss). Exploding dice, "+2 damage this attack," "deal +2 for each Wound," and the like all need a landed hit. Effects that do something independent of damage — apply a status, shift a stat, move a card — still trigger normally.

A standing bonus or penalty like "your next attack deals +X" is not consumed by a miss. If a Defensive Bonus needs to know what an attack would have dealt even though it didn't land, that number is computed for the defender's card, not the attacker's — the attacker's own next-attack bonus or penalty stays untouched, waiting for an attack that actually lands.

### Colorless cards

*Moved here 2026-08-17 from `cards/buckets/colorless.md`'s header — a resolution rule that was living in a card file.*

This file holds cards that don't carry a fixed color or stat on their face — currently cards that resolve to one only at the reveal step, per their own text (the point of them, not an exception to the rule; because RPS and stat totals aren't known until reveal, they deliberately fall outside color-locked bans like Axiom that check at commitment time), and reserved for any future status-effect-only card built without a color or stat of its own.

**How colorless resolves against a defense:** a colorless card auto-loses to any card with a real color — it never wins or ties against one. It only auto-loses when actually challenged that way, though: against no defense at all, or a defender who can't defend (Collapsed, Staggered), a colorless card still wins fully, same as anything else would in that situation. Two colorless cards facing each other tie.

Membership: `cards/buckets/colorless.md`.

---

## Damage Pipeline

The base roll is **Stat + die, with Deadly/Weak folded in** (`rules/card-glossary.md`) — a Deadly stack adds a d6, a Weak stack subtracts one, and one of each cancels before either applies. That total is what enters the pipeline below.

When *attack* damage is dealt, it passes through this pipeline in fixed order:

**redirect** (Shared Burden) → **volunteer shield** (Protect, team play) → **Armour** (flat reduction, creature passive) → **Resist / Vulnerable** (one stack of each cancels the other first; otherwise Resist halves or Vulnerable multiplies by 1.5, rounded down) → apply to HP.

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

The one action that moves someone else between positions. Defined in `rules/keywords/rushdown.md`; it appears in the action table above.

### Interact & Position

Position determines what's within reach. A character can only interact with objects that the fiction places near them. The GM calls it based on where things are — a lever at the center of the room favors Frontline characters, a mechanism on the back wall favors Backline. Neither position has a blanket advantage; the environment decides.

### Grappling

**Grapple** is an action: a contested check against an enemy you can reach. On a success you are **both grappled**, and it holds until someone breaks it.

While grappled, both combatants:

- gain **Rooted** — which is what stops a grappled combatant repositioning at all, Quick included, since Quick is still a voluntary change of position
- may take **no Action and no Item Action** except one: attempt a break, a contested check on your own turn. A success ends the grapple for both.

**Defending is unaffected.** Being held does not stop you answering an attack — you keep your Defensive Bonus and every reaction you had.

The hold costs the grappler exactly what it costs the target. That is the point of it: one combatant spends themselves to take another out of the fight, rather than getting a disable and an attack for the same action.

### Cover

Taking cover is an action. You must be in the Backline, and the fiction must justify it — there must be something to take cover behind.

**Anchored — Evade.** You gain one Evade the moment you take cover, and another at the start of each of your turns while you hold it.

Cover ends the instant you attack. **Attacking means playing a card as the attacker** — a Counter Attack does not end cover, and neither does Thorns. Both happen while you are defending. It also ends on Anchored's own terms (`rules/keywords/anchored.md`): if you move, or if you Collapse. **Cover requires the Backline.** Leave it by any means and cover ends — Rushdown included, which does not end Anchored generally but does end this.

### Confined Spaces

In tight environments (narrow tunnels, low passages, cramped rooms), the GM may limit how many characters fit in either position. If a creature physically blocks a passage, characters behind them cannot be targeted unless the fiction clearly allows it (e.g., ranged attack with line of sight). Rushdown in confined spaces may represent forcing an enemy into unstable terrain rather than a clean positional shift.

---

## Ongoing Effects

Some cards produce **Ongoing Effects.** These cards remain face up in front of the player after use. The effect persists until its stated condition is met, at which point the card is discarded.

Multiple ongoing effects can be active simultaneously unless a card specifies otherwise.

### Tracking a Status at the Table

**The card is the tracker.** A card that grants a temporary status — a Debuff or a Positive Status Effect, landing on you, an ally, or a foe — needs no separate marker. The card *is* the marker: set it face-up in front of whoever it is affecting instead of sending it to the discard pile, and discard it for real once the effect resolves, triggers, or expires.

That is not only convenience. The card is out of its owner's rotation the whole time it serves as a marker — it is not in their discard pile, so it is not coming back on a reshuffle either. That is a real cost on whoever played it, whether the card debuffed a foe or buffed an ally.

**Status tokens supplement the card. They never replace it.** Use one only where the card cannot show the whole state, which is three cases:

- **One card, several combatants.** The card stays in front of the player who played it; **every** affected combatant takes a status token — including that player, if the card caught them too, because the card has stopped marking a recipient and is now only marking the effect. The card says the effect is live and who is paying for it, the tokens say who is under it. A single card cannot sit in front of four people, and passing it to one of them makes that combatant look different from the others for no reason.
- **A count that changes.** A card granting a numbered status keeps showing its printed number no matter what happens to it. Take that many tokens when it lands and remove one each time the number goes down — whether the status is spent a use at a time or counts down a turn at a time. The card stays put; the tokens carry the remainder.
- **No card behind it at all.** A creature passive, an item, or the terrain can grant a status with nothing to set down. Here the status exists as tokens alone — the one case where it does, because there was never a card to leave anyone's rotation.

**A status belongs to whoever it landed on.** Once it resolves it stops being the caster's and becomes the target's. If the player who played the card Collapses, flees, or leaves the fight, every status they applied stays exactly as it is — the card stays out of rotation, the tokens stay on their targets. **A status is not maintained by its source.**

**The effect ends on its own stated condition, and only then does the card go to the discard.** That direction is one-way: an effect ending sends the card away, but moving the card never ends an effect. Nobody may pick a card back up to cancel one early. Tokens record state; they never hold it. Any status can be tracked this way — there is no list of which ones qualify.

*Anchored looks like an exception and is not. It ends when the combatant sustaining it moves or Collapses (`rules/keywords/anchored.md`) — that is the holder's own condition, written into the keyword, not the caster being removed.*

*Not to be confused with the turn markers on the initiative wheel (Initiative, above), which are also called tokens. Status tokens are a different object and never move around the wheel.*

---

## Objects

*Moved here 2026-08-17 from `cards/mason-glyphs.md`'s header, which stated outright that this rule "doesn't belong to Masons specifically." It was a general mechanic living inside one card set's file.*

Mason cards are one specific flavor of a more general mechanic: the **Object** — a persistent, position-anchored battlefield entity, distinct from a summoned creature or a status effect. A Mason's Object happens to be a glyph (the fiction is marking what's already in the environment — a wall, the ground, a statue, anything that will hold the mark — not conjuring something new into the world), but the underlying rule doesn't belong to Masons specifically: a future Construct-themed or Cultivator-themed card could create its own kind of Object (a totem, a ward-stone, whatever fits its own fiction) and reuse the exact same rules below, without inheriting "glyph" as the name for what it made. An Object is created at whatever position (Frontline/Backline) its creator occupied at the moment of creation, and stays there — it outlasts the character who made it, and doesn't move if they do.

Every Object shares the same rules:
- **Any attack can target an Object instead of a combatant.** It never rolls for damage and never triggers the attacking card's Effect — it just destroys the Object outright. The attacking card is discarded as normal.
- **Protect protects an Object the same way it protects an ally.** If anyone on the Object's side currently holds Protect, an attack that would destroy it is redirected to them instead (Protect's own text: "the next time an ally would take attack damage, you take it instead" — an Object counts as an ally for this purpose).
- **Otherwise, an Object's own effect triggers for free** — no roll, no contest — for whoever occupies its position on their turn. It isn't a combat action; it's an ongoing rule of the battlefield until someone bothers to destroy it.
- **An ally-facing Object benefits its creator too, same as anyone else on their side.** Once it exists, an Object isn't "cast" by anyone anymore — there's no caster's turn left to exclude the way a per-turn ally buff excludes itself. If you built it, standing on it pays out for you exactly like it would for anyone else who shares your side.

Mason glyphs are the only Objects currently built (`cards/buckets/position.md`; the MASON tag). A future Construct- or Cultivator-themed card can create its own kind of Object under these same rules without inheriting "glyph" as the name for what it made.

---

## Simultaneous Effects

When two or more effects would resolve at the same moment — several "start of your turn" triggers, two tokens landing at once — the **controller of those effects chooses the order** they resolve in. If the simultaneous effects have different controllers, the player whose turn it is decides the order.

Order can matter: two ticks that commute end at the same number, but a heal that arrives after a lethal tick arrives too late. If two effects would each reduce a combatant to death at the same instant and neither is clearly first, the exchange is a **mutual result** — resolve it as a tie.

**This does not apply to Attack Resolution.** An attacker's Effect and a defender's Defensive Bonus are not a controller's choice to order — Attack Resolution (above) already fixes it: Effect before Defensive Bonus, always, on every tie. Nobody, including the attacker, chooses that order.

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
