# WO-HUP-001 implementation evidence

Date: 2026-08-20

## Result

The bounded standard-root upgrade is locally implemented and passes the required local checks when evaluated on its declared HUP-only candidate surface. `WO-HUP-001` may move to `implemented`, but it is not commit-bound verified: no candidate commit, candidate package, hosted run, VREC, push, pull request, merge, release, publication, deployment, or issue mutation was authorized or performed.

The RCV and 0.5.1 release packets remain draft in the separate drafting workspace. They were deliberately excluded from the projected HUP candidate because they are outside this work order's change surface.

## Authority and immutable baseline

- Approval: the accountable owner approved `INT-HUP-001`, `CAP-HUP-001`, `REQ-HUP-001` through `REQ-HUP-003`, `SPEC-HUP-001`, `ARCH-HUP-001` including its no-significant-decision assessment, `VER-HUP-001`, and `WO-HUP-001` for implementation while keeping the RCV and 0.5.1 release artifacts draft.
- Base revision: `1f67f15034a3f40e2ac7395ee99d866aa9e86442` (`origin/main` at implementation start).
- Applying distribution: immutable public `se-harness==0.5.0`, installed outside the checkout.
- Public wheel SHA-256: `974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f`.
- Released-evaluator identity: PASS under isolated Python; module, distribution, template, entry point, and interpreter origins were all below the external public 0.5.0 environment and outside the checkout; `PYTHONPATH` was absent and user site was disabled.

The first console-entry-point identity attempt failed safely with `RID017` because the launcher was not running Python isolated mode. The successful retry used the same external interpreter with `-I`. A later read-only invocation used an incorrect identity option name and exited at argument parsing; it made no repository change.

## Governing preflight

The released 0.5.0a1 evaluator ran start preflight before mutation:

- work order: `WO-HUP-001`
- phase: `start`
- result: PASS, `ready: true`, no diagnostics
- manifest: 16 files

The implementation actor read all 16 manifest files before changing the work order to `in_progress` or applying the upgrade.

## Upgrade transaction

The external public 0.5.0 dry run reported exactly three managed updates:

- `.engineering-harness.toml`
- `.github/workflows/engineering-harness.yml`
- `ENGINEERING_HARNESS.md`

The supported `upgrade . --apply` transaction updated those files and reconciled `.engineering-harness.lock`. It reported success at 0.5.0. A post-apply dry run reported `34 files, 34 unchanged`.

The owner-curated `docs/engineering/REPOSITORY_CONTEXT.md` was then updated only to identify exact released 0.5.0 as the repository evaluator.

### Managed canonical digests

| Path | 0.5.0a1 baseline SHA-256 | 0.5.0 result SHA-256 |
|---|---|---|
| `.engineering-harness.toml` | `e619955cdcd3cd4ec7e7c8ebf16f91afc1660e1137c49990bec8a51d1ddec844` | `122083cefba68aec9900606f9457744a10d96b8f48b91b4908e20e591dd5a83f` |
| `.github/workflows/engineering-harness.yml` | `373947fa2ec36b1d69ee6c2fa6fe118fec8d1ed1f14ba06e11297274ed31c5f6` | `a4fd7bef3b307ed6a007bf914f9ab7ab11d8591c163fb8b4cfc2736630341a43` |
| `ENGINEERING_HARNESS.md` | `ac62721f3de8170aa60bc62273c7902926024fe2a6dcd5f9a8055e349aae7cd0` | `00aa0afd3a7708aad861944169dd120daa4f3a4443169d747717ae4f3814fa42` |

The schema-2 lock records `tool_version` 0.5.0. Its file SHA-256 is `08441ec0b4825db4c017ce4169f23092162995ff06476004d267f0671c7443b3`. The owner-curated repository-context SHA-256 is `bbb6b11df3dbba6a6cd24ec4ac3ceca84c173a996fb27e25a96c21fdfd8c368f`.

## HUP-only projected candidate

