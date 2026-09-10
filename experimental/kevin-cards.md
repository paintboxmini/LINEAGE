# Kevin's Custom Cards

Three custom cards for the combat chef — one per piece of the kit, one per colour — plus the equipment entry that makes the grinder's loads work. Draft, staged here before landing in `cards/`, same as `experimental/pat-cards.md`.

Kevin's tentative stats are Body 4 / Mind 3 / Soul 2 (`experimental/kevin.md`), so the deck-building heuristic wants roughly 4 Red / 3 Blue / 2 Green. One signature card in each colour fits that without crowding any of them, and it puts his weakest stat on the card he plays for its effect rather than its damage.

The hot knife doesn't get a card. It's flagged as probably flavor-only in `experimental/kevin.md` and nothing about it wants a mechanic yet.

---

## Card 1 — GRIND SHOT (the pepper grinder)

Red, d8, **Melee**. His biggest die on his best stat, and the card that decides how he stands in a fight.

**The range and the Effect are the same joke.** A pepper grinder throws seeds — spread, short range, a shotgun. Melee means both combatants have to be in the Frontline (`rules/combat.md`, Range Matrix), so his best weapon only works in the scrum. Then the Effect moves him to the Backline. He walks in, fires once, and leaves. He is not a sniper and he is not a brawler; he is a cook who does not want to be there and keeps having to be.

**No Special Rule.** Loading is the grinder's business, not the card's — the equipment entry below carries those rules, which keeps the card readable and means a new load never needs the card reprinted.

```
GRIND SHOT
RED — BODY
Attack: Body + d8
Effect: Move to the Backline.
Defense Effect: Attacker gains Blind.
Range: Melee
"One crank. Whatever you fed it is what comes out."
```

**Loaded, the seasoning adds its bonus to the Effect** — cinder flake for +3 damage, sapphire crystal for Vulnerable, hush petal for Rooted (`experimental/kevin-ingredients.md`, The loads). Unloaded it still fires and still repositions him, which is the whole reason he is never out of ammunition.

---

## The equipment — THE PEPPER GRINDER

The weapon that makes the loads mean anything. Tier 2: its entire budget goes into the loading mechanism rather than a flat bonus, because what it actually grants is the ability to spend a separately-acquired consumable as part of an attack.

```
THE PEPPER GRINDER
Equipment — Weapon (Tier 2)
Effect: You may hold one prepared load at a time. Loading takes a free action,
and the grinder may be loaded outside combat and carried loaded. While loaded,
GRIND SHOT gains that load's bonus in addition to its own Effect. The load is
spent when GRIND SHOT resolves, win or lose.
"It was a kitchen tool. It is still a kitchen tool."
```

**Why free-action loading rather than an action.** An action to load would mean the grinder costs a turn to do what other weapons do for nothing, and Kevin would simply never use the loads. A free action is the right price: it is one per turn (`rules/combat.md`, Turn Structure), so loading competes with everything else free — spending a Quick to reposition, most obviously, which is exactly the tension a character who keeps moving between the lines should feel.

**Spent win or lose** is the real cost. A charged round fired into a bad reveal is gone, and that is what makes a read on the table worth having. The version where the load survives a loss would make holding cinder flake permanently correct.

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

They pull him in three directions on purpose. GRIND SHOT is his damage, demands the Frontline, and then throws him back out of it. KINDLE is his control and wants the Backline — which is exactly where GRIND SHOT just put him, so the two chain. SERVE works anywhere and doesn't care about either, which makes it the card he falls back on when the other two are stranded.

The loop that falls out of it: walk in, fire, get thrown clear, throw an orange from where you landed. A player holding all three has a live decision every turn about where to stand, which is the most any three cards can do for a character whose whole concept is *what's loaded gates what it does*.

## Open

- The bandolier still wants an equipment entry of its own, the way the grinder now has one — KINDLE covers throwing an orange, not carrying six
- The static-charge hedgehog: it has a bonus (Initiative Shift -2) but no name, no entry, and no colour
- The rest of the 9-card starting deck, drafted from the Oracle as normal (`rules/character-creation.md`, Starting Deck)
- Whether Senshi stocks cinder flake and hush petal, or whether those stay things Kevin goes and gets

## Related Documents

- `experimental/kevin.md` — the character, the kit, and how the grinder works
- `experimental/kevin-ingredients.md` — the loads table: what each seasoning adds
- `bestiary/scorchback-beetle.md`, `bestiary/hush-bloom.md`, `bestiary/sapphire-ant.md` — where the loads come from
- `experimental/pat-cards.md` — the same exercise for the other player concept
- `rules/cards.md` — colour conventions, and why Range is a real cost
