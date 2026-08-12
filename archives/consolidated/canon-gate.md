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

The 2026-08-06 harness brainstorm captured the desired direction explicitly: routine changes should integrate automatically, structurally risky changes should open review, and constitutional changes should require Drew. fileciteturn146file0

## Review remains real

Presuming integration does not mean skipping review.

Experimental content still has to be read against current canon before shipping. A same-file read can catch internal inconsistency; only a repository-level read can catch a closed thread being reopened, an established identity being mutated, or a newly invented fact duplicating something that already exists.

The review therefore became **targeted rather than universal**: spend expensive reasoning where the repository actually presents a risk.

## The current model

The mature Canon Gate is therefore a jurisdictional integration system:

1. Determine what kind of change this is.
2. Translate the request without silently redefining it.
3. Check it against current canon.
4. Integrate ordinary approved work.
5. Escalate genuine conflicts, ambiguity, propagation failures, or constitutional changes.
6. Reserve constitutional authority for Drew.

The result is not a weaker gate. It is a narrower one: the agent is responsible for **clean integration and zero silent regressions**, not for repeatedly re-litigating creative approval.

## Provenance

The principal historical source for this evolution is the 2026-08-06 harness brainstorm, which proposed explicit Intake → Integration → Arbitration phases and a presumption of integration. fileciteturn146file0

The current authority model is recorded in `CLAUDE.md`; this file preserves the reasoning trail that explains how that model emerged.
