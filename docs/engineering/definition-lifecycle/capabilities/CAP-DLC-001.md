+++
id = "CAP-DLC-001"
type = "capability"
title = "Read authority, generation, and realization from the source that owns each"
status = "approved"
owners = ["product-owner", "domain-owner"]
created = "2026-08-26"
updated = "2026-08-26"

[relations]
derives_from = ["INT-DLC-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-26T09:33:19Z"
decided_by = "product-owner"
+++

# Capability: Read authority, generation, and realization from the source that owns each

## Actor and need

An owner deciding a definition needs to know exactly what the decision means. A
requirements steward needs to know which requirements are covered by verified
work at which commit. A repository owner upgrading a consumer repository needs
pre-contract artifacts to be exempted by something that says so, not by a
lifecycle value that happens to correlate.

None of these needs is met by one overloaded field, and one field cannot meet
all three without lying about at least two.

## Capability statement

`An actor can determine a definition's governing authority from its lifecycle status, its schema generation from an explicit declaration, and its realization from derived work-order and verification coverage at an exact commit, without any of the three answers being inferred from either of the others.`

## Boundaries

- The capability covers the nine definition families only. Work-order,
  verification-record, and release-record lifecycles are unchanged.
- It changes no artifact bytes. Existing statuses, events, and relations remain
  exactly as recorded.
- It removes one edge from the definition lifecycle's reachable graph. It
  removes no status from the accepted vocabulary and no authority from any
  existing artifact.
- Derived realization is a report. It grants no authority, approves nothing,
  transitions nothing, and is stored in no artifact field.
- Declared exemptions suppress an error, never a maintenance diagnostic. Every
  exemption stays visible as outstanding work.
- The capability adds no role, gate, artifact type, relation, or lifecycle
  family.

## Outcomes

- A definition's `status` answers one question, and the answer to that question
  is unchanged for all 630 existing definitions.
- The reachable definition lifecycle matches the eleven-step managed procedure
  and the `DR-DEFINITION-DECIDE` outcome set: approve or reject, and nothing
  else.
- An approved requirement, specification, or architecture is routed to the
  decision that actually comes next — selecting or authorizing a bounded work
  order — instead of to a completion decision no role holds.
- The 14 architectures that predate `decision_assessment` are exempted by name,
  in a frozen closed set, and remain visible as 14 outstanding maintenance
  warnings.
- A pre-contract definition status is exempted by declaration, and a new one
  cannot be authored without a recorded decision.
- Realization is answerable, commit-bound, and self-correcting when a further
  work order selects the same definition.

## Candidate requirements

- `REQ-DLC-001`: resolve architecture generation from a declaration, not from
  lifecycle status.
- `REQ-DLC-002`: terminate the definition lifecycle at `approved`.
- `REQ-DLC-003`: derive definition realization from work-order and verification
  coverage.
- `REQ-DLC-004`: require a recorded decision for every definition state past
  `draft`.
- `REQ-DLC-005`: preserve every existing governing record and diagnostic
  outcome.
