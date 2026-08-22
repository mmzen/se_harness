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

## Post-candidate exact replay (uncommitted retention update)

The repository owner separately authorized one operational C5 candidate commit and local exact-candidate replay, while withholding branch movement, push, credential use, hosted dispatch, lifecycle transitions, VREC/RLS preparation or transition, tag, publication, deployment, maintenance mutation, external-policy change, and root-evaluator upgrade. The resulting immutable candidate is `5653cb52e729ad5d48683bc7e28ee3f0478e2e2c`, with sole parent `39fac46b009727529b6b65f5d8e63972155b0590`, tree `53ddcdc07608ea57f573e41c8d082c2e885d0874`, and commit epoch `1787386198`. Its commit contains exactly the reviewed seventeen paths. The stopped untracked `docs/engineering/release-0-6-0/releases/RLS-SEH-008.md` is absent from the candidate and remains untouched at SHA-256 `eea7a9953767e6b817754a517db72a2484561462fce1c9e440c5e5d1501a75fc`.

Two clean bundle-backed clones were detached at exact C5. Candidate-source identity passed on Windows Python 3.11.9 and 3.14.6 with version `0.6.0`, the exact commit, and source/template origins inside the detached checkout. Both clones remained clean after qualification.

| Exact-candidate check | Result |
| --- | --- |
| Python 3.11.9 full source suite | PASS: 443 tests in 267.774 seconds, 5 declared platform skips |
| Python 3.14.6 full source suite | PASS: 443 tests in 264.940 seconds, the same 5 skips |
| Candidate formal graph | PASS: 645 artifacts, 0 errors, 48 retained maintenance warnings |
| Release-distribution policy | PASS: 0 distribution-bearing records |
| Candidate CLI and source identity | PASS on both runtimes |
| Portable repository and wheel surfaces | PASS |
| Fresh exact-wheel package acceptance | PASS on Python 3.11.9 and 3.14.6: identity, init, doctor, validate, dashboard, upgrade, and checkout no-change |

The exact released 0.5.0 wheel retained SHA-256 `974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f` and payload SHA-256 `d247cc48213b49be52345fcadbf2d93355e5ea7ef15b32014d9fc5010458a2bc`. Two independent applied assessments, one orchestrated by Python 3.11.9 and one by Python 3.14.6, produced byte-identical 4,028-byte canonical `se-harness-predecessor-assessment-view-v1` evidence with SHA-256 `7c75b2a092ffd3fc967f10ab49d340a037c5f3e63fa613314e1c0f01524dc573`. The complete candidate passed at 645 artifacts and 48 warnings; the released evaluator's complete-checkout observation was exactly one `E009` on rejected `RLS-SEH-009`, 645 artifacts, and 47 warnings; and the contract-derived predecessor view passed `doctor`, `validate`, and dashboard at exactly 643 artifacts and 47 warnings. The normalized dashboard manifest SHA-256 was `dd0bb96e25262ca5652ee1321a24269729ef2b4af61d178487a2054b2683a83c`. The view omitted only rejected `REL-SEH-008` and rejected `RLS-SEH-009`, with their committed blob/raw identities unchanged.

Two independent exact Git exports were byte-identical with SHA-256 `9172f0cc44f392f964dfa6e3ffb2ed1c32984d4c76ff0d9e2427a74b125ed6aa`. Using Windows Python 3.11.9, the publication-workflow-pinned `build==1.3.0`, setuptools `84.0.0`, and C5 `SOURCE_DATE_EPOCH=1787386198`, both exports produced byte-identical release files:

- wheel `se_harness-0.6.0-py3-none-any.whl`: SHA-256 `7646a64a919c3ec697b92f85772f4254abd5e2ddf4bb306cc32b2ce8dfab1fa4`;
- normalized sdist `se_harness-0.6.0.tar.gz`: SHA-256 `29dfbc1f955e6c2bdeb77acc67d4be095bb65410f4f8551e378d50ef1d101a14`; and
- an offline no-isolation reconstruction from the normalized sdist reproduced the exact wheel SHA-256 `7646a64a919c3ec697b92f85772f4254abd5e2ddf4bb306cc32b2ce8dfab1fa4`.

