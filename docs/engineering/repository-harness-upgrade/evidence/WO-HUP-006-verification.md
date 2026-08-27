# WO-HUP-006 implementation evidence

artifact: WO-HUP-006
checkpoint: handoff
formal_snapshot_sha256: 006d7b8c9574b9941cd292e16c4a59c35c22f77ef5e81adedd1bea304670449b

Retained by the implementation actor on 2026-08-27. This file is evidence. It
does not complete, verify, or release the work order.

## Outcome

The standard root moved from exact public 0.6.0 to exact public 0.7.0 in one
atomic `harnessctl upgrade` transaction run from the isolated 0.7.0
environment, with canonical evidence, a no-op replay, and the complete graph
validating under 0.7.0 with zero errors. The candidate moved to development
version 0.8.0 with its migration scenario. No release, tag, publication or
deployment byte moved.

## Repository and authorization

- Base commit: `main` at `7284743` (merge of pull request #188).
- Branch: `governance/hup-006-adopt-0-7-0`; packet approved
  2026-08-27T14:37:56Z, `WO-HUP-006` started 2026-08-27T14:38:01Z, both
  applied by the exact public 0.6.0 evaluator outside the checkout.
- Prior lock SHA-256:
  `978cebb7824b7928d95ed43897b0f848441cc4ab7403a0cdd08a55a77df2b79e`.
- Rehearsal: the whole transaction was first run in a throwaway worktree
  (apply, replay, doctor, validate, suite) before approval; its findings
  shaped the approved scope and the scope amendment below.

## Applying evaluator identity

- Environment: `C:\Users\mathi\se-harness-eval-070`, installed from the
  wheel file `se_harness-0.7.0-py3-none-any.whl` (PEP 610 archive digest
  recorded); an earlier index install was replaced because `identity`
  refused it with `RID022`.
- Wheel SHA-256: `e8f4fdc9ad60879a3fa4627c063fa7bb9513e2bd109c47258cf7f7aa6ecf27f3`
  (equal to the digest `RLS-SEH-015` binds and to PyPI's).
- Installed payload SHA-256:
  `26c11ec5e2363c3c0a9a416e69a3faa8bdf2d7a046710075bdeb661dd1003ee9`
  (`se-harness-installed-payload-v1`).
- `identity --role released-evaluator … --require-isolated-python
  --require-entry-point`: `passed: true`, schema
  `se-harness-runtime-identity-v3`, CPython 3.14.6, no diagnostics; proven
  before the plan and again immediately before `--apply`.

## Plan and transaction

- Plan: `summary: 61 files, 18 unchanged`, 43 add or update, zero
  `customized`, zero `conflict` — the set `SPEC-HUP-006` reviews.
- Apply: `harnessctl upgrade . --work-order WO-HUP-006 --evidence-output
  docs/engineering/repository-harness-upgrade/evidence/WO-HUP-006-evaluator-upgrade.json
  --apply` → `upgraded managed files to se-harness 0.7.0`, evidence retained
  (schema `se-harness-evaluator-upgrade-evidence-v1`, LF, zero CR bytes).
- Replay: `summary: 61 files, 61 unchanged`.
- Resulting lock: schema 3, `tool_version = "0.7.0"`, evaluator archive and
  payload digests as above, 55 managed files, 4 fragment files; lock SHA-256
  `44d0232c993c595d3182a6e9a029ae434ecfcf7405e58e9993cbc5fe88aec00d`.
- Root parity: the root workflow, policies and templates are now the 0.7.0
  copies; `templates/repository/standard/` is unchanged.

## Owner content and candidate version

- `AGENTS.md` owner region: names `se-harness==0.7.0` as the evaluator to
  install outside the checkout and identifies every one of the 55 managed
  paths (the skills by basename); trimmed to 5,968 bytes to stay under the
  6,000-byte bound while keeping every required fact.
- `docs/notes/developing-se-harness.md`: the candidate now reports 0.8.0 and
  the root is exact public 0.7.0, adopted by this work order.
- `pyproject.toml` and `se_harness/__init__.py`: `0.7.0` → `0.8.0`, the only
  product bytes that moved (`git diff` over `se_harness/`, `templates/`,
  `release/`: two lines) plus `README.md`'s install example, `0.7.0` →
  `0.8.0`, under the second scope amendment.
- `tests/fixtures/governance_migration/candidate-0.7.0-to-0.8.0.json`:
  written by the canonical writer from the retained
  `candidate-0.6.0-to-0.7.0.json`; `predecessor_facts derive` now yields the
  pair 0.7.0 → 0.8.0 with the 0.7.0 wheel digest. The retained pair stays.
- `.gitattributes`: the managed block is the 0.7.0 fragment (it now carries
  the three migration LF rules); the repository-owned copies of those rules
  **stay**, because `doctor` requires the `governance-migration-protocol`
  class in the repository region
  (`hash-bound-attribute-effective` fails without them). The draft's
  dedupe bullet is therefore not executed — deviation 1 below.

## Scope amendment, 2026-08-27

`repository_tools/predecessor_facts.py` was added to the execution scope by
the repository owner during implementation, for two measured defects:

1. `LEGACY_ACCEPTANCE_CONTRACT_SHA256` mapped only `0.6.0`; with the root at
   0.7.0 `derive` yielded no acceptance-contract digest and the
   candidate-package job refuses to run without one. The 0.7.0 verifier's
   contract digest equals 0.6.0's (`a443e93d…`, read from both installed
   evaluators); the map gained that entry.
2. `write-scenario` did not recompute `fixture.simulated_publication_sha256`,
   so the first written 0.7.0 → 0.8.0 scenario failed its own rehearsal at
   `adopt` with `MIG413`. The writer now recomputes
   `sha256(canonical_json({artifact_id, immutable: true, version}))`; the
   formula reproduces the stored digest of both retained scenarios, the
   scenario was rewritten (`bfd8ea17…`, 3,862 bytes), and the fixed writer
   reproduces it byte for byte.

A second amendment the same day added `README.md` for its install-example
line: `tests/test_progressive_documentation.py` and
`tests/test_public_onboarding.py` require the example to equal the package
version, as `WO-RLS-011` did when it moved to 0.7.0.

## Tests changed, for root assumptions only

| File | Assumption replaced |
| --- | --- |
| `tests/test_ci_pipeline.py` | root workflow was the unfiltered 0.6.0 copy; scenario paths and versions were literal `0.6.0`/`0.7.0`; now derived from the lock and the candidate (`0.9.0` as the next unwritten pair); `tomllib` imported |
| `tests/test_governance_migration.py` | `CANDIDATE` is `candidate-0.7.0-to-0.8.0.json`; the retained `candidate-0.6.0-to-0.7.0.json` is `PREVIOUS_CANDIDATE` and still rehearsed; `PUBLIC_PREDECESSOR_ARCHIVES` gains 0.7.0 |
| `tests/test_artifact_catalog.py` | root work-order template and router equal the candidate (0.7.0 carries the delegation table and the handoff section) |
| `tests/test_hash_bound_integrity.py` | the root managed block now carries the promoted patterns; the repository region still must |
| `tests/test_instruction_architecture.py` | 55 managed paths; `se-harness==0.7.0` |
| `tests/test_standard_repository_lifecycle.py` | the root managed block equals the 0.7.0 fragment |
| `tests/test_validation_taxonomy.py` | root `QUALITY_GATES.md` equals the candidate (authoring and release-unit predicates present) |

## Passing checks

| Command | Evaluator | Result |
| --- | --- | --- |
| `validate .` | 0.7.0 | **PASS** — 968 artifacts, 0 errors, 460 warnings, every plane E0 (maintenance W460: `W-AUT-004` 263, `W-AUT-003` 72, `W-AUT-002` 64, `W013` 24, `W015` 15, `W014` 14, `W024` 6, `W-AUT-001` 2 — the authoring-policy review warnings 0.7.0 adds over the existing graph; later governed work) |
| `doctor .` | 0.7.0 | **0 FAIL**, 143 PASS |
| `inspect .` | 0.7.0 | 968 artifacts, 3719 relations, 599 findings: 0 error, 474 warning, 125 info; 0 decisions required, 0 definitions pending, 0 assurance pending |
| `dashboard` twice | 0.7.0 | deterministic, manifest `ddd2fcc38b004b8974a818f72ca116edd17c2673386b568b56c724c105725e61` |
| `preflight . --work-order WO-HUP-006 --phase review` | 0.7.0 | **PASS** |
| `upgrade .` replay | 0.7.0 | 61 files, 61 unchanged |
| `python scripts/check_portable_release_surface.py --repository .` | candidate | PASS |
| `python scripts/validate_release_distributions.py --root .` | candidate | PASS, 3 distribution-bearing records |
| `python -m repository_tools.predecessor_facts derive --repository .` | candidate | version 0.7.0, candidate 0.8.0, scenario `candidate-0.7.0-to-0.8.0.json`, wheel `e8f4fdc9…` |
| `git diff --check` | git | clean |
| Seven changed test modules | candidate | 203 tests OK, 1 skip |
| `python scripts/run_tests.py --workers 8 --scale full` | candidate, Windows 11, CPython 3.14 | `Ran 995 tests in 92.937s (117 classes, 8 workers)` — `OK (skipped=24)` |
| `py -3.11 scripts/run_tests.py --workers 4 --scale full` | candidate, Windows 11, CPython 3.11 | `Ran 995 tests in 122.960s (117 classes, 4 workers)` — `OK (skipped=24)` |
| `scripts/validate_governor_transition.py assess --base-revision 7284743` with the 0.7.0 evaluator | candidate | needs a clean worktree: run on the candidate commit and recorded in the record's governance commit |
| `harnessctl check . --artifact WO-HUP-006 --checkpoint handoff …` | 0.7.0 and candidate | before this file existed: blocked only by `QGP-G4I-EVIDENCE`; formal snapshot above |
| Hosted | the pull request's lanes | pending the pull request |

## Deviations from the work order, recorded for the completion decision

1. **The `.gitattributes` dedupe was not executed.** The owner rules the
   draft proposed removing are required by the declared repository region of
   the `governance-migration-protocol` class; removing them makes 0.7.0
   `doctor` fail. They stay, duplicated with the managed block, and
   `tests/test_hash_bound_integrity.py` asserts both regions.
2. **Two defects fixed under a scope amendment** (above), in
   `repository_tools/predecessor_facts.py`.
3. **Maintenance warnings rise from 53 to 460 under the new root.** They are
   0.7.0's authoring-policy review warnings over the existing graph (string
   `verification_method`, long statements, multi-SHALL statements). None is
   an error; migrating the graph is later governed work.

## Changed-path ledger

38 paths against `main`: the 43 planned managed files (24 directories and
files as `git status` lists them) and the lock; `AGENTS.md`, `CLAUDE.md`
(fragment), `.gitattributes`; `pyproject.toml`, `se_harness/__init__.py`;
`repository_tools/predecessor_facts.py`; the new scenario; seven test
modules; `docs/notes/developing-se-harness.md`; this packet's work order,
index and evidence.

## Preserved boundaries

Release records, verification records, contracts, tags, `release/0.7`,
publication, replay and Pages workflows, `templates/repository/standard/`,
`README.md`, and external state are byte-identical to `main`. No commit,
push, pull request, verification, merge or deployment was performed by the
transaction.
