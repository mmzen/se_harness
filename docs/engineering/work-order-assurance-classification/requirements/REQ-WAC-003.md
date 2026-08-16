+++
id = "REQ-WAC-003"
type = "requirement"
title = "Expose pending commit-bound assurance"
status = "implemented"
owners = ["quality-owner", "engineering-owner"]
created = "2026-08-16"
updated = "2026-08-16"
statement = "WHEN an implemented work order explicitly requires commit-bound verification and no active VREC proposal covers it, SE Harness SHALL report non-authoritative assurance follow-up and SHALL cease that follow-up when the lifecycle has progressed to an applicable VREC state."
verification_method = "deterministic inspection queue, suggestion, coverage-state, aggregate, and rendering tests"

[relations]
derives_from = ["CAP-WAC-001"]
+++

# Requirement: Expose pending commit-bound assurance

## Rationale

An implemented work order is no longer active execution, so the existing queues omit it. When commit-bound assurance is explicitly required, absence of a VREC proposal is useful lifecycle attention rather than a formal graph error.

## Required response

- Add a deterministic `assurance_pending` queue for explicitly required implemented work with no covering VREC in `ready`, `verified`, or `released`.
- Treat a superseded VREC as historical, not active coverage.
- When a ready VREC covers the work, rely on the existing assurance-review decision queue instead of reporting both steps.
- When a verified or released VREC covers the work, report no assurance follow-up.
- Group and sort aggregate subjects deterministically and provide a bounded suggested action that preserves human scope selection.

## Failure and boundary behavior

The queue must not create a VREC, select an ID, infer an aggregate candidate, change work-order status, or fail validation by exit status. Missing legacy classification and explicit `not_required` do not enter this queue.

## Constraints

Do not treat implementation completion as correctness, a ready VREC as verified, or a suggestion as authorization.

## Acceptance examples

Four required implemented work orders without VREC coverage appear as assurance pending. One aggregate ready VREC covering all four removes them from that queue and appears once under assurance review.

## Open decisions

None.
