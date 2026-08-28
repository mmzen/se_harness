+++
id = "SPEC-REB-015"
type = "specification"
title = "Interpreter-safety rule in code, one runtime"
status = "draft"
owners = ["technical-owner", "security-owner"]
created = "2026-08-28"
updated = "2026-08-28"
[relations]
specifies = ["REQ-REB-030"]
+++

# Specification: Interpreter-safety rule in code, one runtime

## Purpose

Bound the removal of the declaration apparatus around the interpreter-safety
rule, and what must be true afterwards. `SPEC-REB-011` rules 1–11 remain the
definition of the rule and its `EPS` cases; this specification replaces its
rules 12–13 and the retired per-boundary rules 21–26.

## Rules

1. **The rule is code.** `se_harness/interpreter_safety.py` implements the
   rule; `EVALUATION_ORDER` is the ordered case list and the first refusal
   wins, so a path form yields a stable `EPS` identifier. Nothing reads the
   rule as data; no JSON declaration exists.
2. **One runtime.** There is no `repository_tools` loader. The
   `repository_tools` import barrier of `ARCH-REB-010` is unchanged;
   `ImportBarrierTests` keep proving it.
3. **Kept names.** `evaluate`, `SafeEntryPoint`, `refusal_case`,
   `normalized_origin`, `link_classification_available`,
   `reparse_information_observable`, `JUNCTION_PREDICATE`, `POSITION_CLASSES`,
   `PLATFORMS`, `EVALUATION_ORDER`, `InterpreterSafetyError`,
   `InterpreterSafetyRefusal` and every `EPS0xx` identifier keep their names
   and behaviour; `runtime_identity.py`'s `EPS011` diagnostic is unchanged.
4. **Withdrawn names.** `load_declaration`, `declaration_bytes`,
   `declared_cases`, `declared_boundaries`, `declared_corpus`,
   `boundary_identifiers`, the `ISD1xx` and `ISC0xx` families and the schema
   identifier `se-harness-interpreter-safety-v1` are withdrawn; the names are
   reserved and never reused.
5. **Tests own the corpus.** `tests/test_interpreter_safety.py` carries the
   corpus inventory (form, constructable platforms, unconstructable reason)
   the declaration used to carry, builds every constructable form for real
   on the lane that can, and asserts the case; a form no lane can construct
   records why. The behavioural classes (`RuleEvaluationTests`,
   `RecordedFactsTests`, `PurityAndCostTests`, `JunctionPredicateTests`,
   `PlatformCoverageTests`) prove what they proved before.
6. **Packaging.** `interpreter_safety.json` leaves package data, the wheel and
   the portable-surface required members; `interpreter_safety.py` stays
   required.
7. **No behaviour change.** No accepted path becomes refused and no refused
   path becomes accepted; `RuntimeIdentity`'s schema identifier and fields
   are unchanged.

## Error and recovery

A behavioural test that changes outcome, a lost `EPS` identifier, a caller
of a withdrawn name, or a `repository_tools` import of `se_harness` stops the
work order.
