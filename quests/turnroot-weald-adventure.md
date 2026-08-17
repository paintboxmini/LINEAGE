# The Turnroot Weald — Adventure System

A full campaign framework for running the Turnroot Weald. For location overview and world context, see `places/turnroot-weald.md`.

---

## Pressure Track

Pressure only increases on failed navigation or customs violations. The DM may hold at the current level for strong RP or compliance (e.g., following moss signs perfectly).

| Level | Name | State |
|-------|------|-------|
| 0 | Unsettling | Misleading routing. Glimpses of the Pathless Child. |
| 1 | Watched | Hostile plants begin to emerge. Moss-Warden can now be found. |
| 2 | Predation | Failed navigation triggers Rootstalker ambush. Knot-Keeper can now be found. |
| 3 | Lethal Forest | Deadly traps activate on movement between scenes. Pathless Child Trial triggers. |
| 4 | Root Heart | Boss encounter. Beating the Root Heart opens escape. |

**Pressure 4 is not the only road to the Root Heart.** A gold piece paid into Seeker's Price opens the way there directly, at whatever Pressure the party is currently carrying — voluntarily, and much earlier than the track would have taken them.

**Overgrowth Floor.** The Root Heart is currently in its Overgrowth phase (`bestiary/root-heart/README.md`, What It Is / GM Notes) — this holds for the entirety of this campaign. While it's active, Pressure cannot rest below **1 (Watched)**: the hostile-plants-emerging baseline is simply present, independent of how well the party is keeping customs. Escalation past that floor still requires a failed check or a Custom violation exactly as stated above, and the DM may still hold at the current level for strong RP or compliance.

### Rootstalker Trail Quality (Overgrowth)

Under the old, pre-Overgrowth ruleset, Rootstalkers only entered play on failed navigation at Pressure 2+ (`bestiary/rootstalker/README.md`, still the correct behavior once Overgrowth ends — see Post-Defeat). **Overgrowth changes when they start, not what they are:** the mobile pruning tools have turned on the people they used to pass, and that hunger is present in the woods from the moment the party steps under canopy — not gated behind a Pressure threshold or a failed check. What Pressure controls instead is how well they hold the party's trail once they're already looking.

| Pressure | Trail quality | What it looks like at the table |
|----------|---------------|----------------------------------|
| 0 | Thin | Glimpses, wrong turns, a Rootstalker that loses the scent. Ambush is possible but unreliable — the forest is hunting, not yet locked on. |
| 1 | Firming | They find the trail more often. A failed navigation or a loud custom violation is enough for contact. |
| 2 | Reliable | Failed navigation triggers ambush as the original table states. Even successful travel may draw a stalker if the party is noisy or marked. |
| 3 | Locked | The trail is held. Moving between scenes risks contact whether navigation succeeds or not. Stalker Nest becomes a live threat, not a POI the party can stumble past safely. |
| 4 | Centre | Forced Root Heart. Stalkers may still be present as the forest's outer edge of the same hunger. |

Pressure still only rises on failed navigation or customs violations (DM may hold for strong compliance, same as always). Overgrowth doesn't make Pressure climb on its own — it only means the hunters were already in the woods when the party arrived.

**After the cut,** the Weald returns to the ruleset this file already describes everywhere else — that's the normal state, not a new one:

| State | What runs |
|-------|-----------|
| **Overgrowth** (this campaign, until Root Heart falls) | Rootstalkers hunt from entry; trail quality scales with Pressure (above); Forest Customs enforced hard; the Holdfast under pressure |
| **Normal** (after a successful cut, or any future visit past this one) | Rootstalkers gate at Pressure 2+ on failed navigation only (`bestiary/rootstalker/README.md`); no baseline hunting from step-in; forest-people range recovers over time |

The party's own cut, if they make it, is one more ring (`bestiary/root-heart/README.md`, What It Is).

---

## Forest Customs — Sharpened (Overgrowth)

Meta rules for the table. Under canopy, the Weald treats them as law. **Overgrowth doesn't add new laws — it enforces the existing ones with less patience,** which is why three customs (the ones the Moss-Warden asks about) have widened into six, and the consequences now scale with current Pressure instead of landing flat.

Violations are judged by what was *done and said*, not by intent. A player who means well and breaks a custom still broke it.

