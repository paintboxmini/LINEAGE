# Card Keyword Glossary

Canonical definitions for all keywords and status cards used in Tales Untold. When a card uses a keyword, this is the ruling. Card text that contradicts this file should be treated as an error.

---

## Keywords

**Counter Attack**
Deal this card's Attack damage back to the attacker. Melee only unless the card specifies otherwise. The counter is not a separate attack — it does not trigger a new RPS resolution.

**Debuff**
Any non-damage effect applied to you by an enemy: status conditions (Blind, Rooted, Wound), forced position changes from enemy cards, stat reductions, or hand/deck interference. Does not include damage. Cards that "prevent the next debuff" block the next qualifying effect targeting you, then expire.

**Obscure**
Enemies cannot look at or manipulate your hand or deck. Does not prevent status cards from being added to your deck.

**Advantage (Damage)**
Roll twice for your damage die and take the higher result. This applies to combat damage only. For Advantage on skill checks and saves, see `rules/resolution.md`.

**Disadvantage (Damage)**
Roll twice for your damage die and take the lower result. This applies to combat damage only. For Disadvantage on skill checks and saves, see `rules/resolution.md`.

**Armour X**
Reduce all incoming attack damage by X. Applies before Resist. Stacks with other damage reduction effects.

**Anchored**
You gain a specific benefit that persists as long as you do not change positions. The benefit is stated on the card and triggers at the start of each of your turns. If you move — voluntarily or by an enemy effect — Anchored ends immediately.

**Blind**
50% chance to miss. When Blind, roll 1d2 before selecting a card to attack with. On a 1, the attack fails entirely. Lasts until the end of your next turn unless the card specifies otherwise.

**Evade**
50% chance to dodge the next attack declared against you, resolved before you select a card to defend with. Roll 1d2 — on a 1, the attack misses entirely. Expires after the next attack targeting you, whether or not it triggers.

Evade stacks. Each stack protects against one attack. Only one Evade triggers per attack — you cannot roll multiple times against the same attack.

**Exile**
Remove a card from play until end of combat. It does not go to the discard pile. Unless the card specifies otherwise, exiled cards are not returned.

**Expose [Color]**
Choose 1 card in the target's hand without looking. If the chosen card matches the stated color, apply the card's effect. The target does not reveal their hand — selection is blind.

**Initiative Shift X**
Immediately move the target X positions in the initiative order. Positive X moves them toward the top of the order; negative X moves them toward the bottom.

The order wraps. A positive shift that would carry the target past the top instead drops them at the bottom; a negative shift that would carry them past the bottom instead lifts them to the top.

A positive shift can never delay the target's next turn; a negative shift can never accelerate it. If the repositioning above would violate that, correct it directly: a positive shift instead grants the target one immediate turn right now, then they settle into the new position starting next cycle. A negative shift instead skips the target's turn this cycle; they settle into the new position starting next cycle.

To check at the table: see whether the shift's path passes through the position currently taking its turn. If it doesn't, no violation is possible — the target simply takes up the new position, done. If it does, apply the correction above.

**Lifesteal X**
Deal X damage to the target and heal X HP.

**Predictable**
The next time you would reveal a card for RPS resolution, the opponent may look at it before choosing theirs. Expires on use.

**Resist**
The next time an enemy successfully attacks you, take half damage rounded down. Expires after the next successful attack against you.

**Rooted**
Cannot change position until the start of your next turn.

**Rushdown**
Move a target from Backline to Frontline. The user must be in the Frontline. See `rules/combat.md`.

**Quick**
On your next turn, you may change positions without spending your action.

**Scry X**
Look at the top X cards of a deck. If no target is specified, this applies to your own deck. Return them in any order, placing each on top or on the bottom.

**Staggered**
The next time you are attacked, you cannot play a defensive card. The attack resolves without opposition.

**Thorns X**
Deal X damage to any enemy that successfully hits you with a melee attack. Applies after the attack resolves.

**Ward**
Prevent the next debuff applied to you. Expires on use.

---

## Status Cards

Status cards are placed into decks as consequences. They cannot be played. They must be managed.

---

### WOUND
*Status — Colorless*
Cannot be played.
At the end of your turn, discard this card.
*Effect when discarded: none.*
1 Wound may be removed per short rest.

---

### EXHAUST
*Status — Colorless*
Cannot be played.
When discarded, take 2 damage.
At the end of your turn, you may instead discard this card and apply Initiative Shift -1 to yourself.
Use your action to remove all Exhaust cards from your hand.
All Exhaust cards are removed from your deck at short rest.

---

### FOGLUST
*Status — Curse*
When drawn: Gain Blind until end of your turn.
Removal: Story dependent.
*"The fog remembered somewhere beautiful. You went with it."*

*Source: Fog Goggles. See `items/fog-basin-items.md`.*
