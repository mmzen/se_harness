+++
id = "VER-PLG-019"
type = "verification"
title = "Qualification reconciliation and evidence preservation"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-12"
updated = "2026-09-12"

[relations]
verifies = ["REQ-PLG-008", "REQ-PLG-009", "REQ-PLG-013", "REQ-PLG-014"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-12T07:20:05Z"
decided_by = "assurance-owner"
reason = "The operator replied \"i approve\" to the reviewed packet 29507242f4d17369d242da25f37043fdbdc9f1a3254ff9c01938e6c858845514, explicitly requested under all three owner roles. Record the assurance-owner approval of VER-PLG-019 only; owner-approval.json retains the exact request binding."
+++

# Verification Contract: Qualification reconciliation and evidence preservation

## Independence

Expected boundaries come from the operator's accepted limitation, REQ-PLG-008/009/013/014 and the retained observations at the exact adapter heads.
This contract checks the governance reconciliation, not the adapters' future assurance. The assurance owner reviews the amended criteria independently of their author.
Use released evaluator 0.17.0 outside the checkout on Python 3.11 or later. Existing adapter evidence remains confined to its recorded Windows profiles.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-008, REQ-PLG-009 | inspection, analysis | Q01-Q07 | Both host contracts resolve to one explicit limited-qualification assessment without changing accepted profiles or declaring either adapter qualified. |
| REQ-PLG-013 | inspection, analysis | Q02-Q05 | Healthy current checking and timely running-handler refusal stay mandatory; failed enforcement is retained separately. |
| REQ-PLG-014 | inspection, analysis | Q02-Q07 | Gaps, unavailable cases, unsafe configurations and independent-control limits stay explicit. |

## Acceptance scenarios

| Case | Action | Required observation |
| --- | --- | --- |
| Q01 | Compare every changed path with the exact approved scope; run released doctor, validate and scope/checkpoint checks. | No managed or production file change, no unresolved graph error, and every delta admitted by WO-PLG-019. |
| Q02 | Inspect the six amended definitions and the decision after approved application. | No statement makes C10/C11 pass enforcement; one shared classification governs both adapters; original acceptance is recorded verbatim through decide. |
| Q03 | Assess a known profile with all C01-C09 gates met, current matching evidence, accepted deviation, observed local failures and rejected unsafe variants. | Eligible only for an independent assessment of qualification with documented local limitation; no enforcement or lifecycle decision is inferred. |
| Q04 | Substitute a healthy-path refusal failure, missing context, wrong identity, active asynchronous hook, inadequate active timeout, or unaccepted profile. | Every variant is ineligible for limited qualification; the deviation provides no waiver. |
| Q05 | Substitute a missing/unaccepted deviation, changed source without fresh binding, evidence rewrite, or an unlisted unavailable case. | Every variant is ineligible. Only the expressly approved Codex literal OS shell-start subcase may remain unavailable; it stays unobserved and unenforced. |
| Q06 | Compare pinned production files, canonical C10/C11 records, operator records, terminal activation DECs and historical VRECs/RLSs before/after. | Bytes and recorded verdicts are unchanged; later assessment references historical evidence without rewriting it. |
| Q07 | Inspect proposed/applied decision, amendment receipts and next actions. | Technical, assurance and engineering decisions are separately attributable; revisit text is explicit; no remote protection, adapter completion, qualification or VREC verification is claimed. |

## Property and invariant checks

Compare the proposed classification against the independent counterexample table in the retained review.
An experiment's exit 0, a native permission approval, and passing generic CI never substitute for required enforcement or assurance evidence.
Source identity, package identity, loaded identity, configuration rejection and actual effects are assessed separately.

## Static and architecture checks

Retain the six original/proposed file digests and review their unified diff. ARCH-PLG-002/ADR-PLG-002 responsibility boundaries remain unchanged.
Retain a released-evaluator plan for each requested formal decision before application and the corresponding result afterwards.

## Evidence retention

Use evidence/WO-PLG-019/. Keep initial proposals and their manifest immutable after approval; corrections require a new revision and review.
Retain original failed checks alongside successful retries. The complete before/after source list and observed states must be reproducible from Git.

## Residual uncertainty

This contract does not re-run live-host tests or authenticate future remote decisions. Adapter assurance and protected integration remain separate work.
If an unavailable subcase is excluded from limited qualification, no passing behavior may be inferred for that subcase.
