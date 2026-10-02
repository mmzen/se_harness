+++
id = "WO-RLS-032"
type = "work_order"
title = "Qualify and deliver plugin 0.2.4 after evaluator publication"
status = "implemented"
owners = ["mmzen"]
created = "2026-10-01"
updated = "2026-10-02"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen approved the reviewed v0.21.0 release package and required commit-bound verification. Later release, publication and availability decisions depend on this work."
decided_by = "mmzen"

[execution_scope]
paths = [
  "docs/engineering/release-0-21-0/",
]

[relations]
implements = ["REQ-PLG-002", "REQ-IAR-030", "REQ-RLO-018"]
specifications = ["SPEC-PLG-001", "SPEC-IAR-016", "SPEC-RLO-006"]
verification = ["VER-RLS-031", "VER-IAR-021"]
architecture = ["ARCH-PLG-001", "ADR-PLG-001", "ARCH-IAR-012", "ADR-IAR-012"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-01T19:53:49Z"
decided_by = "engineering-owner"
reason = "Human mmzen: Approve package and required verification. Approves REL-SEH-033, WO-RLS-031/032/033 and VER-RLS-030/031/032, required commit-bound verification, plugin 0.2.4, ordinary release-review branch push/draft PR and read-only CI rehearsals. Existing v0.21.0 publication authorization is retained. Final-candidate verification, exact RLS decision and unresolved desktop evidence remain separate. Reviewed SHA256 d3fec6f2510b899e68e3420a26a39c6008bd59c482affbf10a8dbc14f8e70bce; transition-input SHA256 e34f1863f64a0da98b0aac5f7e40dc3d67d57a1c1bc84d9ba3735b54b888fb1d. Only confirmed work-order assurance metadata was added. Codex applies the human decision using the selected evaluator role-label encoding; mmzen is the decision-maker."
scope_paths = ["docs/engineering/release-0-21-0/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-02T05:10:49Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-10-02T06:09:26Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed. Local exact-package qualification completed; DEC-RLS-002 accepts only the retained Claude native and Codex Windows desktop gaps. Human verification, marketplace publication and public readback remain separate."
+++

# Qualify and deliver plugin 0.2.4 after evaluator publication

## Objective

Deliver the accepted plugin 0.2.4 source with the exact independently public 0.21.0 evaluator, through the existing marketplace composition.

## In scope

1. Wait for the released RLS and independent public wheel digest readback.
2. Select the approved committed plugin 0.2.4 source. Run the existing marketplace
   builder and independent check into a new external output directory.
3. Run package and genuine native qualification in disposable profiles on the
   claimed hosts. Retain missing host evidence as pending, including desktop.
4. Capture the package VREC and obtain the human verification decision.
5. Present exact package/source/wheel identities and the current marketplace
   parent for external authorization. Publish one ordinary descendant commit to
   mmzen/se_harness:plugin-marketplace only after that authorization and checks.
6. Read back the entire public tree and hand its identity to WO-RLS-033.

## Proposed assurance

Required commit-bound verification is proposed. Later release, publication and
availability decisions rely on this work. Human confirmation is still needed
for this new bounded package. No assurance decided_by or lifecycle approval is
invented. The work remains draft until its approval is recorded.

## Decision envelope

Approval authorizes bounded assembly, native checks, local commits and VREC
preparation after the public-wheel prerequisite. Marketplace publication and its
exact old/new ref remain a separate human action. Do not infer marketplace authority
from the evaluator publication request.

Human mmzen requested "Publish v0.21.0". Preserve that publication authorization
for the matching release once the required immutable inputs and controls exist.
Do not ask again for the same publication action. This request does not supply a
verification verdict on an unprepared candidate or release record. Apply any
later exact human decisions through the selected evaluator; its legacy role
encoding must retain mmzen and the actual decision in the reason.

## Constraints

Use released 0.20.1 outside the checkout as the governing evaluator. Candidate
0.21.0 is only the system under test until separate adoption. Preserve the root
selection, installed instructions, owner files, accepted definitions and earlier
evidence. Reuse existing build, qualification, marketplace and delivery tools.
No new framework, policy edition or automation is needed.

## Required verification

Meet VER-RLS-031 and VER-IAR-021 for the actual package, not another local
wheel or older plugin. Builder check, host validators and native resource identity
must agree before publication. Source tests do not establish public availability.

Codex Windows desktop remains unverified. VER-IAR-021 explicitly requires it;
CLI or app-server traces do not satisfy it. Keep the criterion pending until
matching native evidence exists or a separately authorized formal resolution
changes its applicability. This draft grants no deferral or waiver.

## Evidence and expected change surface

Only this release domain's package records, delivery plan revisions and evidence
are repository writes. Generated plugin output and disposable profiles stay outside
the repository. Preserve both host inventories, archives and native traces.

The execution_scope lists the permitted files. Directory entries admit only this
work's declared release artifacts and evidence, not unrelated changes. Retain
actual commands, full commits, versions, exit codes, failed attempts and digests.
Keep bulky raw logs and disposable profiles outside the repository; keep complete
native traces when the verification contract requires them.

## Out of scope

Changing shared runtime source, manifest versions after qualification, altering
public immutable packages, repository adoption, real-profile changes, credentials,
provider-directory submissions, force pushes and unreviewed marketplace ref changes.

## Stop conditions

Stop the affected step for changed or occupied identities, missing verification,
an unassessed required criterion, unsafe or customized input, failed checks,
out-of-scope edits, unavailable independent controls, or an advanced destination
ref. Preserve original failures. Inspect uncertain external effects before retry.

## Completion report

Report the exact candidate/package identity, actual checks and limitations,
formal record state, completed external effects and remaining delivery surfaces.
No missing or pending result may be reported as passed or complete.
