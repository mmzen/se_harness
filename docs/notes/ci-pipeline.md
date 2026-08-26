# The CI pipeline and the release path

Repository-owned note. It records the measured shape of the continuous
integration and release path so that each work order of the `ci-pipeline`
domain can show what it removed. Authority stays with the formal artifacts
under `docs/engineering/ci-pipeline/`.

## Question this note answers

Why does the pipeline feel slow when every run finishes in minutes, and
what does each simplification increment change?

## Baseline, measured 2026-08-26 at `e98b788`

Runner wall-clock, last twelve runs per workflow: every workflow between
under one minute and five minutes. The cost is multiplication, not duration.

| Workflow | Trigger | Jobs | Steps | Role |
| --- | --- | ---: | ---: | --- |
| `engineering-harness.yml` (managed) | push + PR, unfiltered | 1 | 9 | governing evaluator: preflight, doctor, validate, dashboard |
| `candidate-evidence.yml` | push + PR, unfiltered | 7 | 44 | suite, wheel, predecessor acceptance, migration x2 platforms x2 runs, integration package |
| `predecessor-evaluator-assessment.yml` | push + PR, unfiltered | 1 | 9 | evaluator-transition plan and assessment |
| `publication-rehearsal.yml` | PR + push to `main`, cancelling | 2 | 10 | re-executes the release qualification on two platforms; digest-checks `publish-pypi.yml` |
| `release-candidate-replay.yml` | dispatch | 1 | 6 | hosted replay of the bound recipe |
| `publish-pypi.yml` | dispatch, `main` | 7 | 44 | resolve, qualify, tag and release, PyPI, Pages, observe |
| `publish-dashboard-pages.yml` | dispatch, `main` | 2 | 17 | standalone copy of the Pages jobs |

Totals: 1,963 lines of YAML, 21 jobs, 139 steps. Scripts under
`.github/scripts/`: 6,490 lines (`rehearse_publication.py` 3,187,
`publish_dashboard.py` 1,465, `build_integration_package.py` 1,038,
`publish_release.py` 540, `reconcile_maintenance_branch.py` 260).

Per push to an open pull request, on one commit:

| Work | Times |
| --- | ---: |
| full `unittest discover` | 4 |
| candidate wheel build | about 14 |
| install of the public predecessor evaluator | about 10 |
| nine-stage migration rehearsal | 8 |
| verification of the integration payload | 3 |
| checkout-cleanliness proof (same three lines) | 7 copies |

Release governance for 0.7.0: five release contracts (`REL-SEH-012` to
`REL-SEH-016`), four rejected because a work order reached `implemented`
after the allow-list was frozen; three release work orders; the approved
contract is 68 KB and `WO-RLS-011` is 39 KB. Since `v0.6.0`: 265 commits,
40 merged pull requests, 117 `docs` and `governance` commits against 26
`feat` and `fix`.

## What each increment changes

| Work order | Proposal | Removes | Measured after |
| --- | --- | --- | --- |
| `WO-CIP-001` | P1, P2 | the second run per push; two of three workflow-level wheel builds; the reconcile-only job | implemented 2026-08-26, see below |
| `WO-CIP-002` | P3, P5 | the Python copy of the qualification, the YAML parser and the digest file; the idle schema leg; the duplicated Pages jobs | implemented 2026-08-26, see below |
| `WO-CIP-003` | P6 | three hand-edited constants and the silent skip on a version bump | implemented 2026-08-26, see below |
| `WO-CIP-004` | P4 | the reject-and-re-issue loop on the release contract | implemented 2026-08-26, see below |

The "Measured after" column is filled by each work order's evidence.

### After `WO-CIP-001`

- `candidate-evidence.yml`, `predecessor-evaluator-assessment.yml` and the
  standard template of `engineering-harness.yml`: `push` restricted to
  `main`, `release/**`, `candidate/**`; a cancelling concurrency group per
  workflow and ref. One run per commit on a pull request instead of two.
  The hash-locked root `engineering-harness.yml` follows at the root-evaluator
  upgrade.
- `candidate-evidence.yml`: six jobs instead of seven. The wheel is built
  once in `candidate-source` and handed down as
  `candidate-wheel-non-promotable-<sha>` with `SHA256SUMS`; `candidate-package`
  and both migration legs verify and never rebuild. Workflow-level wheel
  builds of the commit: 3 to 1. The cross-platform migration comparison is a
  step on job outputs, not a job.
