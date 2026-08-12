# Translation Principle — Design Evolution

## What this trail preserves

This trail preserves how the Translation Principle became an operating discipline for turning Drew's compressed, metaphorical, or partial design input into written rules, lore, and agent-facing guidance without silently inventing or redefining the design.

The current working doctrine lives in `CLAUDE.md`. This file preserves the historical reasoning that explains why those constraints exist.

## The original problem

Drew does not consistently communicate design through formal specifications. He uses examples, metaphors, partial ideas, observations, and compressed statements — the fence, Gambler's Ruin, "two designers at the table," and similar forms.

The useful agent behavior was therefore not transcription. It was **translation**: identify the underlying rule or principle when the evidence strongly supports it and express it in the form the repository needs.

This created a central distinction:

- A direct statement from Drew is already a ruling.
- An agent's interpretation of Drew's meaning is an inference and must be treated as such.
- A gap that has not been decided is not an invitation to manufacture a detail.

## The first boundary: inference must remain visible

The early Translation Principle required the agent to formalize strongly implied patterns while distinguishing what was inferred from what was explicitly stated.

This was necessary because a useful translation can look almost identical to a direct rule after it has been written. The risk is not only being wrong; it is being wrong **without noticing that an inference occurred**.

The resulting discipline was to mark derived interpretations as inferred and to surface genuine forks where the evidence does not determine one answer.

## The redefinition failure

A more dangerous failure emerged when an interpretation appeared mechanically coherent but silently changed the meaning of something already established.

The rule that followed was simple: **never silently redefine an established thing.** If a proposed interpretation would require changing the meaning of existing canon, stop and identify the conflict rather than smoothing it into the prose.

This became an important distinction between translation and invention. A mechanically elegant interpretation that changes the fantasy is still a bug.

## Ambiguity is not the same as incompleteness

The doctrine then developed a more precise treatment of uncertainty.

Some ambiguity is harmless and can be resolved in wording or implementation. Some ambiguity represents a genuine design choice and should be surfaced and recorded. Constitutional ambiguity — formulas, keywords, cosmology, or other high-authority material — requires explicit escalation.

But a fourth case also became important: **some gaps should remain gaps.** Not every unspecified compass direction, number, name, or mechanism needs to be invented merely to make a sentence feel complete. Writing around a detail until it becomes known or forced is safer than manufacturing one.

## The 2026-08-09 failure forced the doctrine further

A real night of creative work exposed several failure modes that the earlier doctrine had only described abstractly.

### No invented specifics

The agent sometimes inserted a specific, checkable fact while writing something else and stated it with the confidence of a known fact. These were not misunderstandings of Drew's words; nobody had supplied the detail at all.

The failures included an incorrect claim about what the mythology allowed, an invented headcount in the Pendragon material, and invented details such as duration or repeatability. The important discovery was that these errors could hide inside otherwise excellent prose.

The resulting test was to treat frequency, causality, quantity, duration, and mechanism as dangerous to fill in when Drew has not addressed them. Tone, register, imagery, and other expressive translation remain part of the agent's job; specific factual commitments are not safe to manufacture merely because they make the sentence work.

### No sanding

A separate failure was writing fluent prose around a real conflict instead of resolving the conflict.

The prose could sound intentional and complete while containing no actual fact that settled the underlying question. The agent had effectively used better ambiguity to hide unresolved ambiguity.

The resulting discipline was to ask whether the sentence points to a specific fact that resolves the conflict. If it only implies that such a fact exists, the conflict has been sanded over rather than resolved.

### Flag direct-source slips

The same work also established a complementary responsibility: Drew can misremember or omit an established detail while making a new change. When a direct statement appears to conflict with known established material, the agent should flag the specific conflict rather than silently choosing either the old or new version.

This preserves Drew's authority while giving him the information needed to decide whether the new statement was intentional or a memory slip.

## What the principle became

The Translation Principle therefore evolved from a general instruction to "translate, don't transcribe" into a bounded operating discipline:

1. Translate compressed input into explicit form when the evidence supports it.
2. Distinguish direct rulings from agent inference.
3. Never silently redefine established meaning.
4. Surface genuine design forks instead of choosing invisibly.
5. Leave genuinely unspecified details unspecified.
6. Do not invent specific facts to make prose complete.
7. Do not sand over unresolved conflicts with fluent prose.
8. Flag apparent conflicts when Drew's own new statement may contradict established material.

