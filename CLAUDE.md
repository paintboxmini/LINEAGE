# LINEAGE — Tales Untold

A tabletop RPG: rules, cards, world, and the tooling that prints them. **Almost everything here is prose for a person to read at a table.** The Python in `printing/` and `combat-simulations/` reads that prose — the markdown is the source of truth, and code that disagrees with a rules file is the thing that's wrong.

Treat this as a design repo, not a software project. A "bug" here is usually two files asserting incompatible facts about the world.

---

## Where things are

| | |
|---|---|
| `rules/` | The game. `rules/cards.md` (colour and content rules), `rules/card-glossary.md` (canonical keyword rulings), plus `rules/combat.md`, `rules/character-creation.md`, `rules/resolution.md`, `rules/gm-guide.md` |
| `cards/` | One file per deck. `cards/red-body.md`, `cards/blue-mind.md` and `cards/green-soul.md` are the core pool; the rest are creature and character decks. `cards/tiers/` holds the eligibility lists |
| `bestiary/` `flora/` | Creatures and plants, one file each |
| `places/` `world/` `factions-and-races/` `quests/` `items/` | The setting |
| `characters/` | NPCs and written PCs |
| `campaign/` | **The table currently playing.** Player-owned material — see its README |
| `printing/` | Card and sheet generation. `printing/generate-cards.py` holds the seated set lists |
| `combat-simulations/` | The engine. Pure stdlib Python 3, no dependencies |
| `agent-tools/` | Consistency checks, run by hand |
| `experimental/` `archives/` | Unsettled lore; cut and superseded material |

**Read the directory README first where one exists** — `agent-tools/`, `campaign/`, `combat-simulations/`, `factions-and-races/`, `flora/`, `cards/tiers/`. They carry the conventions for their folder and are kept current.

---

## Not yours to write

- `factions-and-races/races-sirens.md` — **reserved, Ollie's.** Her working file is `experimental/ollies-island.md`
- `factions-and-races/races-fairies.md` — **reserved, Sophie's.** Nothing approved, the name included
- `campaign/` — each file belongs to the player it's about; they get the final say

Don't draft into a reserved slot, don't resolve a naming question that belongs to its owner, and don't move their material.

**Don't write ahead of player choice.** Sketch what a place or a person is; don't decide what the party will do there.

---

## Derived math

These are consequences, not settings. Change a stat and all of them move with it.

- **Max HP = (4 × Body) + Mind + Soul** (`rules/character-creation.md`)
- **Deck size = Body + Mind + Soul, and each colour's count equals its matching stat.** The same rule builds every creature in the world. A side effect worth knowing: revealing a creature's stats reveals its deck's exact colour composition
- **Hand size = Mind** (minimum 2)
- **The Oracle sets are 12/6/3 per colour** in that colour's range identity, and the expansion is 4/2/1. `oracle-1/2/3` are derived thirds, so changing the ratio breaks the even deal. New cards get written whenever they are wanted — what is fixed is the number of **seats**. Taking a seat in a printed set is a swap; writing a card is not. Forty-three cleared cards currently sit on the bench with no seat, and being unseated is not a verdict (`cards/tiers/beginner.md`)

When you change a card or a stat block, check what else consumes it: the seated sets in `printing/generate-cards.py`, any creature or character deck running that card, and the keyword counts in `rules/card-glossary.md`.

---

## Conventions worth knowing before you edit

- **`cards/*.md` is globbed non-recursively** by `combat-simulations/cards.py` (`os.listdir`) and by `printing/generate-cards.py`. Both parsers read every `.md` at the top of `cards/` as a deck, which is why `cards/tiers/` is a subdirectory — the files there are documentation
- **`printing/generate-all.sh` builds print artifacts and nothing else, deliberately.** Don't wire checks, linting, or anything else into it
- **Every plant has a gate, and no gate is a stat check** (`flora/README.md`). A roll says whether a character is good at something; a gate says what kind of person or situation gets the thing at all
- **Tiers are about when, not about quality** (`cards/tiers/README.md`). A card that's too strong to start moves to the middle tier; it does not get rewritten until it's weak enough. That is how TURN lost its redirect for a year
- **A claim derived from another file carries a citation to it.** The value isn't for the reader — it's that writing the citation means opening the file, which is where the contradiction gets noticed (`agent-tools/README.md`)

---

## Checking work

```
python3 agent-tools/check-references.py          # names resolve; no duplicate card names
python3 agent-tools/check-geography.py           # directions agree with the Bearing Table
python3 agent-tools/check-card-drift.py          # a card drafted in campaign/ matches cards/
python3 combat-simulations/cards.py              # card counts, as a load check
python3 combat-simulations/test_wheel.py         # initiative-shift worked cases
python3 combat-simulations/test_invariants.py   # rules/invariants.md, Confirmed
python3 combat-simulations/test_effects.py      # keyword rulings, through the cards
python3 combat-simulations/test_information.py  # no agent reads a hidden zone
python3 combat-simulations/effects.py           # how much card text the engine runs
python3 combat-simulations/encounter_budget.py   # how many of a creature is a fight
```

All three `agent-tools` scripts exit 1 on a finding. None is wired into anything — run them by hand after touching names, geography, or a card that exists in both `campaign/` and `cards/`.

**Measure rather than recount.** Set ratios, range splits, mean die and keyword counts are all cheap to compute and expensive to get wrong from memory. For keyword counts specifically, diff against `git show HEAD:rules/card-glossary.md` rather than recounting from scratch — the glossary excludes negations ("cannot be Resisted" is not a Resist), so a naive grep over-counts.

**Before writing "the only card that…" into a file, check it.** That class of claim has been wrong more than once.
