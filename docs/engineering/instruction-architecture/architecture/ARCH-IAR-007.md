+++
id = "ARCH-IAR-007"
type = "architecture"
title = "Single-validator assessment-plane classification"
status = "implemented"
owners = ["technical-owner", "engineering-owner", "quality-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
addresses = ["REQ-IAR-015"]
conforms_to = ["SPEC-IAR-007"]

[decision_assessment]
outcome = "adr_required"
triggers = ["public-interface-or-protocol", "cross-cutting-policy", "material-alternatives"]
rationale = "Diagnostic JSON and human output are public contracts used by operators, tests, CI, and Explorer. Classification affects every validator rule and has material implementation alternatives, so the representation requires an explicit architectural decision."
assessed_by = "technical-owner"
+++

# Architecture: Single-validator assessment-plane classification

## Context

One standard-library validator currently owns parsing, graph checks, governance invariants, reporting, and exit behavior. The taxonomy must clarify its results without creating parallel validators or changing its authority.

## Components

- **Plane vocabulary:** one closed, versioned set of four values.
- **Diagnostic construction:** every emission supplies an explicit plane together with code, path, and message.
- **Validation report:** retains errors and warnings and derives deterministic counts by plane.
- **Human renderer:** shows overall validity and plane summaries without a score.
- **JSON renderer:** adds taxonomy metadata while preserving existing fields.
- **Coverage tests:** prove every current emission is classified and baseline diagnostics are otherwise unchanged.
- **Managed distribution:** keeps the canonical validator, installed copy, package data, and lock aligned.

## Data flow

```text
validation rule
   -> Diagnostic(plane, code, path, message)
   -> error or warning collection
   -> ValidationReport
        |-> existing validity and exit code
        |-> human plane summary
        `-> additive JSON taxonomy fields
```

## Constraints

- Plane never determines severity or lifecycle authority.
- Renderers do not reclassify findings.
- Unknown plane values fail during development rather than being reported as `other`.
- Existing rule functions and diagnostic meanings remain intact.
- The validator remains Python 3.11+ standard-library-only and deterministic.
- Repository content remains untrusted data and no diagnostic value is executed.

## Related decision

`ADR-IAR-007` decides how plane ownership is represented in code and output.
