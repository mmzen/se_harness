+++
id = "REQ-DST-043"
type = "requirement"
title = "Render formal artifact bodies safely"
status = "approved"
owners = ["product-owner", "security-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"
statement = "WHEN a focused formal artifact has a Markdown body, THE SYSTEM SHALL render its readable structure without executing repository content or causing an undeclared network request."
verification_method = "automated-test-and-security-review"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Render formal artifact bodies safely

## Rationale

Artifact metadata alone cannot explain rationale, scope, acceptance examples, decisions, or operational constraints. The validator already parses and retains the body, but the canonical Explorer projection omits it. Rendering repository Markdown introduces an executable-content boundary that must be explicit and safe.

## Preconditions and trigger

This requirement applies to the Markdown body separated from a validated artifact's TOML front matter.

## Required response

- Project the exact UTF-8 Markdown body and deterministic content identity into the canonical dashboard payload.
- Render common repository Markdown structure, including headings, paragraphs, emphasis, lists, block quotes, code, tables, and safe links.
- Disable raw HTML and prevent script, style, event-handler, iframe, object, embedded data, active URL, and remote-image execution.
- Use only locally distributed rendering and sanitization code; do not add another runtime CDN or hosted rendering service.
- Fall back to escaped plain text with an explicit rendering notice if safe structured rendering is unavailable.
- Report omitted oversized, unreadable, or unsupported content explicitly rather than silently truncating or partially interpreting it.

## Failure and boundary behavior

Malformed Markdown remains inert. Unsafe HTML and URLs are rejected or rendered as text. A body that exceeds the governed per-document or total projection budget is omitted as a whole with its path, size, digest when available, and omission reason retained.

## Constraints

- Artifact bodies never flow back into validation, lifecycle, approval, verification, release, or repository state.
- The same repository state produces byte-identical canonical content projection and rendered output.
- Rendering must remain usable without the optional Overview 3D CDN dependency.
- Content projection must remain bounded in memory and output size.

## Acceptance examples

### Example: structured body

**Given** an artifact body contains headings, a list, a table, inline code, and a fenced code block,

**When** the artifact is focused,

**Then** those structures are readable in Overview and their exact text is preserved.

### Example: hostile body

**Given** an artifact body contains raw HTML, a script, an event handler, a `javascript:` link, and a remote image,

**When** it is rendered,

**Then** none executes or causes a request and the remaining safe content stays readable.

## Open decisions

None when approved.
