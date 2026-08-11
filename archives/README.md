# Archives — Scope

Archives preserve durable historical trails of the project's design. They are not current sources of truth and should not be used as working memory.

## Consolidated

`consolidated/` is the permanent home for historical design trails. These preserve the evolution of major design ideas: the problem being solved, important alternatives, failed approaches and why they failed, discoveries and counterexamples, major revisions, and the reasoning behind the resulting design.

Consolidation is not a requirement to preserve every detail, but it is also not permission to flatten meaningful history. Preserve the history that helps explain how the design became what it is.

## Retired

`retired/` is a temporary review area for artifacts that may contain valuable material before they are deleted. Review each artifact fully and extract anything that belongs in canon, memory, unresolved concerns, agent tooling/harness, or a consolidated historical trail. Once the review is complete, delete the retired artifact. `retired/` is not a permanent archive category.

## Changelogs and Worklogs

Changelogs and worklogs are source material for consolidation, not permanent archive categories. Review them for historically valuable information, incorporate that information into the appropriate consolidated trails, and delete the original changelog or worklog only after its contents have been fully reviewed and its lasting value has been preserved or deliberately rejected.

## Authority

Archives are never authoritative over current canon. When historical material conflicts with current canon, current canon wins.

The archive preserves why and how the project became what it is; it does not determine what the project is now.

---

# Archive Census — First Pass

This is an inventory classification only. **No classification below authorizes movement, deletion, or consolidation.** A `deep scan` means the artifact needs section-level review before a final archival destination can be chosen.

## Permanent / Structural

- `README.md` — **PERMANENT ARCHIVE CONTRACT**. Defines the archival lifecycle and authority rules.
- `.gitkeep` — **STRUCTURAL / LATER REVIEW**. No content value; retain only if needed for an empty directory.

## Major Historical Sources — Deep Scan Required

- `key-design-decisions.md` — **MIXED HISTORICAL SOURCE / DEEP SCAN**. Very large composite document. Do not treat it as one archival category; classify its sections individually.
- `multi-agent-notes.md` — **WORKLOG / DEEP SCAN**. Chronological records of creative and design work. Likely contains multiple consolidated design trails as well as material with no lasting archival value.

## Existing Focused Historical Trails — Deep Scan / Consolidation Candidates

- `initiative-slots.md` — **CONSOLIDATED-TRAIL CANDIDATE**. Focused history of the Initiative Slots direction, including rejected approaches and unresolved status.
- `oracle-pool-2026-08-03.md` — **CONSOLIDATED-TRAIL CANDIDATE**. Historical Oracle pool composition and selection process.
- `translation-principle-full.md` — **CONSOLIDATED-TRAIL CANDIDATE**. Historical evolution of the Translation Principle and the reasoning behind the trimmed doctrine.
- `harness-brainstorm-2026-08-06.md` — **CONSOLIDATED-TRAIL CANDIDATE**. Agent/harness design history; determine whether it belongs in a broader harness-evolution trail.
- `extraction-brainstorm-2026-08-05.md` — **WORKLOG / CONSOLIDATED-TRAIL CANDIDATE**. Raw worldbuilding development with explicit records of material already extracted into canon.
- `washedashore-brainstorm-2026-08-07.md` — **WORKLOG / CONSOLIDATED-TRAIL CANDIDATE**. Raw creative development plus extraction history and self-correction.

## Retired-Artifacts — Full Extraction Review Required

These are not assumed disposable merely because they are retired. Review them fully for valuable extraction before deletion.

- `card-set-generator.md` — **RETIRED ARTIFACT / EXTRACTION REVIEW**. Former card-generation operating prompt.
- `codex-starter.md` — **RETIRED ARTIFACT / EXTRACTION REVIEW**. Historical Codex onboarding and agent-role guidance.
- `combat-example-2026-08-06.md` — **RETIRED ARTIFACT / EXTRACTION REVIEW**. Former worked combat reference; at least one unique rule was already extracted before retirement.
- `encounter-generator.md` — **RETIRED ARTIFACT / EXTRACTION REVIEW**. Former encounter-generation operating prompt.
- `inspiration-guide.md` — **RETIRED ARTIFACT / EXTRACTION REVIEW**. Former creative-design guide.
- `npc-encounter-generator.md` — **RETIRED ARTIFACT / EXTRACTION REVIEW**. Former NPC encounter-generation operating prompt.
- `ravenhold.md` — **RETIRED ARTIFACT / EXTRACTION REVIEW**. Explicitly deprecated setting material; review only for anything that still has a legitimate home.
- `sailors-story-2026-08-06.md` — **RETIRED ARTIFACT / EXTRACTION REVIEW**. Superseded narrative scene.
- `wall-reader-coil.md` — **RETIRED ARTIFACT / EXTRACTION REVIEW**. Superseded Wall-Reader card set.
- `wall-reader.md` — **RETIRED ARTIFACT / EXTRACTION REVIEW**. Superseded Wall-Reader creature concept.
- `where-the-tracks-stop.md` — **RETIRED CONTENT / EXTRACTION REVIEW**. Former standalone encounter; determine whether any design or narrative material has lasting value.

## Classification Rules for the Next Scan

1. **Do not classify a mixed file as a whole.** When a file contains multiple historical functions, classify its sections separately.
2. **Do not move or delete from this census.** Classification precedes action.
3. **A consolidated-trail candidate is not yet a final consolidated trail.** Its contents still need review and, where appropriate, combination with related changelog/worklog material.
4. **Retired means review-before-deletion, not keep forever.**
5. **Current canon, memory, unresolved concerns, and agent tooling/harness outrank the archive when material belongs there.**
