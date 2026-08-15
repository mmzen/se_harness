+++
id = "REQ-DST-034"
type = "requirement"
title = "Keep validation and inspection documentation synchronized"
status = "approved"
owners = ["product-owner", "documentation-owner", "quality-owner"]
created = "2026-08-15"
updated = "2026-08-15"
statement = "WHEN validation or repository-inspection behavior changes, THE SYSTEM SHALL keep the active public command contract, progressive human documentation, and focused documentation checks synchronized with the implemented semantics while preserving historical evidence and accountable authority boundaries."
verification_method = "automated-test-and-manual-inspection"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Keep validation and inspection documentation synchronized

## Rationale

The validator now classifies findings into explanatory assessment planes, and `harnessctl inspect` provides a separate non-gating operational report with bounded suggestions. The concise README and command reference describe those behaviors, but the older active public-documentation contract still limits the ordinary human command surface to five commands and several progressive notes omit `inspect`. A valid graph cannot detect that prose-level contradiction.

Documentation must evolve with the public command surface without rewriting the evidence, VRECs, releases, or Git history that accurately describe earlier candidates.

## Preconditions and trigger

This requirement applies when a released or candidate CLI changes the meaning, inventory, actor boundary, side effects, or exit behavior of an operation presented to repository owners, operators, reviewers, or coding agents.

## Required response

- The ordinary human-facing repository command surface names `init`, `adopt`, `doctor`, `validate`, `inspect`, and `dashboard`.
- `validate` is described as the deterministic gate-oriented check of the formal graph. Its findings retain their error or warning severity and identify the `structure`, `governance`, configured `policy`, or non-blocking `maintenance` plane without producing an aggregate score.
- `inspect` is described as a read-only, non-gating operational report derived from the validator and Harness Explorer snapshot. A successfully produced report may exit zero while showing an invalid graph or attention items.
- Inspection suggestions are described as bounded, deterministic, non-executable, non-automatic, and non-authoritative. They do not approve work, establish eligibility, mutate artifacts, or perform lifecycle transitions.
- The Tier-0 overview, operational phasing, installation and upgrade guide, practical lineage example, concise README, command reference, and managed review workflow remain mutually consistent at their intended reader depth.
- Current active documentation contracts and focused checks are revised when their normative command inventory changes. Historical evidence and commit-bound records remain unchanged and interpretable at their recorded commits.

## Failure and boundary behavior

The documentation must not present `inspect` as a substitute for `validate`, CI, preflight, evidence assessment, or accountable assurance. It must not claim that a zero inspection exit means a valid or verified repository, duplicate the validator rule catalog into explanatory notes, or generate advice for unsupported findings.

A documentation mismatch is reported and corrected through governed work; it is not hidden by weakening tests or by altering historical evidence.

## Constraints

- Preserve the concise root README and route detailed semantics to `docs/notes/`.
- Preserve the distinction between SE Harness guarantees, configurable policy, repository-specific convention, and illustrative guidance.
- Preserve source and canonical managed-document parity where managed files are touched.
- Do not change runtime behavior solely to make documentation easier to state.
- Do not edit historical evidence, VREC, RLS, or released-candidate facts.

## Acceptance examples

### Example: current human command surface

**Given** a repository owner reads the root README and follows the detailed command reference,

**When** they compare routine repository inspection operations,

**Then** both surfaces identify six ordinary commands and distinguish integrity checking, formal validation, operational inspection, and visual exploration.

### Example: invalid graph inspection

**Given** formal validation reports a blocking graph error,

**When** inspection successfully renders the repository report,

**Then** the report retains the invalid state and observations while its successful production is not described as a passed governance gate.

### Example: historical record preservation

**Given** earlier evidence accurately records a five-command README at its candidate commit,

**When** the current documentation contract adds `inspect`,

**Then** current definitions and tests are updated without modifying that earlier evidence or its commit-bound records.

## Open decisions

None when approved.
