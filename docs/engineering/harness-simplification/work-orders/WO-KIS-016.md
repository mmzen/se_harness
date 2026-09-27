+++
id = "WO-KIS-016"
type = "work_order"
title = "Recognize work approval under the human decision-maker identity"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-09-27"
updated = "2026-09-27"

[assurance]
commit_bound_verification = "required"
rationale = "The human confirmed required commit-bound assurance because later execution and assurance decisions rely on the changed approval-grant check."
decided_by = "Requesting human in this conversation (repository owner)"

[execution_scope]
paths = [
  "se_harness/gate_source.py",
  "se_harness/workflow.py",
  "tests/test_delegation_class.py",
  "tests/test_revision_provenance.py",
  "tests/test_workflow_execution.py",
  "docs/notes/delegation-class.md",
  "docs/engineering/harness-simplification/verification/VER-KIS-009.md",
  "docs/engineering/harness-simplification/work-orders/WO-KIS-016.md",
  "docs/engineering/harness-simplification/evidence/WO-KIS-016/",
  "docs/engineering/harness-simplification/evidence/VREC-KIS-016-evaluator.json",
  "docs/engineering/harness-simplification/verification-records/VREC-KIS-016.md",
]

[relations]
implements = ["REQ-KIS-009"]
specifications = ["SPEC-KIS-003"]
verification = ["VER-KIS-009"]
architecture = ["ARCH-KIS-002", "ADR-KIS-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-27T21:05:31Z"
decided_by = "engineering-owner"
reason = "The requesting human in this conversation (repository owner) explicitly answered \"Approve package and compatibility encoding\" to approval of WO-KIS-016 and VER-KIS-009, required commit-bound assurance and this compatibility encoding. The actual accountable human is that requesting repository owner. The engineering-owner CLI label is used only because released 0.19.0 otherwise rejects the execution grant; the human expressly approved this encoding. Reviewed WO SHA-256 ac8a1b207a511c497288cffeb25fbf24e851c7229e0d08c64bf77326cea87876; only the approved assurance metadata completion preceded this transition. Approval covers bounded implementation and verification preparation, not verification acceptance or external delivery."
scope_paths = ["se_harness/gate_source.py", "se_harness/workflow.py", "tests/test_delegation_class.py", "tests/test_revision_provenance.py", "tests/test_workflow_execution.py", "docs/notes/delegation-class.md", "docs/engineering/harness-simplification/verification/VER-KIS-009.md", "docs/engineering/harness-simplification/work-orders/WO-KIS-016.md", "docs/engineering/harness-simplification/evidence/WO-KIS-016/", "docs/engineering/harness-simplification/evidence/VREC-KIS-016-evaluator.json", "docs/engineering/harness-simplification/verification-records/VREC-KIS-016.md"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-27T21:06:11Z"
decided_by = "Codex agent"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed. Start the approved bounded correction under the human-confirmed scope, assurance and compatibility encoding."
+++

# Recognize work approval under the human decision-maker identity

## Objective

An authorized human can approve a work order under their own identity. Its
executor can then start, complete and prepare required verification under
that approval, with the same scope and gate checks as today.

## Recorded defect and governing definitions

Released 0.19.0 accepted WO-HUP-022 approval with
`decided_by = "Requesting human in this conversation (repository owner)"`.
Its start preview then failed QGP-G3-SCOPE with WEX-ECP-022 because the grant
reader required the literal `engineering-owner`. The user subsequently
rejected that work order and approved replacement WO-HUP-023. Preserve both
records and their evidence.

The retained failure is
`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-023/adopt019-022-start-preview.stdout`.
The mismatch is in `se_harness/gate_source.py`; the transition reason also
hardcodes the role label in `se_harness/workflow.py`.

Reuse the approved INT-KIS-003, CAP-KIS-003, REQ-KIS-009, SPEC-KIS-003,
ARCH-KIS-002 and ADR-KIS-002 chain unchanged. In KIS-EXE-002,
engineering-owner denotes the approval accountability, not a person's required
name. The installed AUTHORITY.md explicitly separates identity and authority.
This correction keeps the single execution grant and its accepted boundaries;
it needs no new architecture, lifecycle edge or approval record format.
VER-KIS-009 adds focused regression coverage without rewriting VER-KIS-003.

## In scope

- Recognize a valid recorded work approval regardless of whether the human's
  supplied identity equals the legacy role label. Preserve the recorded name.
- Keep the common approval and unchanged-scope check used by transitions and
  verification preparation. Keep rejection of missing approval, invalid
  approver data, missing usable scope, changed scope and failed required gates.
- Preserve role-labelled approvals and explicit legacy execution grants.
  Do not turn an old approval without such a grant into execution permission.
- Correct messages that equate approval attribution with `engineering-owner`.
- Add regression tests for the named approver and retained boundaries. Update
  the existing execution note, including its current policy links and the
  distinction between installed behavior and candidate behavior.

## Out of scope

No identity authentication service, role-map redesign, new receipt, schema,
configuration mode or decision right. No independent approval, verification
acceptance or release right for agents. No changes to required gates,
workflow edges, installed policies, CI, plugins or package version. No release,
live evaluator upgrade, historical artifact repair, or changes to adoption
evidence. Push, PR creation, merge and publication need their exact authority.

## Authorized decision envelope

After approval of this work order and VER-KIS-009, the executor may choose the
smallest in-scope implementation, maintain focused fixtures, run checks,
retain evidence, create local commits, record completion and prepare the
required VREC. These routine steps use the approved scope and installed checks.
They do not accept the result. Stop for a changed contract or wider scope.

The requesting repository owner is the proposed accountable human for this
package. Owner labels in metadata name responsibilities; they do not assign
identity or grant approval. This draft records no approval decision.

## Constraints and approval handoff

Released evaluator 0.19.0 continues to govern the real repository. Candidate
source is used only to test the proposed behavior. Do not use the candidate
to authorize its own work or edit lifecycle history by hand.

The assurance classification `required` is proposed because the change affects
execution authority. Its `decided_by` is intentionally empty until the human
confirms it. Record the actual confirming human before previewing approval.

The installed evaluator's defect also affects approval of this work order.
Before applying approval, obtain the human's explicit acceptance of the
compatibility encoding already used for WO-HUP-023: use the CLI's required
`engineering-owner` label for this WO approval only, with the actual human and
exact approval recorded in its reason and retained decision evidence. This
encoding is a disclosed workaround, not a claim that the product is fixed.
If it is not accepted, leave this work order in draft; do not first apply an
approval known to be unusable. VER approval retains its actual decision-maker.

## Expected change surface

| Paths | Purpose |
| --- | --- |
| `se_harness/gate_source.py`, `se_harness/workflow.py` | Recognize the approval's supplied identity and report the grant accurately. |
| The three test files in `[execution_scope]` | Exercise public transitions, capture consumers and retained boundaries. |
| `docs/notes/delegation-class.md` | Explain the identity correction and the installed-release boundary. |
| This WO, VER-KIS-009 and the declared evidence/VREC paths | Record the reviewed scope, checks, completion and exact-candidate assurance. |

VREC-KIS-016 is a planned destination, not a prepared record. Recheck ID
availability before capture. A collision requires resolving the destination
and scope before writing; no existing artifact may be overwritten.

## Required verification

Meet VER-KIS-009. Retain a failing named-approver regression before the fix,
passing targeted tests afterward, the repository suite and distribution checks,
and the applicable released validation, doctor, start/review/handoff results.
Run the existing hosted checks at integration. Keep failures and unavailable
evidence visible; no passing local check implies hosted success.

## Evidence to record

Under `docs/engineering/harness-simplification/evidence/WO-KIS-016/`, retain
reviewed input hashes, the actual human decisions, the compatibility encoding,
command arguments, exit codes, output, regression evidence, candidate identity
and the ordinary review. Reference historical WO-HUP-022/023 evidence without
changing it. VREC preparation must bind the exact clean candidate and
VER-KIS-009 at the declared destination.

## Stop and escalate conditions

Stop the affected action if it needs a wider file scope, a changed accepted
definition, weaker authority or gates, rewritten history, an unavailable
required check, or a different VREC destination. An actor name alone must never
supply the missing approval. Report the actual blocker and bounded remedy.

## Completion report format

Report corrected behavior, the preserved authority and legacy boundaries,
changed files, tests and other observed checks, candidate commit, retained
evidence, limitations and the evaluator's next action. Preparing a VREC leaves
it ready for the human verification decision. It does not release or adopt the
candidate.
