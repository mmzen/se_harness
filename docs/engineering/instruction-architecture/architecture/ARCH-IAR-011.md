+++
id = "ARCH-IAR-011"
type = "architecture"
title = "Separate owner instructions, released guidance and evaluator authority"
status = "approved"
owners = ["repository-owner", "technical-owner"]
created = "2026-09-20"
updated = "2026-09-27"

[decision_assessment]
outcome = "adr_required"
triggers = ["responsibility-or-dependency-direction", "security-privacy-or-trust-boundary", "cross-cutting-policy"]
rationale = "Harness entry moves outside owner AGENTS, release discovery spans evaluator and host boundaries, and instruction ownership changes."
assessed_by = "Codex drafting agent; assessment proposed for technical-owner review"

[relations]
addresses = ["REQ-IAR-022", "REQ-IAR-024", "REQ-IAR-025", "REQ-IAR-026"]
conforms_to = ["SPEC-IAR-014"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-27T07:37:39Z"
decided_by = "technical-owner"
reason = "User instruction: so let's start the work orders. Apply the reviewed package under DEC-IAR-001 versioned-successor; selected 0.18.0 governance remains installed until separate release/adoption."
+++

# Separate owner instructions, released guidance and evaluator authority

## Components and responsibilities

| Component | Responsibility |
| --- | --- |
| Released evaluator | Identity, lifecycle legality, gates, selected formal graph and typed next action. |
| Released entry and procedure collection | Always-applicable rules and precise agent actions. |
| Discovery mapping | Resolve returned procedure/step identifiers to reading destinations. |
| Host adapter | Deliver the correct root on startup/compaction and disclose unsupported delivery. |
| Installer | Publish the versioned collection and safely retire recognized fragments. |
| Repository owner | Maintain AGENTS.md and approve separate owner edits and adoption. |

## Dependency direction

Host adapter → repository-selected entry → current procedure → required references.
Current procedure → released evaluator → machine policy and selected formal graph.
Discovery consumes the evaluator's selected action; it never returns authority
to the evaluator from agent prose. The host adapter does not implement a lifecycle.

## Trust and ownership

Repository paths, lock data and host context are untrusted inputs. Resolve paths
within the selected root and reject ambiguous identity before claiming readiness.
The released entry, required harness instructions and discovery mapping have
explicit integrity ownership. AGENTS.md has none of that ownership. A recognized
legacy fragment may be retired; arbitrary adjacent prose cannot be deleted.
Existing editable guides may contain owner changes and require an explicit
conflict plan before replacement. No real host installation occurs in this work.

## Migration and complexity

The current plugin explicitly has no automatic hooks. Native delivery must be
implemented and observed, not inferred from a skill. A shared content collection
plus thin host adapters avoids duplicating instruction logic. It adds a mapping
and migration tests; that cost serves the agreed context and ownership goals.
No new service, remote index, background agent or general retrieval engine is needed.

## Conformance

VER-IAR-014 checks route completeness, authority invariance, migration preservation
and observed host delivery. ADR-IAR-011 records the coherent architecture choice.
The recorded assessment is the drafting agent's assessment, pending human review.
