# Card Keyword Glossary

Canonical definitions for all keywords and status cards used in Tales Untold. When a card uses a keyword, this is the ruling. Card text that contradicts this file should be treated as an error.

---

## Keywords

**Counter Attack**
Deal this card's Attack damage back to the attacker. If a die is stated instead (e.g., Counter Attack d4), roll that die and deal the result. Melee only unless the card specifies otherwise. The counter is not a separate attack — it does not trigger a new RPS resolution.

**Debuff**
Any negative effect an enemy applies to you: status conditions (Blind, Rooted, Staggered), status cards forced into your deck (Wound, Exhaust), stat reductions, and forced position changes. Does not include damage. Cards that "prevent the next debuff" (Ward, Deflect) block the next qualifying effect targeting you, then expire.

**Obscure**
Enemies cannot look at or manipulate your hand or deck. Does not prevent status cards from being added to your deck. Lasts until end of combat unless the source states otherwise.

**Deadly**
The next time you roll attack damage, roll it twice and take the higher result. Stacks: each stack applies to one future damage roll, not extra dice on the same roll.

**Weak**
The next time you roll attack damage, roll it twice and take the lower result. Stacks the same way Deadly does: each stack applies to one future damage roll, not extra dice on the same roll.

**Anchored**
You gain a specific benefit that persists as long as you do not change positions. The benefit is stated on the card and triggers at the start of each of your turns. If you move — voluntarily or by an enemy effect — Anchored ends immediately.

**Blind**
50% chance to miss. When an attacker with Blind attacks, roll 1d2 before any Evade check on the defender — after the attacker's card is played and committed, immediately before the defender selects a card to defend with. On a 1, the attack fails entirely; the attacker's card is discarded. Lasts until the end of your turn unless the card specifies otherwise. Blind and Evade are separate checks that can both apply to the same attack.

**Evade**
50% chance to dodge the next attack declared against you, resolved before you select a card to defend with. Roll 1d2 — on a 1, the attack misses entirely; the attacker's card is discarded.

Evade stacks. Each stack protects against one attack. Only one Evade triggers per attack — you cannot roll multiple times against the same attack.

**Exile**
Remove a card from play for the rest of combat. It does not go to the discard pile and cannot be retrieved. When combat ends, exiled cards return to their owner's deck.

**Expose [Color]**
Choose 1 card in the target's hand without looking. If the chosen card matches the exposed color, apply the effect printed after the Expose instruction. The target does not reveal their hand — selection is blind.

**Locked**
A card afflicted with Locked cannot be played. Lasts until the end of combat unless the card states otherwise.

**Initiative Shift X**
A positive shift moves the target's token X positions counterclockwise around the wheel (see `rules/combat.md`); a negative shift moves it X positions clockwise. A positive shift can never cause its target to act later. A negative shift can never cause its target to act sooner.

Initiative Shift always moves the token the full requested distance. If that movement would violate "positive never later" or "negative never sooner," place a chip to preserve the invariant instead of changing the movement.

**Tracking skips and bonus turns.** Place a skip chip on a token that needs to be skipped; when the marker reaches it, skip its turn and remove the chip. Place a bonus chip on a token that's earned an immediate extra turn instead; take that turn, then remove the chip.

**With exactly 3 combatants on the wheel, reduce X's magnitude by 1 (toward zero) before applying the shift.** A shift of ±1 becomes no shift at all. This applies only at exactly 3 — the wheel is at its most sensitive there, and this is the one correction for it.

Multiple shifts applied to the same token at once sum into one net shift before it applies. If a positive shift's distance would carry the target past the point where it must act now — including a full lap back around to the marker's own slot — the target instead receives an immediate extra turn, taken as soon as the currently-resolving turn finishes. The combatant already acting when this happens is not shorted a turn, but doesn't get a second one either: the slide moves them to a new slot, and the marker skips that slot when it reaches it, since they already acted this lap. That skip is specifically compensation for the bonus turn just granted — an ordinary bystander displaced by sliding, with no bonus turn triggering it, simply acts normally when the marker reaches wherever it landed. A negative shift is the mirror case: if its math would let the target act sooner than the marker's normal progression allows, the shift still moves the target's token and slides the wheel in full, but the target's turn is skipped the first time the marker reaches its new slot — it acts normally starting the next lap. A shift applies normally even to a token that already repositioned itself with Wait this combat. Reshifting a token that already carries a pending skip or bonus chip removes the pending chip — the token then resolves normally under the new shift, whatever slot it lands on.

For worked cases covering all of the above, see `rules/initiative-shift-examples.md`.

