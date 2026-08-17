+++
id = "REQ-DST-046"
type = "requirement"
title = "Present retained evidence content portably"
status = "approved"
owners = ["quality-owner", "security-owner", "product-owner"]
created = "2026-08-16"
updated = "2026-08-16"
statement = "WHEN a focused artifact has an allowed retained-evidence reference, THE SYSTEM SHALL present its repository identity, safe rendered content, and portable raw source within the generated dashboard boundary."
verification_method = "automated-test-and-security-review"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Present retained evidence content portably

## Rationale

Explorer currently lists evidence paths without the retained evidence itself. A repository-relative path is also not a reachable URL when the static dashboard is published independently through GitHub Pages. Evidence should remain inspectable without manufacturing a GitHub-specific source URL or granting arbitrary repository-file access.

## Preconditions and trigger

This requirement applies to evidence discovered by the governed work-order filename convention and to safe repository evidence paths explicitly referenced by verification records. Only regular UTF-8 files inside the repository's allowed engineering evidence roots are eligible.

## Required response

- Preserve the exact repository-relative evidence path.
- Project deterministic path, size, SHA-256, Markdown content or explicit omission state, and artifact association.
- Render each included document safely in the Evidence tab, with multiple documents individually identifiable and collapsible.
- Produce a collision-resistant, generator-owned raw evidence file inside the dashboard output and link to that local file.
- Keep raw-link names independent of repository-provided path syntax and prevent traversal, overwrite, symlink escape, or active-content execution.
- Record projected and omitted document counts and total projected bytes in generation metadata.
- Make clear that publishing the generated dashboard also publishes every included artifact and evidence body; publication remains a separate explicit action.

## Failure and boundary behavior

Missing, unreadable, unsafe, non-UTF-8, oversized, non-regular, or out-of-root paths retain an explicit unavailable or omitted record. No fallback reads a similarly named file, follows a symlink outside the repository, or silently truncates content.

## Constraints

- No vendor-specific GitHub, GitLab, or hosting URL is inferred.
- Evidence display does not imply that the evidence is sufficient, accepted, verified, or release-eligible.
- Local dashboard generation does not publish or transmit content.
- Content and output budgets must be deterministic and enforced before promotion of the transactional output directory.

## Acceptance examples

### Example: retained Markdown evidence

**Given** an implemented work order has a valid Markdown evidence file,

**When** its Evidence tab is opened,

**Then** the exact path, size, digest, safe rendered content, and local raw link are available.

### Example: unsafe evidence path

**Given** a verification record names a path outside the allowed repository boundary,

**When** the dashboard is generated,

**Then** no outside file is read or copied and the rejected reference is reported explicitly.

## Open decisions

None when approved.
