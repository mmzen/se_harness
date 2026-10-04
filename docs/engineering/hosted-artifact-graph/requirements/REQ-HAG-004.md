+++
id = "REQ-HAG-004"
type = "requirement"
title = "Create and revise legitimate incomplete drafts"
status = "approved"
owners = ["product-owner", "engineering-owner"]
created = "2026-10-04"
updated = "2026-10-04"
statement = "An authenticated sandbox author can create and revise a draft through harnessctl under lifecycle-specific validation while malformed commands, invalid identities, prohibited relationships and protected-state changes are refused."
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

# Create and revise legitimate incomplete drafts

## Why

This behavior is needed for the bounded hosted context and draft-authoring outcome in INT-HAG-001.

## Behavior

A generated incomplete template is a legitimate saved draft. Distinguish unfinished authoring from malformed TOML, duplicate metadata, type/ID disagreement and forbidden relation pairs. Draft edits cannot alter an imported approved artifact in place, insert lifecycle events, impersonate an actor or fabricate verification/release records.

## Acceptance

Save an incomplete requirement draft, then revise its body and a valid derives_from relation. A requirement-to-release-record derives_from relation is refused atomically; the unfilled template alone is not the invalid test.

VER-HAG-001 defines independent inputs, expected results and evidence for this obligation.
