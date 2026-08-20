+++
id = "REQ-DST-055"
type = "requirement"
title = "Keep the initial Explorer payload bounded and observable"
status = "approved"
owners = ["product-owner", "technical-owner", "quality-owner"]
created = "2026-08-17"
updated = "2026-08-19"
statement = "WHEN an Explorer bundle is generated and acceptance-tested, THE SYSTEM SHALL enforce fixed shell and initial-summary budgets, exclude deferred Markdown from the initial path, and report deterministic resource-size measurements without converting them into an assurance score."
verification_method = "automated-performance-budget-test"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Keep the initial Explorer payload bounded and observable

## Rationale

Without explicit structural and byte budgets, later detail features can silently return to the monolithic 2.68 MB HTML design. Repository topology naturally grows with graph size, so the critical path must be bounded without claiming one universal maximum repository size.

## Preconditions and trigger

Generation has produced the complete bundle and the test suite evaluates the current repository plus bounded small, large, and hostile fixtures.

## Required response

The generated output must:

- keep `index.html` at or below 262,144 UTF-8 bytes;
- keep the immediate summary resource at or below 262,144 UTF-8 bytes;
- contain no artifact-body or evidence-body Markdown in `index.html`, summary, topology, or readiness resources;
- retain the existing 262,144-byte per-source-document and 16,777,216-byte total projected-content bounds;
- report every resource byte count plus totals by resource class in generation summary data;
- test the current SE Harness demonstrator topology target at or below 2,097,152 UTF-8 bytes while reporting, rather than misclassifying, larger consumer topology as a repository-governance failure.

## Failure and boundary behavior

Shell, summary, source-document, or total-content hard-budget violation fails generation before output promotion. A topology target regression fails this repository's acceptance test; a larger valid consumer graph remains generatable with explicit size observation and may motivate a separately governed topology-sharding change.

## Constraints

Measurements use deterministic UTF-8 bytes before HTTP compression. Browser timing varies by host and is observational only. No percentage, grade, traffic-light health score, or assurance conclusion is derived from size.

## Acceptance examples

### Example: current demonstrator

**Given** the current SE Harness repository,

**When** its progressive dashboard is generated,

**Then** the shell and summary meet their hard limits, topology meets the repository acceptance target, and no deferred Markdown appears in the initial resources.

### Example: growing consumer graph

**Given** a consumer repository whose compact topology exceeds the demonstrator target,

**When** its dashboard is generated within all hard content limits,

**Then** generation reports the topology size without declaring the formal repository graph invalid.

## Open decisions

None when approved.
