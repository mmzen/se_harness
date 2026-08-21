+++
id = "REQ-REB-002"
type = "requirement"
title = "Resolve publication evaluators from the standard installation"
status = "approved"
owners = ["requirements-steward", "release-owner", "security-owner"]
created = "2026-08-21"
updated = "2026-08-21"
statement = "WHEN a release or release-bound Explorer workflow evaluates a governance snapshot, THE SYSTEM SHALL resolve and verify the exact released evaluator from the snapshot's standard configuration and lock without consulting a special self-hosting descriptor, profile, or role."
verification_method = "automated-workflow-contract-and-integration-test"

[relations]
derives_from = ["CAP-REB-001"]
+++

# Requirement: Resolve publication evaluators from the standard installation

## Rationale

Current publication code still invokes retired governor interfaces that the standard 0.5.0 CLI no longer supports and reads a descriptor deliberately removed from the root. One standard resolver prevents the restored publisher from recreating the incident boundary or failing at dispatch time.

## Preconditions and trigger

A trusted main or immutable governance snapshot contains `.engineering-harness.toml`, `.engineering-harness.lock`, and a selected release record or release-bound Pages request.

## Required response

- Resolve exact evaluator version, wheel filename, and SHA-256 from standard installation data.
- Acquire the exact immutable wheel through the accepted public distribution boundary.
- Verify the downloaded bytes before installation.
- Install outside the checkout, prove the `released-evaluator` runtime role, and validate the snapshot with that environment.
- Use the same resolver in PyPI publication and release-bound Pages workflows.

## Failure and boundary behavior

Missing or inconsistent standard identity, an unavailable immutable wheel, digest mismatch, unsupported CLI contract, checkout fallback, or an unexpected active legacy descriptor fails the workflow before candidate promotion or Pages deployment.

## Constraints

- The resolver does not infer authority from a version string or network response alone.
- Repository-specific publication remains outside the portable consumer template, but it consumes the same standard evaluator identity contract.
- No long-lived descriptor duplicating standard lock ownership may be introduced.

## Acceptance examples

### Example: normal behavior

**Given** a governance snapshot whose standard lock selects public evaluator 0.5.0 and its exact wheel digest

**When** the one-input publisher resolves release authority

**Then** it downloads, hash-checks, installs, and invokes 0.5.0 with `--role released-evaluator` before validating the snapshot.

### Example: failure behavior

**Given** an active workflow that passes `--role governor` or reads `.self-hosting/governor.toml`

**When** the workflow contract test runs

**Then** the candidate fails as an active retired-interface regression.

## Open decisions

The accepted distribution source and standard lock representation are decided by `ADR-REB-001`.
