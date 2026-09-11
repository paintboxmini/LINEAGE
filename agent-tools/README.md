# agent-tools

Consistency checks for the repo's own content. Run by hand, one job each.

**Neither is wired into `printing/generate-all.sh`.** That script rebuilds print artifacts and nothing else, deliberately.

| | |
|---|---|
| `check-references.py` | Every **name** resolves — document paths, section citations, decklist card names, and no duplicate card names |
| `check-geography.py` | Every directional **claim** agrees with the map in `world/geography-overview.md`, Bearing Table |

```
python3 agent-tools/check-references.py
python3 agent-tools/check-geography.py            # contradictions only
python3 agent-tools/check-geography.py --strict   # also approximations
```

Both exit 1 on a finding.

## The gap between them

`check-references.py` proves a name points at something. It cannot prove the thing it points at says what the citing line claims. `check-geography.py` closes one slice of that — direction — because direction is the one class of claim with a single owning file to check against.

Everything else is still hand-checked, and the standing example of why is the Steve bug: `characters/steve-and-pip.md` had Pip forming during the Final Current bathing ritual while `quests/tide-pulls-back.md` said he never bathed and never would. Two files asserting incompatible events. No reference was broken, no compass word appeared, and nothing mechanical could ever have seen it. That class needs a person reading both files with the question in mind.

The cheap discipline that helps most isn't either script: **a claim derived from another file carries a citation to it.** The value isn't for the reader — it's that writing the citation means opening the file, which is where the contradiction gets noticed.
