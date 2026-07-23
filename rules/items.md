# Items — Catalog by Source

Every mechanical item and piece of equipment currently in the world, sorted by where it actually comes from. Built for quick reference when designing a location, NPC, or bestiary entry: who's already trading what, where it makes sense for a new item to show up, and what's already been done so a new entry doesn't quietly duplicate an old one.

For how to *build* a new Weapon, Armor, or Artifact — the tier system, pricing, design guidance — see `rules/equipment.md`. This file is the inventory, not the design guide.

---

## Briarwatch

*Full entries: `items/briarwatch-items.md`*

- **Barbed Wrap** — reflect 1 damage when targeted, 1 battle. *Source: Roadhouse barracks.*
- **Carrion Feather** — negates the first forced reposition, then spent. *Source: given by Aege on delivery to Briarwatch.*
- **Split Wedge** — Anchored, +2 damage this turn. *Source: farmer's reward, after the Hollow.*

---

## The Hollow Below Briarwatch & Turnroot Weald (shared)

*Full entries: `items/hollow-and-weald-items.md`*

- **Luminova Leaves** — heal 2 HP. ~15 gold. *Source: harvestable in the field, Turnroot Weald (Luminova Clearing).* Can be ground into Luminova Powder (below) for roughly double the potency — a real crafting relationship, not a duplicate.
- **Clay Bowl Tremor Detector** — party can't be surprised this encounter. *Source: Borrower goodwill.*
- **Moving-Stone Map** — party acts before all Stonecoils, next combat only. *Source: Borrower goodwill.*

---

## Turnroot Weald

*Full entries: `items/turnroot-weald-items.md` — the most fully built items file in the repo.*

**Consumables**
- **Echothorn Seed** — +2 to next damage/heal roll, free action. ~40 gold. *Source: The Thorne Throne.*
- **Luminova Powder** — heal 4 HP. ~30 gold. *Source: Luminova Clearing.* Ground from Luminova Leaves (above) — the processed, more potent form of the same plant.
- **Sap Vial** — heal 4, or +2 melee damage next attack; costs a Rooted token. ~60 gold. *Source: Rootstalker (rare).*
- **Vision Shard** — Scry 3 on any deck. ~100 gold. *Source: The Mirror-Slick Pond.*

**Equipment**
- **Rusted Armor** — 5 temp HP, breaks when spent or removed. ~80 gold. *Source: The Floating Gallery.*
- **Spider Silk Rope** — 50 ft, stronger than hemp, doesn't fray. ~50 gold. *Source: The Bone Collector.*

**Harvested Materials**
- **Root Fibers** — rope, bowstring (+1 ranged), or armor weave (+1 temp HP). ~15 gold/strand. *Source: Rootstalker (common).*
- **Rootstalker Core** — crafts into a thrown Root Lash Charm or a one-encounter Defensive Barrier. ~250 gold. *Source: Rootstalker (very rare).*

**Passive Items**
- **Harvest Bead** — +1 HP on the first defensive block each cycle. ~150 gold. *Source: The Bone Collector.*

**Quest Ingredients** *(Senshi, the Gilded Tusk — see below)*
- **Bone Collector Flesh** — ~40 gold, half if the casing cracks.
- **Future-Lock Wasp Larvae** — ~35 gold, must be delivered alive within a day.

---

## Vulture's Nest

*Full entries: `items/vultures-nest-items.md`*

**Dock Equipment** (market, dockside traders)
- **Dockhook Line** — pull self or target enemy to Frontline.
- **Low Lantern** — Obscure, 1 combat.

