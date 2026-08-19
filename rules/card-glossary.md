# Card Keyword Glossary

*Generated from `rules/keywords/` and `rules/status-cards/` by `agent-tools/generate-glossary.py`. Edit those, not this file — `verify.py` fails if the two disagree.*

Canonical definitions for all keywords and status cards used in Tales Untold. When a card uses a keyword, this is the ruling. Card text that contradicts this file should be treated as an error.

This file is meant to be printed and handed to players. State the rule, plainly, and stop — no *why* it's shaped that way, no *how* the simulator happens to implement it. Most of the time that reasoning doesn't need a home at all; if it's a live design question worth remembering, it goes in `memory.md`, not here.

**Special Rule** — some cards carry a Special Rule line instead of, or alongside, an Effect and Defensive Bonus. It overrides normal resolution exactly as printed on that card.

---

## Keywords

**At the table — status-effect tokens.** A card that grants a temporary status — a Debuff or a Positive Status Effect, landing on you, an ally, or a foe — doesn't need a separate physical token. The card *is* the token: set it face-up in front of whoever it's affecting instead of sending it straight to the discard pile, and discard it for real once the effect resolves, triggers, or expires. Same physical technique Ongoing Effects already use (`rules/combat.md`). Not just a bookkeeping convenience: the card is out of its owner's rotation the whole time it's serving as a token — it isn't in their discard pile, so it isn't coming back on a reshuffle either. That's a real cost on whoever cast it, whether the card debuffed a foe or buffed an ally.

**Anchored**
A specific benefit persists as long as you do not change positions, triggering at the start of each of your turns. The card states who it targets — not always yourself: PATIENCE OF STONE heals its own caster, ROOTED OATH buffs a named ally, GRAPPLE holds the defender Rooted. Anchored is about what holding position sustains, not about who it's aimed at. If you move — voluntarily or by an enemy effect — Anchored ends immediately. It also ends immediately if you Collapse.

**Armour X**
Reduce all incoming attack damage by X. It applies to every attack, for the whole fight — it is not consumed and does not expire.

Armour applies **before** Resist and Vulnerable, so a creature with both takes the flat reduction first and the halving second. Unpreventable damage ignores Armour entirely, the same way it ignores every other attack-damage defense. An attack reduced to 0 still landed: the attacker's Effect resolves normally, it simply has no damage to work with.

**Armour stacks additively into a single value.** Armour 2 and Armour 1 held at once are Armour 3, reducing every attack by 3 for the rest of the fight. This is a different shape of stacking from Resist and Vulnerable: those stack as charges, each spent on one attack. Armour is never spent, so its stacks add up instead of queuing up.

Armour is the system's general-purpose flat damage reduction: it shows up as a creature passive, as the Armor equipment tier's own effect, and on consumables. Anything that says "reduce damage by X" is Armour X.

**Blind**
50% chance to miss. When an attacker with Blind attacks, roll 1d2 before any Evade check on the defender — after the attacker's card is played and committed, immediately before the defender selects a card to defend with. On a 1, the attack fails entirely; the attacker's card is discarded. Lasts until the end of your next turn unless the card specifies otherwise. Blind and Evade are separate checks that can both apply to the same attack.

**Counter Attack**
Deal this card's Attack damage back to the attacker.

**Critical**
This attack's base damage (stat + die, including any Deadly/Weak already rolled into it) is doubled, calculated before any other bonus is added. Not a status anyone holds or carries between turns — each card that grants Critical states its own triggering condition in its own text.

**Deadly**
The next time you roll attack damage, add an additional d6 to the result. Stacks: each stack applies to one future damage roll, not extra dice on the same roll. 1 stack of Deadly and 1 stack of Weak held at the same time cancel each other out.

**Debuff**
Weak, Blind, Vulnerable, Staggered, Rooted, and stat reductions — the six effects Ward and Deflect can prevent.

**Evade**
50% chance to dodge the next attack declared against you, resolved before you select a card to defend with. Roll 1d2 — on a 1, the attack misses entirely; the attacker's card is discarded, and its Effect does not trigger.

Evade stacks. Each stack protects against one attack. Only one Evade triggers per attack — you cannot roll multiple times against the same attack.

**Exile**
Remove a card from play for the rest of combat. It does not go to the discard pile and cannot be retrieved. When combat ends, exiled cards return to their owner's discard.

**A status card that is exiled is destroyed instead** — it never comes back.

**Immunity**
The next attack against you fails completely, before any cards are revealed — no defense is chosen, no damage is dealt, no Effect resolves. The attacker's card is discarded as normal. One use; expires the instant it triggers.

---

**Initiative Shift X**
A positive shift moves the target's token X positions counterclockwise around the wheel (see `rules/combat.md`); a negative shift moves it X positions clockwise. A positive shift can never cause its target to act later. A negative shift can never cause its target to act sooner.

