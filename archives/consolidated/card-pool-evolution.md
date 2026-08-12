# Card Pool Evolution — Design Trail

## What this trail preserves

This is the historical evolution of the card pool's shape: how deck-building conventions were first set, how the tag convention unlocked a tool for compressing a mature card set, how two compression passes thinned the core sets without losing expressive power, and how range distribution became a deliberate expression of each color's identity rather than an accident of individual card design.

The current card sets are authoritative elsewhere (`cards/`, `rules/cards.md`, `rules/card-glossary.md`). This file preserves the reasoning trail, not the current card list.

## Starting conventions

The earliest deck-building conventions (canonical home: `rules/cards.md`, Deck Building) set the baseline everything below works against: player deck color counts match stats (Mind 4/Body 2/Soul 3 → 4B/2R/3G) as a heuristic, not a law; enemy decks run 3 themed signature cards plus 4–7 core cards (7–10 total), leaning toward the creature's stat spread; enemies draw to hand size like players. Tie-counts-as-successful-defense was deliberately ruled per-card rather than universally — WITNESS says so on its own card, and any new card referencing "successful defense" has to carry its own clarifying line until, or unless, the convention gets promoted to a universal rule.

Signature sets got their own standing loop at the same time: creature combat decks are filled from core cards, and signature cards are Oracle rewards. Drew determines how many signature cards land in a given set only after reviewing the full nine. The standard shape: draft nine, red-team all nine, fix/cut/replace until all pass, present all nine, Drew decides placement.

## The tag convention, and the tool it enabled

Tags started as an unbounded set — every concept in the world (locations, factions, each Seat, the Unheld, Echo) was becoming a tag, and Drew cut them back from the core. The resolution: **a tag marks a card's acquisition source, not its theme.** Source can be a location, an archon, a faction, a creature, the Unheld — anything you can trace acquisition to. At most one tag per card; core cards carry none; a tag is never a theme (theme lives in the flavor line). The test: "does removing the tag change how the card is obtained?" Loose Grip was the proof case (UNHELD = source, "stop fighting the wheel" = theme-in-flavor, not tag-worthy).

That decomposability — mechanic, name, flavor, and source as four cleanly separable strands — is what made the cards analyzable as recombinable genes, and it directly enabled a new tool: **Card Compression Pass** (`agent-tools/card-compression.md`). The tool treats each card as four genes, scores components across the whole set rather than judging cards holistically, finds the weakest genes, and proposes recombinations that cut card count while preserving or increasing expressive power — nothing deleted, only rehoused. It's the constructive sibling of red-team: same Relevance/Identity/Evolution judgments, opposite purpose (recombine strengths instead of finding flaws). A maturity tool, meant to run when a set is bloated, not on a young one.

## First compression pass: the core set, 98 → 92

The core set had grown to roughly 98 cards (Red 34 / Blue 31 / Green 33) — mature enough to compress. Drew accepted all six proposed merges:

- **URGENCY ← Route-Song** (green): Route-Song's effect was identical (Init Shift +3 to ally); its −3-attacker defense became a choice on Urgency's defense (+3 self OR −3 attacker). Route-Song's name and flavor banked.
- **SUPPORT ← Conduct** (green): identical empower+draw; Support unchanged, Conduct deleted. Conduct's d6/"finds its rhythm" banked.
- **ALIGN ← Insight** (blue): two scry-color-gambles became one card with a choice payoff (draw or +4 damage). Drew bumped the scry from 2 to 3 ("if any two share a color"). Insight's distinct party-color-shield defense was banked as a real gene with no home in the scry identity.
- **INTERCEPT ← Fortress Stance** (red): kept Intercept's redirect-and-defend, took Fortress's "all allies +2 HP" as the defense. Fortress's "walls in flesh" flavor banked.
- **MIRROR STEP ← Spiral Current** (green): kept move-both, took Spiral's Quick-granting defense. Spiral's "water teaches stone to dance" flavor banked.
- **FOCUS ← Excavate** (blue): Excavate's recursion became Focus's defense; Excavate was the weakest card in the set.

All retired names, flavor, and mechanics were preserved rather than deleted, for possible reuse later. This was the tool's first real outing, and it worked.

## Second compression pass: the scry cluster