**Lifesteal**
Heal for half the damage this attack actually dealt to HP, rounded down — after Resist and any other reduction, since that's the amount that landed. On a Defensive Bonus, no attack damage was dealt (the defender won), so there's nothing to take half of — same as any Defensive Bonus that needs a damage number a defender-win didn't produce (`rules/combat-example.md`, Edge Cases): roll the attacker's damage anyway, and heal half of that instead.

**Resist**
The next time an enemy successfully attacks you, take half damage rounded down. Expires after the next successful attack against you.

Resist stacks. Each stack halves one successful attack; only one stack applies to a given attack. "Resist X" grants X stacks.

**Rooted**
Cannot voluntarily change position until the start of your next turn. Forced repositioning — Rushdown, Pull, and similar effects — is unaffected; Rooted only blocks your own Move Position action.

**Rushdown**
Move a target enemy from Backline to Frontline. Cannot target allies. The user must be in the Frontline. See `rules/combat.md`.

**Quick**
On your next turn, you may change positions without spending your action — a free move in addition to your normal action that turn, not a replacement for it.

**Scry X**
Look at the top X cards of a deck. If no target is specified, this applies to your own deck. For each card, choose to place it on top, on the bottom, or into the discard pile — in any order.

**Staggered**
A staggered character cannot attack or defend — every attack against them resolves without opposition, and they cannot play a card as an attack of their own. The condition persists until the affected character spends their action to recover their balance, or an ally spends their action to help them recover it instead. Either way, Staggered ends the instant the action resolves.

**Thorns X**
Deal X damage to any enemy that successfully hits you with a melee attack. Applies after the attack resolves. Persists until end of combat unless the card states otherwise.

**Unpreventable**
Damage that cannot be defended against. It ignores every defense that applies to attack damage — Resist, damage floors (Equal Footing), and redirects (Shared Burden, Fortress) — because those defend only against attacks. Thorns, status damage, and HP costs are unpreventable: they land on their target in full and cannot be reduced, reassigned, or capped.

**Ward**
Prevent the next debuff applied to you. Triggers automatically the instant a qualifying debuff would apply — no declaration required. Expires on use.

---

## Stat Change

Not a keyword — a shared mechanic. Some cards change one of your stats for a combat (Sunder drains Mind, Wither drains Body, Erode drains Soul; other cards may raise a stat). A changed stat uses its new value for everything it governs, in real time:

- **Body** — Red-card damage, and max HP: **each point of Body changes your maximum HP by 2** (down when lost, up when gained). If a loss puts your current HP above the new maximum, current HP falls to the maximum; if your maximum reaches 0 you Collapse. Increasing max HP does not increase current HP. Only Body touches HP.
- **Mind** — Blue-card damage, and hand size (equal to Mind, minimum 2 — hand size never drops below 2, however far Mind falls). Hand size changes the moment the stat does.
- **Soul** — Green-card damage, and initiative (1d6 + Soul), applied to rolls made after the change.

A stat change lasts for the combat unless a card says otherwise, then the stat — and any max HP, hand size, or initiative it moved — returns to normal. This applies to every current and future stat-changing card; the card only states the stat and amount.

---

## Status Cards

Status cards are placed into decks as consequences. They cannot be played. They must be managed.

---

### WOUND
*Status — Colorless*
Cannot be played. It stays in your hand and occupies a card slot — a Wound does not leave on its own.
**Quick field first aid** — permanently remove (destroy) 1 Wound from your hand. In combat this costs your action. Outside combat it doesn't require a full action or a short rest at all — tearing a strip of cloth and wrapping it is an ordinary beat, not a resource-gated one, and the GM shouldn't block it. Either way it only clears one Wound per use; a player working through several in a row outside combat should be pointed toward a short rest instead of chaining the quick version for free.
Once per short rest, permanently remove (destroy) 1 Wound from your hand or discard pile — never from your deck, so you never have to search or track hidden Wounds. Short rests chain (`rules/core-rules.md`), so clearing several Wounds in one sitting costs time, not repetition.

---

### EXHAUST
*Status — Colorless*
Cannot be played. It stays in your hand and occupies a card slot — an Exhaust does not leave on its own.
Use your action to permanently remove all Exhaust cards from your hand. That's the only way to clear them.

---

### FOGLUST
*Status — Curse*
When drawn: Gain Blind until end of your turn.
Removal: Story dependent.
*"The fog remembered somewhere beautiful. You went with it."*

*Source: Fog Goggles. See `items/fog-basin-items.md`.*
