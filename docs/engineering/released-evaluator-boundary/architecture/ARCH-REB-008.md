+++
id = "ARCH-REB-008"
type = "architecture"
title = "Contract-indexed lifecycle policy boundary"
status = "approved"
owners = ["technical-owner", "security-owner", "quality-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[relations]
addresses = ["REQ-REB-018", "REQ-REB-019"]
conforms_to = ["SPEC-REB-009"]

[decision_assessment]
outcome = "adr_required"
triggers = ["responsibility-or-dependency-direction", "public-interface-or-protocol", "cross-cutting-policy", "concurrency-consistency-reliability-or-failure-strategy", "difficult-to-reverse", "material-alternatives"]
rationale = "The change advances the public workflow-contract schema, reverses dependency direction from code constants to contract data across package and standalone consumers, and centralizes cross-cutting authority and version-reservation semantics. The alternatives materially affect the released-evaluator boundary and require ADR-REB-008."
assessed_by = "technical-owner"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T10:01:59Z"
decided_by = "technical-owner"
+++

# Architecture: Contract-indexed lifecycle policy boundary

## Context

The transition engine and standalone validator execute in different runtime roles. Package code can import `se_harness`, while a managed root validator must remain independently executable under its locked released evaluator. Sharing Python constants across that boundary would make candidate code part of predecessor authority. Duplicating constants caused the drift this packet is intended to prevent.

## Components

- **Canonical workflow v3 document:** owns lifecycle families, state rows, transitions, authority, version reservation, terminality, visibility, and predecessor-adapter markers.
- **Strict package contract loader:** validates the complete document and exposes immutable indexes to package consumers.
- **Transition consumer:** plans only edges returned by the index and evaluates VREC/RLS authority through state semantics.
- **Provenance consumer:** checks release-version availability through `reserves_version` and keeps distinct non-lifecycle completion rules explicit.
- **Standalone managed validator loader:** independently parses the adjacent installed contract and derives equivalent indexes without importing candidate package code.
- **Validator and presentation consumers:** validate type vocabularies, lifecycle events, same-version uniqueness, and active/history display from derived indexes.
- **Conformance suite:** proves source/installed/package byte parity and semantic agreement for every family/state/property and adversarial contract.

## Approved compatibility amendment

The registry includes seven terminal compatibility rows discovered by complete
repository qualification: five for definitions and two for work orders. They
are data-model inputs to the same strict indexes, not a compatibility branch in
consumer code. No component receives another transition path or predecessor
runtime dependency.

## Dependency direction

```text
authoritative workflow-v3 lifecycle registry
            |                    |
            v                    v
package strict indexer     standalone strict indexer
     |          |                 |
     v          v                 v
transition   provenance     graph validation
 planning    preparation    + dashboard/inspection

released predecessor ---- explicit adapter boundary ---- successor-only state
```

No arrow points from the standalone predecessor evaluator into candidate package code. The two physical JSON copies are distribution surfaces protected by byte-parity and managed-integrity checks, not independent policy sources.

## Trust and failure boundaries

- Contract bytes are untrusted until size, encoding, duplicate-key, schema, exact-field, type, reference, and cross-field checks pass.
- Index construction is all-or-nothing and deterministic. A consumer receives a complete immutable index or a stable error.
- A rejected state has no outgoing edge and no authority/version-reservation effect. Consumer code cannot override those facts with caller input.
- Repository artifact content remains untrusted. Contract semantics do not waive rejection metadata, relation, provenance, or candidate-identity checks.
- The root evaluator, managed root files, credentials, Git refs, release records, tags, and external services are outside the implementation boundary.

## Operational consequences

The contract schema changes from v2 to v3, so candidate source/package checks, installation parity, and the issue #101 migration rehearsal must cover it. Existing repositories do not receive the contract until a separately approved evaluator upgrade. The current exact 0.5-to-0.6 compatibility view remains a predecessor adapter, not an alternate lifecycle source.
