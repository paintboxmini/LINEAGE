# A Worked Combat — Briarwoods Road

A complete combat played out beat by beat, with every rule cited as it fires. Written as engine reference — if you are a person or an AI trying to understand how Tales Untold combat actually resolves, read this after `rules/core-rules.md` and `rules/combat.md`.

The scenario is the standard day-2 road encounter: two Briar Scratchers contest the road to Briarwatch (`bestiary/briar-scratcher.md`). The party is Frost and Steele.

**The decks below are illustrative, not canon.** They are built by the table's deck-building conventions (see `rules/cards.md` — Deck Building) to show legal construction. The party's real decks live in `testcampaigndecks/`.

---

## Setup

### The Party

**Frost** — Mind 3 / Body 3 / Soul 3 — **HP 15** *(2 × Body + 9)* — hand size **3** *(= Mind, minimum 2)*
Deck (9 cards, 3R/3B/3G per the stat-matching heuristic):
STRIKE, PUSH, ENDURE / PROFILE, REFRACT, STILLNESS / FLOW, PATIENCE, WITNESS

**Steele** — Mind 3 / Body 4 / Soul 2 — **HP 17** *(2 × Body + 9)* — hand size **3**
Deck (9 cards, 4R/3B/2G):
STRIKE, DEAD HEAT, BRACE, PULL / PROFILE, CALCULATE, DISTRACT / FLOW, MOCKERY

### The Enemies

**Briar Scratcher ×2** — Mind 1 / Body 1 / Soul 2 — **HP 9** — hand size **2** *(Mind 1, floored at the minimum of 2)*
Each runs its own copy of the same 7-card deck (3 signature + 4 core, per the enemy deck convention):
RAKING CUT, SKITTER AWAY, NIP AND TEAR *(signature — `cards/briar-scratcher.md`)* + DART (R), STILLNESS (B), SHADE AWAY (G), FLOW (G)

### Positions

Frost and Steele are walking the road: both **Frontline**. Scratcher A darts out of the briar wall into its **Frontline**. Scratcher B stays in the undergrowth: **Backline**.

### Initiative — 1d6 + Soul

| Combatant | Roll | Total | Resolution |
|-----------|------|-------|------------|
| Frost | 4 | **7** | Tied with A → higher Soul acts first (3 vs 2) → Frost |
| Scratcher A | 5 | **7** | |
| Steele | 3 | **5** | Tied with B → Soul also tied (2 vs 2) → player before enemy → Steele |
| Scratcher B | 3 | **5** | |

**Wheel order: Frost → Scratcher A → Steele → Scratcher B → back to Frost.** There are no rounds — the wheel just keeps turning (`rules/combat.md`, Initiative). "Cycle" below is descriptive shorthand for one lap, used only to organize this document.

**Opening hands:** when initiative is rolled, every combatant draws to hand size (`rules/combat.md`, Turn Structure — a rule this example surfaced; see Edge Cases at the end).

- Frost draws: PROFILE, PATIENCE, STRIKE *(6 cards left in deck)*
- Steele draws: STRIKE, DEAD HEAT, CALCULATE
- Scratcher A draws: RAKING CUT, SKITTER AWAY
- Scratcher B draws: STILLNESS, RAKING CUT

---

## Cycle 1

### Frost's turn

Start of turn: draw to hand size — hand is already full, no draw.

**Action: Play a Card.** Frost attacks Scratcher A with **PROFILE** (Blue, Mind + d4, Range: Both). Range check: Frost Frontline → A Frontline is melee range; PROFILE says Both, so it's legal from anywhere.

A defends: reveals **SKITTER AWAY** (Blue). Both cards are discarded.

**Blue vs Blue — tie.** No damage. Per the tie rule (`rules/combat.md`, Attack Resolution): *attacker's Effect still triggers, then defender's Defensive Bonus triggers.*

