# WO-CIP-002 implementation evidence

artifact: WO-CIP-002
checkpoint: handoff
formal_snapshot_sha256: 8e1314ffba4e45026cb546450174e7c782d01ee4c697556042d5d2c89b22ae70

Retained by the implementation actor on 2026-08-26. This file is evidence. It
does not complete, verify, or release the work order.

## Evaluators

- Governing: released `se-harness 0.6.0` installed outside the checkout from
  the exact wheel `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`
  (`C:\Users\mathi\se-harness-eval`, invoked with `-I`).
- Candidate: this checkout, `python -m se_harness` from the repository root.
- Workflow assertions are made by tests that read the YAML as text; an
  independent PyYAML 6.0.3 parse of every changed workflow was taken on the
  workstation and is recorded below.

## What was built

- **One release-qualification definition (REQ-CIP-003, CIP-QLF 1–3).**
  `.github/workflows/release-qualification.yml`, `on: workflow_call`, inputs
  `mode` (`candidate` | `release-record`), `release_record`,
  `require_status`, `ref`, `default_ref`; `permissions: contents: read`, no
  secret input, no environment. Steps: check out the subject with full
  history; resolve it (in record mode: `validate_engineering_artifacts`,
  `validate_release_distributions --require-record`, `publish_release.py
  resolve`, and a refusal of any record whose distribution schema is not 2);
  `qualify complete-candidate` in a detached worktree; the unit suite; the CLI
  smoke check; the recipe replayed twice (`scripts/replay_release_build.py`
  for a record, `repository_tools.release_build replay` for a candidate);
  `verify-build-manifest` and `verify-bundle` against the plan in record
  mode; a no-residue proof; retained results; the inert bundle as
  `release-bundle-<RLS>`.
- **Two callers.** `publish-pypi.yml`'s `qualify` job is
  `uses: ./.github/workflows/release-qualification.yml` in `release-record`
  mode with `require_status: released` and no steps of its own.
  `publication-rehearsal.yml` has a `select` job
  (`publish_release.py select-rehearsal-record`: the newest ready or
  released schema-2 record, or the dispatched one, or none), then
  `rehearse-candidate` (mode `candidate`, `ref: github.sha`) and
  `rehearse-record` (mode `release-record` with the selected record's status,
  skipped when there is no subject).
- **Removed (CIP-QLF 4).** `.github/scripts/rehearse_publication.py` (3,187
  lines), `.github/scripts/publication_rehearsal_mechanics.json` (364), the
  `divergence` job, the PyYAML install, `tests/test_publication_rehearsal.py`
  (2,299 lines).
- **Scripts (CIP-QLF 5).** `repository_tools/json_bytes.py` (90 lines) is
  the one definition of canonical JSON encoding, pretty JSON, streaming
  SHA-256, and duplicate-key-refusing JSON parsing; `publish_release.py`,
  `publish_dashboard.py` and `build_integration_package.py` import it and keep
  one-line wrappers that pass their own error class. `reconcile_maintenance_branch.py`
  calls `gh api --include` instead of a hand-rolled `urllib` client.
  `classify-pypi` is deleted. `.github/scripts/`: 6,490 → 3,277 lines.
- **One schema leg and one Pages definition (REQ-CIP-005, CIP-LEG 1–2).**
  The `qualify` matrix and the schema-1 leg are gone; the definition refuses
  a schema-1 record. `.github/workflows/pages-publication.yml`
  (`workflow_call`: `build` and `deploy`, `github-pages` environment, outputs
  `url`) is called by `publish-pypi.yml` (`pages`, after `github_release`)
  and by `publish-dashboard-pages.yml`, now a 42-line caller (was 259).
  `observe` reads the Pages result and URL from the `pages` job.
- **Tests.** `tests/test_ci_pipeline.py::QualificationDefinitionTests` (six
  tests) and the `needs`-graph test (deviation 8); `test_release_orchestration`, `test_pypi_publishing` and
  `test_dashboard_publication` re-pointed at the callers and the definitions;
  the `classify_pypi` unit test removed with the function.
