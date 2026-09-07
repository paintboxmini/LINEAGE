# Pat's Custom Cards

Three custom cards, drawn from a list of ideas Pat gave Drew — the rest of his 9-card starting deck comes from the normal Oracle draft (`experimental/pat.md`, Deck). Draft, staged here before landing in `cards/`.

---

## Card 1 — a pure stall card

Colorless, and it never loses on defense — but it never wins on offense either. Pure risk removal, no guaranteed damage; that trade is the whole card, and what Pat actually agreed to when he picked it.

**Mechanism:** its Special Rule makes it take on whatever color it's resolving against, revealed simultaneously — which means it always ties in RPS (same color never wins or loses against itself). Its Defense Effect reads **you win on a tie**, so a guaranteed tie becomes a guaranteed block when defending. Its Attack Effect is blank — a guaranteed tie with nothing to convert it stays a tie, meaning it never deals damage as an attack. Pure defense, zero offense, by design.

Working name: **HOLD THE LINE** — fits Pat's own backstory (a soldier trained under his Captain father) as much as it fits the mechanic. Open to a different name if this doesn't land for Pat.

```
HOLD THE LINE
COLORLESS
Attack: d4 — no stat bonus, colorless
Effect: None
Defense Effect: You win on a tie.
Range: Both
Special Rule: Upon simultaneous reveal, this card's color becomes identical to whatever it's resolving against — meaning it always ties, never wins or loses on color alone.
"Wherever you plant your feet, that's where I plant mine."
```

**Where this lands in canon later:** `cards/colorless.md`, alongside AFTERIMAGE, FOLLOW-UP, and BECOMING — same shape (a colorless card that determines its actual color only at reveal, per its own text) and the same override of the generic colorless rule (`cards/colorless.md`'s own header: "a colorless card auto-loses to any card with a real color" — this one doesn't, by design, since by reveal it's no longer resolving as colorless at all).

---

## Card 2 — HERE BOY

Green — Soul, d4, Both range. First concrete trigger for Wild Magic Summoning (`experimental/pat.md`).

```
HERE BOY
GREEN — SOUL
Attack: Soul + d4
Effect: Summon a spirit to your position (Wild Magic Summoning — roll a d10 for its HP). It gains the Ongoing Effect: the next time it ties in RPS, it wins instead.
Defense Effect: Same as Effect.
Range: Both
"Here, boy. Come stand with me."
```

Win or tie, attacking or defending, this triggers the same — a normal Green card in every other way, no gimmick like Card 1's. The HP roll isn't restated here since Wild Magic Summoning already covers it for every summon regardless of trigger.

**Answers one of the open questions on Wild Magic Summoning:** this is at least one real trigger. The spirit itself doesn't act — it's an Object, not a combatant, no turn and no wheel token (`experimental/pat.md`, Wild Magic Summoning). Still open: whether HERE BOY is the *only* trigger, and whether more than one spirit can be out at once given there are only three to draw from.

---

## Card 3 — LET'S GO

Red — Body, d4, Both range. Second trigger for Wild Magic Summoning, and the aggressive counterpart to HOLD THE LINE's pure defense.

```
LET'S GO
RED — BODY
Attack: Body + d4
Effect: Summon a spirit (Wild Magic Summoning — roll a d10 for its HP). It carries the Ongoing Effect: you and your allies deal +2 damage this combat. **This buff is tied to the spirit's survival — kill the totem, lose the buff.** A real reason for an enemy to target the spirit instead of Pat or an ally.
Defense Effect: Every enemy makes a Soul Save, DC = your Soul stat + 10. Anyone who fails must attack you on their next turn. Anyone who fails and can't attack you must instead move toward you or Rushdown.
Range: Both
"Come get me. Every one of you."
```

Confirmed: the damage buff dies with the spirit, and the Save is a Soul Save.

**"Move toward you or Rushdown" turned out not to be a self-targeting question at all** — Rushdown was never "you do something to an enemy" in the first place. Its actual fiction: the Frontline isn't a fixed zone, it's wherever opposing sides are actually face to face — Rushdown is just closing that distance yourself, and the enemy you close it against becomes Frontline because that's now where the fight is happening. So a compelled creature that's Frontline and needs to reach a Backline Pat can Rushdown him directly, completely within the existing rule — Pat is a valid Backline enemy target from their side of the field. No carve-out needed. (Worth knowing: `rules/combat.md`'s own Positioning section still reads more like fixed opposing zones than this — not something to fix off one card, just flagging that the fiction described here is looser and more accurate than the current wording.)

---

## Related Documents

- `experimental/pat.md` — the character this deck belongs to, Wild Magic Summoning
- `cards/colorless.md` — the three existing colorless cards Card 1 will sit alongside
- `rules/combat.md` — Reading a Card, Attack Resolution, Initiative (summoned combatants)
