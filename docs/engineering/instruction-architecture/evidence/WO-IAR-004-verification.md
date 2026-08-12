# WO-IAR-004 Verification Evidence

## Scope and authority

- Work order: `WO-IAR-004`
- Verification contract: `VER-IAR-004`
- Requirement: `REQ-IAR-012`
- Execution date: 2026-08-12
- Authorization: repository-owner instruction `ok for implementation`
- Authorized actions: bounded implementation and retained evidence
- Not authorized or performed: commit, push, pull-request creation, verification capture or transition, release, tag, package build, publication, or deployment

## Delivered decision model

- Every new or ongoing architecture declares one structured `decision_assessment` with outcome `adr_required` or `no_significant_decision`.
- The validator enforces the controlled trigger vocabulary, uniqueness, outcome-trigger consistency, bounded non-empty rationale and assessor values, architecture-only placement, and active deciding-ADR coverage.
- Preflight evaluates each selected architecture separately. `adr_required` needs a selected active ADR deciding that architecture; `no_significant_decision` does not create a ceremonial ADR.
- One ADR may decide several architectures when it records one coherent decision. ADR count is independent of requirement count.
- Completed legacy architecture without an assessment emits an advisory and remains preflight-eligible only with an already-active selected deciding ADR.
- Explorer exposes assessment outcome, triggers, rationale, assessor, deciding ADRs, and a derived coverage state. Validator diagnostics become visible anomalies without creating authority.

## Stable diagnostics exercised

| Code | Boundary |
| --- | --- |
| `E014` | Missing, malformed, contradictory, or misplaced decision assessment |
| `E015` | `adr_required` or completed legacy architecture lacks an active deciding ADR |
| `W014` | Repository-wide completed-legacy migration advisory |
| `W017` | Selected ADR decides no selected architecture |
| `W018` | Selected `adr_required` architecture lacks a selected active deciding ADR |
| `W019` | Selected completed-legacy architecture lacks a selected active deciding ADR |
| `W020` | Selected architecture has a missing or invalid assessment |

Test inputs include missing and unknown outcomes, unknown and duplicate triggers, contradictory trigger cardinality, empty and oversized text, non-architecture placement, and an injection-shaped trigger. Values remain parsed data and never enter a shell.

## Test-first observation and focused verification

Before implementation, the new fixture suite failed across the metadata, conditional preflight, legacy, and Explorer behaviors, demonstrating the absence of structured assessment enforcement and the old unconditional ADR rule. After implementation:

```text
python -m unittest tests.test_adr_applicability
Ran 8 tests in 3.318s
OK
```

The tests cover the metadata matrix, per-architecture coverage, a justified no-ADR case, unrelated ADR rejection, completed legacy behavior, ongoing-state fail-closed behavior, distributed authoring guidance, Explorer state, and anomaly projection.

## Managed installation and transactional upgrade

```text
python -m se_harness.cli upgrade . --apply
update     docs/engineering/DECISION_RIGHTS.md
update     docs/engineering/QUALITY_GATES.md
update     docs/engineering/TRACEABILITY.md
update     docs/engineering/WORKFLOW.md
update     docs/engineering/templates/ADR.template.md
update     docs/engineering/templates/ARCHITECTURE.template.md
update     docs/engineering/templates/WORK_ORDER.template.md
summary: 33 files, 26 unchanged
upgraded managed files to se-harness 0.2.1

python -m se_harness.cli upgrade . --apply
summary: 33 files, 33 unchanged
```

Doctor confirmed canonical distribution, operational copies, and schema-2 lock parity for all 33 managed files. Runtime/template validator, dashboard, and Explorer files are byte-identical. Existing repository-owned formal artifacts were not rewritten.

## Preflight, validation, and interfaces

```text
python -m se_harness.cli preflight . --work-order WO-IAR-004
Harness preflight: PASS

python -m se_harness.cli preflight . --work-order WO-IAR-004 --phase review
Harness preflight: PASS

python scripts/validate_engineering_artifacts.py --root .
Engineering artifact validation: PASS
Artifacts: 218 | Errors: 0 | Warnings: 21

python -m se_harness.cli doctor .
PASS

python -m se_harness --help
PASS

git diff --check
PASS
```

The warnings comprise 14 expected `W014` completed-legacy migration advisories and 7 pre-existing `W013` historical-location advisories. The existing CI candidate lane runs the candidate review preflight, validator, and Explorer, so it inherits the new rule. Its exact released `0.2.0` independent-baseline lane continues to enforce only prior released behavior; candidate tests and candidate checks provide evidence for this unreleased behavior until a separately governed release and pin update.

## Explorer determinism

Two consecutive repository dashboard generations produced byte-identical `dashboard-data.json`:

```text
Artifacts: 218 | Relations: 720 | Errors: 0 | Warnings: 22
Snapshot: ee24c66f86ddc96721de6c44159ca197f1b27e80142c7f9ea188caac0fd12745
```

`ARCH-IAR-004` is projected as `adr_required_covered`, with triggers `cross-cutting-policy`, `difficult-to-reverse`, and `material-alternatives`, assessed by `technical-owner`, and covered by `ADR-IAR-004`.

## Dual-runtime regression

```text
python --version
Python 3.14.6

python -m unittest discover -s tests -p "test_*.py"
Ran 102 tests in 46.521s
OK (skipped=3)

.\target\release-0.2.1-final\smoke-venv-311\Scripts\python.exe --version
Python 3.11.9

.\target\release-0.2.1-final\smoke-venv-311\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"
Ran 102 tests in 46.471s
OK (skipped=3)
```

The three skips are pre-existing environment-dependent skips; the change adds no skip.

## Manual assessment and residual risk

The authoring template makes first-design significance prominent without declaring every first design automatically significant. Policies assign assessment and no-ADR acceptance to the technical owner; an implementation agent may draft but not silently self-approve the result. The work-order template makes conditional ADR selection explicit, while traceability states that `ADR.decides -> ARCH` establishes coverage.

Structural checks cannot prove that an author disclosed every material decision or that a `no_significant_decision` rationale is truthful. Accountable technical review must still challenge architecture prose and candidate changes. The legacy exception is intentionally temporary and should be removed only through a separately governed release after migration evidence exists.
