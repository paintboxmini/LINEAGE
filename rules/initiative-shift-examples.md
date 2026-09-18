# The Wheel & Initiative Shift — Worked Examples

Compact worked cases for the Wheel and Initiative Shift, in a short notation: four combatants, `a` through `d`, listed clockwise starting from whoever's currently acting. Read the Wheel (`rules/combat.md`) and Initiative Shift X (`rules/card-glossary.md`) first — this file exists to make those rules concrete, not to restate them.

<!-- print:skip-start -->
Every case below was worked through and confirmed directly; none of it is invented to fill a gap.
<!-- print:skip-end -->

---

## Example 1 — An ordinary shift

`a, b, c, d.` a is acting. a plays a card with Initiative Shift +1 targeting c.

c moves 1 slot counterclockwise, toward the marker. It passes through b's slot on the way, so b slides 1 slot toward the gap c left behind.

**Result: `a, c, b, d`.** No boundary hit, no chip needed. a's turn ends normally; c goes next, then b, then d.

*Demonstrates the base case — most Initiative Shift plays are exactly this. Sliding always happens; skip and bonus chips are only for the wraparound cases below.*

---

## Example 2 — A negative shift that overshoots

`a, b, c, d.` a plays Initiative Shift −2 on d.

d's clockwise math wraps past a full lap and would land it *sooner* than its own start — this is the boundary Initiative Shift's negative-shift guarantee exists to catch. The shift and the slide both still happen in full: `a, b, c, d` becomes `b, d, c, a`, with a **skip chip** placed on d.

**Turn sequence this lap:** a's turn ends → b goes next → **d is skipped** (chip removed) → c goes → a goes again (a was slid to a not-yet-visited slot this lap; nothing protects a bystander from acting twice when that happens — see Example 4). Next lap, the new order (`b, d, c, a`) runs normally with no chips pending.

*Demonstrates the ordinary skip case, and that a displaced bystander with no bonus turn to compensate for just acts on schedule wherever it lands.*

---

## Example 3 — A positive shift landing exactly on the marker's slot

`a, b, c, d.` a is acting. a plays Initiative Shift +3 on d.

d sits 3 slots from the marker and the shift is 3, so it lands **exactly** on the marker's own slot. **Onto is not across.** The shift and slide happen in full: `a, b, c, d` becomes **`d, a, b, c`**, and **no chip is placed on anyone.**

**Turn sequence this lap:** a's turn ends → **d goes next** → a goes → b goes → c goes. Then the new order (`d, a, b, c`) runs normally.

**Why d goes next rather than last:** the marker belongs to a *slot*, not to a combatant, and it has not finished with its own slot — d slid into it. So d takes the very next turn. **Nobody is skipped and nobody gets an extra turn**; d simply cut to the front of the line, which is what a positive shift is supposed to do.

*Demonstrates the boundary that isn't one. Landing on the marker's slot is a landing, not a crossing — d moved as far toward acting sooner as the wheel can express, and it cost nobody a turn. Compare Example 3b, where the shift has further to travel than the distance to the marker, genuinely crosses it, and does cost somebody a turn.*

---

## Example 3b — A positive shift that actually crosses the marker

`a, b, c, d.` a is acting. a plays Initiative Shift +2 on b.

b sits **1** slot from the marker and the shift is **2** — further to travel than the distance to the marker, so b crosses it. There is no slot past "now": b takes an **immediate extra turn** instead. `a, b, c, d` becomes **`b, a, c, d`**, with a **bonus chip** on b and a **skip chip** on a — the combatant displaced off the marker's own slot, in compensation for the extra turn just granted.

**Turn sequence this lap:** a's turn ends → **b goes next** (bonus turn) → **a is skipped** (chip removed) → c goes → d goes.

*Demonstrates the real positive-shift boundary. **Onto the marker's slot buys the next turn; across it buys an extra one, and somebody pays for it.** The displaced-actor skip is compensation for that extra turn — not a rule about landing on the marker's slot. Compare Example 4, where the same displacement happens and nothing is skipped.*

---

## Example 4 — A negative shift landing exactly on the marker's slot

`a, b, c, d.` a plays Initiative Shift −2 on c.

c's clockwise math also lands it exactly on the marker's own slot — but because this is a *negative* shift, the boundary rule is "never sooner," and landing on the marker's slot would mean acting immediately, which is as sooner as it gets. The shift and slide happen in full: `a, b, c, d` becomes `c, b, d, a`. c gets a **skip chip** (not a bonus — a negative shift's target is never granted an early turn). a, displaced off the marker's slot the same way as in Example 3, gets **no chip at all**.

**Turn sequence this lap:** a's turn ends → **c is skipped** (chip removed) → **b goes next** → d goes → **a goes normally** when the marker reaches it.

*Demonstrates the negative-shift wraparound case, and the payoff of comparing it to Example 3b: since c was skipped rather than bonus'd, there was no extra turn to compensate for — so a, despite being displaced exactly the same way, is never skipped. The displaced-actor skip only ever pairs with a bonus turn actually being granted.*

---

## Example 5 — Reshifting a token that already has a pending chip

Continuing from Example 2 (`b, d, c, a`, d holding a skip chip): during b's turn, b plays a card with Initiative Shift +1 on d.

