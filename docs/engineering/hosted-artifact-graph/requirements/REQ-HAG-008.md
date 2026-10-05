+++
id = "REQ-HAG-008"
type = "requirement"
title = "Qualify one reproducible packaged sandbox combination"
status = "approved"
owners = ["product-owner", "engineering-owner"]
created = "2026-10-04"
updated = "2026-10-04"
statement = "The first hosted work package provides a reproducible Docker deployment and demonstrates the twelve-step walkthrough using the actual packaged harness client, plugin guidance and server image with explicit database, schema and evaluator identities."
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

# Qualify one reproducible packaged sandbox combination

## Why

This behavior is needed for the bounded hosted context and draft-authoring outcome in INT-HAG-001.

## Behavior

One local service and one persistent Memgraph instance form the sandbox. Startup reports supported component identities and fails closed on an incompatible schema without migrating it. Initialization/migration is explicit. Candidate manifests distinguish qualification, release, publication, installation and deployment, retaining the original identity of reused components. Subsequent release/deployment tooling and pilot authority require later work.

## Acceptance

Run the walkthrough on the declared Linux Docker platform, retain component and image digests, restart the containers and recover an identical baseline and accepted receipt. An unsupported client/API/evaluator/schema tuple is rejected before mutation. The report states deferred Cypher enforcement and the unperformed Phase 3/4 obligations.

VER-HAG-001 defines independent inputs, expected results and evidence for this obligation.
