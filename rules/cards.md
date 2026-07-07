# Cards

Cards are the primary language of Tales Untold.

In combat, you don't declare an action and roll — you play a card. The card tells you what you're attempting, how hard it hits, and what happens when it lands or fails. Your hand is your tactical options. Your deck is your character in motion.

---

## Card Anatomy

**Name** — What the action is called. Names matter: the Advantage rule lets you discard a card whose name meaningfully supports a noncombat action.

**Color + Stat** — The card's alignment. Red (Body), Blue (Mind), or Green (Soul). Determines which stat is used to calculate damage and how the card interacts with Rock-Paper-Scissors resolution.

**Attack** — Damage dealt when your attack wins: *Stat + die*. The die signals the card's philosophy:
- **d6** — Raw power. High ceiling, less control.
- **d4** — Utility. Moderate damage, strong effects.
- **d2** — Precision. Low damage, high control and information.

**Effect** — Triggers when you play this card as an attack and win the resolution — or tie it. On a tie the Effect still triggers, before the Defensive Bonus (see the tie rule in `rules/combat.md`).

**Defensive Bonus** — Triggers when you win the RPS resolution as the defender — and on ties, unless the attacker's Effect cancels it.

**Range** — Describes the positional relationship required to play this card. See the Range table in `rules/combat.md`.

**Flavor Text** — *Italicized.* Not a rule. The world speaking.

---

## Card Example

```
╔══════════════════════════════════╗
║  FLOW                            ║
║  GREEN — SOUL                    ║
╠══════════════════════════════════╣
║  Attack:           Soul + d4     ║
║  Effect:           Change position
║  Defensive Bonus:  Change position
║  Range:            Melee         ║
╠══════════════════════════════════╣
║  "Water finds its way            ║
║   without forcing."              ║
╚══════════════════════════════════╝
```

---

## The Die Is the Card's Personality

When you look at a hand of cards, the dice tell you who you are right now.

A hand full of d6s is a brawler who hits hard and moves with purpose.
A hand full of d2s is a strategist watching for the moment everything opens up.
A hand full of d4s is someone threading the gap between the two.

Your deck is not just mechanics. It's how your character thinks.

---

## Card Glossary

Short versions for reading cards. `rules/card-glossary.md` is canonical — if these ever disagree, the glossary wins.

**Scry X** — Look at the top X cards of a deck (your own unless the card targets another). Place each on top, on the bottom, or into the discard pile, in any order.

**Ongoing Effect** — The card remains face up after use until its stated condition is met, then discards.

**Both (Range)** — Either position is valid. You may play this card from Frontline or Backline.

**Melee (Range)** — You and the target must be in the Frontline.

**Ranged (Range)** — Works only while not in Melee range with the target.

---

## Deck Building

**Player decks — the stat-matching heuristic.** A solid default: the number of cards of each color matches the corresponding stat. Mind 4 / Body 2 / Soul 3 → 4 Blue, 2 Red, 3 Green. The deck's color weight mirrors who the character is — and since damage runs off the matching stat, it keeps every card in the deck pulling at full strength. A heuristic, not a law: drafting through the Oracle (see `locations/island-in-a-ship.md`) can and should bend it.

**Enemy decks.** Build 3 themed signature cards for the creature, then pull 4–7 cards from the core lists (`cards/red-body.md`, `cards/blue-mind.md`, `cards/green-soul.md`) to finish the deck — 7 to 10 cards total. Lean the core picks toward the creature's stat spread and temperament. Enemies draw to hand size (Mind + 1) like everyone else.

For a full worked combat using both conventions, see `rules/combat-example.md`.

---

## Important: You Are Not Your Own Ally

Card effects that reference "allies" or "enemies" never apply to the card's user. You cannot target yourself with ally effects or accidentally trigger enemy effects on yourself. This applies to area effects, healing bonuses, and damage reduction.

If a card says *"all allies in your position,"* that means every other character sharing your position — not you.

The exception: cards that explicitly name *yourself* as the target (e.g., a self-damage card) apply as written.

### Green counts itself among its allies

**Green (Soul) cards are the exception to the rule above.** A Green card's ally-facing effects — heals, buffs, Resist, card draw, and the like — may treat the user as one of their own allies. When a Green card says "an ally" or "all allies," the caster is a valid target (and "all allies" includes them). This is Green's identity: its support turns inward as readily as outward, so a lone Soul character is never without someone to mend or strengthen. (Green effects that only make sense aimed at *someone else* — redirecting another's incoming damage to you — still need a separate target.)
