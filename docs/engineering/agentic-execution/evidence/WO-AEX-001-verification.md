# WO-AEX-001 implementation verification evidence

This file records implementation-phase evidence for `WO-AEX-001`. It is not an
assurance decision, verification record, release record, or authorization for
external action. After accountable review of this evidence, the engineering
owner accepted the implementation and transitioned the work order to
`implemented` at `2026-08-24T09:46:24Z`. The open items below remain explicit
inputs to independent assurance review.

artifact: WO-AEX-001
checkpoint: handoff
formal_snapshot_sha256: ae46f1115467f43473dc665e5e0bbfb2f43462cb8551c64a5963e66613429a0d

## Candidate and evaluator identity

- Candidate source version: `0.6.0`.
- Candidate base commit observation:
  `db704964139d6c2d88c9aabbf64848a9cf4eadc8`. The working tree contains the
  uncommitted implementation and is not commit-bound evidence.
- Candidate-source identity command used `python -S -B` to disable the
  unrelated system distribution and user site. Result: passed with module and
  template origins inside the checkout.
- Exact released evaluator: `se-harness 0.6.0`, invoked through an external
  isolated interpreter.
- Released wheel:
  `se_harness-0.6.0-py3-none-any.whl`.
- Released wheel SHA-256:
  `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`.
- Released payload SHA-256:
  `c233678548fe742b7a7a5a8bd65de10156ff233edc65b68e2ed0333fbe4dea42`.
- Released identity result: passed, with isolated Python, user site disabled,
  `PYTHONPATH` absent, and exact archive and payload agreement.
- Runtime used for candidate tests: CPython `3.14.6` on Windows.

## Implemented result

- Added strict `se-harness-skill-contract-v1` parsing with duplicate-key,
  unknown-field, type, enum, operation-matrix, authority, delegation,
  retention, size, and canonical-JSON checks.
- Added deterministic `se-harness-skill-manifest-v1` generation over regular
  UTF-8 text normalized by `utf8-text-lf-v1`, with portable paths, stable
  ordering, content SHA-256 values, and a canonical manifest digest.
- Added one canonical portable core at
  `templates/repository/standard/.agents/skills/harness-orient/` containing
  `SKILL.md`, `skill-contract.json`, and `scripts/orient.py`.
- Added no `se_harness/skills/` copy, provider adapter, worker profile,
  subagent, workflow engine, CLI command, dependency, or runtime-specific
  configuration.
- Kept the existing generic recursive installer unchanged because verifier
  cases proved that it already installs, locks, upgrades, preserves
  customization, and rolls back the nested managed core correctly.
- Added explicit source-distribution and wheel data declarations.
- Added public orientation, installation, upgrade, capability-fallback, and
  troubleshooting guidance.

## Portable identities

- Skill name and version: `harness-orient` `1.0.0`.
- Portable-core SHA-256:
  `73d94b02dd1008f5cb8b6a828ba920c128d06b82fc6e4b9b97720b6d91ca7cea`.
- Independent canonical receipt vector SHA-256:
  `96701a0b7b7c0d7fa15decd2cec59f49a46ce730317644a07e2c6aff90c845b0`.
- Exact-evaluator orientation receipt SHA-256 for selected
  `WO-AEX-001`:
  `87d28c8f3ef7af15cf9fdbbbddca99421a7fe7126ffb494aa79c4b68ee8cfece`.

The exact-evaluator orientation completed with evaluator identity passed,
`WO-AEX-001` lifecycle state `in_progress`, 50 unrelated background
observations, no scoped or repository blockers, and zero changed paths. Its
repository and Git-reference before/after digests matched.

## Commands and results

| Check | Result |
| --- | --- |
| `python -B -m unittest discover -s tests -p "test_*.py" -v` | Passed: 511 tests in 286.957 s; 11 platform-capability skips |
| `python -B -m unittest tests.test_agentic_execution -v` | Passed: 19 tests; 2 Windows capability skips |
| skill-creator `quick_validate.py` on the canonical core | Passed: `Skill is valid!` |
| AST parse of the module, portable runner, fake evaluator, and focused tests | Passed: 4 files |
| candidate `python -B -m se_harness validate .` | Passed: 725 artifacts, 0 errors, 50 pre-existing maintenance warnings |
| exact released `identity` | Passed with exact 0.6.0 wheel and payload digests |
| exact released `doctor .` | Passed all installed integrity checks |
| exact released `validate .` | Passed: 725 artifacts, 0 errors, 50 pre-existing maintenance warnings |
| exact released review preflight | Passed for `WO-AEX-001`; read-only and non-authoritative |
| exact released `harness-orient` against this repository and `WO-AEX-001` | Completed with zero changed paths |
| verifier-owned non-promotable ephemeral-wheel inventory and fresh installation | Passed; three canonical skill files appeared once and installed byte-identically |
| fresh standard installation, managed lock, customized-skill upgrade conflict, and interrupted-upgrade rollback | Passed |
| exact released handoff checkpoint with the complete 18-path implementation manifest | Passed; `WO-AEX-001` remains `in_progress` and the engineering-owner decision is not applied |
| `git diff --check` and trailing-whitespace scan of tracked and new implementation files | Passed; line-ending materialization warnings only |

