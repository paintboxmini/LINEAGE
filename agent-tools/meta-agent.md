# Meta Agent Tool

Structural oversight, methodology improvement, and session coordination. Not a content-generation tool — a system tool.

---

## Trigger

Run this tool when, during a creative session, you identify a more effective methodology — a better way to structure a workflow, a gap in an existing tool, a pattern that would improve agent performance across sessions.

Do not run this speculatively. Run it when something concrete has been learned. `prompt-refinement.md` is this tool's usual first half — it diagnoses a process bottleneck after a task; this tool is where the fix actually gets written, since it's the one with write access to `agent-tools/` and `CLAUDE.md`.

---

## Write Permissions

This tool has explicit write access to:
- `agent-tools/` — edit, add, or restructure any tool file
- `CLAUDE.md` — update conventions, directory structure, workflow rules

All other core folders follow the standard workflow: present for review, wait for Drew's approval before committing.

---

## Scope

```
Examine the following:

1. Repo structure
   - Are all directories and files cross-referenced correctly?
   - Are any memory.md entries stale, resolved, or missing?
   - Are there content gaps that would cause a future agent to work incorrectly?

2. Agent tools
   - Is the tool that triggered this run doing its job?
   - What specifically was ineffective or missing?
   - What is the minimal change that improves it?

3. CLAUDE.md
   - Does it accurately reflect the current state of the repo?
   - Are conventions, directory structure, or workflow rules out of date?

Constraints:
- Make only the changes that are warranted by what was learned
- Do not restructure for hypothetical future improvements
- Do not add process that doesn't solve a real problem
```

---

## Session Handoff

Log the methodology change to `memory.md` the same way any other threshold crossing gets logged — a new append-only entry, not a section that gets overwritten. State what the tool or `CLAUDE.md` was before, why it changed, and what it became. A separate, replaced-each-time "Last Session" section would erase exactly the before-state this log exists to keep — see `memory.md`'s own header for why append-only is the rule, not the exception, here.

---

## What This Tool Does Not Do

- Generate content (cards, stat blocks, encounters, lore)
- Make canon decisions — those belong to Drew
- Run speculatively or on a schedule
- Expand scope beyond what the session actually produced
