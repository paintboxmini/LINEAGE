# Card Corpus Analysis — Scope

**Not built. This is a specification, not a tool.** Nothing here runs yet. Do not cite it as if it had produced output.

Scoped 2026-08-17 at Drew's request, as the first stage of a possible batch pipeline. The batch half — generating candidate cards in volume — is deliberately deferred; see Out of Scope.

---

## What It Is

A read-only analysis pass over `cards/`. **Its primary job is identifying unused design space** — the combinations the set doesn't have yet. Drew (2026-08-17): *"like — there's no green melee initiative shift card. a tool that surfaces those would be useful."* Everything else it does is secondary to that.

Output is a **design brief**, never cards. It is input to `agent-tools/card-creation.md`, which stays the authorship and reasoning layer. This tool never writes a card, never edits `cards/`, and never decides anything.

## Why Analysis Before Generation

Three reasons, in order of weight:

1. **It serves a need that already exists.** Drew (2026-08-16): *"the hand built Oracle deck angle — refine the card pool instead and see what falls out."* That is analysis of 340 existing cards, not production of new ones.
2. **It gives corpus-level work a home.** The convergence check failed as an authoring-time rule because it applied a whole-corpus judgment to one card mid-design (`memory.md`, Card Creation Is Reasoning, Not a Pipeline). Clustering shows the same thing empirically, at the altitude where it's actually answerable.
3. **There is a prior on bulk AI card selection here.** The AI-assembled 63-card Oracle pool was cleared and set aside to be built by hand (`Oracle/baseoracledeck.md`). Generating volume before knowing what the set is missing repeats that.

## What It Reuses

`agent-tools/verify.py`'s `load_canon()` already parses every card block into `{name, color, stat, tag, range, die, file, block}`. That is the parser. Do not write a second one — a divergent parser would drift from what `verify.py` enforces, and the two disagreeing is worse than not having the tool.

---

## The Analyses

### 1. Design Space Grid — the primary analysis

Cross-tabulate **color × range × mechanical function**. The first two axes are structural and come free from the parser. The third has to be derived: classify each card by what its Effect and Defensive Bonus actually *do*, against the settled taxonomy below.

**Output:** the empty and near-empty cells, stated as prompts. *"Nothing in the set is a Green/Melee card that touches initiative."* Near-empty (one or two cards) is often as interesting as empty — a cell with a single occupant may be an accident rather than a design.

#### The Taxonomy — Settled

**Nine functions, anchored on the three core pillars** (2026-08-17, Drew). The first three are the game's own established vocabulary (`Oracle/baseoracledeck.md`, `agent-tools/archetypes.md`); the other six are the keyword glossary's real domains.

| Function | What lands here |
|---|---|
| **RPS** | Tie resolution, auto-wins, reversals, attacks cancelled before resolution, color counters |
| **Initiative** | Initiative Shift X, turn order, extra or skipped turns |
| **Position** | Frontline/Backline movement, forced movement, Rushdown, Rooted, **Anchored**, **Quick** |
| **Economy** | Draw, Scry, discard, deck search, Exile, shuffle, return-to-hand |
| **Information** | Reveal, look-at, blind selection, naming a color, Obscure |
| **Damage mod** | Deadly, Weak, Vulnerable, Critical, Thorns, Counter Attack, Unpreventable, flat bonus damage |
| **Defense** | Evade, Resist, Ward, Armour, Protect, Immunity, Deflect |
| **Control** | Staggered, Blind, Sealed, Locked, and any "cannot play/attack/defend/use" |
| **Sustain** | Heal, Lifesteal, HP restoration |

**Multi-label.** A card counts in every function it touches. *"Scry 2. Choose 1 card in the target's hand without looking…"* is both Economy and Information. Forcing a single label would hide real coverage.

**Assign by what the glossary says a mechanic does, never by surface wording.** This is the rule that matters most, and it was learned by getting it wrong. On the first pass Anchored and Quick were filed under Initiative because they *sound* like timing. They aren't: Anchored is a benefit that persists **while you don't move**, and Quick is **a free move**. Both are Position. That single misassignment silently filled `G/Melee/Initiative` — the exact gap Drew had already identified from memory — and the tool reported no hole where a real one exists. A taxonomy is only as good as the assignments under it.

**Changing this table changes every result the tool has ever produced.** Treat an edit here as a design decision with its own discussion, not a tuning knob. Granularity was tested at 5, 9, and 10 categories before settling: the empty-cell rate held at 6–7% throughout, so this was never a signal-to-noise tradeoff — it is a choice about which distinctions are worth seeing.

**What it can't decide:** whether a hole should be filled. Some cells are empty because the design says so — Blue holding almost no d8 is Mind's identity as the utility stat, not a gap. An empty cell is a question about why, and *"because it shouldn't exist"* is a complete and common answer.

### 1b. Structural Grids

The cheap version of the above, on parser-native axes only: color × range, color × die, color × tag, range × die. No taxonomy required, so no judgment baked in. Useful as a sanity check on the set's stated identities, and it runs even if the function taxonomy is still unsettled.

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

### 4. Keyword Trimming (Decompression)

The reverse of compression, and the answer to a problem that was open until 2026-08-17: nothing retired a keyword that stopped earning its place, so the glossary only ever grew. Drew: *"for keyword trimming we could use a cut off of some kind ~4 or less cards with the keyword and we decompress the text back onto the cards that use the keyword."*

**Count triggers the review. It does not make the decision.** The criterion is the same one that governs compression, run backwards: *is the keyword cheaper at the table than its longhand?* A rarely-used keyword whose definition is one short clause should be inlined — the lookup costs the table more than the words would. A rarely-used keyword whose rule carries real subtlety should stay compressed even at one card, because restating it on every card invites the restatements to drift apart. That is already why `rules/card-glossary.md` carries Obscure and Critical at a single use each.

