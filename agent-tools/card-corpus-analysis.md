# Card Corpus Analysis — Scope

**Not built. This is a specification, not a tool.** Nothing here runs yet. Do not cite it as if it had produced output.

Scoped 2026-08-17 at Drew's request, as the first stage of a possible batch pipeline. The batch half — generating candidate cards in volume — is deliberately deferred; see Out of Scope.

---

## What It Is

A read-only analysis pass over `cards/`. It produces a **design brief**, not cards: where the set is dense, where it is empty, which mechanics it keeps restating, and which cards sit outside their own color's power curve.

Output is input to `agent-tools/card-creation.md`, which stays the authorship and reasoning layer. This tool never writes a card, never edits `cards/`, and never decides anything.

## Why Analysis Before Generation

Three reasons, in order of weight:

1. **It serves a need that already exists.** Drew (2026-08-16): *"the hand built Oracle deck angle — refine the card pool instead and see what falls out."* That is analysis of 340 existing cards, not production of new ones.
2. **It gives corpus-level work a home.** The convergence check failed as an authoring-time rule because it applied a whole-corpus judgment to one card mid-design (`memory.md`, Card Creation Is Reasoning, Not a Pipeline). Clustering shows the same thing empirically, at the altitude where it's actually answerable.
3. **There is a prior on bulk AI card selection here.** The AI-assembled 63-card Oracle pool was cleared and set aside to be built by hand (`Oracle/baseoracledeck.md`). Generating volume before knowing what the set is missing repeats that.

## What It Reuses

`agent-tools/verify.py`'s `load_canon()` already parses every card block into `{name, color, stat, tag, range, die, file, block}`. That is the parser. Do not write a second one — a divergent parser would drift from what `verify.py` enforces, and the two disagreeing is worse than not having the tool.

---

## The Analyses

### 1. Coverage Grid

Cross-tabulate the corpus on its own structural axes: color × range, color × die, color × tag, range × die.

**Output:** the filled and empty cells. An empty or near-empty cell is a design prompt — *"no Green/Melee card touches initiative"* — not a defect and not an instruction to fill it.

**What it can't decide:** whether a hole should be filled. Some cells are empty because the design says so. Blue holding almost no d8 is Mind's identity as the utility stat, not a gap.

### 2. Recurrence Clustering

Normalize each card's Effect and Defensive Bonus text (lowercase, numbers to `N`, punctuation stripped), then group identical and near-identical expressions.

**Critical distinction, or the output is noise:** a keyword used by many cards is the keyword system working. Eight cards granting Evade is not drift. The real signal is **longhand text that recurs** — a mechanic the set keeps writing out because it has no defined term. Filter keyword-only grants before clustering.

**Excluded from the scan: conditional triggers.** *"If you did not attack last turn," "if you changed position since your last turn," "if you are in the backline"* — these recur, and they are deliberately not compression candidates. Reporting them is a false positive, not a finding. (2026-08-17, Drew. Reasoning and the general rule it establishes: `agent-tools/card-creation.md`, Mechanic.)

**Output:** ranked recurring longhand expressions, with the cards involved. Feeds the compression rule directly (`agent-tools/card-creation.md`, Mechanic).

**What it can't decide:** whether a cluster has earned a keyword. That's flagged for Drew — no threshold is set, on purpose.

### 3. Power Outliers

`combatsimulations/` already reconciles 174 cards against canon and has a working engine. Run the corpus through it and report cards sitting well outside their color's and die's distribution.

**Output:** outliers, both directions. A card far above the curve is a balance question; far below is often a card that never gets picked.

**What it can't decide:** whether an outlier is wrong. Bosses are bespoke by design, and `bestiary/root-heart.md` carries an explicit HP exception for exactly this reason.

### 4. Oracle Eligibility — moved out

Its own tool (2026-08-17, Drew). See `agent-tools/oracle-eligibility.md`. It measures the corpus against a stated target rather than describing a distribution, which makes it a different kind of pass from the three above.

---

## Validation Run

Run once against the live corpus, 2026-08-17, to confirm the analyses find real things. **A one-time check, not a maintained table — recount rather than trust these.**

- **Coverage grid works and matches stated design.** Red skews Melee, Blue skews Ranged, Green skews Both — the same identity `Oracle/baseoracledeck.md`'s 12/6/3 split encodes. Die spread confirms Body/d8 as the power stat, with Blue holding a single d8 in the entire set.
- **Recurrence clustering needs filtering to be worth anything.** Naive clustering flagged ~105 cards; nearly all were healthy keyword reuse. Filtered to longhand only, the signal narrowed to ~16 recurring expressions across ~40 cards.
- **The run's headline finding was rejected on review, which is the useful part.** The largest cluster was a family of conditional damage riders — at least seven cards across three conditions. It read as an obvious compression candidate and it isn't one; Drew cut the whole category (see the exclusion under Recurrence Clustering). Worth recording rather than quietly deleting: the analysis correctly found the biggest repetition in the set, and the biggest repetition in the set is one that should stay as it is. Frequency ranking will keep surfacing things that shouldn't be compressed. Treat every cluster as a question, never a recommendation.

## Parsing Hazards Found During Validation

- **Parameterized keywords.** The glossary defines `Thorns X`, `Armour X`, `Future-Lock X`. A naive keyword match on the bare name misses these and reports false compression candidates. Match the stem, not the full entry.
- **Conditional and negated references.** `rules/card-glossary.md`'s own counting note already excludes *"if the defender is Rooted"* and *"ignores Evade"* from keyword counts. Clustering has to make the same exclusion or it will read a condition as a grant.
- **Colorless cards.** Three of 340 have no color/stat. They break any grid keyed on color; handle explicitly rather than dropping them silently.

---

## What Stays a Human Call

Everything the tool surfaces is a candidate, never a verdict. Specifically:

- Which gaps are worth filling, and which are the design working.
- Whether a recurring expression has earned a keyword.
- Whether a power outlier is a problem or a boss.
- Whether two similarly-worded cards should converge, or whether the difference is the design. **This is the question that failed at authoring time.** The tool can show that two cards say nearly the same thing; it cannot decide whether that matters.

The word *interesting* does not appear as a filter anywhere in this scope, on purpose. Clustering and ranking are computable. Interest is not — a metric named *interesting* would be doing the same undefined work *"fundamentally alter"* was doing in the removed convergence check.

## Out of Scope

- **Card generation.** No candidate production, combinatorial or otherwise, until the analysis has run and Drew has seen whether the brief alone was the useful part.
- **Any write to `cards/`.** Read-only, without exception.
- **Replacing `verify.py`.** That enforces correctness and gates every commit. This one has no pass/fail and blocks nothing.

## Open Questions Before Building

1. Where does output go — a generated report file, or straight to the session?
2. Is this run on demand, or folded into the roughly-every-5-changes staleness sweep (`CLAUDE.md`, Agent Workflow)?
3. Does `Oracle/baseoracledeck.md`'s eligibility pass share this tool's parser and report format, now that it's split out, or stand fully alone?
