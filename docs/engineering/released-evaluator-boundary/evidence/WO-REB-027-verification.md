# WO-REB-027 implementation evidence

artifact: WO-REB-027
checkpoint: handoff
formal_snapshot_sha256: b195c3d4cc6aa22d97dd0fe87912ab176bda6f8892af3af3789d3974a2a28dcb

Retained by the implementation actor on 2026-08-27. This file is evidence. It
does not complete, verify, or release the work order.

## Evaluators

- Governing: released `se-harness 0.6.0` installed outside the checkout from
  the exact wheel `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`
  (`C:\Users\mathi\se-harness-eval`, invoked with `-I`).
- Candidate: this checkout, branch `governance/reb-027-simple-upgrade` off
  `main` at `7284743`.

## What was built

- **`se_harness/mutation_guard.py`**: the upgrade path takes the installed
  released evaluator as the target identity — version and installed-payload
  digest, archive digest when recorded — and reports whether writing it is
  an identity transition (`MutationAuthority.target_identity`,
  `.transition`; `evaluator_transition_required` moved here). `MG004` is
  raised only when the evaluator cannot identify itself; the PEP 610 archive
  requirement and the `MG007` packet path are gone; `upgrade_work_order` is
  no longer a parameter. `require_archive` for record preparation is
  unchanged (deviation 1).
- **`se_harness/upgrade_authorization.py`**: deleted. The evidence schema
  constant and the evidence-path rule moved into `installer.py`; the path
  rule no longer requires a work-order prefix, only
  `docs/engineering/**/evidence/*.json`.
- **`se_harness/installer.py`**: `apply_changes(..., evidence_output=None)`;
  the transaction proves the guard's target identity again after the write,
  requires the no-op replay on a transition, and writes the canonical
  `se-harness-evaluator-upgrade-evidence-v1` document only when
  `--evidence-output` is given, with the retired packet fields carried as
  `null` and the prior lock digest taken from the lock file's bytes. The
  legacy-release refusal (`REQ-LRE-002`) is unchanged in substance; its
  message names the declaration table, not a work order.
- **`se_harness/cli.py`**: `upgrade` has no `--work-order`;
  `--evidence-output` is optional; the human output says when no evidence
  was retained.
- **`se_harness/evaluator_identity.py`**: `to_lock()` always emits the
  canonical field set, with the archive pair as `null` when unrecorded.
- **`se_harness/runtime_identity.py`**: `RID022` only when the installation
  recorded an archive digest that differs.
- **`se_harness/release_qualification.py`**: `released-root` accepts a lock
  without an archive digest.
- **`.github/workflows/candidate-evidence.yml`**: the candidate-package job
  runs `qualify candidate-package` when the released verifier answers
  `qualify --help`, and the legacy `accept-candidate` bootstrap otherwise;
  each branch asserts the shape of the operation that ran.
- **Templates**: the managed `engineering-harness.yml` template is
  unchanged; its index install now passes `qualify released-root`.
- **Definitions**: `REQ-REB-005` superseded by direct edit; `SPEC-REB-002`
  rule 1 amended by a dated paragraph; `ARCH-REB-001` no longer addresses
  the superseded requirement (dated amendment); the developer note's root
  advancement section rewritten.
- **Tests**: `test_mutation_guard` (packet-free transition with optional
  evidence, index-install transition with `null` archive, `MG004` only on an
  unidentifiable evaluator), `test_evaluator_identity` (no archive → no
  `RID022`, payload still decides), `test_legacy_release_evidence` and
  `test_hash_bound_integrity` (packet-loader cases retired, fixtures
  packet-free).
  `test_release_qualification` and `test_standard_repository_lifecycle`
  pinned the workflow to the legacy `accept-candidate` branch only; they now
  pin the capability-selected pair of branches (SPEC-REB-012 rule 6) and the
  mutation probe targets the exact invocation.

## Commands and results

