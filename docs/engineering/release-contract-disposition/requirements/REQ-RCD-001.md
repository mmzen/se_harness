+++
id = "REQ-RCD-001"
type = "requirement"
title = "Explicitly dispose superseded release proposals"
status = "implemented"
owners = ["release-owner", "repository-owner"]
created = "2026-08-16"
updated = "2026-08-16"
statement = "WHEN a draft release contract was not selected as release authority and all of its gated work was released through a different authoritative contract and release record, SE Harness SHALL retain the proposal as rejected and SHALL identify the actual release lineage without rewriting historical authority."
verification_method = "artifact-graph validation and exact lineage inspection"

[relations]
derives_from = ["CAP-RCD-001"]
+++

# Requirement: Explicitly dispose superseded release proposals

## Rationale

A perpetual draft appears to be unfinished definition. Retroactive approval would create duplicate or misleading release authority, while deletion would erase why the proposal existed. Rejection records that the proposal itself was not selected; it does not reject the implementation that was released elsewhere.

## Required response

- Preserve the original release-contract identity, owners, gates, and contract text.
- Transition only an abandoned `draft` proposal to `rejected` through an accountable decision.
- State which authoritative contract, release record, version, and tag released its work.
- Preserve every historical RLS and its `satisfies` relation unchanged.
- Keep continuing operational obligations independent through their OPS records.

## Failure and boundary behavior

Do not reject a contract referenced by a ready or released RLS. Do not infer release from work-order or VREC state alone. If the complete gated work cannot be mapped to an authoritative release record, leave the proposal unresolved and escalate.
