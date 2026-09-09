# Card Keyword Glossary

Canonical definitions for all keywords and status cards used in Tales Untold. When a card uses a keyword, this is the ruling. Card text that contradicts this file should be treated as an error.

**Special Rule** — some cards carry a Special Rule line instead of, or alongside, an Effect and a Defense Effect. It overrides normal resolution exactly as printed on that card.

---

## Keywords

<!-- print:skip-start -->
*The number before each keyword is how many **core** cards use it — the four lists a deck actually builds from (`cards/red-body.md`, `cards/blue-mind.md`, `cards/green-soul.md`, `cards/colorless.md`), 164 cards as of 2026-09-09. Creature signature cards are deliberately excluded: they are one-offs written for a single stat block, so counting them tells you nothing about how common a keyword is in play. These counts are stripped from the printed packet (`printing/generate-rules-pdf.py`), so they exist for maintenance here and nowhere else.*

*A keyword counts when a card names it in an Attack, Effect, Defense Effect, or Special Rule line, once per card however many times it appears. Conditional references ("if the defender is Rooted") and negations ("cannot be affected by Blind" — CERTAIN STRIKE, the only live example) don't count toward the keyword being referenced; those cards are counted under whatever they actually grant instead. Case and inflection don't matter — several cards write "unpreventable" in lower case mid-sentence, STEAL says "Exiled" rather than "Exile", and three cards write "Positive Status Effect" singular. Match the word stem, not the glossary header. Debuff sits at 0 on purpose: no card names it, and it exists for Ward's definition to point at.*

*To recount: `python3 combatsimulations/cards.py` loads every card, `core_pool()` in that module is exactly the four lists above, and a word-boundary case-insensitive search of the four text lines reproduces these numbers once the two exclusions above are taken out by hand.*

<!-- print:skip-end -->

**At the table — status-effect tokens.** A card that grants a temporary status — a Debuff or a Positive Status Effect, landing on you, an ally, or a foe — doesn't need a separate physical token. The card *is* the token: set it face-up in front of whoever it's affecting instead of sending it straight to the discard pile, and discard it for real once the effect resolves, triggers, or expires. Same physical technique Ongoing Effects already use (`rules/combat.md`). Not just a bookkeeping convenience: the card is out of its owner's rotation the whole time it's serving as a token — it isn't in their discard pile, so it isn't coming back on a reshuffle either. That's a real cost on whoever cast it, whether the card debuffed a foe or buffed an ally.

**(6) Counter Attack**
Deal this card's Attack damage back to the attacker, works with effects like deadly.

**(0) Debuff**
Weak, Blind, Vulnerable, Staggered, Rooted, and stat reductions — the six effects Ward can prevent.

**(5) Positive Status Effects**
Evade, Resist, Deadly, Protect, Anchored, Quick, and Immunity. A card that references this term by name (rather than listing them out) means all of these at once.

**(18) Deadly**
The next time you roll attack damage, add an additional d6 to the result. Stacks: each stack applies to one future damage roll, not extra dice on the same roll. 1 stack of Deadly and 1 stack of Weak held at the same time cancel each other out.

**(8) Weak**
The next time you roll attack damage, subtract an additional d6 from the result. Stacks the same way Deadly does: each stack applies to one future damage roll, not extra dice on the same roll. Cancels 1-for-1 with Deadly (above).

**(10) Anchored**
A specific benefit persists as long as you do not change positions, triggering at the start of each of your turns. The card states who it targets — not always yourself: PATIENCE OF STONE heals its own caster, ROOTED OATH buffs a named ally, GRAPPLE holds the defender Rooted. Anchored is about what holding position sustains, not about who it's aimed at. If you move — voluntarily or by an enemy effect — Anchored ends immediately. It also ends immediately if you Collapse.

**(7) Blind**
50% chance to miss whatever you're doing in the exchange — attacking or defending, not attacker-only. Checked once both sides have already committed a card face down, before the reveal (`rules/combat.md`, Attack Resolution): roll 1d2, and on a 1, whoever holds it misses. The check always happens if it applies, even when another check in the same exchange already decided the outcome — see the resolution order in `rules/combat.md`.