Scry had spread thin as an early-development goto — a card needed a second effect, scry was safe filler — and the sim had already shown deck-reorder to be roughly combat-neutral. The direction: fewer scry cards, and make the survivors pull weight by pairing scry with guaranteed value (a draw, a real effect), since reorder-only was what underperformed.

Applied to blue (29 → 28):

- **ANALYZE cut.** Its team-scry-2-plus-reveal-hand was low-value on both halves; "reveal opponent's hand" banked.
- **PROFILE buffed**: "Scry 2" → "Scry 2, then draw 1," carrying real card advantage now.
- **ANTICIPATE buffed**: "each time attacked, Scry 2" → "the first time attacked, Scry 2 and draw 1," a bounded reactive dig-plus-draw.
- **Rider trim** on background scry filler: PREDICT's defense became "negate attacker's next item use" (mirrors its item-denial identity); SLIPSTREAM's defense became "Gain Evade"; **AXIOM's defense swapped from scry-2 to a mirror-ban** ("name a color, attacker can't play it next reveal").

That last swap moved the sim measurably (duel Steele 63.2% → 56.8%, team B 64.6% → 62.0%) — turning Axiom's scry rider into a real, modeled tempo denial made it a genuine control card. Drew's call: keep the mirror, try it out.

**The differentiation queue, and its resolution.** In the same breath, Drew named a design preference in passing: a card's Effect and Defensive Bonus should not be too similar — a card whose two sides do the same thing is one-dimensional. AXIOM's rider swap had just made both its sides mirror-bans, so it joined a differentiation queue for a future pass, alongside **ALIGN** (whose effect and defense were already flagged as too alike during the first compression pass) and **RALLY** (frontline+2 / backline+2 — the same effect, position-flipped). The queue sat unactioned from the second compression pass through today.

**Resolved 2026-08-12 — Drew's answer: "drop."** The differentiation queue for Axiom, Align, and Rally is closed without action. This is not a deferred task waiting for a future compression pass; it's a closed queue. If any of the three gets touched again, it will be for its own reasons, not because of this old flag.

## Expansion: +21 cards, new engine hooks

The set later grew the other direction — Drew added 21 cards in an even split with a team-play focus, bringing the total to 55 real cards (19B/18R/18G). This introduced genuinely new engine hooks rather than just filling out existing ones: Armour (flat reduction, clears next turn), can't-defend (Interrupt), team Intercept (an ally steps in to defend, Battle-only), Fortress damage-shield, AoE splash (Chain/Trample), ongoing support ticks (Synchrony team heal, Rooted Oath anchored buff), and a Patience "did I wait" flag. All ally effects route through the shared `engine.allies`/`_team` machinery — inert in 1v1, live in Battle.

## Range identity becomes deliberate — and one early instinct about it was wrong

