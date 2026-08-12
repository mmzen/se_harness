# WO-IAR-002 Verification Evidence

## Scope and authority

- Work order: `WO-IAR-002`
- Verification contract: `VER-IAR-002`
- Requirement: `REQ-IAR-010`
- Execution date: 2026-08-12
- Authorization: repository-owner instruction `ok for implementation`
- Authorized actions: bounded implementation and retained evidence
- Not authorized or performed: commit, push, pull-request creation, verification capture or transition, release, tag, package build, publication, or deployment

## Delivered change

- Replaced the duplicated verification/release command sequence in the canonical managed router with the approved invariant-and-route contract.
- Reconciled the self-hosted `ENGINEERING_HARNESS.md` and its schema-2 lock entry through `harnessctl upgrade . --apply`.
- Preserved `WORKFLOW.md` as the owner of ordered verification and release procedure and left `DECISION_RIGHTS.md`, `QUALITY_GATES.md`, and `TRACEABILITY.md` unchanged.
- Added focused tests for semantic responsibility, fresh installation, safe upgrade from the prior router, idempotence, and fail-closed customized-content preservation.
- Added the accepted instruction-architecture scenario and the complete incremental formal chain.

## Test-first observation

Before the canonical template changed, the two new focused tests failed as expected:

```text
python -m unittest tests.test_instruction_architecture.InstructionArchitectureTests.test_router_keeps_invariants_while_workflow_owns_ordered_procedure tests.test_instruction_architecture.InstructionArchitectureTests.test_router_responsibility_refinement_upgrades_safely
Ran 2 tests
FAILED (failures=2)
```

The failures showed that the new invariant summary was absent and the prior procedural paragraph remained. After the template change, the same command passed two tests.

## Managed upgrade and parity

```text
python -m se_harness upgrade .
update     ENGINEERING_HARNESS.md
summary: 33 files, 32 unchanged

python -m se_harness upgrade . --apply
update     ENGINEERING_HARNESS.md
summary: 33 files, 32 unchanged
upgraded managed files to se-harness 0.2.1

python -m se_harness upgrade .
summary: 33 files, 33 unchanged
```

The supported upgrade changed the operational router and regenerated its lock digest. A subsequent plan was a no-op. `doctor` reported both `distribution:ENGINEERING_HARNESS.md: matches distribution` and `managed:ENGINEERING_HARNESS.md: unchanged`.

## Focused verification

```text
python -m unittest tests.test_instruction_architecture
Ran 10 tests in 6.484s
OK
```

The focused suite includes:

- required invariant presence and direct policy routing;
- absence of the duplicated router procedure;
- preservation of `capture-verification`, assurance transition, `prepare-release`, aggregate coverage, and tagging procedure in `WORKFLOW.md`;
- fresh installation output;
- upgrade from the exact prior managed router;
- repeated-upgrade idempotence;
- customized managed-router conflict and no-write preservation;
- ownership-mode, preflight, CI, and schema-2 integrity regression coverage.

## Full regression verification

Runtime discovery:

```text
python --version
Python 3.14.6

.\target\release-0.2.1-final\smoke-venv-311\Scripts\python.exe --version
Python 3.11.9
```

Full local runtime:

```text
python -m unittest discover -s tests -p "test_*.py"
Ran 92 tests in 42.148s
OK (skipped=3)
```

Retained Python 3.11 runtime:

```text
.\target\release-0.2.1-final\smoke-venv-311\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"
Ran 92 tests in 42.882s
OK (skipped=3)
```

The three skips are existing environment-dependent skips; no new skip was introduced.

## Graph, integrity, CLI, and Explorer

```text
python scripts/validate_engineering_artifacts.py --root .
Engineering artifact validation: PASS
Artifacts: 206 | Errors: 0 | Warnings: 7

python -m se_harness doctor .
PASS

python -m se_harness --help
PASS

python -m se_harness dashboard .
Harness Explorer generation: PASS
Artifacts: 206 | Relations: 700 | Errors: 0 | Warnings: 8
Snapshot: 5fd7b785e27400b142e50c6a93a3908dff2a75d178b2a990e1b993b7188f3231

python -m se_harness dashboard .
Harness Explorer generation: PASS
Artifacts: 206 | Relations: 700 | Errors: 0 | Warnings: 8
Snapshot: 5fd7b785e27400b142e50c6a93a3908dff2a75d178b2a990e1b993b7188f3231
```

The seven validator and doctor warnings are existing `W013` location advisories for historical artifacts. The additional Explorer warning is the existing informational stale-ready observation for `VREC-AGR-001`. Neither warning class was introduced or modified by this work order.

## Manual responsibility assessment

- `ENGINEERING_HARNESS.md` retains the exact candidate-commit binding, later governance-commit requirement, accountable decision-right boundary, and prohibition on commit, push, tag, release, publication, and deployment.
- The router directly names `WORKFLOW.md`, `QUALITY_GATES.md`, `TRACEABILITY.md`, and `DECISION_RIGHTS.md`.
- The ordered verification and release procedure remains intact in `WORKFLOW.md`, including aggregate arguments, assurance transition, release preparation, and separate tagging.
- No focused policy body, CLI implementation, artifact schema, historical VREC/RLS fact, ownership mode, installation profile, or external interface changed.
- `git diff --check` passed.

## Changed paths

- `.engineering-harness.lock`
- `ENGINEERING_HARNESS.md`
- `templates/repository/standard/ENGINEERING_HARNESS.md.tpl`
- `tests/test_instruction_architecture.py`
- `docs/engineering/instruction-architecture/README.md`
- `docs/engineering/instruction-architecture/acceptance/instruction-architecture.feature`
- `docs/engineering/instruction-architecture/requirements/REQ-IAR-010.md`
- `docs/engineering/instruction-architecture/specifications/SPEC-IAR-002.md`
- `docs/engineering/instruction-architecture/architecture/ARCH-IAR-002.md`
- `docs/engineering/instruction-architecture/architecture/adr/ADR-IAR-002.md`
- `docs/engineering/instruction-architecture/verification/VER-IAR-002.md`
- `docs/engineering/instruction-architecture/work-orders/WO-IAR-002.md`
- `docs/engineering/instruction-architecture/evidence/WO-IAR-002-verification.md`

## Deviations and residual risk

- Deviations: none.
- Residual risk: textual and structural tests cannot prove that an actor reads or correctly interprets the routed policies. Managed integrity, preflight, independent CI, and accountable review retain their established mitigation roles.
- Assurance status: implementation evidence is complete, but no commit-bound VREC has been prepared or transitioned by this work order.
