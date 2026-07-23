# Items

Items are the second design language in Tales Untold, alongside cards — and the newer, less standardized one. This file exists to give item creation the same standing checklist cards already have (`rules/cards.md`), so building an item for a location, an NPC, or a bestiary entry is as routine a step as building its cards.

---

## The Default: Dress However You Want

Fiction is unrestricted. A character can carry, wear, and wield anything the story supports — three swords, a full suit of borrowed armor, a pocket full of trinkets. None of that needs a rule.

**Only equipment that grants an actual mechanical effect is restricted to the three Equipment Slots** (`rules/character-creation.md`): Weapon, Armor, Artifact. The slot system isn't a limit on what a character can *carry* — it's a limit on how much raw mechanical power a character can have *active* at once. Everything else — how it looks, what it's called, how many of them you own — is free.

Carried items (potions, tools, one-use consumables) don't compete for these slots at all. They're used via the Interact action and are a separate category entirely — see the `items/*.md` files for existing examples (`items/briarwatch-items.md`, `items/hollow-and-weald-items.md`, etc.).

---

## Weapon and Armor Tiers

Weapons and Armor both scale on the same three-tier system. Each tier is a **power budget** — a fixed amount of mechanical value — spendable as a flat numeric bonus, or split across smaller effects, at the designer's discretion.

| Tier | Weapon (default spend) | Armor (default spend) |
|------|------------------------|------------------------|
| 1 | +1 attack damage | −1 damage received |
| 2 | +2 attack damage | −2 damage received |
| 3 | +3 attack damage | −3 damage received |

**The budget doesn't have to go entirely into the flat number.** A tier is a total, not a minimum floor on the stat bonus — spend it instead, in whole or in part, on other effects, calibrated against the same 1-point-per-tier-level scale:

- **1 point ≈** +1 flat damage or reduction, **or** granting yourself one stack of a Positive Status Effect (Deadly, Resist, Evade, etc.) at the start of combat, **or** inflicting one stack of a debuff (Weak, Blind, Staggered, etc.) on an enemy, usually gated behind "the first time you land a successful attack" or "the first time you're hit" so it triggers once per combat, not indefinitely.
- Larger, spikier effects (Critical, Immunity, a full Ward) run stronger than a single point and should either consume a whole tier on their own or come with a real restriction (once per combat, only below half HP, only on a clean win) to stay in budget.
- **Not every keyword is worth the same point regardless of context — check actual value, don't just price by name.** Fortress reads like a strong defensive keyword but is genuinely one of the weakest through an action-economy lens: the party still eats the same total damage, just redirected onto whoever volunteered — no damage is actually prevented unless it's paired with something that mitigates the hit once it lands (Resist, Evade, and similar). Priced alone, it's worth well under 1 point — cheap enough to bundle in at Tier 1 alongside a real effect (e.g., start combat with Evade 1 and Fortress 1) rather than ever anchoring a tier by itself. The general lesson: price a keyword by what it actually does for the action economy, not by how strong it sounds.

**Worked examples, exactly as specified:**
- *Tier 1 weapon:* inflicts Weak on the first successful attack against an enemy. (Whole budget spent on the debuff — no flat bonus.)
- *Tier 2 weapon:* +1 attack damage, and gain Deadly at the start of combat. (1 point flat, 1 point self-buff.)
- *Tier 2 armor:* −1 damage received, and start combat with 1 Resist. (1 point flat, 1 point self-buff.)

This is a budget to design against, not a formula to solve — two tier-2 items should feel different from each other even though they cost the same.

---

## More Fastball Ideas (Unnamed on Purpose)

Straightforward, single-idea equipment across the tiers — no names, no flavor text. They earn an identity when actually built as real "equipment archetypes"; until then they're just budget-legal shapes to pick from or riff on.

**Weapons**
- *Tier 1:* Gain Evade the first time you're attacked each combat.
- *Tier 1:* Scry 1 the first time you attack each combat.
- *Tier 2:* +1 damage; inflict Blind on a clean win, once per combat.
- *Tier 2:* Gain Rushdown for free the first time your turn would otherwise need it.
- *Tier 3:* +2 damage; gain Deadly at the start of combat.
- *Tier 3:* +1 damage; gain Deadly at the start of combat; inflict Weak on the first successful attack against you. (Three-way split of the same budget.)
- *Tier 3:* Gain Critical the first time you attack each combat. (Whole budget on one spike.)

**Armor**
- *Tier 1:* Start combat with 1 Resist.
- *Tier 1:* Inflict Staggered on the first enemy who successfully hits you each combat.
- *Tier 1:* Start combat with Evade 1 and Fortress 1. (Fortress alone is cheap enough to ride along with a real effect at the lowest tier — see the pricing note above.)
- *Tier 2:* −1 damage received; start combat with 1 stack of Thorns.
- *Tier 2:* Start combat with Ward. (Whole budget on one full debuff-block.)
- *Tier 3:* −1 damage received; start combat with Resist; start combat with Evade. (Three-way split.)
- *Tier 3:* Gain Immunity the first time you would Collapse each combat. (Whole budget on one clutch save.)

---

## Artifacts

Artifacts don't run on the tier budget above — they're a different kind of object entirely. Per `rules/character-creation.md`: "resonant objects closely aligned with a Seat's domain... not ordinary equipment. They carry weight — cosmological, narrative, and mechanical. Wearing one is a statement about what you're willing to be near." An Artifact's mechanics should read as an extension of a specific Seat's actual domain (`mythology/seats.md`), not a generic stat stick reskinned — design these bespoke, one at a time, the way a signature card set gets built for a specific creature rather than pulled from a shared budget table.

---

## Where Items Actually Live

Location-specific items go in `items/<location>-items.md`, matching the existing convention (`items/briarwatch-items.md`, `items/hollow-and-weald-items.md`, `items/turnroot-weald-items.md`, `items/vultures-nest-items.md`, `items/fog-basin-items.md`). Items with no fixed location source go in `items/consumables.md`. Each entry states its own **Source** line — where or from whom it's actually obtained (a creature, a merchant, a specific harvest method) — already the standing convention across every existing items file, kept up here so it doesn't quietly lapse as more get added.

When building out a location, NPC, or bestiary entry, treat at least one real item as part of the standard deliverable set, the same as its cards: does this place, this creature, this person leave something behind worth carrying? Not every entry needs one — but the question should get asked every time, not just when it happens to come up.
