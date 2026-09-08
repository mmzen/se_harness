+++
id = "ARCH-AGR-001"
type = "architecture"
title = "Aggregate release provenance architecture"
status = "implemented"
owners = ["technical-owner", "security-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-09-08"

[relations]
addresses = ["REQ-AGR-001", "REQ-AGR-002", "REQ-AGR-003", "REQ-AGR-004", "REQ-AGR-005", "REQ-AGR-006", "REQ-AGR-007", "REQ-AGR-008"]
conforms_to = ["SPEC-AGR-001"]

[decision_assessment]
outcome = "adr_required"
triggers = ["public-interface-or-protocol", "data-ownership-or-persistence", "difficult-to-reverse", "material-alternatives"]
rationale = "ADR-AGR-001 chose one aggregate verification record at the final release candidate over four rejected models. It changed the public record relations, the persisted provenance of every release, and a boundary that published records make hard to reverse."
assessed_by = "technical-owner"
+++

# Architecture: Aggregate release provenance architecture

## Context and scope

Revision provenance already models relations as arrays, but the CLI preparation boundary is scalar and validation assumes a single work-order-to-verification pairing. This architecture extends the existing model into an aggregate release manifest without introducing parallel record types or weakening exact-commit assurance.

## Evidence-keying reassessment

The 2026-08-19 reconciliation of `SPEC-AGR-001` makes the existing keyed-evidence obligation explicit for both flat filenames and components at or below a literal `evidence` directory. Aggregate set coverage, path safety, exact-candidate binding, record structure, dependency direction, and human authority remain unchanged. The package and repository-local assurance planes retain independent predicates aligned by contract tests under `SPEC-EVK-001`.

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

## Amendment record

**Typed `addresses` and `conforms_to` relations replace the legacy
`constrains` relation and a decision assessment is recorded, amended
2026-09-08 under `WO-AUT-005` (`SPEC-AUT-003`, `ADR-AGR-001`).** The legacy
relation named only `SPEC-AGR-001`, which becomes the conformance target;
`addresses` takes the eight requirements that specification specifies, all of
them active. The assessment reads the drivers and rejected options of
`ADR-AGR-001`, the one active ADR that decides this architecture. Title,
status, statement and ADR relations are unchanged.
