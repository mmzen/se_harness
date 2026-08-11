+++
id = "REQ-PMI-002"
type = "requirement"
title = "Make doctor results newline-portable"
status = "implemented"
owners = ["quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN doctor evaluates a canonical-mode managed file or fragment, THE SYSTEM SHALL treat LF, CRLF, and CR representations of the same text as unchanged while reporting real content differences as failures."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-PMI-001"]
+++

# Requirement: Make doctor results newline-portable

## Rationale

Integrity diagnostics must be trustworthy on every supported checkout rather than depend on the machine that wrote or checked out the file.

## Preconditions and trigger

A valid schema-2 canonical lock exists and `harnessctl doctor` evaluates its managed entries.

## Required response

Use the recorded canonical mode for complete managed files and the extracted bounded block for fragments. Report unchanged content as passing regardless of newline representation.

## Failure and boundary behavior

Missing files, malformed fragments, invalid UTF-8, unsupported modes, and non-newline content differences remain failures. Diagnostics identify paths and reasons without printing file bodies.

## Constraints

Doctor remains read-only and deterministic and must not repair locks or target content.

## Acceptance examples

A Markdown file checked out with CRLF passes against an LF-derived canonical digest. A one-character edit in the same file fails.

## Open decisions

None when approved.