Initiative Shift always moves the token the full requested distance. If that movement would violate "positive never later" or "negative never sooner," place a chip to preserve the invariant instead of changing the movement.

**Tracking skips and bonus turns.** Place a skip chip on a token that needs to be skipped; when the marker reaches it, skip its turn and remove the chip. Place a bonus chip on a token that's earned an immediate extra turn instead; take that turn, then remove the chip.

**With exactly 3 combatants on the wheel, reduce X's magnitude by 1 (toward zero) before applying the shift.** A shift of ±1 becomes no shift at all. This applies only at exactly 3 — the wheel is at its most sensitive there, and this is the one correction for it.

Multiple shifts applied to the same token at once sum into one net shift before it applies. If a positive shift's distance would carry the target past the point where it must act now — including a full lap back around to the marker's own slot — the target instead receives an immediate extra turn, taken as soon as the currently-resolving turn finishes. The combatant already acting when this happens is not shorted a turn, but doesn't get a second one either: the slide moves them to a new slot, and the marker skips that slot when it reaches it, since they already acted this lap. That skip is specifically compensation for the bonus turn just granted — an ordinary bystander displaced by sliding, with no bonus turn triggering it, simply acts normally when the marker reaches wherever it landed. A negative shift is the mirror case: if its math would let the target act sooner than the marker's normal progression allows, the shift still moves the target's token and slides the wheel in full, but the target's turn is skipped the first time the marker reaches its new slot — it acts normally starting the next lap. A shift applies normally even to a token that already repositioned itself with Wait this combat. Reshifting a token that already carries a pending skip or bonus chip removes the pending chip — the token then resolves normally under the new shift, whatever slot it lands on.

For worked cases covering all of the above, see `rules/initiative-shift-examples.md`.

**Lifesteal**
Heal for half the damage this attack actually dealt to HP, rounded down — after Resist and any other reduction, since that's the amount that landed.

**Locked**
A card afflicted with Locked cannot be played. Lasts until the end of combat unless the card states otherwise.

**Obscure**
Enemies cannot look at or manipulate your hand or deck. Does not prevent status cards from being added to your deck. Lasts until end of combat unless the source states otherwise.

**Positive Status Effects**
Evade, Resist, Deadly, Protect, Anchored, Quick, and Immunity. A card that references this term by name (rather than listing them out) means all of these at once.

**Protect**
The next time an ally would take attack damage, you take it instead.

**Quick**
You may change positions without spending your action — a free move in addition to your normal action, not a replacement for it. Gained on your own turn, it's usable that same turn and fades when the turn ends. Gained off-turn (a Defensive Bonus, typically), it's held until the end of your next turn. Fades either way whether spent or not — it never carries indefinitely.

**Resist**
The next time an enemy successfully attacks you, take half damage rounded down. Expires after the next successful attack against you.

Resist stacks. Each stack halves one successful attack; only one stack applies to a given attack. "Resist X" grants X stacks. 1 stack of Resist and 1 stack of Vulnerable (below) held at the same time cancel each other out, checked before either applies.

**Reveal Hand**
At the table, this means stating the color counts in hand (e.g. "2 Red, 1 Blue").

**Rooted**
Cannot voluntarily change position until the end of your next turn. Applied immediately on resolution — lasts through the rest of the current round and the afflicted character's entire next turn, fading at the end of that next turn, not the start. Forced repositioning — Rushdown, Pull, and similar effects — is unaffected; Rooted only blocks your own Move Position action.

**Anchored + Rooted.** When an Anchored effect re-applies Rooted to a fixed original target (GRAPPLE — see Anchored, above), that target gains a fresh Rooted at the start of each of your turns for as long as you remain Anchored, full duration each time. Moving ends your own Anchored and stops further re-application; it does not strip a Rooted already in effect.

**Card text.** A card that grants Rooted should say only "gains Rooted" — the duration lives here, not restated on the card.

**Rushdown**
Move a target enemy from Backline to Frontline. Cannot target allies. The user must be in the Frontline. See `rules/combat.md`.

**Scry X**
Look at the top X cards of a deck. If no target is specified, this applies to your own deck. For each card, choose to place it on top, on the bottom, or into the discard pile — in any order.

**Sealed**
You cannot Use an Item, whether by Action or Item Action, and any passive effect from an item you have equipped or are holding stops working for the duration. Lasts until the end of your next turn unless the card states otherwise.

**Staggered**
The next time you would attack or defend, that one instance is skipped instead — either you skip attacking on your turn, or an incoming attack goes undefended — whichever comes first. Staggered ends the instant that happens.

