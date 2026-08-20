# Initiative Shift X

A positive shift moves the target's token X positions counterclockwise around the wheel (see `rules/combat.md`); a negative shift moves it X positions clockwise. A positive shift can never cause its target to act later. A negative shift can never cause its target to act sooner.

Initiative Shift always moves the token the full requested distance. If that movement would violate "positive never later" or "negative never sooner," place a chip to preserve the invariant instead of changing the movement.

**Tracking skips and bonus turns.** Place a skip chip on a token that needs to be skipped; when the marker reaches it, skip its turn and remove the chip. Place a bonus chip on a token that's earned an immediate extra turn instead; take that turn, then remove the chip.

**With exactly 3 combatants on the wheel, reduce X's magnitude by 1 (toward zero) before applying the shift.** A shift of ±1 becomes no shift at all. This applies at exactly 3 and nowhere else.

**Several shifts at once** sum into one net shift before anything moves.

**A positive shift that overshoots** — carrying its target past the point where it must act now, including a full lap back to the marker's own slot — gives that target an immediate extra turn instead, taken as soon as the current turn finishes.

- The combatant acting when this happens is not shorted a turn and does not get a second one. The slide moves them to a new slot, and the marker skips that slot when it reaches it.
- That skip pays for the bonus turn. **A bystander displaced by the slide, with no bonus turn behind it, acts normally** wherever they landed.

**A negative shift that overshoots** is the mirror. The token still moves and the wheel still slides in full, but the target's turn is skipped the first time the marker reaches its new slot; it acts normally from the next lap.

**Wait does not protect a token.** A shift applies normally to one that already repositioned itself.

**Reshifting a token that holds a pending chip removes that chip.** It then resolves under the new shift, wherever it lands.

For worked cases covering all of the above, see `rules/initiative-shift-examples.md`.
