+++
id = "WO-WAC-001"
type = "work_order"
title = "Implement explicit work-order assurance classification"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "quality-owner", "security-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[assurance]
commit_bound_verification = "required"
rationale = "The candidate changes governed metadata, validation, preflight, inspection, managed policy, and consumer distribution behavior relied upon by future engineering and assurance decisions."
decided_by = "repository-owner"

[relations]
implements = ["REQ-WAC-001", "REQ-WAC-002", "REQ-WAC-003", "REQ-WAC-004", "REQ-WAC-005"]
specifications = ["SPEC-WAC-001"]
architecture = ["ARCH-WAC-001", "ADR-WAC-001"]
verification = ["VER-WAC-001"]
+++

# Work Order: Implement explicit work-order assurance classification

## Lifecycle and authorization

The repository owner agreed with the proposed applicability rule and requested this artifact packet plus a supporting implementation branch on 2026-08-16. After reviewing the complete packet, the owner instructed `ok go`, approving the definition chain and authorizing implementation of this exact work order. The work order explicitly requires commit-bound verification because future engineering and assurance decisions will rely on the changed governed metadata, validation, preflight, inspection, policy, and consumer distribution behavior.

## Objective

Make VREC applicability explicit, enforce it at the work boundary, and expose missing commit-bound assurance as useful non-authoritative inspection follow-up without creating recursive governance or rewriting legacy artifacts.

## In scope

- Implement the exact `SPEC-WAC-001` metadata, lifecycle, preflight, inspection, compatibility, and authority rules.
- Add the declaration and decision guidance to the canonical managed work-order template and policy.
- Version and document the inspection JSON contract when adding `assurance_pending`.
- Synchronize canonical and active managed files through the supported self-hosting workflow.
- Add focused and full regression coverage defined by `VER-WAC-001`.
- Update concise operator and agent documentation without copying policy sections into notes.
- Retain exact implementation evidence keyed to `WO-WAC-001`.

## Out of scope

Bulk classification of historical work orders; modifying existing VREC, RLS, REL, OPS, or release artifacts; evidence-completeness enforcement; automatic VREC scope selection or creation; work-order status mirroring; release redesign; branch inference; general artifact-schema versioning; package version changes; release, tag, publication, or deployment.

## Authorized decision envelope

After approval, implementation may choose helper names, exact bounded string limits consistent with existing metadata controls, deterministic internal indexes, and focused fixture organization. It may not change the two classification values, infer missing decisions, weaken decision rights, add an automatic action, broaden legacy migration, or alter provenance and release eligibility.

## Constraints

- Canonical-first managed changes and supported reconciliation are mandatory.
- The released governor remains the CI authority; candidate source and package tests exercise the new behavior without governing themselves.
- Every existing completed work order, current VREC, release record, and repository-owned declaration remains untouched unless explicitly listed in a later approved amendment.
- The inspector remains read-only and non-gating.

## Expected change surface

- Root and canonical work-order template and managed workflow documentation.
- Root and canonical artifact validator and inspector.
- Preflight command implementation and command/documentation surfaces.
- Managed lock and reconciliation outputs produced through supported tooling.
- Focused validator, preflight, inspection, distribution, package, upgrade, documentation, and regression tests.
- This domain index, work order, and retained evidence.

## Required verification

Execute the complete `VER-WAC-001` matrix, formal validation, doctor, start and review preflight, deterministic inspection, root/canonical parity, supported Python 3.11 and current-environment suites, complete tests, fresh installation, safe upgrade, candidate package checks, changed-path audit, and `git diff --check`.

## Evidence to record

Record before/after queue behavior, every lifecycle and VREC coverage case, exact diagnostics, inspection schema and hashes, managed reconciliation, installation and upgrade outcomes, test counts and skips, deviations, and residual human-classification risk.

## Stop and escalate conditions

Stop if implementation requires date/title/path inference, bulk historical edits, a new artifact type, automatic VREC construction, release-policy weakening, an unauthenticated role claim presented as authentication, candidate code governing itself, or a change outside the accepted classification and inspection boundary.

## Completion report format

Report the final data contract, lifecycle enforcement, inspection state matrix, compatibility behavior, managed-distribution changes, exact checks, changed paths, deviations, and residual risks. Stop at an uncommitted `implemented` candidate unless separately authorized.
