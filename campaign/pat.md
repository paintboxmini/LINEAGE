# Pat

*Player character — no character name chosen yet; filed under the player's name until there is one. Most of what's below came out of a long session between Drew and Pat, but the character isn't finished — some backstory questions are still open, and gear hasn't been touched at all yet.*

## Stats

Mind 2 / Body 3 / Soul 4 — HP 18

| Stat | Value | Drives |
|------|-------|--------|
| Mind | 2 | Blue card damage; hand size 2 |
| Body | 3 | Red card damage; HP weighted 4× |
| Soul | 4 | Green card damage; Initiative 1d6 + 4 |

## People

Shunka — dogkin. His people, the war, the curse and the wild-magic line all live at `factions-and-races/races-shunka.md`; the Lizardkin who did it are at `factions-and-races/races-lizardkin.md`. Pat is Shunka but not of the cursed royal line — his connection to the curse runs through his mother's side instead (below).

## Backstory

Son of a Shunka military Captain and a woman his father met and left pregnant during his travels. Raised by his mother alone until age 11, when his father came back and had him join the military. Years of training followed, eventually fighting alongside his father directly. In his twenties, he entered officer school — what that actually looks like in Shunka society isn't worked out yet, flagged rather than guessed at. At 27, at the gravesite of the cursed royal family, the summoning magic below manifested — the one concrete detail on exactly when and how it happened. He set out into the world from there, presumably close to where Session 1 picks him up, though that's an inference, not stated outright.

**His mother's line is the real hook.** She descends from the first generation of Shunka who turned to wild magic trying to break the royal curse, back when it was first laid — and failed, same as everyone else who tried (`factions-and-races/races-shunka.md`). That failed tradition survived anyway, passed down matrilineally, and it's what Pat actually carries — not royal blood, wild magic.

## The Call

**The curse was never dormant.** It was crossing a spiritual distance, and it is only now beginning to reach the Shunka common folk — laid on one royal line generations ago, arriving late and arriving wide. The three cursed royals wake because of it, and they send Pat out.

**The vision at the royal cemetery gives him something specific to chase.** Not a destination and not an instruction — the spirits show him that the woman who laid it had a family, that the technique is theirs and always was, and that **a descendant of hers is alive now and somewhere near Vulture's Nest** (`factions-and-races/races-lizardkin.md`, The Cursegivers). The exact content of the vision is Drew's to set; what it has to leave him with is a direction and a person.

**What he can plausibly get out of it is an explanation rather than a cure.** A cost paid in full doesn't undo on request — that's how the world works, not a wall the GM put up. But the family that holds the technique is the only thing alive that understands what it does over time, and that is what he actually needs.

Where that points him, and how the search runs: `campaign/session-1-convergence.md`.

## Wild Magic Summoning

**This is a Trait**, not a Skill and not a Passive (`rules/character-creation.md`, Passives and Traits) — a line on the sheet that is simply true, costing no Action and taking no slot. It doesn't compete with STRONGJAW or HACKLES RISE for either of his two Passives.

> **Wild Magic Summoning:** Whenever you summon a spirit, roll a d10 — this is the spirit's HP. If the spirit reaches 0 HP, it dissipates.

What's summoned: the spirits of the three Shunka royals born cursed — the last of that line (`factions-and-races/races-shunka.md`). Two triggers confirmed — HERE BOY and LET'S GO (`campaign/pat-cards.md`).

**Spirits are Objects, not combatants.** Confirmed: they don't act, take no turn, and never get a token on the initiative wheel — the "summoned combatant enters the wheel" rule (`rules/combat.md`, Initiative) doesn't apply, because they aren't combatants. They just hold their rolled HP at Pat's position until something reduces them to 0, same as a totem. **They can be attacked directly** — an enemy can target the spirit instead of Pat or an ally. Since a spirit has no cards and can't choose a defense, the natural reading is that an attack against one auto-hits, no RPS — the same outcome already defined for any target that can't or won't defend (`rules/combat.md`, Attack Resolution) — a reasonable extension of an existing rule, not a new one, but worth confirming rather than assuming.