The canonical release-bundle manifest binds C5, version, epoch, Git object format, source manifest, wheel, sdist, and checksum bytes. Its SHA-256 is `0de379aa59ec24acebcbe3c858d23510e456c4a254b52e3e1e72f39b826f16c4`; its source-manifest SHA-256 is `17136ee6d865d5112c9e173ccd5706b1d4d8d696a46111a45c53fe82f3e74840`; and its canonical checksum-content SHA-256 is `ba0724ae80ee1e2039f337a13fe48c360149f6a58ab7d65f3fc1063aa24f58f0`.

This section is the authorized retained exact-replay update and remains deliberately uncommitted. `WO-REB-007` and `WO-REB-006` remain `in_progress`, `REL-SEH-010` remains `approved`, and `REL-SEH-011` remains `draft`. No push, credential use, hosted dispatch, lifecycle transition, VREC/RLS preparation or transition, tag, publication, deployment, maintenance mutation, external-policy change, or root-evaluator upgrade occurred.

## C5 hosted qualification and stop condition

The repository owner subsequently authorized dedicated branch `candidate/0.6.0-c5` at exact C5 and use of the existing configured Git credential only for its push and hosted qualification. The local branch, remote branch, and remote-tracking ref all resolved to `5653cb52e729ad5d48683bc7e28ee3f0478e2e2c`; the uncommitted evidence update and stopped `RLS-SEH-008` were absent from the branch.

