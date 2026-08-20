+++
id = "REQ-WEX-001"
type = "requirement"
title = "Project one bounded workflow scope"
status = "approved"
owners = ["requirements-steward", "quality-owner"]
created = "2026-08-20"
updated = "2026-08-20"
statement = "WHEN an operator selects a work order, verification record, or release record, THE SYSTEM SHALL produce a deterministic working set containing the selected object, its governing artifacts, and its direct lifecycle dependencies; distinguish scoped blockers, repository-wide integrity blockers, and background findings; and not present unrelated background findings as actions for the selected scope."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-WEX-001"]
+++

# Requirement: Project one bounded workflow scope

## Rationale

Repository-wide inspection is valuable for maintenance but allows an agent to redirect attention to unrelated work. A selected workflow action needs a reproducible context boundary without hiding failures that invalidate the repository as a whole.

## Preconditions and trigger

## Required response

## Failure and boundary behavior

## Constraints

## Acceptance examples

### Example: normal behavior

**Given** an implemented work order with a complete governing chain and unrelated maintenance warnings in another domain

**When** the operator selects that work order

**Then** the working set contains the work order and its governing chain, reports the other warnings only as background, and recommends no action on the unrelated domain.

### Example: failure behavior

## Open decisions

The specification must define the exact direct-dependency rules and which validator planes invalidate every selected scope before this requirement is approved for implementation.
An operator supplies exactly one resolvable `WO-*`, `VREC-*`, or `RLS-*` identity in a structurally readable repository.
- Include the selected artifact, its declared governing chain, and the lifecycle records directly required to assess its current state or proposed action.
- Classify findings as selected-scope blockers, repository-wide integrity blockers, or non-blocking background observations.
- Identify artifacts and relation paths that caused each included item to enter the working set.
- Produce stable ordering and stable classification for identical repository state and input.
- Reject an absent, ambiguous, malformed, or type-incompatible selected identity without selecting a substitute.
- Preserve repository-wide structure, governance, or configured-policy failures as blockers when they invalidate safe operation.
- Keep unrelated warnings observable in a background summary, but do not recommend their remediation as the next selected-scope action.
- The projection is derived evidence and grants no lifecycle authority.
- Transitive expansion stops at the governed boundary defined by the applicable specification; arbitrary graph reachability is not a working-scope rule.
**Given** a selected work order and a repository-wide formal graph error that prevents reliable lifecycle evaluation

**When** the scope is projected

**Then** the system reports the graph error as a repository-wide integrity blocker and performs no mutation.