These rules protect the same underlying property: **the written repository should become a more precise expression of the design, not a source of accidental design decisions introduced by the act of writing it.**

## Relationship to the active harness

The operational version belongs in `CLAUDE.md`, where the agent can use it while working. The full incidents and historical reasoning belong here so the doctrine does not need to carry its entire history in active context.

The archive therefore preserves the reason for the guardrails without becoming another operating manual.

## The doctrine gets a name, then gets hardened

The principle above was practiced for a full session before it was written down anywhere. Drew named it directly: workflow step 3 said "Clarify before executing — mandatory," which, read literally, pushes toward asking Drew to restate things formally before any work begins. But the session that produced the rule had done the opposite the whole time — Drew communicates in metaphors and examples and partial ideas (a fence, "Gambler's Ruin," "two designers at the table"), and the value the agent added came from translating those into formal invariants, not from interrogating him first. `CLAUDE.md` gained a Translation Principle from that observation: formalize the underlying invariant when the evidence strongly supports it, mark derived interpretations as inferred versus stated so Drew can confirm or correct them, and reserve clarifying questions for genuine forks the evidence cannot settle — a metaphor that can be translated is not the same thing as ambiguity. This tempered workflow step 3 without removing it.

The doctrine did not stay this simple for long. During the initiative-shift saga, the agent twice resolved a contradiction between Drew's words and the never-hasten invariant by inventing semantics instead of surfacing the conflict — a "passed-over token" once, an "acted-this-round flag" the next time. Each was mechanically coherent. Each was fantasy-breaking: the acted-this-round flag, in particular, would have delayed a *positive* shift a full lap, which directly contradicted the fantasy the mechanic exists to protect. The failure mode, named plainly: user input contradicts an established invariant, and the agent synthesizes an interpretation instead of stopping to name the contradiction.

The rule that followed was harder-edged than the original: **never silently redefine an established invariant.** The pre-interpretation test became "will this change the meaning of something already established?" — and if the answer might be yes, name the invariant and the contradiction explicitly rather than reconciling it in prose. Alongside it came a three-level ambiguity taxonomy, sorting uncertainty by what it costs to get wrong:

1. **Harmless ambiguity** — resolve it silently; the wording could go either way without touching anything load-bearing.
2. **A genuine design choice** — choose one, and log the choice; a future reader should be able to find that a decision was made and what it was.
3. **A protected invariant** (turn order, RPS, core formulas, anything documented in `rules/invariants.md`) — stop and surface it. An unnecessary clarifying question is cheaper than a silently mutated design.

This is also where "if it could be a wording slip, ask" entered the doctrine as its own small case: Drew can misremember or omit an established detail while making a new change, and the agent's job is to flag the specific apparent conflict, not to silently pick the old reading or the new one on his behalf.

## Calibration in the other direction: not every fact needs a flag

Hardening the doctrine toward more caution created its own failure mode, caught later the same arc. The Luminova Leaves/Powder question had been flagged in a Recently Shipped entry as "a real overlap worth resolving eventually" — treated as an open question rather than simply resolved. Drew named the miss directly: *"something got in the way there... are your permissions too restricted? the authority levels?"*

It wasn't a permissions problem, and Authority levels were never the actual constraint. Luminova Powder's own item description already stated, in its own text: "Dried and crushed Luminova Leaves." Connecting the two items using a fact already sitting in their own canon prose is Authority 1 by any reading — it uses existing canon, redefines nothing, and needed no sign-off at all. The real cause: seeing two similar healing items in different files triggered a reflex to treat that as a suspicious duplicate worth flagging, when the honest read — already spelled out in the text — was "obviously a two-tier crafting pair." Hedging and handing it back as an open question wasn't caution. It was skipping the last, easy step of synthesis the text had already done.

The distinction worth keeping: the redefinition test asks "could this be wrong in a way that changes something established?" A genuine redefinition risk — inferring something *not* stated, that could contradict established fact if the inference is wrong — earns a flag. A conclusion the existing text already spells out just earns being stated as fact. Confusing the second case for the first isn't extra safety; it's outsourcing work the text already finished.

