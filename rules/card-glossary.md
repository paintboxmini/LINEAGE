# Card Keyword Glossary

Canonical definitions for all keywords and status cards used in Tales Untold. When a card uses a keyword, this is the ruling. Card text that contradicts this file should be treated as an error.

This file is meant to be printed and handed to players. State the rule, plainly, and stop — no *why* it's shaped that way, no *how* the simulator happens to implement it. Most of the time that reasoning doesn't need a home at all; if it's a live design question worth remembering, it goes in `memory.md`, not here.

**Special Rule** — some cards carry a Special Rule line instead of, or alongside, an Effect and Defensive Bonus. It overrides normal resolution exactly as printed on that card.

---

## Keywords

*The number before each keyword is how many cards in `cards/` grant it — a snapshot as of 2026-07-23, not a live count. It'll drift as cards are added or reworked; recount rather than trust it once it's been a while. Recounted for real across all 241 card blocks in `cards/*.md` (up from 216 at the 2026-07-18 snapshot), not estimated forward from the old numbers.*

**(5) Counter Attack**
Deal this card's Attack damage back to the attacker.

**(1) Debuff**
Any negative *auxiliary* effect an enemy applies to you: status conditions (Blind, Rooted, Staggered), status cards forced into your deck (Injury, Exhaust), stat reductions, forced discard, forced hand reveal, disabling your Defensive Bonus, and the removal of your Positive Status Effects (below). Does not include damage, and does not include anything that manipulates one of the three core pillars — RPS (color-denial, e.g. Axiom), Initiative (Initiative Shift X), or Position (forced movement, e.g. Repel, Calculate, Trample, Push/Pull) — those stay fully live even against Ward, by design; the pillars are meant to always be contestable. Cards that "prevent the next debuff" (Ward, Deflect) block the next qualifying effect targeting you, then expire.

**(5) Positive Status Effects**
Evade, Resist, Deadly, Protect, Anchored, Quick, and Immunity. A card that references this term by name (rather than listing them out) means all of these at once. Removing them from someone is a Debuff (above) — Ward can prevent it.

**(2) Obscure**
Enemies cannot look at or manipulate your hand or deck. Does not prevent status cards from being added to your deck. Lasts until end of combat unless the source states otherwise.

**(3) Reveal HAND**
At the table, this means stating the color counts in hand (e.g. "2 Red, 1 Blue")

**(1) Critical**
This attack's base damage (stat + die, including any Deadly/Weak already rolled into it) is doubled, calculated before any other bonus is added. Not a status anyone holds or carries between turns — each card that grants Critical states its own triggering condition in its own text.

**(19) Deadly**
The next time you roll attack damage, add an additional d6 to the result. Stacks: each stack applies to one future damage roll, not extra dice on the same roll. 1 stack of Deadly and 1 stack of Weak held at the same time cancel each other out 

**(10) Weak**
The next time you roll attack damage, subtract an additional d6 from the result. Stacks the same way Deadly does: each stack applies to one future damage roll, not extra dice on the same roll. Cancels 1-for-1 with Deadly (above).

**(10) Anchored**
You gain a specific benefit that persists as long as you do not change positions. The benefit is stated on the card and triggers at the start of each of your turns. If you move — voluntarily or by an enemy effect — Anchored ends immediately. It also ends immediately if you Collapse.

**(14) Blind**
50% chance to miss. When an attacker with Blind attacks, roll 1d2 before any Evade check on the defender — after the attacker's card is played and committed, immediately before the defender selects a card to defend with. On a 1, the attack fails entirely; the attacker's card is discarded. Lasts until the end of your next turn unless the card specifies otherwise. Blind and Evade are separate checks that can both apply to the same attack.

**(35) Evade**
50% chance to dodge the next attack declared against you, resolved before you select a card to defend with. Roll 1d2 — on a 1, the attack misses entirely; the attacker's card is discarded.

Evade stacks. Each stack protects against one attack. Only one Evade triggers per attack — you cannot roll multiple times against the same attack.

**(6) Exile**
Remove a card from play for the rest of combat. It does not go to the discard pile and cannot be retrieved. When combat ends, exiled cards return to their owner's discard.

**(4) Expose [Color]**
Choose 1 card in the target's hand without looking. If the chosen card matches the exposed color, apply the effect printed after the Expose instruction. The target does not reveal their hand — selection is blind.

**(4) Protect**
The next time an ally would take attack damage, you take it instead.

**(0) Locked**
A card afflicted with Locked cannot be played. Lasts until the end of combat unless the card states otherwise.

**(3) Sealed**
You cannot take the Use an Item action, and any passive effect from an item you have equipped or are holding stops working for the duration. Lasts until the end of your next turn unless the card states otherwise.

**(15) Initiative Shift X**
A positive shift moves the target's token X positions counterclockwise around the wheel (see `rules/combat.md`); a negative shift moves it X positions clockwise. A positive shift can never cause its target to act later. A negative shift can never cause its target to act sooner.

Initiative Shift always moves the token the full requested distance. If that movement would violate "positive never later" or "negative never sooner," place a chip to preserve the invariant instead of changing the movement.

**Tracking skips and bonus turns.** Place a skip chip on a token that needs to be skipped; when the marker reaches it, skip its turn and remove the chip. Place a bonus chip on a token that's earned an immediate extra turn instead; take that turn, then remove the chip.

