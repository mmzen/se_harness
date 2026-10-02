+++
id = "WO-KIS-012"
type = "work_order"
title = "Deliver clear verification requests"
status = "implemented"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"

[assurance]
commit_bound_verification = "required"
rationale = "Humans and agents rely on these instructions when accepting engineering results; verification must bind the exact implemented candidate."
decided_by = "mmzen"

[execution_scope]
paths = [
  "templates/repository/standard/docs/engineering/harness/VERIFY_OUTCOME.md",
  "templates/repository/standard/docs/engineering/harness/EXECUTE_WORK.md",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-011.md",
  "docs/engineering/harness-simplification/specifications/SPEC-KIS-005.md",
  "docs/engineering/harness-simplification/verification/VER-KIS-005.md",
  "docs/engineering/harness-simplification/work-orders/WO-KIS-012.md",
  "docs/engineering/harness-simplification/evidence/WO-KIS-012/",
]

[relations]
implements = ["REQ-KIS-011"]
specifications = ["SPEC-KIS-005"]
verification = ["VER-KIS-005"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T14:21:23Z"
decided_by = "mmzen"
reason = "mmzen explicitly approved REQ-KIS-011, SPEC-KIS-005, VER-KIS-005 and WO-KIS-012 with \"Approve implementation and required verification\". Reviewed SHA-256: 0a2df6d74da2210f269f5fc3dfcb9d9a07773172340815d1dbf0be6f64a77053. This authorizes the two instruction edits, local checks, commits, completion and preparation of required commit-bound verification under VER-KIS-005. WO assurance metadata records that actual decision. Human acceptance and push/PR remain separate."
scope_paths = ["templates/repository/standard/docs/engineering/harness/VERIFY_OUTCOME.md", "templates/repository/standard/docs/engineering/harness/EXECUTE_WORK.md", "docs/engineering/harness-simplification/requirements/REQ-KIS-011.md", "docs/engineering/harness-simplification/specifications/SPEC-KIS-005.md", "docs/engineering/harness-simplification/verification/VER-KIS-005.md", "docs/engineering/harness-simplification/work-orders/WO-KIS-012.md", "docs/engineering/harness-simplification/evidence/WO-KIS-012/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-02T14:23:00Z"
decided_by = "Codex agent"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed. Start the approved two-file instruction change under mmzen's recorded package approval and required commit-bound verification."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-10-02T14:30:35Z"
decided_by = "Codex agent"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed. Implemented the two approved instruction changes and reviewed all REQ-KIS-011 acceptance criteria and six illustrative situations. Final Windows instruction suites passed: 46 tests, no skips. Released validation, integrity, review preflight and the complete Git-derived handoff from 6c675e51e02a063f1c1878b856eb7aab9a723fcd passed. Hosted CI and the separate human verification decision remain pending."
+++

# Deliver clear verification requests

## Objective

Give the human one concise verification request that explains the delivered
outcome, requirement results, material limits and exact decision, with full
record and candidate details available for review.

## In scope

Implement KIS-VRQ-001 through KIS-VRQ-004 through the existing verification
procedure and its implementation-completion pointer. Reuse INT-KIS-001 and
CAP-KIS-001 unchanged. Retain ordinary review evidence and verify the exact
candidate under VER-KIS-005.

## Out of scope

No evaluator, CLI, schema, gate, authority, lifecycle or evidence-capture change.
No new artifact type, request renderer, mandatory receipt or approval stage.
No startup/router, plugin skill, packaging, CI configuration, owner-file or
historical-record edits. Release, installed adoption and external publication
are outside this work.

## Proposed assurance decision

Required commit-bound verification under VER-KIS-005 is proposed because
humans and agents will rely on these instructions when accepting engineering
results. The package approval must confirm this classification. Then record
the actual human and rationale in the assurance metadata before approval.
No human classification is inferred from the request to prepare this package.

## Authorized decision envelope

After package approval and passing start checks, the agent may edit the two
instruction sources within the accepted behavior, run the prescribed checks,
retain evidence, make local commits, record eligible implementation completion
and prepare the required verification record. Human verification remains
separate. Push/PR needs its own authorization.

The agent may choose concise wording and evidence organization within these
paths. A path match does not permit unrelated content changes. Preserve
accepted definitions and decision histories.

## Constraints

Use the exact selected released evaluator 0.21.0 for real governance.
Development source may run the existing tests. Keep instruction anchors,
command operands, decision meanings and current reading routes compatible.
Keep transient working notes outside the repository.

## Expected change surface

| Path | Change and reason |
| --- | --- |
| templates/repository/standard/docs/engineering/harness/VERIFY_OUTCOME.md | Add the concise request to the existing human-decision step; explain evidence gaps, exact reply binding and correction replies. |
| templates/repository/standard/docs/engineering/harness/EXECUTE_WORK.md | Link completion to that request after the required verification preparation. Do not duplicate the card. |
| docs/engineering/harness-simplification/requirements/REQ-KIS-011.md | Carry the reviewed requirement and its evaluator-applied approval. |
| docs/engineering/harness-simplification/specifications/SPEC-KIS-005.md | Carry the reviewed presentation rules and their evaluator-applied approval. |
| docs/engineering/harness-simplification/verification/VER-KIS-005.md | Carry the reviewed verification contract and its evaluator-applied approval. |
| docs/engineering/harness-simplification/work-orders/WO-KIS-012.md | Record the real assurance decision and evaluator-applied lifecycle events for this work. |
| docs/engineering/harness-simplification/evidence/WO-KIS-012/ | Retain the ordinary review, illustrative requests, test results and required start/review/handoff evidence. |

Both instruction sources, the existing implementation-approval card and their
test consumers were inspected. Existing tests already cover links, anchors,
procedure structure, discovery and installation. No test source or fixture
edit is planned for this prose change. The representative cases are reviewed
as prose, not through a new string-matching test.

The same resource paths remain packaged and discoverable. No code, package
manifest, CLI reference, diagnostic index or CI configuration change is needed.

## Generated destinations

The future VREC identity is allocated during preparation. Existing
relationship-based admission covers the record that directly verifies this
work order and its declared evaluator evidence. Check the actual returned
paths after capture; this does not admit neighboring records or directories.
All other planned retained evidence uses the exact directory above.

## Required verification

Perform VER-KIS-005 cases A-C: inspect the instruction diff, review the six
representative situations and run the three existing instruction suites.
Retain skips and limitations. Run the released evaluator's required validation,
integrity, scope and handoff checks. Capture the exact clean candidate.
Hosted integration CI remains a separate observed result.

## Evidence to record

Keep one ordinary review with criterion results and illustrative requests.
Retain check commands, runtime identity, exit codes, output, actual changed
paths, required evaluator evidence and the candidate commit. Preserve failed
attempts and their resolution. Do not edit evidence after it has been captured.

## Stop and escalate conditions

Stop the affected action if it needs another source path, changes an accepted
decision meaning, needs a runtime mechanism, fails a required gate or exposes
an unresolved material verification failure. Report the concrete need and
prepare a bounded correction through the existing procedure.

## Completion report format

Report delivered instruction behavior, actual checks, material limits and
the evaluator's next step. When the captured record is eligible, use the
concise verification request for this change's human review.
