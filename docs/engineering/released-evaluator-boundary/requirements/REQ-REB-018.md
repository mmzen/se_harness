+++
id = "REQ-REB-018"
type = "requirement"
title = "Use one authoritative lifecycle state registry"
status = "approved"
owners = ["requirements-steward", "repository-owner", "quality-owner"]
created = "2026-08-23"
updated = "2026-08-23"
statement = "THE SYSTEM SHALL derive each formal artifact family's admissible states, permitted transitions, authority effect, version-reservation effect, transitionability, visibility obligation, and predecessor-adapter requirement from one versioned machine-readable lifecycle state registry."
verification_method = "automated-contract-consumer-conformance"

[relations]
derives_from = ["CAP-REB-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T10:01:59Z"
decided_by = "requirements-steward"
+++

# Requirement: Use one authoritative lifecycle state registry

## Rationale

Issue #103 and RCA root cause `RC-060-03` identify a drift risk between the machine workflow contract, the transition planner, and the engineering-graph validator. During release 0.6.0, transition policy already permitted rejection, while the released 0.5 validator still used record-type status sets that did not admit rejected VREC or RLS history. Candidate 0.6 corrected the immediate validation behavior, but its transition and validation consumers still encode parts of the lifecycle model independently.

A status is not just a word. It determines whether an artifact is valid for its type, whether another transition is possible, whether the artifact grants authority, whether an RLS reserves a version, whether history must remain visible, and whether an older evaluator needs an explicit adapter. Those facts must change together through one reviewed contract.

## Required response

- Publish one versioned machine-readable registry covering the `definition`, `work_order`, `verification_record`, and `release_record` lifecycle families.
- Give every admitted state exactly one record containing its permitted targets and semantic flags for authority, version reservation, transitionability, visibility, and predecessor-adapter need.
- Make transition planning derive its edges from that registry rather than a separately maintained transition map.
- Make the standalone engineering validator derive global and per-record-type state vocabularies from the same managed contract bytes.
- Make every same-version release check, including release preparation and complete-graph validation, use the registry's version-reservation flag.
- Reject malformed, incomplete, ambiguous, internally inconsistent, or unknown lifecycle definitions before planning, validation, preparation, or mutation.
- Keep packaged `se_harness/workflow_contract.json` and the installed managed `docs/engineering/WORKFLOW.json` byte-identical and conformance-tested.

## Approved compatibility amendment

Repository qualification found that the existing validator deliberately admits
terminal compatibility states which the initial matrix omitted. The registry
therefore also records definition `ready`, `in_progress`, `verified`,
`released`, and `superseded`, plus work-order `ready` and `superseded`. None has
a new outgoing edge. Their authority flags preserve the already shipped active
coverage rule: definition `in_progress`, `verified`, and `released` grant
authority; both `ready` and `superseded` states do not. All seven rows are
non-version-reserving, terminal, visible, and require no predecessor adapter.

## Boundary behavior

The registry describes successor behavior; it does not grant authority and cannot upgrade an installed root. A predecessor that cannot parse the successor registry or a successor-only state must fail honestly or use a separately declared read-only adapter. Candidate code must not be imported into a released predecessor process to make that predecessor appear compatible.

No diagnostic allowlist, record omission, fallback status vocabulary, or legacy constant may silently replace an invalid or unavailable registry. Repository-root managed copies remain owned by the locked released evaluator until a separately approved adoption transaction.

## Acceptance examples

### Normal behavior

**Given** a ready release record and a released release record for different versions

**When** the planner and validator load the lifecycle registry

**Then** both recognize the same admitted states, transition edges, authority effects, and version reservations from the same contract data.

### Failure behavior

**Given** a contract whose `release_record.rejected` entry is missing, whose transition target is unknown, or whose terminal flag disagrees with its outgoing edges

**When** any lifecycle consumer starts

**Then** the contract is rejected before repository mutation and no hand-maintained fallback is used.
