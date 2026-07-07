# Prompt Refinement Pass

Optional. Run after completing the primary task. Reflect on the *process* that produced the work, not the work itself.

This is a feedback loop: the question is not "did I do a good job?" but "how do I make the next thousand runs better?" And silence is information — many clean runs in a row means the process has converged, which is exactly what you want to see.

---

```
After completing the task, reflect on the process itself.

If (and only if) something meaningfully reduced the quality of your work,
identify:

1. What limited your ability to produce the best result?
2. Where was the bottleneck — the prompt, missing repository context, missing
   documentation (e.g. a canonical timing or invariant reference), workflow, or
   another factor?
3. Suggest ONE concrete improvement with the highest expected impact.

Constraints:
- Suggest a change only when it would materially improve future runs.
- Prefer fixes to repository structure, documentation, or workflow OVER wording
  tweaks to the prompt.
- Do NOT suggest adding an instruction if the same problem could be solved by
  improving repository structure or documentation. A prompt that only ever grows
  is a prompt going wrong.
- Keep it concise.

If no meaningful improvement exists, return nothing. Silence means converged.
```
