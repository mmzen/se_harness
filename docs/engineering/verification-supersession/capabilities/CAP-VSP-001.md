+++
id = "CAP-VSP-001"
type = "capability"
title = "Retire stale verification candidates explicitly"
status = "approved"
owners = ["repository-owner", "quality-owner", "release-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
derives_from = ["INT-VSP-001"]
+++

# Capability: Retire stale verification candidates explicitly

## Actor and need

An accountable assurance owner needs to close a ready verification attempt after a later record has become authoritative, without deleting history, validating the wrong commit, or making the stale record release-eligible.

## Capability statement

`An assurance owner can explicitly supersede a ready verification record with one verified or released successor while preserving immutable provenance and complete audit visibility.`

## Boundaries

The capability applies to verification records in `ready` state. It does not automate authority, change successor status, rewrite candidate metadata, retire verified or released records, mutate Git, or publish anything.

## Outcomes

- Closed verification queues with explicit historical lineage.
- Mechanically checked successor type, status, coverage, and acyclicity.
- Release preparation that cannot consume superseded records.
- Dashboard views that separate active candidates from historical attempts.
- Backward-compatible adoption in existing repositories.

## Candidate requirements

`REQ-VSP-001` through `REQ-VSP-007` define lifecycle eligibility, typed successor integrity, coverage and cycle safety, provenance preservation and authority, release exclusion, visualization and anomaly detection, and compatible distribution.
