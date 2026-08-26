+++
id = "REQ-TST-002"
type = "requirement"
title = "Run the scale tests at full size only under an explicit marker"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-26"
updated = "2026-08-26"
statement = "WHILE the SE_HARNESS_TEST_SCALE environment marker is absent, THE SYSTEM SHALL run the artifact-scale tests at their reduced sizes and SHALL run the one-thousand-artifact size when the marker is present."
verification_method = "automated-test"
[relations]
derives_from = ["CAP-TST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-26T19:18:13Z"
decided_by = "requirements-steward"
+++

# Requirement: Run the scale tests at full size only under an explicit marker

## Rationale

Two tests in `test_workflow_execution` build graphs of 100, 500 and 1,000
artifacts to prove focus and planning scale; together they take 29 seconds
serially and they head the longest class, which sets the parallel floor.
The 1,000 size is the assertion that matters for a release; the smaller
sizes catch a regression on every run.

## Preconditions and trigger

The scale tests run.

## Required response

Sizes 100 and 500 always; 1,000 when `SE_HARNESS_TEST_SCALE=full` (any
other value or absence: not). The hosted `candidate-source` job and the
release qualification set the marker; the local default does not.

## Failure and boundary behavior

The skipped size is reported through `unittest`'s subtest mechanism, not
silently.

## Constraints

The assertions at each size are unchanged.

## Acceptance examples

**Given** no marker **When** the two tests run **Then** they finish in under
6 seconds together and report the 1,000 size as skipped.

## Open decisions

None.
