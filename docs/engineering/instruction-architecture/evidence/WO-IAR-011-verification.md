# WO-IAR-011 implementation and verification evidence

## Authority and candidate state

The repository owner authorized the bounded `IAR-011` implementation on 2026-08-19 with `ok go implement`. This evidence records implementation checks against `VER-IAR-011`. At evidence finalization, the implementation was an uncommitted working-tree candidate based on `4f73d516c8d336ec65f3808a64cd280b2f702b8f`; its later candidate commit cannot be self-recorded here and belongs in the VREC created after that commit. The evidence-collection phase did not commit, push, open a pull request, prepare or transition a VREC, prepare a release record, tag, publish, or deploy.

## Implemented behavior

- Added the stable six-field lifecycle-handoff obligation to the canonical managed router without duplicating ordered workflow procedure.
- Added the full draft, implementation, candidate, verification, release, and failure mapping to canonical managed `WORKFLOW.md`, including human authority, exact suggested commands or replies, valid alternatives, unchanged-state failure handling, and the prohibition on generic follow-up questions where a bounded recommendation exists.
- Kept the managed `AGENTS.md` fragment thin and left `harnessctl inspect`, its JSON schema, closed suggestion catalog, and non-executable guidance boundary unchanged.
- Updated the bounded public practical example with draft, failed-stage, and verified-record handoffs using illustrative `WO-RATE-001` and `VREC-RATE-001` identities.
- Updated instruction-architecture acceptance and index material.
- Used `harnessctl upgrade . --apply` to synchronize the root router and workflow from their canonical templates and regenerate the schema-2 lock.

## Test-first and focused evidence

The initial focused run demonstrated that the current distribution lacked the new router heading, workflow stage mapping, and README fields. A test-fixture section-removal setup defect was corrected before implementation; it did not affect product code or the eventual assertions.

After implementation:

- Three new handoff tests passed in 0.829 seconds.
- The final combined instruction-architecture and public-onboarding suites passed 31 tests in 12.223 seconds.
- The final full suite passed 246 tests with 3 expected skips in 79.677 seconds on Python 3.14.6.

The first full-suite attempt had one environmental error because a release-manifest fixture invoked Git directly and the sandbox-owned clone was not on Git's safe-directory list. The exact failing test passed in 0.178 seconds with a process-local `GIT_CONFIG_COUNT` safe-directory entry, and the full clean result above used that same process-local setting. No repository or global Git configuration changed.

## Managed distribution, compatibility, and integrity

- The pre-apply upgrade plan proposed updates only to `ENGINEERING_HARNESS.md` and `docs/engineering/WORKFLOW.md`, retained the two repository-specific self-hosting controls as protected, and reported 30 unchanged files.
- The apply completed transactionally. Focused upgrade coverage proves safe replacement of the exact prior router/workflow state and a byte-stable second apply; existing regression fixtures retain customized, ambiguous, damaged, and no-partial-write coverage.
- `harnessctl doctor .` passed every required, distribution-parity, managed-integrity, template, and lock check. It reported only the known historical W013 location warnings.
- The lock remains schema 2 with `sha256` and `utf8-text-lf-v1`. Its managed hashes are `74e805ad85b007a719508ae92d38cd8b93255d40fb2d339c9bbfc9aefd30dc59` for the router and `b006759796d79666b0dac654d75a9022cc210727de464c581c856fef0caf3a8b` for workflow.
- A final `harnessctl upgrade .` plan proposed no managed updates: 32 files were unchanged and only the two expected self-hosting controls remained protected.
- Package-data coverage is unchanged, and doctor proves the installed root copies match the canonical distribution. No runtime dependency, Python module, package metadata, installation profile, or version changed.

## Repository gates and observations

- Start preflight passed before implementation and returned the complete thirteen-file governing manifest for `WO-IAR-011`.
- Review preflight passed after completion for `WO-IAR-011 (implemented)` and returned the same complete governing manifest without changing state.
- Direct formal validation passed with 472 artifacts, 0 errors, and 44 known maintenance warnings: structure E0/W0, governance E0/W0, policy E0/W0, maintenance E0/W44. This is the same warning backlog observed before implementation.
- `python -m se_harness --help` passed and exposed the unchanged command surface.
- `harnessctl inspect .` passed with 472 artifacts, 1,743 relations, and the same 44 formal warnings; before lifecycle completion it correctly reported only `WO-IAR-011` as active work.
- The final `harnessctl dashboard .` passed with snapshot manifest `d2d2ec5b6fedf6cf912eb72b3a92001fc20a230f481ed0695fb197964bf8336b`.
- The public README remains bounded at 177 lines, retains its nine top-level sections and existing visual/example constraints, and passes all public-onboarding assertions.
- `git diff --check` passes. Git emits only expected Windows working-tree line-ending notices.

## Responsibility and semantic review

The router states only the invariant reporting obligation, actual-ID rule, final-state rule, recommendation/action boundary, and route to workflow. It contains no review-preflight, capture-verification, or release sequence. Workflow owns every ordered stage and distinguishes already-granted implementation authority from commit, assurance, release, hosting, publication, deployment, and operating rights.

Every stage has a bounded primary recommendation. Exact commands appear only for preflight, review observation, VREC preparation, and separately authorized release preparation; approval, verification, release, and external actions use suggested accountable responses instead. Failure retains the formal state and recommends remediation or escalation. The verified-VREC stage exposes pull-request and release-preparation alternatives with distinct authority. No example contains credentials, private locations, unsafe interpolation, or automatic action.

No new architecture artifact applies: this implementation uses the previously approved single-router/focused-policy responsibility split and adds no component, schema, interface, trust boundary, persistence choice, or significant structural decision.

## Changed surface

- Canonical and root `ENGINEERING_HARNESS.md` content.
- Canonical and root `docs/engineering/WORKFLOW.md` content.
- `.engineering-harness.lock`.
- Root `README.md` practical example.
- Instruction-architecture acceptance, `IAR-011` governing packet, domain index, tests, and this evidence.

No `se_harness/` module, Inspector script, CI workflow, release tool, package metadata, historical artifact, or machine-readable output changed.

## Deviations and residual risk

No implementation deviation from `SPEC-IAR-011` was required. Static prose and distribution tests cannot prove universal coding-agent compliance, correct accountable human judgment, or host-specific authority. The 44 formal maintenance warnings predate this packet and remain separate governed backlog. A ready VREC must be prepared after the clean candidate commit and must receive a separate accountable assurance decision before it can become `verified`.