- [Candidate Evidence run 32562498151](https://github.com/mmzen/se_harness/actions/runs/32562498151) passed. Source job `97006147387` and package job `97006212367` both completed successfully.
- [Engineering Harness run 32562498162](https://github.com/mmzen/se_harness/actions/runs/32562498162), job `97006147318`, reached exact released-0.5 validation and failed only with the expected `E009` on rejected `RLS-SEH-009`, with 645 artifacts and 47 warnings. This is the required visible legacy limitation, not an unexpected candidate failure.
- [Predecessor Evaluator Assessment run 32562498180](https://github.com/mmzen/se_harness/actions/runs/32562498180), job `97006147382`, failed unexpectedly in `Assess the complete candidate and exact predecessor view`. The command's `--json` output was redirected to runner-temporary `predecessor-assessment-plan.json`; subsequent proof and artifact-upload steps were skipped, so the hosted log contained only exit code 1.

The configured GitHub credential was later used read-only to retrieve those exact failed logs. No rerun, branch movement, workflow dispatch, setting change, or other external mutation occurred.

## POSIX evaluator-root diagnosis

A disposable Ubuntu 24.04 environment reproduced the hosted topology with a normal symlink-based virtual environment. POSIX `evaluator/bin/python` resolved to `/usr/bin/python3.12`. C5's `_ordinary_external` resolved that terminal link before deriving `python.parent.parent`, treated `/usr` as the evaluator root, and rejected the genuine virtual-environment entry point. The exact closed JSON reproduction was:

```json
{"applied": false, "error": "released-evaluator entry point is outside the interpreter environment", "passed": false}
```

The same exact-C5 assessment completed when the disposable interpreter was created with copy semantics, proving that rejected history, sparse derivation, the 0.5.0 wheel, and the LF checkout were not the cause. After preserving the lexical interpreter path, a second adjacent failure appeared only during canonical evidence creation: generic origin normalization dereferenced the reported lexical `bin/python` and rejected its system target as outside the declared root. This confirmed one repeated incorrect assumption across interpreter selection and evidence normalization, not two independent release-governance defects.

## Bounded C6 correction and local qualification

Under the still-`in_progress` `WO-REB-007` Linux/Windows runtime scope, the reviewed correction:

- preserves the normalized lexical external interpreter path and derives the evaluator root from its virtual environment;
- permits only the terminal interpreter symlink used by a standard POSIX virtual environment, while rejecting linked parents, junction aliases, in-checkout targets, linked entry points, and linked wheels;
- compares the released runtime's reported interpreter to the exact lexical invocation path and normalizes that verified lexical origin without dereferencing it outside the environment;
- adds real POSIX `venv.EnvBuilder(..., symlinks=True)` coverage plus linked-parent rejection, while preserving Windows ordinary-file behavior;
- makes checkout no-change proof and bounded artifact upload run with `if: always()`, and prints the closed assessment-plan JSON before returning its original status; and
- documents the POSIX invocation contract and amends only draft `REL-SEH-011` to retain failed C5 and name future C6 without changing status or the fourteen-work-order, fifteen-path, thirteen-contract aggregate.

A disposable local prototype commit, not an operational candidate, bound the reviewed eight-path overlay to `82a237e541eabf7e9d6b0a5896b5f3e5c4f26b19`, tree `f81bff7fd6de0dd86e08b5e29fe01d3f2162132e`. It exists only in disposable qualification clones and neither moves nor replaces C5.

| Corrected prototype check | Result |
| --- | --- |
| Focused predecessor/workflow tests, Windows Python 3.11 | PASS: 17 tests, 2 POSIX skips |
| Focused predecessor/workflow tests, Ubuntu Python 3.12 | PASS: 17 tests, 0 skips |
| Full clean suite, Windows Python 3.11.9 | PASS: 445 tests in 231.178 seconds, 7 declared platform skips |
| Full clean suite, Windows Python 3.14.6 | PASS: 445 tests in 216.636 seconds, 7 declared platform skips |
| Full clean suite, Ubuntu Python 3.12.3 | PASS: 445 tests in 439.992 seconds, 0 skips |
| Candidate formal graph | PASS: 645 artifacts, 0 errors, 48 retained maintenance warnings |
| Distribution and portable surface | PASS: 0 distribution-bearing records; portable repository surface accepted |

Two independent applied Ubuntu assessments from the clean LF prototype produced byte-identical canonical evidence with SHA-256 `d6cb8287777c96d5e20c3a013fcdc47bdbe359f098db5a5e5d44c981b649b428`. The complete candidate passed at 645 artifacts/48 warnings; exact released 0.5.0 observed only the retained full-checkout `E009` at 645 artifacts/47 warnings; and the exact two-omission view passed at 643 artifacts/47 warnings. The assessment used public wheel SHA-256 `974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f`, payload SHA-256 `d247cc48213b49be52345fcadbf2d93355e5ea7ef15b32014d9fc5010458a2bc`, sparse-spec SHA-256 `448159eec515975b9e7e946bed2653dbd6811dc4c06fd7b9e9d3a3facbd00332`, and dashboard-manifest SHA-256 `8e3ca1777cc8a0c9e17019251c47d334d504089d0be38ec35ae3b3c0f50e3d45`. Omitted path/blob/raw identities remained unchanged.

The live-worktree complete suite separately reported two expected snapshot failures because it includes the deliberately stopped untracked `RLS-SEH-008`; both clean qualification clones exclude that stopped file and passed. The stopped file remains untouched at SHA-256 `eea7a9953767e6b817754a517db72a2484561462fce1c9e440c5e5d1501a75fc`. No root-managed path, released evaluator, lock, rejected history, maintenance state, or external policy changed.

This correction and evidence remain uncommitted. `WO-REB-006` and `WO-REB-007` remain `in_progress`, `REL-SEH-010` remains `approved`, and amended `REL-SEH-011` remains `draft`. No operational C6 commit or branch, push, credential-bearing mutation, hosted dispatch, lifecycle transition, VREC/RLS action, tag, publication, deployment, maintenance mutation, external-policy change, or root-evaluator upgrade occurred. The next accountable boundary is separate authorization for one operational C6 candidate commit containing only this reviewed eight-path correction on top of C5, followed by exact local replay.
