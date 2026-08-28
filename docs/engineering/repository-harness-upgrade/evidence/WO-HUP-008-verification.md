# WO-HUP-008 implementation evidence

artifact: WO-HUP-008
checkpoint: handoff
formal_snapshot_sha256: 41c0215e7cebd746fbd1612f81e4ca3aa7242c87d9ed7707060dddf52a5b7757

Retained by the implementation actor on 2026-08-28. This file is evidence. It
does not complete, verify, or release the work order.

## Outcome

The standard root moved from exact public 0.7.1 to exact public 0.8.0 by the
simple upgrade: one command from a wheel-file install outside the checkout,
no packet, no `--work-order`. The transaction document is
`WO-HUP-008-evaluator-upgrade.json` beside this file.

## Evaluators

- Applying and governing after apply: released `se-harness 0.8.0` installed
  into an isolated environment outside the checkout from the wheel file
  downloaded from PyPI (`pip download --no-deps se-harness==0.8.0`, then
  `pip install <wheel>`), invoked with `-I`. The wheel file's SHA-256 was
  measured before the install and again immediately before apply:
  `e08aab8a96c156f9e5edf99b9a28aad96c7cffe5b18c262a2598a6b6873fadeb`, equal
  to the wheel `RLS-SEH-017` binds and PyPI serves. Identity written by the
  installer: version `0.8.0`, payload
  `ea75cc53a518cfe0f027336f1a9aabfa301175a00410091f6c2f4b50ccd92eb5`,
  archive `se_harness-0.8.0-py3-none-any.whl` with that digest.
- Governing before apply: released 0.7.1 (wheel-file install, archive
  `ddd403cd…`) outside the checkout — packet approvals, start preflight.
- Candidate: this checkout, branch `governance/hup-008-adopt-0-8-0` off
  `main` at `2628627`.

## Plan and transaction

- `upgrade .` before apply: 61 files, 9 `update`, 52 unchanged; zero `add`,
  zero `customized`, zero `conflict`; every path inside the managed set the
  installer declares (`SPEC-HUP-008` rule 3). The nine:
  `.engineering-harness.toml`, `.gitattributes`,
  `.github/workflows/engineering-harness.yml`, `ENGINEERING_HARNESS.md`,
  `docs/engineering/QUALITY_GATES.json`, `docs/engineering/QUALITY_GATES.md`,
  `docs/engineering/WORKFLOW.json`, `docs/engineering/WORKFLOW.md`,
  `scripts/validate_engineering_artifacts.py`.
- `upgrade . --apply --evidence-output docs/engineering/repository-harness-upgrade/evidence/WO-HUP-008-evaluator-upgrade.json`:
  `upgraded managed files to se-harness 0.8.0`, evidence retained. (A
  first attempt on the throwaway rehearsal with an absolute evidence path was
  refused with `upgrade evidence path must be repository-relative` and wrote
  nothing; rule 4 records the relative form.)
- Replay `upgrade .`: 61 files, 61 unchanged.
- Lock after apply: schema 3, `tool_version 0.8.0`, evaluator
  `{version 0.8.0, payload_manifest se-harness-installed-payload-v1,
  payload_sha256 ea75cc53…, archive_name se_harness-0.8.0-py3-none-any.whl,
  archive_sha256 e08aab8a…}`. Prior lock in the transaction document:
  `6739fef03480d55e6d3ba7022068183ce4d60cae46a000a1582b78fec37e243a`,
  prior `tool_version 0.7.1`.
- After apply the root copies of the nine managed files are byte-identical
  to the candidate templates under `templates/repository/standard/`
  (`diff` empty for the validator and the quality gates): 0.8.0 is the
  candidate that was released.

## Readings under the 0.8.0 root, isolated mode

- `validate .`: PASS; structure E0/W0, governance E0/W0, policy E0/W0,
  maintenance E0/W473.
- `doctor .`: 0 FAIL.
- `qualify released-root`: RR001 runtime matches the target root lock;
  RR002 143/143 managed checks; RR003 artifacts=1072, errors=0,
  warnings=473; RR004 target state unchanged.
- `inspect .`: derived observation produced without error.
- `dashboard` twice: content directories identical; only
  `generation-summary.json`'s `generated_at` and `elapsed_ms` differ.
- `evaluator_facts derive` (candidate source): `version=0.8.0`,
  `wheel=se_harness-0.8.0-py3-none-any.whl`, `wheel_sha256=e08aab8a…`,
  `payload_sha256=ea75cc53…`, `acceptance_contract_sha256=` (empty: 0.8.0
  carries `qualify`, no legacy contract), `candidate_version=0.9.0`.
  Measured on the rehearsal export with the candidate still at 0.8.0:
  `PRE008: the candidate version 0.8.0 equals the declared root version`,
  which is why the candidate moves in this change.

## Owner content and candidate version

- `AGENTS.md` owner region: the install instruction reads
  `se-harness==0.8.0`.
