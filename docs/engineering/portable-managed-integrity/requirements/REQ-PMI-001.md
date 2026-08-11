+++
id = "REQ-PMI-001"
type = "requirement"
title = "Use a versioned canonical text digest"
status = "implemented"
owners = ["quality-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN the harness records integrity for managed UTF-8 text or a managed text fragment, THE SYSTEM SHALL compute SHA-256 over an explicitly versioned canonical newline representation."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-PMI-001"]
+++

# Requirement: Use a versioned canonical text digest

## Rationale

Raw checkout bytes are not a stable identity for text when Git or platform tooling may represent the same line boundaries as LF, CRLF, or CR.

## Preconditions and trigger

The installer, upgrade planner, lock writer, or doctor evaluates a harness-managed UTF-8 text payload or extracted managed block.

## Required response

Validate UTF-8, normalize CRLF and remaining CR line endings to LF, preserve all other characters and bytes through UTF-8 re-encoding, and compute SHA-256 over that canonical representation. Record the canonical mode in the lock schema.

## Failure and boundary behavior

Invalid UTF-8 in a text-managed payload fails closed with a bounded path-level diagnostic. Binary canonicalization is not inferred.

## Constraints

The digest remains lowercase 64-character SHA-256. Canonicalization changes representation only, not whitespace other than line terminators, Unicode normalization, BOM handling, trailing newline presence, or content ordering.

## Acceptance examples

LF, CRLF, and CR forms of identical text produce one digest. Changing a letter, space, tab, trailing newline, or Unicode code point produces a different digest.

## Open decisions

None when approved.
