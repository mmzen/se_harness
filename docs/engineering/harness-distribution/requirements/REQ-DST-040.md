+++
id = "REQ-DST-040"
type = "requirement"
title = "Present focused lineage as a structured artifact board"
status = "approved"
owners = ["product-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"
statement = "WHEN a reader opens focused Lineage for an artifact, THE SYSTEM SHALL present its bounded relationship context in a deterministic stage-and-type board that preserves exact artifact identity, lifecycle state, relation direction, and relation authority without implying a new formal lifecycle."
verification_method = "automated-test-and-manual-review"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Present focused lineage as a structured artifact board

## Rationale

The current free-positioned Lineage graph ranks cards from inbound to outbound relations. It becomes difficult to scan when different artifact types, reverse relations, same-stage relations, and cycles share the view. Because selecting a card immediately lays out another neighborhood, the reader must repeatedly reconstruct both the model and the path that led there.

A structured board can make the current model legible without replacing it. Conceptual stage groups and exact artifact-type sublanes provide stable visual coordinates, while directed relation connectors and the existing detail view remain the authority for what the graph actually declares.

## Preconditions and trigger

This requirement applies when Harness Explorer has a valid normalized snapshot and renders the focused Lineage view for a selected formal artifact.

## Required response

- Replace the free-positioned Lineage canvas with a deterministic artifact board organized into these conceptual stage groups and exact-type sublanes:
  - `Purpose`: `intent`, `capability`;
  - `Definition`: `requirement`, `specification`;
  - `Design`: `architecture`, `adr`;
  - `Delivery`: `work_order`;
  - `Assurance`: `verification`, `verification_record`;
  - `Release and operation`: `release_contract`, `release_record`, `operating_contract`.
- Label the groups as a presentation aid. Their order must not redefine the formal schema, require every artifact type, imply that every relation is left-to-right, or establish release eligibility.
- Give unknown future artifact types a deterministic `Other` sublane and retain their exact type labels.
- Show the selected artifact plus every resolved direct neighbor. Provide optional depth-two context, adding no more than 100 distinct non-direct artifacts in deterministic breadth-first order and reporting any truncation explicitly.
- Keep every visible card's exact ID, human title or description, exact artifact type, and lifecycle status readable. Selected, direct, and second-level context must remain distinguishable without color alone.
- Preserve each visible relation's recorded source, direction, relation name, authority, and declared-versus-derived distinction. Direct relations to the selected artifact receive primary emphasis; other visible relations may be de-emphasized to reduce clutter but must remain inspectable.
- Keep unresolved direct relations visible through an explicit summary and the authoritative Relations detail. Do not fabricate a formal artifact card for a missing target.
- Keep complete artifact detail, evidence, and relation-list routes available below the board.
- Use stable stage, type, artifact-ID, and relation ordering so the same snapshot, selected artifact, and depth produce the same board structure.

## Failure and boundary behavior

If no artifact can be selected, render a bounded empty state rather than an incomplete board. Cycles, self-relations, duplicate paths, reverse-stage relations, same-stage relations, unknown types, missing targets, and dense direct neighborhoods must terminate safely and remain explainable.

If the optional CDN-backed Overview topology fails, the Lineage board must remain usable because it consumes only the embedded canonical snapshot and local presentation code.

## Constraints

- Preserve `harness-dashboard-snapshot-v1`; no new persisted UI model or generator field is authorized.
- Preserve canonical artifact-type strings, lifecycle states, relation names, relation direction, and authority.
- Evidence and commit provenance remain detail data, not invented formal-artifact lanes.
- Preserve safe inert rendering, bounded iterative traversal, keyboard use, responsive access, managed-template parity, and the current non-authoritative presentation boundary.
- Do not add a runtime dependency, network request, storage mechanism, telemetry, schema change, validator rule, or governance transition.
- Do not change the Overview 3D topology under this requirement.

## Acceptance examples

### Example: mixed formal lineage

**Given** a requirement is connected to intent, capability, specification, architecture, work, and verification artifacts,

**When** the reader opens its focused Lineage,

**Then** the cards occupy their stable conceptual groups and exact-type sublanes while the connectors retain the recorded directions and relation names.

### Example: relation against visual order

**Given** a formal relation points from a visually later group to an earlier group,

**When** the board renders,

**Then** it preserves that direction and does not reverse the relation to make the board appear sequential.

### Example: dense second-level context

**Given** depth two reaches more than 100 non-direct artifacts,

**When** the board expands,

**Then** the selected artifact and all direct neighbors remain visible, exactly the deterministic first 100 non-direct artifacts are added, and the omitted context is reported as truncated.

## Open decisions

None when approved.
