# Agent Prompts

Drop-in prompts for common Tales Untold design tasks. Read `CLAUDE.md` and `memory.md` before using any of these.

---

| Prompt | Use When |
|--------|----------|
| `repo-orientation.md` | Starting any new task — run this first |
| `encounter-generator.md` | Designing a new combat encounter |
| `npc-encounter-generator.md` | Designing a non-combat NPC or roadside encounter |
| `card-set-generator.md` | Generating a 9-card enemy set |
| `red-team.md` | Reviewing any content for issues before it goes to canon |
| `alignment-checker.md` | Checking whether content fits its intended context (includes Soul Pass) |
| `player-perspective.md` | Stress-testing content from a first-time player's point of view |
| `prompt-refinement.md` | Optional — run after any task to improve the prompt used |

---

## Automatic Triggers

These prompts are not optional when their trigger condition is met. Run them without being asked.

| Trigger | Prompt |
|---------|--------|
| Start of any session or new task | `repo-orientation.md` |
| Any card drafted (before presenting) | `red-team.md` |
| Any encounter or quest content drafted | `red-team.md` (Quest/Encounter pass) |
| Any content touching an existing location, faction, or NPC | `alignment-checker.md` |
| Any content that will be presented to Drew for canon approval | `alignment-checker.md` + Soul Pass |
| Any new NPC with a combat role | `player-perspective.md` |

---

## Workflow

1. Orient (`repo-orientation.md`)
2. Execute (select prompt above)
3. Run automatic triggers for the content type produced
4. Present to Drew — Drew decides what goes to canon
5. Wait for next instruction
