# WO-IAR-003 Verification Evidence

## Scope and authority

- Work order: `WO-IAR-003`
- Verification contract: `VER-IAR-003`
- Requirement: `REQ-IAR-011`
- Execution date: 2026-08-12
- Authorization: repository-owner instruction `ok, make the change accordingly then`
- Authorized actions: bounded implementation and retained evidence
- Not authorized or performed: commit, push, pull-request creation, verification capture or transition, release, tag, package build, publication, or deployment

## Delivered responsibility boundary

- `ENGINEERING_HARNESS.md` routes review and visualization to `WORKFLOW.md` and `QUALITY_GATES.md` and retains the derived-evidence boundary.
- `WORKFLOW.md` owns the exact review-preflight and dashboard commands and instructs the actor to inspect candidate consistency and anomalies.
- Preflight and Explorer remain observations; neither approves work nor verifies a candidate.
- Canonical templates, operational copies, and schema-2 lock entries were reconciled through the supported upgrade path.

## Test-first observation

Before the canonical templates changed:

```text
python -m unittest tests.test_instruction_architecture.InstructionArchitectureTests.test_workflow_owns_review_and_visualization_procedure tests.test_instruction_architecture.InstructionArchitectureTests.test_review_routing_upgrade_is_transactional_and_idempotent
Ran 2 tests
FAILED (failures=2)
```

The failures proved that the router still owned both exact commands and workflow step 6 lacked the dashboard/inspection procedure. After the template changes, the same two tests passed.

## Transactional managed upgrade

```text
python -m se_harness upgrade .
update     ENGINEERING_HARNESS.md
update     docs/engineering/WORKFLOW.md
summary: 33 files, 31 unchanged

python -m se_harness upgrade . --apply
update     ENGINEERING_HARNESS.md
update     docs/engineering/WORKFLOW.md
summary: 33 files, 31 unchanged
upgraded managed files to se-harness 0.2.1

python -m se_harness upgrade .
summary: 33 files, 33 unchanged
```

The focused exact-prior fixture upgraded both files and both digests together. A second apply was idempotent. A workflow customization blocked the otherwise eligible router update and preserved both files and the original lock, demonstrating no-partial-write behavior.

## Focused tests

```text
python -m unittest tests.test_instruction_architecture
Ran 12 tests in 7.755s
OK
```

The suite covers exact responsibility, absence of commands from the router review section, presence and ordering in workflow step 6, two-file exact-prior migration, idempotence, customization preservation, fresh installation, ownership modes, preflight, CI, and integrity behavior.

## Dual-runtime regression

```text
python --version
Python 3.14.6

python -m unittest discover -s tests -p "test_*.py"
Ran 94 tests in 43.857s
OK (skipped=3)

.\target\release-0.2.1-final\smoke-venv-311\Scripts\python.exe --version
Python 3.11.9

.\target\release-0.2.1-final\smoke-venv-311\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"
Ran 94 tests in 43.414s
OK (skipped=3)
```

The three skips are existing environment-dependent skips; no new skip was introduced.

## Graph, integrity, and interfaces

```text
python scripts/validate_engineering_artifacts.py --root .
Engineering artifact validation: PASS
Artifacts: 212 | Errors: 0 | Warnings: 7

python -m se_harness doctor .
PASS

python -m se_harness --help
PASS

git diff --check
PASS
```

Doctor reported the canonical distribution and installed managed copies of both `ENGINEERING_HARNESS.md` and `docs/engineering/WORKFLOW.md` match and are unchanged relative to the regenerated lock. The seven warnings are existing `W013` historical-location advisories unrelated to this work order.

## Final review and Explorer

```text
python -m se_harness preflight . --work-order WO-IAR-003 --phase review
Harness preflight: PASS
Work order: WO-IAR-003 (implemented)

python -m se_harness dashboard .
Harness Explorer generation: PASS
Artifacts: 212 | Relations: 710 | Errors: 0 | Warnings: 8
Snapshot: 05c37d669d8a733a3afe6f9d3e7fb44176c4844ffee3ad529893fd4a6a3bcd37

python -m se_harness dashboard .
Harness Explorer generation: PASS
Artifacts: 212 | Relations: 710 | Errors: 0 | Warnings: 8
Snapshot: 05c37d669d8a733a3afe6f9d3e7fb44176c4844ffee3ad529893fd4a6a3bcd37
```

The additional Explorer warning is the existing informational stale-ready observation for `VREC-AGR-001`.

## Manual assessment

- The router no longer contains `--phase review` or `harnessctl dashboard .` in its review section.
- Workflow step 6 retains evidence-keying, exact review preflight, dashboard generation, and candidate consistency/anomaly inspection before the candidate commit step.
- The router explicitly states that neither output approves work nor verifies a candidate.
- No preflight, dashboard, lifecycle, quality-gate, traceability, ownership-mode, schema, or historical-record behavior changed.

## WO-IAR-003 attributable paths

- `.engineering-harness.lock`
- `ENGINEERING_HARNESS.md`
- `docs/engineering/WORKFLOW.md`
- `templates/repository/standard/ENGINEERING_HARNESS.md.tpl`
- `templates/repository/standard/docs/engineering/WORKFLOW.md`
- `tests/test_instruction_architecture.py`
- `docs/engineering/instruction-architecture/README.md`
- `docs/engineering/instruction-architecture/acceptance/instruction-architecture.feature`
- `docs/engineering/instruction-architecture/requirements/REQ-IAR-011.md`
- `docs/engineering/instruction-architecture/specifications/SPEC-IAR-003.md`
- `docs/engineering/instruction-architecture/architecture/ARCH-IAR-003.md`
- `docs/engineering/instruction-architecture/architecture/adr/ADR-IAR-003.md`
- `docs/engineering/instruction-architecture/verification/VER-IAR-003.md`
- `docs/engineering/instruction-architecture/work-orders/WO-IAR-003.md`
- `docs/engineering/instruction-architecture/evidence/WO-IAR-003-verification.md`

## Deviations and residual risk

- Deviations: none.
- Residual risk: structural checks cannot prove that an actor meaningfully inspects the candidate or interprets anomalies correctly. Accountable review remains the mitigation.
- Assurance status: implementation evidence is complete, but no commit-bound verification record has been prepared or transitioned.
