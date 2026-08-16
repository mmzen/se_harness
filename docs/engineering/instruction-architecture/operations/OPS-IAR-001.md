+++
id = "OPS-IAR-001"
type = "operating_contract"
title = "Operate the instruction and enforcement architecture"
status = "approved"
owners = ["service-owner", "repository-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-16"

[relations]
assures = ["REQ-IAR-001", "REQ-IAR-002", "REQ-IAR-003", "REQ-IAR-004", "REQ-IAR-005", "REQ-IAR-006", "REQ-IAR-007", "REQ-IAR-008", "REQ-IAR-009", "REQ-IAR-010", "REQ-IAR-011", "REQ-IAR-012", "REQ-IAR-013", "REQ-IAR-014", "REQ-IAR-015", "REQ-IAR-016", "REQ-IAR-017", "REQ-IAR-018"]
+++

# Operating Contract: Operate the instruction and enforcement architecture

## Service level objectives

Every supported installation exposes one intact managed instruction route, preserves owner-controlled guidance, passes managed integrity, and evaluates work readiness and pull-request governance with the intended released baseline. Formal validation and inspection remain deterministic, read-only, plane-labelled, and non-authoritative.

## Observability

Use `harnessctl doctor .`, phase-appropriate `harnessctl preflight . --work-order WO-...`, `harnessctl validate .`, `harnessctl inspect .`, and `harnessctl dashboard .`. Monitor required CI for managed drift, incomplete context, invalid graphs, ineligible work-order declarations, independent-check acquisition failures, and governor-pin divergence. Review architecture-decision applicability and the artifact catalog when traceability changes.

## Alerts and escalation

Treat missing or damaged managed routes, ambiguous owner/managed conflicts, incomplete required context, invalid formal graphs, lost required-check protection, unexplained governor-pin changes, or nondeterministic inspection as blocking. Escalate any attempt to infer authority or automate approval, verification, release, publication, or deployment.

## Capacity and cost boundaries

Instruction, validation, inspection, preflight, and dashboard generation operate locally at repository scale with the Python standard library. The independent CI job may acquire one pinned released wheel; no always-on service, database, semantic prose interpreter, or aggregate health score is required.

## Backup and recovery

Version control retains managed templates, locks, repository-owned context, governance records, and candidate history. Recover managed drift through `harnessctl doctor`, a reviewed upgrade, or `reconcile-governor` where applicable; never erase owner content, rewrite historical decisions, or let candidate source silently replace the released governor.

## Security and compliance controls

Maintain managed/owner boundaries, path containment, non-execution of artifact bodies, exact independent-governor pinning and checksum verification, explicit work-order selection, typed architecture traceability, and separate accountable decision rights.

## Automated remediation envelope

Automation may validate, inspect, render derived dashboards, report suggestions with `automatic = false`, and prepare bounded plans or ready records under an approved work order. It may not resolve natural-language conflicts, accept architecture decisions, approve work, transition records, change repository-host protection, commit, release, publish, or deploy.

## Runbooks

Follow `ENGINEERING_HARNESS.md` for routing, `docs/engineering/WORKFLOW.md` for procedure, `TRACEABILITY.md` for artifact applicability, `REPOSITORY_CONTEXT.md` for repository commands, and the self-hosting boundary when developing SE Harness. After an upgrade, run doctor, validate, inspect, and the applicable start/review preflight; reconcile the governor only through its separate upgrade workflow.

## Evidence retention

Retain tool and governor versions, workflow and checksum identity, doctor/validate/inspect/preflight output, managed-upgrade or reconciliation plans, required-check results, artifact and architecture review decisions, candidate commit, deviations, approvals, and follow-up findings under the applicable work order.
