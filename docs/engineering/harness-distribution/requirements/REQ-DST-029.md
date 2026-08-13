+++
id = "REQ-DST-029"
type = "requirement"
title = "Consume the canonical Explorer snapshot"
status = "implemented"
owners = ["product-owner", "technical-owner"]
created = "2026-08-13"
updated = "2026-08-13"
statement = "WHEN Harness Explorer renders a repository, THE SYSTEM SHALL consume the deterministic harness-dashboard-snapshot-v1 contract directly without introducing a second authoritative or persisted dashboard schema."
verification_method = "automated-contract-test"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Consume the canonical Explorer snapshot

## Rationale

The current generator already produces one deterministic snapshot used by the rendered Explorer and commit-bound verification capture. The WebUI design inputs introduce a different top-level schema, artifact vocabulary, relation shape, and readiness model. Maintaining both would create semantic drift and could make the visual interface disagree with the validator.

## Required response

The rendered interface must use `harness-dashboard-snapshot-v1` as its source contract. Presentation-specific metrics, navigation groupings, bounded lineage views, and labels may be derived in memory by the browser, but they must not be persisted as a competing source of truth or treated as formal authority.

The interface must accept the current canonical sections for repository identity, artifacts, relations, diagnostics, findings, definition coverage, readiness, revision provenance and policy, experiments, and evidence.

## Failure and boundary behavior

An unsupported schema, missing required section, invalid repository, or malformed embedded payload must produce a bounded visible state. The UI must not silently invent defaults that look approved, verified, released, covered, or assessable.

## Acceptance examples

### Example: canonical snapshot

**Given** the generator builds a valid `harness-dashboard-snapshot-v1` payload

**When** it renders Harness Explorer

**Then** the UI reads the existing fields without a second schema conversion file.

### Example: unsupported schema

**Given** an embedded payload identifies another schema

**When** the UI starts

**Then** it reports the unsupported input and grants no lifecycle or readiness meaning.
