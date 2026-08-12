# Combat Resolution & Status — Design Trail

This is a historical design trail for the evolution of Tales Untold's combat resolution and status architecture. It preserves the durable reasoning behind the current system without replacing the canonical rules in `rules/combat.md` or `rules/card-glossary.md`.

## The core combat problem

Combat was shaped around a deliberate goal: **the fight should be about reading the opponent, not merely applying the largest numbers.** The current rules describe the resulting combat as fast, positional, and decisive — "outread" rather than outlast.

That goal led to several systems being treated as parts of one resolution architecture rather than independent mechanics:

- RPS makes card choice a prediction.
- Position makes range a legality question before resolution.
- Initiative makes timing and sequencing a manipulable resource.
- Statuses create temporary advantages, constraints, and defenses that change what future reads mean.

A mechanic that bypasses these reads is therefore not merely strong or weak; it changes the kind of game combat is.

## RPS became prediction, not reaction

The attacker's card and defender's card are committed before either is revealed. The defender chooses from public information — previous colors, position, visible status, and other tells — rather than seeing the attack and selecting the direct counter.

This distinction became foundational. Defense is a **prediction**, not a reaction.

That is why simultaneous reveal matters, why illegal defense picks cannot simply be replaced after seeing the attacker's card, and why telegraphed effects are generally preferable to hidden ones. A visible threat gives the opponent a turn to read and answer it; concealment that exists only to surprise is less interesting than a bet the other player can actually contest.

The resolution triangle remains:

- Blue beats Red.
- Red beats Green.
- Green beats Blue.

A tie is not a generic failure state either: the current system allows the attacker's Effect and defender's Defensive Bonus to interact on a tie, unless the specific card says otherwise. That preserved card-level identity rather than forcing every tie into one universal outcome.

## Range became positional law

Combat abandoned measured distances in favor of Frontline / Backline. This was not only a simplification of presentation. It made **position a mechanical axis of the fight**.

Melee requires both combatants to be Frontline. Ranged works when the pair is not in Melee range. Both works in either case.

The same legality applies when defending. A card that cannot legally attack from the current positions cannot be used as a defense in those positions either.

This produced a useful consequence: holding the wrong cards can make a combatant functionally unable to defend even when cards remain in hand. Position therefore affects both offense and defense without granting automatic protection.

Movement costs the action, so changing position is itself part of the decision economy. Rushdown and Cover then became ways to manipulate that positional axis rather than generic movement abilities.