**"Object" as a formal category doesn't exist in `rules/combat.md` yet** — it did before this repo's rebuild, but didn't survive. Deliberately not formalizing it off one example: Pat's spirits work fine defined narrowly as they are above. Worth writing as a real general rule once there are more Objects to generalize from, not before.

**In the simulator, as of 2026-09-19.** Spirits are modelled as Combatants carrying an `is_object` flag rather than as their own class — the damage pipeline, targeting and positions then all work on them unchanged, and having no hand they can never choose a defence, which *is* the auto-hit reading above rather than a special case written to produce it. They take no turn because nothing puts them on the wheel, and a side is not still standing because a totem is. The d10 goes into Soul, because max HP is derived and must stay derived (`rules/invariants.md`), and 4×0 + 0 + HP is exactly the roll.

**LET'S GO's totem buff is held on the spirit and taken back when it drops**, which is what *kill the totem, lose the buff* means mechanically. Its defence half rolls a real Soul Save per enemy against Pat's Soul + 10 and compels the failures through the same MUST_TARGET that MOCKERY runs on.

**HERE BOY's rider goes to Pat, ruled 2026-09-19**, and the card was reworded to say so. The old text read as the spirit gaining it, which could never fire — a spirit does not act and cannot defend, so it never reaches a reveal. The summoning grants the tie-win to the summoner: he holds it and spends it on the next tie he is in, attacking or defending. The engine runs it.

Still open:

- Whether HERE BOY and LET'S GO are the *only* two triggers.
- Whether more than one spirit can be out at a time (there are only three to draw on). *The engine permits it and numbers them; it is not enforcing a cap it was not given.*

## Passives

- **STRONGJAW** — `campaign/passives.md`. A Shunka's bite; Red, Melee only, d6.
- **HACKLES RISE** — `campaign/passives.md`. Instinct for hostile intent; Green, Both, d4.

## Skills

- **Survival +2**
- **Animal Handling +2**

## Gear and coin

**He owns nothing yet, and that is a statement about the sheet rather than about him** — gear simply has not been worked on (the note at the top of this file). Everything below is the correction for that, not a decision about who he is.

**Starting gold: 40.** The maximum anybody starts with, and he gets it because he came out of creation with less on him than anyone at the table (`rules/equipment.md`, Starting Gold). *It is one session's pay in the first band, which means it buys supplies and cannot reach the gear ladder — a Tier 1 accessory is 100 and stays 100.*

**At the Nest that is four things off a counter.** Dockhook Lines and Low Lanterns run 10 apiece and the dock foodstuffs are 5 to 8 (`items/vultures-nest-items.md`). **He is the one character who arrives with shopping to do**, which is a good thing for a first session rather than a hole in the sheet.

**The fiction is a soldier's savings and it needs no more work than that.** Son of a Captain, years in the ranks, officer school in his twenties — a man who was paid for two decades and then left. *Of the three, his is the background where having some money on him requires no explanation at all.*

**He wants one object, and it is the right one.**

### The scrap

**A scrap of cloth off the original cursegiver, and it still carries a faint smell.**

**No slot, no bonus, no rules on it** — the same standing as Chris's spell book (`campaign/chris.md`, The spell book). It is not an accessory and should never be priced. *It does not make him better at anything. It makes one thing possible that is otherwise not possible at all, which is a gate rather than a bonus (`flora/README.md` for the principle, though this is nobody's plant).*

**Why it still smells, which is the whole object.** The cursegiver was not killed. She was **unmade — "as though never Cut at all"** (`factions-and-races/races-lizardkin.md`, The Cursegivers), which means not killed but made never to have been legible. So her own family cannot produce her name or her face; they inherited a technique from a person they are constitutionally unable to describe.

**A smell is not legible.** It is not a name, not a face, not a symbol — it is residue, and the unmaking had no grip on it. **That is why one scrap of cloth outlasted a woman the world deleted**, and why it is faint: it is the last of something reality no longer keeps a slot for.

*Which makes this the only physical trace of her that exists anywhere, held by the one person hunting her line.*

### What it actually does at the table

**It cannot find anyone.** Four hundred islands do not get swept by a nose, and the search still fails productively at the Nest the way it is supposed to (`campaign/session-1-convergence.md`, Pat — chasing one living person).

