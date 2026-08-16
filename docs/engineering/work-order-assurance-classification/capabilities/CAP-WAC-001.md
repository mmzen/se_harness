+++
id = "CAP-WAC-001"
type = "capability"
title = "Classify and follow commit-bound assurance obligations"
status = "approved"
owners = ["quality-owner", "repository-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
derives_from = ["INT-WAC-001"]
+++

# Capability: Classify and follow commit-bound assurance obligations

## Actor and need

Assurance and repository owners need to distinguish implementation validation from commit-bound assurance without relying on titles, dates, branches, prose inference, or agent judgment.

## Capability statement

`An accountable owner can classify whether a work order requires commit-bound verification, while engineering agents and reviewers can enforce and inspect that declared obligation without granting authority automatically.`

## Boundaries

The capability records applicability and derived attention only. It does not verify evidence, select a candidate commit, choose aggregate VREC membership, transition a record, waive release coverage, or make an external decision.

## Outcomes

- Newly actionable work orders carry an explicit, reviewable declaration.
- Preflight exposes the declaration before execution.
- Inspection reports implemented required work lacking an active VREC proposal.
- Completed legacy and explicitly non-required governance work do not create false assurance debt.

## Candidate requirements

See `REQ-WAC-001..005`.
