# Canon Gate — Design Trail

This is a historical design trail for the evolution of the Canon Gate and authority model. It explains why the current process is shaped as it is; it is not a second source of current operating instructions. Current authority and workflow live in `CLAUDE.md`.

## The original problem

The Canon Gate began as a broad review layer: new work was treated as something the agent needed to evaluate before it could enter canon. That made the agent's job larger than necessary. It blurred several different questions:

- Does the proposal have creative approval?
- Does it fit the existing canon?
- Is the requested change merely using established language, extending canon, or changing the language itself?
- Is the agent interpreting Drew's compressed input correctly?
- Does the repository need mechanical propagation after the change?

Treating all of these as one review problem encouraged unnecessary deliberation and made routine integration expensive.

## The jurisdiction distinction

The important conceptual split became **authority vs. interpretation**.

Authority asks: **who is allowed to commit this kind of change?**

Translation asks: **how confidently can the agent determine what Drew means?**

These are different axes. A change can be easy to understand but constitutionally important, or difficult to interpret while remaining an ordinary content extension. The Canon Gate should not use one axis as a proxy for the other.

This led to the three authority levels:

### Authority 1 — Established Language

The agent is using existing canon without changing its meaning: encounters, creatures, NPCs, cards built from established mechanics, and prose improvements. These can ship after the required review checks.

### Authority 2 — Canonical Extension

The agent adds something new without redefining existing canon: new faction behavior, regional custom, a map Seat, a deepened NPC, and similar extensions. These can be integrated with audit and clear visibility, but an extension may not redirect an established theme or meaning.

### Authority 3 — Constitutional

The change alters the language itself: formulas, keywords, progression, cosmology, core Design Principles, contradictions of established canon, or anything else that changes how other content is interpreted. The agent may identify and articulate the issue, but Drew retains authority to decide it.

A3 observations do not need their own standing recommendation queue. When the issue requires Drew's constitutional judgment, surface it in conversation. If an unresolved concern has lasting value, preserve it in `unresolved-concerns.md`.

## From tiers to Authority Levels

