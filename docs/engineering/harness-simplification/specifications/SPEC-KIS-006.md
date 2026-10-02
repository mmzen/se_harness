+++
id = "SPEC-KIS-006"
type = "specification"
title = "Review publication before human verification"
status = "approved"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"
contract = "For PR-based work, publish a reviewable candidate before requesting verification and publish only the recorded verification decision afterward."

[relations]
specifies = ["REQ-KIS-012"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T15:18:37Z"
decided_by = "mmzen"
reason = "mmzen replied \"i approve\" to the reviewed REQ-KIS-012, SPEC-KIS-006, VER-KIS-006 and WO-KIS-013 package, including required commit-bound verification and bounded push/PR updates from work/review-before-verification to main in mmzen/se_harness, on 2026-10-02. This covers implementation, local checks and commits, completion, capture, the review PR and later verification-decision push; human verification and merge remain separate. The installed 0.21.0 evaluator continues to govern this work. Reviewed SHA-256 after recording the confirmed assurance classification: faa5480f6bb789f9ba807058cd56d86f8e18f192b35bba3a9e972b8ff4b3d6ad"
+++

# Review publication before human verification

## Scope

This specification governs PR-based repository work with required commit-bound
verification. Reuse the existing work approval, candidate capture, human
verification and repository integration operations. The new ordering applies
when the selected work is to be delivered through a PR. Local-only work,
work classified as requiring no new verification record, release publication
and adoption keep their applicable procedures.

## Sequence

1. Obtain approval for implementation and the explicitly described review
   publication actions.
2. Implement the work, run its checks and prepare a ready verification record.
3. Push the review branch and open or update its draft PR.
4. Confirm the remote content, then request human verification with the PR link.
5. Apply the human's verification decision to the selected record.
6. Commit and push that record update as the final commit.
7. Mark the PR ready after confirming the pushed decision. Report required
   CI results for the final head. The owner may merge when its checks permit it.

## Rules

**KIS-PRV-001.** Make publication authority explicit. The work-approval request
for this path names the selected work orders, destination repository, source
branch and target branch. It explicitly requests authority to push the bounded
work and evidence, create or update one review PR, and push the later human
verification decision to that same branch. It also covers marking that PR
ready after the verified decision is present remotely.

Use one approval exchange with clear wording such as "Approve implementation
and review publication." Keep the work approval and publication grant distinct
within that reply. Ordinary implementation approval, silence and passing
tests do not imply the publication grant. Preserve the actual decision in
the existing work-order decision envelope and transition reason; do not add
an authority file or receipt type.

The candidate commit is not known when work is approved. Before each external
operation, resolve and check its exact full commit against the approved work,
branch, destination and current gates. This is bounded authority for the
described work, not permission to publish arbitrary later commits. Preserve
provider controls and independently enforced restrictions.

Historical approvals keep their meaning. Reuse matching publication authority
already supplied. Obtain only a missing grant, before publication. Changed
scope or destination requires its own authority. Merge, force-push, release,
tagging, deployment and unrelated work are excluded.

**KIS-PRV-002.** Publish a reviewable result first. Complete the applicable
local checks and capture the ready VREC through the selected released evaluator.
Commit the generated ready record and required generated evidence. Push that
review head and create or update the selected draft PR under the existing grant.

The captured candidate and the review branch head are different identities:
the latter also contains the subsequently prepared verification record.
Preserve the candidate recorded by capture. Check that the later commits add
only the expected record and its preparation material, not new implementation
or changed bound evidence. Do not claim that a record is captured against a
commit which contains itself.

Use the existing PR body and complete-scope checks. State "verification
pending" in the PR and link the candidate, ready record, assessment and evidence.
Retain the work-order declaration. Do not invent a successful assurance result.

Read back the hosting service's PR URL, head repository, source and target
branches, head commit and draft status. Confirm the ready record and evidence
are available at that head to the intended owner. Use immutable links for the
review details. If the same correct PR already exists, reuse it.

**KIS-PRV-003.** Expose the legal review path. The evaluator must offer a
bounded review-publication procedure for a ready VREC. It must not require
verified coverage to publish that review package. Use existing applicable
graph, integrity, scope, record and provider checks.

Keep the existing verified-coverage requirement on the integration or merge
path. Review publication selects no lifecycle transition and grants no human
verification, merge or release authority. Map the review procedure and the
verification decision's PR prerequisite to the appropriate on-demand
instructions. An agent following the PR path must complete and confirm
publication before presenting the human verification request.

Keep existing record states, decision rights and command meanings. A workflow
procedure and its reading prerequisites are sufficient: use the ordinary Git
and hosting tools for publication. Do not add a network dependency to every
VREC transition, a hosting client to the evaluator, a new artifact type, or a
permanent receipt schema solely to track this step. Tests must distinguish
evaluator routing from the provider readback performed by the agent.

**KIS-PRV-004.** Request verification with accessible evidence. Preserve the
concise request in SPEC-KIS-005. Add the PR URL prominently and include remote
links to the ready record, exact candidate, assessment and evidence. Report the
observed CI status truthfully. Required verification checks must pass before
acceptance is offered; a CI run still in progress is not a pass.

Only request verification after the matching remote review package exists.
A local path, intended push or unconfirmed provider response is insufficient.
If authority, publication, access or readback is missing, report that blocker
and the recovery action. Do not solicit acceptance of inaccessible material
as a substitute for completing publication.

**KIS-PRV-005.** Push the decision as the final commit. Bind the human reply
to the displayed VREC, candidate and evidence. Preview, apply and read back the
existing verification transition. Commit only the selected VREC state and
lifecycle event changes, then push that final decision commit to the same PR.
Reuse the explicit decision-publication grant; do not ask for a second push/PR
approval when its bounds still match.

Confirm the remote head and recorded decision before marking the PR ready.
Describe the final commit as recording acceptance of the earlier captured
candidate, not as a new implementation candidate. Do not recapture verification
merely because this decision-only commit exists. Required checks still run
against the final PR head. Being ready is not permission for the agent to merge;
the human decides whether to merge.

For an aggregate review, one final commit may update the exact selected VRECs.
Do not include implementation, evidence changes, unrelated artifacts or other
lifecycle transitions in that commit.

**KIS-PRV-006.** Preserve corrections and recovery. A requested correction
leaves the PR in draft and the verification decision pending. Use eligible
work authority for corrections. Changes to implementation, governing inputs
or bound evidence require reassessment and the applicable capture or refresh
procedure before a new request. Do not restart a completed work order or
reuse verification for changed inputs.

A failed final push leaves the local decision recorded but not delivered.
Report that distinction and inspect the remote before retrying. Do not
reapply an already recorded decision, force-push, duplicate a PR, or mark it
ready while delivery is uncertain. If work changes after verification, the
old decision-only final commit no longer qualifies the changed candidate.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-KIS-012 | KIS-PRV-001, KIS-PRV-002, KIS-PRV-003, KIS-PRV-004, KIS-PRV-005, KIS-PRV-006 |

## Design choice and enforcement boundary

The current PR checker already admits approved or implemented work without
verified coverage. The current workflow only offers its repository integration
path after verification. Add a specific review-publication path and reorder
the instructions instead of weakening the integration gate.

Draft PRs provide the normal hosting barrier to premature merge. Instructions
require live readback and the authorized actor applies the decisions. The
evaluator validates local lifecycle, scope and gates; it does not independently
authenticate a human or prove remote visibility. Do not describe these
instructions as an unbypassable host-side merge policy.

Reuse the existing approval and verification cards, state transitions, Git
tools and PR controls. No new service, scheduler, persistent approval object,
startup instruction load or verification state is needed. This is a workflow
policy change within the existing architecture. No active architecture directly
addresses REQ-KIS-012; no new component or trust boundary is introduced.

## Delivery of this change

These are proposed future contracts. They do not change the active 0.21.0
evaluator or grant this task an unavailable lifecycle path. Govern this work
with the selected released evaluator. Deliver the changed evaluator,
instructions and plugin reference through a later release and adoption.

