+++
id = "REQ-HAG-005"
type = "requirement"
title = "Commit changes and retries atomically under a version guard"
status = "approved"
owners = ["product-owner", "engineering-owner"]
created = "2026-10-04"
updated = "2026-10-04"
statement = "An accepted command commits its revision, declared edges, draft-head update, operation receipt and concurrency version in one transaction, rejecting stale governing context and mismatched reuse of an operation key."
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

# Commit changes and retries atomically under a version guard

## Why

This behavior is needed for the bounded hosted context and draft-authoring outcome in INT-HAG-001.

## Behavior

Use a conservative project-wide version guard, plus the expected context/revision, to invalidate prepared commands when any project input changes. A replay of an accepted identical request returns its original result before testing the now-old expected version. Scope operation keys to project and authenticated principal and bind the full semantic request.

## Acceptance

Two writers starting at version N cannot both accept a different revision at N. A dependency edit makes the pending request stale even if its target did not change. A response lost after commit is recovered once; key reuse with changed body or baseline is refused. Fault before commit leaves no partial result.

VER-HAG-001 defines independent inputs, expected results and evidence for this obligation.
