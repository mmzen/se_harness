+++
id = "ADR-REB-013"
type = "adr"
title = "Keep the interpreter-safety rule in code once the second runtime has no boundary"
status = "draft"
owners = ["technical-owner", "security-owner", "quality-owner"]
created = "2026-08-28"
updated = "2026-08-28"

[relations]
decides = ["ARCH-REB-013"]
+++

# ADR: Keep the interpreter-safety rule in code once the second runtime has no boundary

## Status

Proposed. Supersedes `ADR-REB-010`'s selection of option 6 for the situation
that option addressed; `ADR-REB-010` remains the record of why the rule
exists and how its cases were fixed.

## Context

`ADR-REB-010` (2026-08-24) faced six boundaries in two runtimes that
disagreed about interpreter safety, and a barrier: `repository_tools` must
not import `se_harness`. It chose a JSON declaration with one conforming
loader per runtime, a boundary registry and a cross-runtime corpus, over a
single implementation, precisely because a single implementation could not
serve both sides of the barrier.

Since then `WO-REB-028` deleted the four `repository_tools` boundaries and
`release_qualification.py`'s, and `WO-ECP-011` deleted the migration probe.
Measured on 2026-08-28 at `main` `f62256f`: one boundary
(`se_harness/runtime_identity.py`), one runtime; the `repository_tools`
loader has no caller; the registry has one entry; the corpus check compares a
live loader with a dead mirror. The apparatus is about 440 lines per copy
around a rule of about 300, and every new refusal case would touch two
modules, the JSON, the corpus and the tests (issue #220).

## Decision drivers

- Keep the rule and every `EPS` refusal exactly as they are; the incident
  they fixed (RC-060-06) is real.
- Remove machinery whose reason no longer exists rather than maintain it.
- Keep the `repository_tools` import barrier; it is unaffected.
- Keep the behavioural proof: each path form built for real on the lane that
  can build it.

## Considered options

1. **Keep the declaration and both loaders.** Nothing to do; the apparatus
   stays as insurance for a future second boundary. Rejected: a future
   boundary in `repository_tools` would be a new architecture decision in any
   case, and the insurance costs a dead 592-line mirror and a data document
   nobody reads as data.
2. **Delete the `repository_tools` copy only.** Halves the cost; leaves a
   declaration with one loader, an `ISD` validator for a document only its
   own tests read, and a registry of one. Rejected as stopping halfway.
3. **Rule in code, one runtime, tests own the corpus.** Selected.

## Decision

Select option 3. `se_harness/interpreter_safety.py` keeps `evaluate`, the
ordered `EPS` cases, the junction predicate and the recorded facts; the
loader, validators, registry, corpus accessors, the JSON and the
`repository_tools` copy are deleted; the tests carry the corpus inventory and
keep building every form. `REQ-REB-026` is retired by dated amendment;
`REQ-REB-030` and `SPEC-REB-015` state the new obligation. If a second
runtime ever needs the rule again, that is a new decision taken then, with
the `ADR-REB-010` options on record.

## Consequences

- Positive: one place states the rule; a new case touches one module and one
  test; ~1,300 lines leave (two copies' apparatus, the JSON, three test
  classes).
- Negative: the "declaration is data" reviewability `ADR-REB-010` valued is
  given up; a rule change is now a code change under the same review.
- Security: no refusal changes; the behavioural corpus is the proof, on both
  platforms, before and after.

## Validation

`VER-REB-014`.
