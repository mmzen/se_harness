# WO-REB-006 local implementation and qualification evidence

Date: 2026-08-22

## Authority and lifecycle boundary

This evidence covers only the approved local implementation and qualification of `WO-REB-006`. The work order remains `in_progress`; `REL-SEH-010` remains `draft`. No candidate commit, push, credential use, hosted dispatch, VREC/RLS preparation or transition, tag, publication, deployment, maintenance mutation, external-policy change, or root-evaluator upgrade occurred.

The operational baseline remained governance commit `5e8538c617809f843fd9d38b54c2210caa3a0e17`, tree `5776485189b92533bbbb878d4f3e15a0544e0d46`. The reviewed implementation has no candidate commit identity yet.

## Implemented behavior

- Candidate release-version cardinality counts only `ready` and `released` records. Valid rejected records remain audit history; two active records for one version still fail.
- Ordinary future `prepare-release` applies the same active-status rule.
- `scripts/prepare_predecessor_release.py` plans or applies one contract-derived compatibility operation. It accepts no user-supplied omission pattern.
- The adapter derives one exact rejected predecessor-bootstrap RLS/REL pair, records their committed Git blob and raw LF identities, creates a no-local detached sparse clone at the exact clean source commit, verifies the sparse file and materialized path set, and invokes exact external predecessor `prepare-release` with isolated Python.
- Installed predecessor payload identity must equal the contract-pinned wheel payload before output is accepted.
- Plan mode creates no repository output. Apply exclusively creates only the predecessor-generated ready RLS and canonical `se-harness-predecessor-preparation-view-v1` sidecar, rechecks source/history around each write, rolls back its new outputs on failure, and is idempotent for an already complete exact pair.
- Candidate validation binds the exact view, command, candidate/VREC/work scope, evaluator tuple, sparse digest, historical bytes, and predecessor-output digest. Independent publication replay recomputes the source/tree/blob/raw identities and predecessor-generated ready record from Git history.
- The existing evaluator binder remains the separate operation that attaches `se-harness-predecessor-bootstrap-v1` evaluator evidence. The root schema-2 lock and released evaluator remain unchanged.

## Exact rejected-history preservation

| Path | SHA-256 observed before and after qualification |
| --- | --- |
| `docs/engineering/release-0-6-0/releases/RLS-SEH-009.md` | `e0b8952953e8e180c6d572fe5d1236fded7104e623cc336bb9a93cd3b978f9e3` |
| `docs/engineering/release-0-6-0/release/REL-SEH-008.md` | `24e0962f6957e7501159a223913e16ef82b22e5e1ae1a88174b9887b43cb4aec` |

The separately stopped user-owned untracked `docs/engineering/release-0-6-0/releases/RLS-SEH-008.md` remained untouched at SHA-256 `eea7a9953767e6b817754a517db72a2484561462fce1c9e440c5e5d1501a75fc`. It was excluded only from the disposable qualification view; it was not deleted, moved, edited, staged, or committed.

## Verification observations

| Check | Result |
| --- | --- |
| `python -m unittest tests.test_predecessor_preparation -v` | PASS, 7 tests |
| release-bootstrap, publication, and workflow-documentation focused regression | PASS, 38 tests |
| release-bootstrap plus revision-provenance regression | PASS, 61 tests, 1 platform skip |
| disposable reviewed-source full suite: `python -S -m unittest discover -s tests -p "test_*.py"` | PASS, 435 tests, 5 platform skips |
| candidate formal graph in the same disposable view | PASS, 637 artifacts, 0 errors, 48 retained legacy maintenance warnings |
| `python scripts/validate_release_distributions.py --root .` in the disposable view | PASS, 0 distribution-bearing records at this pre-candidate stage |
| candidate CLI import and parser: `python -S -m se_harness --help` | PASS |
| changed Python syntax compilation and `git diff --check` | PASS |
| protected root/config/managed-script diff | PASS, zero diff |

The adapter integration tests use real temporary Git repositories, commits, clones, sparse checkout, path enumeration, exclusive writes, rollback, and publication-history replay. The released-runtime process and payload functions are replaced with deterministic test doubles in those adapter tests; unchanged bootstrap-binding tests separately exercise external runtime origin, wheel, lock, payload, and atomic-binding behavior. No operational successor contract/VREC exists yet, so no real `RLS-SEH-011` preparation was attempted or authorized.

## Negative and matrix coverage

