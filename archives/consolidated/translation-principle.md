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