- PROFILE Effect: *"Scry 2, then draw 1 card."* Frost looks at his top two — PUSH and REFRACT — puts REFRACT on top, and draws it. Note that the scry and the draw are Frost's alone: a card granting them to "your allies" would *exclude* Frost (**You Are Not Your Own Ally**, `rules/cards.md`) — unless it were green; green counts itself among its allies.
- SKITTER AWAY Defensive Bonus: A gains **Evade** (50% to dodge the next attack against it — `rules/card-glossary.md`).

Neither trigger cancels the other, so both resolve. Frost's hand: PATIENCE, STRIKE, REFRACT.

### Scratcher A's turn

Start of turn: draws to hand size 2 → draws NIP AND TEAR. Hand: RAKING CUT, NIP AND TEAR.

**Action:** A attacks Frost with **RAKING CUT** (Red, Body + d2, Melee — both Frontline, legal).

Frost chooses to defend. **Reveals are simultaneous — defending is a prediction, not a reaction.** A defended with Blue last time, so Frost reads it as a Mind-leaning creature and reveals **PATIENCE** (Green), hoping Green would beat Blue. A played Red.

**Red beats Green — attacker wins.** Damage: Body 1 + d2 *(rolls 1)* = **2**. Frost 15 → 13. RAKING CUT Effect: *shuffle 1 Wound into target's deck.* Frost's deck is now 6 cards: PUSH, ENDURE, STILLNESS, FLOW, WITNESS, **WOUND**.

This is the Scratcher doing exactly what it exists to do — the 2 damage is nothing; the Wound is the attack (`bestiary/briar-scratcher.md`, Tactical Purpose).

Frost's hand: REFRACT, STRIKE.

### Steele's turn

Draws to 3 — hand already full.

**Action:** Steele attacks Scratcher A with **STRIKE** (Red, Body + d8, Melee — both Frontline, legal).

A has **Evade** from cycle 1. Evade resolves *before the defender chooses a card*: roll 1d2 → **1, the attack misses entirely.** The Evade stack is spent. STRIKE was already played and discarded in step 1 of attack resolution, so the card is gone. *(Ruling — see Edge Cases.)* No damage, no Effect, A never had to commit a card.

Steele's hand: DEAD HEAT, CALCULATE.

### Scratcher B's turn

Draws to 2 — hand already full (STILLNESS, RAKING CUT).

B is Backline and wants to use RAKING CUT — but it's **Melee, and melee requires both combatants in the Frontline** (Range Matrix, `rules/combat.md`). Illegal from where B stands. Instead:

**Action:** B attacks Frost with **STILLNESS** (Blue, Mind + d2, Ranged). Range check: Backline → Frontline is not melee range, so Ranged is legal.

Frost holds REFRACT and STRIKE, and wants both for his own turn. Max incoming damage here is Mind 1 + d2 = 3. **Frost declines to defend.** Per resolution step 3: *no defense → attacker wins automatically* — and an automatic win is a full win. Damage: 1 + d2 *(rolls 2)* = **3**. Frost 13 → 10. STILLNESS Effect: *defender discards 1 card at random* — d2 picks **STRIKE**. Declining to defend saved a card and cost a card; the gamble is real.

Frost's hand: REFRACT.

---

## Cycle 2

### Frost's turn

Draws to 3 → draws 2 from his 6-card deck: ENDURE and the **WOUND**. Hand: REFRACT, ENDURE, WOUND.

The Wound arrives. It **cannot be played** and — unlike a normal card — it does not leave on its own. It sits in Frost's hand taking up a slot until he spends an action to discard it or clears it on a short rest (`rules/card-glossary.md`, Status Cards). Frost is effectively playing this turn with a 2-card hand, and it stays that way until he pays to fix it. That's the whole Scratcher lesson, two turns after the claw landed.