**An attacker's miss alone** ends the exchange in the defender's favor — the defender auto-wins the resolution, exactly as if the RPS reveal had gone their way, and the attacker's card is discarded. **A defender's miss alone** on their own block resolves exactly like having no legal defense: the attacker wins automatically. **Both missing in the same exchange** is neither of those — it's a Mutual Miss (`rules/combat.md`, Attack Resolution): the attack failed and the attempted block against it also failed, so nobody wins and no Effect or Defense Effect triggers. A defender's Evade succeeding overrides all of this — a clean dodge wins the exchange outright regardless of what either Blind roll says.

Lasts until the end of your next turn unless the card specifies otherwise. Blind and Evade are separate checks, and a single exchange rolls every one that applies.

**(11) Evade**
50% chance to dodge an attack declared against you. Checked after you've chosen your defense (or declined to defend), before either card is revealed (`rules/combat.md`, Attack Resolution) — triggered by being attacked, not by whether the attack would actually land, so it rolls (and a stack is spent) even when the attacker already missed to their own Blind. Roll 1d2 — on a 1, you auto-win the resolution exactly as if the RPS reveal had gone your way: the attacker's card is discarded and its own Effect does not trigger.

Evade stacks. Each stack protects against one attack. Only one Evade triggers per attack — you cannot roll multiple times against the same attack.

**Cover Evade is not this keyword.** Taking cover grants a dodge that rolls the same way but persists instead of being spent, and it takes the place of your stacks while it lasts rather than adding to them (`rules/combat.md`, Positioning → Cover).

**(7) Exile**
Remove a card from play for the rest of combat. It does not go to the discard pile and cannot be retrieved. When combat ends, exiled cards return to their owner's discard.

**A status card that is exiled is destroyed instead** — it never comes back. Exile is the one way to answer a Wound, an Exhaust, or a curse permanently in the middle of a fight.

**(4) Protect**
The next time an ally would take attack damage, you take it instead.

**(13) Initiative Shift X**
A positive shift moves the target's token X positions counterclockwise around the wheel (see `rules/combat.md`); a negative shift moves it X positions clockwise. A positive shift can never cause its target to act later. A negative shift can never cause its target to act sooner.

Initiative Shift always moves the token the full requested distance. If that movement would violate "positive never later" or "negative never sooner," place a chip to preserve the invariant instead of changing the movement.

**Tracking skips and bonus turns.** Place a skip chip on a token that needs to be skipped; when the marker reaches it, skip its turn and remove the chip. Place a bonus chip on a token that's earned an immediate extra turn instead; take that turn, then remove the chip.

**With exactly 3 combatants on the wheel, reduce X's magnitude by 1 (toward zero) before applying the shift.** A shift of ±1 becomes no shift at all. This applies only at exactly 3 — the wheel is at its most sensitive there, and this is the one correction for it.

Multiple shifts applied to the same token at once sum into one net shift before it applies. If a positive shift's distance would carry the target past the point where it must act now — including a full lap back around to the marker's own slot — the target instead receives an immediate extra turn, taken as soon as the currently-resolving turn finishes. The combatant already acting when this happens is not shorted a turn, but doesn't get a second one either: the slide moves them to a new slot, and the marker skips that slot when it reaches it, since they already acted this lap. That skip is specifically compensation for the bonus turn just granted — an ordinary bystander displaced by sliding, with no bonus turn triggering it, simply acts normally when the marker reaches wherever it landed. A negative shift is the mirror case: if its math would let the target act sooner than the marker's normal progression allows, the shift still moves the target's token and slides the wheel in full, but the target's turn is skipped the first time the marker reaches its new slot — it acts normally starting the next lap. Reshifting a token that already carries a pending skip or bonus chip removes the pending chip — the token then resolves normally under the new shift, whatever slot it lands on.

For worked cases covering all of the above, see `rules/initiative-shift-examples.md`.

**(4) Lifesteal**
Heal for half the damage this attack actually dealt to HP, rounded down — after Resist and any other reduction, since that's the amount that landed.