Range distribution eventually became a hard structural constraint on the Oracle pool (see `archives/consolidated/oracle-pool.md` for that composition's own history) and, following from it, on the core sets too. But the path there included a real reversal Drew named directly, months earlier:

**The flawed "new player friendliness" premise.** Drew had once leaned the core set toward Both range specifically to make onboarding easier for new players — a range that's never illegal removes one more thing to track. Looking back at it: *"I remember I also told myself that having the core set lean on the both range was a way to introduce new players, but I'm seeing that reasoning was totally flawed."* What it actually did was flatten all three colors toward the same safe default — Both didn't just gently lean, it dominated every color's pool — and for Green specifically it inverted the incentive it was meant to protect: the flexible, always-legal range ended up carrying a *higher* average die than either restricted range, meaning the "easy" choice was also the objectively better one, no tradeoff at all. Onboarding ease and mechanical correctness turned out not to be the same axis, and optimizing for the first without checking the second trained new players toward degenerate play instead of away from it. The fix didn't remove the safety net — Both stayed real and available everywhere — it just stopped being the best answer by default.

**Core sets re-ranged toward the Oracle's 57/29/14 shape.** Once the Oracle pool's own 12/6/3 composition existed, Drew extended the same idea to the core sets, but as a rough metric rather than an exact quota: *"for the core set it a rough metric to aim for. we need to bring it closer by going through and changing cards that can support it thematically."* The target became the Oracle's own percentage shape (57/29/14), scaled to each color's actual size, not a literal 12/6/3 — Green's Both pool didn't have enough clean candidates to hit an exact quota any more than the Oracle's had. Every move was a re-range of an existing card, chosen because its own fiction and mechanics survived the new range — never a card built to fit a slot. Final shape landed within a couple of points of target across all three colors:

| | Primary | Secondary | Tertiary | n |
|---|---|---|---|---|
| Red (melee-lean) | Melee 30 (57%) | Both 15 (28%) | Ranged 8 (15%) | 53 |
| Blue (ranged-lean) | Ranged 24 (57%) | Melee 12 (29%) | Both 6 (14%) | 42 |
| Green (both-lean) | Both 26 (58%) | Ranged 13 (29%) | Melee 6 (13%) | 45 |

Twenty-one cards moved in total (Red 5, Blue 6, Green 10). A hard mechanical exclusion was caught before it became a candidate: no card carrying Rushdown or another Frontline-only mechanic was ever eligible for Ranged, because a Ranged card gates itself out of a Frontline-only effect by construction.

**Three red cards re-ranged; SEISMIC REDIRECT rejected as self-gating.** Drew set the counts directly: *"2 red cards needs changed to ranged. and 1 to both."* Red was the most range-locked color at 72% Melee against Blue's 74% Ranged. **SEISMIC REDIRECT was the obvious pick and was wrong** — its Effect is Rushdown, and Rushdown requires the user to be in the Frontline; a Ranged card can only be played while *not* in melee range, so the card would have gated itself out of its own effect. Caught by reading the keyword rather than the card name. REPEL was rejected for the inverse reason — "all enemies must move to backline" is about opening a gap, so as Ranged it could only be played once the gap already existed; fiction pointed at range, mechanic pointed away from it. STARING CONTEST, RHYTHM BREAK, and ROLLOUT were the three that actually moved, each surviving both the fiction test and the keyword test.

**The Immunity trifecta split by Range, per color convention.** Drew: *"blue ranged, red melee, green both"* → *"make the split."* LAST RESORT went to Ranged, UNBROKEN to Melee, UNTOUCHED stayed Both. All three had printed Range: Both, word-for-word identical text otherwise — a coverage pass artifact from putting an Immunity grant in every color. This surfaced that the color-range convention was real for only two colors at the time (Blue measured 74% Ranged, Red 70% Melee) while Green had no range identity at all (39%/37%/24%) — "green both" was new rather than existing practice.

**Die philosophy overrides trifecta uniformity.** The same trifecta had all printed d8, which read as plausible parity — same card in three colors, identical text inviting an identical die. Drew's answer settled the general rule: *"give them the traditional 4/6/8 spread."* When a trifecta's uniformity collides with d6-Mind / d8-Body / d4-Soul, the stat spread wins. Only two cards moved (UNBROKEN was already correct at Body+d8); LAST RESORT went d8→d6, UNTOUCHED went d8→d4. The next trifecta doesn't need asking — the spread always holds.

## Loose Grip's unstated target

Loose Grip (`cards/unheld.md`) is card zero of the Unheld tag — the first UNHELD card, founding the file. Its Effect reads "Initiative Shift +2," and the target was never explicitly stated on the card. It reads as SELF per the flavor text, but was never confirmed in canon or wired into the sim.

**Resolved 2026-08-12 — Drew's answer: "designed gap."** This stays an intentional unstated target, not a bug to fix. The card is not missing a specification; the ambiguity is the design.

## Durable design lessons

- Decomposing a card into separable strands (mechanic / name / flavor / source) is what makes a mature set compressible — the tag convention's real payoff turned out to be structural, not just organizational.
- Compression is not deletion: retired mechanics, names, and flavor are banked for reuse, not discarded.
- A card whose Effect and Defensive Bonus do the same thing is one-dimensional; flagging that is cheap, but a differentiation queue can sit closed indefinitely once nobody chooses to act on it — that's a legitimate outcome, not an oversight.
- Range distribution can be an explicit expression of color identity rather than an emergent statistical result, but reaching that required first discovering that flattening range toward "always legal" for onboarding's sake was actively counterproductive.
- When a uniform trifecta collides with a fixed stat-die spread, the spread wins — this generalizes past the one trifecta it was ruled on.
- An unstated detail on a card is not automatically a gap to close; sometimes the absence is deliberate and confirming it in either direction would foreclose something the design wants left open.
