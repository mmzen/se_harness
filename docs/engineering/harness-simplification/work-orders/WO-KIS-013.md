+++
id = "WO-KIS-013"
type = "work_order"
title = "Deliver the PR before the verification request"
status = "implemented"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"

[assurance]
commit_bound_verification = "required"
rationale = "Human review and external publication depend on these workflow and authority instructions; verification must bind their exact implemented candidate."
decided_by = "mmzen"

[execution_scope]
paths = [
  "se_harness/workflow_contract.json",
  "se_harness/instruction_discovery.json",
  "templates/repository/standard/docs/engineering/WORKFLOW.json",
  "templates/repository/standard/docs/engineering/harness/AUTHORITY.md",
  "templates/repository/standard/docs/engineering/harness/AUTHORIZE_WORK.md",
  "templates/repository/standard/docs/engineering/harness/DRAFT_WORK_ORDERS.md",
  "templates/repository/standard/docs/engineering/harness/EXECUTE_WORK.md",
  "templates/repository/standard/docs/engineering/harness/VERIFY_OUTCOME.md",
  "templates/repository/standard/docs/engineering/harness/PULL_REQUEST.md",
  "templates/repository/standard/docs/engineering/harness/DELIVER_RESULT.md",
  "plugins/verity-plane/common/skills/change/references/authority.md",
  "tests/test_workflow_procedures.py",
  "tests/test_workflow_execution.py",
  "tests/test_workflow_documentation_contract.py",
  "tests/test_instruction_discovery.py",
  "tests/test_instruction_architecture.py",
  "tests/test_cli_shape.py",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-012.md",
  "docs/engineering/harness-simplification/specifications/SPEC-KIS-006.md",
  "docs/engineering/harness-simplification/verification/VER-KIS-006.md",
  "docs/engineering/harness-simplification/work-orders/WO-KIS-013.md",
  "docs/engineering/harness-simplification/evidence/WO-KIS-013/",
]

