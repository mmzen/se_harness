+++
id = "WO-DST-004"
type = "work_order"
title = "Add canonical layout and safe domain-aware authoring"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
implements = ["REQ-DST-015", "REQ-DST-016", "REQ-DST-017", "REQ-DST-018"]
specifications = ["SPEC-DST-005"]
architecture = ["ARCH-DST-005", "ADR-DST-005"]
verification = ["VER-DST-005"]
+++

# Work Order: Add canonical layout and safe domain-aware authoring

## Objective

Make the canonical per-domain artifact layout systematic for new authoring, co-locate single-domain provenance, and guide legacy repositories without weakening metadata authority or moving owner content automatically.

## In scope

- Central canonical type-to-directory and supporting-path definitions.
- `harnessctl scaffold-domain` with validation, dry-run, conflict safety, failure atomicity, and owner-controlled index seeding.
- `harnessctl create-artifact` with canonical template routing, identifier/type validation, dry-run, exclusive creation, and incomplete-draft messaging.
- Explicit and inferred domain-aware defaults for verification capture and release preparation, preserving output precedence and aggregate roots.
- Nonblocking canonical-path advisories in validation and doctor diagnostics.
- Fresh-install and public guidance, CLI help, installed templates, package metadata inclusion, self-hosted template parity, and managed-lock updates only where the existing ownership model requires them.
- Deterministic unit, integration, security, acceptance, upgrade-preservation, package-parity, graph, diagnostic, and dashboard tests using temporary fixtures.

## Out of scope

- Moving, renaming, rewriting, or otherwise altering any artifact in the active `Mokiterions` repository.
- Automatically migrating owner artifacts in any repository during init, adopt, upgrade, doctor, validate, dashboard, provenance capture, or release preparation.
- Making paths a source of artifact identity, type, relations, lifecycle, approval, verification, or release authority.
- Inferring owners, product statements, requirements, relations, decisions, or approvals.
- New installation profiles, interactive authoring, a schema-level domain field, or changes to the five Explorer questions.
- Package build, version change, release selection, tag, publication, deployment, external configuration, commit, push, or pull request unless separately authorized.

## Authorized decision envelope

After explicit approval of this work order, the implementation agent may choose bounded internal helper names, a deterministic advisory code and wording, and transactional mechanics consistent with `SPEC-DST-005` and `ARCH-DST-005`. It may extend the reserved-name list for demonstrated safety conflicts without rejecting a documented valid slug.

It may not turn the advisory into a validation failure, broaden upgrade ownership, silently normalize unsafe input, overwrite a repository-owned file, infer accountable artifact content, change provenance authority, or touch a live consumer repository as a fixture.

## Expected change surface

CLI entry points and help, provenance path routing, artifact loading and diagnostics, canonical standard templates and managed guidance, installer/package data and lock only where managed, distribution and public documentation, unit and integration tests, acceptance scenarios, and retained evidence.

Historical artifacts, records, releases, package version, workflow pins, and external state are protected surfaces.

## Required verification

Apply every assertion and acceptance scenario in `VER-DST-005`. Run focused authoring, path-security, provenance, compatibility, upgrade, packaging, and guidance tests; the complete Python suite; CLI help; artifact validation; doctor; phase-appropriate preflight; and deterministic dashboard generation.

## Evidence to record

Retain exact commands and results, runtime versions, test counts, changed and protected paths, mapping coverage, adversarial and failure-atomicity results, single- and multi-domain routing, legacy advisory output and exit behavior, graph equivalence, upgrade byte preservation, installed and packaged parity, deviations, and residual risks in `docs/engineering/harness-distribution/evidence/WO-DST-004-verification.md`.

## Stop and escalate conditions

Stop if implementation would require path-based authority, an automatic owner-artifact migration, replacement of existing owner content, a backward-incompatible artifact schema or lock migration, weakening safe-write or provenance controls, changes to a live consumer repository, a new installation profile, or external/release actions not explicitly authorized.

## Current authorization

The accountable user approved this governing chain and bounded implementation on 2026-08-11 with `go for implementation`. This authorizes implementation and local verification within this work order. It does not authorize consumer-repository changes, commits, pushes, pull requests, verification transitions, or release actions.
