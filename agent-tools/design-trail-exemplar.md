# Design Trail Exemplar — Initiative Wheel

This file is the exemplar for preserving a **consolidated design trail**: historical reasoning that explains how a non-obvious design reached its current form without becoming a chronological worklog or a second source of truth.

Use it to judge the shape and level of detail of future files in `archives/consolidated/`.

The full Initiative Wheel trail is preserved in `archives/consolidated/initiative-wheel.md`.

## What a good design trail preserves

A consolidated trail should preserve:

- the original design model;
- the problem or pressure that forced reconsideration;
- important alternatives that were genuinely considered;
- the conceptual distinction that resolved the problem;
- provisional solutions when they explain the path, clearly marked as provisional;
- what was learned that remains useful beyond the particular implementation;
- links to the current canonical and working documents.

It should **not** become:

- a chronological worklog;
- a transcript of every iteration;
- a restatement of current canon;
- a collection of unrelated findings;
- a justification for the current design that erases rejected alternatives.

The purpose is to preserve the reasoning that makes a future design decision easier to understand — not to preserve everything that happened.

## Initiative Wheel as the exemplar

The Initiative Wheel trail demonstrates the desired pattern particularly well. It begins with the original ordered model, explains why the wheel was introduced, identifies the hard problem created by a closed loop, follows the serious alternative of a linear track, then isolates the deeper conceptual discovery: **slot and count are different layers**.

That distinction explains why several attempted fixes were treating a scheduling problem as a spatial problem. The trail therefore preserves the **reasoning structure**, not merely the sequence of edits.

It also distinguishes durable lessons from provisional implementation. The historical clamp direction is explicitly not presented as final canon, while the slot/count distinction is preserved as the more durable insight.

Finally, it closes by connecting the historical reasoning back to the broader design purpose and pointing to the files that hold current authority.

## Rule of thumb

If a future designer can understand **what problem the design was solving, why the important alternatives failed or were rejected, and what conceptual discovery matters now** without reading the original worklogs, the consolidation has done its job.
