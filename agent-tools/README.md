# agent-tools

Consistency checks for the repo's own content. Run by hand, one job each.

**None of them is wired into `printing/generate-all.sh`.** That script rebuilds print artifacts and nothing else, deliberately.

| | |
|---|---|
| `check-references.py` | Every **name** resolves — document paths, section citations, decklist card names, and no duplicate card names |
| `check-geography.py` | Every directional **claim** agrees with the map in `world/geography-overview.md`, Bearing Table |
| `check-card-drift.py` | Every card written down **twice** still says the same thing — a signature card drafted in `campaign/` against the copy in `cards/` |

```
python3 agent-tools/check-references.py
python3 agent-tools/check-geography.py            # contradictions only
python3 agent-tools/check-geography.py --strict   # also approximations
python3 agent-tools/check-card-drift.py
```

All three exit 1 on a finding.

## The gap between them

`check-references.py` proves a name points at something. It cannot prove the thing it points at says what the citing line claims. `check-geography.py` closes one slice of that — direction — because direction is the one class of claim with a single owning file to check against.

Worth knowing: building the bearing table caught more than running it did. Briarwatch was described as a day west of Vulture's Nest *and* on Turnroot Weald's edge, ~13 days apart, and nothing flagged it until somebody had to write both facts into the same table.

`check-card-drift.py` closes a second slice, and it exists because `cards/chris.md` and `cards/pat.md` created the gap on the day they were written: a signature card is now in two files on purpose, the reasoning in `campaign/` and the card in `cards/`, and `check-references.py` cannot see a disagreement between them — it loads `cards/` only, so one copy in each directory is not a duplicate to it. It caught a real one on its first run, inside the file that had just been added.

Everything else is still hand-checked, and the standing example of why is the Steve bug: `characters/steve-and-pip.md` had Pip forming during the Final Current bathing ritual while `quests/tide-pulls-back.md` said he never bathed and never would. Two files asserting incompatible events. No reference was broken, no compass word appeared, and nothing mechanical could ever have seen it. That class needs a person reading both files with the question in mind.

The cheap discipline that helps most isn't either script: **a claim derived from another file carries a citation to it.** The value isn't for the reader — it's that writing the citation means opening the file, which is where the contradiction gets noticed.
