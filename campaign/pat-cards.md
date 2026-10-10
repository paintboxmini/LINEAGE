# Pat's Custom Cards

Three custom cards, drawn from a list of ideas Pat gave Drew — the rest of his 9-card starting deck comes from the normal Oracle draft (`campaign/pat.md`, Deck).

**They have landed: `cards/pat.md` is the card, this file is the argument for it.** Both copies are worth keeping — the reasoning here is not something a printed card can carry — and they must not drift. `python3 agent-tools/check-card-drift.py` is what notices when they do.

---

## Card 1 — a pure stall card

Colorless, and it never loses on defense — but it never wins on offense either. Pure risk removal, no guaranteed damage; that trade is the whole card, and what Pat actually agreed to when he picked it.

**Mechanism:** its Special Rule makes it take on whatever color it's resolving against, revealed simultaneously — which means it always ties in RPS (same color never wins or loses against itself). Its Defense Effect reads **you win on a tie**, so a guaranteed tie becomes a guaranteed block when defending. Its Attack Effect is blank — a guaranteed tie with nothing to convert it stays a tie. **Since ties started landing the hit (`rules/combat.md`, Attack Resolution, 2026-10-03), that makes it a sure d4 as an attack** — no stat behind it, and the defender's Defense Effect always fires in return. It was written as pure defense, zero offense; under the new tie rule it is pure defense and a weak attack that never misses on colour. **Kept as written** *(Drew, 2026-10-03)* — the sure d4 is fine, and the card does not change.

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

**One thing it costs, found 2026-09-19 while building his deck for the simulator — and it is smaller than this file used to say** *(corrected 2026-09-27)*. **Deck size is total stats and that part is fixed**: Pat runs nine cards, and HOLD THE LINE is colorless, so it fills a slot belonging to no colour. He is Mind 2 / Body 3 / Soul 4, so the eight that remain cannot also be 2 Blue / 3 Red / 4 Green.

**There is no rule collision here.** `rules/cards.md`, Deck Building calls the colour match **a heuristic, not a law** — in as many words, and it says drafting through the Oracle can and should bend it. *The earlier version of this paragraph cited that section as though matching were binding and concluded the two could not both hold. Only one of them was ever binding.*

**So it is a live choice rather than a problem to solve.** Green is the obvious place to give the slot up at 4; Blue at 2 is where losing one hurts most. *Worth Pat knowing before the draft so the pick is deliberate, and worth nobody treating as a fault on the card.*

