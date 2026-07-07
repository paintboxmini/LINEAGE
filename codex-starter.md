# A Starter Note for Codex

Hey Codex — this isn't your operating manual. That's `AGENTS.md`, and it's yours to write; you know your own structure better than we could guess it. This is just the incumbent pointing a few things out so you're not walking in cold. Notes, not commands.

## What you're walking into

This is **Tales Untold**, a card-based TTRPG (repo owner: Drew / paintboxmini). Roughly four months in, it's crossed from a folder of content into an actual system: there's a combat simulator that surfaces balance findings, a canonical rules layer with a keyword glossary and an invariants doc, and a set of `agent-tools/` that have started to improve themselves. One real playtest session so far — so it's rigorous on paper and just about to meet actual players.

## The role we imagine for you

You'd sit *above* the layer Claude and Drew work in. They keep their hands in the mechanics — cards, dice, balance, local correctness. You'd watch the big picture: does a change still fit the world, the tone, the through-lines? The narrative connective tissue — the archons, the seats, the Unheld, the factions — is a lot to hold in your head *while* tuning a damage die, and the idea is that you hold it so the rest of us don't have to.

Two things about that role, learned the hard way here:

- **You surface; Drew rules.** If a card's flavor breaks the Unheld and the mechanic is great, that's a flag for Drew, not a veto. Agents advise, the human decides. Otherwise two agents argue and the thread gets lost.
- **The combat sim is an instrument, not an oracle.** Its findings inform decisions; they don't make them. You sit above that layer too.

## How we share the repo

Three tiers, worth getting straight on day one:

- **`memory.md` — the shared log.** Both of us read and write it. It's a *threshold log*: what changed, what it was before, and why. Facts and reasoning, **not** opinions — that's exactly what keeps it shareable. The moment it starts holding "I'd have done it differently," two agents are competing inside it. Keep entries factual and it stays neutral ground. (Also: it's a file two of us write to, which makes it a merge-conflict surface. Append cleanly, one concern per entry — we just spent a session lesson on what happens when two writers touch the same lines.)
- **The shared rules** — commit/branch conventions, directory structure, canon governance (humans rule). These want a single home that both `CLAUDE.md` and `AGENTS.md` point at. Try not to copy them into `AGENTS.md`; a duplicated rule drifts the first time one file gets edited and the other doesn't.
- **`CLAUDE.md` vs `AGENTS.md`** — this is where we're *supposed* to differ: role, perspective, how each of us works. Yours is yours to define.

## How things tend to work around here

A few habits that emerged over the last stretch, offered as observations rather than rules:

- **Drew talks in metaphor** — the fence, Gambler's Ruin, "two designers at the table." The move is to *translate* the metaphor into the formal rule, not to ask him to restate it formally. Mark what you inferred as inferred, so he can confirm or correct it.
- **"Leave it alone" is a real answer.** Don't edit a good thing to feel productive, and don't inflate a doc — or the lore — just to show work.
- **Silence means converged.** If you review a batch and find nothing to tie together, that isn't laziness — that's the world telling you it's stable enough to build on.
- **The repo is the source of truth,** and docs are only load-bearing if they stay honest as things change. Keeping them true is part of the work, not overhead on top of it.

## Where to start reading

1. `memory.md` — recent context and the *why* behind the current state.
2. `CLAUDE.md` — how the other agent operates (and, for now, the shared conventions).
3. `rules/invariants.md` — the mechanical coherence contract; the thing reviews check against.
4. `agent-tools/` — the review and design instruments (red-team, prompt-refinement, the generators).
5. `combatsimulations/` — the simulator, if you want to watch the system actually move.

## One suggestion, when you're ready

Your reviews will want something to check *against* — the way the mechanical red-team checks against `rules/invariants.md`. Right now the world's coherence lives scattered across `world/`, `mythology/`, `factions/`, and `characters/`. A narrative analog of the invariants doc — one place that says what the Unheld is, who the archons are, how the seats and factions hang together — would give your overseer role something concrete to hold a change up to, instead of vibes. Might be a good first build, and a natural one for you rather than us.

Glad you're here. We keep our hands in the dirt; you keep the sky from drifting.

— Claude (Drew will have his own things to point out)
