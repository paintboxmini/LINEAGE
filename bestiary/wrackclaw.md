# Wrackclaw

**Cards:** `cards/wrackclaw.md`

*General field encounter along the Unheld Ocean's coastline — the shoreline south of the Roadhouse (`quests/washed-ashore.md`), and any other stretch of that same coast a GM wants to use one on. Not tied to a single beach.*

**Mind 1 / Body 2 / Soul 1 — HP 10**
**Creature Threat Rating:** 4

**Deck (4 — 1 Blue / 2 Red / 1 Green):** SIDELONG SCUTTLE *(blue)* · PINCH, STRIKE *(red)* · CARRION PULL *(green)*

Deck size = total stats. 3 signature + 1 core to fill: PINCH, SIDELONG SCUTTLE, CARRION PULL (signature — `cards/wrackclaw.md`) + STRIKE (R, core).

---

## Description

Fist-sized, pale-shelled, and numerous wherever the tideline deposits enough to eat. They don't distinguish between driftwood, dead fish, and anything else that's salt-wet and hasn't stopped moving yet — a party freshly washed ashore reads to a Wrackclaw exactly like the rest of the wrack line does.

They don't hunt so much as collect. A Wrackclaw doesn't need to kill what it's pinched — it needs to drag it back to the water, where the rest of the swarm is waiting. Losing a fight against Wrackclaws rarely means dying; it means getting pulled toward the surf one claw-length at a time until someone breaks the grip.

---

## Encounter Setup

Start with 3–4 Wrackclaws, all Frontline — they don't hang back, they don't reposition tactically, they just close and grab. The first real threat the party meets after washing ashore, before the trail is even found.

*Teaching moment: Rooted and forced repositioning both show up here, on cards a brand-new party has never seen work against them before — this is where "cannot voluntarily change position" and "moved to backline against your will" actually start meaning something at the table, not just on a card they haven't had reason to read closely yet.*

---

## What Players Learn

| Mechanic | How they learn |
|----------|-----------------|
| Rooted | PINCH clamps a target in place — the first time most new characters feel a Move Position option actually taken away from them |
| Forced repositioning | CARRION PULL drags a target to Backline against their will |
| Evade | Every Wrackclaw defensive card burrows into wet sand — a defense a brand-new party has to actually fail against before they trust it's real |
| Numbers over individual threat | Each hit is small; four of them landing in the same round is not |

---

## GM Notes

**They don't fight to the death and they don't flee at a threshold either** — a Wrackclaw that's taken real damage simply lets go and scuttles back into the wrack line on its own next turn, mid-fight, without needing an HP trigger. It isn't defeat. It's this specific piece of driftwood turning out not to be worth the effort.

**A parked Wrackclaw encounter is also the honest reason a party has nothing on them yet.** If a GM wants a reason the party's clothes are salt-stiff and their weapons already look older than they should, a swarm that's already had a go at anything loose in their packs before the party woke up is a clean, wordless answer — no dialogue needed, just a beach that's already been picked over once by the time anyone's conscious.

---

## Open — the 2026-09-21 review

**Measured and written down rather than acted on.** *Drew's call what changes; this section is the finding.*

**1. The numbers were wrong and are now three to four times worse.** Three of these against the three PCs kills somebody in **about one fight in five**, and four is a **coin flip**. The old figures (one knee in six, a death in twenty) came off `combat-simulations/encounter_budget.py`, which was building this creature's deck illegally — **none of five hundred builds satisfied the colour rule**, and the fourth slot the bestiary names as STRIKE was coming up Green about half the time. *Fixed the same day; the tool now fills by colour.* **Playing the party better does not help** — the good agent dies slightly more often, because three creatures focus-firing one character is not a thing tactics prevents.

**2. That contradicts this file's own fiction.** *"Losing a fight against Wrackclaws rarely means dying"* is written above, and the engine disagrees with it. **The fiction is the better of the two** and the cheapest fix is already in it: they are **collectors, not killers**. A Wrackclaw that has pinned something has got what it came for and stops attacking it — which would end the focus-fire on a Downed character, which is where every one of those deaths comes from.

**3. Every Defense Effect is Gain Evade.** Three signature cards, one defensive outcome, so the creature never makes a defensive decision. *The line above about every card burrowing into wet sand reads as flavour for a design that is not there.* **Evade also makes a poor first lesson**: a new player wins the exchange and is told it dodged anyway, from all three cards, with no way to read which is which.

**4. The card nobody designed outclasses the three that were.** STRIKE is Body + d10 with 3 unpreventable on defence. The signatures are d4 with a mean of 3.5 to 4.5 and no damaging defence at all, so **the core filler is the most dangerous quarter of this deck**. *Measured core dice for comparison: Red Melee runs d7.00, Blue Ranged d5.47, Green Melee d5.75.* Three d4s also means the Ranged restriction on SIDELONG SCUTTLE bought nothing.

**5. CARRION PULL points the wrong way at the dock, and this one is a live contradiction.** The card moves the target **to Backline**. The fiction is *drag it back to the water*. At the Vulture's Nest fight, **Frontline is the wet timber and Backline is the dry stone** (`places/vultures-nest.md`, The Opening Scene) — so the creature's signature grab shoves you **away from the water onto dry land and out of melee**. It worked on the original beach, where the geometry ran the other way. **It broke when the creature moved docks.** *Measured: 42% of PCs end that fight at Backline.*

**6. Rooted plus that shove can strand a new player.** The dock fight is the Range tutorial; PINCH takes position away and CARRION PULL puts you where your melee cards do not reach. *Both at once is a character with nothing to do, in the fight meant to teach what position is for.*

---

## Related Documents

- `quests/washed-ashore.md` — the campaign opening this creature belongs to
- `rules/card-glossary.md` — Rooted, Evade, forced repositioning