The quick-reference sheet is the canonical restatement of this law, kept deliberately terse so it reads as a lookup, not prose: **Melee — both must be Frontline. Ranged — works only while not in Melee range with the target.** Every downstream fix to a mismatched card (a Melee card whose own text checks a condition Melee's legality already guarantees, for instance) traces back to holding the sim and the card text to this exact pointer rather than to a looser paraphrase of it.

## Initiative became a continuous wheel

Turn order evolved from a list-like sequence into a **continuous wheel**. There are no rounds to reset it. Combatants occupy as many slots as there are combatants, and initiative shifts move tokens around that persistent structure.

This made timing a real resource. Effects can move a token, Wait can voluntarily trade an action for a later position, and joining or leaving combat changes the wheel itself.

The deeper design discovery was that initiative is not merely "who goes first." **The position in the wheel is part of the state of the fight.** This is why team sequencing, setup windows, and cards that manipulate initiative can become build-around mechanics.

The Initiative Wheel has its own consolidated historical trail and is preserved separately as the archive exemplar.

## Defense became an economy

Combat simulations repeatedly showed that **game length is a master balance variable**. Faster games convert raw stat advantages into wins more directly because there are fewer turns for reads, card advantage, defense, and positional decisions to matter. Longer games give the underdog more opportunities for those systems to operate.

This explained why several apparent balance fixes failed:

- Small individual card-die changes did little when they did not materially change game length.
- Larger damage dice made the underlying stat advantage worse by shortening fights.
- Removing dice reduced variance and harmed the underdog rather than solving the problem.
- More effective or available defense was identified as a cleaner possible lever because it can lengthen games without removing the d-scale damage identity.

The later team simulations added an important refinement: **hand size is defense capacity**. A larger Mind hand does not merely provide more choices; it gives a combatant more opportunities to hold an appropriate defensive card between turns. The team tests showed this effect strongly enough to validate keeping the Mind/hand-size relationship rather than treating it as a secondary convenience.

The durable lesson is not "always add defense." It is that combat balance has to account for the number of meaningful decisions a combatant gets to make before the fight ends.

## Status effects became a second resolution layer

Status mechanics expanded from isolated card effects into a structured vocabulary. The glossary became the canonical place for shared behavior, while individual cards state only what is specific to that card.

The major structural distinction is between **temporary charges** and **standing states**:

- Evade, Resist, Vulnerable, Deadly, Weak, Protect, Ward, and similar effects generally represent a future event they are waiting to answer. Their stacks are consumed one qualifying event at a time.
- Armour and Thorns are standing values. Their stacks combine into a persistent total rather than queueing as separate future charges.
- Anchored is sustained by maintaining position and therefore interacts directly with movement.
- Rooted blocks voluntary repositioning without preventing forced movement.
- Staggered is a one-instance interruption: it removes the next attack or defense that would occur, whichever comes first.

This distinction matters because **the shape of a status determines how it changes future decisions**. A one-use defense asks "when should this trigger?" A standing value asks "how does this change every subsequent exchange?" They should not be collapsed into one generic stacking rule merely for bookkeeping convenience.

## The card becomes the status token

A temporary status does not require a separate token system. The card itself can be placed face-up in front of the affected combatant and remains there until its effect resolves or expires.

That physical representation preserves a meaningful cost: the card is out of its owner's rotation while serving as the status. A buff or debuff therefore has both its fictional effect and an opportunity cost in the deck cycle.

This was an important consolidation of mechanics and table procedure: **the status's physical representation is part of its economy.**

## Attack damage acquired a fixed pipeline

Once multiple defensive effects existed, their order had to stop being ad hoc. Attack damage now follows a fixed pipeline:

**redirect → volunteer shield → Armour → Resist / Vulnerable → HP**

Unpreventable damage is outside that pipeline because the pipeline governs attack damage. Thorns, status damage, and HP costs therefore cannot accidentally inherit attack defenses merely because they happen to deal damage.

The broader lesson is that once a system has multiple defenses, **resolution order is itself a rule**. It must be explicit enough that adding another defensive effect does not require inventing a new ordering exception.

## Team play clarified color identity

Early 1v1 simulation created misleading conclusions about the three colors. Blue looked extremely strong because its control and large hand are excellent in a duel; Green looked weak because much of its support kit has no ally to support.

The team simulation changed the interpretation. Once Green's actual support kit and a support-aware policy were represented, Green became the team anchor. The resulting team archetypes reproduced the underlying card RPS at the deck level:

**Blue > Red > Green > Blue**

This was a major design finding because it established that color identity is **format-sensitive without being format-broken**:

- Red expresses reliable pressure and bruising.
- Blue expresses control and defensive card advantage.
- Green expresses support, sustain, and team anchoring.

A color should therefore not be buffed or nerfed from a single-format result when its intended identity is inherently relational.

## Death was implemented for real, then superseded by team targeting

For a long stretch of the sim's life, Death existed only in name. `death_floor()` — `-ceil(max_hp/2)`, the actual death threshold `rules/combat.md` describes — sat on `Combatant` but was never read anywhere; only Collapse was modeled. A second, related gap sat alongside it: `enemies()`/`allies()` exclude collapsed combatants from their pools entirely, and every targeting and support function reads from those pools — so a collapsed teammate wasn't a rare finishing-blow risk, they were **completely untargetable** until healed. That can't be right either: the rules say a Collapsed combatant is "automatically hit by any attack targeting you," which only means something if they can still be targeted.

The fix built `is_dead` onto `Combatant`, set only when a hit lands on an already-Collapsed target and drops them to or below `death_floor()` — the existing single-hit-floor rule already protects the hit that causes the *initial* collapse, so this can only trigger on a second hit. `heal()` refuses outright on a dead target. A separate `Battle.downed_enemies()` pool, kept apart from `enemies()` so ordinary targeting logic still never sees collapsed characters, fed a `_pick_target` roll (a flat 25% finishing-blow chance, flagged as tunable rather than derived) against downed targets before falling back to normal focus-fire.

That flat-chance model did not survive contact with Drew's actual mental model of team combat: *"a teams plan is to randomly select a target and pile on. drop the targeting when an enemy collapses and add them back into the pool of random targets."* The 25%-per-attack mechanic was replaced outright by a team-targeting rebuild — `Battle.team_target`, one shared lock per side rather than per attacker. `_pick_target` returns the team's current lock as long as it's standing; the moment it collapses, the lock clears and the next pick draws fresh and random from `Battle.targetable()` (living plus Collapsed-not-dead, replacing `downed_enemies()`). A downed combatant is simply back in the same pool, not hunted or spared specially. Death itself — `is_dead`, `death_floor()` — was not undone by this; only the targeting policy that decided how often a downed combatant got hit again changed underneath it.

## Exhaust disposal was never modeled in the sim

Noted plainly rather than left to be rediscovered by surprise: EXHAUST's disposal was never actually implemented in the sim — it is only flagged as `is_status`, with no seeding or removal logic behind it. A card-text rewrite of EXHAUST therefore carried zero sim regression risk, precisely because there was no simulated behavior to regress. The standing instruction for whenever Exhaust does get modeled: build the current single-path rule (an action removes all Exhaust from hand), not the three-path rule it replaced. This is an informational marker, not a deferred task with an owner — it exists so a future pass doesn't assume disposal logic is already there and go looking for a bug that is actually an absence.

## Typed modifiers with lifetimes — the architectural north star, Step 2

A brainstorm framed five effects — Predictable, Axiom's color-ban, Paradox's RPS inversion, Interrupt's cannot-defend, and Stagger — as one uniform category of "rule-benders" needing one uniform typed-modifier system. Checking each against the live code before designing anything found that framing wrong: "Predictable" does not exist in canon at all; `special_reveal` (PARADOX, AFTERIMAGE) and `wins_ties` (EQUAL FOOTING/ADAPT/CERTAINTY) are static fields declared on the `Card` class itself, not runtime state with a lifetime — there is nothing to type because they never expire, they are just permanent facts about what a card does. The scoped-down set that actually needed a typed-modifier system was `axiom_ban` / `cannot_defend` / `staggered` — genuine one-shot runtime state that fires once and expires. Presenting the narrowed scope to Drew before building, rather than quietly forcing all five examples into one system or quietly dropping the two that didn't fit, is what let his "go ahead" mean something real.

Two things surfaced only by reading the code closely rather than trusting the original note's shape:

- `staggered` turned out to have two independent consumption points — the defense-eligibility gate, and a separate check at the top of the staggered combatant's own turn — where the source note described a single flag with a single lifetime. `keyword_lab.py` also sets `staggered` via a bare `setattr()` that bypasses `apply_staggered()`/`debuff()` entirely, a real dependency invisible from `engine.py`/`team_engine.py` alone; a naive refactor removing the raw attribute would have broken that tool silently.
- `Combatant.ongoing` looked like existing infrastructure for the same problem — per-combatant, list-like, kind-tagged — and reusing existing infrastructure over inventing new structure is this repo's own standing preference. But `ongoing` is architecturally for *recurring* effects re-applied every turn while a position condition holds (healing ticks, stat buffs); `axiom_ban`/`cannot_defend`/`staggered` are one-shot blocks that never re-tick. Forcing them into `ongoing`'s shape would have added more special-case handling than the plain-dict alternative it was rejected in favor of — a real "checked, not assumed" negative result, not a shortcut skipped for convenience.

A genuine AXIOM bug (the ban never clears, in either engine) turned up as a side effect of reading the exact lines this refactor needed to touch. Confirmed with Drew before fixing: close the "never clears" half, which matches the card's own documented text and is provably safe via a scripted before/after test; leave the separate "never checked on the banned combatant's own attack" half alone as its own smaller, explicitly logged thread rather than folding it in because it was adjacent. Most of the refactor (the property-backed dict) is provably behavior-identical by construction — every old call site runs the same code path through a getter/setter instead of a bare attribute — so verification focused on the one line that changed real behavior, not the size of the diff.

This work was explicitly Step 2 of a larger architectural sequence; Step 3, the full policy-stack rewrite, stayed deferred rather than abandoned.

## AXIOM's attacker-side gap closed through a shared chokepoint

The Step 2 typed-modifier work left AXIOM's attacker-side gap open as its own small deferred decision. Closing it was framed to Drew as a real fork: a post-hoc voided reveal (matches the existing defense-side pattern, architecturally cheap, but diverges from the card's literal "cannot play that color" text) versus a true pre-selection filter (accurate to the text, but feared to require touching every policy brain — random/reader/greedy/tactician/punisher — across both engines, "closer to a Step 3 change than a Step 2 fix"). Drew picked the accurate option: a true pre-selection filter.

