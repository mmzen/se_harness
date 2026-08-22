# WO-REB-007 corrective proposal evidence

Date: 2026-08-22

## Authority boundary

The repository owner subsequently approved `REQ-REB-013`, `REQ-REB-014`, `SPEC-REB-006`, `ARCH-REB-005`, `ADR-REB-005`, `VER-REB-005`, and `WO-REB-007` for the exact bounded scope in this packet, authorized their `draft` to `approved` transitions, and authorized `WO-REB-007` start. Those transitions were recorded at `2026-08-22T07:15:02Z`; the work order moved from `approved` to `in_progress` at `2026-08-22T07:15:03Z`.

That authority permits local implementation and qualification only. `REL-SEH-011` remains `draft`, `REL-SEH-010` remains `approved`, and `WO-REB-006` remains `in_progress`. No candidate commit, branch movement, credential use, hosted dispatch, completion/lifecycle disposition, VREC/RLS preparation or transition, tag, publication, deployment, maintenance mutation, external-policy change, or root-evaluator upgrade is authorized or performed.

## Immutable candidate and hosted failures

- Candidate C4: `b099a2728d945ee705c1f956ec012f9730df15ac`, tree `3ee3cdc2b801ebf8b3166589e010f82ea8d40512`.
- Later local governance commit: `39fac46b009727529b6b65f5d8e63972155b0590`; it is not the candidate branch target.
- Dedicated remote branch: `candidate/0.6.0-c4` at exact C4.
- [Engineering Harness run 32558379907](https://github.com/mmzen/se_harness/actions/runs/32558379907), job `96996045728`: exact released 0.5.0 identity, isolation, installation, and managed-integrity checks passed; full-checkout validation then failed with one `E009` on rejected `docs/engineering/release-0-6-0/releases/RLS-SEH-009.md`.
- [Candidate Evidence run 32558379908](https://github.com/mmzen/se_harness/actions/runs/32558379908), source job `96996045654`: candidate identity/surface passed; 435-test regression ended with exactly two errors when Linux Python 3.11 cleanup called the process-wide `os.open` mock using `dir_fd`. Package job `96996119243` was skipped.

These runs are failed qualification evidence. They are not retried, deleted, relabelled, or treated as passing.

## Root causes

1. `WO-REB-006` implemented the exact predecessor compatibility view for release-record preparation but not hosted predecessor assessment. The unchanged hosted workflow invokes released 0.5.0 `doctor .` and `validate .` on the complete checkout, which that evaluator cannot parse after rejected RLS history.
2. `tests/test_predecessor_preparation.py` patches `PREPARATION.os.open`, which is the shared standard-library module object. Windows cleanup did not expose the leak; Linux `shutil.rmtree` did.

## Read-only predecessor-view prototype

A disposable bundle-backed clone was checked out detached at exact C4. Only the already governed closed rejected pair was removed from that temporary view:

| Path | Git blob | Committed bytes | Raw SHA-256 |
|---|---|---:|---|
| `docs/engineering/release-0-6-0/releases/RLS-SEH-009.md` | `0b9661f570e8a85afa4acb4dd995eda57bfc7f67` | 1797 | `e0b8952953e8e180c6d572fe5d1236fded7104e623cc336bb9a93cd3b978f9e3` |
| `docs/engineering/release-0-6-0/release/REL-SEH-008.md` | `d14090b88ff6d1c032333d7a2454ca9a571854e5` | 9093 | `24e0962f6957e7501159a223913e16ef82b22e5e1ae1a88174b9887b43cb4aec` |

Exact installed released 0.5.0 then passed `doctor` and `validate` in the view. Validation reported 635 artifacts, zero errors, and 47 retained legacy maintenance warnings. The full source checkout and both historical files remained unchanged. The disposable prototype is feasibility evidence only; it is not hosted evidence and created no repository output.

## Implemented local correction

- `repository_tools/predecessor_assessment.py` reuses the closed-pair derivation, exact Git view, evaluator identity/payload proof, and source rechecks from predecessor preparation. It requires managed `doctor` to pass on the complete checkout, requires the released evaluator's subsequent JSON validation to contain exactly one `E009` on rejected `RLS-SEH-009`, and runs fixed identity, `doctor`, `validate`, and dashboard commands in the two-omission view.
- `scripts/assess_predecessor_evaluator.py` exposes only exact candidate, approved contract, external evaluator tuple, and external evidence path inputs. It accepts no omission, command, or expected-error input; it refuses recognized publication credential signals and linked, unsafe, colliding, or in-checkout outputs.
- `.github/workflows/predecessor-evaluator-assessment.yml` is a separate candidate-owned read-only lane. It disables persisted checkout credentials, downloads exact 0.5.0 wheel bytes, checks SHA-256 `974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f`, runs the adapter at `GITHUB_SHA`, proves checkout no-change, and uploads only the bounded canonical evidence and plan.
- Canonical `se-harness-predecessor-assessment-view-v1` evidence binds the complete candidate reports, exact legacy refusal, source commit/tree, omitted blob/raw identities, sparse rules, evaluator archive/payload, fixed commands, view graph counts, and dashboard tree. Only predecessor dashboard `generation-summary.json` runtime fields `generated_at` and `elapsed_ms` are explicitly normalized; semantic bundle bytes remain recursively hash-bound.
- `repository_tools/predecessor_preparation.py` now routes exclusive creation through adapter-local `_open_exclusive`. Both rollback tests patch only that seam, preserving production `O_WRONLY | O_CREAT | O_EXCL`, mode `0o644`, call ordering, rollback, and temporary-directory cleanup on Windows and Linux implementations.
- Operator notes explain the honest red-legacy/green-view model and keep the transitional adapter outside generic `harnessctl` lifecycle authority. Internal names use “predecessor evaluator,” preserving the portable product's retired-specialized-lifecycle surface rule.

## Candidate-invalidation implications

C4 is immutable failed evidence and cannot be repaired in place. Any approved code, test, or workflow correction produces candidate C5 with a new commit/tree and later a new dedicated branch. `REL-SEH-010` remains approved until separately dispositioned. Reserved but uncreated `VREC-SEH-011`/`RLS-SEH-011` remain unused; draft `REL-SEH-011` proposes future `VREC-SEH-012`/`RLS-SEH-012`. `WO-REB-006` remains `in_progress` until the combined local and hosted correction is separately accepted.

## Local qualification

- A reviewed seventeen-path implementation overlay on governance commit `39fac46b009727529b6b65f5d8e63972155b0590` passed candidate validation with 645 artifacts, zero errors, and 48 maintenance warnings. The exact released-0.5 full graph remained one `E009` with 645 artifacts and 47 legacy warnings.
- The real released 0.5.0 evaluator on clean `39fac46b009727529b6b65f5d8e63972155b0590` reported complete candidate 637/0, exact legacy 637/1, and exact view 635/0. Omitted paths, blobs, sizes, and raw hashes matched the retained C4 prototype. Python 3.11 assessment plan evidence SHA-256 was `b6422b14150c15469d9e9dbd9710feb3b7581528f00499a430b141ec59b091a9`; normalized dashboard-tree SHA-256 was `37890e96758118b3759b5545d17d8dea8f2bcde518d28c84b4332bd6e6bac156`.
- Two independent Python 3.14 apply rehearsals produced byte-identical 4,028-byte canonical evidence with SHA-256 `4f5879211d39614a76f891699399fc061eb8fe9e5c71e3150ad27b4ab70d00ca`. Their output filenames and temporary roots were absent from canonical bytes; the source checkout stayed clean.
- Focused predecessor, workflow, release-bootstrap, and documentation tests passed 46/46. The predecessor/fault/workflow subset passed 15/15 on clean Python 3.11.9.
- Complete reviewed-source suites passed 443 tests with five intentional skips on clean Windows Python 3.11.9 and Python 3.14.6. Portable release-surface validation passed. Distribution validation passed with zero distribution-bearing records in this pre-candidate overlay.
- `.engineering-harness.toml`, `.engineering-harness.lock`, `.github/workflows/engineering-harness.yml`, all other root-managed files, rejected `REL-SEH-008`/`RLS-SEH-009`, maintenance state, refs, and external policy were not changed. The separately stopped untracked `RLS-SEH-008` remained untouched at SHA-256 `eea7a9953767e6b817754a517db72a2484561462fce1c9e440c5e5d1501a75fc` and is excluded from every reviewed overlay.
- Assurance review found one count-label inconsistency in the approved packet: `SPEC-REB-006` and `VER-REB-005` called the exact C5 view “635-artifact,” but 635 is the retained C4 prototype count. The repository owner then instructed `ok go for next step` after receiving the exact two-document remediation. Those two references now require the view count to equal the complete candidate count minus exactly two (643 for the reviewed 645-artifact C5 scope), preserving both approved statuses and every other scope boundary. The implementation derives and records the count and does not weaken or add omissions.
- Linux Python 3.11, exact candidate identity, candidate package, and hosted assessment evidence remain pending a separately authorized candidate commit/branch/dispatch. These local results do not complete `WO-REB-007`.

## Remaining accountable boundary

The next operational step would be one separately authorized C5 candidate commit containing only the reviewed packet, implementation, documentation, tests, workflow, and retained pre-candidate evidence. Candidate branch creation/push, credential use, hosted dispatch, exact-replay evidence retention, `WO-REB-007`/`WO-REB-006` completion, `REL-SEH-010` disposition, `REL-SEH-011` approval, and all VREC/RLS/release actions remain separate decisions.
