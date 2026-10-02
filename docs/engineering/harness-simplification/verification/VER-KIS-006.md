+++
id = "VER-KIS-006"
type = "verification"
title = "Verify review publication and the final decision commit"
status = "approved"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"

[relations]
verifies = ["REQ-KIS-012"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T15:18:37Z"
decided_by = "mmzen"
reason = "mmzen replied \"i approve\" to the reviewed REQ-KIS-012, SPEC-KIS-006, VER-KIS-006 and WO-KIS-013 package, including required commit-bound verification and bounded push/PR updates from work/review-before-verification to main in mmzen/se_harness, on 2026-10-02. This covers implementation, local checks and commits, completion, capture, the review PR and later verification-decision push; human verification and merge remain separate. The installed 0.21.0 evaluator continues to govern this work. Reviewed SHA-256 after recording the confirmed assurance classification: 0e3b6519f4264c36c59130f9cecac84749222b9bd488e59dce9d9f2b301f39fa"
+++

# Verify review publication and the final decision commit

## Independence

Derive expected results from REQ-KIS-012 and SPEC-KIS-006 before implementation.
The candidate evaluator is used only in isolated tests. The selected released
0.21.0 evaluator governs real artifacts, work authority and evidence capture.
A simulated owner response is not authority for a real artifact or external action.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-KIS-012 | test | A: procedure and gate regression tests | A ready VREC has a legal review-publication route. Its record remains ready. The integration path still requires verified coverage. Rejected or superseded records do not become eligible through the new route. |
| REQ-KIS-012 | test | B: discovery and PR regression tests | The review route resolves its instructions and the PR prerequisite is discoverable before a human request. The existing PR checker accepts the bounded review package and still rejects unauthorized paths or ineligible work. |
| REQ-KIS-012 | inspection | C: complete instruction and authority diff | Initial approval explicitly covers review publication and the final decision push. The request has remote links. Final commit restrictions, existing authority reuse, optional merge and recovery agree across all changed files. |
| REQ-KIS-012 | demonstration | D: ordered review examples and local Git fixture | The normal sequence and failure cases below distinguish the captured candidate, review head and decision head without changing captured inputs or claiming simulated publication as a live result. |

## Required cases

1. A ready record with approved review publication: the agent checks the exact
   branch and PR, retains remote identities and presents the link before asking
   for verification. The record remains ready.
2. No publication grant, failed push, missing PR, wrong head or wrong destination:
   the agent reports the missing prerequisite without requesting verification.
   An uncertain response triggers inspection, not an unconditional repeat.
3. One existing matching draft PR: update or reuse it; do not create another.
4. A human verifies unchanged inputs: apply the normal transition and publish
   one final commit containing only the selected VREC update. The record still
   names the original candidate. Confirm delivery before marking the PR ready.
5. A correction or changed evidence: keep the PR in draft, assess work authority
   and refresh the verification package as required. Do not recycle the earlier
   answer or restart a completed work order.
6. A final push fails: distinguish recorded locally from delivered remotely;
   retry only missing effects under the existing grant.
7. Required verification evidence is missing, or final-head CI fails: do not
   claim acceptance eligibility or merge readiness from a passing unrelated check.
8. Local-only work or work without a new VREC: preserve its existing route.

Use a small local Git fixture to demonstrate the candidate, preparation and
decision commits. Assert that the decision commit changes only the selected
record and preserves the captured candidate and evidence. Label provider
observations and human replies as simulated when they are simulated.
Do not add a fake hosting service, credential requirement, new durable receipt
or live-agent test for this instruction and workflow-data change.

## Commands and platforms

On Windows, use the configured development Python and run the focused suites:

    python -B -m unittest tests.test_workflow_procedures tests.test_workflow_execution tests.test_workflow_compliance tests.test_workflow_documentation_contract tests.test_instruction_discovery tests.test_instruction_architecture tests.test_progressive_instruction_discovery tests.test_cli_shape

Run the repository's normal full suite after those checks because shared
workflow policy and packaged plugin instructions change. Record actual skips.
Hosted CI is assessed when available at integration; a local result does not
establish a hosted result. No live Codex or Claude session is required.

Use released harness validation, integrity, preflight, complete Git-derived
scope and handoff checks for WO-KIS-013. Capture the exact clean implementation
candidate with the released evaluator after required local evidence exists.

## Evidence retention

Retain ordinary review and the requirement assessment, tests with executable,
version, arguments and exit status, local Git demonstration observations, and
required harness outputs under evidence/WO-KIS-013/. Retain failed attempts
and their corrections. Generated capture evidence and the VREC use the
evaluator's normal destinations. Keep bound evidence unchanged after capture.

## Residual uncertainty

Local tests establish evaluator routing, local gates and the instruction
contract. They do not prove every agent follows the instructions or every
hosting service enforces identical controls. A live remote readback remains
required each time the installed procedure publishes a real review.
This work does not deliver the future behavior to installed hosts until release
and adoption occur.

