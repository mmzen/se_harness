+++
id = "ADR-HAG-001"
type = "adr"
title = "Python command service over Memgraph with released evaluator materialization"
status = "approved"
owners = ["technical-owner"]
created = "2026-10-04"
updated = "2026-10-04"

[relations]
decides = ["ARCH-HAG-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-04T12:32:03Z"
decided_by = "mmzen"
reason = "mmzen approved the current artifact package in this conversation: \"i approve the artifact package\". This applies to the 16 reviewed governing definitions in the Phase 0 package, whose review manifest SHA-256 is fc1009f1b5fbfc3259f9df4057695500ac7ad3b80777f3107155c629eaea99cc. Complete reviewed file hashes were compared immediately before application. This records definition approval only; WO-HAG-001 approval remains unchanged. The user clarification remains: keep using Cypher, defer Memgraph-side read-only enforcement and retain the open item. RISK-HAG-001 remains raised; this decision does not accept that risk, verify implementation or authorize external delivery."
+++

# Python command service over Memgraph with released evaluator materialization

## Status and decision

Draft design decision awaiting definition approval. Use a Python service, one Memgraph store, synchronous commands, explicit draft contexts and a conservative project-wide optimistic guard. Invoke the explicitly selected released Python evaluator over disposable materialized views. Keep Cypher within the sandbox restrictions and record database-side read-only enforcement as unresolved.

## Context and drivers

The current evaluator reads TOML-front-matter files, resolves typed relations and work scopes, checks lifecycle and integrity, and binds historical evidence to original paths and scoped code bytes. Its existing released mutation boundary also prevents candidate source from governing its own implementation. The first outcome needs these semantics without an evaluator rewrite. There is no measured native-server throughput requirement for the bounded POC.

## Considered options

| Option | Consequences |
| --- | --- |
| Python service plus released evaluator materialization — selected | Reuses existing runtime, contracts and diagnostic JSON. Adds temporary filesystem work and subprocess cost, but keeps policy outside candidate service code. One service remains easy to package and inspect. |
| Rust service calling the same Python evaluator | Can offer native transport/concurrency tooling, but still needs the evaluator runtime and materialization; adds a language, build and protocol boundary without an established Phase 2 benefit. Revisit only with measured need. |
| Rewrite the evaluator around a direct graph storage interface | Could remove materialization later, but changes a trusted policy boundary, historical path/digest behavior and public evaluator contracts. It is outside this bounded POC. |
| File projection with read-only graph and local draft edits | Simpler read prototype but cannot establish hosted atomic authoring, operation recovery or server-side stale-context refusal. It fails the agreed first-work-package outcome. |

## Why this amount of complexity

An immutable revision store and accepted-operation receipts are needed to reproduce baseline reads and recover a committed command after a lost response. The single project guard covers all governing dependency changes without inventing a fine-grained dependency protocol. A second authoritative database, event log or workflow engine is unnecessary at the declared scale. Separate immutable source/evidence inputs are required for old code/path digests and do not become a second mutable artifact store.

## Consequences

- The server and client need an explicit versioned API and actual packaged combination manifest. Evaluator identity is separate from the candidate client identity.
- Serialization, import fidelity and graph transactions receive independent boundary tests. Parsing a request successfully does not authorize it.
- Project-wide conflicts may refuse unrelated concurrent edits. The client must re-read and deliberately resubmit; no automatic rebasing.
- Service authentication is sufficient only for the sandbox's limited draft operations. Authenticated human decisions and database read-only enforcement remain Phase 3 prerequisites.
- The materialization adapter may prove unable to express lifecycle-specific incomplete-draft validation with the existing release. If so, stop and propose the smallest evaluator contract change; do not suppress findings or recreate policy.
- Git-to-server authority cutover, production failure recovery and public release remain later separately authorized work.

## Validation

VER-HAG-001 checks the actual packaged path, independently fixed context membership, legacy hashes, concurrent writers, operation recovery and baseline immutability. A architecture review traces all command handlers to one admission and transaction path and all domain/MCP reads to one view-resolution path. Qualification must state the cost and unresolved Cypher boundary honestly.
