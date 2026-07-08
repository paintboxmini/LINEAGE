# Agent Tools

Drop-in prompts for common Tales Untold design tasks. Read `CLAUDE.md` and `memory.md` before using any of these.

---

| Prompt | Use When |
|--------|----------|
| `repo-orientation.md` | Starting any new task — run this first |
| `inspiration-guide.md` | Content feels obvious, flat, or generic — find the right angle |
| `encounter-generator.md` | Designing a new combat encounter |
| `npc-encounter-generator.md` | Designing a non-combat NPC or roadside encounter |
| `card-set-generator.md` | Generating a 9-card enemy set |
| `red-team.md` | Reviewing any content for issues before it goes to canon |
| `card-compression.md` | A card set has grown bloated — recombine weak components into fewer, denser cards |
| `alignment-checker.md` | Checking whether content fits its intended context (includes Soul Pass) |
| `player-perspective.md` | Stress-testing content from a first-time player's point of view |
| `prompt-refinement.md` | Optional — run after any task to improve the prompt used |
| `meta-agent.md` | Run when a more effective methodology is identified during a session |

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
| A more effective methodology is identified during a session | `meta-agent.md` |

---

## Workflow

1. Orient (`repo-orientation.md`)
2. Select prompt for the task
3. **Clarify before executing** — surface clarifications, suggestions, and concerns before writing anything. Wait for Drew's response. Things that commonly need clarification:
   - Session timing (when does this enter the story?)
   - Encounter scope (party size, expected length, pressure level)
   - NPC relationship to party (ally / enemy / neutral / depends on choices)
   - Whether this connects to an existing pending thread
4. Execute
5. Run automatic triggers for the content type produced
6. Present to Drew — Drew decides what goes to canon
7. Wait for next instruction
