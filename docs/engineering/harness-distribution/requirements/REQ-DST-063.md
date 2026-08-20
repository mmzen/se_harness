+++
id = "REQ-DST-063"
type = "requirement"
title = "Exercise topology capacity on integration history"
status = "approved"
owners = ["quality-owner", "engineering-owner"]
created = "2026-08-20"
updated = "2026-08-20"
statement = "WHEN topology capacity is qualified, THE SYSTEM SHALL exercise the exact branch and pull-request merge histories that contribute revision provenance and SHALL apply the same declared target on supported platforms."
verification_method = "automated-cross-platform-and-hosted-test"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Exercise topology capacity on integration history

## Rationale

Topology contains valid revision-provenance observations. A branch push may therefore remain below the target while GitHub's pull-request merge ref, and later merged `main`, add legitimate history and cross the same target. Qualification that observes only the feature branch misses the integrated product state.

## Preconditions and trigger

A candidate changes the topology acceptance contract or adds formal artifacts and is evaluated locally, on a branch push, or through a pull-request merge ref.

## Required response

- Assert the declared target directly rather than deriving it from the current output size.
- Retain the current-repository acceptance test on the candidate source tree.
- Run hosted candidate-source evidence on the pull-request merge ref before merge.
- Record branch, merge-ref, and resulting merged-main topology bytes when they differ because their valid revision histories differ.
- Apply the same 2,097,152-byte target on Windows and Linux; platform path or line-ending behavior must not select another target.

## Failure and boundary behavior

A branch-only pass does not override a merge-ref failure. A size difference caused by different valid Git history is recorded and assessed against the same target. Unexplained nondeterminism for the same bytes and history remains a failure.

## Constraints

- Verification does not fabricate or rewrite Git history merely to reduce output.
- Revision provenance remains complete and authoritative only to its existing derived-observation boundary.
- Hosted workflow success does not itself approve, verify, or merge a candidate.

## Acceptance examples

### Example: push and merge-ref differ

**Given** a branch push and pull-request merge ref contain the same formal files but different valid merge history,

**When** topology is generated for each,

**Then** both observed byte counts are retained and each is compared with the same 2 MiB target.

### Example: unexplained repeat difference

**Given** identical repository bytes and Git history,

**When** generation runs twice,

**Then** any topology byte or digest difference fails deterministic qualification.

## Open decisions

None when approved.
