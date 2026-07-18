# A Worked Combat — The Road to Briarwatch

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

**Briar Scratcher ×2** — Mind 1 / Body 1 / Soul 2 — **HP 11** *(2 × Body + 9)* — hand size **2** *(Mind 1, floored at the minimum of 2)*
Each runs its own copy of the same **4-card deck** *(deck size = total stats = 1+1+2; color counts = each stat: 1R/1B/2G)*, 3 signature + 1 core to fill:
RAKING CUT, SKITTER AWAY, NIP AND TEAR *(signature — `cards/briar-scratcher.md`)* + SHADE AWAY (G, core)

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

**Opening hands:** when initiative is rolled, every combatant draws to hand size (`rules/combat.md`, Turn Structure).

- Frost draws: PROFILE, PATIENCE, STRIKE *(6 cards left in deck)*
- Steele draws: STRIKE, DEAD HEAT, CALCULATE
- Scratcher A draws: RAKING CUT, SKITTER AWAY *(2 cards left: NIP AND TEAR, SHADE AWAY)*
- Scratcher B draws: SKITTER AWAY, RAKING CUT *(2 cards left: NIP AND TEAR, SHADE AWAY)* — B needs the one Both-range card in the deck to threaten anything from Backline, and gets it.

---

## Cycle 1

### Frost's turn

Start of turn: draw to hand size — hand is already full, no draw.

**Action: Play a Card.** Frost attacks Scratcher A with **PROFILE** (Blue, Mind + d4, Range: Both). Range check: Frost Frontline → A Frontline is melee range; PROFILE says Both, so it's legal from anywhere.

A defends: reveals **SKITTER AWAY** (Blue, Range: Both — legal regardless of position). Both cards are discarded.

**Blue vs Blue — tie.** No damage. Per the tie rule (`rules/combat.md`, Attack Resolution): *attacker's Effect still triggers, then defender's Defensive Bonus triggers.*

- PROFILE Effect: *"Scry 2, then draw 1 card."* Frost looks at his top two — PUSH and REFRACT — puts REFRACT on top, and draws it.
- SKITTER AWAY Defensive Bonus: A gains **Evade** (50% to dodge the next attack against it — `rules/card-glossary.md`).

Neither trigger cancels the other, so both resolve. Frost's hand: PATIENCE, STRIKE, REFRACT.

A's hand after playing SKITTER AWAY: RAKING CUT. A's deck: NIP AND TEAR, SHADE AWAY.

### Scratcher A's turn

Start of turn: draws to hand size 2 → draws NIP AND TEAR. Hand: RAKING CUT, NIP AND TEAR. A's deck: SHADE AWAY.

**Action:** A attacks Frost with **RAKING CUT** (Red, Body + d2, Melee — both Frontline, legal).

Frost chooses to defend. **Reveals are simultaneous — defending is a prediction, not a reaction.** A defended with Blue last time, so Frost reads it as a Mind-leaning creature and reveals **PATIENCE** (Green, Range: Melee — legal, both Frontline), hoping Green would beat Blue. A played Red.

**Red beats Green — attacker wins.** Damage: Body 1 + d2 *(rolls 1)* = **2**. Frost 15 → 13. RAKING CUT Effect: *insert 1 Injury at the bottom of target's deck.* Frost's deck is now 6 cards, INJURY on the bottom: PUSH, ENDURE, STILLNESS, FLOW, WITNESS, **INJURY**.

This is the Scratcher doing exactly what it exists to do — the 2 damage is nothing; the Injury is the attack (`bestiary/briar-scratcher.md`, Tactical Purpose).

Frost's hand: STRIKE, REFRACT. A's hand: NIP AND TEAR.

### Steele's turn

Draws to 3 — hand already full.

**Action:** Steele attacks Scratcher A with **STRIKE** (Red, Body + d8, Melee — both Frontline, legal).

A has **Evade** from this cycle. Evade resolves *before the defender chooses a card*: roll 1d2 → **1, the attack misses entirely.** The Evade stack is spent. STRIKE was already played and discarded in step 1 of attack resolution, so the card is gone. *(Ruling — see Edge Cases.)* No damage, no Effect, A never had to commit a card.

Steele's hand: DEAD HEAT, CALCULATE.

### Scratcher B's turn

Draws to 2 — hand already full (SKITTER AWAY, RAKING CUT).

