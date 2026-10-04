+++
id = "REQ-HAG-003"
type = "requirement"
title = "Return the exact selected work context"
status = "approved"
owners = ["product-owner", "engineering-owner"]
created = "2026-10-04"
updated = "2026-10-04"
statement = "Given a work order and explicit baseline or draft context, the service returns the selected governing definitions, declared scope, relevant decisions and evaluator findings with exact selection and completeness identities."
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

# Return the exact selected work context

## Why

This behavior is needed for the bounded hosted context and draft-authoring outcome in INT-HAG-001.

## Behavior

Use the released evaluator selection behavior as the comparison oracle, including architecture, verification and dependency classifications. Keep structural scope separate from derived findings. Impact results state that they cover declared traceability only. Do not report an absent dependency when traversal or content has been truncated.

## Acceptance

The reference WO-RLS-038 context at the pinned source commit matches the governing IDs, declared paths and meaningful findings in SPEC-HAG-001. Unknown baselines, missing references and intentionally bounded responses have distinct explicit results.

VER-HAG-001 defines independent inputs, expected results and evidence for this obligation.
