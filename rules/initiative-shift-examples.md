# The Wheel & Initiative Shift — Worked Examples

Compact worked cases for the Wheel and Initiative Shift, in the notation Drew and Claude settled on while building the mechanic: four combatants, `a` through `d`, listed clockwise starting from whoever's currently acting. Read `rules/combat.md` (The Wheel) and `rules/card-glossary.md` (Initiative Shift X) first — this file exists to make those rules concrete, not to restate them.

Every case below was worked through and confirmed directly; none of it is invented to fill a gap. See `memory.md`'s threshold log for the sessions these came from if the reasoning behind a specific ruling matters.

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

`a, b, c, d.` a plays Initiative Shift +3 on d.

d's counterclockwise math lands it exactly on the marker's own slot — the point where "act sooner" runs out of room, since there's no slot before "now." The shift and slide happen in full: `a, b, c, d` becomes `d, a, b, c`, with a **bonus chip** placed on d. a — the combatant just displaced off the marker's own slot to make room — gets a **skip chip**.

**Turn sequence this lap:** a's turn ends → **d goes next** (bonus turn) → **a is skipped** (chip removed) → b goes → c goes. Next lap, the new order (`d, a, b, c`) runs normally.

*Demonstrates the positive-shift wraparound case, and confirms the skip on the displaced combatant (a) is specifically compensation for the bonus turn just granted to the arriving token (d) — not a blanket rule about landing on the marker's slot. Compare Example 4, where the same displacement happens but nothing gets skipped.*

---

## Example 4 — A negative shift landing exactly on the marker's slot

`a, b, c, d.` a plays Initiative Shift −2 on c.

c's clockwise math also lands it exactly on the marker's own slot — but because this is a *negative* shift, the boundary rule is "never sooner," and landing on the marker's slot would mean acting immediately, which is as sooner as it gets. The shift and slide happen in full: `a, b, c, d` becomes `c, b, d, a`. c gets a **skip chip** (not a bonus — a negative shift's target is never granted an early turn). a, displaced off the marker's slot the same way as in Example 3, gets **no chip at all**.

**Turn sequence this lap:** a's turn ends → **c is skipped** (chip removed) → **b goes next** → d goes → **a goes normally** when the marker reaches it.

*Demonstrates the negative-shift wraparound case, and the payoff of comparing it to Example 3: since c was skipped rather than bonus'd, there was no extra turn to compensate for — so a, despite being displaced exactly the same way, is never skipped. The displaced-actor skip only ever pairs with a bonus turn actually being granted.*

---

## Example 5 — Reshifting a token that already has a pending chip

Continuing from Example 2 (`b, d, c, a`, d holding a skip chip): during b's turn, b plays a card with Initiative Shift +1 on d.

d's pending skip chip is removed — a fresh shift on a chip-holding token cancels whatever was pending, rather than stacking or compounding it. d then resolves under the new shift on its own terms: **d goes normally when the marker reaches it**, no bonus, no skip.

*Demonstrates that reshifting a chip-holding token doesn't carry over the old shift's unresolved math — it clears the slate and resolves fresh.*

---

## What These Examples Demonstrate

- Sliding happens on every shift, boundary case or not — see Example 1.
- **Skip chip:** placed when a shift's math would let its target act sooner than allowed (either a negative-shift overshoot, or either direction landing exactly on the marker's slot when the target isn't the one earning a bonus). Removed the first time the marker reaches that token; the turn is skipped.
- **Bonus chip:** placed only when a *positive* shift's math would require its target to act at a point already past — practically, landing exactly on the marker's own slot. Removed once the immediate extra turn is taken.
- The displaced-actor skip (Examples 3 vs. 4) is compensation for a bonus turn actually granted — not a rule about displacement or about landing on the marker's slot on its own.
- A chip-holding token that gets reshifted loses the old chip and resolves fresh under the new shift (Example 5).

---

## Related Documents

- `rules/combat.md` — The Wheel: slot count, sliding, joining and leaving
- `rules/card-glossary.md` — Initiative Shift X: the full rule text these examples illustrate
- `rules/combat-example.md` — a full combat walked beat by beat, in the same reference style
