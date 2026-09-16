+++
id = "WO-ECP-039"
type = "work_order"
title = "Correct the plugin-owned upgrade rehearsal assertion"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-09-16"
updated = "2026-09-16"

[assurance]
commit_bound_verification = "required"
rationale = "CI and integration decisions depend on a real upgrade rehearsal that accepts supported ownership without hiding a failed evaluator handover. The corrected combined PR needs assurance at its new candidate."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "repository_tools/upgrade_rehearsal.py",
  "tests/test_upgrade_rehearsal.py",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-025.md",
  "docs/engineering/execution-control-plane/verification/VER-ECP-027.md",
  "docs/engineering/execution-control-plane/work-orders/WO-ECP-039.md",
  "docs/engineering/execution-control-plane/evidence/WO-ECP-039/",
  "docs/engineering/execution-control-plane/verification-records/VREC-ECP-041.md",
  "docs/engineering/execution-control-plane/evidence/VREC-ECP-041-evaluator.json",
]

[relations]
implements = ["REQ-ECP-012"]
specifications = ["SPEC-ECP-007", "SPEC-ECP-025"]
verification = ["VER-ECP-027"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-16T16:55:52Z"
decided_by = "engineering-owner"
reason = "The owner approved the presented SPEC-ECP-025, VER-ECP-027 and WO-ECP-039 package with \"i apprive\" on 2026-09-16, exercising the engineering-owner decision for WO-ECP-039. Reviewed SHA-256 df418ee693c62109a3b455f651ca7ecda38ec51aa25e65f18ae60d1830a53c80. This records definition and bounded execution approval, not assurance or external delivery."
scope_paths = ["repository_tools/upgrade_rehearsal.py", "tests/test_upgrade_rehearsal.py", "docs/engineering/execution-control-plane/README.md", "docs/engineering/execution-control-plane/specifications/SPEC-ECP-025.md", "docs/engineering/execution-control-plane/verification/VER-ECP-027.md", "docs/engineering/execution-control-plane/work-orders/WO-ECP-039.md", "docs/engineering/execution-control-plane/evidence/WO-ECP-039/", "docs/engineering/execution-control-plane/verification-records/VREC-ECP-041.md", "docs/engineering/execution-control-plane/evidence/VREC-ECP-041-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-16T16:58:21Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed. Start the approved rehearsal correction under DR-015 after passing start preflight."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-16T18:16:02Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded engineering-owner approval; relevant local gates passed. Complete the approved correction under DR-015: 1081 tests pass with 15 skips, two real upgrade replays pass with identical lock digests, required integrity and scope checks pass, and failed attempts remain retained. Owner assurance and hosted CI remain separate."
+++

# Correct the plugin-owned upgrade rehearsal assertion

## Objective and baseline

Resolve PR #487's remaining Linux and Windows rehearsal failure, "the resulting
lock is schema 4, not 3". Baseline is verified/pushed
7268011f19753bf7d5a42b9bc829c3ea33f682aa on work/repository-cleanup. The existing
pipeline performs the real handover successfully before its obsolete assertion.
The earlier run at 0dadc352 has the same failure; this is not introduced by
WO-HUP-020's assessor correction.

This work is drafted in response to the owner's "it failed" report. Approval of
SPEC-ECP-025, VER-ECP-027 and this bounded WO is required before implementation.
No active architecture addresses REQ-ECP-012; as for original WO-ECP-010, no
architecture relation is fabricated for this routine repository-tool change.

## In scope

1. Apply SPEC-ECP-025 in the existing rehearsal helper and its explanatory
   docstring: supported ownership and provider preservation replace the fixed
   schema-3 assertion. Preserve every other handover check and output contract.
2. Extend the existing test module with the missing plugin-owned success and
   meaningful refusal cases. Keep the existing fixture and test runner.
3. Update this domain index and retain the original failures, source diagnosis,
   normal design/implementation review, required checks and scope comparisons.
4. Complete the approved work, make ordinary local commits and prepare the
   aggregate VREC-ECP-041 under VER-ECP-027 using the released evaluator.

## Out of scope

Product runtime, installer, catalogues, templates, root lock/configuration,
evaluator versions, workflows, assessor code, other tests, plugin packages,
marketplace refs and existing verified records or bound evidence. No release
build, merge, publication, installation into user profiles or credential change.

## Authorized decision envelope

Once this package is approved, Codex may start, implement, check, make local
commits, retain evidence, record completion and prepare required verification
under DR-015. Routine helper and fixture organization within the listed paths
is an executor choice. Private test environments and non-promotable replay
artifacts may be created outside the checkout; existing CI wheel reuse is
preferred, with an ephemeral wheel build permitted solely for acceptance.

Use this WO's baseline for its scope/handoff. Check the combined PR against
f05c478a29c39f94968fdc842a34c861d30a42ac with WO-PLG-025, WO-HUP-020 and this WO.
Earlier work is input for aggregate assurance, not authority to edit those
completed scopes. Preserve VREC-PLG-022 and VREC-HUP-019 and all their evidence.
Owner verification and delivery of the new candidate remain separate decisions.

## Verification, stop conditions and completion

Execute VER-ECP-027, including two real local replays, the final full suite and
the normal released-evaluator gates. Report earlier warnings and identity skew
accurately. Retain full candidate and wheel identities, arguments, exits and
raw results. Verify unchanged product, plugin and prior-assurance inputs.

Stop the affected action for missing approval, failed integrity, invalid graph,
scope drift, changed reuse inputs or a need to weaken an existing check. Seek
bounded remediation for failures beyond this helper rather than widening scope.
Record implemented after local work and required evidence are complete, then
prepare the new ready record. Report what changed, checks, exact candidate,
remaining hosted CI and the single next accountable decision.
