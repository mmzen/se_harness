+++
id = "SPEC-KIS-007"
type = "specification"
title = "Give agents one consistent route with bounded reading"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-19"
updated = "2026-09-20"

contract = "Use one action/authority explanation and the existing workflow result for a short selected-task brief, with explicit limits and simple coordinated ID allocation."

[relations]
specifies = ["REQ-KIS-013"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-20T06:27:29Z"
decided_by = "technical-owner"
reason = "On 2026-09-20 the owner approved the presented recovery artifact package with \"i approve\". Record approval of this reviewed artifact in the named owner role. Reviewed full-byte SHA-256: 8f361ce56f76d23408bd8aeab65430612376f8e12233547f415bc8d90522e212. DEC-KIS-001 separately records the explicit owner-review choice. WO approval grants the bounded execution operations in DR-015; this transition records no implementation result, assurance acceptance or external action."
+++

# Give agents one consistent route with bounded reading

## Scope

Use one action/authority explanation and the existing workflow result for a short selected-task brief, with explicit limits and simple coordinated ID allocation.
This is the prospective contract for WO-KIS-013; creation does not change installed behavior.

## Rules

**KIS-GDE-001.** Reconcile candidate DECISION_RIGHTS, WORKFLOW and OPERATING_CARD explanations. One role/action/authority table must identify which approval already covers each operation and which owner decision remains. Replace conflicting start/completion statements and link repeated explanations to that table. Installed executable policy remains authoritative.

**KIS-GDE-002.** Approved executors may start, implement, check, record qualifying completion and prepare required verification without renewed permission while inputs and gates still match. Preparation never approves definitions, assurance, release or external actions. Guides and plugin skills must preserve actual command argument boundaries and separate a projected next action from evaluated readiness.

**KIS-GDE-003.** At the top of the existing result, present the selected work, exact governing checker version, relevant scope, current blockers, remaining decision and one next action. Link to the full selected contracts and reading manifest. Keep requirement and acceptance details that affect the task; remove repeated prose rather than creating another policy file or generator framework.

**KIS-GDE-004.** Use the existing human/task coordinator to allocate non-overlapping blocks of record numbers once per active task. Check published refs and active allocations, use the ordinary artifact creator, and detect duplicates before integration. Record the allocation in the existing task handoff. This does not guarantee uniqueness among uncoordinated writers and does not require a new service or central database.

**KIS-GDE-005.** Observe a fresh-agent and a resumed-agent task through the existing acceptance setup. Verify correct evaluator selection, no unnecessary routine permission requests, an actual stop at an ungranted owner decision, and honest reporting of failed/unknown checks. A deterministic command replay alone is insufficient evidence of agent behavior.

**KIS-GDE-006.** Ship candidate policy and skill updates through normal release and explicit adoption. Reconcile preserved editable guides during upgrade. Do not rewrite root locked policy, previous approvals or historical evidence while implementing this package. Keep the existing one-route and KISS rules.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-KIS-013` | KIS-GDE-001, KIS-GDE-002, KIS-GDE-003, KIS-GDE-004, KIS-GDE-005, KIS-GDE-006 |

## Examples and failure behavior

- **Normal:** A fresh agent and a resumed agent use the project-selected checker, execute ordinary approved steps and stop at the actual assurance decision without repeated permission prompts.
- **Failure:** A task brief lacks a required decision or a relevant contract. The agent identifies that specific gap rather than treating the proposed next command as approval.

Refusal names the failed criterion or missing input and does not imply an applied state change.
Use an existing diagnostic when its meaning fits; do not reserve new codes in this draft.

## Compatibility and KISS review

This corrects explanations of the authority already established by SPEC-KIS-003. It retains the shared simplicity policy in SPEC-KIS-002 and does not invent a second source of lifecycle rules. The brief is a view of the selected result, not a replacement for its governing contracts.

Reuse existing components and remove obsolete tests and instructions with the behavior
they described. No new artifact type, approval service, runtime mode or score is required.
These are repairs within the existing component responsibilities: no new architecture
is introduced and no active architecture addresses this new requirement. If implementation
reveals a material structural or trust-boundary change, obtain a bounded architecture
decision before that change rather than silently expanding this repair.
