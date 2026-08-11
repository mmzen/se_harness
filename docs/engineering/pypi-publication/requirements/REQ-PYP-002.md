+++
id = "REQ-PYP-002"
type = "requirement"
title = "Verify exact release artifact identity"
status = "implemented"
owners = ["quality-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN GitHub release assets are staged for PyPI, THE SYSTEM SHALL require explicit lowercase SHA-256 values and prove that the wheel, source distribution, and checksum manifest agree before publication."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-PYP-001"]
+++

# Requirement: Verify exact release artifact identity

## Rationale

A checksum manifest downloaded beside mutable release assets is insufficient by itself. Independent, human-reviewed expected hashes bind the workflow to retained release evidence.

## Required response

Derive the exact filenames `se_harness-VERSION-py3-none-any.whl` and `se_harness-VERSION.tar.gz` from the approved tag; reject missing or unexpected format; verify both files against required 64-character lowercase SHA-256 inputs; and require `SHA256SUMS` to match the same two lines exactly.

## Failure and boundary behavior

Any malformed hash, absent asset, digest mismatch, or manifest difference stops before publication. The workflow never repairs or regenerates a release asset.

## Constraints

Only the universal wheel and normalized source distribution enter the publisher directory. The checksum manifest remains evidence and is not uploaded as a Python distribution.

## Open decisions

None.
