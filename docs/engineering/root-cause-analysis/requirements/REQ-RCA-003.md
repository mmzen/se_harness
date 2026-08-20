+++
id = "REQ-RCA-003"
type = "requirement"
title = "Preserve retrospective non-authority and follow-up boundaries"
status = "approved"
owners = ["repository-owner", "engineering-owner", "quality-owner"]
created = "2026-08-20"
updated = "2026-08-20"
statement = "WHEN the RCA is published or referenced for follow-up, THE REPOSITORY SHALL keep it outside the formal artifact graph, state its non-authoritative role, and link prevention work to GitHub issue 81 without authorizing that work."
verification_method = "graph-validation-link-check-and-manual-review"

[relations]
derives_from = ["CAP-RCA-001"]
+++

# Requirement: Preserve retrospective non-authority and follow-up boundaries

## Rationale

A retrospective should inform future decisions without becoming an alternative path for work approval, candidate verification, release, or emergency powers. Its recommendations need visible tracking but separate governing authorization.

## Preconditions and trigger

- The RCA is added under `docs/rca/`, linked from an issue, or cited by later engineering work.
- GitHub issue #81 exists as the umbrella prevention tracker.

## Required response

- Keep the RCA under `docs/rca/` without formal TOML front matter or formal artifact identity.
- State that it does not retroactively authorize the emergency releases or promote abandoned draft artifacts.
- Keep this `docs/engineering/root-cause-analysis/` packet as the only repository-native authority for RCA publication work.
- Link issue #81 from the RCA and link the RCA from issue #81 after an immutable repository identity is available.
- Require each preventive implementation to obtain its own bounded authorization rather than inherit authority from the RCA or issue.

## Failure and boundary behavior

- If the RCA claims approval, verification, release, or implementation authority, publication stops.
- If the issue or RCA implies that the preventive checklist is already authorized, the wording must be corrected before review.
- If publishing the RCA requires code, workflow, managed-file, release-record, or root-evaluator changes, the work exceeds this requirement and must be separately governed.

## Constraints

- Preserve historical and abandoned drafts without silently changing their lifecycle status.
- Do not create a second installation profile or revive self-hosting metadata.
- Opening or updating a pull request and editing issue #81 remain separately authorized external actions.

## Acceptance examples

### Example: normal behavior

**Given** issue #81 lists preventive actions

**When** a maintainer reads the linked RCA

**Then** the maintainer can understand the recommendations while seeing that each implementation still needs its own work order.

### Example: failure behavior

**Given** the RCA recommends runtime enforcement

**When** a contributor treats that recommendation as permission to change the CLI

**Then** the proposed work is unauthorized and must stop pending a separate governing chain.

## Open decisions

None. The prioritization and design of preventive implementations are explicitly deferred to future governing packets.
