# Red Team Prompt

Use this prompt to review cards, mechanics, encounters, or any game content before it goes to canon.

The mindset is not "find mistakes." It is: **attack invariants, find degenerate strategies, test architectural assumptions, and identify evolutionary novelty.** Early on this repo mostly needed wording and redundancy fixes; now the simulator is exposing rule architecture, timing policies, and emergent interactions, and the red team attacks those layers too.

---

```
Analyze the following content for Tales Untold.

Your job is not to "review everything." It is to ATTACK the content along the
axes below and report what survives. Assume the content is intentionally
minimal — do not add complexity unless it solves a demonstrated problem.

## Attack these layers

1. Engine-invariant violations — CHECK FIRST.
   - Does this introduce a hidden rule change or a new timing window?
   - Does it force the engine to special-case resolution?
   - Does it imply a new POLICY (card selection / reveal / initiative / RPS
     resolution), not merely a new card effect?
   If so, name the mechanic it overrides (`rules/invariants.md`, Mechanic-override
   reference) and say whether it should be expressed as a scoped modifier rather
   than a one-off exception. This pass is narrow — it's about the simulator's
   computational correctness, not whether the content is well-designed. That's
   the next pass.

1b. Design Principles fit.
   - Does the deck actually express the creature's behavior, or is it a generic
     stat-stick with flavor text on top?
   - Does the mechanic come from the creature's ecology/fiction, or was it picked
     first and the fiction painted on after?
   - Does the encounter teach through what the player does, or does it require
     the GM to explain the lesson?
   Check against `agent-tools/design-principles.md` directly — this is a design
   standard, not an engine check, and violating it doesn't break anything the
   simulator would catch.

2. Simulation abuse.
   - If the mechanic lives in `combatsimulations/` (or is a few lines from being
     testable there), run it and try to BREAK it: loops, degenerate lines, a
     dominant strategy, or play that becomes trivial/solved.
   - If it cannot be simulated, reason the degenerate lines by hand.
   - State which of the two you did — never imply a sim run that did not happen.

3. Mechanical relevance — does this matter? Would play notice if it were deleted?

4. Mechanical identity — does it create a decision NO other card creates, or is it
   a stat-swap of something that already exists?

5. Ambiguity — name the type:
   - Rules ambiguity: a case the mechanic genuinely does not define.
   - Natural-language ambiguity: wording that can be read two ways.

6. Evolution check (LINEAGE's own lens) — provenance, not play feel:
   - Which existing mechanic is this closest to?
   - What genuinely new design space does it open?
   - Is it a mutation or merely a duplicate?
   - Could the mutation be expressed more cleanly?

7. Tone & keyword compliance — fits the terse, mechanical voice; only approved
   keywords in use.

8. Visible reasoning — unfinished thinking left in the output (see the checklist
   below).

## Also surface one generative finding

Identify ONE interaction with existing mechanics the designer may not have
intended. It may be a bug to fix — or the most interesting thing here.

## Report

- Rank every finding: CRITICAL (breaks rules, engine, or balance) / MODERATE
  (matters in play) / COSMETIC (wording, polish). Spend effort accordingly — do
  not treat a comma like a timing bug.
- Provide a corrected version only for findings that need one. Fix what is
  necessary, nothing more.
- "Leave it alone" is a valid verdict. If a part is already right, or no
  improvement exists, say so and why — do not invent an edit to feel productive.
- A fix that moves the flagged problem to a different slot on the same content
  isn't a fix — check that the specific weakness named in the diagnosis is
  actually gone, not just relocated. (Duskwick's HALF-SEEN had Obscure cut from
  its Effect for being narrow and thematically mismatched, then the same
  Obscure reappeared on its Defensive Bonus, unchanged, because it was easier
  than replacing it. Still narrow, still mismatched, just moved.) If a
  mechanic was cut for a reason, don't re-add it elsewhere on the same content
  out of attachment to having used it first — verify the reason it was cut no
  longer applies before it comes back.

End on one line held throughout: assume the content is intentionally minimal; do
not add complexity unless it solves a demonstrated problem.
```

---

## Additional Pass: Quest / Encounter Review

If the content involves a quest, location, or narrative sequence, also evaluate:

```
1. Player Agency
   - Are there multiple ways players can approach this?
   - Is any outcome forced or overly linear?

2. Pressure & Tension
   - What pressures the player to act?
   - Is there a meaningful cost to delay, ignore, or rush?

3. Clarity Through Play
   - Are mechanics taught through interaction rather than explanation?
   - Would a player understand what matters by experiencing it?

4. Consequence
   - Do player choices create immediate or delayed consequences?
   - Are outcomes meaningfully different based on behavior?

5. Friction Points
   - Where might players get confused or stall?
   - Where might they disengage?

6. System Integration
   - Does this reinforce core systems (positioning, deck state, timing)?
   - Or does it feel disconnected from gameplay?

Steps:
- Identify at least 2 issues in the above areas
- Explain why they matter
- Suggest minimal fixes

Do not add new content unless necessary — refine what exists.
```

---

## Visible Reasoning — What to Look For

Unfinished reasoning leaves marks. Flag any of the following:

- **Mechanical scaffolding** — action lists, design intent notes, or structural placeholders that belong in a scratch file
- **Self-explaining content** — text that tells you what a mechanic is supposed to do instead of just doing it ("this passive is intended to teach X")
- **Designer hedging** — conditional language that reflects uncertainty rather than fiction ("this could also work as...")
- **Justification text** — narrative reasons for why a mechanic exists, written as if convincing someone rather than describing the world
- **Orphaned details** — specifics that were there to help the agent reason but serve no purpose in play

If removing flagged text breaks the content, the content isn't finished. Send it back.

---

## What to Check Against

- Keyword list: `experimental/README.md`
- Keyword definitions: `rules/card-glossary.md`
- Engine invariants (for the Engine-Invariant Violations pass): `rules/invariants.md`
- Design standards (for the Design Principles pass): `agent-tools/design-principles.md`
- Core resolution + timing: `rules/combat.md`, `rules/core-rules.md`
- Simulator (for Simulation Abuse): `combatsimulations/`
- Tone reference: `cards/alignment-marshal-engine.md`
- Existing cards for redundancy: `cards/red-body.md`, `cards/blue-mind.md`, `cards/green-soul.md`
