# WO-AEX-005 implementation evidence

This file records the implementation handoff checkpoint for `WO-AEX-005`.
It is not an assurance decision, verification record, lifecycle transition,
commit authorization, release decision, or activation of Phase 4. The work
order is `in_progress` at this checkpoint and requires later commit-bound
verification.

artifact: WO-AEX-005
checkpoint: handoff
formal_snapshot_sha256: bb1dc12f5a684cc548e92867b6436562bd21e1fde894a39ddc88d2d178267883
pre_evidence_formal_snapshot_sha256: 9c54ad7eafbe6b0e03ac18eac5a9b53e2ade1593953929e26386bbc80dd5d93c
post_amendment_formal_snapshot_sha256: bb1dc12f5a684cc548e92867b6436562bd21e1fde894a39ddc88d2d178267883
candidate_base_commit: 005e7ca13491d7e20e37a57a39fbaaea6d575975

## Candidate and evaluator identity

- Candidate source version: `0.6.0` on CPython `3.14.6` for Windows.
- Candidate base commit:
  `005e7ca13491d7e20e37a57a39fbaaea6d575975`. This evidence does not
  identify a later commit containing the implementation or this file.
- Exact released evaluator used for approval, start, and baseline checks:
  `se-harness 0.6.0` from the isolated external launcher.
- Released wheel SHA-256:
  `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`.
- Released payload SHA-256:
  `c233678548fe742b7a7a5a8bd65de10156ff233edc65b68e2ed0333fbe4dea42`.

The candidate modules accept externally proven evaluator identity and managed
catalogs. They do not claim that candidate source can prove its own released
identity.

## Implemented result

- Added strict contract roots for
  `se-harness-repository-observation-v1`,
  `se-harness-agentic-delegation-v1`, and
  `se-harness-autonomy-envelope-v2`.
- Preserved the existing autonomy-envelope v1 parser, vectors, canonical bytes,
  narrowing, and pure admissibility behavior.
- Added a read-only live observer using bounded Git argument vectors with
  `shell=False`, streamed file hashing, exact-root checks, portable-path and
  case-collision checks, link/reparse rejection, conflict/submodule rejection,
  governance digests, and two-consecutive-capture stability.
- Added clean/dirty classification for delegated start and receipt-linked dirty
  continuation without adding that volatile classification to canonical
  observation bytes.
- Added formal delegation parsing and cross-checks for managed delegators,
  rights, operations, profiles, logical delegates, execution scope, retained
  evidence kind/path pairs, expiry, retry, single writer, no child delegation,
  and mandatory stops.
- Added least-authority envelope-v2 derivation with one operation, narrowed
  paths/profile/evidence, evaluator and work-order binding, current state,
  previous receipt, 128-bit nonce, retry ordinal, and an expiry no later than
  five minutes.
- Added an external runtime-state store for one active session, canonical and
  atomic state files, nonce consumption, concurrent replay exclusion,
  revocation, terminal outcomes, recovery-required blocking, recovery
  acknowledgement, and external-directory alias/containment rejection.
- Added fresh-state admission preparation that consumes the nonce but has no
  target-effect callback.
- Added receipt continuity checking that independently validates the receipt,
  exact admitted `state_before`, and fresh live `state_after`.
- Added the optional delegation table to the candidate work-order template and
  shape/scope validation to the candidate artifact validator. Root managed
  templates and validators remain unchanged.
- Added canonical Phase 4 reference vectors and adversarial tests for schema
  closure, v1/v2 separation, observer races, ignored and untracked inputs,
  evaluator and lock drift, links, aliases, case collisions, conflicts,
  submodules, widening, expiry, gates, dirty continuity, nonce replay and
  races, session collision, revocation, recovery, stale fresh state, and
  receipt gaps.

No target file operation, lifecycle transition, workflow activation, skill
change, provider adapter, Git mutation, credential use, network operation,
package release, installation, publication, or external action was added.

## Retained identities

| Item | SHA-256 |
| --- | --- |
| Candidate agent-contract catalog | `3d536d68c3cbf338e1de37ea7c932119c64109204e23a1748a6032e845eaeaec` |
| Phase 4 canonical vector fixture | `1f1deb4efba9e6e358d7114d5ce498e530badb1b444e1e26661dd8e69e29f738` |

These are working-tree identities, not commit-bound assurance identities.

## Verification observations

| Check | Result |
| --- | --- |
| Existing v1-focused contract suite after schema additions | Passed: every v1 vector, canonical byte, narrowing, and behavior case remains green |
| Final focused Phase 4, agentic, and amended catalog suite | Passed: 57 tests in 6.514 s; 2 Windows platform skips |
| Governed candidate-template compatibility assertion | Passed in isolation: the candidate is reconstructed exactly from the released template plus the declared delegation block and guidance paragraph |
| Final exact complete repository suite | Passed: 943 tests in 289.274 s; 22 skips |
| Candidate formal graph | Passed: 846 artifacts, 0 errors, 56 maintenance warnings |
| Canonical root formal graph | Passed: 846 artifacts, 0 errors, 50 pre-existing maintenance warnings |
| Release-distribution consistency | Passed for 1 distribution-bearing record |
| Exact 0.6.0 doctor | Passed every required, distribution, managed, seed, lock, and Python check |
| Exact 0.6.0 graph | Passed: 846 artifacts, 0 errors, 50 maintenance warnings |
| Exact 0.6.0 start preflight | Ready: `WO-AEX-005` is `in_progress` with 0 diagnostics |
| Exact released CLI help | Passed for root, doctor, validate, and preflight surfaces |
| Whitespace and final-newline checks | Tracked `git diff --check` passed with only informational Windows LF conversion warnings; an independent scan of all 32 tracked and untracked changed files found 0 issues |
| Candidate catalog closed-reference validation | Passed with 11 schemas; definitions are canonical, sorted, and reference-complete |
| Target-effect sentinel | Passed: authority/admission modules expose no effect callback; observer tests preserve target state except test-owned fixture mutations |

The changed-path audit found only the approved Phase 4 artifact pack and the
amended `WO-AEX-005` exact/prefix paths. No root managed file changed. The exact
complete suite now passes. A commit-bound VREC must replace these working-tree
observations with exact candidate-commit evidence.

## Governed scope amendment and resolution

On 2026-08-25 the user explicitly accepted the governed amendment adding
`tests/test_artifact_catalog.py` to `WO-AEX-005` execution scope. The work order
records the amendment and limits the file change to the candidate-template
compatibility assertion.

The amended test reconstructs the candidate work-order template from the
unchanged released root template plus the exact optional delegation table and
its exact guidance paragraph, then requires full byte equality with that
reconstruction. It also proves the released template has no delegation table.
Traceability-copy equality and the separate candidate-router exception remain
unchanged.

No assertion was skipped or made open-ended, no wildcard exception was added,
and no root managed file changed. The isolated assertion, expanded focused
suite, and complete suite pass after the amendment. No completion transition,
commit, or verification decision is requested or recorded by this evidence.

## Residual uncertainty

- POSIX filesystem permission and hostile-name cases require independent
  supported-platform execution; this Windows run cannot prove them.
- Reparse and symlink creation depends on host privilege; static rejection and
  supported cases are covered, but cross-platform external verification
  remains required.
- The runtime state is intentionally bounded to one evaluator process and one
  active repository session. The later effect journal and crash recovery
  execution belong to `WO-AEX-006`.
- Candidate unit tests and this evidence are implementer-generated and cannot
  satisfy `VER-AEX-004` independent assurance.
