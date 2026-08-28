+++
id = "REQ-REB-030"
type = "requirement"
title = "Keep the interpreter-safety rule as one implementation at its one boundary"
status = "draft"
owners = ["technical-owner", "security-owner"]
created = "2026-08-28"
updated = "2026-08-28"
statement = "WHILE se_harness/runtime_identity.py is the only code path validating an interpreter for an evaluator-identity purpose, THE SYSTEM SHALL implement the interpreter-safety rule once, in code, in the package runtime, with every EPS refusal and the terminal-link acceptance unchanged and proven by tests."
verification_method = ["test", "analysis"]
priority = "must"
source = "issue #220 (complexity audit P1-8); WO-REB-028 and WO-ECP-011, which retired every other identity boundary"
measure = "one interpreter_safety.py, under se_harness/; no interpreter_safety.json and no repository_tools copy; the behavioural corpus of REQ-REB-024 green on Linux and Windows; every EPS identifier and runtime_identity's EPS011 diagnostic unchanged"
[relations]
derives_from = ["CAP-REB-001"]
+++

# Requirement: Keep the interpreter-safety rule as one implementation at its one boundary

## Statement

WHILE `se_harness/runtime_identity.py` is the only code path that validates
an interpreter for an evaluator-identity purpose, THE SYSTEM SHALL implement
the interpreter-safety rule once, in code, in the package runtime, with every
`EPS` refusal of `REQ-REB-024` and the terminal-link acceptance of
`REQ-REB-023` unchanged and proven by tests that build each path form.

## Rationale

`REQ-REB-026` asked for one rule shared by two runtimes because six
boundaries in two runtimes disagreed and `repository_tools` could not import
`se_harness`. `WO-REB-028` deleted the four `repository_tools` boundaries and
`release_qualification.py`'s; `WO-ECP-011` deleted the migration probe. One
boundary remains, in one runtime. The apparatus that made two runtimes agree
— a JSON declaration, a loader that validates it (`ISD` codes), a boundary
registry, a conformance corpus (`ISC` codes) and a second loader — now
checks a live loader against a dead mirror with no caller. The rule itself
(`evaluate`, the `EPS` cases in order, the junction predicate with its 3.11
fallback) fixed a real incident and stays.

## Acceptance

- `se_harness/interpreter_safety.py` holds the rule; `EVALUATION_ORDER` is
  the ordered case list; `evaluate`, `SafeEntryPoint`, `refusal_case`,
  `normalized_origin`, `link_classification_available` and the `EPS`
  identifiers keep their names and behaviour.
- `se_harness/interpreter_safety.json` and `repository_tools/interpreter_safety.py`
  do not exist; the `ISD` and `ISC` families are withdrawn and their names
  reserved.
- `tests/test_interpreter_safety.py` owns the corpus of forms (constructable
  platforms and unconstructable reasons) and builds each form for real; the
  behavioural classes are unchanged in what they prove.
- `repository_tools` still imports only the standard library and its own
  package (the barrier is unchanged; it simply no longer needs a copy).