B is Backline and wants to use RAKING CUT — but it's **Melee, and melee requires both combatants in the Frontline** (Range Matrix, `rules/combat.md`). Illegal from where B stands. Instead:

**Action:** B attacks Frost with **SKITTER AWAY** (Blue, Mind + d2, Ranged: Both). Range check: Backline → Frontline is not melee range, so Both is legal.

Frost holds REFRACT and STRIKE, and wants both for his own turn. Max incoming damage here is Mind 1 + d2 = 3. **Frost declines to defend.** Per resolution step 3: *no defense → attacker wins automatically.* Damage: 1 + d2 *(rolls 2)* = **3**. Frost 13 → 10. SKITTER AWAY Effect: *after attack, may reposition* — B declines; Backline is already exactly where it wants to be. Unlike a discard effect, this doesn't touch Frost's hand.

Frost's hand: STRIKE, REFRACT *(unchanged)*. B's hand: RAKING CUT. B's deck: NIP AND TEAR, SHADE AWAY.

---

## Cycle 2

### Frost's turn

Draws to 3 → draws 1 from his 6-card deck: the **INJURY**.

The Injury arrives. It **cannot be played** and — unlike a normal card — it does not leave on its own. It sits in Frost's hand taking up a slot until he spends an action to discard it or clears it on a short rest (`rules/card-glossary.md`, Status Cards). Frost's hand: STRIKE, REFRACT, INJURY — two cards he can actually play.

**Action:** Frost attacks A with **STRIKE** (Red, Body + d8, Melee — both Frontline, legal). A's hand is just NIP AND TEAR; it reveals it — **Green** (Range: Melee, legal). **Red beats Green — attacker wins.** Damage: Body 3 + d8 *(rolls 2)* = **5**. A: 11 → 6. STRIKE Effect: None.

End of turn: the **INJURY stays in hand.** Frost's hand: REFRACT, INJURY. A's hand: empty. A's deck: SHADE AWAY.

### Scratcher A's turn

Hand empty → draws to 2. A's deck has one card: draws **SHADE AWAY** — deck now empty, still one short of hand size. **"If your deck is empty, shuffle your discard pile into a new deck before drawing"** (`rules/combat.md`, Turn Structure) — A's discard (SKITTER AWAY, RAKING CUT, NIP AND TEAR) reshuffles into a fresh 3-card deck, and A draws again: **RAKING CUT**. Hand: SHADE AWAY, RAKING CUT. A's deck: SKITTER AWAY, NIP AND TEAR — the 4-card deck is small enough to genuinely cycle mid-fight, which the old 7-card version never surfaced.

**Action:** A attacks Frost with **SHADE AWAY** (Green, Soul + d2, Melee — both Frontline, legal).

Frost's hand is REFRACT and INJURY. REFRACT is **Ranged**, and both combatants are Frontline — melee range applies, so a Ranged card cannot defend here (`rules/card-glossary.md`, Range; the same rule that gates attacking gates defending too). INJURY cannot be played at all. **Frost holds a card and still has no legal defense** — functionally an empty hand. Per resolution step 3, A wins automatically.

Damage: Soul 2 + d2 *(rolls 1)* = 3. SHADE AWAY Effect: A gains **Evade**. Frost 10 → **7**.

Because there was no legal defense to choose, nothing left Frost's hand — REFRACT and INJURY are both still there. A's hand after playing SHADE AWAY: RAKING CUT. A's deck: SKITTER AWAY, NIP AND TEAR.

### Steele's turn

Draws to 3 → draws BRACE. Hand: DEAD HEAT, CALCULATE, BRACE.

**Action:** Steele attacks Scratcher B with **DEAD HEAT** (Red, Body + d6, Ranged). Range check: Frontline → Backline is not melee range — Ranged is legal.

B's hand is RAKING CUT — its only card, and **Melee**. B is still Backline: not melee range against a Frontline Steele, so RAKING CUT can't defend here either, the same gap that just caught Frost above. **B has no legal defense.** Steele wins automatically.

Damage: Body 4 + d6 *(rolls 3)* = **7**. B: 11 → 4. DEAD HEAT's Effect only fires on a tie, and this isn't one, so it does nothing here — there was no Defensive Bonus in play to cancel anyway.

RAKING CUT was never a legal option, so it was never revealed — B's hand is unchanged. Steele's hand: CALCULATE, BRACE.

### Scratcher B's turn