**Its first real use is a no, and that is by design.** Pneum's congregation is led by a Lizardkin (`places/pneum.md`, The Speaker) — the first specific lead anybody hands him, learned off Corvel for the cost of a question nobody else at that dock would think to ask. **He follows it, and the scrap clears them.** *A negative from an instrument that cannot be wrong is worth more this early than a hit would be: it proves the thing works, it eliminates a lead honestly, and it leaves him standing in front of the first Lizardkin off the island he has ever met — which is the first person alive who can tell him why one of them would leave.*

**What it does is confirm.** Family scent carries. Put Pat in a room with the bloodline and **he knows — no roll**, because the alternative is a die deciding whether the campaign's spine is findable. *Until then it tells him nothing, which is most of the year.*

**The roll is for everything past yes.** How recently, how many, which way they went, whether this is the one or a cousin — that is where **Survival +2** earns its place, and it is a real check with a real failure that costs nothing load-bearing.

### What it is worth to the people he is hunting

**They cannot describe their own ancestor, and he is carrying her.** A family that has held one technique for generations, around a hole where the woman who first used it should be — and a stranger walks in with the last of her.

*So the eventual meeting is a trade before it is a fight, and it does not have to become one at all.* **Offered rather than set**, in the same register as the gap in the line it hangs off, which that file also marks as a proposal (`factions-and-races/races-lizardkin.md`, The gap in the line). **Pat's, and Drew's.**

**Deliberately not being tracked yet** *(Drew, 2026-09-21)*. That meeting is far enough out that maintaining it as a live thread would cost more than it is worth, and a consequence this clean does not decay from being left alone. **It is written down so it is here when the meeting gets close, not so anyone carries it in the meantime.** *Nothing between now and then needs to be arranged for it. If the scrap survives and the bloodline turns up, the trade is simply available.*

### Where he got it — settled

**His mother's line.** *Confirmed 2026-09-21 — Pat had already said so, and it was the reading this file arrived at independently.*

Generations of Shunka who turned to wild magic trying to break the curse, and failed (`factions-and-races/races-shunka.md`). **A failed research tradition keeps its samples.** They had a piece of her, they kept it, and it came down matrilineally with everything else he carries.

*Which ties the object to the hook this file already calls the real one — his mother's side, not royal blood. **The cemetery gave him a direction. His mother's people gave him the only thing that can tell him when he has arrived.** The vision is what sent him; the scrap is what his own family had been holding the whole time, against the day somebody could use it.*

**Still open beyond the scrap:** what he carries out of Shunka service, and whether anything else of his mother's came with him. **He has asked for one item and one item is an answer**, not a gap — a man who left with a single object is a clearer character than a man with a packing list.

## Deck

Nine cards total, same shape as any character (`rules/character-creation.md`, Starting Deck): **3 custom cards** (all 3 now written — `campaign/pat-cards.md`: HOLD THE LINE, HERE BOY, LET'S GO), drawn from a list of ideas Pat gave Drew, plus **6 from the normal Oracle draft** alongside the rest of the table, still to happen at the table.

## Not Yet Set

Not everything below is a Session 1 gap — some of what Drew and Pat talked about is meant to come in through character progression later, not land on the sheet now. Genuinely still needed before Session 1:

- Character name
- Appearance beyond the Cane Corso reference, voice
- Some backstory questions — not itemized yet, Drew flagged these as still open without specifics
- **Gear** — hasn't come up at all yet: starting garb/weapon, and whatever he ends up actually using (`rules/character-creation.md`, Equipment — there is no slot limit, only what one person can use in concert)
- Price
- The 6-card Oracle draft (table activity, not something to pre-decide)

Open, but possibly progression rather than a creation-time gap — not yet sorted which:

- The open questions under Wild Magic Summoning, above

## Related Documents

- `campaign/passives.md` — STRONGJAW, HACKLES RISE
- `campaign/pat-cards.md` — his 3 custom deck cards
- `factions-and-races/races-shunka.md` — the Shunka people, the curse, the wild-magic line
- `rules/character-creation.md` — Stats, Skills, Passives, Starting Deck
