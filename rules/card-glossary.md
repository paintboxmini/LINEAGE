# Card Keyword Glossary

Canonical definitions for all keywords and status cards used in Tales Untold. When a card uses a keyword, this is the ruling. Card text that contradicts this file should be treated as an error.

---

## Keywords

**Counter Attack**
Deal this card's Attack damage back to the attacker. If a die is stated instead (e.g., Counter Attack d4), roll that die and deal the result. Melee only unless the card specifies otherwise. The counter is not a separate attack — it does not trigger a new RPS resolution.

**Debuff**
Any non-damage effect applied to you by an enemy: status conditions (Blind, Rooted, Staggered), status cards forced into your deck (Wound, Exhaust), forced position changes from enemy cards, stat reductions, or hand/deck interference. Does not include damage. Cards that "prevent the next debuff" block the next qualifying effect targeting you, then expire.

**Obscure**
Enemies cannot look at or manipulate your hand or deck. Does not prevent status cards from being added to your deck. Lasts until end of combat unless the source states otherwise.

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
Remove a card from play for the rest of combat. It does not go to the discard pile and cannot be looked at, moved, or retrieved. When combat ends, exiled cards return to their owner's deck. Unless the card specifies otherwise, nothing returns an exiled card during combat.

**Expose [Color]**
Choose 1 card in the target's hand without looking. If the chosen card matches the stated color, apply the effect printed after the Expose instruction. The target does not reveal their hand — selection is blind.

**Initiative Shift X**
Immediately move the target X positions in the initiative order. Positive X moves them toward the top of the order; negative X moves them toward the bottom. The target cuts into the new position; everyone seated between the old and new position shifts one seat over to make room.

The order wraps. A positive shift that would carry the target past the top instead drops them at the bottom; a negative shift that would carry them past the bottom instead lifts them to the top.

A positive shift can never delay the target's next turn; a negative shift can never accelerate it. If the repositioning above would violate that, correct it directly: a positive shift instead grants the target one immediate turn right now, then they settle into the new position starting next cycle. A negative shift instead skips the target's turn this cycle; they settle into the new position starting next cycle.

For shifts of N or more (N = number of combatants): resolve one full revolution at a time, awarding one additional turn (positive) or one skipped turn (negative) per revolution. Then resolve the remaining positional shift normally, including its own correction above if it applies.

To check at the table: see whether the shift's path passes through the position currently taking its turn — landing exactly on it counts as passing through. If it doesn't, no violation is possible — the target simply takes up the new position, done. If it does, apply the correction above.

**Lifesteal X**
Deal X damage to the target and heal X HP.

**Predictable**
The next time you would reveal a card for RPS resolution, the opponent may look at it before choosing theirs. Expires on use.

**Resist**
The next time an enemy successfully attacks you, take half damage rounded down. Expires after the next successful attack against you.

Resist stacks. Each stack halves one successful attack; only one stack applies to a given attack. "Resist X" grants X stacks.

**Rooted**
Cannot change position until the start of your next turn.

**Rushdown**
Move a target enemy from Backline to Frontline. Cannot target allies. The user must be in the Frontline. See `rules/combat.md`.

**Quick**
On your next turn, you may change positions without spending your action.

**Scry X**
Look at the top X cards of a deck. If no target is specified, this applies to your own deck. Return them in any order, placing each on top or on the bottom.

**Staggered**
The next time you are attacked, you cannot play a defensive card. The attack resolves without opposition.

**Thorns X**
Deal X damage to any enemy that successfully hits you with a melee attack. Applies after the attack resolves. Persists until end of combat unless the card states otherwise.

**Ward**
Prevent the next debuff applied to you. Expires on use.

---

## Stat Loss

Not a keyword — a shared mechanic. Some cards reduce one of your stats for a combat (Sunder drains Mind, Wither drains Body, Erode drains Soul). Whenever a stat is reduced this way:

- **Your maximum HP drops by 3 for every point lost, regardless of which stat.** Losing Body, Mind, or Soul all cost max HP the same. If your current HP now exceeds your new maximum, it drops to the maximum. If your maximum reaches 0, you Collapse.
- The lowered stat uses its reduced value for everything else it governs — damage, and its listed derived value — until the loss ends.

Stat loss lasts for the combat unless a card says otherwise, then the stat returns to normal (and lost max HP with it). This applies to every current and future stat-draining card; the card only states the stat and amount.

---

## Status Cards

Status cards are placed into decks as consequences. They cannot be played. They must be managed.

---

### WOUND
*Status — Colorless*
Cannot be played.
You may use your action to discard this card.
*Effect when discarded: none.*
1 Wound may be removed per short rest.

---

### EXHAUST
*Status — Colorless*
Cannot be played.
When discarded, take 2 damage.
At the end of your turn, you may instead discard this card and apply Initiative Shift -1 to yourself.
Use your action to remove all Exhaust cards from your hand — removal this way is exile, not a discard, so it deals no damage.
All Exhaust cards are removed from your deck at short rest.

---

### FOGLUST
*Status — Curse*
When drawn: Gain Blind until end of your turn.
Removal: Story dependent.
*"The fog remembered somewhere beautiful. You went with it."*

*Source: Fog Goggles. See `items/fog-basin-items.md`.*
