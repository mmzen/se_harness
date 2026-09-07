# WO-DST-024 verification evidence

Retained under `VER-DST-025` for the retirement of the evaluator scripts from
the standard repository template. Measurements were taken on Windows 11 at
candidate revision `e7b0402f` (branch `wo/dst-retire-engine-footprint`, base
`main` at `2268a54c`), then `main` at `bdc8d175` was merged in as `8752a981`
and the scope and handoff checkpoints were re-run. The governing evaluator is
released 0.15.0 in `C:/Users/mathi/se-harness-eval-0150`, run with `-I` from
outside the checkout. The candidate wheel and the consumer scenarios ran in
`C:/Users/mathi/dst024-acceptance`, outside the checkout.

## Authorization

- 2026-09-06: the owner approved `REQ-DST-070`, `SPEC-DST-025`,
  `VER-DST-025` and `WO-DST-024` by selecting the presented option
  "Approve all four, do not start (Recommended)".
- 2026-09-06: the owner started the work order with the instruction
  "start WO-DST-024".
- 2026-09-06: the owner amended the execution scope by selecting the presented
  option "Amend the scope with the two exact paths (Recommended)", adding
  `repository_tools/explorer_design/build_explorer_template.py` and
  `repository_tools/diagnostic_code_index.py`; the amendment record on the work
  order says why.

## Engine directory

`se_harness/engine/`, a package whose `__init__.py` carries only a docstring
stating that the scripts are run as subprocesses by path and are not an
import surface. The scripts keep their sibling imports; each runs with its own
directory first on `sys.path` (DST-ENG-006).

## Paths deleted, moved and added

| Change | Path |
| --- | --- |
| moved, identical | `templates/repository/standard/scripts/artifact_layout_registry.py` to `se_harness/engine/artifact_layout_registry.py` |
| moved, identical | `templates/repository/standard/scripts/generate_harness_dashboard.py` to `se_harness/engine/generate_harness_dashboard.py` |
| moved, identical | `templates/repository/standard/scripts/inspect_engineering_artifacts.py` to `se_harness/engine/inspect_engineering_artifacts.py` |
| moved, identical | `templates/repository/standard/scripts/harness_explorer/index.template.html` to `se_harness/engine/harness_explorer/index.template.html` |
| moved, one edit | `templates/repository/standard/scripts/validate_engineering_artifacts.py` to `se_harness/engine/validate_engineering_artifacts.py`: the managed workflow contract is read from the package's `workflow_contract.json` instead of `../docs/engineering/WORKFLOW.json`; the two files are byte-identical (36,079 bytes, LF) |
| deleted | `templates/repository/standard/scripts/select_harness_work_order.py` (DST-ENG-008) |
| deleted | `templates/repository/standard/scripts/check_engineering_harness.sh`, `check_engineering_harness.ps1` (DST-ENG-009) |
| added | `se_harness/engine/__init__.py` |
| edited | `pyproject.toml`: the two `scripts` entries leave `[tool.setuptools.data-files]`; `engine/harness_explorer/index.template.html` joins `[tool.setuptools.package-data]` |
| edited | `se_harness/installer.py` (`ENGINE_ROOT`, `engine_script`), `cli.py`, `preflight.py`, `provenance.py`, `release_qualification.py`, `renumber.py` (DST-ENG-004, DST-ENG-005, DST-ENG-010) |
| edited | `repository_tools/explorer_design/build_explorer_template.py` (default output), `repository_tools/diagnostic_code_index.py` (scan roots) |
| edited | `docs/notes/harness-installation-and-upgrades.md`, `docs/notes/developing-se-harness.md` (DST-ENG-017) |

## Test files changed

`tests/test_artifact_authoring.py`, `test_dashboard_publication.py`,
`test_dashboard_webui.py`, `test_fixture_support.py`, `test_glossary.py`,
`test_harnessctl.py`, `test_inspection.py`, `test_instruction_architecture.py`,
`test_legacy_release_evidence.py`, `test_lifecycle_state_contract.py`,
`test_predecessor_bootstrap_retirement.py`, `test_reader_first_capabilities.py`,
`test_reader_first_intents.py`, `test_reader_first_requirements.py`,
`test_reader_first_specifications.py`, `test_repository_context_retirement.py`,
`test_revision_provenance.py`. Seventeen modules. The `init` test asserts no
`scripts/` path and no `scripts/` lock entry; the decoy test asserts the
package copy runs while unmanaged decoys are ignored by `doctor`; the
root-versus-candidate validator ledger gains `DST024_CANDIDATE_VALIDATOR_EDITS`
declaring the one `replace` at root line 107 plus the WO-TCM-009 insertions
(line delta 152); the fixture count moves from 49 to 41; the retirement
baseline filters the three retired required paths.

## Wheel listing (DST-ENG-001, DST-ENG-003)

Built with `python -m pip wheel --no-deps` from the checkout at `e7b0402f`
into `C:/Users/mathi/dst024-acceptance/wheel/se_harness-0.16.0-py3-none-any.whl`,
an acceptance artifact and not a distribution. 83 members. Engine members:
`se_harness/engine/__init__.py`, `artifact_layout_registry.py`,
`generate_harness_dashboard.py`, `harness_explorer/index.template.html`,
`inspect_engineering_artifacts.py`, `validate_engineering_artifacts.py`, each
once. No member under `share/se-harness/templates/repository/standard/scripts/`.
The only `share/.../scripts/` members are the two skill helpers
`.agents/skills/*/scripts/*.py`, which are host-run adapters, not evaluator
scripts. No member named `select_harness_work_order` or
`check_engineering_harness`.

