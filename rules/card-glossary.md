# Card Keyword Glossary

Canonical definitions for all keywords and status cards used in Tales Untold. When a card uses a keyword, this is the ruling. Card text that contradicts this file should be treated as an error.

---

## Keywords

**Counter Attack**
Deal this card's Attack damage back to the attacker. If a die is stated instead (e.g., Counter Attack d4), roll that die and deal the result. Melee only unless the card specifies otherwise. The counter is not a separate attack — it does not trigger a new RPS resolution.

**Debuff**
Any negative effect an enemy applies to you: status conditions (Blind, Rooted, Staggered), status cards forced into your deck (Wound, Exhaust), stat reductions, and forced position changes. Does not include damage. Cards that "prevent the next debuff" (Ward, Deflect) block the next qualifying effect targeting you, then expire.

Two kinds of interference are **not** debuffs and ignore Ward: being made to **discard**, and having your **deck scried**. They interfere but cannot be warded off. (Obscure is the answer to those — see below.)

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
Immediately move the target X positions in the initiative order: positive X toward the front (acts sooner), negative X toward the back (acts later). The target cuts into the new seat; everyone between the old and new seat shifts one over to make room.

The order is a loop — there are no ends to fall off, only the turn marker to cross (see `rules/combat.md`, The turn marker). A shift *crosses* the marker when the target's path passes over it; landing exactly on it counts. A shift that does not reach the marker simply reseats the target. A shift that crosses it does one of the following instead — which is why a positive shift can never delay the target's next turn, nor a negative one hasten it:
- **Forward** (positive, lapping past the marker): the target takes one extra turn immediately, then settles into its new seat next cycle.
- **Backward** (negative, lapped past the marker): the target's next turn is skipped, then it settles into its new seat next cycle.

**On the fence.** A target shifted while it is taking the current turn is standing *on* the marker — hopping off is not a crossing (see the fence, `rules/combat.md`). It crosses only if the shift carries it a full loop back around to the marker. So a small self-shift just reseats it — never a free turn, never a self-skip.

For shifts of X ≥ N (N = number of combatants): resolve one revolution at a time — one extra turn (positive) or one skipped turn (negative) each — then apply the leftover positional shift. A target on the fence counts its first revolution from the marker it stands on.

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
Look at the top X cards of a deck. If no target is specified, this applies to your own deck. For each card, choose to place it on top, on the bottom, or into the discard pile — in any order. (Binning a card to the discard lets you dig past dead draws, not just reorder them.)

**Staggered**
The next time you are attacked, you cannot play a defensive card. The attack resolves without opposition.

**Thorns X**
Deal X damage to any enemy that successfully hits you with a melee attack. Applies after the attack resolves. Persists until end of combat unless the card states otherwise.

**Unpreventable**
Damage that cannot be defended against. It ignores every defense that applies to attack damage — Armour, Resist, damage floors (Equal Footing), and redirects (Shared Burden, Fortress) — because those defend only against attacks. Bleed, Thorns, status damage, and HP costs are unpreventable: they land on their target in full and cannot be reduced, reassigned, or capped.

**Ward**
Prevent the next debuff applied to you. Expires on use.

---

## Stat Change

Not a keyword — a shared mechanic. Some cards change one of your stats for a combat (Sunder drains Mind, Wither drains Body, Erode drains Soul; other cards may raise a stat). A changed stat uses its new value for everything it governs, in real time:

- **Body** — Red-card damage, and max HP: **each point of Body changes your maximum HP by 2** (down when lost, up when gained). If a loss puts your current HP above the new maximum, current HP falls to the maximum; if your maximum reaches 0 you Collapse. Only Body touches HP.
- **Mind** — Blue-card damage, and hand size (Mind + 1). Hand size changes the moment the stat does. If a Mind loss leaves you holding more cards than your new hand size, discard down to it immediately.
- **Soul** — Green-card damage, and initiative (1d6 + Soul), applied to rolls made after the change.

A stat change lasts for the combat unless a card says otherwise, then the stat — and any max HP, hand size, or initiative it moved — returns to normal. This applies to every current and future stat-changing card; the card only states the stat and amount.

---

## Status Cards

Status cards are placed into decks as consequences. They cannot be played. They must be managed.

---

### WOUND
*Status — Colorless*
Cannot be played. It stays in your hand and occupies a card slot — a Wound does not leave on its own.
You may use your action to discard this card.
*Effect when discarded: none.*
Once per short rest, permanently remove (destroy) 1 Wound from your hand or discard pile — never from your deck, so you never have to search or track hidden Wounds.

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
