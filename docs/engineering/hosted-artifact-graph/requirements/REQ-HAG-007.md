+++
id = "REQ-HAG-007"
type = "requirement"
title = "Reuse explicit evaluator and historical evidence semantics"
status = "approved"
owners = ["product-owner", "engineering-owner"]
created = "2026-10-04"
updated = "2026-10-04"
statement = "The server independently evaluates each accepted draft command with its explicitly selected released evaluator and preserves legacy code, path/content snapshot and evidence bindings without treating local success as mutation authority."
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

# Reuse explicit evaluator and historical evidence semantics

## Why

This behavior is needed for the bounded hosted context and draft-authoring outcome in INT-HAG-001.

## Behavior

A disposable materialization adapter preserves original paths and required pinned code/evidence inputs for the unchanged evaluator. Cache/projection files are replaceable and not a second authoritative store. New remote baseline digests have a different named scheme. Historical records keep the original digests. Missing evidence is unavailable, not valid. This POC does not introduce remote VREC/RLS preparation or authenticated human decisions.

## Acceptance

Server tampering with evaluator selection, an unsupported payload or a stale policy identity fails before commit. Legacy snapshots recompute with original paths and scoped code inputs. The remote baseline digest cannot satisfy a legacy snapshot field. A local validated request still fails when server-side state or rights differ.

VER-HAG-001 defines independent inputs, expected results and evidence for this obligation.