- rejected plus one ready successor passes active-version cardinality; two ready successors fail;
- mixed or changed rejected bootstrap history continues to fail existing bootstrap validation;
- partial destinations fail without repair or overwrite;
- injected second-write failure removes the exclusively created evidence file;
- source/history mutation between writes is detected and the new pair is rolled back;
- installed payload versus exact-wheel payload mismatch fails before output;
- a third sparse omission is independently detected as an unexpected missing path;
- changed command arguments fail candidate validation and publication replay even when the sidecar digest is recomputed;
- preparation evidence must be canonical compact UTF-8/LF JSON with a raw SHA-256 binding;
- default-Windows CRLF checkout source and canonical-LF installed output are compared using the declared LF normalization contract;
- full-suite candidate dashboard tests now load the candidate validator explicitly and cannot inherit the released root validator through process-global import order.

## Reviewed uncommitted change surface

Governance and evidence:

- `docs/engineering/released-evaluator-boundary/requirements/REQ-REB-011.md`
- `docs/engineering/released-evaluator-boundary/requirements/REQ-REB-012.md`
- `docs/engineering/released-evaluator-boundary/specifications/SPEC-REB-005.md`
- `docs/engineering/released-evaluator-boundary/architecture/ARCH-REB-004.md`
- `docs/engineering/released-evaluator-boundary/architecture/adr/ADR-REB-004.md`
- `docs/engineering/released-evaluator-boundary/verification/VER-REB-004.md`
- `docs/engineering/released-evaluator-boundary/work-orders/WO-REB-006.md`
- `docs/engineering/released-evaluator-boundary/evidence/WO-REB-006-local-qualification.md`
- `docs/engineering/release-0-6-0/release/REL-SEH-010.md` (`draft` only)

Implementation, replay, tests, and operator documentation:

- `se_harness/provenance.py`
- `repository_tools/predecessor_preparation.py`
- `scripts/prepare_predecessor_release.py`
- `templates/repository/standard/scripts/validate_engineering_artifacts.py`
- `.github/scripts/publish_dashboard.py`
- `tests/test_predecessor_preparation.py`
- `tests/test_release_bootstrap.py`
- `tests/test_dashboard_webui.py`
- `tests/test_workflow_documentation_contract.py`
- `docs/notes/developing-se-harness.md`
- `docs/notes/harnessctl-reference.md`

## Qualification-view disclosure

The operational working tree intentionally contains the stopped untracked `RLS-SEH-008`, whose incomplete evaluator binding produces candidate diagnostic `E012` if indiscriminately scanned. The authoritative local full-suite and graph run therefore used a disposable bundle-backed clone overlaid with every reviewed change and omitted only that exact stopped path. Candidate graph validity was independently confirmed in that view. This omission is qualification hygiene for a user-owned stopped artifact, not the predecessor preparation view and not a validation bypass in product code.

## Post-candidate exact replay (uncommitted retention update)

The reviewed C4 implementation was committed locally as exact candidate `b099a2728d945ee705c1f956ec012f9730df15ac`, tree `3ee3cdc2b801ebf8b3166589e010f82ea8d40512`, with sole parent `5e8538c617809f843fd9d38b54c2210caa3a0e17`. The candidate commit contains exactly the 20 reviewed paths listed above. It does not contain the stopped untracked `docs/engineering/release-0-6-0/releases/RLS-SEH-008.md`, which remained untouched at SHA-256 `eea7a9953767e6b817754a517db72a2484561462fce1c9e440c5e5d1501a75fc`.

An exact Git bundle of that immutable candidate, including committed history and tags but no working-tree overlay, was cloned to a disposable directory and checked out detached at the candidate identity. The clone was clean before and after replay.

| Exact-candidate check | Result |
| --- | --- |
| `python -S -m unittest discover -s tests -p "test_*.py"` | PASS, 435 tests in 212.437 seconds, 5 platform skips |
| candidate formal graph | PASS, 637 artifacts, 0 errors, 48 retained legacy maintenance warnings |
| `python -S scripts/validate_release_distributions.py --root .` | PASS, 0 distribution-bearing records |
| `python -S -m se_harness identity --role candidate-source --expected-version 0.6.0 --expected-root <exact-clone> --checkout-root <exact-clone> --candidate-commit b099a2728d945ee705c1f956ec012f9730df15ac` | PASS; schema `se-harness-runtime-identity-v3`, version `0.6.0`, candidate commit and source/template roots exact, no diagnostics |
| `python -S -m se_harness --help` | PASS |

This post-candidate section is a retention-only working-tree update and remains deliberately uncommitted pending separate governance authority. No push, credential use, hosted dispatch, lifecycle transition, VREC/RLS preparation, tag, publication, deployment, maintenance mutation, external-policy change, or root-evaluator upgrade occurred.