| Command | Evaluator | Result |
| --- | --- | --- |
| `harnessctl preflight . --work-order WO-REB-027 --phase start` | released 0.6.0 | `PASS` (recorded in the start transition) |
| `harnessctl preflight . --work-order WO-REB-027 --phase review` | released 0.6.0 | `PASS` |
| `harnessctl validate .` | released 0.6.0 | PASS, 968 artifacts, 0 errors, 53 warnings |
| `harnessctl validate .` | public 0.7.0, outside the checkout | PASS, 0 errors |
| `harnessctl doctor .` | released 0.6.0 | 0 FAIL |
| `python scripts/check_portable_release_surface.py --repository .` | candidate | PASS |
| `python scripts/validate_release_distributions.py --root .` | candidate | PASS |
| `git diff --check` | git | clean |
| PyYAML parse of `candidate-evidence.yml` | workstation | parses, six jobs |
| `python -m unittest` over `test_mutation_guard`, `test_legacy_release_evidence`, `test_hash_bound_integrity`, `test_evaluator_identity`, `test_ci_pipeline`, `test_release_orchestration`, `test_governance_migration`, `test_dashboard_webui` | candidate | OK |
| End to end: `pip install .` of this candidate into a fresh venv (no PEP 610 archive record), then `harnessctl init`, `upgrade` plan, `upgrade --apply`, `qualify released-root` | candidate as its own evaluator | init lock evaluator carries `archive_name: null, archive_sha256: null`; plan `61 files, 61 unchanged`; apply succeeds and reports no evidence retained; `released-root` `passed: true`, RR001–RR004 |
| `python scripts/run_tests.py --workers 8 --scale full` | candidate, Windows 11, CPython 3.14 | OK, 983 tests, 24 skipped (Windows-only guards), 0 failures |
| `py -3.11 scripts/run_tests.py --workers 4 --scale full` | candidate, Windows 11, CPython 3.11 | OK, 983 tests, 24 skipped (Windows-only guards), 0 failures |
| `harnessctl check . --artifact WO-REB-027 --checkpoint handoff --changed-path … --changes-complete --json` | released 0.6.0 and candidate | before this file existed: blocked only by `QGP-G4I-EVIDENCE`; formal snapshot above |
| Hosted | pull request #198 at `8dcd561` | all ten lanes pass (runs 33089362243, 33089362246, 33089362342, 33089362619); the candidate-package job took the legacy `accept-candidate` branch under the 0.6.0 verifier, as rule 6 requires until a verifier with `qualify` is the root |

## Deviations from the specification, recorded for the completion decision

1. **`MG004` still guards release-record preparation.** `SPEC-REB-012`
   rule 2 says `MG004` is raised only when the evaluator cannot identify
   itself; `prepare-release` keeps `require_archive=True` because a release
   record binds the evaluator's archive identity and both validators check
   it when present. Upgrades, identity and root qualification are free of
   the archive requirement as the requirements state; preparing a release
   from an index-installed root still needs a wheel-file install. Left to a
   later decision rather than widened here.
2. **The legacy-release declaration keeps its carrier.** `REQ-LRE-002`'s
   declaration still lives in an approved work order's
   `[evaluator_upgrade].legacy_releases_without_evaluator_evidence` table;
   only the table's use as an upgrade authorization is gone. This
   repository declares nothing (measured: zero undeclared records).
3. **No template change.** The managed workflow template needed no edit:
   its index install passes once the evaluator accepts it.

## Deviation acceptances

Recorded on 2026-08-27 from the owner's interactive answers, before the
completion decision. These are the owner's statements; the assurance decision
on the verification record remains separate.

| Deviation | Owner answer |
| --- | --- |
| 1 - `MG004` still guards release-record preparation | Accept: left to a later decision; the wheel-file install for release preparation stays documented. |
| 2 - the legacy-release declaration keeps its carrier | Accept: nothing in this repository is affected. |
| 3 - no managed template change | Accept. |

## Complete changed-path set

```
.github/workflows/candidate-evidence.yml
docs/engineering/released-evaluator-boundary/README.md
docs/engineering/released-evaluator-boundary/architecture/ARCH-REB-001.md
docs/engineering/released-evaluator-boundary/evidence/WO-REB-027-verification.md
docs/engineering/released-evaluator-boundary/requirements/REQ-REB-005.md
docs/engineering/released-evaluator-boundary/specifications/SPEC-REB-002.md
docs/engineering/released-evaluator-boundary/work-orders/WO-REB-027.md
docs/notes/developing-se-harness.md
se_harness/cli.py
se_harness/evaluator_identity.py
se_harness/installer.py
se_harness/mutation_guard.py
se_harness/release_qualification.py
se_harness/runtime_identity.py
se_harness/upgrade_authorization.py
tests/test_evaluator_identity.py
tests/test_hash_bound_integrity.py
tests/test_legacy_release_evidence.py
tests/test_mutation_guard.py
tests/test_release_qualification.py
tests/test_standard_repository_lifecycle.py
```

## Not done

- The hosted reading (needs the pull request); the completion transition;
  the verification record; the release that ships this change and the
  adoption that follows it.
