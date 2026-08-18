+++
id = "REQ-PYP-001"
type = "requirement"
title = "Select one released record explicitly"
status = "implemented"
owners = ["release-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-18"
statement = "WHEN production publication is requested, THE SYSTEM SHALL accept one released RLS identifier from main, derive its final semantic-version GitHub release and exact distribution identities, and reject missing, draft, prerelease, partial, or mismatched state."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-PYP-001"]
+++

# Requirement: Select one released record explicitly

## Rationale

Publishing whichever checkout, record, or release happens to be current would make authority and distribution identity ambiguous. Re-entering a tag and hashes after the release decision also creates avoidable transcription risk.

## Required response

Accept one manual `RLS-*` identifier, require that record to be `released` in trusted first-parent `main` history, and derive its `vMAJOR.MINOR.PATCH` tag, candidate, filenames, and hashes. The PyPI boundary proceeds only after the named GitHub Release is final and exact.

## Failure and boundary behavior

Fail before requesting publication credentials or copying any file into the publisher input directory when authority or immutable state is missing, partial, or mismatched. Prerelease publication requires a separately approved requirement change.

## Constraints

The top-level workflow is manually dispatched from `main` and its PyPI job runs through the `pypi` environment. It does not select the latest record or release implicitly, and it accepts no tag or hash override.

## Open decisions

None.
