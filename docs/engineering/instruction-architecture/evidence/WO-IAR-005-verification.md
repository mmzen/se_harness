# WO-IAR-005 Verification Evidence

## Scope and authority

- Work order: `WO-IAR-005`
- Verification contract: `VER-IAR-005`
- Requirement: `REQ-IAR-013`
- Execution date: 2026-08-12
- Authorization: repository-owner instruction `ok for implementation`
- Authorized actions: bounded implementation and retained evidence
- Not authorized or performed: commit, push, pull-request creation, verification capture or transition, release, tag, package build, publication, or deployment

## Delivered relation model

- `ARCH.addresses -> REQ` declares only architecturally significant requirement drivers.
- `ARCH.conforms_to -> SPEC` declares detailed behavioral or interface contracts relevant to the architecture.
- Every addressed requirement must be included in the `specifies` targets of at least one conforming specification. The transitive set may contain additional routine requirements.
- Preflight retains specification and verification coverage for every work-order requirement without demanding fabricated architecture coverage for routine behavior.
- An active architecture that addresses a work-order requirement is applicable and must be selected; every selected typed architecture must share a conforming specification with the work order.
- Existing decision assessments and conditional `ADR.decides -> ARCH` coverage remain independent and unchanged.
- Explorer preserves declared edges and adds visibly derived `conforms_transitively_to_requirement` projections with their intermediate specification paths.

## Compatibility and diagnostics

| Code | Boundary |
| --- | --- |
| `E011` | Typed architecture relation targets the wrong artifact type |
| `E016` | Missing typed relations, duplicate values, incoherent triangle, or ambiguous/inconsistent compatibility declaration |
| `W015` | Completed legacy or consistent dual-declared architecture uses deprecated `constrains` |
| `W021` | Selected architecture is unrelated to selected work-order specifications or requirements |
| `W022` | Active architecture addressing work-order requirements is not selected |

Completed legacy `constrains` relations are classified as `legacy_requirement_trace` or `legacy_specification_trace`. Mixed target types fail closed. New or ongoing architecture must use the typed relations. Consistent dual declaration remains a bounded bootstrap case and receives `W015`. Installation and upgrade never rewrite repository-owned formal artifacts.

## Test-first observation

Before implementation, the new suite failed in 11 assertions across all 8 initial tests. The failures demonstrated that validation still required polymorphic `constrains`, preflight required architecture coverage for every requirement, no compatibility classifier existed, Explorer lacked typed/transitive state, and managed guidance still described the old model.

After implementation:

```text
python -m unittest tests.test_architecture_traceability
Ran 9 tests in 3.562s
OK
```

The final suite covers target types, non-array and injection-shaped values, duplicates, triangle coherence, status-bounded compatibility, consistent dual declarations, routine requirements, omitted applicable architecture, irrelevant selected architecture, declared-versus-derived Explorer relations, managed guidance, deterministic JSON, and byte preservation of repository-owned legacy architecture across repeated upgrades.

## Managed transactional upgrade

```text
python -m se_harness.cli upgrade . --apply
update     docs/engineering/QUALITY_GATES.md
update     docs/engineering/TRACEABILITY.md
update     docs/engineering/WORKFLOW.md
update     docs/engineering/templates/ARCHITECTURE.template.md
update     docs/engineering/templates/WORK_ORDER.template.md
summary: 33 files, 28 unchanged
upgraded managed files to se-harness 0.2.1

python -m se_harness.cli upgrade . --apply
summary: 33 files, 33 unchanged
```

Doctor confirms that canonical templates, self-hosted operational copies, and schema-2 lock entries match. The validator, dashboard generator, and Explorer template are byte-identical to their canonical distribution copies. The managed router was not changed because relation semantics belong to focused traceability, workflow, and quality policy.

## Validation and preflight

```text
python scripts/validate_engineering_artifacts.py --root .
Engineering artifact validation: PASS
Artifacts: 224 | Errors: 0 | Warnings: 36

python -m se_harness.cli preflight . --work-order WO-IAR-005
Harness preflight: PASS

python -m se_harness.cli preflight . --work-order WO-IAR-005 --phase review
Harness preflight: PASS

python -m se_harness.cli doctor .
PASS
```

The 36 warnings are the expected migration and historical advisories: 15 `W015` legacy architecture relations, 14 `W014` legacy decision assessments, and 7 pre-existing `W013` historical locations. The candidate CI lane executes candidate review preflight, validator, and Explorer, so it inherits the new behavior. The exact released `0.2.0` independent baseline continues to enforce only previously released behavior until a separately governed release and pin update.

## Dual-runtime regression

```text
python --version
Python 3.14.6

python -m unittest discover -s tests -p "test_*.py"
Ran 111 tests in 50.198s
OK (skipped=3)

.\target\release-0.2.1-final\smoke-venv-311\Scripts\python.exe --version
Python 3.11.9

.\target\release-0.2.1-final\smoke-venv-311\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"
Ran 111 tests in 49.742s
OK (skipped=3)
```

The three skips are existing environment-dependent skips; the change introduces no skip. Existing verification-record `conforms_to`, ADR applicability, revision provenance, installer, managed integrity, and instruction-routing tests remain green.

## Explorer determinism

The final repository dashboard was generated twice from the completed implementation. Both `dashboard-data.json` files were byte-identical. Final artifact/relation counts and snapshot hash are recorded after lifecycle completion below.

```text
Artifacts: 224 | Relations: 732 | Errors: 0 | Warnings: 37
Snapshot: a9cd2f4167a2e848361fdbe7d77333c6d4908c4b61e322d46e522bd8c35202bd
```

`ARCH-IAR-005` must appear as typed, address `REQ-IAR-013`, conform to `SPEC-IAR-005`, project the transitive requirement through that specification, and remain covered by `ADR-IAR-005`.

## Security and residual risk

Tests treat relation content and artifact types as parsed data, including deceptive prefixes, non-array values, Unicode-capable JSON serialization, and an injection-shaped unknown target. No relation value enters a shell. Repeated upgrade testing proves a repository-owned legacy architecture remains byte-identical.

Typed metadata cannot prove that authors disclosed every architecturally significant requirement. Accountable technical review must challenge suspicious omissions. The legacy classifier intentionally preserves old meaning imperfectly: it reports target class but never infers which requirements were significant. Removing that compatibility behavior requires a later governed release with migration evidence.
