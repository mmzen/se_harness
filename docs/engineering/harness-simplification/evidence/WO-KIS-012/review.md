# Clear verification requests: implementation review

Work: WO-KIS-012. Requirement: REQ-KIS-011. Specification: SPEC-KIS-005.
Verification contract: VER-KIS-005. Reviewer: Codex agent, 2026-10-02.
This is implementation evidence, not the human verification decision.

## Delivered behavior

The existing human-verification step now asks the agent to lead with the
delivered result, meaningful evidence, material limits and the decision's scope.
Record IDs, the full candidate commit and supporting links stay in review details.
Implementation completion points to the existing verification route.

## Requirement assessment

| REQ-KIS-011 acceptance | Inspection result | Evidence |
| --- | --- | --- |
| 1: outcome and requirement evidence | Passed | VERIFY_OUTCOME.md requests delivered behavior and requirement results; test counts cannot replace them. Case 1 below applies that wording. |
| 2: visible gaps and blocked decisions | Passed | The request distinguishes passed, failed and not assessed, names limits and preserves recorded risk decisions. Cases 2 and 3 show the difference. |
| 3: exact decision and review details | Passed | The card names the exact VREC and full candidate, links the WO/VER/assessment/evidence, and separates merge and release. |
| 4: plain replies and unchanged binding | Passed | The instructions bind an unambiguous reply, require clarification for ambiguity and retain reassessment of changed inputs. Cases 4 and 6 apply these rules. |
| 5: correction semantics | Passed | Corrections leave the decision pending and require eligible execution authority. Explicit rejection and supersession still follow their existing procedure. Case 5 applies this boundary. |
| 6: existing route, no additional stage | Passed | The card stays at the existing human-decision heading. EXECUTE_WORK.md links to it after preparation. No startup instruction or new command is added. |

The diff changes two instruction sources. Existing headings and command operands
remain unchanged. No evaluator, gate, schema, packaging or CI file changes.
The formal package and this work's evidence account for the supporting paths.

## Review finding and correction

The first draft tied the generic human-decision action to verification
eligibility. That could also constrain a legitimate explicit rejection when
verification is blocked. The final wording keeps the generic human-decision
action unchanged and limits only the acceptance offer. The separate rejection
and supersession routes remain explicit. The initial passing test run is
retained; the final instruction suites are rerun after this correction.

## Illustrative request review

Everything in the six cases below is synthetic. The identities, outcomes and
replies are example inputs, not actual artifact decisions or host-test results.
The reviewer applied the candidate instructions and compared each response
with the expected meaning in the approved contract. No real lifecycle state
was changed for these examples.

### Case 1: required criteria passed

Input: both required criteria passed for the exact synthetic candidate; the
synthetic verification check permits the decision.

**Verification requested - reject invalid imports**

**Delivered:** Invalid rows are rejected with their row number. Valid rows
continue to import.

**Evidence:** Both agreed criteria passed: invalid rows produce the specified
error, and valid inputs retain their expected result. See the
[criterion results](#synthetic-evidence).

**Limits:** No material gap is known for this example's two required criteria.

**Your decision:** "Verify result" accepts this exact candidate against the
agreed requirements. Merge and release remain separate decisions.

**Review details:** [Exact record and candidate](#synthetic-record),
[work and verification contract](#synthetic-contracts), and
[assessment and evidence](#synthetic-evidence).

Choices: **Verify result** / **Request corrections**.

Observed: the request explains behavior and criterion results before IDs.
It keeps material limits visible and links exact details. Passed by inspection.

### Case 2: a required check is unavailable

Input: the contract requires Linux evidence. None is available. The synthetic
check blocks verification and requests the missing Linux result.

Proposed response: "Verification is blocked: the required Linux criterion is
not assessed because its result is unavailable. The Windows result passed.
The next action is to supply the required Linux evidence."

Observed: no acceptance choice is offered, and Windows success does not hide
the missing required result. Passed by inspection.

### Case 3: a non-required check is skipped

Input: both required criteria passed. An optional large-file benchmark did not
run. It is not an acceptance criterion, and the synthetic gate permits the
verification decision.

Proposed limits field: "The optional large-file benchmark was skipped.
Performance at that size is not established; the required behavior checks
passed. This request does not accept a separate risk or add a performance claim."

Observed: the skipped check stays skipped, and the limit is visible without
inventing a required gate or risk decision. Passed by inspection.

### Case 4: a plain verification reply

Input: the human replies "I verify" immediately to Case 1; its record, candidate,
evidence and authority remain unchanged.

Observed handling: retain the reply against VREC-DEMO-001 and the exact
candidate and evidence shown below, then use the existing transition procedure.
If two unresolved requests make "I verify" ambiguous, clarify which record
the human means. Do not guess or verify both. Passed by inspection.

### Case 5: corrections, rejection and supersession

Input: the human replies "Request corrections: include the row number in the
error." This replaces the assumptions of Case 1 for the example.

Observed handling: leave the verification decision pending, record the issue,
and find an eligible work order before changing implementation. Do not apply
a terminal rejection, reopen a completed work order or infer new scope.

A separate explicit rejection still uses its reason and the existing rejection
procedure. A supersession still names its eligible successor. Neither route
requires a passing verification decision. Passed by inspection.

### Case 6: candidate or evidence changed

Input: after the Case 1 request, the candidate changes from the synthetic
commit below to 2222222222222222222222222222222222222222, or one bound evidence
digest changes.

Observed handling: the earlier reply does not cover the new inputs.
Reassess the selected candidate and evidence and obtain the matching decision.
Do not attach the old answer to the new record. Passed by inspection.

### Synthetic record

Example record: VREC-DEMO-001, state ready.
Example full candidate: 1111111111111111111111111111111111111111.
Example evidence identity: demo-evidence-A, unchanged in Cases 1 and 4.
These values identify the illustrative request only.

### Synthetic contracts

Example work: WO-DEMO-001. Example verification contract: VER-DEMO-001.
Required criteria: invalid rows identify their row number; valid rows retain
their expected result. Case 2 adds a required Linux result as an explicit
different input. No real contract or formal artifact is created here.

### Synthetic evidence

Example criterion 1: passed, error includes the invalid row number.
Example criterion 2: passed, valid rows match expected imported values.
These supplied demonstration inputs are not observed software-test results.

## Automated checks

The final run passed all 46 tests in 34.647 seconds, with no skips.
The initial run also passed all 46 tests; it preceded the review correction.

See instruction-tests-final.log and instruction-tests-final-command.json
for the final actual results and invocation. The earlier successful run is
retained in instruction-tests.log and instruction-tests-command.json.
These are existing tests; no new test source or fixture was needed.

## Simplicity and limits

The smallest complete change is two instruction edits using the current
human-decision step. A parser, renderer, new skill or shared request framework
would add machinery without serving the accepted outcome.

This review establishes content conformance for representative cases, not a
measured usability improvement or proof of every agent's behavior.
Hosted CI has not run for this candidate. No live Codex/Claude session is
needed by VER-KIS-005. Installed instructions change only after release and
adoption. Human verification and external publication remain separate.