Because the drafting workspace also retains separately authorized draft RCV and 0.5.1 packets, a detached projection was created from the exact base revision and populated only with:

- the four installer-owned managed/lock changes;
- the owner-curated repository-context change;
- the engineering-domain index entry for the HUP packet; and
- the approved/implemented HUP packet and this evidence.

No RCV, release-0.5.1, product, package, publisher, Pages, or issue surface was copied into the projection. This projection is not a commit and has no external authority; it exists only to test the exact future HUP candidate surface.

## Verification results

| Check | Result |
|---|---|
| External 0.5.0 released-evaluator identity | PASS |
| Upgrade replay after apply | PASS: 34 unchanged |
| `doctor` under external 0.5.0 | PASS; 15 inherited W013 placement warnings |
| Formal graph validation on HUP-only projection | PASS: 531 artifacts; structure, governance, and policy E0/W0; maintenance E0/W44 |
| Inspection on HUP-only projection before completion transition | PASS: no decision required, no draft definitions, one active HUP work order |
| Review preflight after completion transition | PASS: `ready: true`, no diagnostics, 16-file manifest, work order `implemented` |
| Inspection after completion transition | PASS: no active work; one expected assurance-pending item for `WO-HUP-001` |
| Dashboard on HUP-only projection | PASS: 531 artifacts, 1,928 relations, topology 519,362 bytes of 524,288, target not exceeded |
| Default-runtime unit suite | PASS: 263 tests, 4 skipped |
| Python 3.11.9 unit suite | PASS: 263 tests, 4 skipped |
| CLI help smoke test | PASS |
| Release-distribution record validator | PASS: zero distribution-bearing records in this non-release candidate |
| `git diff --check` on HUP-only projection | PASS; host emitted only line-ending conversion notices |
| Product/package/publisher/Pages diff audit | PASS: no changes under `se_harness/`, `templates/`, package metadata, repository tools, candidate evidence, PyPI publisher, or Pages publisher |

The repository test suites exercise the managed consumer workflow contract, including exact version installation, read-only permissions, isolated evaluator execution, selected-work-order review preflight, doctor, validation, and dashboard commands.

## Mixed-workspace observation

Running the same full suite directly in the combined drafting workspace produced one identical failure on both runtimes: `test_progressive_bundle_is_deterministic_partitioned_and_bounded` measured a 533,114-byte topology against the 524,288-byte limit. That workspace contained 544 artifacts and 1,980 relations because it also included the 13 draft RCV/release definitions.

The HUP-only projection reduced the topology to 519,362 bytes and both suites passed. A clean pre-packet comparison generated 522 artifacts, 1,905 relations, and a 511,398-byte topology. This establishes that the failure was caused by combining independently scoped governance packets, not by the 0.5.0 evaluator upgrade or product behavior. The correction is candidate separation; no capacity threshold or product code was changed.

## Candidate and hosted checks not yet available

- Candidate-source identity correctly returned `RID015` when attempted without a candidate commit. No commit was authorized, so no commit identity was invented.
- Candidate-package acceptance was not run because no candidate build or candidate commit was authorized, and this work order changes no package source.
- Hosted Engineering Harness and candidate-evidence checks require a pushed exact candidate commit and therefore remain pending.
- Review preflight passed after the local `implemented` transition. Commit-bound assurance still requires a later exact candidate, hosted evidence, ready VREC, and accountable verification.

## Rollback and residual risk

The 0.5.0a1 baseline is recoverable from the base revision. The current changes remain uncommitted, so no remote rollback is necessary. The main residual risk is accidentally combining the draft RCV/release packets with the later HUP candidate; any candidate authority should explicitly require an HUP-only commit. Service availability, branch protection, and hosted runner behavior remain external until that commit is pushed under separate authority.

## Unperformed actions

No candidate commit, VREC preparation or transition, push, pull-request mutation, merge, tag, GitHub Release, PyPI publication, Pages deployment, protected-environment decision, issue #81 edit, force push, or history rewrite was performed.