- Kept, and why: the two migration runs per platform (`REQ-REB-017`'s
  determinism example); the integration package's own two builds and its
  retention job (`SPEC-IPK-001` rules 1 and 5: a different distribution with a
  local-version overlay, byte-equal across two builds, retained only after
  every matrix member passes).
- Per pull-request push, one commit: full suite 2 (was 4); wheel builds 5
  (was about 14: 1 candidate + 2 integration in `candidate-evidence`, 2 in
  the rehearsal, which `WO-CIP-002` addresses); predecessor installs about 5
  (was about 10); migration rehearsals 4 (was 8).

- Hosted reading, pull request #171 at `ff44da2` (2026-08-26): 13 checks
  pass; the repository-owned workflows ran on `pull_request` only and the
  superseded commit's runs were cancelled by the concurrency group; the root
  0.6.0 managed workflow still ran on `push` as well. The `candidate-evidence`
  log shows one `pip wheel` (in `candidate-source`), `candidate-package`
  verifying `SHA256SUMS: OK`, and the integration build comparing the two
  platforms' migration digests (`1bcca199…`). These are `VER-CIP-001`
  scenarios 1 and 2.

### After `WO-CIP-002`

- One release-qualification definition, `.github/workflows/release-qualification.yml`
  (`workflow_call`, `contents: read`, no secret input, Linux): resolve the
  record, qualify the candidate, replay the bound recipe twice, verify the
  bundle. `publish-pypi.yml`'s `qualify` job and both jobs of
  `publication-rehearsal.yml` are callers. `rehearse_publication.py`
  (3,187 lines), `publication_rehearsal_mechanics.json` (364 lines), the
  `divergence` job, the PyYAML install, and `tests/test_publication_rehearsal.py`
  (2,299 lines) are gone.
- One Pages definition, `.github/workflows/pages-publication.yml`; `publish-pypi.yml`
  and `publish-dashboard-pages.yml` are callers (the standalone workflow is
  42 lines, was 259). The idle schema-1 qualification leg is gone; a schema-1
  record is refused by the definition.
- `.github/scripts/`: 6,490 lines to 3,277, plus `repository_tools/json_bytes.py`
  (90 lines) holding the one definition of canonical JSON, duplicate-key
  refusing parsing and file hashing; `reconcile_maintenance_branch.py` uses
  `gh api`; `classify-pypi` is deleted (the PyPI job executes no repository
  code by policy, so it classifies inline).
- Workflow YAML: 1,963 lines to 1,984. The definitions moved into two files;
  the YAML did not shrink, the copies did.
- Per pull-request push: the rehearsal no longer runs the unit suite twice on
  two platforms with two `python -m build` pairs each; it runs the
  qualification once (candidate mode) plus, when a schema-2 record exists,
  once for that record.

- Correction, 2026-08-26: the hosted run of pull request #172 showed that
  `WO-CIP-003`'s `governance-migration` job did not list `candidate-source`
  in its `needs`, so the derived outputs it consumes were empty. Fixed under
  `WO-CIP-002` by the owner's decision, with a test that every
  `needs.<job>.outputs` reference in every workflow names a job in the
  consumer's `needs`. `VREC-CIP-003` remains the record of the commit that
  carried the defect.

### After `WO-CIP-004`

- `RELEASE_CONTRACT.template.md` (standard template) carries
  `candidate_commit` and `previous_release_tag`, a "Release unit" section
  stating that `gates` is measured, and a stop condition that names a
  differing census or a non-ancestor candidate — not a later merge to `main`.
  The 0.6.0 root validator accepts the two fields as unknown keys (measured:
  913 artifacts, 0 errors with them added to an approved contract).
- `harnessctl release-unit` (`se_harness/release_unit.py`): the census from
  the trailers on the first-parent history, merges contributing their merged
  commits' trailers; statuses and packaged-surface flags from the catalog;
  `--contract` compares and reports `E-CIP-001`; `--toml` prints the array.
- Measured over `v0.6.0..e98b788` (the `main` the 0.7.0 contracts were
  drafted on): see the WO-CIP-004 evidence for the census and its comparison
  with `REL-SEH-015`'s thirty-six gates.

### After `WO-CIP-005`

- `release_unit_ready`, an evaluator in the closed set, bound as
  `QGP-G5P-RELEASE-UNIT` on `QG-G5-RELEASE-PREPARATION` and applied when a
  release contract leaves `draft`: a contract naming a `candidate_commit`
  is re-measured with `se_harness.release_unit`, and every `E-CIP-001`
  finding refuses the approval; a contract without a candidate commit (the
  retained allow-list form) passes unmeasured; a history that cannot be
  derived is `not_assessable`, never a pass. Exemptions for untraced commits
  come from the contract's `[release_unit] untraced_exemptions`.