Draws to 2 → draws NIP AND TEAR. Hand: RAKING CUT, NIP AND TEAR. B's deck: SHADE AWAY.

NIP AND TEAR is Melee and B is still Backline — and RAKING CUT is Melee too. **Both cards in hand are illegal to attack with from here.** **Action: Move Position** — B crosses into its Frontline. Moving costs the whole action; B does nothing else this turn. The deck resize just made a Backline Scratcher's hand a real liability, not only an attack-range inconvenience — worth flagging as a genuine finding, not a scripted one (see Edge Cases).

---

## Cycle 3 — The Disengage

### Frost's turn

Frost's hand is REFRACT and INJURY — REFRACT was never legally playable this fight (Ranged, and every exchange so far has been melee range), so it's still sitting there. Draws to 3 → draws PUSH from his deck. Hand: REFRACT, INJURY, PUSH.

**Action:** Frost attacks B — both Frontline now — with **PUSH** (Red, Body + d4, Melee). B reveals **NIP AND TEAR** (Green, Melee — legal, both Frontline now). **Green beats Red — defender wins.** No damage. NIP AND TEAR Defensive Bonus: *Heal 1.* B: 4 → 5.

### Scratchers A and B — the exit

A Scratcher fight doesn't end in a kill. They mark and they leave (`bestiary/briar-scratcher.md`: *"They're not trying to win. They're marking."*).

On A's turn it bolts for the briar wall — moving out of the combat area entirely. Movement in Tales Untold is abstract: leaving the field ends your participation in combat, and if every enemy leaves, **combat is over** (they can re-engage later if the fiction demands). B follows on its turn, gone between two heartbeats.

Note the asymmetry: enemy disengagement is a GM call, made from behavior — Scratchers leave because leaving is what Scratchers do. A *player* trying to exit combat under pressure uses the **Flee** action: 2d10 + Soul vs DC 10 + highest enemy Soul, GM-adjusted for the fiction (`rules/combat.md`, Fleeing Combat). The world doesn't owe the party the same clean exit it gives its animals.

No initiative to unwind, no cleanup step. The wheel simply stops mattering.

---

## After the Fight

| | HP | Deck state |
|---|----|-----------|
| Frost | 7 / 15 | **1 Injury** clogging his hand — stays until he spends an action to discard it or clears it on a short rest (1 per rest); REFRACT never found a legal moment to be played |
| Steele | 17 / 17 | Clean — never targeted |
| Scratcher A | 6 / 11 | Gone |
| Scratcher B | 5 / 11 | Gone — spent a whole turn just crossing the field, and its Backline hand was dead weight twice over |

Frost's Injury doesn't heal with HP, and it won't leave until he spends a whole action on it or takes a short rest. It rides in his deck into Briarwatch and the Hollow below it, surfacing into his hand to eat a slot every time it's drawn (`quests/hollow-below-briarwatch.md`). Two more Scratcher encounters without a rest and the party's decks — not their HP bars — are the injured thing.

---

## What This Example Demonstrated

- **Initiative:** 1d6 + Soul; ties break by higher Soul, then player-before-enemy; the order is a wheel with no rounds.
- **Turn economy:** draw to hand size (Mind, minimum 2) at start of turn, then exactly one action — attack, move, item, Rushdown, interact, or flee.
- **Three of the four resolution outcomes:** attacker win (damage + Effect), defender win (no damage + Defensive Bonus), and the automatic win when the defender declines or has nothing legal to offer.
- **Simultaneous reveal:** defense is a prediction. Frost guessed wrong once; that's the game.
- **Range is positional law, for both sides of an exchange:** melee needs both Frontline; Ranged fails inside melee range whether it's the card attacking or defending. A hand that holds a card can still have no legal defense — Frost's REFRACT and B's RAKING CUT both sat in hand, useless, at the moments that mattered.
- **A 4-card deck genuinely cycles mid-fight:** Scratcher A ran its deck dry and reshuffled its discard pile inside a single combat — a real consequence of deck size = total stats that a larger deck wouldn't have surfaced.
- **Status flow:** Evade (spent on one attack, whether or not it dodges), and the Injury life cycle — shuffled into the deck, drawn into the hand where it occupies a slot and *stays*, cleared only by spending an action or taking a short rest.
- **You Are Not Your Own Ally** unless the card says "you and" (`rules/cards.md`).

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
