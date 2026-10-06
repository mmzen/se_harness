+++
id = "WO-HAG-003"
type = "work_order"
title = "Correct decision attribution without rewriting artifact owners"
status = "implemented"
owners = ["mmzen"]
created = "2026-10-04"
updated = "2026-10-04"

[assurance]
commit_bound_verification = "required"
rationale = "Later decision recording and evaluator release depend on the correctness of this trusted behavior. mmzen confirmed required commit-bound verification with approval of the reviewed package."
decided_by = "mmzen"

[relations]
implements = ["REQ-HAG-010"]
specifications = ["SPEC-HAG-005"]
architecture = ["ARCH-HAG-002", "ADR-HAG-002"]
verification = ["VER-HAG-003"]

[execution_scope]
paths = ["se_harness/cli.py", "se_harness/decisions.py", "se_harness/risks.py", "se_harness/workflow_edges.py", "se_harness/workflow.py", "se_harness/engine/validation_decisions.py", "tests/test_decision_management.py", "tests/test_risk_management.py", "tests/test_workflow_execution.py", "tests/test_workflow_documentation_contract.py", "docs/notes/harnessctl-reference.md", "docs/notes/decision-artifacts.md", "templates/repository/standard/docs/engineering/harness/AUTHORITY.md", "templates/repository/standard/docs/engineering/harness/AUTHORIZE_WORK.md", "docs/engineering/hosted-artifact-graph/evidence/WO-HAG-003/"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-04T16:54:20Z"
decided_by = "mmzen"
reason = "mmzen explicitly approved WO-HAG-003 and required verification in response to the reviewed six-artifact correction package. This applies only to that package: local implementation, checks, commits and commit-bound verification preparation. Human verification acceptance, publication, release, adoption and the live DEC-HAG-001 disposition remain separate. Reviewed file hashes were compared before this transition; approval bindings are retained under docs/engineering/hosted-artifact-graph/evidence/WO-HAG-003/."
scope_paths = ["se_harness/cli.py", "se_harness/decisions.py", "se_harness/risks.py", "se_harness/workflow_edges.py", "se_harness/workflow.py", "se_harness/engine/validation_decisions.py", "tests/test_decision_management.py", "tests/test_risk_management.py", "tests/test_workflow_execution.py", "tests/test_workflow_documentation_contract.py", "docs/notes/harnessctl-reference.md", "docs/notes/decision-artifacts.md", "templates/repository/standard/docs/engineering/harness/AUTHORITY.md", "templates/repository/standard/docs/engineering/harness/AUTHORIZE_WORK.md", "docs/engineering/hosted-artifact-graph/evidence/WO-HAG-003/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-04T16:56:11Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed. Codex starts the unchanged approved correction after passing start preflight, under mmzen recorded approval and required commit-bound verification."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-10-04T17:27:05Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed. Codex completed the approved correction. VER-HAG-003 cases, installed Windows/Linux probes, pinned builds, review preflight and Git-derived handoff passed. Human verification, publication, release/adoption and live DEC-HAG-001 disposition remain separate."
+++

# Correct decision attribution without rewriting artifact owners

## Objective

Deliver the explicit decision-owner binding defined in SPEC-HAG-005. A human
can be named accurately while the evaluator retains its existing check on
which owner holds the decision right. This draft grants no execution authority.

## In scope

One optional command input, its shared API/planner path, disposition audit
field, validator shape check, meaningful regression tests and released usage
instructions. Reuse current decision, workflow and risk mechanisms.

## Out of scope

No live DEC-HAG-001 disposition; no accepted owner/history rewrite; no new
identity registry or authentication provider; no blanket acceptance of actor
names; no changes to existing holder selection, risk rights, human decision
rules or hosted service policy. Release, adoption, merge and deployment are
separate. Preserve VREC-HAG-001 and all evidence for its exact candidate.

## Proposed assurance classification

Required commit-bound verification: later decision recording and evaluator
release depend on the correctness of this trusted behavior. The human must
confirm this classification with approval; no decided_by is inferred here.

## Expected change surface

| Inspected paths | Purpose |
| --- | --- |
| se_harness/cli.py | Add optional input and actual-human help; existing _decide dispatch. |
| se_harness/decisions.py | Existing deciding_roles and request validation; preserve holders and retain the explicit binding. |
| se_harness/risks.py | Thread the optional binding through the actual CLI dispatcher and paired transaction. |
| se_harness/workflow_edges.py | Pass the binding to the shared disposition check. |
| se_harness/workflow.py | Existing closed disposition writer must retain the optional field. |
| se_harness/engine/validation_decisions.py | Validate optional metadata without rewriting historical records. |
| tests/test_decision_management.py, tests/test_risk_management.py | Positive attribution, incorrect mapping, lifecycle, atomicity and paired-risk cases. |
| tests/test_workflow_execution.py, tests/test_workflow_documentation_contract.py | Shared transition behavior, command semantics and published instruction coverage where affected. |
| docs/notes/harnessctl-reference.md, docs/notes/decision-artifacts.md | Existing command synopsis and decision-model examples must describe actual human identity and explicit owner binding. |
| templates/repository/standard/docs/engineering/harness/AUTHORITY.md | Explain explicit mapping under an actual human decision. |
| templates/repository/standard/docs/engineering/harness/AUTHORIZE_WORK.md | Show preview/apply procedure without owner impersonation. |
| docs/engineering/hosted-artifact-graph/evidence/WO-HAG-003/ | Bounded test/review/packaged observations. |

The existing package includes these Python modules and instruction resources;
no dependency, CI, plugin or build-file edit is needed. New VREC and evaluator
evidence paths are unresolved until released capture allocates them; check
the direct-record scope rules against those actual paths before writes.
The work order's own file and packet use existing admission rules.

## Authorized decision envelope, effective only after approval

The implementer may make local in-scope edits and commits, run tests and build
disposable packages, retain evidence and prepare required commit-bound
verification. The reviewed six-draft package must be approved before execution.
Actual acceptance, external delivery and adoption remain separate decisions.
No review-publication grant is requested by this work order; the current
unfinished PR #535 retains its existing destination and explicit limitations.

## Verification and stop conditions

Perform VER-HAG-003, including both installed-package platforms. Stop if the
fix needs changed owner rules, an accepted-definition amendment, an uncovered
path or an unavailable required check. Do not imitate success with an owner
alias or candidate governor. Report required checks as passed, failed or
unperformed with their actual evidence. No live decision is disposed here.

## Dependency route after this work

Qualify one later release candidate containing this correction and the
WO-HAG-002 standalone draft validator. Preserve VREC-HAG-001 at
169430fe25d28972a9b86fef2d00eccde2baa5db and its tested source
08694a22ed754474267b0da98a9514648068f5f9. The combined release needs a new
final VREC and release contract under the existing release process.

After publication, separately authorize installation/adoption and the exact
hosted pin amendment. SPEC-HAG-003 and VER-HAG-001 currently pin 0.22.0;
wire constants and fixtures must be reviewed for the new identity too. The
current release has no linked-definition revision activation command. Keep
that amendment proposal outside the repository until the human explicitly
selects a supported resolution or authorizes a bounded manual amendment
that preserves and links the accepted bytes. No amendment is inferred here.

Then use the new released command to record the already-given
extend-evaluator decision under mmzen, rerun affected gates, and resume the
dependent adapter under its applicable approved definitions. Prior choice
and WO-HAG-001 approval need no repeat decision.

## Completion report

State actual behavior, refusal/attribution evidence, candidate and package
identities, checks and gaps, unchanged historical bindings, and the released
evaluator's one current next step. Distinguish correction verification from
release/adoption and hosted-service verification.
