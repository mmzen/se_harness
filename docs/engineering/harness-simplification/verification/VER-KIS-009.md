+++
id = "VER-KIS-009"
type = "verification"
title = "Verify execution grants with named human approvers"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-27"
updated = "2026-09-27"

[relations]
verifies = ["REQ-KIS-009"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-27T21:04:58Z"
decided_by = "Requesting human in this conversation (repository owner)"
reason = "The requesting human in this conversation (repository owner) explicitly answered \"Approve package and compatibility encoding\" to approval of WO-KIS-016 and VER-KIS-009, required commit-bound assurance and the disclosed 0.19.0 compatibility encoding. Reviewed VER SHA-256 d0d756c218d4341429ef8b2a97dc22b4e9d8c61dd67dc525278326efa8bf7b8f. This records definition approval only; no assurance acceptance or external delivery."
+++

# Verify execution grants with named human approvers

## Independence

Expected results come from REQ-KIS-009 and SPEC-KIS-003, especially
KIS-EXE-001, 002, 003, 005 and 007. The installed AUTHORITY.md distinguishes
the accountable person's identity from their decision right. A recorded
approval must support execution without making the person use a role name.
This contract adds regression coverage; it does not change those definitions.

Use independently specified fixture identities and expected states. Do not
derive expected results from the candidate's approval filter. Retain the
observed WO-HUP-022 failure as historical evidence; do not rerun transitions
against that rejected work order or change its history.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-KIS-009 | test | A: approval and start | A selected eligible WO approved under an actual human identity starts under a human or agent executor. The original approval identity and scope remain unchanged. |
| REQ-KIS-009 | test | B: completion and capture | The same grant supports completion and required VREC preparation when their checks pass. Capture checks every selected WO and leaves the VREC `ready`. |
| REQ-KIS-009 | test | C: retained boundaries | Missing approval, missing usable scope, invalid approver, changed scope, or a failed required gate blocks the affected operation without writes. Executor names do not bypass a check. |
| REQ-KIS-009 | test | D: legacy grants | Existing role-labelled approvals and earlier explicit execution grants still work. An old approval without an execution grant remains blocked. Reading history does not rewrite it. |
| REQ-KIS-009 | inspection | E: authority and explanation | One shared grant check remains in use. Messages describe the recorded work approval without asserting that the person's identity is `engineering-owner`. Human-reserved decisions remain separate. |

## Checks and execution conditions

**A. Reproduce the mismatch through the CLI.** In a temporary fixture, apply
WO approval using a valid human name other than `engineering-owner`, including
a name with spaces. Supply the same authorized decision and scope for the
role-labelled comparison. Preview and apply start. Check that the named
approval follows the same gates as the comparison and that the executor's
identity is recorded separately. Retain the regression failure before the fix
and its result afterward. Keep fixtures outside the real artifact graph.

**B. Exercise the consumers.** Use eligible fixtures with passing handoff and
candidate evidence. Complete a WO approved by the named human, then capture
its verification record through the public command. Also cover selected
multi-WO capture: one WO lacking its required grant must block preparation
without partial output. The result must not verify or release anything.

**C and D. Reuse and extend boundary tests.** Keep the existing missing
approval, changed scope, failed completion gate, historical scope lookup,
explicit legacy delegation, and absent legacy grant cases. Add empty or
malformed approver coverage at the boundary that rejects it. Do not accept
`status = "approved"`, a role label, or current delegation metadata alone as
an execution grant. Exercise checks under both human and agent executor names.
Reserved definition, assurance and release rights must remain unavailable
through the execution grant. No test requires a new authentication service.

**E. Inspect the focused diff.** Check the common grant consumer, transition
reasons and current explanatory note. Preserve operation IDs, lifecycle edges,
required gates, legacy grant meaning and formal history. Treat the supplied
identity as attribution under the existing authority model, not independent
proof that a human approved. Record this limit in the review.

Run targeted tests with the candidate source:

```text
python -m unittest tests.test_delegation_class tests.test_revision_provenance tests.test_workflow_execution
```

Then run `python scripts/run_tests.py`,
`python scripts/validate_release_distributions.py --root .`, and
`python -m se_harness --help`, following repository build prerequisites.
Use Windows locally and the existing Linux/Windows CI jobs at integration.
Report unavailable or skipped evidence explicitly. Use released evaluator
0.19.0 for real repository validation, doctor, selected start/review/handoff
checks, lifecycle writes and commit-bound verification preparation. Candidate
source tests exercise the future behavior; they do not govern this work.

## Evidence retention

Retain commands, inputs, exit codes, output, candidate commit, regression
results and the ordinary review under the selected WO's declared evidence
directory. Keep failed attempts. The VREC must bind the exact clean candidate,
selected WO and this contract. Do not claim CI success from local tests.

## Residual uncertainty

The released 0.19.0 evaluator still has the reported defect. Passing candidate
tests does not fix the installed evaluator. Release and repository adoption
are separate actions. This change neither authenticates human identities nor
repairs rejected historical work orders.
