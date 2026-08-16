+++
id = "OPS-AGR-001"
type = "operating_contract"
title = "Maintain aggregate release lineage"
status = "approved"
owners = ["service-owner", "quality-owner", "release-owner"]
created = "2026-08-11"
updated = "2026-08-16"

[relations]
assures = ["REQ-AGR-001", "REQ-AGR-002", "REQ-AGR-003", "REQ-AGR-004", "REQ-AGR-005", "REQ-AGR-006", "REQ-AGR-007", "REQ-AGR-008"]
+++

# Operating Contract: Maintain aggregate release lineage

## Service level objectives

Every retained aggregate graph validates deterministically, and every released version has one declared candidate commit and complete released-work coverage.

## Observability

Use `harnessctl validate .`, `harnessctl inspect .`, and `harnessctl dashboard .` to inspect aggregate scope, lifecycle, commit equality, checkout drift, and intent-to-release paths. Retain `capture-verification` and `prepare-release` output when those commands are authorized.

## Alerts and escalation

Treat missing coverage, extra released work, commit mismatch, unsafe evidence, duplicate version, invalid lifecycle, unavailable candidate, or moved tag as release-blocking. Escalate scope ambiguity to product and release owners.

## Capacity and cost boundaries

Operate locally with standard-library tooling. Do not introduce a required network service for validation or exploration.

## Backup and recovery

Formal records, evidence, tags, and package checksums are retained through version control and the authorized release host. Never rewrite a published candidate tag to repair provenance.

## Security and compliance controls

Preserve explicit selection, path containment, exact commit identity, separate human authority, safe target handling, and non-execution of artifact bodies.

## Automated remediation envelope

Automation may regenerate derived dashboards and prepare new ready records. It may not alter approved scope, lifecycle decisions, commits, tags, releases, or published assets.

## Runbooks

Follow `docs/engineering/WORKFLOW.md`, `SPEC-AGR-001`, the applicable approved release contract, and repository-context commands. A draft release contract is a proposal and grants no release authority.

## Evidence retention

Retain aggregate verification evidence per work order, the verified VREC, released RLS, candidate and tag identity, wheel checksum, smoke-test output, authorization decision, and post-release review.
