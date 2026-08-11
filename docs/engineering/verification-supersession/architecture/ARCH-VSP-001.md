+++
id = "ARCH-VSP-001"
type = "architecture"
title = "Typed verification-supersession lineage"
status = "implemented"
owners = ["technical-owner", "security-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
constrains = ["SPEC-VSP-001"]
+++

# Architecture: Typed verification-supersession lineage

## Context and scope

VRECs already preserve candidate identity and human lifecycle status, but there is no record-to-record relation for retirement. The architecture extends the existing graph rather than adding a parallel artifact type or an automatic lifecycle service.

## Components and responsibilities

- Formal VREC metadata carries terminal supersession state, target, time, and authorizer.
- The artifact validator enforces shape, type, lifecycle, coverage, cycle, and active-release constraints.
- Provenance release preparation continues to accept only eligible VREC states and never substitutes successors.
- The dashboard generator derives inverse edges, stale-ready warnings, and active-versus-historical classifications.
- Harness Explorer renders the lineage and clearly labels derived observations.
- Canonical templates and workflow documentation carry the same contract into installed repositories.
- Governance review and retained evidence establish authority and compare immutable fields across the transition diff.

## Dependency direction

Authored metadata is consumed by validation. Release preparation depends on validated artifact state. Dashboard projection consumes formal artifacts and validation results. Presentation never feeds authority back into artifacts. Git history supports review but is not a product-authority dependency.

## Data and control flow

Human review -> separate approved governance work order -> bounded VREC lifecycle edit -> formal validation -> governance commit -> dashboard projection. Release selection reads the resulting state but cannot alter or bypass it.

## Trust boundaries

Artifact metadata, relation targets, evidence paths, Git state, and record prose are untrusted inputs. Only an explicit accountable decision retained through governance grants transition authority. Dashboard heuristics are derived hints.

## Required patterns

- Reuse the existing `verification_record` type and relation graph.
- Validate exactly one typed successor and a superset of work coverage.
- Detect cycles deterministically even though current eligible targets are terminal active records.
- Keep historical captured fields immutable through bounded diff review.
- Fail closed when an active release references the source.
- Keep source and canonical installed copies byte-equivalent where managed.

## Prohibited patterns

- Deleting or rewriting historical VRECs.
- Automatically choosing a successor from overlap, timestamps, ancestry, naming, or PR state.
- Treating candidate ancestry as verification equivalence.
- Allowing superseded records to qualify release scope.
- Hiding superseded records or presenting derived warnings as authority.
- Adding a profile, database, network service, or background reconciler.

## Quality attributes

Auditability, deterministic validation, least authority, release safety, backward compatibility, explainability, and customization preservation take precedence over automated convenience.

## Conformance checks

Tests cover all lifecycle shapes, typed targets, coverage sets, cycles, release back-references, immutable transition diffs, dashboard JSON, Explorer snapshots, old-repository compatibility, canonical parity, doctor, wheel contents, and fresh installation.

## Related ADRs

`ADR-VSP-001` selects explicit terminal state plus a typed successor edge on the existing VREC artifact.
