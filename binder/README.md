# binder

**Player pages for the bestiary binder Chris keeps** *(Drew, 2026-10-08)*. **The players never see this repo** — everything they hold is printed, and a creature's page is earned at the table (`CLAUDE.md`, Conventions worth knowing before you edit).

**These are not the bestiary files.** `bestiary/` is written for the GM — tactics, how to beat it, win rates, traits the party may never see. **A page here is written fresh, for players, and holds only what the party could know.** *Never copy a bestiary file in; write the player page from it and leave everything else behind.*

**Two pages per creature, each with its own `# ` heading so it prints on its own sheet:**

| Page | Handed over | What is on it |
|---|---|---|
| **Field notes** | After the party's first real encounter with it | What it looks like and what anyone would notice, **plus blank lines** for the note-taker to fill in |
| **Measured** | **When MEASURE (or anything that reveals stats) lands on one** | **Stats, HP, Skills, Traits and Passives**, and for a simple creature run from a blank deck, **its signature cards** (`rules/card-glossary.md`, Reveal stats) |

*Field notes can be handed over without the Measured page ever following — a creature nobody measured stays a page of the party's own guesses, which is the point.*

**Not part of `printing/generate-all.sh`.** A page goes out when something happens at the table, not when the repo changes, so it is built on request: `printing/generate-rules-pdf.py` finds files in this folder, and the PDF goes to Drew in chat like every other printed artifact (`printing/README.md`).

## Pages

| Creature | Pages | Note |
|---|---|---|
| Wrackclaw | `binder/wrackclaw.md` | |
| Redjaw | `binder/redjaw.md` | |
| Duskwick | `binder/duskwick.md` | **Measured is printed blank** — it is Obscure (`rules/card-glossary.md`, Obscure). *The ordinary one; the Large One at Briarwatch is not on it* |
| Flapjack Octopus | `binder/flapjack-octopus.md` | |
| Foulhaul | `binder/foulhaul.md` | **Plus a page for the Grandfather**, with his own cards |
| Gollop | `binder/gollop.md` | |
| Gowra | `binder/gowra.md` | Its own four cards |
| Ocellus | `binder/ocellus.md` | The pup. *No cards of its own — the page shows the three it plays* |
| Glassgut | `binder/glassgut.md` | The spooklight that is an animal. *Most spooklights are nothing and get no page* |
| Gene-Thief Tardigrade | `binder/gene-thief-tardigrade.md` | The baseline; **a line to write in what this one started with** |
| Muirn Hunter, Vaun, Neshi, Draksa | `binder/muirn-hunter.md`, `binder/vaun.md`, `binder/neshi.md`, `binder/draksa.md` | **People.** Hand the page over once the party knows the name |

**Field notes only — nothing to measure:**

| | | |
|---|---|---|
| Driftfire | `binder/driftfire.md` | **Not a fight.** Its second page is **In the Water** — the Thread Save, handed over the first time someone goes in |
| Bicolor Spider, High-Altitude Bat, Sapphire Ant | `binder/bicolor-spider.md`, `binder/high-altitude-bat.md`, `binder/sapphire-ant.md` | **Harvest creatures**, with no stat block — the notes ask how they took one and what it is good for |
