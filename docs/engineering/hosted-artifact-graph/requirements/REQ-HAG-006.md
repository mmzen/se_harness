+++
id = "REQ-HAG-006"
type = "requirement"
title = "Expose bounded read operations and Cypher with honest limits"
status = "approved"
owners = ["product-owner", "engineering-owner"]
created = "2026-10-04"
updated = "2026-10-04"
statement = "The service exposes domain reads and constrained Cypher exploration that report project, baseline or explicit live/draft view, provenance and incomplete results, and denies unsupported operations before execution."
verification_method = ["test", "inspection", "demonstration"]
priority = "must"
source = "2026-10-04 hosted artifact graph brief, Sections 3, 8-16, and the subsequent user instruction retaining Cypher while deferring Memgraph-side read-only enforcement."

[relations]
derives_from = ["CAP-HAG-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-04T12:32:03Z"
decided_by = "mmzen"
reason = "mmzen approved the current artifact package in this conversation: \"i approve the artifact package\". This applies to the 16 reviewed governing definitions in the Phase 0 package, whose review manifest SHA-256 is fc1009f1b5fbfc3259f9df4057695500ac7ad3b80777f3107155c629eaea99cc. Complete reviewed file hashes were compared immediately before application. This records definition approval only; WO-HAG-001 approval remains unchanged. The user clarification remains: keep using Cypher, defer Memgraph-side read-only enforcement and retain the open item. RISK-HAG-001 remains raised; this decision does not accept that risk, verify implementation or authorize external delivery."
+++

# Expose bounded read operations and Cypher with honest limits

## Why

This behavior is needed for the bounded hosted context and draft-authoring outcome in INT-HAG-001.

## Behavior

Domain reads include exact revision, work context, comparison, impact, verification lineage and evaluator blockers. MCP exposes those same reads. In accordance with the user instruction of 2026-10-04, retain Cypher and defer database-side read-only enforcement as an unresolved item. The sandbox uses application-side syntax restrictions, limits and rollback defense; none establishes a database authorization boundary.

## Acceptance

Unknown projects, unsupported Cypher clauses/procedures and over-budget traversals are refused or marked incomplete. Every response states the selected view. The qualification report prominently retains the unresolved database enforcement item and makes no authoritative/multi-tenant safety claim.

VER-HAG-001 defines independent inputs, expected results and evidence for this obligation.
