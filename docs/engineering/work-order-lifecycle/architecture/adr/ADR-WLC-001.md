+++
id = "ADR-WLC-001"
type = "adr"
title = "End governance work at implemented and validate assurance separately"
status = "approved"
owners = ["technical-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
decides = ["ARCH-WLC-001"]
+++

# ADR: End governance work at implemented and validate assurance separately

## Decision

Use `implemented` as the completed state for governance-only work not selected into a VREC. Reserve `verified` and `released` work-order status for work covered by corresponding commit-bound records when repository policy requires provenance. Promote uncovered verified-work detection from a derived Explorer warning to formal policy-aware validation.

## Rationale

Marking the work order that authorizes a verification transition as `verified` creates a new uncovered verified work order and invites infinite recursion. Completion and assurance are separate facts: the work order records completed governance action, while the target VREC records the assurance decision.

## Alternatives rejected

- Add a new `completed` lifecycle value: rejected because `implemented` already expresses completed work and is supported by release tooling.
- Create a VREC for every governance-decision work order: rejected because it creates unnecessary recursive governance and expands release-irrelevant provenance.
- Keep a derived warning only: rejected where configured provenance is mandatory because a required invariant must be authoritative and blocking.
- Infer completed status from evidence prose or Git history: rejected because automation cannot infer authority or completion decisions safely.

## Consequences

Legacy statuses require an explicit one-time correction. Repositories without the configured requirement remain compatible. Repositories opting into the requirement receive a blocking diagnostic instead of `W-REV-001`.
