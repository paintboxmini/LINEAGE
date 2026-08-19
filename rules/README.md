# Rules — Jurisdiction

**One fact, one owner.** This file records which rules file owns which topic. Confirmed by Drew, 2026-08-18.

`rules/` carries three parallel voices — the detailed canon, `core-rules.md`'s quick reference, and `player-guide.md`'s printed player prose. That is deliberate: a printed player guide that only points at other files is not a player guide. What is *not* deliberate is a second **source**. A voice restates; it does not decide.

So the rule is not "no duplication." It is: **duplication is allowed as a second voice, never as a second source.** Where two files state the same mechanical value, `verify.py`'s `check_restatements` fails if they ever disagree — 11 facts, including the HP formula's own check.

---

## Owners

| File | Owns |
|------|------|
| `combat.md` | Everything that happens in a fight — attack resolution, turn structure, initiative, positioning, ongoing effects, Collapse |
| `core-rules.md` | Formulas and tables — the HP formula, the stat table, Difficulty Classes, the Range Matrix |
| `cards.md` | What a card is and how to read it — anatomy, Attacker/Defender vs. Target, deck building |
| `out-of-combat.md` | Checks, saves, Advantage, and Perception outside a fight |
| `character-creation.md` | Making a character and advancing one — stats, starting deck, hand size, resting, the Oracle |
| `equipment.md` | Gear and the gear economy — tiers, currency, pricing, pacing |
| `card-glossary.md` | Keyword and status-card definitions. **Generated** from `keywords/`, `status-cards/` and `glossary-frame.md` — edit those |
| `items.md` | The item catalog, indexed by source |
| `people.md`, `places.md` | The three Cuts applied to a person and to a place |
| `river-fishing.md` | The Pull — a real-time table minigame |
| `initiative-shift-examples.md` | Worked cases for Initiative Shift X |

## Voices

| File | Restates |
|------|----------|
| `player-guide.md` | Everything a player needs, in player prose. The printed artifact, with `the-summons.md` |
| `gm-guide.md` | Everything a GM needs, in GM prose |
| `the-summons.md` | The Oracle's summons — fiction, not rules. Printed |

A voice may restate any owner's rule. It may not introduce one. If a voice says something no owner does, that is the defect — either the owner is missing it, or the voice invented it.

---

## What this does not yet cover

`check_restatements` compares facts with an extractable value. The **prose** overlaps are unguarded: Stealth & Ambush, Chase, Cover, Positioning, Turn Structure, Ongoing Effects, Advancement, Resting and Equipment are each stated two or three times in different words, and nothing compares them. Short-rest chaining is the clearest gap — `character-creation.md` says three back-to-back, `core-rules.md` says only that they chain. Neither is wrong; that is exactly where a contradiction would hide.

## Related Documents

- `agent-tools/verify.py` — `check_restatements`, `check_hp_formula`, `check_glossary_generated`
- `agent-tools/invariants.md` — the index of what is enforced and what is not