**Foodstuffs** (Marta's Jerky and Bake, general stalls)
- **Salted Strip** — heal 2 HP.
- **Dock Broth** — remove 1 status card, gain Weak on next damage roll.
- **Chewfat Ration** — Resist 1 for a combat, discard 1 card at the end of each turn.

**Harwick Sundries — deliberately mechanics-free.** The Tuning Fork Sword, the Desire Compass, the Guard's Boots, and the Ticking Box (`locations/vultures-nest.md`) are mystery objects on Dess Harwick's counter, built to be developed later if the party returns. Not part of this inventory — don't treat them as priced or mechanical until someone actually builds them out.

---

## Fog Basin

*Full entries: `items/fog-basin-items.md`. Primary source: Pell.*

- **Fog Goggles** *(Artifact)* — never Blind from fog/Fogburst; costs adding FOGLUST (a Blind-on-draw curse card) to your deck. Price varies per customer — Pell charges in memories and secrets, not coin. Which Seat, if any, it's aligned to is open design, not a gap to close — same register as the rest of the Fog Basin's unresolved edges.
- **Pell's Lanterns** — four named, single-use, price set by Pell: Lantern of Returning (immune to the Misdirection Trap), Lantern of the First Path (reveals the original path through an area, DC 12 Mind), Lantern of the Unlost (Echoes repeat useful fragments nearby), Lantern of Quiet Wings (Fogcallers won't initiate combat while lit).

---

## Kaine (Storm Seat Artifact)

*Full entry: `items/lightning-loop.md`, `characters/kaine.md`.*

- **The Lightning Loop** — a ring, Storm Seat-aligned, currently worn by Kaine. Heals 1 HP when used for his "water trick"; calls down real, only partially controllable lightning in a confrontation. The one existing Artifact in the world that actually matches `rules/equipment.md`'s "extension of a specific Seat's domain" framing directly — worth using as the reference example for future Artifacts. The Storm Seat itself is now borne by Greed (`mythology/seats.md`) — whether that has any bearing on Kaine's own claim to this Artifact is unestablished, on purpose.

---

## No Fixed Source

*Full entries: `items/consumables.md`. Sources and availability left to GM discretion.*

- **Terrormite Capsule** — Resist 1 and +1d6 damage, 1 combat; costs 2 Injury cards at combat's end.
- **Echo Shell** — repeat your last action, if it's still retrievable from discard.
- **Blood Phial** — add the target's own last-used card's effect to your attack.
- **Imprint Sigil** — target follows a simple command, 1 turn.
- **Universal Pin** — fix a target in place until their next turn.
- **Phase Draught** — take your turn, then return to your prior position and state at turn's end.

---

## Underground Bazaar — a real gap, not an oversight

Checked directly: nothing in `locations/underground-bazaar.md` has an actual `Use:`/`Effect:` line. Willem's paintings, the Soul Economy trades, Kess's and Moth's own possessions — all narrative, no mechanics, and there's no `items/underground-bazaar-items.md` file yet. Given the location's whole premise (a market that trades in memories, secrets, and soul-economy debt instead of coin), items here would likely need their own pricing logic entirely, not a straight gold-cost — worth thinking through before just bolting standard prices onto bazaar goods.

---

## Who Trades With Whom

A quick reference for where it makes sense for a new item to surface:

- **Senshi (the Gilded Tusk)** buys quest-ingredient ideas straight from Turnroot Weald — Bone Collector Flesh, Future-Lock Wasp Larvae — and turns them into dishes. A new Weald creature with an unusual byproduct is a natural fit for his counter.
- **Dess Harwick (Vulture's Nest, Harwick Sundries)** deals in practical dockside goods plus whatever gets traded in — the mystery counter items came from unrelated trades she never resolved. A believable place for a found, undeveloped object to land.
- **Pell (Fog Basin)** is the one dealer whose price is never coin — memories, secrets, names. Anything sold through him should keep that convention rather than getting a flat gold price.
- **Borrowers (the Hollow)** trade in goodwill, not currency — their two items are both earned, not bought.
- **Aege / the Briarwatch farmer** hand over items as direct narrative rewards tied to a specific job finished, not shop stock.
- **The Underground Bazaar** trades in secrets and soul-economy debt — see the gap noted above before assuming standard pricing applies there at all.
