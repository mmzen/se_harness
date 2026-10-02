+++
id = "WO-KIS-010"
type = "work_order"
title = "Deliver complete scope preparation and clear approval requests"
status = "implemented"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"

[assurance]
commit_bound_verification = "required"
rationale = "Later human approval and engineering decisions rely on the correctness of the CLI report and released instructions."
decided_by = "mmzen"

[execution_scope]
paths = [
  "se_harness/cli.py",
  "se_harness/workflow.py",
  "se_harness/workflow_change_set.py",
  "se_harness/workflow_result.py",
  "se_harness/scope_preparation.py",
  "templates/repository/standard/docs/engineering/ARTIFACT_AUTHORING.md",
  "templates/repository/standard/docs/engineering/harness/DRAFT_WORK_ORDERS.md",
  "templates/repository/standard/docs/engineering/harness/AUTHORIZE_WORK.md",
  "templates/repository/standard/docs/engineering/harness/WORK_AND_EVIDENCE.md",
  "templates/repository/standard/docs/engineering/templates/WORK_ORDER.template.md",
  "docs/notes/harnessctl-reference.md",
  "tests/test_scope_preparation.py",
  "tests/test_cli_shape.py",
  "tests/test_workflow_execution.py",
  "tests/test_workflow_compliance.py",
  "tests/test_workflow_restitution.py",
  "tests/test_one_validation.py",
  "tests/test_artifact_authoring.py",
  "tests/test_artifact_authoring_policy.py",
  "tests/test_workflow_documentation_contract.py",
  "tests/test_artifact_catalog.py",
  "tests/test_instruction_architecture.py",
  "tests/test_progressive_instruction_discovery.py",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-010.md",
  "docs/engineering/harness-simplification/specifications/SPEC-KIS-004.md",
  "docs/engineering/harness-simplification/verification/VER-KIS-004.md",
  "docs/engineering/harness-simplification/work-orders/WO-KIS-010.md",
  "docs/engineering/harness-simplification/evidence/WO-KIS-010/",
]

