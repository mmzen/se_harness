# Remaining plugin work after the KISS changes

Two useful implementation jobs remain: connect and maintain a project, then provide
a guide checked against actual host use. Optional helpers stay deferred.

The owner requested this revision after merging WO-KIS-009. Baseline: main
`cc03b381f7d80eaf7f79da90f0dab8c462434a61`. [WO-PLG-022](../engineering/plugin-integration/work-orders/WO-PLG-022.md)
governs the amendment. This is planning work; the future implementation packets stay draft.

## Disposition of the five old packets

| Old packet | Decision | Useful outcome kept | Unnecessary obligation removed |
| --- | --- | --- | --- |
| WO-PLG-009 | Rewrite | Connect new/existing projects through the existing setup and installer; check the result. | Edited generated-skill conflicts, plan binding, ownership signatures, obsolete adopt route, DEC-PLG-004 prerequisite. |
| WO-PLG-013 | Absorb into 009 | Repair the checker; keep the selected project version unless an upgrade is requested. | Empty replacement environment, activation switch, repeated identity/receipt proofs, separate maintenance workstream. |
| WO-PLG-014 | Defer and narrow | A genuinely read-only helper, if a concrete future task justifies it. | Speculative helper framework, host/credential/spawn matrix and automatic dependency on helpers. |
| WO-PLG-015 | Absorb useful checks into 016 | Check actual discovery/use; report observed delay or unnecessary prompts. | Mandatory performance baseline, cold/warm matrix, numeric launch threshold, DEC-PLG-005 prerequisite and a dedicated CI workflow. |
| WO-PLG-016 | Rewrite | A short guide with truthful development/release and host claims. | Hook activation, repair-by-environment-swap, local authority ceremony and blocking all guide work until a release decision. |

WO-PLG-009/013/015/016 existed only in the unmerged umbrella PR #416, inspected at
`17382d8e7f7a5709f4f55facfe875fbf455e5794`. This branch imports only the rewritten
009 and 016 chains. Do not later merge the obsolete 013/015 contracts or open draft
DEC-PLG-003/004/005 as new prerequisites. Their IDs remain historical proposal IDs;
they are not reused for new work or marked implemented without execution.

The old REQ-PLG-022/023 maintenance outcomes now fall under REQ-PLG-015 and the
already approved REQ-PLG-035. REQ-PLG-025's useful host observations fall under
REQ-PLG-027. REQ-PLG-026's compulsory timing/prompt baseline is dropped; only an
observed problem warrants further measurement. Those four old drafts are not imported.

## Coherent requirements and checks

| Current chain | Definition of done |
| --- | --- |
| REQ-PLG-015/016 → SPEC-PLG-009 → VER-PLG-009 → WO-PLG-009 | Existing operations connect and maintain small projects, retain version choice and preserve unrelated files. Three outcome groups reuse current safety tests. |
| REQ-PLG-027 → SPEC-PLG-016 → VER-PLG-016 → WO-PLG-016 | The guide matches an actual walkthrough of each claimed host route, has useful failure guidance and states availability honestly. Three checks, no benchmark project. |
| REQ-PLG-024 → SPEC-PLG-014 → VER-PLG-014 → WO-PLG-014 | Conditional read-only behavior only. No implementation until a useful task and bounded scope are selected. |

The approved helper requirement remains conditional. Its specification/verification
bodies now carry the dated owner-directed prospective amendment; original approval
events remain unchanged. Its draft work order no longer includes speculative runtime
paths. All historical VREC/RLS files and bound evidence remain untouched.

## Alignment with every accepted simplification

| Accepted work | Application to this remaining plan |
| --- | --- |
| WO-PLG-021 | Replace disposable skill copies, repair one environment, use explicit checks, and reuse simple packaging. |
| WO-KIS-001 | Plain instructions and ordinary paths/input; no exact prose, receipt-header or scoring requirements. |
| WO-KIS-002 | Local evidence supports local work; no live-CI authorization, dashboard dependency or unrelated-change blocker. |
| WO-KIS-003 | Use actual checker origin/version; no extra interpreter hashes, activation receipts or machine-path binding. |
| WO-KIS-004 | Identify the tested candidate and relevant evidence; reuse unchanged results instead of rerunning everything after harmless changes. |
| WO-KIS-005 | Use existing package/release jobs at their proper boundaries; no plugin-only rehearsal or qualification pipeline. |
| WO-KIS-006 | One concise summary with usable result references; no copied repositories/per-case archives, no deletion of old evidence. |
| WO-KIS-007 | Test user outcomes and actual failure boundaries; remove synthetic permutations and internal call/spawn inventories. |
| WO-KIS-008 | Start from the useful outcome and simplest adequate design. Explain material complexity in ordinary artifacts; add no KISS gate or score. |
| WO-KIS-009 | One execution route, no delegation toggle or repeated routine permission. Preparation does not make the assurance decision. |

The shared wording and questions remain in the candidate
[ARTIFACT_AUTHORING.md](../../templates/repository/standard/docs/engineering/ARTIFACT_AUTHORING.md).
This note applies that policy; it does not create a second plugin-specific policy.
More complex work can still be justified by a real need or credible risk. The current
request provides neither for a helper framework or universal performance matrix.

## Useful protections retained

Confirm replacement input before deleting disposable copies. Do not write outside
the selected target or overwrite unrelated owner content. Keep project-version
changes explicit and retry actual failed operations. Use the selected governing
checker and real package checks at installation/publication boundaries. Claim only
the host behavior and release availability actually established by evidence.

## Execution order and release boundary

First approve and execute the rewritten WO-PLG-009. Then use its settled instructions
in WO-PLG-016. Keep WO-PLG-014 deferred. Development work can use clearly labeled
disposable fixtures; it need not wait for public publication. A public-install claim
needs an actual selected release and walkthrough. Live project changes need their
named target/action authorization. No release or host installation is performed here.

The current root still uses released 0.17.0. Until the merged KISS implementation is
released and adopted, obey that evaluator's actual commands; do not pretend that
editing prospective work orders upgraded it. Future packets describe the accepted
single route without restoring the old optional delegation or base/CI gate.
