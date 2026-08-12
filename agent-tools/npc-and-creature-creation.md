# NPC and Creature Creation

Operational tool for creating **NPCs and creatures** in the LINEAGE setting.

> **This tool is for non-player entities. It is not a player-character creation guide.**

Use it when creating or revising an NPC or creature in `characters/` or `bestiary/`. It covers the entity as a whole; the stat block is one component of that entity.

## 1. Start With the Entity

Before filling numbers, establish what the entity is and what it does in the world.

Ask:

- What is this being's identity, role, or function?
- What makes it distinct from another entity of the same broad type?
- What does it want, protect, avoid, or pursue?
- How does it behave when no one is fighting it?
- What should players be able to notice, infer, or learn about it?

Do not invent details merely to make the entry feel complete. Leave genuinely unspecified details unspecified.

## 2. Build the Stat Block

Use the established mechanical structure appropriate to the entity:

```text
Mind X / Body X / Soul X — HP X
Creature Threat Rating: X

Deck (X — X Blue / X Red / X Green): [cards]
```

Use the canonical rules for the actual formulas and meanings of these values. Do not redefine them here.

### Stats

Choose Mind, Body, and Soul to express the entity's actual capabilities and combat identity. Do not treat them as arbitrary difficulty knobs.

### HP

Use the current canonical HP relationship to Body. If scaling an existing entity, remember that changing a stat changes its current derived values; do not treat derived values as independent knobs.

### Creature Threat Rating

Use the current canonical CTR calculation and established balance guidance. If the entity is intentionally exceptional, preserve the reason in its design rather than silently altering the meaning of CTR.

### Deck

Build the deck from the entity's actual combat identity.

- Prefer existing canonical cards when they express the intended behavior.
- Use signature cards when the entity needs a capability that belongs specifically to it.
- Keep the deck's color distribution coherent with its stats and identity.
- Do not invent new cards inside the stat block; create them through the card-creation process.

## 3. Give the Entity a Full Identity

A stat block alone is not a finished NPC or creature.

Use the sections appropriate to the entity:

### Description / Appearance

Give players a concrete way to perceive the entity. Use distinctive details rather than generic category description.

### Behavior

Describe what it does, wants, avoids, and how it normally acts. Behavior should remain meaningful outside combat.

### Combat Identity

Describe the kind of fight the entity creates. What does it reward? What does it punish? What does it try to make the players understand?

### Encounter Behavior

For creatures and enemies, explain how the entity actually uses space, positioning, cards, terrain, and its instincts during an encounter.

### The Tell

Give players observable information that can let them understand or anticipate danger. A tell should support discovery and informed decisions rather than function as a hidden stat check with no visible basis.

Use only the sections that fit the entity. Do not force every NPC or creature into an identical template.

## 4. Scale Existing Entities Carefully

When creating a stronger or weaker version of an existing NPC or creature:

- Preserve the identity unless the fiction establishes a meaningful change.
- Adjust stats and derived values through the canonical relationships.
- Adjust the deck when the entity's capabilities genuinely change.
- Do not add new abilities merely because the numbers increased.
- If a variant is a distinct encounter, say what makes it distinct.

Scaling should preserve the thing while changing its magnitude or circumstance unless the fiction calls for transformation.

## 5. Canon Checks

Before finalizing:

- Check the current rules for stats, HP, CTR, cards, and combat mechanics.
- Check nearby `characters/` and `bestiary/` entries for established structure and terminology.
- Check the relevant world and place files for lore that constrains the entity.
- Check every referenced card against its canonical card file.
- Do not silently redefine an established mechanic or canon fact.

If the requested entity conflicts with current canon, surface the conflict rather than resolving it invisibly.

## 6. Creation Test

A finished NPC or creature should make four things agree:

**Identity — Behavior — Mechanics — Fictional Context**

The mechanics should express what the entity is. The behavior should make those mechanics intelligible in play. The fictional context should explain why this particular entity has these capabilities.

If the numbers, behavior, and fiction describe different beings, the entity is not finished.

## 7. Final Review

Before presenting the entity as finished, ask:

1. Is this clearly an NPC or creature rather than a player-character build?
2. Does it have a distinct identity and function?
3. Do Mind, Body, and Soul express that identity?
4. Are HP and CTR derived from the current canonical rules?
5. Does the deck express the intended combat identity?
6. Are signature cards actually specific to the entity?
7. Can players understand its behavior through observation and play?
8. Does it have meaningful tells where appropriate?
9. Does the entity fit its established world context?
10. Did anything get invented merely to fill a template?

If the entity is mechanically ready but the fiction is thin, do not call it finished. If the fiction is strong but the mechanics contradict it, fix the contradiction before finalizing.