- Follow-up to WO-CIP-004's deviation 1; the managed validator stays
  git-free.

### After `WO-CIP-003`

- `repository_tools/predecessor_facts.py`: `derive` reads the declared root
  and the candidate version and exports the predecessor's version, wheel,
  wheel digest, payload digest, legacy acceptance-contract digest, and the
  migration scenario path and digest; `write-scenario` is the canonical
  scenario writer. Both fail closed with a `PRE0nn` code that names what is
  missing.
- `candidate-evidence.yml`: one derivation step in `candidate-source`, before
  any network access; `candidate-package` and both migration legs take the
  values from job outputs. Literals restating the evaluator in the
  repository-owned workflows: 8 → 0 (the pinned build-tool versions are not
  evaluator facts and stay). A version bump without its scenario fails the
  first job with the expected path instead of skipping four jobs.
- Tests that restated the same literals (`test_release_qualification`,
  `test_governance_migration`, `test_standard_repository_lifecycle`) now
  derive them through the module; the legacy contract digest lives in one
  table in the module.
- Not changed: the managed `engineering-harness.yml` keeps its version
  literal (`{{HARNESS_VERSION}}` in the template) until the root-evaluator
  upgrade; `predecessor-evaluator-assessment.yml` already derived its facts
  through `scripts/validate_governor_transition.py` and carries no literal.

## The test suite

Measured 2026-08-26 on the workstation (twelve CPUs), `main` at `11f4eac`:

| Run | Wall | Note |
| --- | ---: | --- |
| `python -m unittest discover` (serial) | 367 s | 958 tests; 365 s inside the tests |
| one process per module, 4 workers | 125 s | all 52 modules pass in isolation |
| one process per module, 8 workers | 122 s | `test_workflow_execution` (84 s serial) is the critical path |
| class-level scheduling, computed floor | 91 / 61 / 47 s | at 4 / 6 / 8 workers, from the recorded class costs |
| serial with `os.fsync` neutralised | 333 s | durable writes cost 34 s, not the lever |

Where the serial time goes: `test_workflow_execution` 84 s (two 1,000-artifact
scale tests, 29 s); `test_revision_provenance` 35 s; `test_artifact_renumbering`
28 s; `test_instruction_architecture` 21 s; `test_harnessctl` 18 s; and a
fixed cost of about 0.5 s in most fixtures, a `harnessctl init` (61 files,
0.57 s) plus a validate. The `test-suite` domain packet proposes a
repository-owned parallel runner (class-level, longest-first), a marker for
the scale tests, and a cached fixture install.

### After `WO-TST-001`

Measured 2026-08-26 on the same workstation, 965 tests:

| Run | Wall | Verdict |
| --- | ---: | --- |
| `python -m unittest discover` (canonical serial; the 1,000-artifact size skipped by default) | 335 s | OK, 24 skips |
| `python scripts/run_tests.py --workers 1` | 332 s | OK, 24 skips — the same verdict |
| `python scripts/run_tests.py --workers 4 --scale full` (the hosted lane's form) | 114 s | OK, 24 skips |
| `python scripts/run_tests.py --workers 8` | 80 s | OK, 24 skips |

The runner schedules test classes longest-first from `target/test-timings.json`.

### After `WO-TST-002`

`tests/fixture_support.py` initialises one standard repository per project
name per test process and copies it into each fixture (`shutil.copytree`,
byte-identical to a direct `init`, asserted); eleven fixtures converted.
Measured 2026-08-26, 968 tests:

| Run | Wall | Verdict |
| --- | ---: | --- |
| `python -m unittest discover` (canonical serial) | 329 s | OK, 24 skips |
| `python scripts/run_tests.py --workers 4 --scale full` (the hosted lane's form) | 86 s | OK, 24 skips |
| `python scripts/run_tests.py --workers 8` | 56 s | OK, 24 skips |
| hosted `candidate-source` suite step (PR #178, before the cache) | 29 s | success |

Before the packet: 367 s serial and about six to seven minutes on the hosted
lane.

### After `WO-TST-003`

`release-qualification.yml` sets `SE_HARNESS_TEST_SCALE=full`, so a release
qualification (and the rehearsal's candidate mode on every pull request)
runs the 1,000-artifact scale size; its suite step stays the canonical
serial command.

## What stays

The N-1 to N migration rehearsal, the acceptance of the candidate by the
public predecessor evaluator, the byte-identical recipe replay, and the
`pypi` environment decision. They protect a user; they were only run too
often.
