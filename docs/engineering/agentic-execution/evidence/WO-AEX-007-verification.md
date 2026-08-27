# WO-AEX-007 implementation evidence

This file records the implementation handoff checkpoint for `WO-AEX-007`.
It is implementer-generated evidence, not an assurance decision, verification
record, lifecycle transition, candidate-commit authorization, release decision,
or activation of Phase 4. The work order remains `in_progress` at this
checkpoint and requires later independent commit-bound verification.

artifact: WO-AEX-007
checkpoint: handoff
formal_snapshot_sha256: 939528487560531ba8ea1a558ffd48143770b649497f919283bc788512503cd5
pre_evidence_formal_snapshot_sha256: 939528487560531ba8ea1a558ffd48143770b649497f919283bc788512503cd5
candidate_base_commit: 61c6880ea8799fb397baf3b8ae3c2f080e0d2199

## Candidate, dependency, and evaluator identity

- Candidate source version: `0.6.0` on CPython `3.14.6` for Windows.
- Candidate branch: `feat/wo-aex-007-delegated-workflow`.
- Exact `WO-AEX-005` dependency line:
  `74df7b531eb0379b5b00cdcb1cc615f62b61abd7`.
- Exact `WO-AEX-006` implementation commit:
  `45b259bdd255daea53f77a68770729825bdb069d`.
- Exact verified `WO-AEX-006` candidate/base commit:
  `61c6880ea8799fb397baf3b8ae3c2f080e0d2199`.
- This evidence does not identify a later commit containing the
  `WO-AEX-007` implementation or this file.
- Exact released evaluator used for lifecycle status, doctor, formal
  validation, and review preflight: `se-harness 0.6.0` from
  `C:\Users\mathi\Documents\Codex\ev4b-01a037e8\Scripts\python.exe`.
- Released wheel SHA-256:
  `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`.
- Released payload SHA-256:
  `c233678548fe742b7a7a5a8bd65de10156ff233edc65b68e2ed0333fbe4dea42`.

Candidate code cross-checks the exact evaluator identity returned by the
released launcher. It does not claim that candidate source can establish its
own authority or govern this work order.

## Implemented result

- Versioned the candidate workflow contract from
  `se-harness-workflow-v3` to `se-harness-workflow-v4` and added a closed,
  ordered four-operation `agentic_operations` catalog.
- Added a single delegated-workflow coordinator for released-evaluator
  admission, clean-baseline start, broker-only effects, receipt-bound
  completion, candidate-commit stop, and undecided VREC preparation.
- Registered delegated work-order start, work-order completion, and VREC
  preparation as guarded lifecycle mutation operations. Bundle application
  remains the separately guarded effect-broker operation.
- Reused the existing observation, autonomy-envelope, execution-receipt,
  effect-receipt, runtime-state, provenance, decision-packet, workflow, and
  mutation-guard schemas. No duplicate authority-bearing workflow schema was
  introduced.
- Bound lifecycle proofs to the execution receipt, exact admitted envelope,
  before observation, and after observation. Completion binds the start proof,
  uninterrupted effect-receipt chain, full live changed-path set, final state,
  gates, tests, retained evidence, deviations, and residual uncertainty.
- Prevalidates proof shape before lifecycle mutation. A failed post-transition
  observation marks the external runtime session recovery-required and closes
  the active session instead of claiming success.
- VREC preparation requires a complete completion proof. A dirty candidate
  returns the zero-effect Git stop; a separately committed clean candidate
  prepares reviewable undecided material and stops for `DR-VREC-DECIDE`.
- Added `harnessctl delegated-workflow catalog`, `execute`, and
  `prepare-vrec`. JSON input is bounded and rejects duplicate keys; outputs
  retain the full lifecycle/effect proof material. No emitted packet command is
  executed automatically.
- Updated the candidate standard workflow and decision-right projections,
  standalone candidate validator, CLI reference, Phase 4 operator note,
  roadmap, and retained model fixtures. Root installed managed files remain
  byte-locked and unchanged.

## Closed operation, right, state, and gate model

| Operation | Decision right | Required state | Result state | Gate | Procedure |
| --- | --- | --- | --- | --- | --- |
| `delegated-work-order-start` | `DR-WO-START` | `approved` | `in_progress` | `QG-G3-WORK-AUTHORIZATION` | `PROC-WO-START` |
| `change-bundle-apply` | none; admitted broker effect | `in_progress` | `in_progress` | `QG-G4-IMPLEMENTATION-EVIDENCE` | `PROC-WO-IMPLEMENT` |
| `delegated-work-order-complete` | `DR-WO-COMPLETE` | `in_progress` | `implemented` | `QG-G4-IMPLEMENTATION-EVIDENCE` | `PROC-WO-IMPLEMENT` |
| `delegated-vrec-prepare` | `DR-VREC-PREPARE` | `implemented` | `implemented` | `QG-G4-CANDIDATE-READY` | `PROC-WO-PREPARE-VREC` |