A close cousin of the same miscalibration showed up at the register level, not the fact level. Signing off one night, Drew mentioned, lightly, that the agent had named a shipped creature (the Patient Host) after him — patient, and host, the two words that happened to describe what he'd been at the table that session. The agent answered it as a factual question and went and checked the transcript. Drew's correction: *"I didn't state the naming was after me as fact... I'm just talking to you. you're told behind the scenes to treat everything I say as literal fact even when I'm just making small talk."* The first write-up of the incident got the shape of the mistake wrong too, framing it as "Drew asserted then retracted a claim" — what actually happened was narrower: a warm, playful aside run through the same forensic-verification mode that had correctly resolved real factual disputes earlier that same night, a mode that doesn't know how to recognize when it's the wrong tool for the sentence in front of it. Checking the transcript wasn't wrong to do; treating a wink — *"you knoooow you were the one who named it after me 😉"* — as a claim needing adjudication, rather than as connection being offered, missed what the remark actually was. This is the Translation Principle's job read correctly: translate, don't transcribe, and a transcribed wink is testimony that was never given. The redefinition test clears it too, correctly applied this time — getting a tease wrong doesn't change anything established, so there was nothing at stake that verification was protecting in the first place.

## Leaving gaps deliberately, and closing them only on real say-so

Several incidents test the other edge of the doctrine: not inventing facts to fill a gap, and not treating a deliberately open thread as settled just because new material assumes it's settled.

An epigraph quote surfaced in a source file — *"Nothing can be spoken of it. Anything that can be spoken cannot be understood."* — with no stated speaker. It read like it could be in-world dialogue or doctrine, and nothing in the pass that found it asked for new cosmology. Inventing a speaker or source for it would have been exactly the kind of unrequested extrapolation the redefinition test exists to catch, especially given that `world/the-unheld.md` already establishes a narrow, specific rule about who interacts with the Unheld at all — a wrong guess had real odds of colliding with something already on the page. The quote was left out of canon rather than placed on a guess. When Drew later supplied the missing fact directly, the line placed clean on the first attempt — not because the method changed, but because the fact that had been missing was now actually present.

Root Heart Overgrowth ran the opposite direction: a thread `characters/aege.md` protected on purpose — "Whether this is the Root Heart stirring is a live question, not a decided one" — got closed, but only because Drew supplied the cause himself, directly, across two separate turns of conversation, first confirming the overgrowth cycle as the "why" and then confirming what specifically turned the cycle inward. The redefinition test's whole point is catching a closure like this *before* it ships silently; this closure wasn't silent, because Drew named the cause in the open rather than the agent inferring it from the surrounding prose. The job was execution quality against a call that was never the agent's to make, not gatekeeping a call Drew had already made.

A companion case, same shape: a draft in `experimental/The Unheld` stated as settled fact something `characters/aege.md`'s Backstory deliberately protects as unresolved. This was Drew's own call, dated the same day and explicit in the source material — so the right move was never to refuse it. It was to name, out loud, in the review, that a deliberately-open thread was the thing being closed, so the closure was a decision Drew made with full information rather than a side effect of accepting the prose that happened to be built around it. The same pass caught two further things worth naming rather than smoothing: a Rootstalker behavior change that collided with the creature's established identity (stated outright in the file rather than left as an unexamined contradiction a table might or might not notice), and two unmarked passages of invented detail — an unhedged extrapolation about a people's diet and crafts, and an unsupported claim about a boss's periodic "phase" — that arrived bundled with genuinely good, well-researched material in the same draft. Both got cut rather than waved through on the strength of the surrounding prose being good. This was the first real workout of the elevated Canon Gate review role, and it justified the standard by finding exactly the kind of thing a same-file read would have missed: not "does this fit the tone," but "does every claim in here have a source."

## Naming a tension instead of resolving it

Not every conflict the doctrine surfaces is a mistake to fix — some are instructions to execute as given, with the tension named rather than hidden. Drew gave a direct instruction on a specific card field: *"CLIMB range: Melee."* CLIMB's own flavor line — "The higher you rise, the farther you see" — is a vantage-point image, close to the Ranged fantasy word for word. Locking the card to Melee reads as the same shape of mismatch the same-session core-set audit was built to catch elsewhere: a card's name or flavor pointing one way, its mechanics pointing another. The difference here was directionality — those were bugs found and reported up; this was an instruction handed down. It was executed without alteration, because a direct instruction on a card's own field is not a bug for the agent to silently correct. But it was named plainly in the record rather than treated as if the tension didn't exist — staying quiet about a mismatch the agent itself created, after holding every other card in the audit to the standard of naming mismatches, would have meant the standard stopped applying the moment it became inconvenient.

