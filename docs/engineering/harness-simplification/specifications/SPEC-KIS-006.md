+++
id = "SPEC-KIS-006"
type = "specification"
title = "Match repository protection to the stated approval policy"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-19"
updated = "2026-09-20"

contract = "Apply the selected owner-review policy at integration and publishing, protect control changes, and keep local asserted authority separate from authenticated owner decisions."

[relations]
specifies = ["REQ-KIS-012"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-20T06:27:29Z"
decided_by = "technical-owner"
reason = "On 2026-09-20 the owner approved the presented recovery artifact package with \"i approve\". Record approval of this reviewed artifact in the named owner role. Reviewed full-byte SHA-256: 5b16814f0a378da908f27fbdfbf6c7f7b8c032145e2aa81a32ec763e8175e4c1. DEC-KIS-001 separately records the explicit owner-review choice. WO approval grants the bounded execution operations in DR-015; this transition records no implementation result, assurance acceptance or external action."
+++

# Match repository protection to the stated approval policy

## Scope

Apply the selected owner-review policy at integration and publishing, protect control changes, and keep local asserted authority separate from authenticated owner decisions.
This is the prospective contract for WO-KIS-012; creation does not change installed behavior.

## Rules

**KIS-PRT-001.** Before proposing live edits, inspect the effective current rules, active workflow jobs, publishing routes and bypass permissions of mmzen/se_harness. Retain a concise dated before/after record. September 16 observations are a baseline, not a statement of current settings. Select actual acceptance statuses from the existing candidate and governance jobs; do not duplicate the pipeline.

**KIS-PRT-002.** Resolve DEC-KIS-001 before approving WO-KIS-012 or applying its target controls. These definitions describe both choices without selecting one. In the independent-review option, require a qualified human other than the author to approve the latest reviewable candidate and prevent self-review at the relevant publication gate. In the owner-review option, retain explicit owner acceptance of the exact candidate and describe the guarantee as owner-controlled, including any documented bypass. Never invent a second identity or claim independent assurance from one person.

**KIS-PRT-003.** Require the applicable acceptance checks at the normal merge boundary. Review changes to checking workflows, selected evaluator versions, owner rules, evidence contracts and approval records as control changes. Scope owner review through existing host ownership features. Routine agent credentials must not change protections or use an administrative bypass. A check name alone is not proof that the expected checker ran.

**KIS-PRT-004.** Retain the actual owner decision reference and reviewed version in the existing decision record or review evidence. Review the proposed purpose, file scope, governing requirements and pass conditions against that version. A changed purpose, wider scope, weakened acceptance or changed governing requirement requires the existing amendment decision. Ordinary in-scope coding reuses approval. Locally typed names and edited events remain assertions, never authenticated proof.

**KIS-PRT-005.** Reuse protected host review and existing CI as the minimum control. Human review of an editable workflow remains an owner-controlled safeguard. Claim automatic resistance to candidate workflow replacement only after a required checking entry point outside candidate control has been configured and demonstrated using supported host features. If unavailable, record that limit rather than adding a custom authentication, signing or policy service.

**KIS-PRT-006.** Inspect every currently used publishing route and apply the selected reviewer and credential policy at that boundary. Offline local work remains permitted under unchanged actual authority. Installing this product or approving this WO alone does not authorize live repository-rule changes, credential changes, merge, publication or deployment; those actions need their exact target-specific authorization and applicable checks.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-KIS-012` | KIS-PRT-001, KIS-PRT-002, KIS-PRT-003, KIS-PRT-004, KIS-PRT-005, KIS-PRT-006 |

## Examples and failure behavior

- **Normal:** The selected review policy is recorded, required checks succeed for the current candidate, and the responsible human reviews the actual change before the permitted integration action.
- **Failure:** A required test is missing or failed, a required current review is absent, or an approval scope is expanded without the owner decision. The normal protected route refuses, or the owner-controlled residual is clearly recorded where enforcement is unavailable.

Refusal names the failed criterion or missing input and does not imply an applied state change.
Use an existing diagnostic when its meaning fits; do not reserve new codes in this draft.

## Compatibility and KISS review

The owner and executor trust model remains the existing single local route. This makes boundary claims and review practice explicit without turning local approval into authenticated identity. SPEC-KIS-001/003 continue to permit local progress without live CI. DEC-KIS-001 selects the feasible host review guarantee; it is not a product runtime mode.

Reuse existing components and remove obsolete tests and instructions with the behavior
they described. No new artifact type, approval service, runtime mode or score is required.
These are repairs within the existing component responsibilities: no new architecture
is introduced and no active architecture addresses this new requirement. If implementation
reveals a material structural or trust-boundary change, obtain a bounded architecture
decision before that change rather than silently expanding this repair.