[relations]
implements = ["REQ-KIS-010"]
specifications = ["SPEC-KIS-004"]
verification = ["VER-KIS-004"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T11:41:55Z"
decided_by = "mmzen"
reason = "mmzen approved the package published for review in PR #523 with \"Ok i approve\". This approves WO-KIS-010 at reviewed SHA-256 62d8a3bf0bfdf2246afbd37c7a5884b48f2ca860b5fd5617a102444753eb84d0, including required commit-bound verification under VER-KIS-004 and bounded local execution under WO-KIS-010. Pending assurance fields were completed from this decision. Verification acceptance and implementation publication remain separate."
scope_paths = ["se_harness/cli.py", "se_harness/workflow.py", "se_harness/workflow_change_set.py", "se_harness/workflow_result.py", "se_harness/scope_preparation.py", "templates/repository/standard/docs/engineering/ARTIFACT_AUTHORING.md", "templates/repository/standard/docs/engineering/harness/DRAFT_WORK_ORDERS.md", "templates/repository/standard/docs/engineering/harness/AUTHORIZE_WORK.md", "templates/repository/standard/docs/engineering/harness/WORK_AND_EVIDENCE.md", "templates/repository/standard/docs/engineering/templates/WORK_ORDER.template.md", "docs/notes/harnessctl-reference.md", "tests/test_scope_preparation.py", "tests/test_cli_shape.py", "tests/test_workflow_execution.py", "tests/test_workflow_compliance.py", "tests/test_workflow_restitution.py", "tests/test_one_validation.py", "tests/test_artifact_authoring.py", "tests/test_artifact_authoring_policy.py", "tests/test_workflow_documentation_contract.py", "tests/test_artifact_catalog.py", "tests/test_instruction_architecture.py", "tests/test_progressive_instruction_discovery.py", "docs/engineering/harness-simplification/requirements/REQ-KIS-010.md", "docs/engineering/harness-simplification/specifications/SPEC-KIS-004.md", "docs/engineering/harness-simplification/verification/VER-KIS-004.md", "docs/engineering/harness-simplification/work-orders/WO-KIS-010.md", "docs/engineering/harness-simplification/evidence/WO-KIS-010/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-02T11:43:08Z"
decided_by = "Codex agent"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed. Start bounded implementation under mmzen's recorded package approval."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-10-02T12:29:01Z"
decided_by = "Codex agent"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed. Implemented the approved planned-path view and preparation/approval guidance. Final Windows suite: 1233 tests, 1211 passed and 22 skipped. Focused, instruction, distribution and released validation/integrity checks passed. Combined-scope handoff passed from ccbfbdec811d722974336924125b070d91f111f4 under both approved work orders, with Git long-path support. Hosted CI and human verification remain separate."
+++

# Deliver complete scope preparation and clear approval requests

## Objective

For the human requesting a bounded change, provide one understandable
implementation decision after the agent has inspected the affected work,
included foreseeable supporting paths, and assessed the proposed scope.

## In scope

Implement KIS-SCP-001 through KIS-SCP-006: dependency inspection guidance,
one complete bounded WO, the optional planned-path view of check, explicit
explanation of generated outputs, and a clear approval request. Reuse
INT-KIS-001 and CAP-KIS-001 unchanged. Existing KIS design simplicity and
routine-execution authority remain applicable.

## Out of scope

No change to authority, lifecycle edges, gates, actual change-set admission,
record capture, release or adoption. No automatic dependency scanner,
persistent planning inventory, new artifact type or scoring framework.
No host authentication or live desktop test. Push, PR, merge, marketplace
publication and installed evaluator/plugin updates are separate actions.

## Proposed assurance decision

Proposed classification: required commit-bound verification under VER-KIS-004.
Reason: later human approval and engineering decisions rely on the correctness
of the CLI report and released instructions. Confirm this classification with
the package approval. The assurance metadata will then record the actual
human decision; no deciding identity is fabricated in this draft.

## Authorized decision envelope

Once this package is approved and start checks pass, the agent may implement
within the listed paths, run checks, make local commits, retain evidence,
record eligible completion and prepare the required VREC. It may choose
local helper structure and test organization within the accepted behavior.
It must not treat preparation as approval or independently accept verification.

The change surface is an allowed boundary, not a quota: do not edit a listed
file when the implementation does not need it. Approval covers the exact
reviewed definitions and verification contract. Any changed accepted meaning
or actual scope expansion requires the applicable human decision.

## Constraints

Use the selected released evaluator 0.21.0 for real governance. Candidate
source may run only as development tests and isolated demonstrations.
Preserve existing calls without the new option. Reuse validation and path
admission instead of a second graph pass or competing matcher.
Keep transient working notes outside the repository. Preserve owner content.

## Expected change surface

| Paths | Planned change and reason |
| --- | --- |
| se_harness/cli.py | Parse planned-path input, enforce mutually exclusive options and use the existing check result route. |
| se_harness/workflow.py | Add the planning view while reusing the already validated catalog and selected lifecycle projection. |
| se_harness/workflow_change_set.py | Reuse or expose the smallest existing normalization/admission seam; do not widen its behavior. |
| se_harness/workflow_result.py | Render preparation coverage and its limits; preserve canonical lifecycle content and bind machine planning data to the digest. |
| se_harness/scope_preparation.py | Small read-only assessment helper if separation is clearer than extending the existing module. No persistent state. |
| templates/repository/standard/docs/engineering/harness/DRAFT_WORK_ORDERS.md | Put dependency inspection and planned-path assessment in the existing preparation procedure. |
| templates/repository/standard/docs/engineering/harness/AUTHORIZE_WORK.md | Present the concise decision card at the existing human approval step. |
| templates/repository/standard/docs/engineering/harness/WORK_AND_EVIDENCE.md | Explain complete bounded scope and existing automatic generated-output admission at the shared reference. |
| templates/repository/standard/docs/engineering/ARTIFACT_AUTHORING.md | Point the WO checklist to the common preparation guidance without duplicating its procedure. |
| templates/repository/standard/docs/engineering/templates/WORK_ORDER.template.md | Replace guessed-file guidance with inspected paths, short reasons and explicit unknown outputs in Expected change surface. |
| docs/notes/harnessctl-reference.md | Document the opt-in check mode, report meaning, compatibility and limitations. |
| tests/test_scope_preparation.py | Public CLI coverage, path boundaries, no-write assertions, generated outputs and the two representative demonstrations. |
| tests/test_cli_shape.py | Preserve command shape and exercise the new option's input contract. |
| tests/test_workflow_execution.py | Protect checkpoint-free projection, selection and lifecycle compatibility. |
| tests/test_workflow_compliance.py | Protect actual scope and generated-record admission when shared helpers are reused. |
| tests/test_workflow_restitution.py | Check human/JSON clarity and machine-field digest binding. |
| tests/test_one_validation.py | Assert that the planning view reuses one repository validation. |
| tests/test_artifact_authoring.py; tests/test_artifact_authoring_policy.py | Verify the supported authoring route and updated WO guidance. |
| tests/test_workflow_documentation_contract.py; tests/test_artifact_catalog.py | Keep instruction links, headings and CLI documentation consistent. |
| tests/test_instruction_architecture.py; tests/test_progressive_instruction_discovery.py | Ensure agents discover the guidance at preparation/approval without loading it at every startup. |
| The four exact formal-artifact paths in execution_scope | Carry this reviewed package and its evaluator-applied lifecycle history with the work. No manual rewrite of accepted decisions. |
| docs/engineering/harness-simplification/evidence/WO-KIS-010/ | Retain local checks, demonstration results, ordinary review and generated start/review/handoff evidence for this WO. |

The code entry point, projection, result renderer, admission helpers, current
CLI reference, WO template and relevant test consumers were inspected before
this draft. The common change skill already routes agents to released
authoring and continuation procedures, so no duplicate skill policy is
needed. Existing package data includes these modules and resources;
packaging and CI configuration changes are not planned. Distribution and
CI checks will verify that assumption.

No existing fixture file needs revision; the focused test creates small
temporary fixtures through current helpers. No new schema for formal
artifacts or machine gate contract is needed. Do not change unrelated stale
documentation while carrying this proposal.

## Generated outputs and unresolved destinations

The selected WO's own path is explicitly listed. Start, review, handoff,
test and ordinary review evidence use the explicit evidence directory above.

The future VREC ID is allocated by the evaluator during preparation. Its
exact record and evaluator-evidence paths are not known yet. Existing
relationship-based admission covers a record that directly verifies this
WO and its declared evaluator evidence. Recheck the actual returned paths
when the record exists. This does not admit its whole directory or a record
for another WO. No release record or publication output is planned.

## Required verification

Perform VER-KIS-004 cases A-F. Run focused CLI, workflow, authoring and
discovery tests, then the repository suite and distribution checks. Retain
unavailable checks and skips explicitly. Windows local checks and existing
Linux/Windows CI serve their distinct scopes; local passing results do not
stand in for CI. Human acceptance uses the exact candidate-bound VREC.

## Evidence to record

Under the declared evidence directory, retain one ordinary review plus
commands, exit codes, outputs, the requirement-to-result assessment and the
two fixture demonstrations. Record actual changed files and compare them
with this plan. Use the released evaluator's required evidence format for
start, review, handoff and verification capture. Preserve failed attempts.

## Stop and escalate conditions

Stop the affected action if the implementation requires an unlisted path,
changes accepted semantics, changes path admission or lifecycle authority,
needs another persistent schema or cannot preserve existing check behavior.
Also stop for a failed required gate or unresolved material verification
failure. Report the exact new need and prepare one bounded correction.

## Completion report format

State the user-visible change, actual scope, test results, limitations and
the evaluator's next decision. Show whether either demonstration needed
an additional WO for a foreseeable omission. Do not turn these two examples
into a general measured improvement claim.
