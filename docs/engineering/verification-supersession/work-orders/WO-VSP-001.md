+++
id = "WO-VSP-001"
type = "work_order"
title = "Implement verification-record supersession"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
implements = ["REQ-VSP-001", "REQ-VSP-002", "REQ-VSP-003", "REQ-VSP-004", "REQ-VSP-005", "REQ-VSP-006", "REQ-VSP-007"]
specifications = ["SPEC-VSP-001"]
architecture = ["ARCH-VSP-001", "ADR-VSP-001"]
verification = ["VER-VSP-001"]
+++

# Work Order: Implement verification-record supersession

## Authorization

The accountable repository owner validated this artifact packet and explicitly authorized its bounded implementation on 2026-08-11 with the instruction `go implementation`. This authorizes implementation and verification only; it does not authorize superseding a concrete VREC, committing, pushing, opening a pull request, creating a release or tag, publishing, or deploying.

## Objective

Add an explicit, typed, release-safe, and visible lifecycle for superseding stale ready verification records while preserving commit-bound history and human authority.

## In scope

- Verification-record `superseded` status and structured transition metadata.
- Typed `superseded_by` validation, target eligibility, coverage preservation, and cycle detection.
- Active-release back-reference and release-preparation exclusion rules.
- Derived stale-ready findings and complete dashboard/Explorer supersession projection.
- Workflow, traceability, VREC template, user documentation, and canonical installed-template updates.
- Deterministic validator, provenance, dashboard, Explorer, compatibility, upgrade, wheel, and fresh-install tests.
- Retained implementation evidence keyed to this work order.

## Out of scope

- Transitioning `VREC-AGR-001` or any concrete VREC.
- Automatically selecting or applying a successor.
- Superseding verified or released VRECs, RLS records, requirements, or other artifact types.
- Resolving active release records that reference a source VREC.
- Creating commits, tags, pushes, pull requests, releases, packages, publications, or deployments without separate authorization.
- Adding installation profiles, runtime dependencies, databases, or network services.

## Authorized decision envelope

After explicit approval, implementation may choose internal graph helpers, diagnostic wording within the specified codes and severity, indexes, JSON field placement, Explorer layout details, and fixture organization. It may not change lifecycle eligibility, authority, successor cardinality, coverage, release safety, immutability, or compatibility rules.

## Constraints

Preserve one standard installation, Python 3.11 compatibility, standard-library runtime, deterministic output, path and symlink safety, atomic non-overwrite, customized-file preservation, source/canonical parity, and commit-bound provenance sequencing.

## Expected change surface

Formal artifact validation, provenance release selection, dashboard normalization and findings, Explorer rendering, workflow and traceability guidance, VREC templates, canonical standard installation, managed lock entries, tests, packaging verification, and evidence.

## Required verification

Execute `VER-VSP-001`, artifact validation, the complete unit suite, CLI help, source doctor, deterministic dashboard generation, source/canonical parity, init/adopt/upgrade compatibility, wheel inspection, and a fresh installation. Review the known `VREC-AGR-001`/`VREC-PMI-001` graph as a non-mutating fixture or derived dashboard case.

## Evidence to record

Retain exact commands, results, requirement mapping, valid and invalid lifecycle matrices, coverage and cycle cases, release back-reference cases, dashboard snapshots, visual review, compatibility results, wheel checksum, deviations, platform limitations, and residual risks in `docs/engineering/verification-supersession/evidence/WO-VSP-001-verification.md`.

## Stop and escalate conditions

Stop if safe behavior requires automatic authority, deletion or rewrite of historical metadata, superseding an active-release input, weakening exact-commit assurance, changing the first transition beyond `ready -> superseded`, overwriting customized files, or introducing a new artifact type or external service.

## Completion report format

Report implemented requirements, exact verification results, compatibility behavior, dashboard treatment, deviations, residual risks, and explicitly excluded governance actions. Identify a candidate commit only after separate commit authorization. Do not claim that any concrete VREC was superseded.