The fear behind that framing turned out to be wrong, and finding out why is the actual lesson. Every policy brain's `choose_action` already routes attack-card selection through exactly one shared function per engine — `legal_attacks()` (`policies.py`) and `legal_attacks_team()` (`team_policies.py`) — which in turn call `can_attack()`/`can_attack_t()` for range legality. A third site, DOUBLE DOWN's bonus attack in `content.py`, independently reimplements the same selection shape but still calls `can_attack()` directly. All three sites already funneled through one true chokepoint per engine, so the ban only needed to land there once rather than being threaded through five separate policy brains. Assuming an architecture change requires touching every call site, without first checking whether those call sites already share a function, was the actual scoping error in the original question to Drew.

Extending `can_attack()` — nominally a range-legality function — to also cover the axiom ban is a real, if small, scope widen, named rather than slid in quietly. The alternative (checking the ban separately inside each of the three call sites) would have meant writing the same two-line check three times instead of once, purely to keep the function's name matching its historical scope exactly. Verification checked what "cannot play" actually means, not just what a single `can_attack` call returns: confirmed `legal_attacks()` genuinely excludes the banned-color card from the returned list, confirmed a combatant holding only banned-color cards falls through to move/idle like any other total legality lockout, confirmed the mirrored team-side filter behaves identically, and confirmed — via a forced-through `attack()` call bypassing selection entirely — that the ban still clears on reveal even if some future caller skipped the selection-time filter.

## What the combat architecture ultimately protects

The historical arc points to a coherent priority order:

1. **The player should have something meaningful to read.**
2. **Position and timing should change what choices are legal or valuable.**
3. **Defense should create decisions, not merely erase damage.**
4. **Statuses should alter future exchanges in legible, mechanically distinct ways.**
5. **Resolution order should be explicit enough that the system remains composable.**
6. **Balance should be judged across the format the mechanic is actually designed for.**

The current combat rules are the authority. This trail preserves why those rules accumulated the shape they have.

## Provenance

The principal historical material is the archived combat work and simulation findings in `archives/key-design-decisions.md`, the retired worked combat example preserved at `archives/combat-example-2026-08-06.md`, and the current canonical implementations in `rules/combat.md` and `rules/card-glossary.md`.
