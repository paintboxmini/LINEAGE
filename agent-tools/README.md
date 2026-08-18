# Agent Tools

---

| Prompt | Use When |
|--------|----------|
| `repo-orientation` | read when working on canon |
| `compiled-crib.md` | Practical efficiency tool — read INSTEAD of full canon for routine generation; refresh when canon shifts |
| `red-team.md` | Reviewing any content for issues before it goes to canon |
| `archetypes.md` | Building a new card — a design compass, not canon; never surfaces at the table |
| `design-principles.md` | What makes content well-made — the standard red-team and alignment checks measure against |
| `alignment-checker.md` | Verifying new content fits its intended context, plus the Soul Pass and Finding the Angle for when it reads flat |
| `card-creation.md` | Creating or editing a card |
| `npc-and-creature-creation.md` | Creating an NPC or creature |
| `name-price-distance.md` | Building a person, place, or thing — applying the three Cuts |
| `finding-a-voice.md` | Giving a named person real interiority — belief, wound, refusal |
| `player-perspective.md` | Stress-testing content from a first-time player's perspective before it reaches the table |

---

## Executable checks

Not prompts — programs. These fail loudly, which is the point: a prose invariant
nobody runs reads exactly like coverage.

| Tool | Use When |
|------|----------|
| `verify.py` | Before every commit — the full acceptance pass, all repo-wide invariants |
| `conserve.py` | Either side of a restructure — snapshot before the move, check after; catches content lost or duplicated in transit |
| `keyword-usage.py` | Recount how many cards use each keyword; regenerates `keyword-usage.md` |
| `invariants.md` | Index of what is enforced, by which check, and what is stated but unchecked |

---

## Automatic Triggers

| Trigger | Prompt |
|---------|--------|
| Any card, encounter, or quest content drafted (before presenting) | `red-team.md` |

---

## Workflow

1. Orient (`repo-orientation.md`)
2. Do the work — read the relevant canon, think it through, write it
3. **Clarify before executing** when something is genuinely ambiguous (see `CLAUDE.md`, Agent Workflow step 3) — not by default, only when the evidence doesn't pick a side
4. Run `red-team.md` on anything going to canon
5. Apply the current Canon Gate in `CLAUDE.md`
6. Present the finalized result and await the next instruction
