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