**(24) Resist**
The next time an enemy successfully attacks you, take half damage rounded down. Expires after the next successful attack against you.

Resist stacks. Each stack halves one successful attack; only one stack applies to a given attack. "Resist X" grants X stacks. 1 stack of Resist and 1 stack of Vulnerable (below) held at the same time cancel each other out, checked before either applies.

**(0) Armour X**
Reduce all incoming attack damage by X. It applies to every attack, for the whole fight — it is not consumed and does not expire.

Armour applies **before** Resist and Vulnerable, so a creature with both takes the flat reduction first and the halving second. Unpreventable damage ignores Armour entirely, the same way it ignores every other attack-damage defense. An attack reduced to 0 still landed: the attacker's Effect resolves normally, it simply has no damage to work with.

**Armour stacks additively into a single value.** Armour 2 and Armour 1 held at once are Armour 3, reducing every attack by 3 for the rest of the fight. This is a different shape of stacking from Resist and Vulnerable: those stack as charges, each spent on one attack. Armour is never spent, so its stacks add up instead of queuing up.

Armour is the system's general-purpose flat damage reduction: it shows up as a creature passive, as the Armor equipment tier's own effect, and on consumables. Anything that says "reduce damage by X" is Armour X.

**(5) Vulnerable**
The next time an enemy successfully attacks you, take 50% more damage, rounded down. Expires after the next successful attack against you — same shape as Resist, opposite direction. A Debuff, removable by Ward. Stacks the same way Resist does: each stack applies to one future successful attack, not a running multiplier. Cancels 1-for-1 with Resist (above) rather than ever applying alongside it.

**(5) Rooted**
The next time you would change position, that movement is cancelled and the Rooted is spent. It is a charge, not a timer — it waits as long as it has to, and it is used up by the first movement it stops, whenever that comes.

**It stops forced movement too, and is spent doing it.** A Pull, a compelled Rushdown, a card that shoves you to the other position — Rooted cancels that just as it cancels your own Move Position, and then it is gone. This is the trade: Rooted is harder to wait out than a timer, and an enemy can strip it by making you move.

Rooted stacks. Each stack cancels one movement.

**Anchored + Rooted.** When an Anchored effect re-applies Rooted to a fixed original target (GRAPPLE — see Anchored, above), that target gains a fresh Rooted charge at the start of each of your turns for as long as you remain Anchored. Moving ends your own Anchored and stops further re-application; it does not spend a Rooted charge the target is already holding.

**Card text.** A card that grants Rooted should say only "gains Rooted" — the rule lives here, not restated on the card.

**(6) Quick**
A banked free Move Position, Rushdown included — spending it is your one free action for the turn (`rules/combat.md`, Turn Structure) and costs nothing from your Action. Holds until spent, however many turns that takes. Stacks: hold as many as you've been granted, spend one per turn.

**(9) Scry X**
Look at the top X cards of a deck. If no target is specified, this applies to your own deck. For each card, choose to place it on top, on the bottom, or into the discard pile — in any order.

**(5) Staggered**
The next time you would attack or defend, that one instance is skipped instead — either you skip attacking on your turn, or an incoming attack goes undefended — whichever comes first. Staggered ends the instant that happens.

**(7) Thorns X**
Deal X damage to any enemy that successfully hits you with a melee attack. Applies after the attack resolves. Persists until end of combat unless the card states otherwise.

**Thorns stacks additively into a single value**, the same way Armour does — Thorns 2 and Thorns 1 held at once are Thorns 3, dealt to every melee attacker for the rest of the fight. Not consumed, so stacks add rather than queue.

**(5) Unpreventable**
Damage that cannot be defended against. It ignores every defense that applies to attack damage — Armour, Resist, and reassignment (Protect) — because those defend only against attacks. Thorns, status damage, and HP costs are unpreventable: they land on their target in full and cannot be reduced, reassigned, or capped.

**(6) Ward**
Prevent the next Debuff (above) applied to you. Triggers automatically the instant a qualifying Debuff would apply — no declaration required. Expires on use.

