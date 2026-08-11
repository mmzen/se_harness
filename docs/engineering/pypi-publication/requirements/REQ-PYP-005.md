+++
id = "REQ-PYP-005"
type = "requirement"
title = "Keep publication authority and evidence explicit"
status = "implemented"
owners = ["release-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN a PyPI publication is contemplated or completed, THE SYSTEM SHALL require a separate accountable release-owner authorization and retain the workflow run, PyPI URLs, hashes, attestations, and installation result as evidence."
verification_method = "manual-assessment"

[relations]
derives_from = ["CAP-PYP-001"]
+++

# Requirement: Keep publication authority and evidence explicit

## Rationale

Workflow availability is capability, not authorization. The existing `RLS-SEH-001` decision explicitly excluded PyPI and must remain truthful history.

## Required response

Record a new bounded publication authorization naming the release record, tag, exact hashes, target project, and accountable owner before dispatch. After success, retain the run URL, PyPI project/version/file URLs, published hashes and attestations, and a clean exact-version installation smoke test.

## Failure and boundary behavior

No authorization or incomplete provenance means no dispatch. A failed or partial upload is recorded as an anomaly and escalated; it is not silently retried with duplicate tolerance.

## Constraints

This implementation work order does not itself authorize a PyPI workflow run.

## Open decisions

None.
