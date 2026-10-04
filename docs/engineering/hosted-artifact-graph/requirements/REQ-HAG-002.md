+++
id = "REQ-HAG-002"
type = "requirement"
title = "Preserve immutable revisions and reproducible baselines"
status = "approved"
owners = ["product-owner", "engineering-owner"]
created = "2026-10-04"
updated = "2026-10-04"
statement = "Every accepted artifact edit creates a new immutable revision, and each baseline resolves an explicit project-scoped revision set and relationships under a named digest scheme."
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

# Preserve immutable revisions and reproducible baselines

## Why

This behavior is needed for the bounded hosted context and draft-authoring outcome in INT-HAG-001.

## Behavior

A mutable draft head selects revisions without overwriting earlier revisions or baseline membership. Revision identity binds body, metadata, declared relation values and provenance. Content and derived declared edges are accepted together. Imported lifecycle information cannot be edited through the draft route.

## Acceptance

Read baseline B before and after two accepted draft edits: the selected revision set, relations, raw content and baseline digest are identical. A changed body, relation target or provenance field changes the new revision digest.

VER-HAG-001 defines independent inputs, expected results and evidence for this obligation.
