+++
id = "OPS-VSP-001"
type = "operating_contract"
title = "Operate verification-supersession lineage"
status = "draft"
owners = ["service-owner", "quality-owner", "release-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
assures = ["REQ-VSP-001", "REQ-VSP-002", "REQ-VSP-003", "REQ-VSP-004", "REQ-VSP-005", "REQ-VSP-006", "REQ-VSP-007", "REL-VSP-001"]
+++

# Operating Contract: Operate verification-supersession lineage

## Service level objectives

Every explicit supersession graph validates deterministically, every superseded VREC has one eligible coverage-preserving successor, and no superseded record participates in active verification or release readiness.

## Observability

Use artifact validation and Harness Explorer to inspect source and successor status, commits, work coverage, authorizer, transition time, active release references, stale-ready findings, and checkout drift.

## Alerts and escalation

Treat missing or ineligible successors, lost coverage, cycles, changed captured metadata, active release references, release use, missing governance evidence, or ambiguous authority as blocking. Treat stale-ready findings as review prompts rather than automatic errors.

## Capacity and cost boundaries

Operate locally with standard-library tooling and repository-scale artifact graphs. Do not introduce a required service, database, or network dependency.

## Backup and recovery

Retain source and successor records, governance work orders, evidence, commits, release records, and tags in version control. Correct mistakes through later explicit governance; never delete or rewrite published history.

## Security and compliance controls

Preserve typed relation validation, cycle detection, exact commit identity, evidence paths, non-execution of bodies, separate human authority, release exclusion, and target-repository ownership rules.

## Automated remediation envelope

Automation may validate, regenerate dashboards, and identify possible stale records. It may not choose a successor, change lifecycle status, edit historical VRECs, resolve release records, commit, tag, publish, or deploy.

## Runbooks

Follow `docs/engineering/WORKFLOW.md`, `SPEC-VSP-001`, the applicable governance work order, and repository context. Review candidate identity and work coverage before authorizing a transition; validate and inspect the bounded diff before committing.

## Evidence retention

Retain the superseded and successor IDs, immutable candidate metadata, work-set comparison, transition authorizer and timestamp, governance diff, validation and dashboard outputs, release-reference check, approval, and any follow-up observation.