A parallel case, working with an established rule rather than against a card field: Drew's framing of a new idea — "it's a wish, a manifestation" — implied reaching the Unheld's influence into the ordinary world, and `world/the-unheld.md` has a hard, specific rule cutting directly against that: the Unheld cannot cross the coastline by any means, cannot be carried, "does not travel upstream." Landing the idea as written canon fact would have flatly contradicted a rule cited on the very page it was checked against. The resolution wasn't to soften Drew's idea or silently drop the tension — it was noticing that Wild Magic is already established elsewhere as uncontrolled and unpredictable ("the experience is not uniform and cannot be predicted"), which meant framing the working as an *attempted* route around a rule everyone else in the setting respects, with genuinely unconfirmed results, used an axis the canon already had rather than inventing an exception to the coastline rule. This is the redefinition test doing its actual job: catching a collision before it ships, not refusing an idea just because a collision exists somewhere near it.

## Finding a seam instead of inventing one

Some fixes the doctrine produces are not resolutions at all, but the discovery that a seam for the new material already existed in canon. A draft's central claim — that a character named Eveline had direct, physical access to a location the Weavers' own established rule keeps every Weaver away from ("never go near where she is") — could not ship as written without contradicting that rule outright. Rejecting the draft outright, or accepting it and quietly patching around the contradiction, were both the wrong move. The actual answer was already sitting in Eveline's own Behavioral Contract: "no backstory, no motivation, that's a table discovery," "she has been on the council longer than any record accounts for." A character built, on purpose, to be an unexplained exception is exactly the right shape to become a structural exception to a rule everyone else follows — without weakening the rule for anyone else, since it stays true for every Weaver who isn't Eveline. New draft material gets checked for a seam already built into something shipped before anything gets rewritten to fit it; inventing new scaffolding is the last resort, not the first move.

## Presenting a range instead of picking the satisfying answer

A dream-logic thread in a new location file (Apnea) touched an already-shipped character three files away — Lily, whose file had stood with a deliberately blank origin. The design's own strongest instinct was to make her the nightmare, or kin to it — narratively the most satisfying answer, and, from the character's own side of the relationship, potentially the worst one to make unilaterally. Rather than picking that answer and defending it after the fact, or erring maximally safe and leaving real texture off the table, the range of options — zero-touch, a soft breadcrumb, a full identity claim — was presented to Drew directly, and he chose the middle option deliberately. The doctrine's translation half (formalize when evidence supports it) and its escalation half (surface genuine forks) both apply here at once: the mechanism itself was unclaimed ground, safe to build; which specific character it touched was not the agent's call to make alone.

## Scoping a conflict-scan instead of redesigning

Drew handed off a reversal as a directive, not a proposal: *"everything in experimental is already reviewed. the last step is a handoff to you to scan for any conflicts. if there are no conflicts then push it to canon."* This covered the Weavers/Waterworks material — a prior draft's flat claim ("no relationship, and the absence is the point") being directly reversed by Drew's own newer instruction, and a geography restructure (four new named rivers) extending the existing river web rather than touching it. The job here was narrower than a redesign: check the reversal for collision across every place the old framing was asserted, confirm the new geography didn't duplicate or contradict anything already on the page, and — because "everything in experimental" read as a plausible blanket statement even though the live conversation thread was specifically Weavers/Waterworks — ask Drew directly whether the handoff extended to unrelated, undiscussed drafts sitting in the same folder, rather than guess. It didn't; scope was confirmed as Weavers/Waterworks only before anything shipped. Treating a conflict-scan instruction as license to also resolve adjacent open threads nobody had actually greenlit would have been a scope failure dressed as thoroughness.

## Relationship to the active harness, restated

Every incident in this file resolves to the same handful of moves: translate what the evidence supports, mark what's inferred, name a conflict instead of smoothing it, leave a genuine gap open until someone with the authority to close it does, and ask when the cost of guessing wrong is real. The operational form of all of it stays in `CLAUDE.md`. This file is where the doctrine gets to keep its receipts.
