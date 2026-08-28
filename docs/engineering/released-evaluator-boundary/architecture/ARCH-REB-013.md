+++
id = "ARCH-REB-013"
type = "architecture"
title = "One interpreter-safety rule, one runtime"
status = "approved"
owners = ["technical-owner", "security-owner"]
created = "2026-08-28"
updated = "2026-08-28"
[relations]
addresses = ["REQ-REB-030"]
conforms_to = ["SPEC-REB-015"]
[decision_assessment]
outcome = "adr_required"
triggers = ["security-privacy-or-trust-boundary", "difficult-to-reverse"]
rationale = "ADR-REB-010 selected a declared data document with one loader per runtime over a single implementation, for a trust-boundary rule; removing the declaration reverses that selection and is recorded as a superseding decision, ADR-REB-013, not as an incidental refactor."
assessed_by = "technical-owner"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T19:36:39Z"
decided_by = "technical-owner"
reason = "Approved on 2026-08-28 by the accountable owner, 'Approve and start', for issue #220: with one identity boundary left in one runtime after WO-REB-028 and WO-ECP-011, the interpreter-safety rule stays in code and its declaration apparatus and the repository_tools mirror are deleted, the tests owning the corpus. Measured before this transition over branch state cdc48a6 carrying unmoved main f62256f under the governing exact public 0.8.0 root: validate PASS at 0 errors; rehearsal on a throwaway export: tests.test_interpreter_safety 65 OK, full suite 989 tests with only the known workstation file-mode failure, 0.8.0 doctor 0 FAIL, portable-surface repository and wheel checks PASS."
+++

# Architecture: One interpreter-safety rule, one runtime

## Boundary

`se_harness/interpreter_safety.py` is the rule. Its one consumer is
`se_harness/runtime_identity.py`, which applies it to `sys.executable` for the
environment-bounded roles and turns a refusal into a diagnostic. The
`repository_tools` runtime validates no interpreter and imports no
`se_harness` module; the import barrier of `ARCH-REB-010` stands, with
nothing left on the far side of it that needs the rule.

## What replaces what

| `ARCH-REB-010` component | Now |
| --- | --- |
| declaration `interpreter_safety.json` | gone; `EVALUATION_ORDER` in code |
| package loader | the rule module, without the loader half |
| repository-tools loader | gone (no caller since `WO-REB-028`) |
| boundary registry + registry check | gone; `StaticArchitectureTests` keep the pinned inventory of modules that reach the rule |
| cross-runtime corpus | gone; the tests own the corpus and build each form |
| trust boundaries, required and prohibited patterns of `ARCH-REB-010` | unchanged, except those that name two runtimes |

## Why an ADR

`ADR-REB-010` chose the declaration to make two runtimes agree without
crossing the barrier. With one runtime that problem no longer exists;
`ADR-REB-013` records the supersession so the reason the apparatus was built,
and the reason it is removed, are both on record.
