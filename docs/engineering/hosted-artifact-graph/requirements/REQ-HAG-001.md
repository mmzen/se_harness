+++
id = "REQ-HAG-001"
type = "requirement"
title = "Import complete artifacts without changing historical claims"
status = "approved"
owners = ["product-owner", "engineering-owner"]
created = "2026-10-04"
updated = "2026-10-04"
statement = "For an explicitly identified Git snapshot, the importer preserves complete artifact content, declared relations and original provenance and reports duplicate or unresolved identities without silently repairing or approving them."
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

# Import complete artifacts without changing historical claims

## Why

This behavior is needed for the bounded hosted context and draft-authoring outcome in INT-HAG-001.

## Behavior

Read full Git blobs and record repository, object format, commit, original path and raw SHA-256. Parse identity and relations with the selected evaluator. Retain raw bytes as well as their normalized reading form. Import membership is explicit; external dependencies are resolved through the pinned snapshot. Explorer output is not an import format.

## Acceptance

Repeated import of the same snapshot returns the same baseline and report; altered bytes under the same provenance identity are refused. Duplicate IDs and unresolved relations appear in the deterministic report and prevent declaring a complete imported baseline.

VER-HAG-001 defines independent inputs, expected results and evidence for this obligation.
