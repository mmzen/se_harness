+++
id = "ARCH-IAR-008"
type = "architecture"
title = "Read-only inspection projection over the existing graph snapshot"
status = "implemented"
owners = ["technical-owner", "engineering-owner", "quality-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
addresses = ["REQ-IAR-016"]
conforms_to = ["SPEC-IAR-008"]

[decision_assessment]
outcome = "adr_required"
triggers = ["responsibility-or-dependency-direction", "public-interface-or-protocol", "cross-cutting-policy", "material-alternatives"]
rationale = "The command introduces public human and JSON interfaces and must choose whether inspection owns rules or depends on the existing validator and Explorer projection. That responsibility boundary affects every future inspection capability and has material alternatives."
assessed_by = "technical-owner"
+++

# Architecture: Read-only inspection projection over the existing graph snapshot

## Lifecycle

Approved on 2026-08-15 through the repository owner's instruction `go for implementation`; the accountable technical decision is recorded by `ADR-IAR-008`.

## Context and scope

The validator owns formal graph and governance diagnostics. The Explorer generator already reuses that validator and adds deterministic derived findings such as missing evidence, inactive governing references, stale dependencies, cycles, unlinked artifacts, duplicate relations, and revision observations. Inspection needs a terminal projection of those facts, not a third rule engine.

## Components and responsibilities

- **CLI adapter:** adds `inspect`, resolves the target, and invokes the installed repository script through the existing bounded launcher.
- **Inspection script:** requests one snapshot and constructs deterministic queues and renderers without adding findings.
- **Validator:** remains the owner of formal validity, diagnostic severity, codes, planes, and gate behavior.
- **Explorer snapshot projection:** remains the owner of normalized artifacts, relations, revision context, and derived finding rules.
- **Human renderer:** provides a compact operational view with explicit derived authority.
- **JSON renderer:** provides the versioned inspection contract for agents and future tooling.
- **Managed distribution:** keeps candidate, canonical template, package data, documentation, and schema-2 lock expectations aligned.

## Data and control flow

```text
harnessctl inspect TARGET
        |
        v
repository-local inspect_engineering_artifacts.py
        |
        v
generate_snapshot
    |-> validate_repository -> diagnostics + assessment planes
    `-> Explorer projection -> artifacts + relations + existing findings
        |
        v
mechanical lifecycle queues + deterministic summary
        |-> human report
        `-> se-harness-inspection-v1 JSON
```

## Dependency and authority direction

Inspection depends on the existing validator and Explorer snapshot. Neither depends on inspection. Inspection may select, group, count, and render existing facts; it may not reinterpret validity, alter severity, mint finding rule IDs, transition lifecycle state, or become release evidence by itself.

Because the script comes from the inspected repository, the report explicitly identifies `producer = "repository-local"`. This makes its development-feedback role honest but does not resolve the separately tracked independent-evaluator boundary.

## Trust and failure boundaries

- Treat every repository-derived string as data; render it without terminal escape effects or code execution.
- Resolve the target and repository scripts using the existing path-safety boundary.
- Write nothing, including dashboard output or caches.
- Preserve partial observations when formal validation fails, provided the existing snapshot can be built safely.
- Fail with a concise operational error when the snapshot cannot be produced; do not manufacture an empty healthy report.

## Conformance checks

Architecture tests prove the dependency direction, absence of duplicate finding constants, deterministic rendering, no-write behavior, CLI/package parity, and unchanged validator and dashboard behavior.

## Related ADR

`ADR-IAR-008` decides that the first inspection command is a projection over existing evidence rather than a new rule authority.
