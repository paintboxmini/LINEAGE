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

Prefer existing canonical keywords when they exactly express the intended rule. Do not create a new keyword merely to make one card's wording shorter.

Do not duplicate a keyword's definition on the card unless the canonical format specifically requires it.

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

If current canon and the requested card conflict, do not silently redefine canon. Surface the conflict.

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

For adversarial review, run `agent-tools/red-team.md` after creation. For mature sets where redundancy has accumulated, `agent-tools/card-compression.md` is the appropriate later pass — not a substitute for creating the card correctly in the first place.
