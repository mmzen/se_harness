+++
id = "REQ-DST-051"
type = "requirement"
title = "Load artifact details on demand"
status = "approved"
owners = ["product-owner", "technical-owner", "quality-owner"]
created = "2026-08-17"
updated = "2026-08-17"
statement = "WHEN a reader focuses an artifact whose detail has not been loaded for the current revision, THE SYSTEM SHALL fetch and verify exactly that artifact detail before rendering its metadata and body through the existing safe presentation boundary."
verification_method = "automated-browser-test-and-security-review"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Load artifact details on demand

## Rationale

Most readers inspect only a small fraction of repository artifacts. Embedding all Markdown bodies in the initial snapshot pays the cost of every document regardless of navigation.

## Preconditions and trigger

The topology index contains a resolved artifact and its manifest-controlled detail descriptor. The reader selects it through a card, relation, search result, graph, breadcrumb, Back, Forward, or return action.

## Required response

- Display the selected artifact identity immediately from verified compact topology data and mark detail content as loading.
- Fetch one manifest-declared artifact-detail resource, verify size and SHA-256, then render exact metadata, dates, type-specific fields, labels, EARS presentation, and sanitized Markdown.
- Reuse verified details from a revision-scoped bounded in-memory cache.
- Preserve the existing 20-entry visit-history semantics and reveal/focus behavior regardless of cache state.

## Failure and boundary behavior

A missing, malformed, oversized, or mismatched artifact detail remains an explicit unavailable detail for the selected ID. It must not render another artifact, fall back to a similarly named path, remove the history visit, or reinterpret the compact topology record as the full body.

## Constraints

- Repository IDs never become unchecked URL paths.
- No artifact content is persisted to browser storage under this requirement.
- Existing safe Markdown and EARS non-authority rules remain applicable after loading.

## Acceptance examples

### Example: first visit and revisit

**Given** artifact `REQ-DST-049` has not been opened,

**When** it is selected and later revisited,

**Then** one verified detail request is made and the cached exact content is reused on the revisit.

### Example: stale detail response

**Given** one detail request is slow and the reader selects another artifact,

**When** the older response completes,

**Then** it may enter the cache but cannot replace the newer selected artifact's panel.

## Open decisions

None when approved.
