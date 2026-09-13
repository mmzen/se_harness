# WO-KIS-002 implementation evidence

Source candidate: `6f946632626ddcbdb63222a16a295a2450aad9e5`. Governing checker: isolated released 0.17.0.
This covers seven cuts. Work is implemented through delegated completion; owner verification is pending.

| Check | Observed result | Evidence |
| --- | --- | --- |
| K04 | A plural PR declaration checks each approved work order and their combined scope. Duplicate IDs, draft work and outside paths fail. | CombinedWorkOrderTests |
| K05 | Recorded owner approval on a local branch permits start without a preliminary merge. A class label alone or widened scope fails. | LocalDelegationTests; installed-local-start |
| K06 | Local start, completion and capture succeed without a GitHub remote or delegation configuration. Failed local gates still block. | LocalDelegationTests; installed-local-complete |
| K08 | Unrelated artifact edits preserve freshness; selected requirement and code changes change it. | CanonicalSnapshotTests |
| K09 | Capture succeeds with the dashboard generator unavailable and creates no dashboard. | test_capture_is_independent_of_dashboard_generation |
| K10 | Explicit committed capture runs its test command in a temporary checkout; preserves the caller note; removes the checkout. Failed tests write no record. | RevisionCliTests; installed-committed-capture |
| K12 | Unrelated draft and parse errors appear as background findings; selected errors and duplicate IDs block. | LocalScopePreflightTests |

The committed source suite passed **1,173 tests, 25 skipped**, on Windows/Python 3.14.
Command: `python scripts/run_tests.py --workers 4 --timings ../work/kis002-committed-timings.json`.
Elapsed time: 127.095 seconds. This is a recorded duration, not a measured speedup.

The non-promotable wheel was built from a Git export of that exact commit and installed
outside the checkout under Python 3.12. Installed identity, initialization, validation,
doctor, ordinary local delegation/completion, and committed capture passed. The latter
ran without a remote, preserved a caller note, retained a ready record for the actual
commit and left one Git worktree. Wheel SHA-256: `3ec6f7458c4112dbd8f7931e16fee13a841c7a565cd964947ededc0ab40d29d0`.

Released doctor and review preflight passed. Source graph validation passed; release
distribution validation passed for all 14 distribution-bearing records. The root remains
on 0.17.0. Historical records, package integrity, file boundaries and owner verification
rights remain intact. All hosted checks passed, including Linux/Windows upgrade and integration-package acceptance. Exact head and check URLs are retained in `ci-implementation.json`.

Source: 288 lines added, 316 removed.
Tests: 206 added, 536 removed.
Local delegation shrank from 352 to 147 lines.
The workflow template shrank from 197
to 91 lines.

The implementation retires CI-provider simulations and embedded-workflow-reader tests.
The suite initially found a shared snapshot regression affecting definition/risk
transitions and obsolete documentation expectations; both were fixed before this
committed passing run. No tests were disabled to obtain the pass.

## Ready verification record

The released evaluator prepared VREC-KIS-002 against `7cae3a4cf098a5be73562507b558c03f1d100dd2`.
The required `validate` check passed on that commit; see `ci-verification-candidate.json`.
The full hosted suite passed before the completion metadata was added; see `ci-implementation.json`.
Source, templates and tests are unchanged from the locally tested source commit.
The record is ready for the assurance owner, not yet verified.
