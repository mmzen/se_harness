+++
id = "OPS-WLC-001"
type = "operating_contract"
title = "Operate work-order lifecycle consistency"
status = "approved"
owners = ["service-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-16"

[relations]
assures = ["REQ-WLC-001", "REQ-WLC-002", "REQ-WLC-003", "REQ-WLC-004", "REQ-WLC-005", "REQ-WLC-006"]
+++

# Operating Contract: Operate work-order lifecycle consistency

## Service level objectives

Every work order uses its defined lifecycle meaning, completed governance-only work stops honestly at `implemented` unless a distinct eligible VREC covers it, and every configured `verified` or `released` work claim has commit-bound coverage. Installed and self-hosted lifecycle policy remain equivalent.

## Observability

Use `harnessctl validate .` to detect uncovered verified or released work, `harnessctl inspect .` and `harnessctl dashboard .` to review lifecycle queues without duplicate authority, and phase-appropriate preflight to confirm work-order eligibility. Compare canonical and installed workflow, template, validator, and Explorer material during distribution checks.

## Alerts and escalation

Treat uncovered verified or released work, contradictory lifecycle meanings, missing retained evidence, duplicate authoritative/derived findings, or root/canonical semantic drift as blocking. Escalate legacy normalization, lifecycle ambiguity, and every proposed automated authority transition to repository and quality owners.

## Capacity and cost boundaries

Lifecycle checks operate locally over repository artifacts with standard-library tooling. They require no network service, database, background monitor, historical rewrite, or recursive verification chain.

## Backup and recovery

Version control retains work orders, VRECs, RLS records, evidence, and lifecycle corrections. Correct a mistaken current definition through separately authorized governance; never delete an eligible historical record, infer coverage, or rewrite a released candidate.

## Security and compliance controls

Maintain exact work-order identity, configured commit-bound coverage, non-execution of artifact bodies, separate human decision rights, immutable captured provenance, and a clear distinction between authoritative validator errors and derived Explorer observations.

## Automated remediation envelope

Automation may validate relations, surface uncovered work, derive non-authoritative queues, and prepare records when separately authorized. It may not decide that work is implemented, verified, released, superseded, or rejected; normalize historical status; select coverage; commit; tag; publish; or deploy.

## Runbooks

Follow `docs/engineering/WORKFLOW.md` for lifecycle meanings, `TRACEABILITY.md` for VREC and RLS applicability, the applicable work order for status corrections, and repository-context commands for validation. When a governance-only action completes, record it as `implemented`; create a later aggregate VREC only when accountable assurance is intentionally requested.

## Evidence retention

Retain the work-order status before and after, governing configuration, related VREC/RLS IDs, exact candidate commits, validator and Explorer output, canonical/root parity, authorization, rationale, changed paths, and any unresolved lifecycle anomaly.