## Consumer scenarios (VER-DST-025 A to C)

Log: `C:/Users/mathi/dst024-acceptance/scenarios.log`. The candidate wheel was
installed with `pip install --no-deps` into a fresh venv there; the released
0.15.0 venv produced the earlier installations.

- **A, fresh init with the candidate.** `init` wrote 40 files. `scripts/`
  absent; lock keys under `scripts/`: none. `doctor` PASS; `validate` PASS
  (0 artifacts, 0 errors); `dashboard` PASS, `target/harness-dashboard/index.html`
  written.
- **B, 0.15.0 installation upgraded by the candidate.** 0.15.0 wrote the eight
  `scripts/` paths. The candidate `upgrade` plan listed exactly eight `remove`
  actions, one per retired path, plus three `update` actions for template
  documents that changed between the versions. `upgrade --apply` completed
  with `written: true`; afterwards `scripts/` is absent, the lock has no
  `scripts/` key and records evaluator 0.16.0, `doctor` exits 0, and the file
  set equals scenario A's byte for byte (DST-ENG-011, DST-ENG-013). One
  scripting error is disclosed: the first `--apply` attempt passed an invalid
  `--evidence-output` path and was refused by the existing path rule before
  writing; the re-run without it is the measurement.
- **C, one edited retired copy.** With `scripts/generate_harness_dashboard.py`
  appended to, the plan reported that path `customized` and the other seven
  `remove`; `--apply` printed "customized files require manual review; no
  files were written". Lock digest unchanged, edited copy present, all eight
  files present (DST-ENG-012). The command's exit code on that refusal is 0;
  that is the existing upgrade behaviour and is not changed by this work order.

## Released-evaluator readings

- `validate .`: 0 errors, 71 warnings before and after the change.
- `preflight . --work-order WO-DST-024 --phase review`: no diagnostics.
- `check --checkpoint scope --from-git <merge-base>`: `completed`, no failing
  predicate, at `2268a54c` before the merge and at `bdc8d175` after it.
- `check --checkpoint handoff --from-git origin/main`: `completed` after the
  evidence packet was written; before it, the same command was blocked by
  `QGP-G4I-EVIDENCE` (no packet) and, before `main` was merged in, by
  `QGP-G4I-PATHS` on `docs/engineering/technical-communication/README.md`, a
  file this branch never touched that `main` had changed. The hosted
  `validate` lane failed on `e7b0402f` for that second reason; the merge of
  `main` is the repair.
- `repository_tools.explorer_design.build_explorer_template --check`: the
  moved template matches its sources (445,615 bytes).

## Static checks

The retirement grep over `se_harness/`, `templates/`, `.github/` and
`docs/notes/` outside `history/` finds: the three repository-owned lanes
`release-qualification.yml`, `release-candidate-replay.yml` and
`pages-publication.yml`, one reference each, which DST-ENG-016 binds to the
root-adoption work order; the two notes this work order edited, which name
the retired paths on purpose; and `docs/notes/complexity-audit-2026-08.md`,
a dated assessment that describes the pre-change state and is left as
history. Nothing under `se_harness/` or `templates/`.

## Local control reading (Windows, not the record)

`python scripts/run_tests.py` at `e7b0402f`: 1265 tests, 0 failures, 1 error,
26 skipped. The error is `test_artifact_authoring.IdentifierAllocationTests.
test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`,
`PermissionError` on a temporary `.git` object during teardown, the known
Windows flake; the skips are the Windows-only guards. An earlier run before
two test corrections had 2 failures (`test_fixture_support` count 49 versus
41, `test_repository_context_retirement` baseline required paths), both
caused by this change and both fixed in `e7b0402f`.

## Hosted lanes

At `e7b0402f`: Governor Transition Assessment success (run 34041625419),
Publication Rehearsal success (run 34041625567), SE Harness Candidate
Evidence in progress at the time of writing (run 34041625418), Engineering
Harness failure (run 34041625407) on the live-`main` scope diff explained
above. The lanes for the final head, which carries the merge of `main` and
this evidence, are on pull request #365; the engineering owner reads them
there before the completion decision.

## Root footprint (DST-ENG-014)

`git diff --stat bdc8d175 HEAD -- scripts/ .engineering-harness.lock AGENTS.md`
is empty. The eight root copies remain the 0.15.0 footprint and `doctor`
under the released evaluator still reports them unchanged.

## Carried forward to the root-adoption work order

- DST-ENG-015: AGENTS.md lines 9, 32 and 34, and the paragraph under
  "Candidate source versus released evaluator" that says changes to the eight
  managed scripts belong in `templates/repository/standard/`; the managed-path
  count in `SPEC-IAR-012` moves from 28 to 20.
- DST-ENG-016: `release-qualification.yml`, `release-candidate-replay.yml`
  and `pages-publication.yml` run root scripts from a checkout or snapshot;
  `tests/test_release_build.py` and `tests/test_dashboard_publication.py`
  assert those lines and move with them.
- The eight root copies leave through the leaving-set rule at that upgrade.

## Residual

The classification `commit_bound_verification = "not_required"` is still not
consulted by any coverage rule; a path-confinement guard for it is a separate
proposal. Folding the engine scripts into importable modules is packet 2
(complexity audit item #225).
