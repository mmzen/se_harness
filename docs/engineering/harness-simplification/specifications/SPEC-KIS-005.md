+++
id = "SPEC-KIS-005"
type = "specification"
title = "Clear human verification requests"
status = "approved"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"
contract = "Present one concise verification request with outcome, evidence, limits and exact decision details at the existing human verification step."

[relations]
specifies = ["REQ-KIS-011"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T14:21:23Z"
decided_by = "mmzen"
reason = "mmzen explicitly approved REQ-KIS-011, SPEC-KIS-005, VER-KIS-005 and WO-KIS-012 with \"Approve implementation and required verification\". Reviewed SHA-256: 986fb6bf5afe7e1bbb5610fe327238d031086c24bd62ca80efebe457c8019361. This authorizes the two instruction edits, local checks, commits, completion and preparation of required commit-bound verification under VER-KIS-005. WO assurance metadata records that actual decision. Human acceptance and push/PR remain separate."
+++

# Clear human verification requests

## Scope

This specification governs the agent's presentation of an existing human
verification decision. The evaluator still decides lifecycle legality.
The verification contract still defines required evidence and pass conditions.

## Rules

**KIS-VRQ-001.** Present the result and decision. At "Obtain the human's
verification decision" in VERIFY_OUTCOME.md, use one concise card:

- **Verification requested - [outcome]:** Name the useful result being assessed.
- **Delivered:** Describe the behavior delivered against the agreed outcome.
- **Evidence:** Summarize the requirement results and meaningful checks. Link
  the requirement-by-requirement assessment and retained evidence. Test counts
  alone are insufficient.
- **Limits:** State material failures, skipped or unavailable checks, unassessed
  criteria and residual uncertainty. If none are known, say so only when the
  evidence supports it.
- **Your decision:** Explain that "Verify result" accepts this exact candidate
  against the agreed requirements. Merge and release remain separate decisions.
- **Review details:** Identify the exact VREC and full candidate commit. Link
  the governing work orders, verification contracts, assessment and evidence.

Offer "Verify result" and "Request corrections" when verification is eligible.
Use ordinary language before identifiers. Details may be linked; the human
must not need to open them to learn about a material gap or the decision's scope.
Scale the explanation to the work. Do not impose a word count or new template
file, persistent receipt, score or UI component.

**KIS-VRQ-002.** Preserve the evidence verdict. Use actual retained results
for the selected candidate. Distinguish passed, failed and not assessed.
Do not convert a skip, unavailable check or unverified platform into a pass.
If the evaluator blocks verification, state the blocker and its next action
instead of presenting acceptance as currently available.

An existing accepted risk may be summarized with its exact decision reference.
A risk without that decision remains unresolved. The verification request must
not silently request a waiver, lower a pass criterion or bundle a risk-acceptance
decision. Required gates and existing authority rules remain unchanged.

**KIS-VRQ-003.** Bind the human's answer. The human need not type IDs, hashes
or commands. An unambiguous "I verify" or "Verify result" applies to the exact
displayed record, candidate and bound evidence, subject to existing authority
and gates. Retain that association before applying the selected transition.
If several requests make the referent ambiguous, clarify it.

Reuse an actual earlier decision only while its record, candidate, evidence
digests, authority and current gates still match. Reassess changed inputs.
Do not treat silence, passing tests or an implementation approval as verification.

"Request corrections" keeps the verification decision pending; it is not a
terminal rejection. Identify the correction and an eligible work order before
implementation. A completed work order does not become executable again.
An explicit rejection or supersession follows its existing procedure and
required reason or successor.

**KIS-VRQ-004.** Use the existing route. Keep the card in VERIFY_OUTCOME.md's
existing human-decision step. EXECUTE_WORK.md points to that step after the
required verification preparation. It does not request a second human approval
merely because implementation is complete.

Keep existing commands, anchors, capture steps, decision rights and lifecycle
semantics. Do not add startup reading, a new gate or command, or duplicated card
instructions in skills, templates and the root router. A work order that needs
no new verification record follows its evaluator-selected route unchanged.

## Examples

These are illustrative review cases, not decisions about actual work.

| Situation | Expected request or response |
| --- | --- |
| Required criteria passed for the captured candidate | Summarize the delivered behavior and criterion results, link the record and full commit, then offer the two choices. |
| A required platform check is unavailable | Show it as not assessed and name the blocker; do not hide it under a total test count or offer acceptance while blocked. |
| A non-required check was skipped | Show any material limit and its relevance; do not relabel the skip as passed. |
| The human replies "I verify" to one exact request | Bind the reply to that displayed record and unchanged inputs; use the existing transition procedure. |
| The human requests a correction | Leave the decision pending and assess correction authority; do not apply a rejection or restart a completed work order. |
| The candidate changes before the reply is applied | Reassess and present the changed candidate; the earlier answer does not authorize it. |

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-KIS-011 | KIS-VRQ-001, KIS-VRQ-002, KIS-VRQ-003, KIS-VRQ-004 |

## Design choice and limits

Two instruction edits meet the agreed need. The current procedure already
collects evidence, obtains a human decision and records its exact target.
A renderer, CLI extension or shared request framework would add code and
maintenance without a requested benefit.

Reuse INT-KIS-001 and CAP-KIS-001 unchanged. REQ-KIS-010 and SPEC-KIS-004
remain unchanged because they govern implementation preparation and approval.
No new architecture boundary or active architecture applies to this
presentation-only requirement. No separate architecture or decision record is
needed. Local review demonstrates instruction clarity for representative cases;
it does not prove every model will always comply or measure user effort.
