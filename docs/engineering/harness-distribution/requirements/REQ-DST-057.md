+++
id = "REQ-DST-057"
type = "requirement"
title = "Use one released evaluator in consumer CI"
status = "implemented"
owners = ["product-owner", "technical-owner", "security-owner", "quality-owner"]
created = "2026-08-17"
updated = "2026-08-17"
statement = "WHEN consumer CI evaluates a governed revision, THE SYSTEM SHALL install one exact declared released SE Harness version in an isolated environment and use that runtime for every SE Harness check without a second bootstrap version."
verification_method = "automated-workflow-and-runtime-identity-test"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Use one released evaluator in consumer CI

## Rationale

A consumer repository is not developing SE Harness. Its requested evaluator is already an external released package, so a second older runtime that validates only itself adds latency and conceptual ambiguity without assessing the consumer repository.

## Preconditions and trigger

GitHub starts the managed consumer workflow for a push or pull request. The workflow declares the exact SE Harness distribution version rendered by the standard installation.

## Required response

- Create one runner-temporary virtual environment outside the checkout.
- Install the exact declared `se-harness` wheel version, binary-only and without transitive runtime dependencies.
- Prove that the installed version equals the declared version and that its executable package origin is outside the checkout.
- Use only that environment for all SE Harness CI commands.
- Keep the implementation repository's independently released governor and candidate planes unchanged and explicitly outside the consumer contract.

## Failure and boundary behavior

Missing distribution, version disagreement, source import from the checkout, unsupported runtime, installation failure, or evaluator identity ambiguity fails the workflow before repository assessment. The workflow never falls back to a globally installed CLI, checkout source, or an older bootstrap evaluator.

## Constraints

- The exact version is visible in the generated workflow and equals the distribution version used to render it.
- PyPI package acquisition remains the simple consumer default; stronger artifact attestation may be added only through separately governed work.
- One consumer evaluator does not collapse the special self-hosting authority boundary.

## Acceptance examples

### Example: ordinary consumer

**Given** a standard installation rendered by SE Harness 0.4.0,

**When** GitHub evaluates the repository,

**Then** one isolated `se-harness==0.4.0` runtime performs the complete harness assessment.

### Example: checkout attempts import shadowing

**Given** the checkout contains a misleading `se_harness` package path,

**When** runtime identity is checked,

**Then** the workflow fails rather than treating checkout code as the released evaluator.

## Open decisions

None when approved.
