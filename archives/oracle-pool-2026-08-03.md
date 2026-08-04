# Oracle Pool — Archived 2026-08-04

Moved here from `Oracle/baseoracledeck.md` verbatim, at Drew's request: the mechanic stays (the shared starter pool players draft from at character creation and draw from at end of session — `CLAUDE.md`, `README.md`), but the populated 63-card list is going away. Drew is building the actual pool by hand from the core sets, right before Session 1, rather than using this AI-selected composition. `Oracle/baseoracledeck.md` now holds only the mechanic's rules (eligibility criteria, the 12/6/3 range-composition target) and points here for the reasoning trail behind everything that was tried.

This file is preserved exactly as it stood the moment it was archived — including every pass's own reasoning, every cut, every swap. Not a current-state reference; a record of one specific, fully-worked composition that got built and then set aside, useful groundwork if Drew wants to crib from it rather than start from nothing.

---

Cards available in the Oracle pool for this campaign. At end of session, GM draws 3 — active player picks 1.

---

## Current Pool

Starter tier — simplest, lowest power/impact cards from the three core sets. Each card touches one of the three core pillars (RPS, Initiative, Position) or a standard keyword; none force the opponent to discard, inject a status (Wound/Exhaust), force a hand reveal, or presuppose a system (Anchored, an RPS auto-win/reversal, a precondition set by another card, an open-ended amount choice) the pool doesn't otherwise introduce. All core cards — `cards/red-body.md`, `cards/blue-mind.md`, `cards/green-soul.md`. Selection trail: `memory.md`.

**Fixed composition (2026-08-03, Drew): 21 per colour, split 12 / 6 / 3 along that colour's range identity.**

| | 12 | 6 | 3 |
|---|---|---|---|
| **Red** | Melee | Both | Ranged |
| **Blue** | Ranged | Melee | Both |
| **Green** | Both | Ranged | Melee |

These are exact counts, not a lean. Any card entering or leaving the pool has to keep all nine cells true; `combatsimulations/content.py`'s `ORACLE_DECK` carries the same list and is checked against these numbers.

**Red** (21)
- ATTRITION
- BLINDSIDE
- BLOOD IN THE GAP
- CHARGE
- CLIFF SONG
- EMERGENCY REPAIRS
- ENDURE
- FOOTWORK
- GROUNDING STANCE
- GUARD
- INTERCEPT
- OPEN GUARD
- PAIN IS FUEL
- PULL
- PUSH
- RECOVER
- REELING
- SLIP THE BLADE
- STARING CONTEST
- UNBROKEN
- WEATHERED

**Blue** (21)
- ANTICIPATE
- AXIOM
- CALCULATE
- DEAD END
- DEFLECT
- FOCUS
- FORESEEN
- HESITATE
- LAST RESORT
- MARKED
- PREDICT
- PROFILE
- REALIGNMENT
- REFRACT
- RETORT
- SECOND GUESS
- SHARPEN
- SIDESTEP
- STUDY
- TELL
- VEIL

**Green** (21)
- ACCEPTANCE
- BALANCE
- BIND
- BRAMBLE
- COMMUNION
- DEAD RECKONING
- DUST
- GIVE WAY
- INSTINCT
- LEVEL THE FIELD
- MIRROR STEP
- MOCKERY
- OPENING
- QUICKEN
- RENEWAL
- RESONATE
- SETTLE
- SUPPORT
- SWAY
- UNTOUCHED
- YOU'RE NEXT

FORESEEN and STEADFAST are new (2026-08-01) — plain, unconditional Resist both sides, filling a real gap: neither color had a clean self-Resist grant before (`memory.md`). WARSONG cut (2026-08-01) — its Effect duplicated RESONATE's verbatim ("All allies gain Deadly").

**Keyword-coverage pass, round 1 (2026-08-01):** OPEN GUARD, MARKED, OPENING grant Vulnerable to the foe — one per color, filling the pool's starkest gap (Vulnerable was at zero anywhere in the Oracle before this). UNBROKEN and UNTOUCHED match LAST RESORT's exact shape ("if your HP is 6 or less, gain Immunity") in the two colors that had no Immune grant at all.

**Keyword-coverage pass, round 2 (2026-08-01):** ATTRITION (Weak), REELING (Staggered), FOOTWORK (Quick), BLINDSIDE (Blind) close every keyword Red had at zero. RETORT (Thorns), VEIL (Blind), DEAD END (Rooted) do the same for Blue. BRISTLE (Thorns), INSTINCT (Ward) close Green's last two. **BRACE cut** — Resist was at 10, 6 of them Red; BRACE was the most purely-redundant (PAIN IS FUEL pairs Resist with Thorns, BRACE was Resist and nothing else).

