# Canon Gate — Authority

The Canon Gate determines **who may commit a change**, not how important or difficult the change is. Authority and interpretation are separate questions; Translation Principle governs interpretation.

## Authority Levels

### Authority 1 — Established Language

The change uses existing canon without changing its meaning: encounters, creatures, NPCs, cards built from established mechanics, prose improvements, and similar work.

**Agent authority:** may integrate after the required review pass is clean.

### Authority 2 — Canonical Extension

The change adds new content without redefining existing canon: new faction behavior, regional customs, a new map Seat, a deepened NPC, and similar extensions.

**Agent authority with audit:** may integrate when the extension fits current canon. An extension may add to an established theme but may not redirect its meaning. If it would change established meaning, escalate it as constitutional rather than silently executing it.

### Authority 3 — Constitutional

The change alters the language itself or changes how established content is interpreted: formulas, keywords, progression, cosmology, core Design Principles, contradictions of established canon, or other world-level changes with downstream interpretive effects.

**Drew's authority:** surface the issue and wait for explicit direction. Do not commit the constitutional change on agent authority.

A3 observations do not need a standing recommendation queue. Raise them in conversation. If an unresolved A3 issue has lasting value, preserve it in `unresolved-concerns.md`.

## Review and Integration

Approved work is presumed ready for integration. The agent's responsibility is to integrate it cleanly and catch genuine risks, not repeatedly relitigate creative approval.

Every Authority 1/2 ship gets one entry in `changelog.md` — the navigable record of what changed and why, one of the repository's six layers (`CLAUDE.md`, Repository Layers). At the top, newest-first, the moment it lands — not staged elsewhere first. Distinct from `archives/`: the changelog entry records that something changed and why; if there's a real reasoning trail behind it worth preserving, that goes to `archives/` directly, not folded into the changelog entry itself.

Experimental content must be checked against current canon before shipping. A same-file read catches internal inconsistency; a repository-level read catches conflicts with established identity, reopened closed threads, duplicated facts, or changes that affect other systems.

Escalate when there is a:

- canonical conflict;
- genuine ambiguity that changes the result;
- propagation or dependency problem;
- constitutional change; or
- uncertainty about the appropriate authority level.

Mechanical integration should remain mechanical. Semantic conflicts and constitutional changes require judgment.

## Current Authority Test

When deciding whether a change may ship, ask:

1. Does this merely use established language? → **A1**
2. Does it extend canon without redefining it? → **A2**
3. Does it change the language or how established content is interpreted? → **A3**

When uncertain between levels, do not silently choose the lower authority. Surface the distinction.

The historical evolution of this model is preserved in `archives/consolidated/canon-gate.md`.