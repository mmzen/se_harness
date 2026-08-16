+++
id = "REQ-IAR-018"
type = "requirement"
title = "Report only actionable temporal reassessment observations"
status = "implemented"
owners = ["repository-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"
statement = "WHEN repository inspection compares artifact update dates, SE Harness SHALL report temporal reassessment only for explicitly supported declared dependency relations whose source remains meaningfully reassessable."
verification_method = "Automated predicate, lifecycle, relation-authority, compatibility, determinism, distribution, and regression tests"

[relations]
derives_from = ["CAP-IAR-001"]
+++

# Requirement: Report only actionable temporal reassessment observations

## Lifecycle

Approved on 2026-08-16 through the repository owner's instruction to create a branch and implement the reviewed Phase 1 correction.

## Problem

The current `W-HEX-003` implementation treats every older relation source as stale when its target has a newer `updated` date. This produces misleading reassessment advice for completed work orders, immutable verification and release records, supersession lineage, and derived graph projections. Those artifacts record history; their dates do not create a new action merely because a related definition changed later.

## Required outcome

- Restrict temporal comparison to an explicit catalog of declared dependency relations with a defined reassessment meaning.
- Keep living definitions eligible while excluding inactive definitions.
- Keep work orders eligible only while work can still be defined or executed; completed work remains historical.
- Exclude verification records and release records from this generic rule because their commit-bound provenance requires dedicated checks.
- Preserve `W-HEX-003`, inspection's non-authoritative suggestion boundary, validator behavior, and read-only operation.
- Identify the relation that caused each observation so its meaning can be reviewed.

## Acceptance criteria

1. An older active architecture that declares conformance to a newer specification emits `W-HEX-003`.
2. An older non-terminal work order with a supported dependency may emit the finding.
3. Implemented, verified, released, rejected, or superseded work orders do not emit the generic finding.
4. Verification records, release records, `superseded_by` relations, derived relations, and unknown extension relations do not emit it.
5. Rejected or superseded definition artifacts do not emit it.
6. The finding preserves derived, warning-only authority, includes the declared relation name, and continues to map to the existing non-automatic suggestion.
7. Repeated generation and inspection remain deterministic, read-only, and compatible with Python 3.11+ and standard distribution.

## Deferred questions

Dedicated provenance observations for verification records or release records, configurable reassessment catalogs, aging thresholds, automatic remediation, and changes to historical architecture artifacts remain separately governed work.

## Authority boundary

A date comparison is an attention signal only. It does not establish invalidity, require an artifact edit, reopen completed work, weaken commit-bound provenance, authorize a transition, or perform maintenance.