- **Documentation (CIP-DOC).** `docs/notes/developing-se-harness.md`
  ("Release sequences": the rehearsal and the schema-1 paragraph, the last
  mile), `docs/notes/release-publication-rehearsal.md` rewritten,
  `docs/notes/README.md` row, `docs/notes/ci-pipeline.md` ("After
  WO-CIP-002"), and `docs/engineering/release-orchestration/evidence/WO-CIP-002-rehearsal-mechanism.md`
  recording how `CAP-RLO-003` is now evidenced. Every changed workflow has a
  header naming its purpose, policy and note.

## Commands and results

| Command | Evaluator | Result |
| --- | --- | --- |
| `harnessctl preflight . --work-order WO-CIP-002 --phase review` | released 0.6.0 | `PASS` |
| `harnessctl validate .` | released 0.6.0 | PASS, 910 artifacts, 0 errors, 50 warnings |
| `harnessctl doctor .` | released 0.6.0 | 0 FAIL |
| `python scripts/validate_release_distributions.py --root .` | candidate | PASS (1 distribution-bearing record) |
| `python scripts/check_portable_release_surface.py --repository .` | candidate | PASS |
| `git diff --check` | git | clean |
| PyYAML parse of `publish-pypi.yml`, `publish-dashboard-pages.yml`, `publication-rehearsal.yml`, `release-qualification.yml`, `pages-publication.yml` | workstation | jobs `[resolve, qualify, github_release, pypi, pages, observe]`, `[pages]`, `[select, rehearse-candidate, rehearse-record]`, `[qualify]`, `[build, deploy]`; the two definitions trigger on `workflow_call` only |
| `harnessctl check . --artifact WO-CIP-002 --checkpoint handoff --changed-path … --changes-complete --json` (complete set below) | released 0.6.0 and candidate | first probe refused `docs/notes/release-publication-rehearsal.md` as out of scope; after the owner's two scope amendments (commits `3f676e2` and `0704d31`) and before this file existed: blocked only by `QGP-G4I-EVIDENCE`; both report formal snapshot `8e1314ffba4e45026cb546450174e7c782d01ee4c697556042d5d2c89b22ae70` |
| `python -m unittest` over `test_ci_pipeline`, `test_release_orchestration`, `test_pypi_publishing`, `test_dashboard_publication`, `test_maintenance_branch`, `test_integration_package`, `test_release_build` | candidate | OK |
| `python -m unittest discover -s tests -p "test_*.py"` | candidate, Windows 11, CPython 3.14 | `Ran 907 tests in 343.187s` — `OK (skipped=23)`; 1035 → 907 because `test_publication_rehearsal.py` (135 tests) went with its subject and seven tests were added |
| Hosted runs | `.github/workflows/publication-rehearsal.yml` | not observed locally; the pull request is `VER-CIP-001` scenario 3 (the rehearsal executes the definition; `candidate` mode replays this commit's own recipe) |

## Deviations from the specification, recorded for the completion decision

1. **The definition runs on Linux only; the rehearsal has no Windows leg.**
   `CIP-QLF` 1 declared a `platform` input and `CIP-QLF` 3 rehearsed on both
   platforms. The recipe producer is a Linux/amd64 container and the release
   runs the definition on `ubuntu-latest`; the Windows leg of the old
   rehearsal exercised the legacy schema-1 build path, which `CIP-LEG` 1
   deletes. A Windows rehearsal of a path the release never takes would
   rehearse nothing. `VER-CIP-001` row 3's "both platforms" is therefore not
   met; the Windows coverage of the candidate remains `candidate-evidence`'s
   Windows migration and integration-package legs.
2. **The definition's steps are the recipe path, not the build-twice path.**
   `CIP-QLF` 2 listed the legacy leg's steps (`python -m build` twice,
   `normalize_sdist`, byte comparison, bundle manifest). With the schema-1 leg
   deleted, that path is not what the release executes; the definition
   contains the recipe replay and the two `publish_release.py` verifications.
   In `candidate` mode it replays the candidate's own recipe, which the old
   rehearsal never did.
3. **`release-record` mode has no subject today.** The newest released
   record, `RLS-SEH-012` (0.6.0), is schema 1. Until a schema-2 record is
   ready or released, the rehearsal's record job is skipped and the run
   summary says why. `VER-CIP-001` scenario 3 is met by `candidate` mode on
   this pull request; the record mode is exercised when 0.7.0's record is
   prepared. The WO's "rehearsal in release-record mode against the latest
   released record" cannot be satisfied by any implementation while the
   latest released record is schema 1.
4. **`classify-pypi` deleted rather than called.** The `pypi` job executes no
   repository code by policy (`test_release_orchestration` and
   `test_pypi_publishing` pin it), so the inline `curl`/`jq` classification
   stays and the unused subcommand and its unit test are removed. The
   decision envelope allowed either.
5. **The shared helpers live in `repository_tools/json_bytes.py`, and the
   scripts keep one-line wrappers.** `CIP-QLF` 5 named `se_harness`
   helpers; `se_harness/` is not in this work order's scope beyond
   `workflow_contract.py`, and `repository_tools` may not import the package
   (pinned crossing inventory, see WO-CIP-003). The scripts' wrappers exist so
   each script's callers keep the exception type they always had; the logic
   is defined once. Three error-message wordings changed to the shared form.
6. **`release-candidate-replay.yml` is unchanged.** It is not in scope; it
   replays a ready record's recipe and could become a third caller of the
   definition under a later work order.
7. **Scope amendment.** `docs/notes/release-publication-rehearsal.md` was
   added to the execution scope by the owner's decision during
   implementation (commit `3f676e2`); the formal snapshot above is the
   amended one.

8. **Correction of `WO-CIP-003`'s implemented change, under this work
   order.** The hosted run of pull request #172 (WO-CIP-003) failed both
   `governance-migration` legs: the job listed `needs: candidate-package`
   only, so the `needs.candidate-source.outputs.*` values it consumes
   resolved to empty strings and the guard added under WO-CIP-003 refused to
   run. Local tests read the YAML as text and did not check the `needs`
   graph. Owner decision 2026-08-26: fix it here under a second scope
   amendment (commit `0704d31`) rather than reopen an implemented work
   order. The fix is `needs: [candidate-source, candidate-package]`; the
   guarding test `test_every_consumed_job_output_is_declared_in_the_consumers_needs`
   checks every `needs.<job>.outputs`/`.result` reference in every workflow
   against the consumer's `needs`. `WO-CIP-003` stays implemented and
   `VREC-CIP-003` stays the verified record of commit `7baca57`, which
   carries the defect; its bound evidence cannot be edited, so this file and
   `docs/notes/ci-pipeline.md` are the disclosure.
## Complete changed-path set

```
.github/scripts/build_integration_package.py
.github/workflows/candidate-evidence.yml
.github/scripts/publication_rehearsal_mechanics.json (deleted)
.github/scripts/publish_dashboard.py
.github/scripts/publish_release.py
.github/scripts/reconcile_maintenance_branch.py
.github/scripts/rehearse_publication.py (deleted)
.github/workflows/pages-publication.yml
.github/workflows/publication-rehearsal.yml
.github/workflows/publish-dashboard-pages.yml
.github/workflows/publish-pypi.yml
.github/workflows/release-qualification.yml
docs/engineering/ci-pipeline/evidence/WO-CIP-002/WO-CIP-002-verification.md
docs/engineering/release-orchestration/evidence/WO-CIP-002-rehearsal-mechanism.md
docs/notes/README.md
docs/notes/ci-pipeline.md
docs/notes/developing-se-harness.md
docs/notes/release-publication-rehearsal.md
repository_tools/json_bytes.py
tests/test_ci_pipeline.py
tests/test_dashboard_publication.py
tests/test_publication_rehearsal.py (deleted)
tests/test_pypi_publishing.py
tests/test_release_orchestration.py
tests/test_standard_repository_lifecycle.py
```

## Not done

- Hosted observation of the rehearsal (scenario 3), which needs the pull
  request; the completion transition; `VREC-CIP-002`.
- A real release dispatch; the `release-record` mode against a schema-2
  record (deviation 3).
- `se_harness/workflow_contract.py` and `docs/notes/harnessctl-reference.md`
  are in scope and unchanged: no contract or `harnessctl` command changed.
