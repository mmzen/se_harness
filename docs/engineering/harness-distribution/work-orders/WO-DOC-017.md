+++
id = "WO-DOC-017"
type = "work_order"
title = "Restore the approved README starting path"
status = "implemented"
owners = ["engineering-owner", "documentation-owner"]
created = "2026-09-20"
updated = "2026-09-20"

[assurance]
commit_bound_verification = "required"
rationale = "Readers rely on installation guidance, and recovery completion relies on the corrected repository checks."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "README.md",
  "docs/engineering/harness-distribution/verification/VER-DST-030.md",
  "docs/engineering/harness-distribution/work-orders/WO-DOC-017.md",
  "docs/engineering/harness-distribution/evidence/WO-DOC-017/",
  "docs/engineering/harness-distribution/verification-records/VREC-DOC-009.md",
  "docs/engineering/harness-distribution/evidence/VREC-DOC-009-evaluator.json",
]

[relations]
implements = ["REQ-DST-069"]
specifications = ["SPEC-DST-024"]
verification = ["VER-DST-030"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-20T08:30:03Z"
decided_by = "engineering-owner"
reason = "On 2026-09-20 the owner replied \"i approive\" to the reviewed README package, explicitly approving WO-DOC-017 and the proposal. Reviewed artifact SHA-256: 3a501912ad01097a4dffdb18aceea958be4e61ef6f1dd8b16f3c36d11eb295cb. Reviewed README SHA-256: 6566a636021d3aaa29345094ad19362289cd26efe01b3684a26da57e7c2d2c9d. This records the named formal approval; no assurance acceptance or external delivery is granted."
scope_paths = ["README.md", "docs/engineering/harness-distribution/verification/VER-DST-030.md", "docs/engineering/harness-distribution/work-orders/WO-DOC-017.md", "docs/engineering/harness-distribution/evidence/WO-DOC-017/", "docs/engineering/harness-distribution/verification-records/VREC-DOC-009.md", "docs/engineering/harness-distribution/evidence/VREC-DOC-009-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-20T08:30:59Z"
decided_by = "delegated-executor"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed. Codex starts the exact owner-approved README restoration under DR-015."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-20T08:38:51Z"
decided_by = "delegated-executor"
reason = "Execution of DR-WO-COMPLETE under recorded engineering-owner approval; relevant local gates passed. Codex completed the reviewed README restoration. The applied 32 documentation tests and both 1081-test Windows/Ubuntu source suites pass; released doctor, graph, review and Git-derived handoff passed. Actual results and limitations are retained under evidence/WO-DOC-017. No assurance or delivery decision is inferred."
+++

# Restore the approved README starting path

## Objective and exact input

Restore the missing CLI setup and two documentation links so new users have
the starting path already required by REQ-DST-069 and SPEC-DST-024. The 12
onboarding assertion failures predate the recovery work. They block the
required full suite under WO-KIS-014; this separate order owns their repair.

The proposed README restores the CLI section from retained approved-readme.md
under evidence/WO-DOC-016/ and preserves the two navigation links already added
on origin/main at 2b87e04490b933a71a9986c0235ea8b201b3bffc.
Complete proposal SHA-256: 6566a636021d3aaa29345094ad19362289cd26efe01b3684a26da57e7c2d2c9d.
It contains 604 source words, 110 lines and six level-two headings.
The review package supplies the complete README and its exact patch.
The owner's "ok for your plan" authorizes preparing this repair for review;
this draft records no approval of its new formal records.

## In scope and simplicity

Restore only README.md and keep the scoped verification/work/evidence records.
Keep the existing plugin path, add back the previously reviewed Windows/Linux
CLI environments, init/doctor examples, existing-project explanation and links.
Reuse the existing approved requirement/specification and existing tests.
VER-DST-030 provides a current check plan because the older verification
contracts name historical work orders, evidence paths and publication inputs.
No architecture addresses REQ-DST-069; this text restoration needs no ADR.

## Execution and limits

After actual approval, the executor may start, apply the reviewed README,
run checks, retain evidence, make ordinary local commits, record qualifying
completion and prepare VREC-DOC-009 through released 0.18.0 procedures.
Ordinary evidence naming within the listed folder is an implementation choice.
The exact README bytes are fixed for this restoration; material changes return
for review. Local execution follows DR-015 without duplicate start/completion
permission. Assurance acceptance remains the owner's separate decision.

Product code, tests, other documentation, managed root policy, package metadata,
historical evidence/approvals and the scopes of WO-KIS-014/011/012/013 are
unchanged. No push, PR, merge, release, publication, live settings change or
promotable build is authorized. This does not restart historical WO-DOC-016.

## Verification, stop and handoff

Meet VER-DST-030 and repository-required checks. Record this order's actual
change set from its implementation base and preserve the earlier scope/test
evidence for WO-KIS-014. Do not hide either change under a different base.
Before combined acceptance, verify each selected order's evidence and scope.

Stop affected work for changed inputs/scope, invalid managed integrity or
governing chain, overlapping owner changes, required failed checks, uncertain
writes or missing decision rights. Report actual changes, checks, limitations,
state and the released schema-2 result's next accountable action. Completion,
VREC preparation, owner acceptance and delivery remain separate facts.
