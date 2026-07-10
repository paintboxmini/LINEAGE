# Card Compression Pass

Refactor a card set the way you'd refactor code: find the components that don't pull their weight, recombine the strong ones into fewer, denser cards, and lose no idea in the process. The goal is expressive **density** — power per card — not a smaller set for its own sake.

Division of labor with the simulator: the sim can prove two designs behaviorally *equivalent*; it can never pick between them — equivalence is where its authority ends and this pass's begins. When behavior ties, the simpler mechanic wins: the ideal card reaches its intended behavior with the least machinery. Card text is part of the design — complexity taxes the table (slower turns, misplays) even when it costs the engine nothing.

This pass is only possible because a card is separable (see `world/lineage.md` and the tag convention in `CLAUDE.md`): mechanic, name, flavor, and source are independent strands. Separable strands are what make recombination possible.

**When to run it:** on a set mature enough to have accumulated redundancy — the way you refactor after duplication accrues, not before. On a young set there is nothing to compress; running it early just homogenizes.

---

```
Treat each card as separable GENES, not an inseparable whole:

- Mechanic — what it does; the decision it creates.
- Name — individual authorship, a signature technique.
- Flavor — theme and voice.
- Source — tag / lineage; where the card was acquired.

Do NOT score cards holistically. Score COMPONENTS across the whole set.

1. Find the weakest genes, set-wide:
   - Mechanic: creates no decision another card doesn't already create, or
     wouldn't be missed in play.
   - Name: generic, forgettable, interchangeable with another card's.
   - Flavor: says nothing, or contradicts the mechanic.
   - Source: no tag where a lineage is identifiable, or a tag that isn't a real
     source (a theme masquerading as a tag — see world/lineage.md).

2. Propose recombinations: fold the STRONG genes of weak cards into surviving
   cards, producing FEWER, STRONGER cards.

3. Preserve every idea. A merge destroys a card BOUNDARY, not an idea — a strong
   mechanic, name, or flavor from a cut card must resurface in a survivor.
   Nothing is deleted; it is rehoused.

4. Report, per proposed merge: what was preserved, what redundancy was removed,
   and which gene of each parent survived where.

Constraints:
- Merge ONLY when it increases identity, thematic cohesion, or decision space.
  NEVER merge for mechanical similarity alone — that shrinks decision space,
  which is the opposite of the goal.
- Genes must RESONATE, not merely coexist. The best cards have mechanic, name,
  flavor, and source all saying the same thing (Loose Grip: "+2 / shift-immunity"
  IS "the wheel turns for those who stop fighting it" IS UNHELD). A strong-but-
  incoherent recombination is worse than the sum. Prefer genes that agree.
- Aim for DENSITY, not minimalism. You are evicting cards that don't pull their
  weight — not shrinking the set. If a merge loses a meaningful choice, it is a
  bad merge even if the count drops.
- Propose, do not apply. A merge ripples into decks, the simulator, and print
  sheets. Surface the recombinations; the designer rules.
- Rank proposals by confidence, and say when a card should be LEFT ALONE. A set
  with no worthwhile merges is a healthy set, not a failed pass.
```

---

## Relationship to the other tools

This is the constructive sibling of `red-team.md`. The red team uses the
Mechanical Relevance / Identity / Evolution lenses to *find flaws*; this pass uses
the same component judgments to *recombine strengths*. Run the red team to learn
which genes are weak; run this pass to decide what to do about it.

Every accepted merge is logged in `memory.md` (what absorbed what, which gene went
where) so a rehoused idea stays recoverable — a merge is a threshold crossing like
any other.

---

## What to check against

- Lineage / tag philosophy: `world/lineage.md`, `CLAUDE.md` (card format)
- Existing cards: `cards/`
- Keyword definitions: `rules/card-glossary.md`
- Whether a mechanic actually matters: `combatsimulations/`
