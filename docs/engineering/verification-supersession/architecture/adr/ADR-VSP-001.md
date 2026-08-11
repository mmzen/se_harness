+++
id = "ADR-VSP-001"
type = "adr"
title = "Explicit terminal supersession on existing verification records"
status = "approved"
owners = ["technical-owner", "quality-owner", "release-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
decides = ["ARCH-VSP-001"]
+++

# ADR: Explicit terminal supersession on existing verification records

## Status

Accepted.

## Context

`VREC-AGR-001` is a valid ready record for an earlier candidate, while `VREC-PMI-001` is the later verified record that covers its work plus the corrective work. The old record should remain auditable but should not look like an active decision queue item or remain eligible for release preparation.

## Decision drivers

Preserve immutable provenance, make authority explicit, prevent stale release inputs, avoid deletion, retain backward compatibility, expose the relationship visually, and keep automation non-authorizing.

## Considered options

1. Leave stale records `ready` forever. Rejected because active and historical intent remain ambiguous.
2. Mark the old record `verified`. Rejected because that falsely approves its earlier candidate.
3. Delete or rewrite the old record. Rejected because audit history and commit-bound evidence would be lost.
4. Automatically supersede on overlapping verified coverage. Rejected because coverage does not grant human authority or uniquely identify intent.
5. Add a new supersession artifact type. Rejected because the lifecycle fact and record-to-record edge fit the existing VREC graph.
6. Add terminal `superseded` state with one typed, human-authorized successor relation. Selected.

## Decision

Permit only `ready -> superseded` for VRECs in this iteration. Require `superseded_by` to identify exactly one distinct verified or released VREC whose work coverage is a superset. Require structured transition time and authorizer plus retained governance evidence. Preserve the old record's captured metadata and original relations. Block active-release references and all release use of superseded records. Display the edge and non-authoritative stale-ready warnings.

## Consequences

Historical attempts remain visible and accurate, active queues become meaningful, and release eligibility is explicit. Governance requires an additional bounded transition commit. Existing stale records are not cleaned automatically. Verified or released record retirement and release-record supersession remain future decisions. Current-state validation cannot prove prior-byte immutability alone, so the governance diff and evidence remain required controls.

## Validation

Automated validator, release, dashboard, Explorer, compatibility, installation, and packaging tests enforce the observable contract. Manual review confirms terminology, immutable-field diffs, authority evidence, and readable many-to-one history.
