# Heuristics

Operational principles about *how the work gets done* — not truths about the fictional world (that's Invariants), not vocabulary (that's Rule Definitions), not concrete demonstrations (that's Exemplars). See `rules/invariants.md`'s header for how these four layers relate and why they're kept apart.

A heuristic tells an agent or a future session *when to act*, not *what is true*. Add to this list whenever a repeated pattern in how we work gets named — don't let it stay implicit in a paragraph somewhere it'll get lost.

---

- **Promote repeated retrieval.** If an agent repeatedly retrieves the same examples to rediscover a pattern, that pattern has earned a permanent home — promote it into `agent-tools/exemplars.md` (or wherever its layer lives) rather than re-deriving it from scratch next time.

- **Promote a rule-bender's architecture only when the current one hurts.** Today every rule-bender (Axiom, Paradox, Interrupt, Stagger, Intercept...) is a per-combatant flag read inline at one pipeline step — cheap, and sufficient so far. The agreed escalation path (`memory.md`, architecture north star) is flags → typed modifiers with lifetimes → a policy stack. Move up a level only when adding the *next* bender as a flag has become genuinely painful — not preemptively. A rule-bender that can't be expressed as (1) name the invariant it changes, (2) set a flag with a clear expiry, (3) read that flag at exactly one pipeline step, (4) revert on expiry, is the concrete signal that the next architecture level is due — raise it before shipping, don't route around it.

- **A cheap experiment that gets overridden the same day is not a failure — it's the gate working.** The tier→authority-level rename, and the six-hour difficulty-tier recalibration that Strength immediately superseded, both cost almost nothing and both surfaced the right answer faster than deliberating up front would have. Prefer shipping a fast, reversible attempt over holding a decision open.

- **Mark inferred connections, don't assert them.** When a new piece of content resonates with something already established (a location's open mystery, a faction's stated purpose) but the connection wasn't stated outright, write it as a flagged, optional GM thread — not as fact. Recent instances: the Turnroot-thorns/Mason-perimeter tension in the Skeinwing's file; the ruins/fence connection before Drew confirmed it. The cost of a wrongly-asserted connection is much higher than the cost of a clearly-labeled maybe.

- **When an aside contradicts the canon it's illustrating, flag it — don't quietly harmonize.** If a worked example, a recalled definition, or a design aside doesn't match what's actually written elsewhere, that's a signal worth surfacing before building on it, even mid-conversation. Silently picking the "probably intended" version is a silent redefinition wearing a helpful face.