**Slimmed back to 60 (2026-08-01)** — the pass above grew the pool to 72; re-trimmed to 20/20/20, cutting only from the pre-coverage-pass cards (every keyword-coverage card from both rounds above is untouched). Cut: DART, PUSH, GROUNDING STANCE, INTERCEPT, RALLY (Red — RALLY specifically for its 5 HP cost, steep for a starter; the rest for redundant movement/Resist already covered elsewhere in Red); UNDERSTANDING, CLIMB, PARTITION, ALIGN (Blue — UNDERSTANDING for quietly outpunching its Blue peers, d8 plus a guaranteed +1d6; the rest for being the least-essential utility picks); FLOW, ACCEPTANCE, DELAY (Green — DELAY specifically chosen over HEAVE AND HAUL despite both being Initiative-adjacent, since HEAVE AND HAUL is Green's only Quick source and cutting it would have reopened a gap this same pass just closed). Full reasoning and final per-keyword counts: `memory.md`. All 8 cards with "Target gains X" wording (OPEN GUARD, MARKED, OPENING, ATTRITION, REELING, BLINDSIDE, VEIL, DEAD END) corrected to "Defender gains X" / "Attacker gains X" — the code was always bound to the current RPS opponent, never a free choice of target; the wording was simply wrong.

**HEAVE AND HAUL replaced by EDDY (2026-08-01)** *(EDDY was renamed **SWAY** on 2026-08-03 — this entry keeps the name it had on the day, since that is what happened.)* — the exact card the entry above worked hard to keep turned out to be too strong for a starter pool after all: all-enemies forced movement plus a team-wide free Quick, stacked on one card. It keeps the niche (Green movement manipulation) and Green's one working Quick source, scaled to starter level — single-target reposition, Quick moved to its own self-only line, d4 instead of d8. HEAVE AND HAUL itself is untouched everywhere else in the pool. Full reasoning: `memory.md`.

**REPEL replaced by PUSH (2026-08-01)** — same shape of problem as HEAVE AND HAUL: REPEL's Effect and Defensive Bonus were both the same unconditional all-enemies-to-Backline function, no differentiation between the two sides at all. PUSH — cut in the original slimming pass above as redundant with REPEL, no longer true once REPEL is the thing leaving — is the exact single-target sibling this pool should have had: PULL's own directional counterpart, already core-legal, no new card needed. Full reasoning: `memory.md`.

**Fixed to 12/6/3 (2026-08-03)** — Drew set the counts; card selection was mine. The pool went 60 → 63.

*Seven new cards, because two slices could not be filled from core.* **Blue melee** needed 6 and the entire colour had 3 (PREDICT, DEFLECT, ANTICIPATE) — hence **HESITATE**, **TELL**, **SECOND GUESS**. **Green Both** needed 12 and ran out of candidates clearing the bar above — hence **SETTLE**, **GIVE WAY**, **BRAMBLE**, **QUICKEN**. The Green four are deliberately the coverage the Green melee cut displaced (STEADFAST's Resist, SHADE AWAY's Evade, BRISTLE's Thorns, URGENCY's Initiative), re-homed from Melee into Both — which is where Green's identity now says that coverage belongs.

*Cuts made on the eligibility bar, not just on counts.* **EQUAL FOOTING** (Red), **CERTAINTY** (Blue) and **ADAPT** (Green) all carry *"Wins ties"* — an RPS auto-win, which this pool's own criteria exclude. They were a deliberate one-per-colour trifecta and they left as a set; all three remain untouched in core. **RETALIATE** (Red) and **REBUTTAL** (Blue) both key off "if an enemy attacked successfully on the turn immediately before yours" — a precondition set by another turn. **INTERRUPT** cut for turn denial, **TRAMPLE** for granting an extra action, **GAMBLER'S RUIN** for exploding dice. Green's melee cut to 3 keeps one clean keyword grant each: BIND (Rooted), DUST (Blind), OPENING (Vulnerable).

*Previously-cut cards returning.* **PUSH, GROUNDING STANCE, ACCEPTANCE** and **DART**'s slot-mates were trimmed in the 2026-08-01 slimming for redundancy at a 20-card pool. Red Both is only nine cards deep in core and several fail the bar, so RECOVER, CLIFF SONG and GROUNDING STANCE come back to fill it. That is the counts binding, not a reversal of the earlier reasoning.

**GORE swapped for INTERCEPT (2026-08-03).** GORE's own bug got fixed the same day — Range Melee → Both, since as Melee its *"if target is Frontline"* condition checked something Melee's own legality already guaranteed, so the bonus fired unconditionally every time. Full reasoning: `memory.md`. Fixing it broke this pool's Red Melee-12, so GORE left as a set member and **INTERCEPT** took its slot: `Body + d4`, *Gain Protect and Resist 2* both sides — a pure double-keyword grant, the same shape as GUARD and PAIN IS FUEL already in the pool. Count and composition unchanged.
