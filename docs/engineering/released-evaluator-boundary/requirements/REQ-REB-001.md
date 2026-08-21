+++
id = "REQ-REB-001"
type = "requirement"
title = "Reject non-released runtimes before installed-root mutation"
status = "approved"
owners = ["requirements-steward", "security-owner", "technical-owner"]
created = "2026-08-21"
updated = "2026-08-21"
statement = "WHEN an installed repository lifecycle operation would write managed controls or formal lifecycle state, THE SYSTEM SHALL prove that the invoking runtime matches the repository's locked released-evaluator identity and SHALL reject any candidate, missing, or ambiguous identity before the first write."
verification_method = "automated-boundary-and-failure-test"

[relations]
derives_from = ["CAP-REB-001"]
+++

# Requirement: Reject non-released runtimes before installed-root mutation

## Rationale

Issue #81 was detected only after candidate tooling had already participated in root lifecycle work. A pre-write identity boundary moves detection to the first potentially authoritative mutation and makes failure recoverable by construction.

## Preconditions and trigger

The target is already a standard installed repository with a readable managed configuration and lock, and the selected operation can change managed files, formal artifacts, verification records, release records, or structured identifiers.

## Required response

- Resolve the configured and locked evaluator version and distribution identity.
- Inspect runtime role, installed distribution, module, templates, executable, entry point, user-site state, `PYTHONPATH`, and checkout boundary.
- For ordinary mutations, require exact agreement with the current lock.
- For an upgrade apply, require the separately selected already-published target evaluator and a valid old-root integrity state.
- Complete every check before opening a write transaction.

## Failure and boundary behavior

Missing lock data, candidate-source fallback, editable source, candidate wheel digest, wrong version, origin ambiguity, user-site contamination, `PYTHONPATH` contamination, or checkout-bound execution fails with a bounded diagnostic and no target change. Read-only plans may describe the blocked condition but grant no authority.

## Constraints

- Initial `init` and `adopt` do not have a prior installed identity and follow their existing conflict-safe installation boundary.
- A command name, version string, caller-supplied role, or unverified digest is insufficient proof.
- Direct public mutation APIs must not bypass the same guard used by the CLI.

## Acceptance examples

### Example: normal behavior

**Given** an installed root locked to an exact public evaluator wheel and an isolated environment installed from those bytes

**When** an authorized actor creates a draft artifact

**Then** identity proof passes before the exclusive file create begins.

### Example: failure behavior

**Given** candidate source with the same displayed version as the lock

**When** it attempts `create-artifact`, `capture-verification`, or another installed-root mutation

**Then** the operation fails before writing and a recursive byte snapshot of the target remains unchanged.

## Open decisions

The technical owner must accept the standard lock identity and upgrade-migration design in `ADR-REB-001` before this requirement can become approved.
