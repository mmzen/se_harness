+++
id = "REQ-DST-020"
type = "requirement"
title = "Keep the public README current and technically accurate"
status = "approved"
owners = ["product-owner", "documentation-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"
statement = "WHEN a reader uses the root README to understand or install SE Harness, THE SYSTEM SHALL accurately describe the current released implementation, concepts, terminology, commands, repository structure, and authority boundaries for a 6/10 reader."
verification_method = "automated-test-and-manual-inspection"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Keep the public README current and technically accurate

## Rationale

The README is both the repository entry point and the package-index description. Its overall structure is useful, but parts of its graphs, lineage, gate terminology, and current-state descriptions predate the 0.2.2 architecture and self-hosting boundary.

## Required response

- Preserve the recognizable PyPI-first structure unless a focused structural change demonstrably improves comprehension or removes duplication.
- Synchronize exact-version examples with project metadata.
- Describe the current CLI, installed layout, typed architecture traceability, conditional ADR applicability, commit-bound verification, release behavior, self-hosting separation, and publication boundary accurately.
- Distinguish formal authority, derived validation, repository policy, and illustrative examples.
- Remove obsolete claims rather than retaining them for narrative continuity.

## Failure and boundary behavior

The README must not claim that automation approves, verifies, releases, publishes, configures branch protection, or establishes repository-specific product facts. It must not hide a known implementation-versus-policy discrepancy by describing an unimplemented resolution.

## Constraints

Keep the README useful on GitHub and PyPI, keep local Markdown links valid, and preserve text fallbacks for diagrams. This requirement does not authorize a package version change, build, release, publication, workflow change, or harness behavior change.

## Acceptance examples

A reader following the installation and quick-start commands gets behavior matching the current CLI, and a reader following the conceptual graph sees the same typed relationships defined by current traceability policy.

## Open decisions

None when approved.
