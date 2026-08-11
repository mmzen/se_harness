+++
id = "OPS-IAR-001"
type = "operating_contract"
title = "Operate the instruction and enforcement architecture"
status = "draft"
owners = ["service-owner", "repository-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
assures = ["REL-IAR-001"]
+++

# Operating Contract: Operate the instruction and enforcement architecture

## Operational checks

- Monitor required CI for managed drift, incomplete context, invalid graphs, missing or ineligible work-order declarations, and independent-check acquisition failures.
- Review the exact external harness pin on every harness release and upgrade it through a separately reviewed change.
- Periodically confirm that the default branch requires the harness check and that review ownership covers workflow, lock, managed instruction, and governance paths.
- Run `doctor` after harness upgrades and preflight before implementation begins.
- Review owner context and domain-index accuracy when repository commands, architecture, ownership, or sensitive paths change.
- Treat a persistent customized managed file as an explicit reconciliation task, not as a reason to weaken integrity checks.

## Service indicators

- Required harness check success rate and acquisition failures.
- Count and age of managed-file drift or ambiguous migration reports.
- Pull requests rejected for missing, multiple, malformed, or ineligible work-order declarations.
- Repositories with incomplete required context fields.
- Age of the external harness pin relative to the approved released version.

## Escalation

Escalate owner/managed instruction conflicts, lost required-check protection, unexplained pin changes, integrity drift, incomplete context before implementation, attempts to infer authority, or any proposal to automate approval, verification, release, publication, or deployment.

## Authority boundary

Operational observation and remediation proposals do not authorize artifact transitions, repository-host setting changes, commits, releases, or publications.
