+++
id = "VER-REB-014"
type = "verification"
title = "Verify the interpreter-safety rule kept in code at one boundary"
status = "draft"
owners = ["assurance-owner", "security-owner"]
created = "2026-08-28"
updated = "2026-08-28"
[relations]
verifies = ["REQ-REB-030"]
+++

# Verification: Verify the interpreter-safety rule kept in code at one boundary

## Method

| Requirement | Method | Pass condition |
| --- | --- | --- |
| `REQ-REB-030` | behavioural suite `tests/test_interpreter_safety.py` on Linux and Windows | every corpus form constructable on the lane yields the same `EPS` case or acceptance as at the base commit; `RecordedFactsTests`, `PurityAndCostTests`, `JunctionPredicateTests` green |
| `REQ-REB-030` | static | `se_harness/interpreter_safety.json` and `repository_tools/interpreter_safety.py` absent; no withdrawn name in `se_harness/`, `repository_tools/`, `scripts/`, `.github/`; `EVALUATION_ORDER` unchanged; `runtime_identity.py` unchanged |
| `REQ-REB-030` | import barrier | `ImportBarrierTests` green: `repository_tools` imports only the standard library and its own package |
| `REQ-REB-030` | packaging | candidate wheel carries `se_harness/interpreter_safety.py` and no `interpreter_safety.json`; `check_portable_release_surface.py --wheel` and `--repository` PASS |
| `REQ-REB-030` | released root | 0.8.0 `validate` 0 errors, `doctor` 0 FAIL; full suite; the pull request's lanes |

## Independence

Readings under the released 0.8.0 root are taken outside the checkout; the
suite runs candidate source. The assurance decision is the assurance owner's.

## Evidence

`docs/engineering/released-evaluator-boundary/evidence/WO-REB-030-verification.md`.
