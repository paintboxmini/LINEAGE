# Card Creation

Operational tool for creating or editing cards in `cards/`.

Use this tool for **authoring a card**. It does not replace canon. Check the canonical files named below whenever a rule, keyword, lineage question, or existing card creates uncertainty.

## 1. Start With the Decision

Before writing the card, identify the decision or behavior the card is meant to create.

Ask:

- What does playing this card ask the player to choose, risk, notice, or exploit?
- What situation makes the card worth choosing?
- What would be meaningfully different in play if this card did not exist?

Do not begin by filling the template mechanically. The mechanic comes first; the format serves it.

## 2. Choose the Card's Mechanical Identity

Use the established color/stat relationship:

- **RED — Body**
- **BLUE — Mind**
- **GREEN — Soul**

Choose the color and stat that express the card's actual function rather than choosing a color for aesthetics.

When a card changes a stat, interacts with a keyword, or depends on a system rule, verify the current ruling in the canonical rules before writing the text.

## 3. Write the Card

Use the established card structure:

```text
CARD NAME
COLOR — STAT

Attack: [stat + die or other canonical attack form]
Effect: [what happens]
Defensive Bonus: [what happens defensively, if any]
Range: [Ranged / Melee / Both]

"[flavor]"
```

Include only the fields the card actually uses. If a card requires a Special Rule or another established field, follow the canonical card examples and rules rather than inventing a new format.

### Name

The name should give the card individual identity. It can carry authorship, signature technique, metaphor, or voice that the mechanic alone cannot.

Do not use the name to smuggle a mechanical rule that the text does not establish.

### Mechanic

Write the smallest clear expression of the intended behavior.

**Plain mechanical text is a first-class option, not a failure to find the right keyword.** Much of the existing set already works this way — CALCULATE's *"Move target enemy to backline,"* STUDY's *"Discard 2, draw 2,"* the Root Heart's FOREST MEMORY naming a color and paying out if the target plays it — sitting alongside cards that use Deadly, Sealed, or Scry. Reach for a keyword when one *exactly* expresses the rule. Write it out plainly when none does.

Do not create a new keyword merely to make one card's wording shorter. Do not duplicate a keyword's definition on the card unless the canonical format specifically requires it.

**Compression — how keywords are actually earned.** A keyword's job is to compress something the game already keeps saying. When the same mechanic has been written out longhand across enough cards, that repetition is the qualification: it has become vocabulary, and folding it into `rules/card-glossary.md` is bookkeeping catching up to practice rather than an invention. **Flag the candidate; do not mint it mid-card** (`CLAUDE.md`, Do Not — *"flag if something is genuinely new"*). How many repeats earn it isn't set — that's a judgment call surfaced for Drew, not a bar an agent clears on its own.

Frequency isn't the only justification. `rules/card-glossary.md` carries keywords used by a single card — Obscure, Critical — because the rule itself is intricate enough that restating it in full every time would cost more than a defined term does. Compression answers repetition; a defined term can also answer complexity.

### Defensive Bonus

Treat the Defensive Bonus as part of the card's identity, not as free extra text. It should create a meaningful defensive choice or reinforce the card's intended function.

If there is no worthwhile defensive behavior, leave it absent rather than adding one for symmetry.

### Range

Use only the established range vocabulary:

- **Ranged**
- **Melee**
- **Both**

Do not invent new range categories.

### Flavor

Flavor should reinforce the card's identity and relationship to its mechanic. It should not contradict the mechanic or carry an unstated rule.

## 4. Source and Lineage

A card's tag records the **most specific source players can still meaningfully identify**. A living location tradition can be a tag; an individual master's technique belongs in the card's name, not as a new tag.

Do not invent a tag merely because a card has a theme.

Before assigning or changing a tag, check `world/lineage.md`.

## 5. Canon Checks

Before finalizing a card:

- Check `rules/card-glossary.md` for every keyword used.
- Check relevant rules files for mechanics the card touches.
- Check `world/lineage.md` for source/tag questions.
- Inspect nearby cards in `cards/` for established wording and formatting.
- Check whether the proposed effect duplicates an existing card without creating a meaningful new decision.
- If the card writes a mechanic out longhand, check whether other cards already say the same thing. A repeat isn't a problem — it's a compression candidate worth flagging (see Mechanic, above).

If current canon and the requested card conflict, do not silently redefine canon. Surface the conflict.

### Convergence Check

Find the cards already doing something mechanically similar — not the same card, the same *move* — and compare how they say it. Then run the test:

**Would rewriting this card to follow the established convention change what it does, or how its behavior reads at the table?**

"Fundamentally" can't carry that question by itself, so check it against something concrete. A difference is load-bearing if aligning would change:

- the decision the card exists to create (Step 1)
- when, or whether, the effect triggers
- what it interacts with — keywords, positions, other cards in the same deck
- whether the four strands still agree (Step 6)

If none of those move, the difference is wording, not design.

- **Clearly nothing moves** — align it. Match the established expression. A near-variant that behaves identically but phrases itself differently is drift: the rule gets harder to learn, and every extra wording of one mechanic raises the cost of ever compressing it into a keyword later (see Mechanic, above).
- **Clearly something moves** — keep the divergence, and say plainly what it buys. That difference *is* the card's design, and it should survive review on those terms.
- **Close call** — **flag it; do not resolve it inside a rewrite.** Present both versions and what each costs, and let Drew choose. If you find yourself assembling an argument for why the two are "basically the same," that effort is the signal: this is a design decision, not a formatting one. Same escalation as compression, for the same reason (`CLAUDE.md`, Canon Gate — surface genuine design forks rather than choosing invisibly).

The default is convergence. Divergence has to earn itself — but it earns it in the open, not quietly inside an agent's rewrite.

## 6. Creation Test

A finished card should have four strands that agree:

**Mechanic — Name — Flavor — Source**

The mechanic creates the decision. The name gives it individual identity. The flavor gives it voice and theme. The source establishes where the knowledge comes from.

They do not need to say the same thing literally, but they should feel like expressions of the same card.

If the strands fight each other, revise rather than sanding the conflict over with prose.

## 7. Final Review

Before presenting the card as finished, ask:

1. Does it create a meaningful decision?
2. Is its color/stat relationship appropriate?
3. Does every keyword use canonical meaning?
4. Is the wording as simple as the intended behavior allows?
5. Does the defensive side matter?
6. Is the range correct?
7. Does the name add identity rather than merely restating the effect?
8. Does the flavor reinforce rather than contradict the card?
9. Is the source tag real and appropriately specific?
10. Does the card belong in the existing set, rather than merely resembling something already there?
11. If it states a mechanic in longhand, has the set now written that same mechanic out often enough to flag for compression into a keyword?
12. Is it a near-variant of how an existing card already expresses the same move — and has that been aligned, justified, or flagged for Drew, rather than settled quietly?

For adversarial review, run `agent-tools/red-team.md` after creation.
