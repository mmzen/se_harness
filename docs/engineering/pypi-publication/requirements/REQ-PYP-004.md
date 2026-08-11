+++
id = "REQ-PYP-004"
type = "requirement"
title = "Promote without rebuilding or replacement"
status = "implemented"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN publication preflight passes, THE SYSTEM SHALL submit only the verified GitHub wheel and source distribution to PyPI with metadata verification and attestations enabled, without rebuilding or tolerating an existing filename."
verification_method = "inspection-and-end-to-end"

[relations]
derives_from = ["CAP-PYP-001"]
+++

# Requirement: Promote without rebuilding or replacement

## Rationale

Rebuilding would sever the exact hash relationship to the verified release. Ignoring an existing filename would hide a duplicate or partial publication anomaly.

## Required response

Stage only the two verified distributions, run the pinned official publisher with metadata verification and attestations enabled, and leave duplicate tolerance disabled.

## Failure and boundary behavior

A PyPI rejection, existing filename, metadata failure, or attestation failure is blocking. Recovery requires inspection and, if artifact correction is needed, a new verified package version.

## Constraints

The publication workflow contains no build command and produces no distribution archive.

## Open decisions

None.
