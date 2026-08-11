+++
id = "REQ-PYP-001"
type = "requirement"
title = "Select one final GitHub release explicitly"
status = "implemented"
owners = ["release-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN a production PyPI publication is requested, THE SYSTEM SHALL require an explicit final semantic-version GitHub release tag and reject a draft, prerelease, malformed tag, or missing release."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-PYP-001"]
+++

# Requirement: Select one final GitHub release explicitly

## Rationale

Publishing whichever checkout or release happens to be current would make the distribution target ambiguous.

## Required response

Accept one manual `vMAJOR.MINOR.PATCH` tag, query the named GitHub release, and proceed only when it exists and is neither draft nor prerelease.

## Failure and boundary behavior

Fail before requesting publication credentials or copying any file into the publisher input directory. Prerelease publication requires a separately approved requirement change.

## Constraints

The workflow is manually dispatched and runs through the `pypi` environment. It does not select the latest release implicitly.

## Open decisions

None.