| Custom | What counts as violation |
|--------|---------------------------|
| **Do not name a destination under canopy.** | Saying where you are going, where you came from, or where you hope to arrive. Includes "back to the road," "the Heart," "Aege's people," "the way we came," and pointing while naming. Soft references ("somewhere safer," "out") are still naming if the table can tell what you meant. |
| **Do not thank the forest.** | Thanks, gratitude, or debt acknowledged *to the Weald or its signs* — trees, roots, moss, birds, "luck," "the path that opened." Thanking a *person* (Aege, a forest-family member, another PC) is safe. Thanking "whatever got us here" is not. |
| **Step over what lies in your path.** | Going around a fallen branch, a root, a stone, a body, or a pool counts as refusal. Stopping to clear it and then walking the cleared line is also refusal — you reshaped the path instead of taking it. Stepping over is the only clean option. If it's too large to step over, the path wasn't offered; turn back or take a different route. |
| **Do not leave a mark that claims.** | Blazes, cairns, tied ribbons, mapped notes left on trees, nails, or anything that says *we were here and this way is ours*. The forest erases these and treats the attempt as a claim on its ground. Temporary rope for a climb is fine if it comes with you when you leave. |
| **Do not take without a reciprocal gesture.** | Harvest (leaves, fibers, larvae, cores) requires a small, deliberate return — a coin pressed into bark, water poured at the root, a knot left untied for the next walker, silence held for a count of ten. Pocketing and walking on is theft. The gesture doesn't have to be valuable; it has to be *offered*. |
| **Do not speak of leaving as a plan.** | Discussing exit strategy, "when we're done," "once we find a way out," or counting days until the capital, while under canopy, is treated as naming a destination you haven't been given. You may leave. You may not *schedule* it out loud. |

The first three are the ones the Moss-Warden will ask about (her riddle, below, is unchanged spine). The last three are the ones parties invent for themselves and then trip over.

### Violation Consequence Matrix

Consequences scale with Pressure. Under Overgrowth, Rootstalker trail quality is already climbing on the same track (above) — a custom violation can hand them the scent.

**Naming a destination**
| Pressure | Consequence |
|----------|-------------|
| 0 | Misroute to a neutral node. Trail thins for the stalkers this time. |
| 1 | Misroute. Next navigation DC +2. |
| 2 | Misroute into hostile flora **or** Rootstalker contact (DM picks which fits the fiction). |
| 3 | Rootstalker ambush on a held trail. |
| 4 | Forest tightens — toward the Heart, not away from it. |

**Thanking the forest**
- Pressure +1 immediately, every time.
- At Pressure 2+, the forest may also "collect" — a small item goes missing from a pack, or a wound refuses to close until something is left behind. Not lethal; noticeable.

**Stepping around (refusal)**
| Pressure | Consequence |
|----------|-------------|
| 0–1 | Next navigation DC +2, or the path behind closes (cannot backtrack the way you came this scene). |
| 2 | Trap roll or environmental complication **and** DC +2. |
| 3 | Pressure +1 **or** Rootstalker contact. |
| 4 | Both. |

**Leaving a claim-mark**
- Pressure +1 the first time.
- The mark is gone by the time they look back. If they insist on re-marking, treat as a second violation at the next Pressure band up.

**Taking without gesture**
- The thing taken withers, sours, or fails when used (Luminova leaf heals half; fiber rope frays on first load; larvae arrive dead for Senshi).
- Second offense in the same visit: Pressure +1, and Rootstalkers treat the party as thieves of the body — trail quality one band higher than current Pressure until the party makes a deliberate reciprocal offering somewhere the forest can see it.

