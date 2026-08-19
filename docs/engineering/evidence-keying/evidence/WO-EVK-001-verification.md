# WO-EVK-001 Implementation Verification Evidence

Date: 2026-08-19

Work order: `WO-EVK-001`

Issue: GitHub issue 72

State: retained implementation evidence; not a VREC and not verification or release authority

## Authorization and preflight

- The repository owner approved the complete `INT-EVK-001` through `VER-EVK-001` chain and `WO-EVK-001` with the instruction `go implement`.
- Start preflight passed while the work order was `approved`.
- The complete 18-file preflight reading manifest was read before implementation began.
- Commit-bound verification is classified `required`; a later clean candidate commit and accountable VREC remain necessary.

## Issue reproduction and corrected behavior

Before the change, the package predicate returned `True` for `docs/engineering/x/evidence/WO-MOK-001-check.md` and `False` for `docs/engineering/x/evidence/WO-MOK-001/check.md`. The validator and dashboard contained equivalent filename-only matching.

After the change, both independent execution-plane predicates return:

| Normalized path | Ordered keys |
| --- | --- |
| `docs/engineering/example/evidence/WO-ABC-001-check.md` | `WO-ABC-001` |
| `docs/engineering/example/evidence/WO-ABC-001/check.md` | `WO-ABC-001` |
| `docs/engineering/example/evidence/archive/WO-ABC-001/check.md` | `WO-ABC-001` |
| `docs/engineering/WO-ABC-001/evidence/check.md` | none |
| `docs/engineering/example/evidence/X-WO-ABC-001/check.md` | none |
| `docs/engineering/example/evidence/wo-abc-001/check.md` | none |
| `docs/engineering/example/evidence/WO-ABC-0010/check.md` | none |
| `docs/engineering/example/evidence/WO-ABC-001_check.md` | none |
| `docs/engineering/example/Evidence/WO-ABC-001/check.md` | none |
| `docs/engineering/example/evidence/WO-ABC-001/WO-ABC-001-check.md` | `WO-ABC-001` |
| `docs/engineering/example/evidence/WO-XYZ-002/WO-ABC-001-check.md` | `WO-ABC-001`, `WO-XYZ-002` |
| `reports/WO-ABC-001.md` | `WO-ABC-001` |

The shared case table executes against package provenance and the portable validator predicate and asserts exact tuple equality. Host-independent `PurePosixPath` component semantics are used in both planes.

## Surface observations

- Aggregate `capture-verification` accepts a mixed candidate with flat `WO-001` evidence and directory-keyed `evidence/WO-002/check.md`, retains both exact paths, and prepares one ready record without committing or tagging.
- Formal validation accepts an authored aggregate VREC whose two evidence paths are `evidence/WO-001/check.md` and `evidence/archive/WO-002/check.md`.
- Dashboard discovery associates flat, direct-directory, nested-directory, duplicate-key, and multi-key layouts deterministically.
- The directory-keyed aggregate snapshot has no `W-HEX-001` for either work order; G3 `verification_evidence` is `satisfied` with each exact path.
- Inspection consumes that snapshot and likewise has no `W-HEX-001`; it contains no evidence-path matcher of its own.
- Finding rules advance from `harness-findings-v7` to `harness-findings-v8`; snapshot schema remains `harness-dashboard-snapshot-v1`.

## Safety, architecture, and compatibility

- Existing normalization, absolute/backslash/traversal rejection, containment, existence, regular-file, symlink/junction, clean-worktree, atomic-output, and destination checks remain independent of key extraction.
- Dashboard discovery skips paths with a symlink or junction component before an association can satisfy readiness.
- Repository-local validator and dashboard scripts remain Python 3.11+ standard-library-only and do not import target `se_harness` code.
- Package provenance does not import target repository scripts.
- Root managed validator/dashboard scripts and their standard-template copies are byte-identical.
- Plan-first upgrade reported 32 unchanged managed files and two protected repository controls, then updated only the two authorized managed lock digests.
- `doctor` passed after upgrade with the same 15 pre-existing `W013` placement advisories.
- No historical evidence path, VREC, RLS, release workflow, package version, browser template, CI topology, or governor descriptor was changed.
- Inspection initially reported three new `W-HEX-003` observations after the aggregate and Explorer definitions advanced to 2026-08-19. The accountable architecture and ADR records were reassessed against the new convention without changing their decisions. Final inspection reports no `W-HEX-*` warning and retains only pre-existing validator maintenance observations, derived provenance information, and the required `WO-EVK-001` assurance follow-up.

## Test and validation results

Commands used the repository editable environment at `.venv/Scripts/python.exe` with repository-local Git safe-directory configuration.

| Check | Result |
| --- | --- |
| Python compile of changed source and tests | pass |
| `python -m unittest tests.test_revision_provenance tests.test_dashboard_webui tests.test_inspection` | 64 passed, 2 skipped, 0 failures |
| `python -m unittest discover -s tests -p "test_*.py"` | 247 passed, 4 skipped, 0 failures |
| `python scripts/validate_engineering_artifacts.py --root .` before completion | pass; 479 artifacts, 0 errors, 44 pre-existing maintenance warnings |
| `python -m se_harness upgrade .` plan and `--apply` | pass; no customized/blocked file and no partial update |
| `python -m se_harness doctor .` | pass; managed integrity and exact released governor check pass |
| Root/template SHA-256 equality for both changed managed scripts | pass |
| `python -m se_harness --help` | pass; command surface unchanged |
| `python -m se_harness preflight . --work-order WO-EVK-001 --phase review` | pass with status `implemented` and commit-bound verification `required` |
| `python -m se_harness inspect . --json` | no `W-HEX-*` warning; exactly `WO-EVK-001` is assurance-pending |
| Two consecutive `python -m se_harness dashboard .` runs | pass; identical manifest SHA-256 `33a489aa5a321269895dff39c747e9345aad81356779711edc6467ad07769047` |

## Changed-file inventory

- New approved evidence-keying domain: intent, capability, four requirements, specification, architecture, ADR, verification, acceptance feature, work order, index, and this retained evidence.
- Reconciled active definitions: `REQ-DST-046`, `SPEC-DST-012`, `VER-DST-012`, `SPEC-AGR-001`, and `VER-AGR-001`; reassessed `ARCH-DST-009`, `ADR-DST-009`, `ARCH-AGR-001`, and `ADR-AGR-001` without changing their decisions.
- Runtime behavior: `se_harness/provenance.py`.
- Managed portable behavior: root and canonical-template validator/dashboard scripts plus `.engineering-harness.lock`.
- Verification: `tests/test_revision_provenance.py` and `tests/test_dashboard_webui.py`.
- Repository domain index: `docs/engineering/README.md`.

## Deviations and residual risk

No authorized-scope deviation is known. Structural attribution cannot prove that evidence content is substantively adequate for every associated work order. A later approved issue-49 change may enforce keying for single-work-order VRECs; this work intentionally preserves their current behavior. Commit-bound verification, release, build, commit, tag, push, publication, deployment, and governor promotion remain outside this implementation evidence.