The retained model proves these are the only four advancing rows. Only the
three named existing decision rights are activated for lifecycle action. The
catalog validator rejects entry reordering, catalog widening, right changes,
gate changes, procedure changes, and older v3 candidate projections. No
quality-gate definition or accountable role was changed.

## Receipt, gate, path, and recovery matrix

| Boundary or attack | Required observation | Result |
| --- | --- | --- |
| Start | Clean baseline, current exact delegation, correct delegate, prerequisites, G3 pass, no conflict/recovery marker | Passed real-Git coordinator path |
| Start denial | Failed gate, wrong delegate, or dirty baseline | Rejected with zero lifecycle effect |
| Effect | Exact admitted envelope and bundle path set, broker-only mutation, chained effect receipt | Passed real bundle application |
| Completion | Start-after equals first effect-before; complete receipt chain; exact final changed paths and live state; G4 pass | Passed start/effect/complete integration |
| Missing effect receipt | No uninterrupted effect proof | Rejected before completion |
| Altered receipt link | Previous-receipt or observation identity mismatch | Rejected before completion |
| Direct unreceipted write | Live changed paths differ from receipt-bound effects | Rejected before completion |
| Failed completion gate | G4 failed or not assessable | Rejected before completion |
| Altered completion observation | Final proof no longer matches current candidate | Rejected before VREC preparation |
| Post-transition observer failure | Applied lifecycle mutation cannot be re-proved | Session closed and external recovery block set |
| Dirty VREC candidate | Commit-bound candidate absent | Zero-effect `DR-EXTERNAL-ACTION` Git stop |
| Clean changed commit | Candidate content unchanged except Git identity and work order implemented | Undecided ready VREC prepared; stop for `DR-VREC-DECIDE` |
| Failed candidate-preparation gate | Required preparation gate is not pass | Candidate-commit stop rejected |

The executable retained chains are in
`tests/test_delegated_workflow.py::DelegatedWorkflowIntegrationTests`.
They use a real temporary Git repository, exact released-evaluator launcher
stub behavior, real bundle construction and application, execution receipts,
effect receipts, lifecycle proofs, runtime session state, and VREC draft
preparation. Test-side stubs replace authority identities only where a
deterministic isolated evaluator is required; they do not bypass coordinator
validation.

## Stop and prohibited-effect matrix

The retained fixture and test matrix covers `approval`,
`assurance-decision`, `child-agent`, `child-delegation`, `credential`,
`deploy`, `external-action`, `git`, `merge`, `network`,
`parallel-writer`, `publish`, and `release`. Every request returns one
action-specific response in a lossless v2 decision packet with zero performed
effect.

Candidate-commit handling is deliberately informational and zero-effect. The
coordinator does not add, restore, checkout, clean, reset, commit, branch,
merge, rebase, tag, push, pull, fetch, publish, deploy, decide assurance, or
perform packet commands.

## Retained working-tree identities

| Item | SHA-256 |
| --- | --- |
| Candidate workflow contract | `13b5a84460e9f437f96290c9293478a3ab4c72df6a72a944a776a33bc59b7091` |
| Delegated-workflow coordinator | `e2b8ff1f12e06657641aec9186b3fe26a85002a847ca649d127143158c62944f` |
| Candidate CLI | `0636f13bcfa1b0be0ddcaee6c3061df7e89915a22e547859863dcf5f01a37fc9` |
| Phase 4 workflow model fixture | `afc75f773d5760c7fd3bbf90f0876e3ec60b051e936d0aabd92c04f8f06b1dca` |
| Phase 4 workflow operator note | `d158002c43d5931cb72038a60f153ee3ff549317ea07ffb4ea3cc1bd6ef7e511` |

These are working-tree identities, not commit-bound assurance identities.

## Verification observations

| Check | Result |
| --- | --- |
| Focused delegated-workflow, workflow-documentation, lifecycle-contract, mutation-guard, progressive-documentation, and taxonomy suite | Passed after evidence sealing: 66 tests in 73.203 s |
| Exact complete candidate-source repository suite | Passed: 1,000 tests in 428.667 s; 23 skips |
| Retained operation/right/state model | Passed: exactly four advancing rows, three lifecycle rights, and one logical writer |
| Completion adversarial matrix | Passed missing, altered-link, failed-gate, and unreceipted-write cases |
| Start denial/recovery matrix | Passed failed gate, wrong delegate, dirty baseline, and post-transition observer failure |
| Prohibited-action matrix | Passed 13 actions; zero effect and exactly one action-specific response each |
| VREC/commit behavior | Passed dirty Git stop, altered-proof rejection, and separately committed undecided-ready VREC preparation |
| Candidate CLI/API parity | Passed machine-readable catalog equality and exact help for three closed subcommands |
| Candidate bytecode compilation | Passed for `se_harness` and `tests` |
| Candidate release-build and ephemeral-wheel suite | Passed: 13 tests in 12.723 s |
| Release-distribution consistency suite | Passed: 24 tests in 5.547 s |
| Exact 0.6.0 doctor and root managed integrity | Passed all required, distribution, managed, seed, lock, and Python checks |
| Exact 0.6.0 formal graph | Passed: 861 artifacts, 0 errors, 50 pre-existing maintenance warnings |
| Exact 0.6.0 review preflight | Ready: `WO-AEX-007` is `in_progress` with 0 diagnostics |
| Candidate workflow/document projection identity | Passed byte equality and deterministic-documentation contract tests |
| Scaling checks at 100, 500, and 1,000 artifacts | Passed bounded validation, focus, and plan paths |
| Whitespace check | Tracked `git diff --check` passed with informational Windows LF warnings only |
| Changed-path audit | All 20 implementation/evidence paths are within declared exact or prefix scope |
| Root managed-file integrity | Passed exact doctor; no root managed file changed |

