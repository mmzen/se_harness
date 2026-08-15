+++
id = "ARCH-IAR-009"
type = "architecture"
title = "Closed guidance catalog over inspection sources"
status = "implemented"
owners = ["technical-owner", "engineering-owner", "quality-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
addresses = ["REQ-IAR-017"]
conforms_to = ["SPEC-IAR-008", "SPEC-IAR-009"]

[decision_assessment]
outcome = "adr_required"
triggers = ["public-interface-or-protocol", "cross-cutting-policy", "responsibility-or-dependency-direction", "material-alternatives"]
rationale = "Suggestions extend the public inspection JSON contract and must choose whether guidance is governed static policy, repository-derived inference, or generated advice. That authority and dependency direction affects operator trust and future remediation capabilities."
assessed_by = "technical-owner"
+++

# Architecture: Closed guidance catalog over inspection sources

## Lifecycle

Approved on 2026-08-15 through the repository owner's instruction `ok i approve`; the accountable technical decision is recorded by `ADR-IAR-009`.

## Context

Inspection already has two trustworthy source categories: mechanical lifecycle queues and findings produced by the validator or Harness Explorer. Adding advice creates a new responsibility boundary because a plausible next step can easily be mistaken for eligibility, authorization, or an instruction to mutate the repository.

## Components and responsibilities

- **Existing producers:** validator, Explorer snapshot, and inspection queue projection continue to own all observations and their authority.
- **Guidance catalog:** maps only approved queue action classes and selected derived warning rule IDs to static action, message, and accountable-role records.
- **Suggestion projector:** copies source identifiers and affected artifact IDs, applies the closed catalog, and emits `automatic = false`.
- **Renderers:** expose individual source traceability in JSON and compact grouping in human output.
- **Managed distribution:** keeps root and canonical scripts, package data, documentation, tests, and lock metadata synchronized.

## Data and dependency flow

```text
existing inspection queues -------------------+
                                               |
existing findings -- rule/severity/authority -+--> closed catalog lookup
                                                      |
                                                      v
                                           structured suggestion records
                                                |                |
                                                v                v
                                           human grouping   JSON traceability
```

The catalog depends on stable source identifiers. Existing producers do not depend on the catalog, and the catalog cannot change their output.

## Authority and trust boundary

Catalog matching uses only explicit machine fields. Repository-controlled titles, messages, paths, evidence, and prose are displayed as untrusted data but never select or construct advice. A suggestion identifies a review path and accountable role; it never claims that the action is valid for the current facts.

The repository-local producer limitation from `ARCH-IAR-008` remains. Suggestions do not resolve the independent-evaluator boundary and are not assurance evidence by themselves.

## Failure behavior

- Unknown, informational, validator-owned, or uncatalogued findings remain visible without suggestions.
- Missing catalog coverage is not a validation error and does not change inspection exit behavior.
- Invalid catalog constants fail focused tests and, where detected at runtime, fail inspection rather than emitting ambiguous advice.
- Rendering escapes control characters and writes nothing.

## Related ADR

`ADR-IAR-009` decides to use a small closed catalog rather than free-form or repository-configurable advice.