**Thorns X**
Deal X damage to any enemy that successfully hits you with a melee attack. Applies after the attack resolves. Persists until end of combat unless the card states otherwise.

**Thorns stacks additively into a single value**, the same way Armour does — Thorns 2 and Thorns 1 held at once are Thorns 3, dealt to every melee attacker for the rest of the fight. Not consumed, so stacks add rather than queue.

**Unpreventable**
Damage that cannot be defended against. It ignores every defense that applies to attack damage — Armour, Resist, damage floors (Equal Footing), and redirects (Shared Burden, Protect) — because those defend only against attacks. Thorns, status damage, and HP costs are unpreventable: they land on their target in full and cannot be reduced, reassigned, or capped.

**Vulnerable**
The next time an enemy successfully attacks you, take 50% more damage, rounded down. Expires after the next successful attack against you — same shape as Resist, opposite direction. A Debuff, removable by Ward. Stacks the same way Resist does: each stack applies to one future successful attack, not a running multiplier. Cancels 1-for-1 with Resist (above) rather than ever applying alongside it.

**Ward**
Prevent the next Debuff (above) applied to you. Triggers automatically the instant a qualifying Debuff would apply — no declaration required. Expires on use.

**Weak**
The next time you roll attack damage, subtract an additional d6 from the result. Stacks the same way Deadly does: each stack applies to one future damage roll, not extra dice on the same roll. Cancels 1-for-1 with Deadly (above).

---

## Stat Change

Not a keyword — a shared mechanic. Some cards change one of your stats for a combat (Sunder drains Mind, Wither drains Body, Erode drains Soul; other cards may raise a stat). A changed stat uses its new value for everything it governs, in real time:

- **Body** — Red-card damage, and max HP at **3 points per point of Body** (down when lost, up when gained) — the heaviest of the three shares, matching the HP formula's own weighting: (3 × Body) + Soul + Mind.
- **Mind** — Blue-card damage; hand size (equal to Mind, minimum 2 — hand size never drops below 2, however far Mind falls; changes the moment the stat does, and a hand already above the new, lower size is not discarded down, it simply can't draw back up until it naturally falls below the cap); and max HP at **1 point per point of Mind**.
- **Soul** — Green-card damage; initiative (1d6 + Soul, applied to rolls made after the change); and max HP at **1 point per point of Soul**.

**All three stats touch max HP** *(changed 2026-08-06 to match the HP formula's own three-stat shape — Body at 3×, Mind and Soul at 1× each; previously Body was the only stat that did)*. If a loss puts your current HP above the new maximum, current HP falls to the maximum; if your maximum reaches 0 you Collapse. Increasing max HP does not increase current HP.

A stat change lasts for the combat unless a card says otherwise, then the stat — and any max HP, hand size, or initiative it moved — returns to normal. This applies to every current and future stat-changing card; the card only states the stat and amount.

---

---

## Status Cards

Status cards are placed into decks as consequences. They cannot be played. They must be managed.

### A ROOTED HEART
*Status — Curse*
Cannot be played. At the end of your turn, discard it if it is in your hand.
It costs you the draw and the hand slot for one turn, then cycles back through your deck on the next reshuffle — it does not clog your hand the way a Wound does, it simply keeps coming back.
Removal: story dependent. Exiling it destroys it (see Exile).
*"Something of the Weald is in you now. It is patient about it."*

*Source: the Root Heart's GRAFT. See `cards/graft.md`.*

---

### EXHAUST
*Status — Colorless*
Cannot be played. It occupies a card slot while in your hand, and an Exhaust does not leave on its own.
Where it enters is whatever the source card says — hand or deck. A card that adds Exhaust to your hand costs you the slot immediately; a card that shuffles Exhaust into your deck costs you nothing until you draw it.
Use your action to rest in place: every Exhaust card in your hand is destroyed.
A short or long rest removes every copy of Exhaust from your hand, deck, and discard pile.

**Exhaust always clears in bulk; a Wound comes off one at a time.** That is the difference between them. Rest once and every Exhaust you are carrying is gone at once, wherever it sits. Wounds have to be answered individually — one per action, one per short rest.

---

### FOGLUST
*Status — Curse*
When drawn: Gain Blind until end of your turn.
Removal: Story dependent.
*"The fog remembered somewhere beautiful. You went with it."*

*Source: Fog Goggles. See `items/fog-basin-items.md`.*

---

### WOUND
*Status — Colorless*
Cannot be played. It stays in your hand and occupies a card slot — a Wound does not leave on its own.
In combat, use your action to destroy 1 Wound from your hand.
Once per short rest, destroy 1 Wound from your hand, discard pile, or deck. Short rests chain (`rules/out-of-combat.md`), so clearing several Wounds in one sitting costs time, not repetition.
On a long rest, all Wounds are destroyed.