**Action:** Frost attacks Scratcher A with **ENDURE** (Red, Body + d2, Both). A's hand is just NIP AND TEAR; it reveals it — **Green. Red beats Green — attacker wins.** Damage: Body 3 + d2 *(rolls 2)* = **5**. A: 9 → 4. ENDURE Effect: Frost gains **Resist** (next successful enemy attack against him deals half damage, rounded down).

Note what Frost could *not* do: his REFRACT (Ranged) is unplayable as an attack against A — Frontline vs Frontline **is** melee range, and Ranged only works when you're not in melee range with the target. In melee it's only good to him as a defense reveal.

End of turn: the **WOUND stays in hand** — it isn't going anywhere until Frost pays to remove it. Frost's hand: REFRACT, WOUND.

### Scratcher A's turn

Hand empty → draws 2: DART, SHADE AWAY. A is at 4 HP and has been cut once — it wants one more mark before it leaves.

**Action:** A attacks Frost with **SHADE AWAY** (Green, Soul + d2, Melee — legal). Frost defends with **REFRACT** (Blue), predicting another Red claw. **Green beats Blue — attacker wins.**

Damage: Soul 2 + d2 *(rolls 1)* = 3 — but Frost has **Resist**: half rounded down → **1**. Frost 10 → 9. Resist expires. SHADE AWAY Effect: A gains Evade.

### Steele's turn

Draws to 3 → draws BRACE. Hand: DEAD HEAT, CALCULATE, BRACE.

**Action:** Steele attacks Scratcher B with **DEAD HEAT** (Red, Body + d6, Ranged). Range check: Frontline → Backline is not melee range — Ranged is legal. B's only card is RAKING CUT; it reveals it — **Red.**

**Red vs Red — tie.** No damage. Now the tie ordering matters:

1. Attacker's Effect first: DEAD HEAT — *"If this attack ties, the defender's Defensive Bonus does not trigger."*
2. Defender's Defensive Bonus: RAKING CUT would shuffle a Wound into Steele's discard — **canceled.**

This is the exact clause in the tie rule: *"If the Effect cancels the Defensive Bonus, the Defensive Bonus does not trigger"* (`rules/combat.md`). Steele traded a tied attack for dodging a Wound. B's hand is now empty.

### Scratcher B's turn

Draws to 2: SKITTER AWAY, NIP AND TEAR.

NIP AND TEAR is Melee and B is still Backline. **Action: Move Position** — B crosses into its Frontline. Moving costs the whole action (`rules/combat.md`, Turn Structure); B does nothing else this turn. Committing to the Frontline is a real decision — next cycle it can claw, and be clawed.

---

## Cycle 3 — The Disengage

### Frost's turn

REFRACT went to the discard pile defending last cycle, so Frost starts this turn holding only the **WOUND**. He draws to 3 — but the Wound occupies a slot, so he draws only two real cards, PUSH and STILLNESS, and never reaches FLOW or WITNESS, which stay buried in his deck. Hand: PUSH, STILLNESS, WOUND — two cards he can actually play. That's the Wound's real cost: not the 2 damage that put it there, but the card it's quietly keeping out of his hand every turn until he spends an action to be rid of it. Frost is at 9 HP and carrying a passenger he can't put down until the party rests.

**Action:** Frost attacks B — both Frontline now — with **PUSH** (Red, Body + d6, Melee). B reveals **SKITTER AWAY** (Blue). **Blue beats Red — defender wins.** No damage. Defensive Bonus: B gains **Evade**.

### Scratchers A and B — the exit

A Scratcher fight doesn't end in a kill. They mark and they leave (`bestiary/briar-scratcher.md`: *"They're not trying to win. They're marking."*).

On A's turn it bolts for the briar wall — moving out of the combat area entirely. Movement in Tales Untold is abstract: leaving the field ends your participation in combat, and if every enemy leaves, **combat is over** (they can re-engage later if the fiction demands). B follows on its turn, Evade unspent, gone between two heartbeats.