**With exactly 3 combatants on the wheel, reduce X's magnitude by 1 (toward zero) before applying the shift.** A shift of ±1 becomes no shift at all. This applies only at exactly 3 — the wheel is at its most sensitive there, and this is the one correction for it.

Multiple shifts applied to the same token at once sum into one net shift before it applies. If a positive shift's distance would carry the target past the point where it must act now — including a full lap back around to the marker's own slot — the target instead receives an immediate extra turn, taken as soon as the currently-resolving turn finishes. The combatant already acting when this happens is not shorted a turn, but doesn't get a second one either: the slide moves them to a new slot, and the marker skips that slot when it reaches it, since they already acted this lap. That skip is specifically compensation for the bonus turn just granted — an ordinary bystander displaced by sliding, with no bonus turn triggering it, simply acts normally when the marker reaches wherever it landed. A negative shift is the mirror case: if its math would let the target act sooner than the marker's normal progression allows, the shift still moves the target's token and slides the wheel in full, but the target's turn is skipped the first time the marker reaches its new slot — it acts normally starting the next lap. A shift applies normally even to a token that already repositioned itself with Wait this combat. Reshifting a token that already carries a pending skip or bonus chip removes the pending chip — the token then resolves normally under the new shift, whatever slot it lands on.

For worked cases covering all of the above, see `rules/initiative-shift-examples.md`.

**(4) Lifesteal**
Heal for half the damage this attack actually dealt to HP, rounded down — after Resist and any other reduction, since that's the amount that landed.

**(34) Resist**
The next time an enemy successfully attacks you, take half damage rounded down. Expires after the next successful attack against you.

Resist stacks. Each stack halves one successful attack; only one stack applies to a given attack. "Resist X" grants X stacks. 1 stack of Resist and 1 stack of Vulnerable (below) held at the same time cancel each other out, checked before either applies.

**(0) Vulnerable**
The next time an enemy successfully attacks you, take 50% more damage, rounded down. Expires after the next successful attack against you — same shape as Resist, opposite direction. A Debuff (removable by Ward, like any other negative auxiliary effect). Stacks the same way Resist does: each stack applies to one future successful attack, not a running multiplier. Cancels 1-for-1 with Resist (above) rather than ever applying alongside it.

**(14) Rooted**
Cannot voluntarily change position until the start of your next turn. Forced repositioning — Rushdown, Pull, and similar effects — is unaffected; Rooted only blocks your own Move Position action.

**(5) Rushdown**
Move a target enemy from Backline to Frontline. Cannot target allies. The user must be in the Frontline. See `rules/combat.md`.

**(3) Quick**
You may change positions without spending your action — a free move in addition to your normal action that turn, not a replacement for it.

**(24) Scry X**
Look at the top X cards of a deck. If no target is specified, this applies to your own deck. For each card, choose to place it on top, on the bottom, or into the discard pile — in any order.

**(12) Staggered**
The next time you would attack or defend, that one instance is skipped instead — either you skip attacking on your turn, or an incoming attack goes undefended — whichever comes first. Staggered ends the instant that happens.

**(7) Thorns X**
Deal X damage to any enemy that successfully hits you with a melee attack. Applies after the attack resolves. Persists until end of combat unless the card states otherwise.

**(4) Unpreventable**
Damage that cannot be defended against. It ignores every defense that applies to attack damage — Resist, damage floors (Equal Footing), and redirects (Shared Burden, Protect) — because those defend only against attacks. Thorns, status damage, and HP costs are unpreventable: they land on their target in full and cannot be reduced, reassigned, or capped.

**(15) Ward**
Prevent the next Debuff (above) applied to you. Triggers automatically the instant a qualifying Debuff would apply — no declaration required. Expires on use.

**(2) Immunity**
The next attack against you fails completely, before any cards are revealed — no defense is chosen, no damage is dealt, no Effect resolves. The attacker's card is discarded as normal. One use; expires the instant it triggers.

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

### INJURY
*Status — Colorless*
Cannot be played. It stays in your hand and occupies a card slot — an Injury does not leave on its own.
**Quick field first aid** — permanently remove (destroy) 1 Injury from your hand. In combat this costs your action. Outside combat it doesn't require a full action or a short rest at all — tearing a strip of cloth and wrapping it is an ordinary beat, not a resource-gated one, and the GM shouldn't block it. Either way it only clears one Injury per use; a player working through several in a row outside combat should be pointed toward a short rest instead of chaining the quick version for free.
Once per short rest, permanently remove (destroy) 1 Injury from your hand or discard pile — never from your deck, so you never have to search or track hidden Injuries. Short rests chain (`rules/core-rules.md`), so clearing several Injuries in one sitting costs time, not repetition.

---

### EXHAUST
*Status — Colorless*
Goes directly into your hand when applied — not into the deck. It cannot be played and occupies a card slot; an Exhaust does not leave on its own. This is the difference from an Injury, which enters the deck and has to be drawn before it costs you anything: Exhaust costs you the slot immediately.
Use your action to permanently remove all Exhaust cards from your hand. That's the only way to clear them.

---

### FOGLUST
*Status — Curse*
When drawn: Gain Blind until end of your turn.
Removal: Story dependent.
*"The fog remembered somewhere beautiful. You went with it."*

*Source: Fog Goggles. See `items/fog-basin-items.md`.*