**(4) Immunity**
The next attack damage you would take is reduced to 0. Nothing else about the exchange changes: cards are chosen and revealed as normal, the RPS outcome stands, and the attacker's Effect and any Defense Effect trigger exactly as they otherwise would. Only the damage is negated.

It applies inside the Damage Pipeline (`rules/combat.md`), which has two consequences worth knowing. It protects whoever actually receives the damage, so an attack reassigned onto someone else meets *their* Immunity, not yours. And it does nothing against unpreventable damage — Thorns, status damage, and HP costs were never attack damage to begin with.

One use, spent the moment it actually negates something. An exchange that deals you no damage anyway — you won, or it was a tie — leaves it untouched for the next one.

---

## Stat Change

Not a keyword — a shared mechanic. Some cards change one of your stats for a combat (Sunder drains Mind, Wither drains Body, Erode drains Soul; other cards may raise a stat). A changed stat uses its new value for everything it governs, in real time:

- **Body** — Red-card damage, and max HP at **4 points per point of Body** (down when lost, up when gained) — the heaviest of the three shares by a wide margin, matching the HP formula's own weighting: (4 × Body) + Soul + Mind.
- **Mind** — Blue-card damage; hand size (equal to Mind, minimum 2 — hand size never drops below 2, however far Mind falls; changes the moment the stat does, and a hand already above the new, lower size is not discarded down, it simply can't draw back up until it naturally falls below the cap); and max HP at **1 point per point of Mind**.
- **Soul** — Green-card damage; initiative (1d6 + Soul, applied to rolls made after the change); and max HP at **1 point per point of Soul**.

**All three stats touch max HP** *(changed 2026-08-06 to match the HP formula's own three-stat shape — Body at 4×, Mind and Soul at 1× each; previously Body was the only stat that did. Body's multiplier went from 3× to 4× on 2026-09-06, widening the HP spread so Body carries more of it.)*. If a loss puts your current HP above the new maximum, current HP falls to the maximum; if your maximum reaches 0 you Collapse. Increasing max HP does not increase current HP.

A stat change lasts for the combat unless a card says otherwise, then the stat — and any max HP, hand size, or initiative it moved — returns to normal. This applies to every current and future stat-changing card; the card only states the stat and amount.

---

## Status Cards

Status cards are placed into decks as consequences. They cannot be played. They must be managed.

---

### WOUND
*Status — Colorless*
Cannot be played. It stays in your hand and occupies a card slot — a Wound does not leave on its own.
In combat, use your action to destroy 1 Wound from your hand.
Once per short rest, destroy 1 Wound from your hand, discard pile, or deck. Short rests chain (`rules/character-creation.md`, Resting), so clearing several Wounds in one sitting costs time, not repetition.
On a long rest, all Wounds are destroyed.

---

### EXHAUST
*Status — Colorless*
Cannot be played. It occupies a card slot while in your hand, and an Exhaust does not leave on its own.
Where it enters is whatever the source card says — hand or deck. A card that adds Exhaust to your hand costs you the slot immediately; a card that shuffles Exhaust into your deck costs you nothing until you draw it.
Use your action to rest in place: every Exhaust card in your hand is destroyed.
A short or long rest removes every copy of Exhaust from your hand, deck, and discard pile.

**Exhaust always clears in bulk; a Wound comes off one at a time.** That is the difference between them. Rest once and every Exhaust you are carrying is gone at once, wherever it sits. Wounds have to be answered individually — one per action, one per short rest.

---

### A ROOTED HEART
*Status — Curse*
Cannot be played. At the end of your turn, discard it if it is in your hand.
It costs you the draw and the hand slot for one turn, then cycles back through your deck on the next reshuffle — it does not clog your hand the way a Wound does, it simply keeps coming back.
Removal: story dependent. Exiling it destroys it (see Exile).
*"Something of the Weald is in you now. It is patient about it."*

*Source: the Root Heart's GRAFT. See `cards/root-heart-weald.md`.*

---

### FOGLUST
*Status — Curse*
When drawn: Gain Blind until end of your turn.
Removal: Story dependent.
*"The fog remembered somewhere beautiful. You went with it."*

*Source: Fog Goggles. See `items/fog-basin-items.md`.*
