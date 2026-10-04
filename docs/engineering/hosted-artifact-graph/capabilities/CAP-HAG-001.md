+++
id = "CAP-HAG-001"
type = "capability"
title = "Read a hosted work context and safely author sandbox drafts"
status = "approved"
owners = ["product-owner"]
created = "2026-10-04"
updated = "2026-10-04"
ability = "A sandbox author retrieves a work context at an explicit baseline and creates or revises a draft through the harness with recoverable, server-checked results."

[relations]
derives_from = ["INT-HAG-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-04T12:32:03Z"
decided_by = "mmzen"
reason = "mmzen approved the current artifact package in this conversation: \"i approve the artifact package\". This applies to the 16 reviewed governing definitions in the Phase 0 package, whose review manifest SHA-256 is fc1009f1b5fbfc3259f9df4057695500ac7ad3b80777f3107155c629eaea99cc. Complete reviewed file hashes were compared immediately before application. This records definition approval only; WO-HAG-001 approval remains unchanged. The user clarification remains: keep using Cypher, defer Memgraph-side read-only enforcement and retain the open item. RISK-HAG-001 remains raised; this decision does not accept that risk, verify implementation or authorize external delivery."
+++

# Read a hosted work context and safely author sandbox drafts

## Ability

An authorized sandbox author selects an explicit project and baseline, retrieves the governing work context, opens a draft context, and creates or revises draft artifacts through harnessctl. The author can inspect refusals, compare states and recover an accepted operation without duplicating it. An operator can reproduce the packaged local deployment and reconstruct the selected baseline.

## Conditions and limits

The selected baseline, context version, evaluator and actual component identities accompany results. The sandbox accepts no new human approval, verification or release decisions. Imported decisions remain historical claims. Cypher exploration remains available under the bounded application contract; database-side read-only enforcement is an unresolved item and authoritative pilot use is excluded.
