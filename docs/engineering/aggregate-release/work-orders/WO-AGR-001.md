+++
id = "WO-AGR-001"
type = "work_order"
title = "Implement aggregate verification and release manifests"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
implements = ["REQ-AGR-001", "REQ-AGR-002", "REQ-AGR-003", "REQ-AGR-004", "REQ-AGR-005", "REQ-AGR-006", "REQ-AGR-007", "REQ-AGR-008"]
specifications = ["SPEC-AGR-001"]
architecture = ["ARCH-AGR-001", "ADR-AGR-001"]
verification = ["VER-AGR-001"]
+++

# Work Order: Implement aggregate verification and release manifests

## Authorization

The accountable repository owner explicitly approved this bounded implementation on 2026-08-11 with the instruction `ok, perform the change` after reviewing the draft artifact packet. The authorization covers implementation and verification only; it does not authorize a commit, push, pull request, verification transition, release record, tag, publication, or deployment.

## Objective

Extend existing commit-bound provenance so one final candidate and one version can explicitly cover multiple release-bearing work orders without weakening exact-commit assurance, human decision rights, or single-item compatibility.

## In scope

- Repeatable aggregate inputs for verification capture and release preparation.
- Deterministic rendering of list-valued record metadata and relations.
- Aggregate contract, evidence, work coverage, lifecycle, type, and commit validation.
- Complete aggregate provenance and readiness projection in the dashboard and Explorer.
- Canonical standard-template, workflow, schema, CLI-help, and user documentation updates.
- Safe upgrade behavior, deterministic unit and end-to-end tests, wheel-content and fresh-install verification, and retained evidence.

## Out of scope

- Selecting the actual work scope for version 0.2.0.
- Creating or approving a VREC or RLS for a product version.
- Changing historical verification records or treating different ancestor commits as final verification.
- Inferring release scope from Git, paths, pull requests, artifact status, or naming.
- Creating commits, tags, pushes, pull requests, releases, packages, deployments, or lifecycle transitions.
- Adding installation profiles or external runtime services.

## Authorized decision envelope

After explicit approval, the implementation agent may choose bounded collection helpers, deterministic formatting, diagnostic wording, and test fixture structure consistent with `SPEC-AGR-001`. It may not change authority semantics, relax exact-commit or path safety, or infer product scope.

## Constraints

Preserve the single standard installation, Python 3.11 compatibility, standard-library runtime, atomic non-overwrite, customization preservation, existing record compatibility, and the candidate-then-governance sequence.

## Expected change surface

CLI argument handling, provenance preparation, formal validation, dashboard projection and Explorer rendering, canonical installed-template copies, artifact templates and workflow guidance, tests, packaging verification, and retained evidence.

## Required verification

Execute `VER-AGR-001`, the repository artifact validator, the complete unit suite, CLI help and doctor checks, deterministic dashboard generation, temporary Git end-to-end scenarios, init/adopt/upgrade compatibility, and a fresh installation from the built wheel.

## Evidence to record

Retain exact commands, results, requirement mapping, aggregate success and rejection cases, changed-file parity, deviations, residual risks, and manual Explorer observations in `docs/engineering/aggregate-release/evidence/WO-AGR-001-verification.md`.

## Stop and escalate conditions

Stop if aggregate scope requires inference, different candidate commits must be treated as equivalent, existing records would become invalid, customized files would be overwritten, a new authority transition is implied, or safe deterministic set mapping cannot be expressed without a schema decision.

## Completion report format

Report implemented requirements, exact verification commands and outcomes, candidate commit only after separately authorized creation, deviations, residual risks, and explicitly excluded release actions.

This work order is approved for the bounded implementation and verification described above.
