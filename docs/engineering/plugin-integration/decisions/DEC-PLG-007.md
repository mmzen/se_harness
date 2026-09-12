+++
id = "DEC-PLG-007"
type = "decision"
title = "Reconcile plugin ownership with the existing schema-3-only contract"
status = "open"
owners = ["technical-owner"]
created = "2026-09-12"
updated = "2026-09-12"
kind = "question"
question = "May the selected plugin-owned schema-4 design be added as a narrow exception to the existing schema-3-only contracts?"
raised_by = "implementation-planner"
recommendation = "narrow-schema4-exception"

[[options]]
id = "narrow-schema4-exception"
label = "Permit schema 4 only for validated explicit plugin ownership; retain the pre-3 refusal and default schema-3 behavior."

[[options]]
id = "stop"
label = "Keep the existing schema-3-only contract and stop this migration packet before implementation."

[relations]
concerns = ["SPEC-PLG-020", "WO-PLG-020", "ARCH-PLG-003", "ADR-PLG-003", "VER-PLG-020", "REQ-HUP-024", "SPEC-HUP-012", "VER-HUP-012", "SPEC-PMI-001"]
blocks = ["SPEC-PLG-020"]
+++

# Decision: Reconcile plugin ownership with the existing schema-3-only contract

## Question

The reviewed migration packet proposed schema 4 but omitted the current schema-3-only obligation in REQ-HUP-024 and SPEC-HUP-012.
The operator selected delegated execution after reviewing that packet. This additional contract reconciliation has not been approved.
Delegation cannot decide this question or amend the affected contracts on an owner's behalf.

## Options

The recommended narrow exception allows only a validated plugin-owned schema-4 lock under SPEC-PLG-020.
Default repository ownership keeps schema 3, schemas 1 and 2 remain refused, unknown formats remain refused, and integrity/evaluator identity semantics remain unchanged.
The complete alternative is to stop implementation and retain the current schema-3-only contract.

## Concrete reconciliation

The exact four additional contract amendments and the candidate WORKFLOW paragraph are written in the [packet review](../../../notes/plugin-ownership-migration-2026-09-12.md#additional-schema-floor-reconciliation).
They cover REQ-HUP-024, SPEC-HUP-012, VER-HUP-012, and SPEC-PMI-001 without rewriting their historical facts.
The candidate policy source changes later under the WO; the currently installed hash-locked WORKFLOW remains unchanged.
The repository-owned governor-transition assessor stays schema-3-only and makes no schema-4 support claim.

## Disposition

Pending. The technical owner must select the option; the affected definition owners must approve the named applicability amendments.
Only the released evaluator records the decision disposition. This draft applies no lifecycle transition.
