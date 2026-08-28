+++
id = "ARCH-REB-013"
type = "architecture"
title = "One interpreter-safety rule, one runtime"
status = "draft"
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
