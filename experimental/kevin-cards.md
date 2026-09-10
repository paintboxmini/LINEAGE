# Kevin's Custom Cards

Three custom cards for the combat chef — one per piece of the kit, and one per colour. Draft, staged here before landing in `cards/`, same as `experimental/pat-cards.md`.

Kevin's tentative stats are Body 4 / Mind 3 / Soul 2 (`experimental/kevin.md`), so the deck-building heuristic wants roughly 4 Red / 3 Blue / 2 Green. One signature card in each colour fits that without crowding any of them, and it puts his weakest stat on the card he plays for its effect rather than its damage.

The hot knife doesn't get a card. It's flagged as probably flavor-only in `experimental/kevin.md` and nothing about it wants a mechanic yet.

---

## Card 1 — GRIND (the pepper grinder)

Red, d8, **Melee**. His biggest die on his best stat, and the card that decides how he stands in a fight.

**The range is the character beat.** A pepper grinder throws seeds — spread, short range, a shotgun. Melee means both combatants have to be in the Frontline (`rules/combat.md`, Range Matrix), so Kevin's best weapon only works when he's in the scrum. He is not a sniper. He's a cook who has to get close, and the biggest number in his deck is the reason he keeps walking toward people.

**The Special Rule answers an open question.** `experimental/kevin-ingredients.md` asks whether firing a seasoning is a locked choice made before resolution, like the colour-mirror cards, or something looser. This says locked: you name the load when you commit the card face down, before the reveal — so a wrong guess is a real cost, and reading the table is part of firing the gun. That is the whole "what's loaded gates what it does" premise made mechanical instead of narrative.

```
GRIND
RED — BODY
Attack: Body + d8
Special Rule: Name the load when you commit this card, before the reveal.
Effect: Cinder — deal +3 damage. Sapphire — defender gains Blind. Hush — defender gains Weak.
Defense Effect: Deal 3 damage to the attacker.
Range: Melee
"One crank. Whatever you fed it is what comes out."
```

**Dependency worth naming:** the three loads are the three seasonings in `experimental/kevin-ingredients.md`, and only Sapphire Ant is canon. Scorchback Beetle (cinder flake) and Hush Bloom are proposed, not built. This card doesn't work until they are — which is arguably the point, since it turns two loose ingredient concepts into things the game actually needs.

---

## Card 2 — KINDLE (the incendiary oranges)

Blue, d6, **Ranged**. The grenade.

**Why Blue and not Red.** The obvious read is Red — it's fire, and fire is damage. But the orange's job on the board isn't to hurt one person, it's to make a whole position a bad place to be standing, and that's control, which is Blue's identity (`rules/cards.md`, What Each Colour Tends Toward). It also puts the artificer's cleverness in the Mind colour, where the crafting actually lives. Kevin throws it from the back while his grinder keeps him at the front — the two cards want him in different places, and choosing which is the interesting turn.

The damage is unpreventable because it's fire rather than an attack landing, matching SPARK OF VIOLENCE and HAMMER. Two per enemy across a whole position prices it between them: HAMMER is 4 to one target at d4, SPARK is 3 to one target at d6.

```
KINDLE
BLUE — MIND
Attack: Mind + d6
Effect: Deal 2 unpreventable damage to every enemy in a position of your choice.
Defense Effect: Attacker gains Blind.
Range: Ranged
"The peel does the work. The fruit is just what carries it there."
```

---

## Card 3 — SERVE (the beverages)

Green, d6, **Both**. The party card.

`experimental/kevin.md` already names what the basic drinks do — **Quick** or a small **Initiative Shift** — so this card is those two and nothing invented on top. Modal, like CHANNEL, which is the only other card in the game that lets you pick one of several on either half.

Its two modes are each roughly a whole existing d6 Green card — HASTEN hands the party Initiative Shift +1, MIRROR STEP's defence half hands allies Quick — so getting to choose between them is the premium a signature card is allowed. Kevin's Soul is 2, which means this is the card he plays for the effect and not the number, and that reads correctly for handing out drinks mid-fight.

```
SERVE
GREEN — SOUL
Attack: Soul + d6
Effect: Choose one — all allies gain Quick, or apply Initiative Shift +1 to all allies.
Defense Effect: Target ally gains Quick.
Range: Both
"Drink it. Don't ask what's in it. Drink it."
```

---

## What these three do together

They pull him in three directions on purpose. GRIND is his damage and it demands the Frontline. KINDLE is his control and it wants the Backline. SERVE works anywhere and doesn't care about either, which makes it the card he falls back on when the other two are stranded. A player holding all three has a live decision every turn about where to stand, which is the most any three cards can do for a character whose whole concept is *what's loaded gates what it does*.

## Open

- The two unbuilt seasonings GRIND depends on (Scorchback Beetle, Hush Bloom)
- Whether the oranges want an item entry as well as a card — `experimental/kevin.md` still lists the bandolier's numbers as unwritten, and a card is not the same thing as a piece of gear
- The rest of the 9-card starting deck, drafted from the Oracle as normal (`rules/character-creation.md`, Starting Deck)

## Related Documents

- `experimental/kevin.md` — the character, the kit, and how the grinder works
- `experimental/kevin-ingredients.md` — the seasonings GRIND names
- `experimental/pat-cards.md` — the same exercise for the other player concept
- `rules/cards.md` — colour conventions, and why Range is a real cost
