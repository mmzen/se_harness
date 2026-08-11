+++
id = "REQ-PMI-006"
type = "requirement"
title = "Verify distribution and self-lock consistency"
status = "implemented"
owners = ["quality-owner", "release-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN a harness release candidate is verified, THE SYSTEM SHALL prove that source managed files, canonical templates, lock entries, wheel contents, and a fresh installation use consistent canonical integrity semantics."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-PMI-001"]
+++

# Requirement: Verify distribution and self-lock consistency

## Rationale

Unit behavior alone cannot detect a stale self-repository lock or a package that contains different managed bytes.

## Preconditions and trigger

The complete verification contract runs for a candidate that changes integrity semantics or managed standard content.

## Required response

Regenerate the self-repository lock through the supported lock writer, verify every managed entry, assert required source/canonical parity, inspect the wheel, install it in a fresh environment, and run doctor on LF and CRLF-equivalent target content.

## Failure and boundary behavior

Any stale entry, missing managed asset, parity mismatch, invalid wheel content, or fresh-install diagnostic is release-blocking.

## Constraints

Generated evidence records exact commands, tool versions, hashes, deviations, and platform limitations.

## Acceptance examples

The corrected repository doctor passes after a clean checkout, and a deliberately stale lock fixture fails deterministically.

## Open decisions

None when approved.
