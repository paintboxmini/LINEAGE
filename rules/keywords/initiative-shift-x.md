# Initiative Shift X

A positive shift moves the target's token X positions counterclockwise around the wheel (see `rules/combat.md`); a negative shift moves it X positions clockwise. A positive shift can never cause its target to act later. A negative shift can never cause its target to act sooner.

Initiative Shift always moves the token the full requested distance. If that movement would violate "positive never later" or "negative never sooner," place a chip to preserve the invariant instead of changing the movement.

**Tracking skips and bonus turns.** Place a skip chip on a token that needs to be skipped; when the marker reaches it, skip its turn and remove the chip. Place a bonus chip on a token that's earned an immediate extra turn instead; take that turn, then remove the chip.

**With exactly 3 combatants on the wheel, reduce X's magnitude by 1 (toward zero) before applying the shift.** A shift of ±1 becomes no shift at all. This applies only at exactly 3 — the wheel is at its most sensitive there, and this is the one correction for it.

Multiple shifts applied to the same token at once sum into one net shift before it applies. If a positive shift's distance would carry the target past the point where it must act now — including a full lap back around to the marker's own slot — the target instead receives an immediate extra turn, taken as soon as the currently-resolving turn finishes. The combatant already acting when this happens is not shorted a turn, but doesn't get a second one either: the slide moves them to a new slot, and the marker skips that slot when it reaches it, since they already acted this lap. That skip is specifically compensation for the bonus turn just granted — an ordinary bystander displaced by sliding, with no bonus turn triggering it, simply acts normally when the marker reaches wherever it landed. A negative shift is the mirror case: if its math would let the target act sooner than the marker's normal progression allows, the shift still moves the target's token and slides the wheel in full, but the target's turn is skipped the first time the marker reaches its new slot — it acts normally starting the next lap. A shift applies normally even to a token that already repositioned itself with Wait this combat. Reshifting a token that already carries a pending skip or bonus chip removes the pending chip — the token then resolves normally under the new shift, whatever slot it lands on.

For worked cases covering all of the above, see `rules/initiative-shift-examples.md`.
