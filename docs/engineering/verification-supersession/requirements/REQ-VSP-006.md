+++
id = "REQ-VSP-006"
type = "requirement"
title = "Visualize supersession and stale-ready anomalies"
status = "implemented"
owners = ["repository-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN the dashboard contains verification records, THE SYSTEM SHALL project supersession lineage, separate historical records from active candidates, and report potentially stale ready records as derived non-authoritative findings."
verification_method = "snapshot-test-and-review"

[relations]
derives_from = ["CAP-VSP-001"]
+++

# Requirement: Visualize supersession and stale-ready anomalies

## Rationale

The lifecycle is useful only when operators can see which record is active, which is historical, and why.

## Preconditions and trigger

Harness Explorer generation processes VRECs with overlapping work coverage or explicit supersession relations.

## Required response

Expose `superseded_by` in JSON and render a directed old-to-successor edge with status, commit, coverage, and successor eligibility. Exclude superseded records from active ready counts and readiness satisfaction while retaining them in history. Emit a deterministic warning when a ready VREC's work set is fully covered by another verified or released VREC and no explicit supersession exists.

## Failure and boundary behavior

Label stale-ready detection as derived and non-authoritative. A warning must never mutate status or choose a successor. Invalid explicit relations remain blocking validator errors.

## Constraints

The Explorer remains generated, local, deterministic, and non-authoritative. Existing filters and record views remain usable.

## Acceptance examples

Before governance cleanup, `VREC-AGR-001` is flagged as a potentially stale ready record. After its authorized supersession, the warning clears and a visible edge points to `VREC-PMI-001`.

## Open decisions

None when approved.
