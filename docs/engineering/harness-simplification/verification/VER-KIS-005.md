+++
id = "VER-KIS-005"
type = "verification"
title = "Verify clear human verification requests"
status = "approved"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"

[relations]
verifies = ["REQ-KIS-011"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T14:21:23Z"
decided_by = "mmzen"
reason = "mmzen explicitly approved REQ-KIS-011, SPEC-KIS-005, VER-KIS-005 and WO-KIS-012 with \"Approve implementation and required verification\". Reviewed SHA-256: 94df197f68c44e6965ba9dfe352722171591d95d1683d3f983412c737e36742f. This authorizes the two instruction edits, local checks, commits, completion and preparation of required commit-bound verification under VER-KIS-005. WO assurance metadata records that actual decision. Human acceptance and push/PR remain separate."
+++

# Verify clear human verification requests

## Independence

Derive expected results from REQ-KIS-011 and SPEC-KIS-005 before reviewing the
instruction edits. Agent inspection and examples are evidence, not the human
verification decision. The accountable human assesses the exact captured
candidate. Do not treat example replies as actual authority.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-KIS-011 | inspection | A: instruction diff and ordinary review | The six card fields appear at the current verification-decision step. Implementation completion links to it after preparation. Commands, anchors, gates and decision meanings remain unchanged; no startup content or new stage is added. |
| REQ-KIS-011 | demonstration | B: illustrative request review | The cases below show actual criterion results, visible limits, exact decision binding and correct handling of blocked or changed inputs. |
| REQ-KIS-011 | test | C: existing instruction checks | The existing instruction architecture, progressive discovery and workflow documentation contract suites pass, with actual skips retained. |

## Illustrative request review

Prepare short examples in the ordinary review evidence for these cases:

1. Required criteria passed: show the delivered outcome and meaningful results,
   with a record and full candidate identity in details. State the decision's
   scope and offer "Verify result" and "Request corrections".
2. A required check is unavailable: show not assessed, the blocker and the
   next corrective action. Do not offer acceptance while blocked.
3. A non-required check is skipped: explain any material limit without calling
   the check passed or silently accepting its risk.
4. One exact request receives "I verify": identify the displayed record and
   unchanged inputs to which the reply applies. An ambiguous reply across
   multiple records requires clarification.
5. "Request corrections": leave the decision pending, identify the correction
   and require eligible execution authority. Do not reject automatically.
6. The candidate or bound evidence changes: do not reuse the old answer for
   the new inputs. Preserve explicit rejection and supersession routes.

Label these as illustrative. Check the expected meaning by inspection; do not
add a parser, test service or simulated decisions on real artifacts. Retain
failed review attempts and corrections if any.

## Commands and platforms

On local Windows, run the existing suites from the source checkout:

    python -B -m unittest tests.test_instruction_architecture tests.test_progressive_instruction_discovery tests.test_workflow_documentation_contract

These exercise instruction content, links, procedure discovery and existing
installation behavior. Use the configured development Python and retain its
exact executable, version, arguments, exit code and results.

Use the selected released evaluator 0.21.0 for real artifact validation,
integrity, scope, handoff and verification capture. Candidate source remains
limited to development tests. Existing hosted CI runs at integration; a local
pass does not establish CI success. No new runtime behavior is introduced,
so no live model session, credentials or desktop demonstration is required.

## Evidence retention

Retain one ordinary review, the representative requests and observed results,
test output, required harness evidence and exact invocation details in the
selected work order's evidence directory. Capture a VREC against the exact
clean candidate through the released evaluator. Keep its evidence bytes
unchanged after capture.

## Residual uncertainty

This verifies the instruction text and its existing delivery paths.
Representative examples do not prove all agents will comply or establish a
measured improvement in human comprehension. Installed agents receive the
changed instructions only through a later release and adoption.
