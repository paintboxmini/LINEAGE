# Cards

Cards are the primary language of Tales Untold.

In combat, you don't declare an action and roll — you play a card. The card tells you what you're attempting, how hard it hits, and what happens when it lands or fails. Your hand is your tactical options. Your deck is your character in motion.

**Cards are not objects in Eclipseria.** Nobody in the world holds one, drops one, or finds one in a drawer. A card is a way of acting that somebody learned — *"every technique, every card, every way of surviving a fight was learned from something"* (`world/lineage.md`) — and the deck is how that is handled at the table, not a thing the character is carrying. The bank is the same: real, yours, and nowhere.

This is why a card can be traded for a memory or a secret at the Underground Bazaar and why nothing is ever bought with coin there. What changes hands is the experience, not a piece of card.

---

## Card Anatomy

**Name** — What the action is called. Names matter: the Advantage rule lets you discard a card whose name meaningfully supports a noncombat action.

**Color + Stat** — The card's alignment. Red (Body), Blue (Mind), or Green (Soul). Determines which stat is used to calculate damage and how the card interacts with Rock-Paper-Scissors resolution.

**Attack** — Damage dealt when your attack wins: *Stat + die*. The die signals the card's philosophy:
- **d8** — Raw power. High ceiling, less control.
- **d6** — Utility. Moderate damage, strong effects.
- **d4** — Precision. Low damage, high control and information.

*(d10 exists on a small number of cards as a genuine outlier above this scale — rare and deliberately unlabeled, same as before the 2026-07-22 dice step-up; it was never a fourth named tier.)*

**Effect** — Triggers when you play this card as an attack and win the resolution — or tie it. On a tie the Effect still triggers, before the Defensive Bonus (see the tie rule in `rules/combat.md`).

**Defensive Bonus** — Triggers when you win the RPS resolution as the defender — and on ties, unless the attacker's Effect cancels it.

**Range** — Describes the positional relationship required to play this card. See the Range table in `rules/combat.md`.

**Flavor Text** — *Italicized.* Not a rule. The world speaking.

---

## "Attacker" / "Defender" vs. "Target"

Two different words in card text, two different mechanics — not interchangeable:

**Attacker** / **Defender** means whoever you're resolving *this specific RPS exchange* against. No choice is ever involved — it's fixed by who attacked and who defended this reveal (e.g. "Defender gains Rooted," "Attacker gains Weak").

**Target** means you genuinely choose who receives the effect — an ally among several ("Target ally gains Deadly"), or a specific enemy when more than one is present ("Target enemy can only attack frontline targets"). If a card doesn't actually let the player choose, it isn't a Target effect, even if the caster and recipient could theoretically differ — write it as Attacker/Defender instead.

**Choice is the default.** When a card names a pile or a group without naming which member of it — *"Exile 1 card from your discard pile," "Destroy 1 Wound in your hand or discard pile"* — the player resolving the card picks. *"Of your choice"* is written out on some cards for emphasis; its absence never means random, forced, or top-of-pile. A card that means to remove the choice has to say so.

---

## Card Example

```
╔══════════════════════════════════╗
║  FLOW                            ║
║  GREEN — SOUL                    ║
╠══════════════════════════════════╣
║  Attack:           Soul + d6     ║
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

A hand full of d8s is a brawler who hits hard and moves with purpose.
A hand full of d4s is a strategist watching for the moment everything opens up.
A hand full of d6s is someone threading the gap between the two.

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

**Player decks — the stat-matching heuristic.** A solid default: the number of cards of each color matches the corresponding stat. Mind 4 / Body 2 / Soul 3 → 4 Blue, 2 Red, 3 Green. The deck's color weight mirrors who the character is — and since damage runs off the matching stat, it keeps every card in the deck pulling at full strength. A heuristic, not a law: drafting through the Oracle (see `places/island-in-a-ship.md`) can and should bend it.

**Trading cards.** Cards change hands at the Underground Bazaar and effectively nowhere else (`places/capital/underground-bazaar.md`, Card Trading). Selling is always possible and permanent; buying is rare, is paid for in cards, memories, or secrets rather than coin, and adds to a deck rather than swapping into it. Everywhere else in the world a card is earned — from the Oracle, or from whatever taught it.

**Enemy decks.** Deck size equals the creature's **total stats**, with each color's count equal to the matching stat (signature cards count toward their color). Build 3 themed signature cards, then fill from the core lists (`cards/buckets/red.md`, `cards/buckets/blue.md`, `cards/buckets/green.md`) to reach the stat counts, leaning picks toward the creature's temperament. Enemies draw to hand size (Mind, minimum 2) like everyone else.

---

## Important: You Are Not Your Own Ally

Card effects that reference "allies" or "enemies" never apply to the card's user. You cannot target yourself with ally effects or accidentally trigger enemy effects on yourself. This applies to area effects, healing bonuses, and damage reduction.

If a card says *"all allies in your position,"* that means every other character sharing your position — not you.

The exception: cards that explicitly name *yourself* as the target (e.g., a self-damage card) apply as written.