**The process, in order:**

1. **Filter by category first.** A raw count targets the wrong entries. The glossary holds at least four kinds of thing, and only one is a decompression candidate:
   - **Card-printed status keywords** (Evade, Rooted, Sealed) — the real targets.
   - **Umbrella terms** (Debuff, Positive Status Effects) — defined so *other rules* can name a set. They aren't printed as effects, so a card count is meaningless for them. Never candidates.
   - **Damage and rule properties** (Unpreventable, Critical) — describe how something behaves; referenced by other glossary entries.
   - **Actions** (Exile) — referenced by rules and status cards, not only by cards.
2. **Count live usage**, not the glossary's stated number. Those counts are a dated snapshot and the file says so.
3. **Flag everything at or below the threshold** for review.
4. **Apply the table-cost test** per flagged keyword. Decompress only where longhand is genuinely cheaper for a player.
5. **If decompressing:** rewrite every card that uses it with the longhand, remove the glossary entry, and log it. Partial decompression is the failure mode to avoid — see Expose, below.

**Threshold: not set. Needs Drew's call.** At ≤4 the review list is roughly a dozen of 31 glossary entries, and several of those are category errors that step 1 removes. There's no natural cliff in the distribution to snap to — usage tails off smoothly from the high fifties down to one — so the number is a judgment about how much review work is wanted at once, not something the data settles. Recommend running step 1's category filter and a live recount first, then picking the threshold against the list that actually results.

**Expose is the live case, and it is mid-decompression right now.** `Expose [Color]` is defined in the glossary and used by four cards. Three use the compressed form (*"Expose Red — inflict Staggered"*). The fourth, in `cards/tithe-engine-ashfall.md`, restates the keyword's whole definition inline: *"Expose Blue — choose 1 card in the target's hand without looking. If it is Blue, they discard it."* That is the keyword and its longhand definition on the same card, which `agent-tools/card-creation.md` explicitly says not to do. It should be resolved deliberately in one direction — not left as one card explaining itself while three don't.

### 5. Oracle Eligibility — moved out

Its own tool (2026-08-17, Drew). See `agent-tools/oracle-eligibility.md`. It measures the corpus against a stated target rather than describing a distribution, which makes it a different kind of pass from the three above.

---

## Validation Run

Run once against the live corpus, 2026-08-17, to confirm the analyses find real things. **A one-time check, not a maintained table — recount rather than trust these.**

- **Structural grids match the set's stated design.** Red skews Melee, Blue skews Ranged, Green skews Both — the same identity `Oracle/baseoracledeck.md`'s 12/6/3 split encodes. Die spread confirms Body/d8 as the power stat, with Blue holding a single d8 in the entire set.
- **The design space grid works, and independently confirmed the hole Drew named.** Under the settled nine-function taxonomy, 81 cells, 7 empty:

  `R/Both/RPS` · `R/Both/Initiative` · `B/Melee/Sustain` · **`G/Melee/Initiative`** · `G/Melee/Economy` · `G/Melee/Information` · `G/Ranged/RPS`

  Plus ten cells holding exactly one card, which are often the better prompts — a lone occupant may be an accident rather than a design. Notable singletons: `B/Melee/Position` (BINDING RITE), `G/Ranged/Position` (FLOW), `R/Both/Information` (EMBER CIRCLE), `B/Both/Sustain` (FOREST MEMORY). RPS is a singleton in four separate cells and empty in two more — the thinnest function in the set by a wide margin, which is worth a look on its own.
- **Recurrence clustering needs filtering to be worth anything.** Naive clustering flagged ~105 cards; nearly all were healthy keyword reuse. Filtered to longhand only, the signal narrowed to ~16 recurring expressions across ~40 cards.
- **The run's headline finding was rejected on review, which is the useful part.** The largest cluster was a family of conditional damage riders — at least seven cards across three conditions. It read as an obvious compression candidate and it isn't one; Drew cut the whole category (see the exclusion under Recurrence Clustering). Worth recording rather than quietly deleting: the analysis correctly found the biggest repetition in the set, and the biggest repetition in the set is one that should stay as it is. Frequency ranking will keep surfacing things that shouldn't be compressed. Treat every cluster as a question, never a recommendation.

## Parsing Hazards Found During Validation

- **Parameterized keywords, two different shapes.** The glossary defines both `Thorns X` / `Armour X` / `Future-Lock X` and `Expose [Color]`. A bare-name match misses the first kind; matching the literal entry misses the second, since cards print *"Expose Blue,"* never *"Expose [Color]."* Both forms produced false findings on the validation run — Thorns reported as undefined, Expose reported as unused at 4 live cards.
- **Conditional and negated references, excluded carefully.** `rules/card-glossary.md`'s own counting note excludes *"if the defender is Rooted"* and *"ignores Evade"*. A naive "any `if` near the keyword" filter over-excludes and will drop real usage: *"If your HP is 6 or less, gain Immunity"* is a genuine grant behind a condition, and a crude filter reported Immunity as unused. Exclude the keyword appearing **as the condition's subject**, not every keyword sharing a line with an `if`.
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

1. **What is the decompression threshold?** See Keyword Trimming — recommend deciding it against a category-filtered live recount rather than in the abstract.
2. Where does output go — a generated report file, or straight to the session?
3. Is this run on demand, or folded into the roughly-every-5-changes staleness sweep (`CLAUDE.md`, Agent Workflow)?
4. Does `Oracle/baseoracledeck.md`'s eligibility pass share this tool's parser and report format, now that it's split out, or stand fully alone?
