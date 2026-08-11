# Oracle Pool — Design Evolution

## What this trail preserves

This is the historical evolution of the Oracle pool: how a generic reward pool became a deliberately constrained starter-selection pool, how the pool's composition rules were discovered, and why the 2026-08-03 63-card composition was ultimately retired rather than treated as canon.

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

## Local corrections during construction

Several individual card decisions exposed useful rules about pool construction:

- GORE's range/condition interaction revealed that a conditional bonus can become unconditional when its condition is guaranteed by the card's own range. The card's correction changed the pool's Red Melee count, requiring a replacement.
- HEAVE AND HAUL was retained during coverage work because Green needed a Quick source, then rejected as too strong for a starter pool because it combined forced movement with team-wide free Quick. EDDY (later renamed SWAY) preserved the tactical niche at starter scale.
- REPEL was replaced by PUSH when it became clear that its two sides repeated the same unconditional all-enemies movement effect without differentiation.
- Wording errors such as "Target gains X" were corrected to identify the RPS opponent as the actual defender/attacker target; the simulator had already been resolving the intended relationship.

These were not isolated balance tweaks. They reinforced the same larger principle: **the Oracle pool should teach the system's vocabulary without introducing exceptional rules that obscure the vocabulary itself.**

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
- A generated composition can be valuable historical design work without becoming canon. Preserve the reasoning, then author the actual pool deliberately.