The first attempted isolated package command named nonexistent unittest modules,
and a second direct-file command lacked the repository-root import bootstrap.
Both were test-selection errors. The supported discovery commands shown above
then passed the complete release-build and release-orchestration test files.

## Changed-path audit

Implementation and evidence paths:

- `docs/engineering/agentic-execution/README.md`
- `docs/engineering/agentic-execution/evidence/WO-AEX-007-verification.md`
- `docs/notes/README.md`
- `docs/notes/agentic-execution-phase4-workflow.md`
- `docs/notes/agentic-execution-roadmap.md`
- `docs/notes/harnessctl-reference.md`
- `se_harness/cli.py`
- `se_harness/delegated_workflow.py`
- `se_harness/mutation_guard.py`
- `se_harness/workflow_contract.json`
- `se_harness/workflow_contract.py`
- `templates/repository/standard/docs/engineering/DECISION_RIGHTS.md`
- `templates/repository/standard/docs/engineering/WORKFLOW.json`
- `templates/repository/standard/docs/engineering/WORKFLOW.md`
- `templates/repository/standard/scripts/validate_engineering_artifacts.py`
- `tests/fixtures/agentic_execution/phase4/workflow/model-cases.json`
- `tests/test_delegated_workflow.py`
- `tests/test_lifecycle_state_contract.py`
- `tests/test_mutation_guard.py`
- `tests/test_workflow_documentation_contract.py`

The released evaluator and explicit governed amendments separately changed
`docs/engineering/agentic-execution/work-orders/WO-AEX-007.md` to record its
approved-to-in-progress lifecycle event, the two approved scope amendments,
and the current lifecycle description. It is not counted as an implementer
execution-scope change.

`MANIFEST.in`, `pyproject.toml`, the existing contract/effect/provenance
modules, quality-gate projections, and several authorized compatibility tests
did not require changes. Existing package discovery and package-data rules
carry `delegated_workflow.py` and the updated workflow contract.

## Deviations and residual uncertainty

- Execution and integration testing ran on Windows. POSIX-specific filesystem
  and launcher behavior remains for independent assurance on a supported POSIX
  host.
- The integration matrix uses real Git and broker writes but deterministic
  evaluator fixtures. Independent assurance must repeat the commit-bound path
  against the exact candidate commit and successor released evaluator.
- The recovery case injects an observer exception after a lifecycle mutation;
  it does not claim a real hardware power-loss, disk-full, or hostile-process
  experiment.
- The CLI `execute` command intentionally applies one supplied change bundle
  per invocation. Multiple effects are represented by the Python coordinator's
  ordered receipt sequence and may be exercised by a higher-level caller
  without adding a parallel writer.
- Candidate unit tests, fixtures, hashes, and this document are
  implementer-generated. They cannot satisfy `VER-AEX-004`, replace
  commit-bound independent assurance, activate Phase 4, or authorize a pilot.
- A successor released evaluator and separately governed disposable target
  pilot remain future milestones. Candidate v4 projections do not modify the
  installed root v3 managed contract.

## Intentionally not performed

No transition to `implemented`, candidate commit, VREC artifact creation for
this work order, assurance decision, branch rewrite, merge, push, pull request,
release, installation, publication, deployment, credential access, network
effect, external-system action, target pilot, skill change, provider change,
child-agent execution, parallel writer, or root managed-file change was
performed by this implementation checkpoint.

## Handoff result

Outcome: The approved `WO-AEX-007` implementation and implementer evidence
are complete.

Done: Closed delegated start/effect/complete/VREC-preparation integration,
candidate workflow-v4 projection, guarded CLI, executable receipt and recovery
matrices, documentation, scope audit, and required implementer verification.

Not done: Work-order completion transition, exact candidate commit,
commit-bound independent assurance, VREC decision, release, or activation.

Current lifecycle state: `in_progress`.

Decision required: The accountable engineering owner must decide whether the
implementation evidence is sufficient to transition `WO-AEX-007` to
`implemented`.

Next: Authorize the released evaluator to mark `WO-AEX-007` implemented.

Command or response: `Mark WO-AEX-007 implemented.`

Alternatives: Request a bounded correction while the work order remains
`in_progress`, or stop without lifecycle effect.
