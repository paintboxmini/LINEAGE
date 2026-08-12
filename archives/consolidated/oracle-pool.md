# Oracle Pool — Design Evolution

## What this trail preserves

This is the historical evolution of the Oracle pool: how a generic reward pool became a deliberately constrained starter-selection pool, how the pool's composition rules were discovered, how a bug in one of its pinned cards got fixed without breaking the composition, and why the 2026-08-03 63-card composition was ultimately retired rather than treated as canon.

The current Oracle mechanic is authoritative elsewhere. This file preserves the reasoning trail, not the current card list.

## Starting shape

The Oracle is a living reward pool. The pool is shared rather than owned by an individual character: after an encounter/session, the GM can add eligible cards, and character advancement draws a small selection from the pool rather than granting a fixed reward. The intended experience is that advancement is partly discovery and choice.

The initial populated pool was AI-selected from the core card sets. That composition proved useful as design material but was never the final authored pool.

## First constraint: starter-level eligibility

The first major pass established that the Oracle is not simply "good cards from the core sets." It needs to introduce the system gradually.

Starter candidates were screened for cards that:

- touch one of the three core combat pillars — RPS, Initiative, or Position — or use a standard keyword;
- avoid forcing the opponent to discard;
- avoid injecting Wound or Exhaust;
- avoid requiring systems the pool has not otherwise introduced, such as Anchored interactions;
- avoid RPS auto-win/reversal effects;
- avoid preconditions that depend on another card or turn establishing a state;
- avoid open-ended amount selection that asks the starter pool to introduce a new decision structure.

This established the important distinction between **a card being legal in the game** and **a card being appropriate for the Oracle's introductory reward pool**.

## Second constraint: coverage, not just power

The first coverage passes revealed that a good pool also needs breadth. A color should not enter the game with entire keyword families or important tactical functions absent simply because the individually strongest cards happened to cluster elsewhere.

The pool was therefore checked for keyword coverage within each color. Cards were added to close genuine gaps, then the pool was slimmed back down while preserving the newly established coverage.

This produced a useful design lesson: **starter-pool construction is a constrained coverage problem, not merely a ranking exercise.** Redundancy matters, but so does ensuring that each color can demonstrate the vocabulary and tactical identity the broader system expects players to discover.

## Range identity becomes a hard structural constraint

The next refinement made range distribution part of the pool's identity rather than an incidental consequence of selection.

Drew fixed the final composition target on 2026-08-03:

- **21 cards per color**
- each color split **12 / 6 / 3** across its three ranges
- the dominant range follows that color's established identity:
  - Red: **12 Melee / 6 Both / 3 Ranged**
  - Blue: **12 Ranged / 6 Melee / 3 Both**
  - Green: **12 Both / 6 Ranged / 3 Melee**

These are exact cells, not a preference. Once the target was established, every addition or cut had to preserve the full nine-cell composition.

This changed the nature of pool construction again: a card could be individually suitable and still be the wrong choice because the composition could no longer satisfy the range matrix.

## The 63-card composition

The 2026-08-03 pass expanded the pool from 60 to 63 because the fixed 12/6/3 matrix could not be filled from the existing core candidates while maintaining the starter eligibility bar.

Seven new cards were created because two range/color slices lacked enough eligible candidates:

- Blue Melee needed six cards while only three existing candidates cleared the bar, leading to HESITATE, TELL, and SECOND GUESS.
- Green Both needed twelve and likewise ran out of eligible candidates, leading to SETTLE, GIVE WAY, BRAMBLE, and QUICKEN.

Several cuts were driven explicitly by the eligibility bar rather than by raw strength. EQUAL FOOTING, CERTAINTY, and ADAPT were excluded because their "Wins ties" effect introduced an RPS auto-win. RETALIATE and REBUTTAL depended on another turn establishing a condition. INTERRUPT introduced turn denial, TRAMPLE granted an extra action, and GAMBLER'S RUIN introduced exploding dice.

Previously cut cards could return when the fixed composition demanded them. That was not treated as a reversal of their earlier evaluation: the composition constraint had changed what problem they were solving.

## GORE, the pinned slot, and a condition that was never real

The same day the 12/6/3 composition target was fixed, Drew asked how GORE actually worked — and the honest answer was that it didn't, quite. GORE's Effect read *"If target is Frontline, deal +d6 additional damage,"* printed on a card whose own Range was Melee — and Melee is legal only when both combatants are already Frontline. GORE could never legally be played against a target that wasn't Frontline, so the "if" could never resolve false. The simulator's own damage function implemented this literally: a branch that always fired whenever the function ran at all.