**Speaking of leaving as a plan**
- Same band as **naming a destination** (it's naming, deferred).
- Soft first warning only if Pressure is 0 and the line was ambiguous; after that, full matrix.

**Table notes:**
- **Stacking.** Two different customs broken in one scene can both fire. Naming + thanking is a common pair.
- **Whispers and notes.** Writing a destination on paper under canopy is still naming if it's read aloud later under canopy. Passing a written note silently is the loophole that exists until the DM decides it doesn't.
- **Forest-people.** They keep these customs without thinking. They will correct the party once, flatly. A second correction isn't coming; the forest will.
- **Aege.** She doesn't explain the list. She'll change the subject, take a path that makes the broken custom expensive, or say *"You're already ahead of yourselves."* and wait.
- **Compliance.** The DM may hold Pressure for a stretch of clean conduct — the track still only rises on failures and violations — but Overgrowth means the hunters were already out. Clean conduct doesn't send them home; it only keeps the trail thin.

Custom violations may also justify failed navigation or direct escalation at DM discretion.

---

## Navigation

A navigation check is required when attempting to change location — even when backtracking. No check is required when following forest "signs."

**Clear signs must be earned, not handed out freely by the DM.** Examples of earned signs:
- The direction the moss grows
- The slope of terrain
- Birds and other wildlife

**Signs can also be bought.** Seeker's Price takes coin pressed into the wood and gives signs back — see that entry for what each denomination buys.

**Standard check:** DC 13 using one of three modes. DM can adjust ±2 based on fiction (e.g., +2 in dense roots, −2 when following earned moss signs).

| Mode | Stat | Used When |
|------|------|-----------|
| Reason | Mind | Reading the environment analytically |
| Senses | Body | Navigating by physical instinct or feel |
| Read | Soul | Interpreting the forest's intent or mood |

---

## NPC Escalation

NPCs unlock at specific Pressure levels and do not appear before their threshold.

### Pressure 0 — The Pathless Child *(glimpsed only)*

Observed in the trees. Not yet fully interactable. A flash of movement, a small figure vanishing between roots. Players cannot initiate contact at this stage.

---

### Pressure 1 — The Moss-Warden

*Moss cloak has a shifting, living pattern. Can hint at the forest's inner workings. Grants the Moss-Warden Mark via riddle.*

The Moss-Warden turns as the players enter the clearing. Concentric circles of moss form around them.

> *"Have you come to abuse the forest like so many others? Or are you finally ready to return to it?"*

The shifting patterns of the moss on their cloak draw the players' eyes.

> *"Three passed this way before you."*
>
> A pause.
>
> *"One thanked the trees. One named where they were going. One stepped around what fell."*
>
> Now they look up.
>
> *"Which one are you?"*

**Mark granted:** Moss-Warden Mark (awarded if players answer honestly or demonstrate alignment with forest customs).

---

### Pressure 2 — The Knot-Keeper

*Sacrificial mechanic. Bracelet = Mark. A core personality trait is woven into the bracelet — this is a roleplay cost.*

**The Mechanic:** Players can sacrifice a core personality trait (e.g., bravery, mercy). The trait becomes "woven in" — unreachable but not gone.

**Bracelet Ability:** When the bracelet is undone, the player auto-wins one RPS exchange. The trait is restored immediately after. Single use per undoing.

The Knot-Keeper may be introduced in one of three tones depending on table energy:

**1. Calm, Ritualistic**

The shaded hollow feels wider than it should. Roots curl back from a flat stone where the Knot-Keeper sits, fingers working dark cord into tight, deliberate loops. They do not look up.

> *"You have learned how quickly the forest closes."*

A pause.

> *"I can hold it open for you."*

Now they look up — steady, unblinking.

> *"But it will take something that would otherwise help you."*

**2. Intense, Direct**

The air is quieter here. Even the insects stop at the boundary of shade. The Knot-Keeper ties a final knot and pulls it tight with a sharp snap.

> *"Safety is not free."*

They lift the bracelet.

> *"You may walk with less of yourself."*

A thin smile.

> *"The forest prefers travelers who are incomplete."*

**3. Warning Without Drama**

The stone beneath them is worn smooth by years of sitting.

> *"You think the roots hunt because they hate you."*

A knot is tightened.

> *"They hunt because you are whole."*

The bracelet is offered.

> *"I will bind away a piece."*

Their eyes hold yours.

> *"Understand this: it will not be gone. Only… unreachable."*

**Mark granted:** Bracelet (Knot-Keeper Mark).

---

### Pressure 3 — The Pathless Child Trial

A skill-based routing challenge. All checks are DC 13. Likely Senses (Body) heavy.

**The Binary Trail** *(Mind / Reason)*
You find a barefoot print pressed deep into soft mud, heading North. Simultaneously, a cluster of white flowers ten feet to the East is bent and crushed, as if someone just ran over them.

*Choice:* Follow the Heavy Mark (the print) or the Light Interruption (the flowers)? One leads deeper into the chase; the other leads to a dead end.

**The Whispering Canopy** *(Body / Senses)*
The brush is so thick it feels like a wall, but you see the Child's red cloak flash through a gap to the left. At that exact moment, the branches to your right shiver and thrum rhythmically, as if something just brushed past them.

*Check:* Body check to push through the resisting brush. On failure, the forest tightens and you lose the scent.

**The Inverse Horizon** *(Soul / Read)*
You reach a small rise. Below you, the Child sits calmly on a stump. But when you look at the dew on the leaves in front of you, the reflection shows the Child standing directly behind you, watching.

*Check:* Soul check to trust the Reflected Truth over the Visual Lie.

**Mark granted:** Pathless Trial Mark (awarded for passing all three checks).

---

## Mark System

Marks represent alignment with the forest. They do not reduce Pressure.

| Mark | Source | How Earned |
|------|--------|------------|
| Moss-Warden Mark | Moss-Warden | Answer the Warden's riddle honestly |
| Bracelet | Knot-Keeper | Accept the bracelet and sacrifice a trait |
| Pathless Trial Mark | Pathless Child Trial | Pass all three DC 13 checks |

**Marks unlock the primary escape condition.** Collecting all three marks allows the party to exit the Weald freely.

---

## Escape Conditions

Three ways out, and the forest treats them as equally valid:

1. **Collecting all 3 Marks** — the forest releases you. *Earn it.*
2. **Defeating the Root Heart** — boss encounter at Pressure 4. *Win it.*
3. **Paid Passage** — pay gold into Seeker's Price, be guided to the Root Heart, and *look at it*. The forest lets you leave. *Buy it.*

**The Root Heart does not attack a party that paid.** The forest brought them; the Heart honours that. They stand in front of it, they get as long a look as they want, and nothing happens. A GM who runs it as a boss encounter anyway has collapsed the third exit back into the second.

**On the third.** The transaction completed. They asked to be taken to the heart of it, they were taken, and they saw. Nothing further is owed in either direction, and the Root Heart is still alive behind them — the only exit that ends with that being true.

It is not a shortcut past the others so much as a different bargain. Marks cost three separate acts of alignment with a forest that is hard to align with — including sacrificing a trait to the Knot-Keeper. The boss fight costs a boss fight.

**Paid Passage costs almost nothing and returns almost nothing.** No Marks. No kill. No loot off the Heart. The party leaves with exactly what they walked in holding, minus a coin, having looked at the thing everyone else in the Weald is trying to survive. It is cheap because it is empty, and that is the correct trade rather than a hole in it — a table that takes this exit will feel the difference without anyone at the table saying so.

---

## Points of Interest

The following locations can be discovered during navigation. DM places them as appropriate or uses them as navigation destinations (unnamed, of course).

---

### Root Tunnel

Interwoven root fibers, still damp. Some pulse faintly. The air smells green — like fresh growth. When someone whispers, it sounds like it comes from deeper ahead.

Halfway through, the corridor narrows. Roots tighten. Then stop.

There is a pocket. Not a chamber — just a widening.

In the damp soil: a child's footprint.

---

### The Fallen Tree *(custom enforcement — ties to "Step over what lies in your path")*

A trunk has come down across the only clean line the signs were offering. Not a branch — a full tree, crown still tangled in the canopy on one side, root-plate lifted on the other. Bark is wet. Branches form a rough ladder if you commit to the climb. There's no gap underneath a person can crawl without going around.

**The custom is absolute here.**

| Choice | Result |
|--------|--------|
| Go around | Refusal — full consequence matrix for stepping around |
| Clear it / cut a path | Refusal — you reshaped the path instead of taking it |
| Take a different route entirely | Naming/refusal hybrid — the forest offered *this* path; leaving it is treated as going around |
| **Climb over** | Clean. No Pressure. No custom break. |

There's no third option that stays legal. They go over, or they raise the track.

**The Climb — DC 17 Body (Senses or raw exertion, DM's read of the fiction).** Only one character must succeed. On a success, that character reaches the crown and can lower a rope, extend a hand, or haul the others up — the rest follow without individual checks once the first is set. **Advantage** if at least one ally helps from below (boost, braced rope, calling holds) — helping is an action or a clear fiction commitment, not free while also climbing. On a **failure**, the climber falls or slides back to the near side; no damage required unless the fiction is nasty, the cost is time, noise, and another attempt. A loud failure is a gift to anything tracking them — treat as a minor noise event against current Rootstalker trail quality (above). Tools (rope, a Dockhook Line) justify Advantage or a second helper; they don't lower the DC. The tree is the test, not the kit.

**What's in the crown.** The first climber reaches the top *alone*. The others are still on the trunk or the ground. A **Flower Snake** (`bestiary/flower-snake/README.md`) has been still the whole climb — pattern matches blossom and bark. It strikes while the climber is alone. See that file's Ambush section for the check. This isn't a Rootstalker. The forest isn't pruning anyone here — something smaller is using the custom as cover.

---

### The Thorne Throne

**The Sight:** A massive, gnarled throne grown directly out of the forest floor. Not made of wood — grown from a singular, continuous Echothorn vine that has wrapped around itself millions of times. Beautiful, jagged, and looks deeply uncomfortable.

**The Sound:** *Orororororo…* A low vibrating hum that feels like it comes from the ground beneath the throne. The sound of the forest looping a specific intent.

**Loot:** Echothorn Seeds. See `items/turnroot-weald-items.md`.

**GM Secret — Not Player-Facing.** This is the manifested Seat of Change — a Resonant Item at Stage III, Embodiment (`world/seats.md`, Change). It was a thorn whip once, carried and used by Elias without him ever noticing how long, until continued use pushed it past a whip and into whatever this is now. The moment it finished becoming this, he left it and never came back. Nobody in Turnroot Weald knows what it actually is or who left it. The low looping hum is the closest thing to an explanation anyone here has — the forest repeating an intent nobody's left to explain, over and over, the same way the vine itself is one strand wrapped around its own pattern millions of times.

---

### The Floating Gallery

**The Sight:** Large, iridescent leaves hover inches away from the branches they "belong" to. In the center, a rusted piece of armor is suspended in mid-air, held by the forest's repulsion field. It is clean of rust only where hovering leaves brush past it.

**The Sound:** A low-frequency vibration that makes water in canteens ripple.

**Loot:** Rusted Armor (5 temp HP). See `items/turnroot-weald-items.md`.

---

### The Reciprocal Clearing

**The Sight:** Moss grows in perfect concentric circles.

**The Interaction:** If a player leaves something behind (a ration, a copper coin), the trees lean back and the path ahead widens. If they take something (a stone, a flower), the exit they came from is simply gone when they turn around.

---

### The Mirror-Slick Pond

**The Sight:** A pool of water so black and still it looks like obsidian.

**The Sound:** Absolute silence. The forest's ambient noise stops at the water's edge.

**The Reveal:** Your reflection isn't doing what you are doing. It shows a different choice you made earlier in the forest. Look long enough and you see your reflection holding one of the Marks you haven't earned yet.

**Loot:** Vision Shard. See `items/turnroot-weald-items.md`.

---

### Seeker's Price

**The Sight:** A cluster of trees where the bark has grown around hundreds of copper coins and rusted gear — not covered, but fused. A wall of metal and wood.

**The Sound:** When wind blows, the metal chimes against the wood — hollow and metallic.

**The Reveal:** These are payments made by travelers for safe passage. **The wall still takes them.**

---

**Paying in.** Press a coin into the wood and it accepts — closes over the metal without ceremony, the way a mouth takes something offered. What the party gets back is *signs*: the moss, the slope, the birds, all of it suddenly legible. Following forest signs requires no Navigation check (see Navigation), and this is how those signs are earned.

**What you give decides what you are shown.**

| Payment | What the forest gives back |
|---|---|
| **Copper** | Signs for the next leg. One location change, no Navigation check. |
| **Silver** | Signs that hold. No Navigation checks until Pressure next rises. |
| **Gold** | It routes you to the centre. **The way to the Root Heart opens.** |

**Do not advertise the third row.** A party offering a whole gold piece at a wall of coppers is not asking for directions — it is asking to be taken to the thing, and the forest's answer to that question is always the same place. Let them find that out by doing it.

**The wall reads the gesture, not the sum.** One gold coin is a trivial amount of money — the Tollworn Plate a foot away is worth two hundred of them. That is the point. The wall is not being bought; it is being *addressed*, in a denomination nobody else here uses, and it answers accordingly. A party that presses in fifty gold gets exactly what one buys.

This is also the only way to reach the Root Heart **on the party's terms** rather than being forced into it at Pressure 4. The forest is perfectly willing. It just takes the request literally.

---

**Taking out.** The standing rule holds — **Pressure +1** — and it is worse than ordinary theft. These tolls were *accepted*. Taking one back undoes a transaction the forest already closed, on behalf of someone who paid it and walked away.

**The Plate.** Set into the wall, chest-high, is a piece of armor — old pattern, rust in the seams, bark grown through the strap holes. The **Tollworn Plate** (`items/turnroot-weald-items.md`): Tier 1 armor, **Armour 1**. It is the first real equipment the campaign hands over, and it should arrive **before the Root Heart**, not after.

**How they get it out decides what it costs:**

- **If they have paid into this wall** — any denomination, at any point — the wood lets go. No Pressure. They are taking out less than they put in, and the wall keeps its own books.
- **If they have not** — Pressure +1. They go into that fight wearing something somebody else bought their life with.

**A party that pays gold and then pries the Plate out is trying to have both.** The wall permits it. Let them feel it anyway.

**There is exactly one, and the party has to decide who wears it.** Do not let this pass as inventory management. It is the first time the group has had to put something real on one person, and the choice is worth the minute it takes — the one who has been going down most, the one at the front, the one who asked. Whoever it is, everyone watched it happen.

If the party cannot agree, the plate stays in the wall. The forest is content to keep it.

---

### The Holdfast *(Aege's people)*

A small region of the Weald that still behaves. Moss signs stay true. Roots do not surface underfoot mid-stride. Rootstalkers have been seen at the edge and turned away — or have not, and the holdfast is smaller this week than last.

**Who lives here.** A forest family: a handful of adults, fewer children, no permanent structures that would insult the canopy. Cord-wrist customs — the same grammar as the Knot-Keeper's bracelets, practiced without the sacrifice. They will share water and a route-song. They will not leave with the party.

**What they know.**
- The Root Heart is awake in a way it was not a season ago.
- Rootstalkers have taken three of theirs in the last month — not redirected, *taken*. Bodies not found.
- The safe ground is measured in walks, not miles, and it is shorter every time someone counts.
- A daughter left years ago. They do not use her name with strangers. If Aege is present, no introduction is required.

**Customs.** These people already keep the Forest Customs. Thanking them for help is safe; thanking *the forest* in their hearing is still a violation. They will correct the party once, flatly.

**Pressure.** Arriving here does not raise Pressure. Fighting a Rootstalker on the holdfast's edge does. If the party leads a Rootstalker *into* the holdfast, Pressure +1 and the family's trust is spent.

**Aege.** If she has already parted from the party at Briarwatch, she may be found here when the party arrives — or the family may say she passed through and went deeper, toward the Heart. She does not use the party as escort. She will accept their company if they are already going the same way.

**Loot / payment.** Nothing for sale. If the party clears a Rootstalker that was pressing the edge, the family may offer a route-song that functions as forest signs for one navigation (no check) — the same gift Seeker's Price sells for copper, given freely once.

---

### The Half-Sunken Shrine

A shrine overtaken by roots. A single intact bronze bell hangs, undisturbed by growth around it. The roots seem to curl away from the bell specifically.

---

### Stalker Nest

**The Sight:** Roots at the base of a tree have pulled away from the forest floor, forming an archway that descends into the earth.

**The Sound:** Skittering movements echo from below.

**The Reveal:** An underground Rootstalker nest. Half-formed Rootstalkers are being *extruded* from the thick root lattice of the den walls. Sleeping Rootstalkers lie in the den — players who are not careful will wake them.

See `bestiary/rootstalker/README.md` for stat block and loot.

---

### Luminova Clearing

A clearing dense with Luminova growth — translucent leaves emitting soft bioluminescent light. The glow is faint enough to navigate by, bright enough to disturb sleep.

**Loot:** Luminova Powder. See `items/turnroot-weald-items.md`.

---

### The Hanging Gallery *(hazard — Future-Lock Wasp colony)*

Old trees with heavily grooved bark. The overhanging bark creates natural alcoves along each trunk. Closer inspection reveals something inside each one.

DC 13 Mind/Reason to spot the nests before entering. On failure, the party disturbs the colony.

**Encounter:** See `bestiary/future-lock-wasp/README.md` for swarm mechanics, save DCs, and dispersal methods. Fire is risky here — dense canopy, DM discretion on spread.

**Harvest:** DC 14 Body/Senses to extract larvae without triggering the swarm. A dispersed swarm leaves nests unguarded for 1 minute — free harvest window.

**Loot:** Future-Lock Wasp Larvae. See `items/turnroot-weald-items.md`.

---

### The Web-Forest *(optional — Bone Collector lair)*

Fog thickens here. Ancient spider webs span between trees like abandoned bridges.

Fresh corpses hang in the webs — but they're *missing pieces*. Precise cuts. A merchant's arm. A guard's helmet. A horse's leg. The bodies look *edited*.

A massive spider corpse hangs center-web. Investigation reveals it died first. Something else has been using its territory.

Soft scraping sounds move deeper in the web-maze. Something large, moving between silk highways.

**Encounter:** See `bestiary/bone-collector/README.md` for the full encounter, cycle structure, and investigation aftermath.

**Loot:** Spider Silk Rope, Harvest Bead, Bone Collector Flesh. See `items/turnroot-weald-items.md`.

*This area is not placed on the critical path. DM drops it when the party is exploring off-route, or as a destination if they've taken the Gilded Tusk commission from Senshi.*

---

## Distractions

False navigation cues the forest uses to mislead. DM rolls or chooses based on Pressure level.

| Type | The Lure | The Path | The Consequence |
|------|----------|----------|-----------------|
| **Mineral** | A trail of jagged obsidian shards reflecting the sky. | Smooth, worn river stones hidden under dead leaves. | You follow the sparkle into a Stalker Den. |
| **Flora** | Broken branches pointing East with jagged, fresh white wood. | A line of saplings leaning West, as if bowing to a passing guest. | The brush knots behind you, trapping you in a Root Tunnel. |
| **Atmospheric** | A sudden shaft of bright sunlight hitting a clearing ahead. | A pocket of cold, damp mist that smells like fresh growth. | You arrive at the Thorne Throne — but it isn't empty. |

---

## Encounter Loot Summary

| Item | Found At | Notes |
|------|----------|-------|
| Echothorn Seed | Thorne Throne | See `items/turnroot-weald-items.md` |
| Luminova Powder | Luminova Clearing | See `items/turnroot-weald-items.md` |
| Rusted Armor | Floating Gallery | See `items/turnroot-weald-items.md` |
| **Tollworn Plate** | **Seeker's Price** | **Tier 1 armor — the campaign's first real equipment. One only; party chooses the wearer.** |
| Vision Shard | Mirror-Slick Pond | See `items/turnroot-weald-items.md` |
| Root Fibers | Rootstalker (common) | See `items/turnroot-weald-items.md` |
| Sap Vial | Rootstalker (rare) | See `items/turnroot-weald-items.md` |
| Spider Silk Rope | The Bone Collector | See `items/turnroot-weald-items.md` |
| Harvest Bead | The Bone Collector | See `items/turnroot-weald-items.md` |
| Bone Collector Flesh | The Bone Collector | See `items/turnroot-weald-items.md` |
| Future-Lock Wasp Larvae | The Hanging Gallery | See `items/turnroot-weald-items.md` |
| Rootstalker Core | Rootstalker (very rare) | See `items/turnroot-weald-items.md` |
| Kiwi Bird | Weald undergrowth | Not a fight — a tracking/stealth problem. Senshi's Second Commission, `places/capital/gilded-tusk.md`. See `bestiary/kiwi-bird/README.md`. |

---

## What It Pays

This is a framework rather than a single session, so it pays by the session rather than in a lump: **~40 gold per character per session at Tier 1**, rising with the party (`rules/equipment.md`, Pacing; multiply by party size).

**Most of it should arrive as harvest, not as fee.** The Weald is the most thoroughly priced region in the world — `items/turnroot-weald-items.md` lists what things are worth and Senshi at the Gilded Tusk buys specimens outright. A party that engages with the forest as a place with things in it will out-earn a party waiting to be paid, which is the correct incentive for this region and worth letting them discover rather than telling them.

Payment for specific jobs, where a job exists, comes from whoever asked — and in the Weald that is rarely anyone official.

**The Tollworn Plate is not part of this number.** It is found gear, off the gold curve entirely (`rules/equipment.md`, Pacing), and it is the campaign's first real piece of equipment — placed at Seeker's Price, before the Root Heart, one only. Do not price the session's income around it and do not hand out a second one.
