# Design Principles

What makes Tales Untold content well-made. Not a rule (`rules/card-glossary.md`), not a computational fact about the simulator (`rules/invariants.md`), and not a specific instance of one of these principles in action (`agent-tools/exemplars.md` exists to demonstrate them concretely, extractably). A piece of content can violate one of these and the engine won't break — it will just be weaker, less integrated, or harder to teach from. Checked by `agent-tools/red-team.md` and `agent-tools/alignment-checker.md`, not by whether the sim throws an error.

*Archived 2026-07-15 in the doctrine-layer trim, restored to living status 2026-07-23 on Drew's direct call ("pretty sure those were rock solid and should have stayed") — the "check with fresh eyes after real creative work" condition the archiving set for itself, now met.*

---

- **Mechanics exist to reflect the fantasy.** A resolution rule that produces a mechanic without a felt truth behind it is broken, no matter how clean the math is. This is the standard every new mechanic gets checked against.
- **A creature's deck is a collection of its behaviors.** The deck doesn't just enable what a creature can do — card by card, it should *be* what the creature does.
- **Ecology drives mechanics.** A creature's environment and biology generate its rules. The rules aren't picked first with fiction painted on after.
- **Encounters teach through interaction, not explanation.** A lesson lands because the player did something and felt the consequence — not because a GM explained the rule beforehand.
- **Fiction and mechanics reinforce one another.** Neither stands alone: a mechanic with no fictional reason is arbitrary; fiction with no mechanical expression is decoration.
- **Local rules emerge from the environment, not arbitrary exception.** When a place needs a special rule (the Larder Fence's barbs, Shifting Burrow's unstable ground), the rule should read as a discovered property of that place, not a bolt-on carve-out from the general system.
- **Difficulty should be precise and computable, not a vague label.** Total stats (Creature Threat Rating) replaced Early/Mid/Late for exactly this reason — see `CLAUDE.md`, Stat Blocks, for the formula.
- **A mechanic without impact doesn't matter. Meaning without mechanics doesn't either.** *(Adopted by Drew, A3 sign-off, 2026-07-18 — coined while this file was archived; moved here from `memory.md`'s Standing Reasoning, which holds the full adoption trail.)* Both halves are load-bearing: a mechanic that changes nothing about play is decoration, and a piece of fiction the system can't touch mechanically isn't really *in* the game, just described near it.

---

The Tollbird (`bestiary/tollbird.md`) is the current strongest exemplar of several of these at once — see `agent-tools/exemplars.md` for why it's worth reading, not for a template to copy.
