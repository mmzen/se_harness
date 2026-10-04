+++
id = "ARCH-HAG-001"
type = "architecture"
title = "One hosted graph service with an isolated released evaluator"
status = "approved"
owners = ["technical-owner"]
created = "2026-10-04"
updated = "2026-10-04"

[relations]
addresses = ["REQ-HAG-001", "REQ-HAG-002", "REQ-HAG-003", "REQ-HAG-005", "REQ-HAG-006", "REQ-HAG-007", "REQ-HAG-008"]
conforms_to = ["SPEC-HAG-001", "SPEC-HAG-002", "SPEC-HAG-003"]

[decision_assessment]
outcome = "adr_required"
triggers = ["system-boundary", "public-interface-or-protocol", "data-ownership-or-persistence", "security-privacy-or-trust-boundary", "deployment-or-operating-model", "concurrency-consistency-reliability-or-failure-strategy", "technology-framework-vendor-or-external-service"]
rationale = "A hosted persistence and service boundary changes data ownership, protocols, deployment, authorization and concurrency. ADR-HAG-001 records the chosen bounded design for review."
assessed_by = "Codex (draft technical assessment; human approval pending)"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-04T12:32:03Z"
decided_by = "mmzen"
reason = "mmzen approved the current artifact package in this conversation: \"i approve the artifact package\". This applies to the 16 reviewed governing definitions in the Phase 0 package, whose review manifest SHA-256 is fc1009f1b5fbfc3259f9df4057695500ac7ad3b80777f3107155c629eaea99cc. Complete reviewed file hashes were compared immediately before application. This records definition approval only; WO-HAG-001 approval remains unchanged. The user clarification remains: keep using Cypher, defer Memgraph-side read-only enforcement and retain the open item. RISK-HAG-001 remains raised; this decision does not accept that risk, verify implementation or authorize external delivery."
+++

# One hosted graph service with an isolated released evaluator

## Context and scope

One tenant and one disposable project demonstrate remote context and draft authoring. Git remains the authority for this development repository and the source of historical import claims. The hosted graph is authoritative only for its own sandbox draft state. Moving the repository to hosted authority is a separate Phase 3 cutover.

## Components and responsibilities

| Component | Responsibility | State |
| --- | --- | --- |
| Packaged harness client | Explicit remote selection, typed commands, operation keys, readable and JSON results | Connection configuration only; no authoritative cache |
| Plugin guidance | Tell the agent how to select the candidate client separately from the governing evaluator | Versioned packaged instructions |
| Python service | Authentication, command admission, read API, MCP, constrained Cypher and receipt recovery | No independent authoritative store |
| Evaluator adapter | Materialize an exact view and invoke the released evaluator in isolation | Disposable files and bounded subprocesses |
| Memgraph | Immutable content, derived declared edges, baseline membership, draft heads, versions, operation receipts | One durable volume, explicit transaction boundary |
| Pinned source/evidence archive | Preserve historical Git blobs and code/evidence referenced by old records | Read-only, content-addressed inputs; no mutable artifact head |

## Dependency direction

The remote client depends on the versioned command/read contract. The service depends on the graph repository adapter and evaluator adapter. The graph adapter depends on Memgraph's transaction interface. The evaluator stays independent of the service, HTTP and Memgraph. Candidate code cannot govern the checked-out implementation repository. No second copy of lifecycle or decision-right policy is added to the service.

## Data and control flow

For reads, the service authenticates the principal, resolves the explicit view, reads its revisions and edges in a consistent transaction, and returns the view identity with completeness markers. Domain context selection is compared with the released evaluator's existing work-scope behavior. MCP calls the same read handlers.

For writes, the service checks authentication and the operation key, captures the full project version, materializes that selection, and asks the pinned evaluator to parse and assess the candidate draft. A transaction then matches the same project/context/revision guards and writes the new revision, edges, head, version and accepted receipt together. A concurrent project mutation causes refusal. Accepted identical retries return the stored result even when the live version has advanced. These semantics follow SPEC-HAG-002; this architecture adds no new lifecycle transition.

## Trust boundaries

Client content, imported metadata, Cypher and credentials are untrusted inputs. Credentials map to sandbox roles on the server. The server supplies identity; request bodies cannot grant rights. Imported approval and verification fields remain historical claims. Phase 2 refuses new lifecycle/decision/evidence-record mutations instead of presenting test authentication as human approval enforcement.

The evaluator subprocess receives fixed arguments and bounded regular files in a disposable directory. It receives no executable import content, arbitrary URLs or caller-selected shell commands. The source resolver permits only the pinned source/evidence archive and preserves original relative paths.

Cypher remains enabled for the requested sandbox. Application syntax restrictions, explicit view binding, resource limits and rollback reduce accidental writes but are not Memgraph-side read-only authorization. That unresolved boundary is tracked as a raised risk and must be resolved before an authoritative pilot or untrusted network exposure.

## Required patterns and exclusions

Use immutable revision content, named digest schemes, explicit views, atomic receipts and a project-wide version guard. Use one synchronous process and one store. Refuse unsupported combinations and missing evidence. Do not add a queue, event bus, enrichment pipeline, UI, parallel policy engine, background synchronization or local-file fallback.

## Quality and conformance

The small project-wide guard intentionally trades concurrent throughput for simpler stale-input protection. Full materialization trades CPU and temporary disk use for evaluator reuse and historical path fidelity. Bounds and qualification measurements are in SPEC-HAG-002 and VER-HAG-001. The service may not claim power-loss durability from a successful process restart. ADR-HAG-001 records this coherent design decision.
