# WO-CIP-001 implementation evidence

artifact: WO-CIP-001
checkpoint: handoff
formal_snapshot_sha256: c2b1a5d7aa93cf0cc64e571103ccd6abcd3a3c4f03f8f1dff9cb600b99e9ce97

Retained by the implementation actor on 2026-08-26. This file is evidence. It
does not complete, verify, or release the work order.

## Evaluators

- Governing: released `se-harness 0.6.0` installed outside the checkout from
  the exact wheel `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`
  (`C:\Users\mathi\se-harness-eval`, invoked with `-I`).
- Candidate: this checkout, `python -m se_harness` from the repository root.
- Workflow assertions: `tests/test_ci_pipeline.py` reads the YAML as text
  (no PyYAML dependency); an independent PyYAML parse of the three workflows
  was taken on the workstation and is recorded below.

## What was built

- **Trigger policy (REQ-CIP-001, CIP-TRG).** `candidate-evidence.yml`,
  `predecessor-evaluator-assessment.yml` and the standard template
  `templates/repository/standard/.github/workflows/engineering-harness.yml`
  declare `push: branches: [main, "release/**", "candidate/**"]`,
  `pull_request:` unfiltered, and `concurrency: {group: <workflow>-${{
  github.ref }}, cancel-in-progress: true}`. Each carries a header comment
  naming its purpose, the policy, and the note section that describes it.
  The hash-locked root `engineering-harness.yml` is untouched.
- **One build per workflow (REQ-CIP-002, CIP-ART).** `candidate-source`
  builds the wheel from `git archive` of the commit, writes `SHA256SUMS`,
  and uploads `candidate-wheel-non-promotable-<sha>` (one-day retention).
  `candidate-package` downloads it and runs `sha256sum --check --strict`;
  both `governance-migration` legs download it and verify with
  `Get-FileHash` against `SHA256SUMS`. No consumer contains `git archive`,
  `pip wheel` or `python -m build`. `governance-migration` publishes each
  platform's `semantic_sha256` as a job output (`Linux`, `Windows`; an empty
  matrix output does not overwrite the other leg's value) and the first step
  of `integration-package-build` requires the two to agree.
  `governance-migration-reconcile` is removed. Jobs: 7 → 6.
- **Documentation (CIP-DOC).** `docs/notes/developing-se-harness.md`
  ("Evaluator and candidate evidence": trigger policy and the wheel handover;
  the migration paragraph; the integration-package diagram),
  `docs/notes/ci-pipeline.md` ("After WO-CIP-001" figures), and the three
  workflow header comments.

## Commands and results

| Command | Evaluator | Result |
| --- | --- | --- |
| `harnessctl preflight . --work-order WO-CIP-001 --phase review` | released 0.6.0 | `PASS` |
| `harnessctl validate .` | released 0.6.0 | PASS, 908 artifacts, 0 errors, 50 warnings |
| `harnessctl doctor .` | released 0.6.0 | 0 FAIL |
| `python scripts/validate_release_distributions.py --root .` | candidate | PASS (1 distribution-bearing record) |
| `git diff --check` | git | clean |
| PyYAML 6.0.3 parse of the three workflows | workstation | `on: [pull_request, push]`, `concurrency` group per workflow with `cancel-in-progress: True`; `candidate-evidence` jobs `[candidate-source, candidate-package, governance-migration, integration-package-build, integration-package-verify, integration-package-retain]` |
| `grep -c "pip wheel"` / `"python -m build"` in `candidate-evidence.yml` | text | 1 / 0 |
| `harnessctl check . --artifact WO-CIP-001 --checkpoint handoff --changed-path … --changes-complete --json` (complete set below) | released 0.6.0 and candidate | before this file existed: blocked only by `QGP-G4I-EVIDENCE`; both report formal snapshot `c2b1a5d7aa93cf0cc64e571103ccd6abcd3a3c4f03f8f1dff9cb600b99e9ce97` |
| `python -m unittest tests.test_ci_pipeline` | candidate | 7 tests, OK |
| `python -m unittest` over `test_harnessctl`, `test_instruction_architecture`, `test_predecessor_assessment_contract`, `test_standard_repository_lifecycle`, `test_ci_pipeline` | candidate | 92 tests, OK, 1 skip (after the two pinned assertions were updated) |
| `python -m unittest` over `test_integration_package`, `test_governance_migration`, `test_release_qualification` | candidate | 42 tests, OK |
| `python -m unittest discover -s tests -p "test_*.py"` | candidate, Windows 11, CPython 3.14 | `Ran 1028 tests in 338.801s` — `OK (skipped=23)`; the 23 skips are the Windows-only guards. A first run failed one test: the portable-surface checker rejects the retired term "governor" in operator notes; the two notes were reworded and the suite re-run |
| Hosted runs | `.github/workflows/*` | not observed locally; `VER-CIP-001` scenarios 1 and 2 are read from the pull request that carries this change (two pushes; the `candidate-evidence` logs) |

