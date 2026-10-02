+++
id = "REQ-KIS-012"
type = "requirement"
title = "Publish the review PR before requesting verification"
status = "approved"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"
statement = "For a repository change delivered through a pull request, the agent shall publish the candidate and its ready verification record before requesting the human verification decision, then publish that decision as the final commit before optional merge."
verification_method = ["test", "inspection", "demonstration"]
priority = "must"
source = "mmzen requested PR publication at the verification request, followed by a final verification commit and optional merge, on 2026-10-02."

[relations]
derives_from = ["CAP-KIS-001", "CAP-KIS-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T15:18:37Z"
decided_by = "mmzen"
reason = "mmzen replied \"i approve\" to the reviewed REQ-KIS-012, SPEC-KIS-006, VER-KIS-006 and WO-KIS-013 package, including required commit-bound verification and bounded push/PR updates from work/review-before-verification to main in mmzen/se_harness, on 2026-10-02. This covers implementation, local checks and commits, completion, capture, the review PR and later verification-decision push; human verification and merge remain separate. The installed 0.21.0 evaluator continues to govern this work. Reviewed SHA-256 after recording the confirmed assurance classification: 3e5c75166264230b3a272da0481c9c69fde6016056049044f4a1d9d17c57fb6e"
+++

# Publish the review PR before requesting verification

## In plain words

The owner receives a verification request with a working PR link. The branch
already contains the implementation, evidence and ready verification record.
After the owner verifies the result, the agent records and pushes that decision.
The owner may then merge when the required checks pass.

## Why

A verification request that only links local files excludes an owner who is
away from the workstation. Waiting for verification before publishing the PR
also adds a permission exchange after the review decision.

## Acceptance

1. The work-approval request explicitly includes bounded authority to publish
   the review branch and PR and to push the later verification decision. The
   repository, source branch, target branch and selected work are identified.
   Verification and merge decisions are not included in implementation approval.
2. Before requesting verification, the agent confirms that the remote branch
   and draft PR contain the exact candidate, supporting evidence and ready
   verification record. The request links the PR and remotely readable records.
3. The evaluator offers a review-publication path for a ready record without
   requiring that record to be verified. This path does not authorize merge,
   release or changes outside the selected scope.
4. After the human verifies the unchanged candidate, the agent applies the
   decision and pushes a final commit containing only its verification record
   update. It reuses the publication authority already supplied. It does not
   request verification of this decision-only commit as if it were new work.
5. The draft PR remains unmergeable through the normal draft-PR controls until
   verification is recorded remotely. The agent can then mark the PR ready;
   merge remains an optional human choice, subject to current required checks.
6. Missing publication authority, failed publication or a mismatched remote
   target prevents the verification request. Required evidence failures remain
   blockers. Corrections that change the candidate or evidence require a new
   assessment and the applicable verification-record procedure.

## Limits

This governs PR-based repository work requiring a verification record. It does
not force a PR for read-only discussion, local-only work or release records.
It preserves the concise request defined by REQ-KIS-011 and adds accessible
review before that decision. Existing accepted artifacts and their history
remain unchanged. Release publication and installed adoption are separate work.