- `docs/notes/developing-se-harness.md`: the candidate/root paragraph now
  states candidate 0.9.0 and root 0.8.0 (it had drifted to 0.6.0/0.7.0), and
  the root-evaluator paragraph names `WO-HUP-008`, the wheel-file install and
  the archive pair, and why this repository installs the root from the
  digest-verified wheel (`MG004` under the 0.7.1 root, `REL-SEH-019`).
- `.gitattributes` owner region: the comment on the retained migration rules
  now states that `WO-HUP-008` adopted 0.8.0 and that the files and rules are
  deleted together by issue #210's follow-up; the rules themselves stay.
- Candidate moved to `0.9.0`: `pyproject.toml`, `se_harness/__init__.py`,
  the README install example (`test_readme_version_matches_package_metadata`
  and `test_installation_is_short_released_and_upgrade_aware` require the
  README example to equal the package version). No scenario, no legacy map
  entry.

## Test assumptions replaced

Each module below carried a pin the rehearsal on the throwaway export
surfaced (1011 tests, 24 failures, 1 error before any change):

| Module | Assumption carried | Identity-aware form |
| --- | --- | --- |
| `tests/test_ci_pipeline.py` | `LEGACY_ACCEPTANCE_CONTRACT_SHA256[root]` exists (0.6.0, 0.7.1) | `.get(root)`, `None` for a root that carries `qualify`; `0.8.0` added to the forbidden literal set for repository-owned workflows |
| `tests/test_predecessor_bootstrap_retirement.py` | root validator copy carries the 16 retired names and differs from the candidate copy by the declared deletion ledger | reads the lock's evaluator version: under 0.7.1 the ledger; otherwise the root copy equals the candidate copy and the names are absent from both |
| `tests/test_validation_taxonomy.py` | root `QUALITY_GATES.md` lacks WO-ECP-009's markers | reads the lock's version: under 0.7.1 the declared divergence; otherwise root equals the candidate template |
| `tests/test_standard_repository_lifecycle.py` | root managed `.gitattributes` block is the 0.7.1 fragment with the migration rules | reads the lock's version: 0.7.1 fragment or the candidate fragment; the owner-region rules are still asserted |
| `tests/test_instruction_architecture.py` | owner region names `se-harness==<lock version>` | no test change; the owner content moved |
| `tests/test_progressive_documentation.py`, `tests/test_public_onboarding.py` | README and the note name the package version | no test change; README and the note moved |
| `tests/test_release_build.py` | `test_declared_mode_set_is_what_a_posix_export_already_carries` | not a root assumption: fails on this workstation before and after the move (file modes 420/493 in the export), passes hosted; unchanged |

`tests/test_upgrade_rehearsal.py` keeps its fake 0.7.1 predecessor defaults
by design (they name a scenario of the rehearsal, not this root) and passed
unchanged.

## Suite on the moved root

`python scripts/run_tests.py --scale full` with candidate source against the
moved root (CPython 3.12, this workstation): 1011 tests, 1 failure, 4 skips —
the failure is `test_release_build…test_declared_mode_set_is_what_a_posix_export_already_carries`,
the workstation file-mode condition named above, unchanged from before the
move; every root-pinned test named above passes.

## Readings over the complete change set (after every edit)
- `validate .`: Planes: structure E0/W0 | governance E0/W0 | policy E0/W0 | maintenance E0/W473
- `doctor .`: 0 FAIL
- `qualify released-root`: PASS RR002 managed-root: 143/143 managed checks passed;PASS RR003 engineering-graph: artifacts=1072; errors=0; warnings=473;

## Handoff check

`harnessctl check . --artifact WO-HUP-008 --checkpoint handoff --changed-path … --changes-complete` with released 0.8.0 outside the checkout: Completed over the 28 paths below; before this file carried the formal snapshot the only non-pass predicate was QGP-G4I-EVIDENCE, and before the change set was declared QGP-G4I-COMPLETE and QGP-G4I-PATHS. Formal snapshot as bound above.

## Complete changed-path set

Every path this work order changed since `main` at `2628627`, packet included:

```
AGENTS.md
docs/engineering/QUALITY_GATES.json
docs/engineering/QUALITY_GATES.md
docs/engineering/repository-harness-upgrade/architecture/ARCH-HUP-006.md
docs/engineering/repository-harness-upgrade/evidence/WO-HUP-008-evaluator-upgrade.json
docs/engineering/repository-harness-upgrade/evidence/WO-HUP-008-verification.md
docs/engineering/repository-harness-upgrade/README.md
docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-016.md
docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-017.md
docs/engineering/repository-harness-upgrade/specifications/SPEC-HUP-008.md
docs/engineering/repository-harness-upgrade/verification/VER-HUP-008.md
docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-008.md
docs/engineering/WORKFLOW.json
docs/engineering/WORKFLOW.md
docs/notes/developing-se-harness.md
.engineering-harness.lock
ENGINEERING_HARNESS.md
.engineering-harness.toml
.gitattributes
.github/workflows/engineering-harness.yml
pyproject.toml
README.md
scripts/validate_engineering_artifacts.py
se_harness/__init__.py
tests/test_ci_pipeline.py
tests/test_predecessor_bootstrap_retirement.py
tests/test_standard_repository_lifecycle.py
tests/test_validation_taxonomy.py
```
