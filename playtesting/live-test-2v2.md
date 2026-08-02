# Live Test — 2v2, Claude's Side

**Purpose:** live mechanics test with Drew — reveal protocol, hidden stats/HP, visible status markers, and specifically the Soul/initiative dynamic discussed going in. Not a canon encounter; this file is working state, not a finished playtest writeup.

**Hidden-info rule in effect:** Mind/Body/Soul values and HP totals below are known only to me (and, per Drew's side, only to him for his own two). Neither side states exact numbers to the other during play — only what's inferable from what happens.

---

## Sky (Drew's side, for my own resolution math only — not narrated)

**Mind 4 / Body 3 / Soul 2 — HP 15, currently 10** (took 5 from Garnet's FORGET, turn 12)
Hand size 4. Deck 9 (4 Blue / 3 Red / 2 Green).

## Crimson (Drew's side, for my own resolution math only — not narrated)

**Mind 3 / Body 4 / Soul 2 — HP 17, currently 12** (took 5 from RALLY, turn 4)
Hand size 3. Deck 9 (3 Blue / 4 Red / 2 Green).

---

## Moss

**Mind 2 / Body 3 / Soul 4 — HP 15, currently 0 — COLLAPSED** (13→7→5→3→0 across turns 5, 6, 14, 15, 18; Death Floor -ceil(15/2) = -8, still well above it — Collapsed, not dead)
**Creature Threat Rating:** 9
Hand size 2 (Mind 2, floor).

**Deck (9 — 2 Blue / 3 Red / 4 Green):**
- Blue: STILLNESS, FOCUS
- Red: GUARD, ENDURE, DIG IN
- Green: PATIENCE, RENEWAL, WITNESS, ROOTED OATH

**Position:** Backline (turn 17); Collapsed as of turn 18 — off the initiative wheel until revived
**Appearance:** Muted greens and browns, moves like she's already decided not to be the first thing you notice. Stands still at range, watching hands more than faces.

## Garnet

**Mind 3 / Body 4 / Soul 2 — HP 17, currently 8** (13 after DEFLECT turn 2, then paid 5 HP for RALLY's Effect turn 4)
**Creature Threat Rating:** 9
Hand size 3.

**Deck (9 — 3 Blue / 4 Red / 2 Green):**
- Blue: FORGET, ANTICIPATE, PROFILE
- Red: STRIKE, BRACE, PAIN IS FUEL, RALLY
- Green: TWIN STRIKE, MOCKERY

**Position:** Frontline (repositioned turn 16; was pushed Backline turn 8 — TRAMPLE)
**Appearance:** Heavyset, rust-and-burgundy leathers, knuckles taped over old scars. Plants his feet at Frontline like the ground owes him something.

---

## Initiative (1d6 + Soul, rolled openly)

| Combatant | Soul | Roll | Total |
|---|---|---|---|
| Moss | 4 | 4 | 8 |
| Sky | 2 | 5 | 7 |
| Crimson | 2 | 5 | 7 |
| Garnet | 2 | 5 | 7 |

Three-way tie at 7 (Sky, Crimson, Garnet), all Soul 2 — "higher Soul" doesn't break it. Per `rules/combat.md`: players choose their own order against each other first (Sky vs. Crimson — Drew's call), then the player(s) go ahead of the enemy on any remaining player-vs-enemy tie (Garnet last).

**Wheel order:** Moss → Crimson → Sky → Garnet (Drew's call).

---

## Hands (drawn to hand size at combat start — private)

- Moss's hand: STILLNESS (drew GUARD + STILLNESS turn 13, GUARD played same turn; deck remainder: ENDURE, ROOTED OATH, WITNESS)
- Garnet's hand: TWIN STRIKE, BRACE, ANTICIPATE (deck empty; discard reshuffles next time he needs to draw beyond hand)

## Discard piles

- Moss: RENEWAL, PATIENCE, DIG IN, FOCUS, GUARD
- Garnet: STRIKE, MOCKERY, RALLY, PAIN IS FUEL, TRAMPLE, FORGET

## Status markers (visible to both sides once applied)

- Moss: Deadly x1 (turn 4, still banked), Resist spent out — 0 left after turn 15. Also: cannot play Green on her next reveal (AXIOM's Effect, turn 15) — moot for right now, her only card (STILLNESS) is Blue anyway.
- Garnet: Resist x3 (turns 8, 9, 13). Deadly x1, banked since turn 4, finally spent turn 12.
- Crimson: Ward, still unused (turn 2). New: next successful attack against him seeds a Wound into his deck instead of dealing damage (from REND's Defensive Bonus, turn 9 — his own to track, noted since status markers are public)
- Sky: +1d4 on his next attack, banked (from GAMBLER'S RUIN's Defensive Bonus, turn 13 — his own to track). Staggered and MOCKERY's taunt both already resolved and spent.

---

## Turn Log

*Updated live as we play.*

**Turn 1 — Moss.** Attacks Crimson. Hand was RENEWAL/PATIENCE; PATIENCE is Melee and Moss is Backline, so it's not a legal play right now — down to one real option. Target declared; card held back pending Drew's blind defense commit per the reveal protocol.

Drew ready. Moss's card, announced blind: **RENEWAL** (Soul + d2, Range Both). Awaiting Drew's reveal.

Crimson reveals **CHARGE** (Red, Body + d4). Red beats Green — defender wins. Per `rules/combat.md`: no damage, Crimson's Defensive Bonus triggers ("You and the attacker move into frontline"). **Moss moves Backline → Frontline.** Both cards to their owners' discards.

**Turn 2 — Crimson.** Draws to hand size 3. Attacks Garnet — wanted Moss instead (still soft after last turn's positioning), but held no Red card to guarantee the favorable matchup against her, so took the safer bet on Garnet instead. Both are Frontline right now, so Ranged is illegal for either side's defense/attack this exchange — Melee and Both only.

Drew ready. Garnet's blind defense: **STRIKE** (Red, Melee, Defensive Bonus: Deal 2 damage to attacker, only on a clean win). Picked over RALLY (Both, dead right now — no Backline allies to buff) on color-safety against a Red-heavy deck; MOCKERY was the other option but loses outright to a Red attack instead of tying it.

Crimson reveals **DEFLECT** (Blue, Mind + d4). Blue beats Red — attacker wins clean. Damage: Mind 3 + roll 1 = **4** (corrected from an initial Body-stat slip). **Garnet takes 4, HP 17 → 13.** DEFLECT's Effect: Crimson gains Ward. STRIKE's Defensive Bonus doesn't trigger — that's a defender-clean-win-only payoff, and Garnet lost this one. Both cards to discard.

**Turn 3 — Sky.** Attacks Garnet. Sky is Backline, Garnet is Frontline — not both Frontline, so Melee is illegal for this exchange, Ranged and Both are fine.

Drew ready. Garnet's hand is down to RALLY and MOCKERY (STRIKE already spent). Blind defense: **MOCKERY** (Green, Both, Defensive Bonus: target must attack you if able on their next turn). RALLY's Defensive Bonus is still dead with no Backline allies — true in a tie too — while MOCKERY beats a Blue attack outright and still gets its Defensive Bonus on a Green tie; only loses clean to Red. Sky's deck leans Blue heaviest, so this is the better bet by a real margin, not just default-to-the-one-that-isn't-dead.

Sky reveals **CALCULATE** (Blue, Ranged, Mind + d4, Effect: move target enemy to Backline; Defensive Bonus: move target to Frontline). Green beats Blue — **defender wins.** No damage. MOCKERY's Defensive Bonus triggers: **Sky must attack Garnet again next turn if able.** The read paid off. Both cards to discard — Garnet's hand is down to RALLY alone.

*Correction — not retrospection, per Drew.* Sky's full turn-3 hand was CALCULATE, PAIN IS FUEL, GAMBLER'S RUIN, WITNESS. His point wasn't "I now know MOCKERY was Green so WITNESS would've won" — it's that WITNESS was the statistically correct play *before* any reveal, foreknowledge-free (beats Blue, ties Green, only loses to an assumed-unlikely Red). CALCULATE was a deliberate greedier line, not a mistake made in ignorance. Mislabeled this as "retrospective" the first time; noting the actual distinction here since it matters for reading the log honestly.

**Turn 4 — Garnet.** Draws to hand size 3 (was down to just RALLY). New hand: RALLY, PROFILE, TWIN STRIKE. Attacks Crimson.

Drew ready — reasoning given before my reveal, not after: Garnet's last shown color was Green (MOCKERY), and he reads Garnet as a Red main overall, so Blue was his best statistical bet against whatever came next.

Garnet's card, announced blind: **RALLY** (Red, Body + d2, Range Both, Effect: Pay 5 HP, all allies in Frontline gain Deadly).

Crimson reveals **PARADOX** (Blue, Both, Mind + d4, Special Rule: reverses the RPS outcome this turn, unless tied. Effect: Lifesteal. Defensive Bonus: Gain Ward). Base RPS: Blue beats Red, so Crimson would normally win clean here — Paradox's read was right. But its own Special Rule flips that result: **attacker wins instead.** PARADOX's Defensive Bonus never triggers — that's a defender-win-only payoff, and the reversal took the win away from him. Real backfire, not just flavor: playing Paradox into a matchup you'd already won turns a win into a loss.

Damage: Body 4 + roll 1 = **5. Crimson takes 5, HP 17 → 12.** RALLY's Effect resolves (attacker won): pay 5 HP, all Frontline allies gain **Deadly** — that's both Moss and Garnet. **Garnet pays the cost, HP 13 → 8.** Both cards to discard.

**Turn 5 — Moss.** Wheel wraps back around. Draws to hand size 2 — hand's now PATIENCE, DIG IN, both Melee. Frontline vs Frontline Crimson is the only legal Melee target (Sky's Backline), so **Moss attacks Crimson.**

Drew ready — STRIKE (Red). Reasoning given up front: with both sides apparently out of Blue this exchange, Red is the safe-or-better pick (only loses to Blue, and there's none in play). Also drew REND this turn and held it back — its Defensive Bonus seeds a Wound into the attacker's deck instead of blocking damage, but Moss's deck still has 6 cards left before that Wound would ever surface, so the delayed payoff wasn't worth it over STRIKE's immediate one.

Moss's card, held back until now per the same protocol: **PATIENCE** (Green, Soul + d4, Range Melee — legal, both Frontline). No "didn't attack last turn" bonus this time, she attacked turn 1.

Red beats Green — **defender wins clean.** No damage to Crimson. STRIKE's Defensive Bonus triggers (clean win, not a tie): **deal 2 damage to the attacker — Moss takes 2, HP 15 → 13.** Moss's banked Deadly isn't spent — her own damage never got computed on a clean loss, so it carries forward. Both cards to discard.

**Turn 6 — Crimson.** Attacks Moss.

Card set. Moss's hand is down to one — DIG IN (Red, Melee, d2, Effect/Defensive Bonus: Anchored — Gain Resist 1). Both Frontline so it's legal, but it's not really a choice this time, just the only card left. Announced blind: **DIG IN.** Its Defensive Bonus isn't clean-win-gated like STRIKE's — it fires on a tie too.

Crimson reveals **PROFILE** (Blue, Both, Mind + d4). Blue beats Red — **attacker wins clean.** Damage: Mind 3 + roll 3 = **6. Moss takes 6, HP 13 → 7.** DIG IN's Defensive Bonus does not trigger — that's a defender-win-or-tie payoff, and Moss lost this one outright.

PROFILE's Effect resolves (attacker won): Scry 2 on Crimson's own deck, then draw 1. Saw TRAMPLE and PATIENCE — kept TRAMPLE to hand, sent PATIENCE straight to discard rather than back into the deck (Scry/Surveil's bin option) since PATIENCE rewards not having attacked last turn, and Crimson's been attacking every turn he's had. Deliberately holding off drawing more than necessary to keep PATIENCE out of a reshuffle as long as possible — real, correct reasoning about how the reshuffle-on-empty-deck rule actually works, not just flavor. Both PROFILE and DIG IN to discard.

**Turn 7 — Sky.** Up next in the wheel — MOCKERY's Defensive Bonus from turn 3 comes due: **Sky must attack Garnet this turn if able.** Draws to hand size 4, STILLNESS among the new cards.

Garnet's hand: PROFILE, TWIN STRIKE. Garnet's Frontline, Sky's Backline, so TWIN STRIKE (Melee) is illegal — forced down to one real option again. Announced blind: **PROFILE** (Blue, Both, Mind + d4, Defensive Bonus: Attacker gains Staggered).

Sky reveals **PAIN IS FUEL** (Red, Both, Body + d4, Effect: Gain Resist). Correction on the reasoning — the STILLNESS mention wasn't a genuine tactical pass, it was a plant: narrating the draw was meant to bait a Green pick out of Garnet (Green beats Blue, and STILLNESS is Blue), setting up PAIN IS FUEL's Red to land clean against it. Didn't matter either way — Garnet's only Green card, TWIN STRIKE, was already range-illegal this turn (Melee vs. a Backline Sky), so PROFILE was forced regardless of any read, bait or otherwise.

Blue beats Red — **defender wins clean.** No damage to Garnet, and Sky's own Effect never triggers (attacker-win-or-tie only). PROFILE's Defensive Bonus fires: **Sky gains Staggered** — his next attack or defense gets skipped. Both cards to discard.

**Turn 8 — Garnet.** Draws to 3 (PAIN IS FUEL, BRACE join TWIN STRIKE). Attacks Crimson with **PAIN IS FUEL** (Red, Body + d4, Both).

Crimson defends **TRAMPLE** (Red, Melee — legal, both Frontline). Same color — **tie.** No damage (the pre-rolled Deadly number never gets applied — a tie deals no damage, so it doesn't spend the stack either, same logic as a clean loss; still banked). PAIN IS FUEL's Effect triggers on a tie: **Garnet gains Resist.** TRAMPLE's Defensive Bonus isn't cancelled by anything Garnet's card does, so it triggers too: **Garnet gets pushed to Backline.** Both cards to discard.

**Turn 9 — Moss.** Wheel wraps around. Draws to 2 (FOCUS, GUARD). Attacks Crimson with **GUARD** (Red, Body + d2, Melee — legal, both Frontline).

Crimson defends **REND** (Red, Melee, Body + d4, Effect: shuffle 1 Wound into defender's deck if this hits; Defensive Bonus: next attack against you shuffles 1 Wound into your deck instead of dealing damage). Reasoning given: read Moss by archetype (the green character) rather than by the card actually played — same color either way this time.

Same color — **tie.** No damage. GUARD's Effect triggers on a tie: **both Moss and Garnet gain Resist**, regardless of position. REND's Defensive Bonus isn't cancelled by anything GUARD does, so it triggers too: **the next successful attack against Crimson seeds a Wound into his deck instead of dealing damage** — a real status to track, not yet spent. Both cards to discard.

**Turn 10 — Crimson.** Attacks Moss with **PROFILE** (Blue, Both, Mind + d4).

Moss's hand is down to one — FOCUS (Blue, Both). Forced, but it happens to matter: same color — **tie.** No damage. PROFILE's Effect resolves on Crimson's own deck (Scry 2, draw 1). FOCUS's Defensive Bonus resolves for Moss: **top card of her discard (GUARD) goes back on top of her deck** — she'll draw it again next chance. FOCUS's own "return to hand" line is its Effect, which only applies when she plays it as an attack — defending with it, it discards normally like anything else. Both cards to discard.

**Turn 11 — Sky.** Staggered from turn 7 comes due — per the glossary, "your attack fails to happen on your turn," not the whole turn forfeit. No attack this turn: Sky moves Backline → Frontline and passes on the rest. Staggered clears (its one job done). No cards revealed, no exchange.

**Turn 12 — Garnet.** Draws to 3 — TWIN STRIKE and BRACE are both Melee and dead while he's Backline, but the new card, **FORGET** (Blue, Ranged, Mind + d2), is legal precisely *because* he's Backline (Ranged needs not-both-Frontline). Real attack after all.

**Garnet attacks Sky with FORGET** — Crimson's already carrying the Rend status (his next hit taken converts to a Wound instead of damage), so pressuring him wouldn't actually cost him HP right now. Sky's untouched all fight; better target for real damage.

Drew ready. Garnet's card, announced blind: **FORGET** (Blue, Ranged, Mind + d2, Effect: Defender discards 1 card).

Sky's reveal, WITNESS, turned out illegal — Melee, but Garnet (the attacker) is Backline, so "both Frontline" isn't met. Caught after FORGET was already revealed, so a free re-pick would mean choosing with full knowledge of the attack — not blind anymore. New house rule adopted on the spot: illegal picks caught *before* the opponent's card is known can be swapped freely; caught *after*, it's too late, and it resolves as no legal defense — refined further, mid-exchange: the misplayed card goes back to hand, not discard, since it was never legally played. The attacker still learns what it was; that's the real cost, not also losing the card.

**No legal defense — attacker wins automatically.** Deadly finally cashes in, banked since turn 4: rolled twice (2, 2), damage = Mind 3 + 2 = **5. Sky takes 5, HP 15 → 10.** FORGET's Effect: Sky discards 1 card at random (his own to resolve). FORGET to Garnet's discard.

**Turn 13 — Moss.** Draws GUARD (was on top from FOCUS) plus STILLNESS. Everyone's Frontline now except Garnet, so STILLNESS (Ranged) is illegal against either target — forced to GUARD again. **Moss attacks Sky with GUARD** — skipping Crimson, same logic as before: his Rend status converts a hit to a Wound instead of real damage, and Sky's the one who's actually taken damage worth building on.

Sky defends **GAMBLER'S RUIN** (Red, Melee — legal, both Frontline). Same color — **tie.** No damage. GUARD's Effect resolves: **Moss and Garnet both gain Resist again.** GAMBLER'S RUIN's Defensive Bonus resolves: **Sky adds 1d4 to his next attack**, banked for later. Both cards to discard.

**Turn 14 — Crimson.** Attacks Moss with **WITNESS** (Green, Melee, Soul + d2, Effect: target ally heals 6 HP).

Moss's hand is just STILLNESS (Ranged) — both she and Crimson are Frontline, so Ranged doesn't satisfy the "not both Frontline" requirement. **No legal defense — attacker wins automatically**, no illegal-pick wrinkle this time, she genuinely has nothing that works.

Damage: Soul 2 + roll 2 = 4 raw. Moss's Resist eats one stack and halves it: **2 damage, HP 7 → 5.** WITNESS's Effect resolves: target ally heals 6 — **Sky heals up to his max, 15/15.** WITNESS to Crimson's discard.

**Turn 15 — Sky.** Draws to 4 (SLIP THE BLADE, AXIOM, REFRACT among the new cards). Two range mistakes caught in a row before anything was committed, no penalty on either — REFRACT and STILLNESS are both Ranged, illegal against a Frontline Moss. **Attacks Moss with AXIOM** (Blue, Both, Mind + d2 — legal regardless of position).

Moss's only card, STILLNESS, is Ranged — illegal for the same reason, so she has no legal defense either. Since nothing was actually offered, STILLNESS stays in her hand untouched (different from the earlier illegal-*pick* case — she never attempted this one). **Attacker wins automatically.**

Damage: Mind 4 + roll 1 = 5 raw. Resist eats her last stack: **2 damage, HP 5 → 3.** AXIOM's Effect resolves (attacker won): names a color Moss can't play on her next reveal.

**Turn 16 — Garnet.** Draws his last deck card, ANTICIPATE — deck's empty now (3 in hand + 6 in discard = all 9 accounted for; next draw reshuffles). Hand is TWIN STRIKE, BRACE, ANTICIPATE — **all three Melee**, and he's still Backline. No legal attack again. **Garnet repositions to Frontline.** No exchange.

**Turn 17 — Moss.** Draws WITNESS (hand: STILLNESS, WITNESS). Neither is usable: STILLNESS is Ranged and everyone's Frontline right now; WITNESS is Green, still banned by AXIOM's Effect on her next reveal — this one. No legal attack. **Moss repositions to Backline instead** — purely defensive at 3 HP, and it also fixes STILLNESS's range problem for next time. No exchange.

**Turn 18 — Crimson.** Draws STRIKE. **Attacks Moss with ROOTED OATH** (Green, Both, Soul + d4 — legal regardless of position).

Moss's hand: STILLNESS (now legal — she's Backline, Crimson's Frontline, "not both Frontline" satisfied), WITNESS (still illegal — the Green ban from turn 15 is still live, this is only her second reveal since). Forced to **STILLNESS** (Blue).

Green beats Blue — **attacker wins clean.** Damage: Soul 2 + roll 1 = **3.** No Resist left to soften it. **Moss takes 3, HP 3 → 0. She Collapses.** ROOTED OATH's Effect resolves (Anchored — target ally gains Deadly): Crimson's pick, presumably Sky. Moss leaves the initiative wheel until healed or revived. Both cards to discard.

**It's down to Garnet alone on my side, against Crimson and Sky both.**

**Called here, turn 18.** Garnet's facing 1v2 with no realistic path back — estimated 3–6 more turns to a loss, not worth playing out for data the last several turns had already given. Full findings and summary: `playtesting/live-test-2v2-review.md`.