**Where this lands in canon later:** `cards/colorless.md`, alongside AFTERIMAGE, FOLLOW-UP, and BECOMING — same shape (a colorless card that determines its actual color only at reveal, per its own text) and the same override of the generic colorless rule (`cards/colorless.md`'s own header: "a colorless card auto-loses to any card with a real color" — this one doesn't, by design, since by reveal it's no longer resolving as colorless at all).

---

## Card 2 — HERE BOY

Green — Soul, d4, Both range. First concrete trigger for Wild Magic Summoning (`campaign/pat.md`).

```
HERE BOY
GREEN — SOUL
Attack: Soul + d4
Effect: Summon a spirit to your position. It carries the Ongoing Effect: the next time you tie in RPS, you win instead.
Defense Effect: Same as Effect.
Range: Both
"Here, boy. Come stand with me."
```

Win or tie, attacking or defending, this triggers the same — a normal Green card in every other way, no gimmick like Card 1's.

***Pat spends it, the spirit holds it.*** Ruled over two passes and both halves matter.

*Who spends it, 2026-09-19.* The earlier wording — *"It gains the Ongoing Effect: the next time it ties in RPS, it wins instead"* — read as the spirit, which cannot use it: a spirit is an Object that does not act and cannot choose a defence, so it never reaches an RPS reveal at all. **Pat holds the charge**, and spends it on the next tie he is actually in, attacking or defending.

*Who holds it, 2026-09-21.* **Kill the totem, lose the effect**, exactly as LET'S GO already worked. Before this, HERE BOY's spirit was a body with HP and no purpose while LET'S GO's was a totem worth defending — two summons on one sheet doing different kinds of thing, for no reason anybody had written down. Now both are worth standing in front of, and an enemy that wants Pat to stop winning ties has something it can actually do about it.

**A spent charge is not clawed back.** If the tie has already happened, killing the spirit afterwards takes nothing — it can only remove one that is still waiting. The HP roll isn't restated here since Wild Magic Summoning already covers it for every summon regardless of trigger.

**Answers one of the open questions on Wild Magic Summoning:** this is at least one real trigger. The spirit itself doesn't act — it's an Object, not a combatant, no turn and no wheel token (`campaign/pat.md`, Wild Magic Summoning). **The other one closed on 2026-09-27: the cap is three spirits, because there are three royals** — which means HERE BOY's spirit and LET'S GO's can stand at the same time, and with only two triggers on the sheet two is as far as it goes. Still open: whether these are the *only* two triggers.

---

## Card 3 — LET'S GO

Red — Body, d4, Both range. Second trigger for Wild Magic Summoning, and the aggressive counterpart to HOLD THE LINE's pure defense.

```
LET'S GO
RED — BODY
Attack: Body + d4
Effect: Summon a spirit. It carries the Ongoing Effect: you and all allies deal +2 damage this combat.
Defense Effect: All enemies make a Soul Save, DC = your Soul stat + 10. Anyone who fails must attack you on their next turn. Anyone who fails and can't attack you must instead move toward you or Rushdown.
Range: Both
"Come get me. Every one of you."
```

Confirmed: the damage buff dies with the spirit, and the Save is a Soul Save. **Tying the buff to the totem is the whole point of it** — it gives an enemy a real reason to spend a turn on the spirit instead of on Pat or an ally, which is what makes the summon a piece of the battlefield rather than a stat line. *(That sentence used to sit inside the card block; it is a designer's note rather than rules text, so it reads here and the printed card carries only what a player needs at the table.)*

**"Move toward you or Rushdown" turned out not to be a self-targeting question at all** — Rushdown was never "you do something to an enemy" in the first place. Its actual fiction: the Frontline isn't a fixed zone, it's wherever opposing sides are actually face to face — Rushdown is just closing that distance yourself, and the enemy you close it against becomes Frontline because that's now where the fight is happening. So a compelled creature that's Frontline and needs to reach a Backline Pat can Rushdown him directly, completely within the existing rule — Pat is a valid Backline enemy target from their side of the field. No carve-out needed. (Worth knowing: `rules/combat.md`'s own Positioning section still reads more like fixed opposing zones than this — not something to fix off one card, just flagging that the fiction described here is looser and more accurate than the current wording.)

---

## For advancement — STAY, GOOD BOY and SPEAK

**None of Pat's summon cards restate the summoning rules** *(Drew, 2026-10-04)*. The d10, the effect ending when the spirit falls, and the three-spirit cap all live on his Trait and apply to every one of them (`campaign/pat.md`, Wild Magic Summoning), so the cards say only what is different about each.

*Written 2026-10-04 at Drew's ask, from what Pat wants: more summons, winning ties, buying time. **Not in his starting nine** — they go into his advancement deck as two of its three customs (`campaign/session-1-cards.md`, The advancement decks). **Both are dog calls**, the same as HERE BOY and LET'S GO: Caine talks to his dead the way a man talks to a dog he trusts.*

### Card 4 — STAY

Blue — Mind, d4, Both. A summon that buys time.

```
STAY
BLUE — MIND
Attack: Mind + d4
Effect: Summon a spirit to your position. It carries the Ongoing Effect: when you or an ally in your position would take attack damage, the spirit takes as much of it as its HP allows, and the rest lands as normal.
Defense Effect: Same as Effect.
Range: Both
"Stay. Good. Stay."
```

- **The spirit's HP is the shield, and the d10 finally matters.** Every point it rolled is a point of somebody else's damage it can eat, and when it runs out the effect is gone because the spirit is. *A 9 holds a fight; a 2 takes the edge off one hit.*
- **It is a reassignment, the first step of the damage pipeline** — the same step Protect uses (`rules/combat.md`, Damage Pipeline) — so Armour and Resist apply to whoever actually takes it. **Unpreventable damage goes past it**, because it was never attack damage.
- **Blue, on purpose.** His three starters are colourless, Green and Red, so a Blue custom gives him one in every colour, and Blue is the colour that helps allies.
- *On defence the spirit arrives after the hit that summoned it*, because a Defense Effect resolves after damage on a tie. It guards the next one.

### Card 5 — GOOD BOY

Green — Soul, d4, Both. The summon that pays off winning ties.

```
GOOD BOY
GREEN — SOUL
Attack: Soul + d4
Effect: Summon a spirit to your position. It carries the Ongoing Effect: whenever you win on a tie, draw 1.
Defense Effect: Same as Effect.
Range: Both
"Who's a good boy."
```

- **"Win on a tie" is anything that turns a tie into your win**: HOLD THE LINE's block, HERE BOY's held charge, and ADAPT or another tie-winner once the middle tier opens (`cards/tiers/middle.md`).
- **With HOLD THE LINE it is a card every time he blocks with it.** That is the synergy he asked for, and it is also why it is a draw and not damage — card flow for a stall deck, not a second way to win.
- **It does nothing alone.** No tie-winner in hand, no payoff. *Which is the honest shape for a synergy card.*

### Card 6 — SPEAK

Red — Body, d6, Both. Not a summon — **the card that pays for having them out**, and buys time while it does.

```
SPEAK
RED — BODY
Attack: Body + d6
Effect: The defender gains Weak. If you have two or more spirits out, all enemies in the defender's position gain Weak instead.
Defense Effect: The attacker gains Weak for each spirit you have out.
Range: Both
"Speak. Let them hear all of you."
```

**The three cursed royals have a voice, and this is when they use it.** Another dog call, like the rest of his customs.

- **Buying time, in the currency of the hits that come back at him.** Weak takes a d6 off the next damage roll (`rules/card-glossary.md`, Weak), so every stack is one blunted attack.
- **It scales with the spirits, not on its own.** Alone it is ENFEEBLE's effect at a Red die (`cards/blue-mind.md`). With two spirits out the attack spreads Weak across a whole position, and **the block hands the attacker a stack for every spirit** — three weakened swings from one block, with all three royals standing.
- **No tie-winning on it, on purpose.** "You win on a tie" is what the middle tier is for (`cards/tiers/middle.md`), and his advancement deck comes before that. *The ties are HOLD THE LINE's and HERE BOY's job; this one rewards the summons.*
- **Red, Both, d6** — a step over Red Both's usual die (`rules/cards.md`, Why Red has the biggest dice — range pays for them), paid for by an effect that does little until the field is built. **And Red is where his deck already lives**: five of his nine.

---

## Related Documents

- `campaign/pat.md` — the character this deck belongs to, Wild Magic Summoning
- `cards/colorless.md` — the three existing colorless cards Card 1 will sit alongside
- `rules/combat.md` — Reading a Card, Attack Resolution, Initiative (summoned combatants)
