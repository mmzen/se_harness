+++
id = "WO-IAR-038"
type = "work_order"
title = "Include the recorded compatibility decision in the reconciled change"
status = "implemented"
owners = ["mmzen"]
created = "2026-10-01"
updated = "2026-10-01"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen confirmed required commit-bound verification within VREC-IAR-020 for the unchanged DEC-IAR-004 and its preservation evidence. Subsequent handoff and assurance rely on this traceability."
decided_by = "mmzen"

[execution_scope]
paths = [
  "docs/engineering/instruction-architecture/decisions/DEC-IAR-004.md",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-038.md",
  "docs/engineering/instruction-architecture/evidence/WO-IAR-038/",
  "docs/engineering/instruction-architecture/verification-records/VREC-IAR-020.md",
  "docs/engineering/instruction-architecture/evidence/VREC-IAR-020-evaluator.json",
]

[relations]
implements = ["REQ-IAR-031"]
specifications = ["SPEC-IAR-016"]
architecture = ["ARCH-IAR-012", "ADR-IAR-012"]
verification = ["VER-IAR-022"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-01T15:55:30Z"
decided_by = "mmzen"
reason = "Human mmzen: I approve. This answers the explicit request to approve WO-IAR-038 and required commit-bound verification within VREC-IAR-020, covering the unchanged DEC-IAR-004 and preservation evidence without changing the decision or product implementation. Reviewed draft SHA-256 3e85e5a8c5f29262412452a54bc8d9fda910e1b1fda4a8470396658e06e963ae. Only the confirmed assurance metadata and matching explanatory paragraph were completed before preview. Codex applies the recorded human decision; no verification acceptance or external action is authorized."
scope_paths = ["docs/engineering/instruction-architecture/decisions/DEC-IAR-004.md", "docs/engineering/instruction-architecture/work-orders/WO-IAR-038.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-038/", "docs/engineering/instruction-architecture/verification-records/VREC-IAR-020.md", "docs/engineering/instruction-architecture/evidence/VREC-IAR-020-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-01T15:56:22Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-10-01T16:18:15Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed."
+++

# Include the recorded compatibility decision in the reconciled change

## Objective

Cover the byte-preserving transport of DEC-IAR-004 in the reconciled branch.
The decision records mmzen's existing choice to release and adopt a compatible
maintenance evaluator before requalifying the minimal-layout candidate.
This work does not make that decision again.

## Observed scope gap

The complete Git scope check from adopted main
`d0157d969d0e3c2d5ed58d218c74abcd28592248` reports one uncovered path:
`docs/engineering/instruction-architecture/decisions/DEC-IAR-004.md`.
Predicate QGP-G4I-PATHS reports WEX201. The existing implementation paths are
covered by WO-IAR-030 and WO-IAR-034 through WO-IAR-037.

DEC-IAR-004 was retained in the original saved checkout. Reconciliation copied
its exact bytes into local commit `c1bcbfb8e053ee8099e98b1dc34fcf547adc46eb`.
That local copy does not authorize formal handoff or external delivery.

## In scope and expected change surface

Transport DEC-IAR-004 unchanged. Record this work order's checks and lifecycle
history. Include its coverage in the already planned aggregate VREC-IAR-020.
The paths above are the complete permitted surface.

## Out of scope

No change to the decision, its disposition, approved definitions, existing
approval history, product code, tests, installed harness, evaluator selection,
release records, native-delivery claims or external state. No push or PR.

## Authorized decision envelope

After approval, the executor may check the preserved record, retain evidence,
make local commits, apply permitted start and completion transitions and prepare
its aggregate verification coverage. Human verification and external actions
remain separate. No new decision may be inferred from the existing DEC record.

## Constraints

Preserve the original saved checkout and all retained failures. Use the selected
released 0.20.1 evaluator adopted under WO-HUP-025. DEC-IAR-004 records the
compatibility sequence; accepted historical artifacts keep their original text.
Desktop delivery remains unverified. This scope correction supplies no missing
behavioral evidence and waives no gate or verification criterion.

## Required verification

Confirm DEC-IAR-004 is byte-identical to the saved decided record and retains
mmzen, the compatibility-release option and its complete lifecycle history.
Run released validation, review preflight and the complete Git-derived scope
and handoff checks against the adopted baseline above. Preserve failures.
Continue the existing VER-IAR-022 assessment; do not treat scope coverage as
proof that all integrated or native criteria pass.

Confirmed assurance: required commit-bound verification in VREC-IAR-020.
Human mmzen answered "I approve" to the explicit WO-IAR-038 and required
verification question. Subsequent handoff and assurance rely on the preserved
decision and its traceability.

## Evidence to record

Retain the source and transported decision digests, actual command results,
review findings and handoff evidence under evidence/WO-IAR-038/.
Use the existing VREC-IAR-020 destinations only if still available at capture.

## Stop and escalate conditions

Stop for changed decision bytes, additional uncovered paths, failed required
checks, missing verification evidence or a changed requested decision.
An unsupported operation does not permit a manual lifecycle edit.

## Completion report format

State the exact preserved decision, candidate, tests, scope result, remaining
qualification gaps and the evaluator's next step. Completion does not verify
the candidate or authorize external delivery.