## Test coverage added

`tests/test_ci_pipeline.py`: the three workflows' push filters, concurrency
groups and header comments; the release workflows keep
`cancel-in-progress: false`; the root managed copy is untouched; only
`candidate-source` builds and both consumers verify the handover; the
integration package keeps its own build; the reconcile job is gone and the
comparison reads the matrix outputs; the retention job and the double
rehearsal per platform are kept. Two existing assertions on the removed job
were updated in `tests/test_integration_package.py` and
`tests/test_standard_repository_lifecycle.py`.

## Deviations from the specification, recorded for the completion decision

1. **The integration package keeps its own two builds.** `CIP-ART` 2 says no
   consumer builds. `build_integration_package.py build` builds a different
   distribution — a PEP 440 local-version overlay applied inside two
   disposable exports, built twice for byte equality — under the approved
   `SPEC-IPK-001` rule 1. It cannot take the candidate wheel, whose version
   is the plain candidate version. The script was not changed. Workflow-level
   builds of the commit went 3 → 1; the integration package's two remain.
2. **`integration-package-retain` stays as a job.** `CIP-ART` 4 folds it into
   verify. `SPEC-IPK-001` rule 5 requires retention only after every matrix
   member passes, which a matrix leg cannot know. Kept under the decision
   envelope ("may keep a fifth job … the evidence says why"). Jobs: 7 → 6,
   not 7 → 4.
3. **The rehearsal still runs twice per platform.** `CIP-ART` 3 says once.
   `REQ-REB-017`'s acceptance example ("When the rehearsal runs twice on
   supported platforms") is the determinism check; removing it would change
   what an approved requirement's evidence covers. Only the cross-platform
   reconciliation job was folded.
4. **The cross-platform comparison runs where the lane runs.** The comparing
   step is in `integration-package-build`, which is conditioned on
   `pull_request` or push to `main`. On a push to `release/**` or
   `candidate/**` the migration legs still run and each proves its own two
   runs agree, but the Linux–Windows comparison does not run. Before this
   change the same comparison ran on every push; after `CIP-TRG` the only
   pushes that run at all are those three branch families.
5. **The managed workflow's root copy.** `CIP-TRG` 1 applies to the template
   only; the root `engineering-harness.yml` keeps `push:` unfiltered and no
   concurrency until the governor upgrade. On this repository, a push to a
   pull-request branch therefore still runs that one workflow twice.

## Complete changed-path set

```
.github/workflows/candidate-evidence.yml
.github/workflows/predecessor-evaluator-assessment.yml
docs/engineering/ci-pipeline/evidence/WO-CIP-001/WO-CIP-001-verification.md
docs/notes/ci-pipeline.md
docs/notes/developing-se-harness.md
templates/repository/standard/.github/workflows/engineering-harness.yml
tests/test_ci_pipeline.py
tests/test_integration_package.py
tests/test_standard_repository_lifecycle.py
```

## Deviation acceptances

Recorded on 2026-08-26 from the owner's interactive answers, before the
completion decision. These are the owner's statements; the assurance decision
on `VREC-CIP-001` remains separate.

| Deviation | Owner answer |
| --- | --- |
| 1 - the integration package keeps its own two builds | Accept: a different distribution governed by SPEC-IPK-001 rule 1. |
| 2 - `integration-package-retain` stays as a job | Accept: SPEC-IPK-001 rule 5 requires retention after every matrix member passes. |
| 3 - the rehearsal still runs twice per platform | Accept: REQ-REB-017's determinism example; only the reconciliation job was folded. |
| 4 - the cross-platform comparison runs only where the integration lane runs | Accept: pull requests and main are where it matters; release and candidate pushes keep the per-platform proof. |
| 5 - the managed workflow changed in the template only | Accept: the root copy follows at the root-evaluator upgrade. |

## Not done

- Hosted observation of the runs (scenarios 1 and 2), which needs the pull
  request; the completion transition; `VREC-CIP-001`.
- `.github/scripts/build_integration_package.py` is in scope and unchanged
  (deviation 1).
