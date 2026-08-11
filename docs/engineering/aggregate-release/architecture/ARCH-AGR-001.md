+++
id = "ARCH-AGR-001"
type = "architecture"
title = "Aggregate release provenance architecture"
status = "implemented"
owners = ["technical-owner", "security-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
constrains = ["SPEC-AGR-001"]
+++

# Architecture: Aggregate release provenance architecture

## Context and scope

Revision provenance already models relations as arrays, but the CLI preparation boundary is scalar and validation assumes a single work-order-to-verification pairing. This architecture extends the existing model into an aggregate release manifest without introducing parallel record types or weakening exact-commit assurance.

## Components and responsibilities

- CLI parsing collects explicit repeatable values without inferring scope.
- The provenance service resolves typed artifacts, derives the final candidate identity, validates set invariants, and atomically renders one ready record.
- The artifact validator enforces aggregate coverage, lifecycle, type, evidence, and commit consistency for authored as well as generated records.
- The dashboard generator projects complete many-to-one lineage and derived checkout comparison.
- Canonical templates and documentation carry identical behavior into installed repositories.

## Dependency direction

CLI depends on the provenance service. Provenance uses the managed validator and bounded Git observation. Validation depends only on formal metadata and retained repository files. Presentation consumes validated derived data and never grants authority.

## Data and control flow

Explicit IDs -> typed catalog resolution -> set-consistency validation -> clean Git identity and artifact snapshot -> atomic ready verification record -> accountable verification decision -> explicit release selection -> commit and coverage validation -> atomic ready release record -> accountable release decision -> separately authorized tag and publication.

## Trust boundaries

Command arguments, repository artifacts, evidence paths, Git output, and target files are untrusted. Human lifecycle decisions are authoritative only when explicitly recorded. The observed checkout and commit availability are derived context.

## Required patterns

- Use exact set comparisons for verification-contract coverage and released-work coverage.
- Normalize only after rejecting duplicate user input; render sorted arrays deterministically.
- Anchor aggregate assurance at the final integrated candidate commit.
- Reuse existing safe path, Git, timestamp, atomic write, and artifact-type validation.
- Keep candidate commits separate from later governance commits.

## Prohibited patterns

- Inferring work orders from commit ranges, paths, status, branch names, or PRs.
- Treating ancestor commits as equivalent to final-candidate verification.
- Treating all release-contract gates as automatically included work.
- Including publication or approval work as payload merely because it exists in the repository.
- Creating a new installation profile or bypassing customized-file preservation.

## Quality attributes

Auditability, deterministic failure, backward compatibility, least authority, safe migration, and clear human review take precedence over command brevity.

## Conformance checks

Architecture tests exercise multi-item set validation, exact commit agreement, fail-closed atomic behavior, installed-template parity, and complete dashboard lineage. Code review confirms that command handlers do not mutate Git or lifecycle state.

## Related ADRs

`ADR-AGR-001` selects aggregate use of existing record types and a single final-candidate anchor.