[relations]
implements = ["REQ-KIS-012"]
specifications = ["SPEC-KIS-006"]
verification = ["VER-KIS-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T15:18:37Z"
decided_by = "mmzen"
reason = "mmzen replied \"i approve\" to the reviewed REQ-KIS-012, SPEC-KIS-006, VER-KIS-006 and WO-KIS-013 package, including required commit-bound verification and bounded push/PR updates from work/review-before-verification to main in mmzen/se_harness, on 2026-10-02. This covers implementation, local checks and commits, completion, capture, the review PR and later verification-decision push; human verification and merge remain separate. The installed 0.21.0 evaluator continues to govern this work. Reviewed SHA-256 after recording the confirmed assurance classification: 924a1e58eccc944311086cb8c353c2588a1871fbea4ddbdf63cbd3bb9049ee2a"
scope_paths = ["se_harness/workflow_contract.json", "se_harness/instruction_discovery.json", "templates/repository/standard/docs/engineering/WORKFLOW.json", "templates/repository/standard/docs/engineering/harness/AUTHORITY.md", "templates/repository/standard/docs/engineering/harness/AUTHORIZE_WORK.md", "templates/repository/standard/docs/engineering/harness/DRAFT_WORK_ORDERS.md", "templates/repository/standard/docs/engineering/harness/EXECUTE_WORK.md", "templates/repository/standard/docs/engineering/harness/VERIFY_OUTCOME.md", "templates/repository/standard/docs/engineering/harness/PULL_REQUEST.md", "templates/repository/standard/docs/engineering/harness/DELIVER_RESULT.md", "plugins/verity-plane/common/skills/change/references/authority.md", "tests/test_workflow_procedures.py", "tests/test_workflow_execution.py", "tests/test_workflow_documentation_contract.py", "tests/test_instruction_discovery.py", "tests/test_instruction_architecture.py", "tests/test_cli_shape.py", "docs/engineering/harness-simplification/requirements/REQ-KIS-012.md", "docs/engineering/harness-simplification/specifications/SPEC-KIS-006.md", "docs/engineering/harness-simplification/verification/VER-KIS-006.md", "docs/engineering/harness-simplification/work-orders/WO-KIS-013.md", "docs/engineering/harness-simplification/evidence/WO-KIS-013/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-02T15:20:41Z"
decided_by = "Codex agent"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed. Start the approved review-publication workflow change under mmzen approval, including required commit-bound verification and the bounded review-PR grant."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-10-02T15:48:35Z"
decided_by = "Codex agent"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed. Implemented the approved review-publication route and instructions; focused checks, 1238-test full suite with 22 skips, released preflight and combined Git-derived handoff passed."
+++

# Deliver the PR before the verification request

## Objective

The owner can inspect the pushed branch, evidence and ready verification record
through a draft PR when verification is requested. After the human verifies the
candidate, the agent pushes only the recorded decision as the final commit.
The owner may then merge when required checks permit it.

## In scope

Implement KIS-PRV-001 through KIS-PRV-006 in the existing workflow contract,
discovery map, task instructions and shared plugin authority reference.
Add focused regression coverage and retain ordinary review and test evidence.
Reuse INT-KIS-001, CAP-KIS-001 and CAP-KIS-003 unchanged.

## Out of scope

No new lifecycle state, formal artifact type, CLI command, hosting service,
receipt schema or network call inside the evaluator. No change to the required
verified coverage for integration, human verification authority, release rules
or merge protections. No automatic merge, release, marketplace publication,
installed evaluator/plugin modification or adoption. No startup/root instruction
expansion, broad formatting or historical artifact rewrite.

## Authorized decision envelope

This is a draft proposal, not an applied approval. The requested implementation
approval covers the named source changes, local checks and commits, required
evidence, work completion and preparation of one commit-bound verification record.
The human is asked to confirm required assurance at the same time.

The proposed publication grant covers this work's review branch
work/review-before-verification in mmzen/se_harness, one PR targeting main,
updates within the approved scope and the later recorded verification decision.
The grant also permits marking that PR ready after verified delivery. It excludes
merge, force-push, release, tags and unrelated changes. Bind every actual
operation to its full commit and passing current checks.

The requested future workflow does not override the selected released 0.21.0
evaluator for this implementation. Use only a route and authority supported by
that evaluator. If its integration route prevents early review publication,
report that compatibility limit before acting; do not run candidate code to
grant authority. Human verification remains a separate decision.

## Constraints

Keep procedure identifiers and reading anchors stable where their meaning
remains valid. Maintain agreement between the packaged workflow contract and
its template. Add only the bounded review-publication alternative and its
necessary instruction discovery. Preserve local-only routes and existing
verification cards. Do not turn review publication into merge permission.

The final decision commit changes only the selected VREC. Corrective source or
evidence changes require their own eligible work and verification assessment.
Do not add a second verification cycle merely to record an actual human decision.

## Expected change surface

| Files | Change |
| --- | --- |
| workflow_contract.json and the WORKFLOW.json template | Add the legal pre-verification review-publication route using existing appropriate gates; retain the integration path's verified coverage. |
| instruction_discovery.json | Map the route and its conditional verification prerequisite to the on-demand procedure. |
| AUTHORITY.md, AUTHORIZE_WORK.md, DRAFT_WORK_ORDERS.md and plugin authority reference | Explain the explicit bounded publication grant in the initial approval, exact-operation checks and reuse after the decision. |
| EXECUTE_WORK.md, VERIFY_OUTCOME.md, PULL_REQUEST.md and DELIVER_RESULT.md | Order publication before the request, require remote readback and links, and publish the final decision before optional merge. |
| Six named test files | Cover procedure eligibility, unchanged integration refusal, discovery, scope, instruction agreement and commit identities as applicable. |
| This package and evidence/WO-KIS-013/ | Preserve the actual approvals, completion and ordinary implementation evidence. Generated VREC outputs follow the evaluator's normal admitted destinations. |

Only edit listed test files when a relevant assertion or case belongs there.
Do not duplicate tests solely because several files are admitted.

## Required verification

Proposed assurance classification: `required`. Human review and external
publication depend on these workflow and authority instructions; verification
must bind their exact implemented candidate. Record `[assurance]` and its
actual human decision-maker after confirmation, before approval is applied.

Apply VER-KIS-006. Derive expected outcomes from the requirement and specification.
Run focused suites, then the normal full suite. Use the released evaluator for
real validation, integrity, preflight, scope, handoff, completion and capture.
Retain actual skips and failures. Human verification must bind the exact candidate.

## Evidence to record

Use evidence/WO-KIS-013/ for the requirement assessment, reviewed instruction
and contract diff, tests with exact invocations and results, the small local
Git demonstration and required harness outputs. Use a transient location outside
the repository for planning material. Do not manufacture live provider or agent
observations from a simulated case.

## Stop and escalate conditions

Stop the affected action if implementation needs a file outside this scope,
a new command/state/receipt/service, a weaker integration or verification gate,
or a change to an accepted definition. Report the discovered need before
extending the package. Missing publication authority or an unavailable released
procedure blocks publication, not independent local work.

## Completion report format

State the delivered ordering, requirement results, actual checks and limits.
Link the exact candidate, verification record and readable review material.
Use the selected evaluator's actual next step and identify any remaining
compatibility or human-decision boundary. Do not claim installed delivery
before the separate release and adoption.

