+++
id = "REQ-DPG-001"
type = "requirement"
title = "Publish an immutable release-bound dashboard"
status = "implemented"
owners = ["repository-owner", "release-owner"]
created = "2026-08-16"
updated = "2026-08-18"
statement = "WHEN publication is requested for a completed SE Harness release, THE SYSTEM SHALL deploy an Explorer generated from one validated immutable governance commit whose released record and candidate commit match the published Git tag."
verification_method = "automated-provenance-and-deployment-test"

[relations]
derives_from = ["CAP-DPG-001"]
+++

# Requirement: Publish an immutable release-bound dashboard

## Rationale

The release tag points to the software candidate, while the completed governance graph exists in a later commit that contains the released release record. Publishing the tag checkout alone would omit verification and release decisions; publishing a moving branch head could include unrelated later work. The demonstration needs both identities and must not blur them.

## Preconditions and trigger

Normal publication starts inside the main-context released-record orchestrator after the exact GitHub Release is final. A separate main-only action supports an explicitly authorized Pages replay. In both paths, the matching formal release record must be `released`, its recorded tag must resolve to its recorded candidate commit, and the governance snapshot must be a full immutable commit reachable from the repository's main integration history.

## Required response

- Resolve exactly one released record for the selected GitHub Release tag.
- Resolve the immutable governance commit that first integrated that released record into the main history, or accept an explicit full governance commit for a controlled replay.
- Verify the release record, Git tag, candidate commit, object format, version, and governance commit before generation.
- Validate the checked-out governance repository, then generate the canonical Explorer from that exact clean checkout.
- Expose release, candidate, and observed governance provenance in the deployed snapshot and workflow summary.

## Failure and boundary behavior

Missing, ambiguous, mutable, dirty, invalid, unreachable, or mismatched provenance must fail before upload or deployment. A failed run must leave the last successful Pages deployment intact and must not manufacture a successful release or verification state.

## Constraints

The published dashboard is derived demonstration output. It does not become commit-bound evidence and does not modify the release record, tag, VREC, repository history, or source branch.

## Acceptance examples

### Example: completed release

**Given** `v0.4.0` resolves to the candidate recorded by released `RLS-SEH-006`

**When** the publication resolves the immutable main-history commit that integrated that released record

**Then** it generates and deploys the Explorer from that governance commit and reports both commit identities.

### Example: tag mismatch

**Given** a selected release record names a candidate commit different from the Git tag target

**When** publication runs

**Then** it fails before a Pages artifact is uploaded.

## Open decisions

None. The implementation may choose a bounded Git-history query, but it must produce a unique immutable result or stop.
