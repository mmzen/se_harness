+++
id = "REQ-DST-052"
type = "requirement"
title = "Load retained evidence only when requested"
status = "approved"
owners = ["quality-owner", "security-owner", "product-owner"]
created = "2026-08-17"
updated = "2026-08-17"
statement = "WHEN a reader explicitly expands an included retained-evidence document, THE SYSTEM SHALL fetch, verify, and safely render only that declared document while keeping its identity and integrity metadata visible before expansion."
verification_method = "automated-browser-test-and-security-review"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Load retained evidence only when requested

## Rationale

Evidence Markdown contributes roughly 496 KB to the current compact snapshot and is duplicated again as approximately 461 KB of raw content. Evidence identity is useful immediately, but content is needed only when a reader chooses to inspect it.

## Preconditions and trigger

An artifact detail has loaded an included evidence descriptor containing the exact repository-relative identity, associations, byte count, digest, and manifest-controlled raw-content resource. The reader expands that evidence entry.

## Required response

- Present evidence path, associations, state, size, and digest without fetching its body.
- Fetch the one declared passive UTF-8 content resource on explicit expansion.
- Verify its size and SHA-256 before safe Markdown rendering.
- Cache verified content for the current manifest and share identical digest-addressed evidence safely.
- Retain the statement that evidence presence does not imply sufficiency, approval, verification, or release authority.

## Failure and boundary behavior

Missing, mismatched, malformed, oversized, or unavailable content leaves the evidence identity visible with a scoped failure and retry action. It must not fetch the original repository path, follow a redirect to an undeclared origin, render unverified bytes, or affect another document.

## Constraints

- Raw evidence remains passive generated text and uses content-addressed filenames.
- Evidence content is not requested merely by opening Lineage or the Evidence tab.
- The existing renderer/sanitizer, link allowlist, disclosure, and document-size limits remain authoritative.

## Acceptance examples

### Example: collapsed evidence

**Given** an artifact lists three included evidence documents,

**When** the reader opens the Evidence tab but expands none,

**Then** all three identities are shown and none of their content resources is requested.

### Example: one expanded document

**Given** the same three evidence documents,

**When** the reader expands one,

**Then** only that document is fetched, verified, sanitized, and rendered.

## Open decisions

None when approved.
