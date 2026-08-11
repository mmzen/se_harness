+++
id = "REQ-VSP-005"
type = "requirement"
title = "Exclude superseded records from release eligibility"
status = "implemented"
owners = ["release-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN verification coverage is evaluated for release preparation or validation, THE SYSTEM SHALL exclude superseded verification records and SHALL prevent supersession of a record referenced by an active release record."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-VSP-001"]
+++

# Requirement: Exclude superseded records from release eligibility

## Rationale

Historical attempts must not qualify a release or invalidate an already active release manifest without an explicit release-lifecycle decision.

## Preconditions and trigger

Release preparation selects VRECs, release validation examines included records, or a VREC transition is proposed.

## Required response

Reject superseded VRECs from release preparation and from any `ready` or `released` release record. Reject a VREC supersession while that VREC is referenced by an active release record.

## Failure and boundary behavior

Identify the affected VREC and release record. Leave all files and lifecycle states unchanged. Do not silently substitute the successor into an existing release manifest.

## Constraints

Release scope and candidate identity remain explicit human selections. Resolving an active RLS requires separate release governance outside this packet.

## Acceptance examples

An unreferenced `VREC-AGR-001` can later be superseded. A VREC included by a ready RLS cannot be superseded until the RLS is separately resolved.

## Open decisions

None when approved.
