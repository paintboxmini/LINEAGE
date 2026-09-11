# Geography Overview

Glasslight Reach, Turnroot Weald, and Vulture's Nest form a rough triangle — Glasslight Reach to the north, Turnroot Weald to the southwest, Vulture's Nest to the southeast. Eclipseria sits at the center of that triangle. Ashfall Wastes sits below Turnroot Weald; the Abyssal Ruins sit below Vulture's Nest.

The Capital is roughly 8 days of travel from each major hub. Major hubs are roughly 13 days of travel apart from each other, extrapolated from that same measurement. The Regency maintains the roads and halfway-inns between them.

## The Kings Road

Three segments: a spoke from each corner in to the Capital at the center. All three are official Regency roads, maintained the same way, each with an official inn on it — a government installation, guards stationed, not a private business.

Where the roads are the Regency's arteries, the rivers and paths are everyone else's.

The three roads:
- Glasslight Reach ↔ Eclipseria
- Turnroot Weald ↔ Eclipseria — the Milestone sits on this one, roughly at the midpoint
- Vulture's Nest ↔ Eclipseria — the Kings Road Inn sits on this one, roughly at the midpoint

Turnroot Weald
wrapping the northeastern edge of the Ashfall Wastes, a sentient forest that insulates the rest of the continent from the barren lands beyond.

Vulture's
ringed by many islands in the surrounding rivers and lakes, where the river web is densest, and it's a hub for trade.

## River system 

A web of interconnected rivers laces the whole continent, pooling into lakes and joining and splitting again. This web is the continent's second road system — and its first, if you ask a sailor.

The water itself stays ordinary. The coastline is a hard threshold — unheldness does not cross it, not by flowing and not by being carried.

Waterfalls drive the circuit itself — climbing and falling, the push that keeps the whole web moving. The coast's own tide sets the in-and-out layered over that: water pushes inland as the tide comes in, holds, then pulls back out as it goes. That rhythm propagates through the web with a lag — when the outermost rivers, closest to the coast, are on their inward pulse, the innermost reaches are on their outward one, and vice versa. Two stretches of the same network can be running opposite directions at the same hour. The innermost reaches sit on the loop's own shortest circuit — bank width varies same as anywhere else in the system, that's not what does it. The loop itself simply has less distance to cover at the center than at the outer rings, and forcing a full inland pulse through that short a loop is what makes it dangerous: the same surge that spreads out and slows going out, has nowhere to go but through, all at once, near the center. High tide at the innermost web is the part sailors plan the most around. Eclipseria sits dead center of the river web, exactly where the loop is shortest and the tide runs fastest. This is exactly why river sailors are skilled at two different things, not one — reading which pulse a stretch is on and when it's about to turn is its own discipline, and actually handling a vessel through a current that can reverse under it is another. Knowing the water and working it are both real skill, not the same skill twice.

The loop runs clockwise — south along the eastern reach from Glasslight down toward Vulture's Nest, west across the southern stretch to Turnroot Weald, north back up to Glasslight. Traveling with that grain is the easy way: the current is doing half the work. Traveling against it — Vulture's Nest to Turnroot the short way, or any long haul upstream of the loop's natural pull — means giving up on fighting the current head-on and using the tide instead: ride an inland pulse as far as it goes, hold through the pause, catch the next outflow, repeat. Slower, and it only works because the tide's rhythm doesn't care which way the loop turns. A sailor who's only ever traveled with the loop has never actually needed both skills at once. A sailor who's fought it has.

Islands stand in the larger lakes and wider rivers. They are often inhabited, trade-connected, and reachable by boat. Whatever strangeness they hold is their own.

Where a river runs close to the coastline itself, its banks turn to coral — reef growth thick enough to shape the channel, not just line it.


## Wind system

The system breathes, on top of the loop.
Wind doesn't share the loop. It breathes the same in-and-out the tide does, only faster — each gust or breeze its own full inhale, a pause, an exhale, sometimes tight and quick, sometimes drawn into long still gaps between breaths — but there's no clockwise grain to it, nothing it runs with or against. It just pulses. Eclipseria with no prevailing direction to inherit, sits in crosswinds because of it — arriving from every side at once, never settling into one dependable quarter the way a coastal city's would.

## Bearing Table

**This file owns direction, distance and adjacency.** Anything anywhere in the repo that says where a place is relative to another place is making a claim about this table, and `agent-tools/check-geography.py` reads the rows below to check those claims. A bearing that isn't here isn't established — it's either unwritten or somebody guessed.

Bearings are rough compass sense, not survey lines. "Northeast" means *that general way*, not 45.0°.