The ephemeral wheel was created in a temporary directory named as
non-promotable, installed only into disposable fixtures, and deleted by fixture
cleanup. It was not retained as a release candidate.

## Capability matrix exercised

| Capability | Exact released 0.6.0 | Verifier-owned 0.5.0 profile fixture |
| --- | --- | --- |
| version | passed | passed |
| released identity | passed | emulated public success |
| doctor | passed | emulated public success |
| validation JSON | passed | passed |
| inspection JSON | passed through the exact orientation run | passed |
| selected focus JSON | passed | deliberately unavailable |
| unavailable-focus behavior | not applicable | `degraded`; selected scope only became `not_assessable` |
| candidate-source fallback | not used | prohibited and not used |

The 0.5.0 column is deterministic verifier-fixture coverage of the approved
public capability contract. It is not evidence from an independently installed
published 0.5.0 wheel.

## Negative, security, and no-write evidence

- Duplicate and unknown contract fields, authority-like mutation classes,
  enabled delegation, target receipt retention, floats, missing required
  files, invalid UTF-8, reserved names, line-ending variants, changed bytes,
  and symlink cases are covered.
- POSIX tests additionally cover portable case collisions and alternate path
  separators. Those and unprivileged symlink creation are skipped on this
  Windows host and remain active in the test corpus for a capable host.
- Black-box orientation covers missing and old evaluators, identity failure,
  managed-integrity failure, invalid graphs, malformed required JSON, bounded
  oversized output, candidate/released version skew, secret-bearing repository
  content, selected scope, explicit preflight failure, and absence of focus in
  the 0.5.0 profile.
- Host paths and secret values are redacted from bounded failure diagnostics.
  Repository file content and candidate version text do not enter governing
  output.
- The runner uses structured argument arrays with `shell=False`, removes
  inherited `PYTHONPATH`, disables user site for the child, uses no stdin, and
  invokes no network or credential interface.
- Repository bytes and Git references are independently hashed before and
  after orientation. Healthy and required-failure cases retain identical
  snapshots and an empty `changed_paths` array.
- Skill instructions require exact-evaluator version, identity, and doctor
  checks before a bundled helper becomes trusted execution input. The helper
  repeats those checks for the receipt.

## Changed implementation paths

- `MANIFEST.in`
- `README.md`
- `pyproject.toml`
- `se_harness/skill_contract.py`
- `templates/repository/standard/.agents/skills/harness-orient/SKILL.md`
- `templates/repository/standard/.agents/skills/harness-orient/skill-contract.json`
- `templates/repository/standard/.agents/skills/harness-orient/scripts/orient.py`
- `tests/fixtures/agentic_execution/canonical_vectors.json`
- `tests/fixtures/agentic_execution/fake_evaluator.py`
- `tests/test_agentic_execution.py`
- `tests/test_instruction_architecture.py`
- `tests/test_public_onboarding.py`
- `tests/test_release_build.py`
- `tests/test_standard_repository_lifecycle.py`
- `docs/notes/harness-orient.md`
- `docs/notes/harness-installation-and-upgrades.md`
- `docs/notes/README.md`
- `docs/engineering/agentic-execution/evidence/WO-AEX-001-verification.md`

Every implementation path is admitted by the `WO-AEX-001` execution scope.
The work-order lifecycle event and the previously approved Phase 1 artifact
packet are separate governed changes that preceded implementation.

## Open verification items and deviations

1. No independently installed published exact 0.5.0 evaluator is available in
   this no-network workspace. The required released-wheel 0.5.0 version,
   identity, doctor, validation, inspection, and reduced-focus evidence remains
   open for independent verification.
2. The AEX-specific symlink and case-collision filesystem cases require a host
   that can create those entries. The tests remain enabled where supported.
3. The exact candidate commit is intentionally bound by the subsequent VREC,
   because this evidence file is contained in that candidate and cannot name
   its own commit. A candidate wheel built through the real build backend,
   cross-platform run, and independent commit-bound assurance evidence remain
   open. Installing missing build or 0.5.0 inputs was not performed.
4. The non-promotable wheel is a verifier-owned standard-library fixture driven
   by the explicit packaging inventory. It proves installed behavior but does
   not substitute for a later real build-backend distribution assessment.
5. Formal orientation performance measurements at 100, 500, and 1,000
   artifacts remain for the independent verification run. Existing full-suite
   workflow scale evidence passed at those sizes but is not relabeled as
   orientation-specific evidence.

The engineering owner accepted the implementation with these deviations visible
and transitioned `WO-AEX-001` to `implemented`. That decision does not verify
the candidate; the assurance owner must independently accept, reject, or defer
the subsequent ready VREC after reviewing every open item.

## Intentionally not performed

At the implementation checkpoint, no autonomy envelope, delegated mutation,
subagent, worker, adapter, new CLI, workflow-policy change, managed-root
refresh, commit, branch, push, pull request, verification record, assurance
decision, release record, tag, publication, deployment, installation into a
user environment, network access, credential use, or external action was
performed. Candidate commit and ready-VREC preparation are later, separately
authorized governance steps.
