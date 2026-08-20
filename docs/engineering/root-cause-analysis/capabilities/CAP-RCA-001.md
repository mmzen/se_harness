+++
id = "CAP-RCA-001"
type = "capability"
title = "Review evidence-backed release incident learning"
status = "approved"
owners = ["product-owner", "repository-owner"]
created = "2026-08-20"
updated = "2026-08-20"

[relations]
derives_from = ["INT-RCA-001"]
+++

# Capability: Review evidence-backed release incident learning

## Actor and need

Repository maintainers, accountable owners, and reviewers need one durable account of the 0.5.0 governance deadlock so that they can understand the failed boundary, evaluate the recovery, and prioritize prevention without reconstructing the incident from transient conversation state.

## Capability statement

Maintainers can review a canonical, evidence-backed, non-authoritative RCA under the standard repository lifecycle and trace its proposed follow-up to a public tracking issue.

## Boundaries

- The capability publishes retrospective documentation only.
- It does not execute or authorize any preventive action.
- It does not replace formal intent, requirements, work authorization, verification records, or release records.
- It does not change the root evaluator, candidate, release, workflow, or external publication.
- It preserves the distinction between public evidence and repository-native authority.

## Outcomes

- The incident's primary cause and causal chain are explicit.
- Recovery steps and exact release evidence are inspectable.
- Completed corrections are not confused with recommendations.
- The RCA and GitHub issue #81 cross-reference each other after governed publication.
- Future work can cite a stable incident record while obtaining its own authorization.

## Candidate requirements

- `REQ-RCA-001`: publish a complete canonical RCA.
- `REQ-RCA-002`: retain exact evidence and distinguish fact from authority.
- `REQ-RCA-003`: preserve the non-authority boundary and connect follow-up tracking.
