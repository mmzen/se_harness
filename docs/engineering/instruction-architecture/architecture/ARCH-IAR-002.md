+++
id = "ARCH-IAR-002"
type = "architecture"
title = "Responsibility-separated managed instruction layers"
status = "implemented"
owners = ["technical-owner", "engineering-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
constrains = ["REQ-IAR-010"]
+++

# Architecture: Responsibility-separated managed instruction layers

## Context and scope

The established instruction architecture uses a thin agent gate, one managed router, and focused policy modules. This refinement defines the boundary between the router's compact non-waivable contract and the detailed procedure owned by those modules.

## Components and responsibilities

- **`AGENTS.md` managed gate:** discovers exactly one harness router.
- **`ENGINEERING_HARNESS.md`:** states authority and safety invariants, selects the applicable policy, and defines stop conditions.
- **`WORKFLOW.md`:** owns ordered lifecycle and command procedure.
- **`DECISION_RIGHTS.md`:** owns accountable human and automation authority boundaries.
- **`QUALITY_GATES.md`:** owns evidence required at each gate.
- **`TRACEABILITY.md`:** owns record binding, coverage, relations, and provenance semantics.
- **Installer and lock:** distribute the fully managed files and detect drift without interpreting their prose.

## Dependency direction

The agent gate depends on the router. The router depends on focused policies by direct reference. Focused policies do not depend on duplicated router prose for completeness. Owner-controlled indexes may aid discovery but are outside the normative dependency path.

## Data and control flow

```text
agent gate -> managed router -> select focused policy
                              |-> WORKFLOW: ordered procedure
                              |-> DECISION_RIGHTS: authority
                              |-> QUALITY_GATES: evidence gates
                              +-> TRACEABILITY: provenance semantics
```

## Trust boundaries

Concise wording does not make prose an approval or enforcement mechanism. Managed integrity proves installed content identity, preflight proves structural readiness, checks provide evidence, and accountable actors retain decision rights.

## Required patterns

- **Summary-route-detail:** the router summarizes stable invariants, routes by decision point, and leaves change-prone ordered detail to the focused owner.
- **Semantic preservation:** responsibility moves only when all necessary invariants remain accessible through the managed route.
- **Canonical propagation:** canonical template changes reach self-hosted and target repositories through the supported installer and integrity model.

## Prohibited patterns

- Repeating an ordered lifecycle procedure in both router and workflow.
- Removing authority or provenance constraints merely to reduce word count.
- Merging focused policy bodies into the router.
- Making an owner-controlled file the only route to managed policy.
- Hand-editing the self-hosted managed digest.

## Quality attributes

Maintainability through one procedural owner; usability through a compact entry contract; integrity through managed parity; compatibility through the existing transactional upgrade rules; and auditability through explicit responsibility and tests.

## Conformance checks

- Inspect the router and focused modules against their responsibility table.
- Assert the concise section contains all required invariants and omits duplicated command sequencing.
- Verify canonical template, fresh-install output, upgraded output, self-hosted copy, and lock agree.
- Run managed integrity, preflight, artifact validation, deterministic dashboard generation, and full regression tests.

## Related ADRs

- `ADR-IAR-001`: Use a thin adapter, one managed router, and modular policy.
- `ADR-IAR-002`: Keep invariant summaries in the router and procedure in focused policy.
