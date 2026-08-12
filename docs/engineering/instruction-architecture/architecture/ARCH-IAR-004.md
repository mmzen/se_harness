+++
id = "ARCH-IAR-004"
type = "architecture"
title = "Conditional architecture-decision assurance"
status = "implemented"
owners = ["technical-owner", "engineering-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
constrains = ["REQ-IAR-012"]

[decision_assessment]
outcome = "adr_required"
triggers = ["cross-cutting-policy", "difficult-to-reverse", "material-alternatives"]
rationale = "The harness must choose between unconditional ADR selection, optional agent judgment, and explicit conditional applicability enforced across authoring and readiness boundaries."
assessed_by = "technical-owner"
+++

# Architecture: Conditional architecture-decision assurance

## Context and scope

The artifact graph already models architecture and ADRs and preflight currently requires at least one selected ADR. The new boundary makes the applicability decision explicit on each architecture so automation can distinguish significant decisions from routine conformance without attempting semantic inference.

## Components and responsibilities

- **Architecture artifact:** holds the structured applicability assessment and its accountable rationale.
- **ADR artifact:** records a significant coherent decision and targets every architecture it decides.
- **Artifact validator:** verifies metadata shape, controlled vocabulary, and contradictions without evaluating prose truth.
- **Preflight:** composes selected architecture assessments with selected active ADR relations and blocks incomplete coverage.
- **Managed policy and templates:** tell agents when and how to assess significance and where decision authority resides.
- **Harness Explorer:** visualizes coverage state and anomalies per architecture.
- **CI:** executes the same validation and review-preflight behavior using an independent released baseline when available.

## Dependency direction

Requirements are covered by specification, architecture, and verification. Work orders select applicable architecture and ADR artifacts. ADRs point to architectures through `decides`; they do not point one-to-one at requirements. Validation and views consume formal metadata without becoming authority.

## Data and control flow

```text
requirement/specification
          |
          v
architecture + decision assessment
          |
          +-- adr_required ----------> active ADR decides architecture
          |
          +-- no_significant_decision -> accountable rationale, no trigger
          |
          v
work-order selection -> preflight/CI -> Explorer evidence -> accountable review
```

## Trust boundaries

An agent may draft assessment metadata and an ADR but may not convert its own unreviewed judgment into technical-owner approval. Validators check declared structure and relations, not whether prose concealed a material decision. Protected review remains responsible for challenging false no-ADR assessments.

## Required patterns

- Explicit applicability for every new or changed architecture.
- Controlled triggers that make the assessment reviewable.
- Per-architecture coverage rather than one global ADR presence check.
- One ADR per coherent significant decision, not per requirement.
- Fail closed for missing or contradictory active-chain assessment.
- Advisory-only migration for completed historical architecture with already-valid ADR coverage.

## Prohibited patterns

- Treating an omitted ADR as implicit non-applicability.
- Auto-generating empty or ceremonial ADRs.
- Inferring approval from source code, tests, dashboards, or agent prose.
- Allowing one unrelated ADR to satisfy all selected architectures.
- Rewriting repository-owned historical artifacts during installation or upgrade.

## Quality attributes

Auditability, low ceremony for routine work, fail-closed readiness for material decisions, deterministic diagnostics, compatibility for existing repositories, and clear human accountability.

## Conformance checks

Metadata matrix tests, per-architecture preflight coverage, legacy compatibility fixtures, authoring-template inspection, CI parity, Explorer state/anomaly assertions, security boundary tests, dual-runtime regression, and canonical/self-hosted integrity parity.

## Related ADRs

- `ADR-IAR-001`: Use a thin adapter, one managed router, and modular policy.
- `ADR-IAR-004`: Use explicit conditional ADR applicability rather than unconditional or implicit selection.