Note the asymmetry: enemy disengagement is a GM call, made from behavior — Scratchers leave because leaving is what Scratchers do. A *player* trying to exit combat under pressure uses the **Flee** action: 2d10 + Soul vs DC 10 + highest enemy Soul, GM-adjusted for the fiction (`rules/combat.md`, Fleeing Combat). The world doesn't owe the party the same clean exit it gives its animals.

No initiative to unwind, no cleanup step. The wheel simply stops mattering.

---

## After the Fight

| | HP | Deck state |
|---|----|-----------|
| Frost | 9 / 15 | **1 Wound** clogging his hand — stays until he spends an action to discard it or clears it on a short rest (1 per rest) |
| Steele | 17 / 17 | Clean — Dead Heat's tie denial dodged the only Wound aimed at him |
| Scratcher A | 4 / 9 | Gone |
| Scratcher B | 9 / 9 | Gone — never took a hit |

Frost's Wound doesn't heal with HP, and it won't leave until he spends a whole action on it or takes a short rest. It rides in his deck into Briarwatch and the Hollow below it, surfacing into his hand to eat a slot every time it's drawn (`quests/hollow-below-briarwatch.md`). Two more Scratcher encounters without a rest and the party's decks — not their HP bars — are the wounded thing.

---

## What This Example Demonstrated

- **Initiative:** 1d6 + Soul; ties break by higher Soul, then player-before-enemy; the order is a wheel with no rounds.
- **Turn economy:** draw to hand size (Mind, minimum 2) at start of turn, then exactly one action — attack, move, item, Rushdown, interact, or flee.
- **All four resolution outcomes:** attacker win (damage + Effect), defender win (no damage + Defensive Bonus), tie (no damage, Effect then Defensive Bonus — including the cancellation clause), and the automatic win when the defender declines.
- **Simultaneous reveal:** defense is a prediction. Frost guessed wrong twice; that's the game.
- **Range is positional law:** melee needs both Frontline; Ranged fails inside melee range; Both is always legal. B lost a full turn crossing the field to get claw-range.
- **Status flow:** Evade (spent on one attack, whether or not it dodges), Resist (halves one hit), and the Wound life cycle — shuffled into the deck, drawn into the hand where it occupies a slot and *stays*, cleared only by spending an action or taking a short rest.
- **You Are Not Your Own Ally** unless the card says "you and" — green being the standing exception: green counts itself among its allies (`rules/cards.md`).

---

## Edge Cases This Example Surfaced

All four were reviewed and resolved by Drew. Recorded here because the reasoning is part of the reference:

1. **Opening hands.** The rules said only that you draw at the start of your turn — nothing gave combatants cards before their first turn, which would have made everyone acting late in cycle 1 defenseless. Resolved: **everyone draws to hand size when initiative is rolled** — now canonical in `rules/combat.md`, Turn Structure.
2. **Evade vs the attacker's card.** The attack card is played and discarded at step 1; Evade resolves after. Resolved: **a dodged attack still consumes the attacker's card** (and its Effect does not trigger).
3. **Defensive Bonuses that reference the attack's damage** (e.g., REFRACT's redirect) fire on a defender win, when no damage was dealt. Surfaced while scripting, though the final example doesn't exercise it. Resolved: **roll the attack's damage anyway to resolve the redirect.**
4. **Does a tie count as "successfully defending"?** Cards like WITNESS trigger on a successful defense. A tie prevents all damage and fires the Defensive Bonus, but the defender didn't *win*. **Resolved per-card, not universally:** WITNESS now states on the card that a tie counts. Future cards that care about "successful defense" carry their own clarifying line; if every card ends up ruling the same way, the convention gets promoted to a universal rule.

---

## Related Documents

- `rules/core-rules.md` — the quick reference this example animates
- `rules/combat.md` — full combat rules
- `rules/card-glossary.md` — canonical keyword definitions
- `rules/cards.md` — card anatomy and deck-building conventions
- `bestiary/briar-scratcher.md`, `cards/briar-scratcher.md` — the enemies used here
