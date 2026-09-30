+++
id = "WO-IAR-032"
type = "work_order"
title = "Transport the approved external-resource package in its pull request"
status = "implemented"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-09-30"

[assurance]
commit_bound_verification = "not_required"
rationale = "Solely transports the publication decision already authorized by human mmzen; frozen definitions, implementation and evidence are unchanged."
decided_by = "mmzen"

[execution_scope]
paths = [
  "docs/engineering/instruction-architecture/architecture/ARCH-IAR-012.md",
  "docs/engineering/instruction-architecture/architecture/adr/ADR-IAR-012.md",
  "docs/engineering/instruction-architecture/decisions/DEC-IAR-003.md",
  "docs/engineering/instruction-architecture/requirements/REQ-IAR-029.md",
  "docs/engineering/instruction-architecture/requirements/REQ-IAR-030.md",
  "docs/engineering/instruction-architecture/requirements/REQ-IAR-031.md",
  "docs/engineering/instruction-architecture/specifications/SPEC-IAR-016.md",
  "docs/engineering/instruction-architecture/verification/VER-IAR-020.md",
  "docs/engineering/instruction-architecture/verification/VER-IAR-021.md",
  "docs/engineering/instruction-architecture/verification/VER-IAR-022.md",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-032.md",
  "docs/engineering/instruction-architecture/evidence/WO-IAR-032/"
]

[relations]
implements = ["REQ-IAR-029"]
specifications = ["SPEC-IAR-016"]
architecture = ["ARCH-IAR-012", "ADR-IAR-012"]
verification = ["VER-IAR-020"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-30T12:09:56Z"
decided_by = "mmzen"
reason = "Human mmzen confirmed: Approve WO-IAR-032 and classification. Approves transport of the ten unchanged already-approved files and not_required assurance; existing authorization covers push and PR followed by WO-IAR-029. Reviewed draft SHA-256 bcdc8eddc762a906a4b0dfa93812c2ee37efed2d6507ae0da4fdfb288eeda80c. Only confirmed assurance metadata and its explanatory paragraph were completed before preview."
scope_paths = ["docs/engineering/instruction-architecture/architecture/ARCH-IAR-012.md", "docs/engineering/instruction-architecture/architecture/adr/ADR-IAR-012.md", "docs/engineering/instruction-architecture/decisions/DEC-IAR-003.md", "docs/engineering/instruction-architecture/requirements/REQ-IAR-029.md", "docs/engineering/instruction-architecture/requirements/REQ-IAR-030.md", "docs/engineering/instruction-architecture/requirements/REQ-IAR-031.md", "docs/engineering/instruction-architecture/specifications/SPEC-IAR-016.md", "docs/engineering/instruction-architecture/verification/VER-IAR-020.md", "docs/engineering/instruction-architecture/verification/VER-IAR-021.md", "docs/engineering/instruction-architecture/verification/VER-IAR-022.md", "docs/engineering/instruction-architecture/work-orders/WO-IAR-032.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-032/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-30T12:10:24Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-30T12:15:53Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed."
+++

# Transport the approved external-resource package

## Objective and bounded correction

Include the ten existing approved definition/decision files in the authorized
pull request for the external-resource work. The released 0.20.0 check-pr
rejects the complete diff from main because these paths were omitted from the
implementation work orders. Drafting and approving the package was permitted;
this correction covers its transport in that same PR. Preserve all earlier
approvals, implementation and verification records.

## Exact content and constraints

The first ten execution_scope paths must remain byte-identical to commit
ffe41ce4dae358cc966430907d645ebded9f91c9. They are ARCH-IAR-012, ADR-IAR-012,
DEC-IAR-003, REQ-IAR-029 through REQ-IAR-031, SPEC-IAR-016, and VER-IAR-020
through VER-IAR-022. This work does not amend their content, links or decisions.
Only this work order's lifecycle record and its small transport/check evidence
are new repository writes. Source, tests, installed harness files, existing
evidence and accepted definitions remain unchanged.

## Confirmed assurance classification

Human mmzen confirmed commit_bound_verification = "not_required":
"Approve WO-IAR-032 and classification".
This work solely transports the publication decision already supplied by human
mmzen: "you can push and PR and then start next work order". It changes none of
the definitions, implementation or evidence behind that decision. VREC-IAR-018
remains verified for its exact candidate. No additional assurance acceptance is
claimed; all required validation, scope and delivery checks remain required.
This human decision permits the assurance metadata and approval transition;
no assurance acceptance is inferred for any changed content.

## Execution and delivery authority

Approval permits local evidence retention, permitted lifecycle transitions and
commits for this bounded transport correction. Existing separate human authority
covers pushing work/external-harness-resources to mmzen/se_harness and opening its
PR against main after required checks pass. It does not authorize merge, a product
release or marketplace publication. After opening the PR, start already-approved
WO-IAR-029 under its own scope, as the human requested.

## Verification and evidence

Use released 0.20.0 to validate and run start/review preflight. Compare every
transported file byte-for-byte against the exact commit above and compare source,
tests and package inputs against the verified implementation. Reuse VER-IAR-020's
retained results because those inputs are unchanged; this work adds no runtime
behavior to test. Retain that comparison and the original failed PR check under
this work order's evidence directory.

Run the released combined check-pr against the full main comparison base
4a03dabcd632976b8262f5f516b1810a850e2209, with all selected work orders covering
the complete diff, including this work order. Do not narrow the diff to hide the
package files. Run the existing integration pre-action check for VREC-IAR-018.
Retain actual gate results and the eventual PR URL and remote commit readback.
Generated packets use harnessctl evidence; their binding fields are tool-owned.

## Stop conditions and completion

Stop for any changed frozen file, uncovered path, failed required check, changed
candidate/evidence, or missing external control. A content change requires its
own authority and assurance classification. Complete when the reviewed transport
scope is covered, required checks pass and evidence is retained. Report actual
local and remote effects separately. This draft supplies no approval.
