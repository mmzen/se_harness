# Proposed owner-file adoption

Status: proposed. No live owner file has been edited. AGENTS.proposed.md is the
complete proposed AGENTS.md; AGENTS.proposed.diff shows every change. These are
review materials, not additional instruction sources. Compare the retained
baseline hashes before applying an approved edit; new owner bytes need review.

| Current content | Proposed edit | Destination after adoption |
| --- | --- | --- |
| Opening managed-gate hook | Remove. | Native injection of ENGINEERING_HARNESS.md. |
| Commands | Keep setup, tests, distribution checks, CLI smoke check and source entry points. Remove governance invocations. | SETUP.md and action procedures. |
| Release sequence pointer | Keep the project build-documentation pointer. | Existing development notes. |
| Ungoverned paths | Remove the old waiver. No replacement exemption is introduced. | EXCEPTIONS.md explains the unavailable future capability. |
| Scope of the managed obligations | Remove duplicate applicability rules. | Root: Scope of these rules. |
| Locked policy and editable supplied files | Remove old ownership/installation rules; keep script locations in Source layout. | UPGRADE.md, SKILL_PROVIDER.md and resulting lock. |
| Candidate source versus released evaluator | Keep source/template/package locations. Remove evaluator setup and authority rules. | SETUP.md and current setup facts in development notes. |
| Traps | Remove PR, lifecycle, ID and evidence-history rules. Keep preservation of unrelated changes. | PULL_REQUEST.md, DRAFT_DEFINITIONS.md, VERIFY_OUTCOME.md, RELEASE.md and RECORD_STATE.md. |
| Change and verification constraints | Keep boundary tests, untrusted-input handling, owner-content preservation and domain-index location. Remove authority and formal-policy restatements. | RELEASE.md and root invariants. |
| Software engineering harness block | Released installer retires only recognized managed bytes with reviewed native evidence. | Injected root and conditional procedures. |

Guide names above are below docs/engineering/harness/. No harness governance
instruction is moved into another section of AGENTS.md.

CLAUDE.md contains only the recognized harness block. The installer may remove
it when retirement leaves no owner content. If owner content appears, preserve
it and reassess the proposed removal.

The root stays on 0.18.0 during preparation. The installed plugin is still
0.1.0. Assembling a 0.2.0 package does not install it or prove native delivery.
Review real startup and post-compaction traces of the exact planned root before
removal approval. Previous demonstration traces refer to other roots.