The three levels were not named this way from the start. Early on they were called tiers, and "tier" quietly implied the wrong axis — magnitude, how big or impressive a change was — when the actual axis is jurisdiction: who is allowed to commit this kind of change. A creature built entirely from established mechanics can be extraordinary and still sit at Authority 1; a four-word wording tweak to a formula can carry constitutional weight and sit at Authority 3. GPT, via Drew, caught the mismatch, and the rename followed the same day: Authority 1 (Established Language, agent authority), Authority 2 (Canonical Extension, agent authority with audit), Authority 3 (Constitutional, Drew's authority). The vocabulary swept through `CLAUDE.md`, the experimental README, both content generators, and the agent-tools README; "tier" was retired from governance entirely and now belongs only to creature/encounter difficulty (Early/Mid/Late) — a genuinely different scale that happened to share the word by accident.

The rename carried Authority 2's anti-drift rule along with it: an extension may extend canon, but it may not redirect an existing theme — the guard against five hundred individually-harmless extensions quietly reshaping the world underneath everyone. The rule reuses the Translation Principle's own redefinition test (*will this change the meaning of something already established?*), so one question polices both how confidently an interpretation can be trusted and how far an extension is allowed to reach.

GPT's own framing of the rename is worth keeping: the gate wasn't an invented governance model bolted on afterward. It named the process that was already being practiced. That's why the rename had evidence behind it rather than being a guess at a better structure.

## From review gate to integration gate

A major harness insight was that approved experimental work should be **presumed ready for integration**. The agent's default job is not to prove that a proposal deserves to exist. That creative decision has already been made when Drew approves the work.

The agent's narrower responsibility is to determine whether it can be integrated cleanly without violating existing architecture.

The practical escalation conditions are things such as:

- canonical conflict;
- constitutional rule change;
- ambiguous placement;
- cross-system contradiction;
- missing propagation target;
- authority-level uncertainty.

Everything else should remain ordinary integration work.

This produces a useful separation:

- **Semantic work** requires judgment.
- **Mechanical work** should remain mechanical.

Moving files, updating links, fixing references, changing headings, and propagating renamed concepts should not consume the same reasoning budget as resolving a constitutional conflict.

The 2026-08-06 harness brainstorm captured the desired direction explicitly: routine changes should integrate automatically, structurally risky changes should open review, and constitutional changes should require Drew.

## Review remains real

Presuming integration does not mean skipping review.

Experimental content still has to be read against current canon before shipping. A same-file read can catch internal inconsistency; only a repository-level read can catch a closed thread being reopened, an established identity being mutated, or a newly invented fact duplicating something that already exists.

The review therefore became **targeted rather than universal**: spend expensive reasoning where the repository actually presents a risk.

### Worked examples: what a repository-level read catches

Three cases from the mechanics side of the repo show why the review stayed real even after integration became the default.

**The Anchored bug was in the glossary, not the card.** A first read of GRAPPLE's "Anchored — Defender gains Rooted" flagged the card as misusing the keyword — the glossary's own wording ("You gain a specific benefit...") reads as self-only. Drew corrected the location of the actual bug: the glossary was wrong, not the card. Checking whether the mechanic already worked this way anywhere in shipped canon settled it fast — it did, twice (Rooted Oath targets a named ally; Iron Grip states the plain-Rooted-vs-Anchored distinction directly, on the same card). The instinct that produced the wrong flag is worth naming plainly: the newer, less-tested thing (a hand-pushed experimental card) was assumed more likely wrong than the older, load-bearing thing (a keyword definition four other cards already depend on) — usually a sound prior, wrong here. A rule that's documented narrower than what's actually implemented is its own kind of drift, and the fix belongs in the documentation.

The same pass held AID back rather than shipping it or cutting it outright. AID and SUPPORT weren't a clean duplicate — the numbers differ — which made "ship both, more variety" tempting. But the mechanical-identity check (does this create a decision no other card creates?) says variety in stat totals isn't variety in decision space, and AID didn't ask a player to weigh anything SUPPORT didn't already ask. Rather than rendering a verdict, the side-by-side comparison went to Drew directly — concrete enough that he could see the overlap himself instead of taking "these are similar" on faith. The call wasn't ambiguous enough to need his design judgment, but it also wasn't the reviewer's call to make unilaterally.

**Future-Lock needed checking against the glossary's own existing rules, not just against the draft that proposed it.** A draft described Future-Lock as though the keyword already existed, when what it actually proposed was a full swap of the underlying mechanic. `experimental/README.md`'s own rule — no new keyword without discussion first — applied directly, so the mechanic got discussed before any file was touched. The real find came from reading the glossary's existing Stat Change section on its own terms, not from the draft at all: hand size is guaranteed never to drop below 2 from Mind loss. Future-Lock's approved design needs to go to 0. Neither the draft nor Drew's approval of its direction had checked the new keyword against that rule, because neither reading crossed the two documents. Resolved as a stated exception, not a silent one — the glossary entry says outright *"No floor at 2. This is not a Mind loss"* — because Future-Lock is a direct hand-size modifier, the same category CLIMB's own +1 already lives in, not a Mind-stat drain. A future reader hits the explanation at the point of the exception instead of finding a contradiction and having to go looking for why.

**The nine-card audit triage separated "fixed the wording" from "fixed the mechanic," and a routine collision sweep on one card surfaced staleness in six unrelated files.** Drew triaged a three-agent audit into nine per-card instructions, ranging from exact ("fix CHARGE's Range") to open ("STUDY and PROFILE take a swing"). SLIPSTREAM's reword fixed a contradiction with Anchored's own glossary definition; it didn't newly implement a mechanic that was never wired into the simulator — worth stating precisely, since the two claims read alike from the outside but aren't the same fact. PROFILE's hand-peek rework wasn't a new category of unmodeled effect either; it joined an already-established, already-justified precedent (hand-reveal and hand-peek effects are no-ops against a policy AI with full information regardless). CHARGE's own fix collided with the Oracle pool's frozen composition — the third time that exact shape of collision had come up in one session — and the right call was to do nothing: the pool was already explicitly marked pending-propagation, waiting on Drew's own hand-build, and swapping a card into it would have meant touching a file he'd already said not to touch yet. That restraint got flagged in the plan rather than silently applied. The actual yield of the pass wasn't any of the nine cards — it was that checking BREAK's, PROFILE's, and FLOW's restated text against every file that quoted them turned up five character files where the wording had already gone stale, independent of this batch, traced back to an earlier Initiative Shift rework. Six instances of the same failure shape (a card's canonical text moves; a restatement elsewhere doesn't move with it) found only because checking collisions had become routine instead of optional.

## The current model

The mature Canon Gate is therefore a jurisdictional integration system:

1. Determine what kind of change this is.
2. Translate the request without silently redefining it.
3. Check it against current canon.
4. Integrate ordinary approved work.
5. Escalate genuine conflicts, ambiguity, propagation failures, or constitutional changes.
6. Reserve constitutional authority for Drew.

The result is not a weaker gate. It is a narrower one: the agent is responsible for **clean integration and zero silent regressions**, not for repeatedly re-litigating creative approval.

## The gate loosened

Even after integration became the default framing, the practice underneath it hadn't actually changed: everything still waited for Drew's formal pass before touching canon, and because most content verdicts were predictably "approved," finished work piled up at a gate that no longer needed to hold it that tightly. Both an internal audit of this branch and an independent sweep from Codex flagged the same failure mode without coordinating with each other.

Drew's instruction was precise about scope: *"loosen the gate, on content only, not rules/invariants."* The three Authority levels became placement rules, not just jurisdiction labels. Authority 1 — content built from established canon only (encounters, creatures, cards, items, NPCs) — ships direct, after the mandatory red-team and alignment checks, with no pre-approval wait. Authority 2 — clean extensions (new faction behavior, a map Seat, a deepened NPC) — ships flagged: Drew's review becomes veto-after instead of approve-first. Authority 3 — rules, invariants, keywords, formulas, cosmology, contradictions, open world-level hooks — stays gated exactly as before, permanently, with no loosening at all.

The mechanism that makes veto-after safe rather than reckless is a standing **Recently shipped (post-review queue)** section at the top of `memory.md`: one line per Authority 1/2 ship, Drew clears each by blessing it or objecting, and every ship stays one revert away for as long as it sits unreviewed. The gate loosened because the automated checks got good enough to trust, not because review stopped — the checks stayed mandatory, and the history stayed reversible. The boundary between the levels wasn't invented for the occasion; it was traced back from rulings Drew had already made that same week — a creature shipped and kept was already Authority 1 in practice, a one-line faction ratification was already Authority 2, a piece of world lore sent back for more work was already Authority 3. Naming the boundary just made explicit what his own decisions had already been doing.

**External validation followed, rather than being sought out.** Three outside models navigated the repository cold in the weeks around the loosening — Grok, GPT (ongoing, via the Drew copy-paste channel), and Codex (a full sweep on its own branch) — and the pattern held across all three: no structural complaints, ever. Feedback stayed content-focused; each one oriented and went straight into design work, which is what a working architecture looks like from the outside. Codex's own biggest finding — good material stranded in `experimental/` — was the same conclusion this branch's own audit had reached independently, days earlier (the promotions of Canille, Pneum, and the Lightning Loop item), confirming both the specific finding and the underlying failure mode behind it: a canon gate that works well enough is also a canon gate that finished work piles up in front of. The standing habit that followed — periodic experimental sweeps with promotion recommendations, whenever the folder starts to feel heavy — is the gate's own answer to its own success.

## Untangling the Translation Principle from the gate

The two systems this file exists to explain — the Translation Principle (how confidently the agent can read Drew) and the Canon Gate (who may commit this kind of change) — had drifted into each other's territory on the page, and Drew caught it directly rather than trusting the existing text: *"the translation principle was conflated, as was the authority levels... don't overly trust what I have to say when it comes to CLAUDE.md, agent tools, etc."* — an explicit instruction to apply independent scrutiny to agent-doctrine structure specifically, since his own calibration put him as a novice on the agent side and an expert on the game itself.

Investigating rather than assuming confirmed the conflation was real and specific. The redefinition test — *will this change the meaning of something already established?* — was stated three separate times across roughly eighteen lines: once in Authority 2's body, once in its parenthetical, once again in the Translation Principle's own bullet. And two independently-numbered 1/2/3 systems — the Translation Principle's ambiguity levels and the Canon Gate's Authority levels — shared the word "constitutional" for their own tier 3, with no stated mapping between the two 1s or the two 2s: an unlabeled parallel structure inviting exactly the conflation Drew had named. This wasn't accidental drift; the file's own history — the tier-to-Authority rename above, and its anti-drift rule deliberately reusing the same redefinition test — shows the duplication started as intentional reuse of one test for two jobs. It needed surgical un-conflating, not a rewrite.

**Drew's own pushback on the draft fix was the sharpest catch of the pass:** *"shouldn't the translation principle be applied before the canon gate? if something's not interpreted correctly then how can it be correctly gated?"* Correct, and it exposed a real ordering bug the draft fix itself had been about to ship: Authority 2 forward-referenced a term the document hadn't introduced yet (*"apply the Translation Principle's redefinition test, below"*), which is bad document structure independent of the conflation — a reader shouldn't need a concept before it's been defined. The sections were reordered so the Translation Principle now precedes the Canon Gate in `CLAUDE.md`, matching both the real logical dependency (interpret first, then classify what's been interpreted) and ordinary expository writing (define before use).

Resolved: the redefinition test is now stated exactly once, in the Translation Principle, and named — "the redefinition test" — so Authority 2 can point backward at it instead of restating it. The two 1/2/3 systems no longer share unlabeled numerals: Authority keeps its numbers, used too pervasively downstream (the encounter and NPC generators, both READMEs) to be worth renaming twice in one file's history; the ambiguity levels dropped their numerals entirely and are framed explicitly as a different axis — confidence in a reading, not who may ship it — kept genuinely distinct per Drew's own example: a fully-confident reading of a clearly-stated new keyword is still Authority 3, no matter how little doubt the agent has about what it means.

## Provenance

The principal historical source for this evolution is the 2026-08-06 harness brainstorm, which proposed explicit Intake → Integration → Arbitration phases and a presumption of integration.

The current authority model is recorded in `CLAUDE.md`; this file preserves the reasoning trail that explains how that model emerged.