| Place | Bearing | From | Established by |
|---|---|---|---|
| Glasslight Reach | north | Eclipseria | The Shape of the World, above |
| Turnroot Weald | southwest | Eclipseria | The Shape of the World, above |
| Vulture's Nest | southeast | Eclipseria | The Shape of the World, above |
| Ashfall Wastes | south | Turnroot Weald | The Shape of the World, above |
| Abyssal Ruins | south | Vulture's Nest | The Shape of the World, above |
| Canille | northeast | Vulture's Nest | `places/canille.md` |
| Pneum | northeast | Vulture's Nest | `places/pneum.md` |
| Apnea | southwest | Vulture's Nest | `places/apnea.md` — stated as south-southwest |
| The Coil | east | Vulture's Nest | `places/the-coil.md` |
| Briarwatch | east | Turnroot Weald | `places/briarwatch.md` — on the Weald's eastern edge |

**Adjacency, where it's stated rather than a bearing:**

- Turnroot Weald wraps the **northeastern edge** of the Ashfall Wastes, acting as a natural boundary.
- Glasslight Reach sits at the **northernmost edge of the known world**; the Soft Edge is the northernmost water.
- Briarwatch is cut into **Turnroot Weald's own eastern edge**, and its western fence is the boundary against the Weald.

**Distances.** The Capital is roughly 8 days from each of the three hubs. The hubs are roughly 13 days from each other. The Kings Road runs as three spokes, hub to centre — so the Turnroot spoke runs **northeast** from the Weald toward Eclipseria, and the Glasslight spoke runs **south** from the Reach.

**Coordinates** exist only on the Session 1 stretch, on a relative grid: the Unheld shoreline at roughly (0, −11), the Roadhouse at (0, −7) (`quests/washed-ashore.md`, `places/roadhouse.md`). Nothing else in the world is gridded and nothing needs to be.

### Deliberately unplaced

Not an oversight — these have no established position and a file that gives them one is inventing it.

- **North of Turnroot Weald** — blank country. The Weald's expansion runs into it (`quests/turnroot-weald-adventure.md`, The Return — After the Line Breaks), which is the reason to develop it.
- **The Silent Choir** — deliberately unmappable, not on any grid (`places/the-silent-choir.md`).
- **Clayhollow, Veldmire, Fog Basin, Weatherheart Vale, the Collection Plate** — written places with no stated position.
- **Havenrise, Roaat** — named in rumour only (`places/capital/adventurers-hall.md`, Word of Mouth).

### Resolved — Briarwatch

`places/briarwatch.md` used to open with Briarwatch **a day's travel west of Vulture's Nest** *and* cut into Turnroot Weald's edge. Those couldn't both hold: the hubs are ~13 days apart, so one day west of the Nest is nowhere near the Weald.

**The Weald adjacency won**, because everything load-bearing about Briarwatch hangs off it — the Masons' fence, the Weald's encroachment, the Root Heart's redirected growth, and Aege's own "a forest that presses right up against Briarwatch's own western edge." The Vulture's Nest day count was doing nothing but placing it, and placing it wrong.

Briarwatch is now described by what it touches: the Weald's eastern edge, two days inland from the Unheld shoreline by way of the Roadhouse. No distance to Vulture's Nest is asserted anywhere, and none needs to be.

## Key Landmarks (Summary)

| Location | Where | Notes |
|----------|-------|-------|
| Eclipseria (city) | Centre of the triangle | Capital; seat of the Regency |
| Glasslight Reach | North | Cliff town; faces the Soft Edge |
| Turnroot Weald | Southwest | Sentient forest; wraps Ashfall's northeastern edge |
| Ashfall Wastes | South of the Weald | Ash-buried ruins; strange heat |
| Vulture's Nest | Southeast | Heart of the river web; trade centre |
| Abyssal Ruins | South of the Nest | Vast warped ancient site |
| Briarwatch | The Weald's eastern edge | Farmland claim; two days inland from the shoreline |
| The Roadhouse | (0, −7) on the Session 1 grid | Regency waypoint between shoreline and Briarwatch |
| Canille | Lake northeast of the Nest | Island village; still water |
| Pneum | Lake northeast of the Nest | Sleeping village |
| Apnea | Own lake southwest of the Nest | Hospice island; the dreaming layer |
| The Coil | Deep lake east of the Nest | Doesn't appear on charts; the Ferryman knows where to look |

*Unplaced on purpose, and not listed above: the Silent Choir, Clayhollow, Veldmire, Fog Basin, Weatherheart Vale, the Collection Plate, and everything north of the Weald. See Deliberately unplaced, above.*
