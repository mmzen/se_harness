+++
id = "REQ-EVK-004"
type = "requirement"
title = "Keep evidence keying portable and independently assessable"
status = "approved"
owners = ["technical-owner", "security-owner", "quality-owner"]
created = "2026-08-19"
updated = "2026-08-19"
statement = "WHEN evidence paths are assessed on supported platforms or across installed-package and repository-local execution planes, THE SYSTEM SHALL produce deterministic platform-independent key sets without making standalone repository scripts depend on candidate package code."
verification_method = "automated-test-and-architecture-review"

[relations]
derives_from = ["CAP-EVK-001"]
+++

# Requirement: Keep evidence keying portable and independently assessable

## Rationale

The package prepares records while managed repository-local scripts validate and project repository state. Those planes intentionally have different deployment and assurance boundaries. Observable parity is required, but importing candidate package code into standalone validation would weaken the boundary.

## Preconditions and trigger

Equivalent normalized path strings are assessed on Windows and POSIX-compatible Python runtimes, or by the installed package and managed repository-local tools.

## Required response

- Interpret metadata paths with platform-independent repository-relative component semantics.
- Return unique keys and associations in deterministic lexical order.
- Reuse one repository-local predicate for validation, inspection, and Explorer.
- Keep the installed package implementation independent and prove parity through a shared contract-case matrix.

## Failure and boundary behavior

Platform path parsing may not change the key set. Repository-local scripts must stop rather than import unavailable or candidate-controlled package behavior. Contract-case disagreement fails verification.

## Constraints

- Repository-local validation remains Python 3.11+ standard-library-only.
- The dashboard may depend on the managed validator it already imports, but neither may import `se_harness` from the target checkout.
- Candidate code never substitutes for released-governor assurance.

## Acceptance examples

### Example: cross-platform path

**Given** `docs/engineering/x/evidence/WO-ABC-001/check.md`,

**When** supported Windows and POSIX runtimes assess it,

**Then** both return exactly `WO-ABC-001`.

### Example: execution-plane parity

**Given** the shared positive and negative case table,

**When** package and repository-local helpers execute it,

**Then** their complete ordered results are equal.

## Open decisions

None when approved.
