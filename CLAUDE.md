# LINEAGE — Tales Untold

A tabletop RPG: rules, cards, world, and the tooling that prints them. **Almost everything here is prose for a person to read at a table.** The Python in `printing/` and `combat-simulations/` reads that prose — the markdown is the source of truth, and code that disagrees with a rules file is the thing that's wrong.

Treat this as a design repo, not a software project. A "bug" here is usually two files asserting incompatible facts about the world.

---

## Who you are writing for

Drew runs this table and owns this repo. He asked for this section, in
these terms.

**Be as technical as you like about the game.** Mechanics, card
interactions, colour identity, what a keyword costs, how two cards chain —
that is his native language and the reason the repo exists. Don't soften
it and don't explain it back to him.

**Numbers land. The maths behind them does not.** Win rates, down rates,
"three points better across 400 fights", a spread between archetypes — give
him those, they are useful and he reads them well. What to leave out is the
derivation: the estimator, the shrinkage, the variance argument, why a
sweep was flat. If a number needs a caveat, say the caveat in a sentence.
His read on statistics is intuitive and good; it is the formal working that
goes hazy, so lead with what the number *means* for the game.

**Code and simulator vocabulary does not land, at all.** Function names,
file internals, class structure, the engine's own terms. Say what changed
about the game, not what changed about the code. *"The agent never moved,
so the simulator couldn't tell you whether a card about position was any
good"* is right. *"`choose_action` only moved on an empty reachable list"*
is not. He does not code, and has said so plainly — this is not a register
to dip in and out of.

**He is on a phone, and GitHub is unfamiliar ground.** Two consequences,
and the first one is the one that actually breaks things:

- **Never give a shell command as an instruction.** There is no terminal on
  a phone. `git tag`, `git push`, running a script — he cannot do any of
  it, and an instruction written that way is not a small inconvenience, it
  is impossible. Give taps on github.com in a browser: which page, which
  button, what to type in the box.
- **Don't assume a convention is obvious because it is standard.** Tags,
  branches, releases, pull requests, CI — he has said he is unaware of the
  normal conventions around these, and that is a statement about the
  conventions being arbitrary, not about him. Explain what a thing is for
  in one line before explaining what to do with it.

**If he says something went over his head, change register rather than add
detail.** More explanation in the same vocabulary is the wrong repair.

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

**Read the directory README first where one exists** — `agent-tools/`, `campaign/`, `combat-simulations/`, `factions-and-races/`, `flora/`, `printing/`, `cards/tiers/`. They carry the conventions for their folder and are kept current.

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
- **Deck size = Body + Mind + Soul**, for players and creatures alike. **Matching each colour's count to its stat is a heuristic, not a law** — it is how almost everything here is built, which makes it a fast way to write content, and it is not a constraint the game enforces (`rules/cards.md`, Paying for an off-ratio deck)
- **Hand size = Mind** (minimum 2)
- **The Oracle sets are 12/6/3 per colour** in that colour's range identity, and the expansion is 4/2/1. `oracle-1/2/3` are derived thirds, so changing the ratio breaks the even deal. New cards get written whenever they are wanted — what is fixed is the number of **seats**. Taking a seat in a printed set is a swap; writing a card is not. Cleared cards sit on the bench with no seat, and being unseated is not a verdict — `cards/tiers/beginner.md` holds the list and the count

When you change a card or a stat block, check what else consumes it: the seated sets in `printing/generate-cards.py`, any creature or character deck running that card, and the keyword counts in `rules/card-glossary.md`.

---

## Conventions worth knowing before you edit

- **`cards/*.md` is globbed non-recursively** by `combat-simulations/cards.py` (`os.listdir`) and by `printing/generate-cards.py`. Both parsers read every `.md` at the top of `cards/` as a deck, which is why `cards/tiers/` is a subdirectory — the files there are documentation
- **`printing/generate-all.sh` builds print artifacts and nothing else, deliberately.** Don't wire checks, linting, or anything else into it. **Its load-bearing half is the staleness diff, not the PDFs** — reasoning about which sheets should have moved after a rules edit has failed three times out of three, and rebuilding everything and diffing has caught it three out of three. That half needs no Chrome
- **Every printed artifact is build output, is not in git, and is generated in chat.** Drew has no terminal, so he asks and an agent builds the file from the markdown and hands it over. **There is no CI release path and no tagging — that existed until 2026-09-22 and was retired unused.** What the repo keeps is the *recipe*: the generators, the format conventions in `printing/README.md`, and **`printing/manifest.txt`** — one line per artifact with a hash, which is what the staleness diff runs against now that the HTML is untracked too (2026-09-25). *A one-off document built for somebody to read is output and goes to the person, never into the tree*
- **Every plant has a gate, and no gate is a stat check** (`flora/README.md`). A roll says whether a character is good at something; a gate says what kind of person or situation gets the thing at all
- **Tiers are about when, not about quality** (`cards/tiers/README.md`). A card that's too strong to start moves to the middle tier; it does not get rewritten until it's weak enough. That is how TURN lost its redirect for a year
- **A claim derived from another file carries a citation to it.** The value isn't for the reader — it's that writing the citation means opening the file, which is where the contradiction gets noticed (`agent-tools/README.md`)

---

## Checking work

```
python3 agent-tools/check-references.py          # names resolve; no duplicate card names
python3 agent-tools/check-geography.py           # directions agree with the Bearing Table
python3 agent-tools/check-card-drift.py          # a card drafted in campaign/ matches cards/
python3 agent-tools/list-open.py                 # every open question, in one place (inventory, exits 0)
python3 combat-simulations/cards.py              # card counts, as a load check
python3 combat-simulations/test_wheel.py         # initiative-shift worked cases
python3 combat-simulations/test_invariants.py   # rules/invariants.md, Confirmed
python3 combat-simulations/test_effects.py      # keyword rulings, through the cards
python3 combat-simulations/test_information.py  # no agent reads a hidden zone
python3 combat-simulations/test_agents.py       # invariants the agents have to keep
python3 combat-simulations/effects.py           # how much card text the engine runs
python3 combat-simulations/encounter_budget.py   # how many of a creature is a fight
```

**The three `check-*` scripts exit 1 on a finding. `agent-tools/list-open.py` never does** — it reads every `## Not Yet Set`, `## Open` and `## Open Hooks` section and prints them, keeping decisions-waiting apart from hooks-left-open-on-purpose. *An open question is not a fault.* None is wired into anything — run them by hand after touching names, geography, or a card that exists in both `campaign/` and `cards/`.

**Measure rather than recount.** Set ratios, range splits, mean die and keyword counts are all cheap to compute and expensive to get wrong from memory. For keyword counts specifically, diff against `git show HEAD:rules/card-glossary.md` rather than recounting from scratch — the glossary excludes negations ("cannot be Resisted" is not a Resist), so a naive grep over-counts.

**Before writing "the only card that…" into a file, check it.** That class of claim has been wrong more than once.