The same diagnosis turned up on `cards/vescal.md`'s CENSER SWING (Range Melee, *"If target is Frontline, deal +2 damage"*) — a twin, not a one-off, reported alongside GORE's own fix and corrected the same way, at a proportionally smaller die cut (a flat +2 kicker, not a d6 one, so the compensating cut stopped one die step short of GORE's).

Drew's fix made the sentence true instead of rewriting it: **Range Melee → Both, base die d8 → d4.** Moving to Both is what turns "if target is Frontline" back into a real, sometimes-false condition — the target can now legitimately be Backline when GORE is played. The die drop is what pays for that: a guaranteed d8 became a floor of d4 with a genuine, not guaranteed, d6 kicker on top.

The fix collided immediately with the pool's own pinned composition. GORE was one of the Oracle's fixed **Red Melee-12**, set the same day. Moving it to Both would have silently dropped Red to 11/7/3. **INTERCEPT** was swapped into the vacated slot — a plain "Gain Protect and Resist 2" grant, the same shape as GUARD and PAIN IS FUEL already in the pool, and notably a card that had been cut from this exact pool on 2026-08-01 for redundancy at a 20-card size. GORE's departure reopened exactly the slot INTERCEPT had been trimmed from — a closed loop, not a coincidence chased for its own sake.

Measured, not just reasoned through: a levelled duel series (GORE plus generic filler vs. a mirrored control, 20,000 paired seeds) showed the fixed version (d4/Both) at 34.2% against the as-printed version (d8/Melee) at 33.0% — a small **+1.2 point** net gain, meaning Both's added flexibility outweighs the smaller guaranteed floor at this stat level. Reported, not acted on further; Drew had already set both numbers deliberately in the same instruction that ordered the fix.

This became the template for two more range-condition collisions the same session (STILLNESS, then CHARGE) — by the third occurrence, with the pool already frozen pending Drew's own hand-build (see below), the right call was to do nothing about the composition and flag the collision rather than force another swap into a file that was about to be emptied anyway.

## "Delete the Oracle folder" — the instruction that got a pause instead of a keystroke

Drew's actual words the next day were blunt: *"Delete the Oracle folder and its contents entirely."* Taken literally, that would have removed a directory `CLAUDE.md`'s own canonical structure table describes as *"the shared starter pool players draft from at character creation and draw from at end of session,"* referenced from `README.md`, `memory.md`, the combat simulator, and the print pipeline — and would have discarded, with zero stated reason, a composition that had just received a fixed 12/6/3 target, seven newly-written cards, and a bug-driven card swap (GORE → INTERCEPT, above), all in that same session. Documented shared infrastructure, wide reference fan-out, hours of very recent deliberate work, no reason given: exactly the shape of request this repo's own safety posture says to confirm rather than execute silently.

The question came back with three concrete options rather than a bare "are you sure," so the answer could be specific instead of a yes/no: cut the mechanic entirely with full cleanup, delete just the file and leave the code dangling, or something narrower. Drew's actual answer matched none of the three exactly: *"the mechanics are staying but the folder needs to be at least emptied. I'm going to build it by hand from the coreset right before session 1."* The mechanic — the rule, the eligibility criteria, the 12/6/3 target — stays. Only the specific 63-card selection goes, because Drew wants to make that selection himself rather than use the AI-drafted one.

The 63-card build was archived rather than deleted, unprompted — house convention (superseded material moves to `archives/`, "untouched, not deleted"), not a new call. It represented real, reusable design reasoning — which keywords were at zero and got covered, why certain cards were too strong for a starter pool, the eligibility bar that eliminated three "Wins ties" cards as a set — that Drew might want to reference later even though he wasn't using the selection as-is.

A gap was left deliberately, and named as a judgment call rather than buried for a future reader to discover: the combat simulator's `ORACLE_DECK` and the print pipeline's oracle card list are hand-maintained duplicates of what used to be in the markdown file, never generated from it — emptying the markdown broke nothing mechanically; the simulator and print pipeline kept running exactly as before. But that also means canon (the now-empty `Oracle/baseoracledeck.md`) and code disagreed about what the Oracle pool contained, and would keep disagreeing until Drew's hand-built version replaced both. Left alone on the reasoning that nobody asked for the code changed and touching working simulator/print logic uninstructed is a real risk for zero requested benefit.

## Why the 63-card list was retired

The 63-card composition was a completed selection exercise, not the final authored Oracle.

On 2026-08-04, Drew removed the populated list from `Oracle/baseoracledeck.md` and chose to hand-build the actual campaign pool from the core sets immediately before Session 1. The mechanic remained; the AI-selected composition did not.

That decision matters because it separates two things that had become conflated:

1. **The Oracle's design constraints** — shared reward pool, eligibility, range composition, and the lessons learned from constructing the first pool.
2. **One particular generated pool** — useful evidence and candidate material, but not authoritative content.

The 63-card list therefore remains preserved as historical groundwork rather than being treated as a hidden canon deck.

## Durable design lessons

- The Oracle pool is a **curated introduction to the system**, not a generic pile of rewards.
- Eligibility should prevent the starter pool from requiring unexplained subsystems or exceptional rules.
- Coverage matters: the pool should expose the meaningful vocabulary of each color rather than accidentally hiding entire mechanics.
- Range composition can be an explicit expression of color identity rather than an emergent statistical result.
- Hard composition constraints can legitimately cause previously rejected cards to return and previously acceptable cards to leave; the constraint changes the role the candidate must fill.
- A card's own printed condition can be structurally vacuous — always true by construction, not by intent — and the fix is to change the field that made it vacuous (Range) rather than the sentence.
- A card fix that touches a pool's pinned composition needs its own resolution, not a silent gap; swapping in a card the same pool cut for redundancy earlier closes the loop cleanly.
- A generated composition can be valuable historical design work without becoming canon. Preserve the reasoning, then author the actual pool deliberately.
- A literal, sweeping instruction against documented shared infrastructure and recent deliberate work is exactly the shape of request to confirm with concrete options rather than execute silently — the actual answer narrowed the blast radius from "delete the mechanic" to "empty one file."
