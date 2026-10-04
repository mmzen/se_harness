+++
id = "INT-HAG-001"
type = "intent"
title = "Retrieve engineering context and revise drafts against an immutable hosted baseline"
status = "approved"
owners = ["product-owner"]
created = "2026-10-04"
updated = "2026-10-04"
outcome = "An agent reads the expected context for WO-X at baseline B, submits a valid draft revision through harnessctl, recovers correct refusal and retry results, and retrieves B unchanged."

[relations]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-04T12:32:03Z"
decided_by = "mmzen"
reason = "mmzen approved the current artifact package in this conversation: \"i approve the artifact package\". This applies to the 16 reviewed governing definitions in the Phase 0 package, whose review manifest SHA-256 is fc1009f1b5fbfc3259f9df4057695500ac7ad3b80777f3107155c629eaea99cc. Complete reviewed file hashes were compared immediately before application. This records definition approval only; WO-HAG-001 approval remains unchanged. The user clarification remains: keep using Cypher, defer Memgraph-side read-only enforcement and retain the open item. RISK-HAG-001 remains raised; this decision does not accept that risk, verify implementation or authorize external delivery."
+++

# Retrieve engineering context and revise drafts against an immutable hosted baseline

## In plain words

An agent can retrieve the engineering context for a selected work order from a hosted graph and submit a draft revision through the harness while the baseline it read remains reproducible. A baseline is an immutable selection of artifact revisions; a draft context is a named set of proposed revisions based on that selection.

## Problem

Current artifacts are files in the software repository. Collaboration and context retrieval are tied to filesystem snapshots. The requested hosted model needs explicit revisions, consistent graph reads and server-checked draft changes without losing historical approval, code or evidence bindings.

The source review is anchored to commit 82f5a0ed7438a73da8f03aee23ad02a9b8cc09e1. The 2026-10-04 user brief supplies the outcome, one-service/one-store constraints and Phase 2 completion statement. The later user instruction retains Cypher and defers database-side read-only enforcement as an open item.

## Success measures

| Measure | Today | When reached | Observed |
| --- | --- | --- | --- |
| Pilot author can recover the exact context used before an edit | Hosted route unavailable | Every supported context request resolves its explicit baseline after subsequent draft edits | Author compares baseline identities during each sandbox work session |
| Author can recover a committed submission after a lost response | Hosted route unavailable | Retry returns the original accepted result | Author uses the operation receipt during sandbox recovery |

VER-HAG-001 contains acceptance tests. This draft makes no operating service claim.

## Scope

One repository contains the harness, plugin and new Python service. One tenant and one disposable project use Memgraph, synchronous commands and Docker. The first implementation ends with the complete twelve-step Phase 2 read/author/check walkthrough. Phases 3 and 4 require later work, authenticated decision enforcement, operational qualification and explicit authority cutover.

## Not this

- Repository adoption of remote authority or a production deployment.
- A second authoritative store, bidirectional synchronization, queues or a workflow engine.
- A replacement evaluator, remote shell, build service or hosted autonomous agent.
- Enterprise account administration, general draft merging, enrichment or a web authoring console.
- Publication, plugin installation, release acceptance or changes to historical evidence.
