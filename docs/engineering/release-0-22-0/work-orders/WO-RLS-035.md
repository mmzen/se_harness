+++
id = "WO-RLS-035"
type = "work_order"
title = "Qualify and publish plugin 0.2.5"
status = "in_progress"
owners = ["mmzen"]
created = "2026-10-03"
updated = "2026-10-03"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen confirmed required commit-bound verification; subsequent release, marketplace publication and public-delivery decisions depend on this work."
decided_by = "mmzen"

[execution_scope]
paths = [
  "docs/engineering/release-0-22-0/"
]

[relations]
implements = ["REQ-PLG-002", "REQ-IAR-030", "REQ-RLO-018"]
specifications = ["SPEC-PLG-001", "SPEC-IAR-016", "SPEC-RLO-006"]
verification = ["VER-RLS-034", "VER-IAR-021"]
architecture = ["ARCH-PLG-001", "ADR-PLG-001", "ARCH-IAR-012", "ADR-IAR-012"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T22:07:58Z"
decided_by = "mmzen"
reason = "Human repository owner mmzen answered \"Approve package and required verification\" to the reviewed evaluator 0.22.0 / plugin 0.2.5 package: REL-SEH-034, WO-RLS-034/035/036 and VER-RLS-033/034/035. This confirms required commit-bound verification and authorizes bounded preparation, qualification, review pushes/PRs and listed delivery work under the retained request \"Merged. Next: prepare and execute the release\". Human verification of exact results, the exact release-record decision and merge remain separate. Repository adoption and provider-setting changes are excluded. Selected released 0.21.0 governs; Codex applies the recorded human decision. Reviewed SHA-256 6888abc1d730c88512e8b578a25a700c7fb089f61e1a4ad47985c2cb9442a9f3; transition-input SHA-256 1cd29d3fec2a778e6a8bb555d424baed1b2f37e476374467e730607eb0c4a0cc. Only confirmed assurance fields were added."
scope_paths = ["docs/engineering/release-0-22-0/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-03T04:29:21Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."
+++

# Qualify and publish plugin 0.2.5

## Objective

Deliver both host packages of plugin 0.2.5 with exact public evaluator 0.22.0.

## In scope

1. Independently download and verify the wheel released by RLS-SEH-032.
2. Assemble both packages from the committed manifests and shared assets using
   the existing build/check route. Retain inventories and exact tree digests.
3. Run package qualification and the applicable native delivery checks in
   disposable Codex and Claude Code profiles. Assess the exact resource inputs.
4. Complete handoff, capture VREC-PLG-032, publish its review and obtain human
   verification before the marketplace write.
5. Recheck the public marketplace parent and publish an ordinary descendant
   commit to mmzen/se_harness:plugin-marketplace under the matching release
   execution grant. Preserve history. Read the remote tree back independently.
6. Hand qualified and published identities to WO-RLS-036 for public-route checks.

## Expected change surface

Only this release domain receives source-repository changes: evidence/WO-RLS-035/,
verification-records/VREC-PLG-032.md, evidence/VREC-PLG-032-evaluator.json,
shared delivery-plan versions, handoffs and subsequent publication receipts.
Generated marketplace files live in an isolated output/checkout outside this
repository and must match the existing assembly inventory exactly.

## Required verification

VER-RLS-034 and VER-IAR-021 apply. Desktop and authenticated native criteria are
not presumed passed. Older accepted omissions do not authorize this release.

## Out of scope

Plugin implementation changes, normal host profile updates, new dependencies,
provider-directory submission, repository adoption and public closeout claims.

## Authority and assurance

Propose required commit-bound verification. Later release and availability
decisions rely on these changes. The human must confirm this classification
with package approval; no assurance decision or lifecycle event is invented.

Human mmzen requested: "Merged. Next: prepare and execute the release".
Retain this release-execution request. Package approval makes its versions,
destinations and permitted work concrete. Reuse matching grants as required
checks pass; do not ask again for an unchanged external action.

The review grant proposed here covers ordinary pushes and draft PRs from
work/release-0-22-0 to mmzen/se_harness:main, later decision/receipt updates,
and existing read-only publication rehearsals. Publish the review before asking
for verification. Human verification and the exact release-record decision
remain separate from work approval. No merge is inferred.

Released 0.21.0 governs formal artifacts and gates outside the checkout.
Candidate 0.22.0 is the system under test. Do not adopt it, activate the new
complete-release route, change provider settings, or overwrite old evidence.
Preserve credentials and normal user profiles; use disposable test profiles.

## Evidence and completion

Retain actual commands, runtimes, commits, results, failures and digests in this
release domain. Include canonical VREC/RLS files and fixed evaluator JSON
destinations under evidence/, plus handoff records and decision transport.
Keep temporary builds and profiles outside the repository. Retain concise
durable evidence with raw outputs only where required by the selected contract.

Stop the affected action for failed or missing required evidence, changed
identities or destinations, uncovered paths, unavailable independent controls,
or a conflicting remote ref. Inspect uncertain writes before retrying.
Report the actual formal state, completed surfaces, outstanding work and next
decision. A publication or a version label alone cannot establish completion.
