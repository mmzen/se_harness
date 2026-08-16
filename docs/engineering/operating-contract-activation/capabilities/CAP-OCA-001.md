+++
id = "CAP-OCA-001"
type = "capability"
title = "Accept and operate explicit domain assurance obligations"
status = "approved"
owners = ["service-owner", "repository-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
derives_from = ["INT-OCA-001"]
+++

# Capability: Accept and operate explicit domain assurance obligations

## Actor and need

Accountable service owners need to know exactly which implemented requirements they are committing to operate, how those requirements are observed, and when a failure must block or escalate.

## Capability statement

`An accountable service owner can approve a complete operating contract that names its active requirement scope, observable controls, recovery boundary, and retained evidence without granting release authority.`

## Boundaries

- Approval is a human governance decision.
- Commands and dashboards provide evidence but cannot accept the contract.
- Release contracts and records retain their own lifecycle and authority.
- Repository-specific operating policies may be stricter than these contracts.

## Outcomes

- The six current domains have active, reviewable operating commitments.
- Contract relations and the managed authoring template agree with `TRACEABILITY.md`.
- Operators can identify a runbook, escalation route, recovery rule, and evidence set for every contract.

## Candidate requirements

- `REQ-OCA-001`: activate only complete, current, requirement-scoped operating contracts through accountable review.