d's pending skip chip is removed — a fresh shift on a chip-holding token cancels whatever was pending, rather than stacking or compounding it. d then resolves under the new shift on its own terms, and nothing about the cancelled chip carries into that.

Resolving it fresh means resolving it by Example 3, because that is the case it is: d sits one slot off the marker and the shift is 1, so it lands exactly on the marker's own slot and **onto is not across**. `b, d, c, a` becomes **`d, b, c, a`**, with **no chips on anyone**.

**Turn sequence:** b's turn ends → **d goes next** → b goes → c goes → a goes.

*Demonstrates that reshifting a chip-holding token doesn't carry over the old shift's unresolved math — it clears the slate and resolves fresh, under whatever case the new shift actually lands in.*

*(History: this example originally read "d goes normally, no bonus, no skip." It was changed on 2026-09-06 to grant a bonus, on the reasoning that landing on the marker's slot was the bonus case. That reasoning is retired as of 2026-09-12 — landing on the marker's slot is a landing, and sooner/later is measured against when a token's own turn would have arrived rather than by ring position. The original reading was right.)*

---

## Example 6 — Shifting yourself on your own turn

`a, b, c, d.` a is acting. a plays **QUICKEN**, Initiative Shift +2 on itself.

a is standing on the marker's slot, so the distance to the marker is **zero** — and by the letter of the crossing rule, every positive shift a makes would cross it and buy an extra turn. **It does not.** Nothing carries you past a point you are standing on, and a has just acted.

Measure it where the rule says to: against when a's own next turn would have arrived. Having acted, that is after all three others. A shift of +2 makes it **two sooner** — after one other instead of three. `a, b, c, d` becomes **`b, a, c, d`**. No chip for anyone.

**Turn sequence:** a's turn ends → b goes next → **a goes again** → c → d.

*Demonstrates the case the crossing rule reads backwards on. A combatant on the marker's slot is at position zero but their next turn is a full table away — read the slot as their place in the queue and every shift on them comes out inverted. The floor is acting next: a +9 here is the same as a +2, because acting after nobody at all is a bonus turn under another name.*

---

## Example 7 — Pushing back whoever is acting

`a, b, c, d.` a is acting and attacks b. b defends with **RETALIATE**, Initiative Shift **-1** on the attacker.

Same trap, mirrored. a has just acted, so a is already last — reading a's slot as its place in the queue says a is first, and moving a "later" would hand a an *earlier* turn.

Measured properly: a's next turn was after three others, and **-1 puts one more turn in front of it**. After four. The ring says it in two motions — a's token slides one slot along, and it is **passed over** the first time the marker reaches it.

**Turn sequence:** a's turn ends → b goes → **a is passed over** → c → d → b → **a goes**. Four others, where three would have gone.

**-2 is after five, -3 is after six.** One more person in front per point, at any table size. A large delay at a small table means being passed over more than once: at a table of three, a -3 is passed over twice and acts again after five others.

*Demonstrates that a negative shift on the current actor is a later turn, not a lost one — which is why `rules/cards.md` carves initiative out of its ban on costing an enemy a whole attack. The turn arrives, and the wheel shows exactly when it will. Nobody earns a bonus turn here and no third party is skipped: that machinery belongs to a shift that crosses the marker, and standing on it is not crossing it.*

---

## What These Examples Demonstrate

- Sliding happens on every shift, boundary case or not — see Example 1.
- **Onto the marker's slot is not across it.** A positive shift that lands exactly on slot 0 just lands there, with no chip for anyone — and the token takes the next turn, because the marker belongs to a slot and hasn't finished with its own (Examples 3 and 5). Only a shift with further to travel than the distance to the marker has crossed (Example 3b).
- **Onto buys the next turn. Across buys an extra one, and the displaced actor pays for it.** That is the entire difference between the two cases.
- **Sooner and later are measured against when a token's own next turn would have arrived**, not by where it sits in the ring. Going last is not acting later.
- **Skip chip:** placed when a negative shift's math would let its target act sooner than allowed (Examples 2 and 4), and on the combatant displaced off the marker's slot when a bonus turn is granted (Example 3b).
- **Bonus chip:** placed only when a positive shift genuinely crosses the marker — its distance greater than the distance to the marker's slot. Removed once the immediate extra turn is taken.
- The displaced-actor skip (3b vs. 4) is compensation for a bonus turn actually granted — not a rule about displacement or about landing on the marker's slot.
- A chip-holding token that gets reshifted loses the old chip and resolves fresh under the new shift (Example 5).
- **A combatant shifting on their own turn is the exception, and it is not a small one** (Examples 6 and 7). They stand on the marker's slot, so its distance is zero and the crossing rule would fire on every shift they touch. Measure against when their own next turn would have arrived — after everyone else — and both directions come out right: +X is X sooner, floored at acting next; -X puts X more turns in front of theirs. No chips either way.
- **There is no table-size correction.** The old "with exactly 3 combatants, reduce X's magnitude by 1" rule is retired as of 2026-09-12. It existed because shifts near the marker were explosive, and the real cause was proximity to the marker rather than slot count — which onto-is-not-across fixes at every size. Three on the wheel now behaves exactly like four, scaled down, and no shift is ever silently reduced to nothing.

---

## Related Documents

- `rules/combat.md` — The Wheel: slot count, sliding, joining and leaving
- `rules/card-glossary.md` — Initiative Shift X: the full rule text these examples illustrate
