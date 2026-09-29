+++
id = "WO-HUP-024"
type = "work_order"
title = "Adopt released 0.20.0 in the development repository"
status = "implemented"
owners = ["repository-owner", "engineering-owner"]
created = "2026-09-29"
updated = "2026-09-29"

[assurance]
commit_bound_verification = "required"
rationale = "Later decisions rely on the adopted evaluator, instruction integrity, CI pin and retained upgrade transaction. Human mmzen confirmed the reviewed required classification when approving WO-HUP-024 and VER-HUP-022."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  ".engineering-harness.lock",
  ".engineering-harness.toml",
  ".github/workflows/engineering-harness.yml",
  "ENGINEERING_HARNESS.md",
  "docs/engineering/harness/DEFINE_CHANGE.md",
  "docs/engineering/harness/DELIVER_RESULT.md",
  "docs/engineering/harness/EXECUTE_WORK.md",
  "docs/engineering/harness/PULL_REQUEST.md",
  "docs/engineering/harness/UPGRADE.md",
  "docs/engineering/harness/migration/IMPLEMENTATION_PLAN.md",
  "docs/engineering/instruction-architecture/README.md",
  "docs/engineering/repository-harness-upgrade/README.md",
  "docs/engineering/repository-harness-upgrade/evidence/VREC-HUP-022-evaluator.json",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-024-evaluator-upgrade.json",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-024/",
  "docs/engineering/repository-harness-upgrade/verification-records/VREC-HUP-022.md",
  "docs/engineering/repository-harness-upgrade/verification/VER-HUP-022.md",
  "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-024.md",
  "docs/engineering/templates/WORK_ORDER.template.md",
  "docs/notes/developing-se-harness.md",
  "docs/notes/harness-installation-and-upgrades.md",
  "pyproject.toml",
  "se_harness/__init__.py",
  "tests/test_progressive_documentation.py",
]

[relations]
implements = ["REQ-IAR-022", "REQ-IAR-023", "REQ-IAR-024", "REQ-IAR-025", "REQ-IAR-027", "REQ-IAR-028"]
specifications = ["SPEC-IAR-014", "SPEC-IAR-015"]
verification = ["VER-HUP-022"]
architecture = ["ARCH-IAR-011", "ADR-IAR-011"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-29T20:27:15Z"
decided_by = "engineering-owner"
reason = "Human mmzen: i approve WO-HUP-024 and VER-HUP-022. Approval confirms the reviewed path scope, required commit-bound assurance and explicit WORK_ORDER.template.md replacement. Legacy engineering-owner records that human decision; Codex applies it. Reviewed draft SHA-256 f979b8ce85137918d1ef85ee220ec37218b481535b5cf6b2c74b5171a72945f1"
scope_paths = [".engineering-harness.lock", ".engineering-harness.toml", ".github/workflows/engineering-harness.yml", "ENGINEERING_HARNESS.md", "docs/engineering/harness/DEFINE_CHANGE.md", "docs/engineering/harness/DELIVER_RESULT.md", "docs/engineering/harness/EXECUTE_WORK.md", "docs/engineering/harness/PULL_REQUEST.md", "docs/engineering/harness/UPGRADE.md", "docs/engineering/harness/migration/IMPLEMENTATION_PLAN.md", "docs/engineering/instruction-architecture/README.md", "docs/engineering/repository-harness-upgrade/README.md", "docs/engineering/repository-harness-upgrade/evidence/VREC-HUP-022-evaluator.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-024-evaluator-upgrade.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-024/", "docs/engineering/repository-harness-upgrade/verification-records/VREC-HUP-022.md", "docs/engineering/repository-harness-upgrade/verification/VER-HUP-022.md", "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-024.md", "docs/engineering/templates/WORK_ORDER.template.md", "docs/notes/developing-se-harness.md", "docs/notes/harness-installation-and-upgrades.md", "pyproject.toml", "se_harness/__init__.py", "tests/test_progressive_documentation.py"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-29T20:28:20Z"
decided_by = "Codex executor under mmzen approval"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed. Start approved adoption under DR-015; mmzen approved WO-HUP-024 and VER-HUP-022, required commit-bound assurance and selected template replacement."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-29T20:35:26Z"
decided_by = "Codex executor under mmzen approval"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed. Execution under DR-015 and recorded mmzen approval. Approved 0.20.0 adoption applied; full-scale suite passed 1162 tests with 17 skips. Released identity, doctor, graph validation, qualification, predecessor assessment, distribution validation and complete Git-derived handoff passed. Host delivery and pointer cleanup remain separate; hosted CI required before integration."
+++

# Adopt released 0.20.0 in the development repository

## Objective

Use RLS-SEH-029's public 0.20.0 wheel as the governing evaluator for
`mmzen/se_harness`. Install its released instructions and reconcile the lock.
Keep existing owner pointers for the separately reviewed cleanup. This work
applies the accepted instruction architecture; it adds no product behavior.

## In scope

1. Adopt `se_harness-0.20.0-py3-none-any.whl`, SHA-256
   `7bcfe788c5daaf670bcee25a235663e8210002ce79ffba7162317b1f0509a6e0`.
   Verify its payload digest against RLS-SEH-029's released evidence. Reuse the
   persistent private evaluator environment after execution is authorized.
2. Apply the reviewed released installer plan. Its eight supplied-file updates
   are the configuration, root and six conditional/migration guides. Let the
   installer write its lock; do not edit the lock by hand.
3. Explicitly replace only `docs/engineering/templates/WORK_ORDER.template.md`
   with the released template. The reviewed two-line diff changes the assurance
   placeholder from an accountable role to the actual human and replaces the
   obsolete DECISION_RIGHTS anchor with the current AUTHORITY destination.
4. Retain one upgrade transaction at the exact path listed in execution_scope.
   Preserve AGENTS.md, the six old guide pointers, other owner files and all
   historical formal records. CLAUDE.md remains absent.
5. Change the owner-maintained CI evaluator pin from 0.19.0 to 0.20.0.
6. Advance only the package and source version declarations from 0.20.0 to
   0.21.0. The existing evaluator-facts contract requires a distinct development
   candidate for predecessor assessment. This does not select a release.
7. Update current root/candidate facts in the two selected notes and two domain
   indexes. Preserve historical adoption accounts and public delivery receipts.
   Update the documentation test's pinned installation example to 0.20.0;
   preserve its package-install, preview, apply and doctor ordering checks.
8. Execute VER-HUP-022, retain the results and prepare VREC-HUP-022 with its
   generated evaluator companion at the listed destination.

## Out of scope

Deleting the six owner pointers; replacing customized owner prose; changes to
AGENTS.md or CLAUDE.md; changes to evaluator behavior, source templates or machine
lifecycle policy; accepted-artifact amendments; host/plugin installation;
marketplace publication; tags; package release; push, PR or merge.

## Authorized decision envelope

After human approval, the executor may start, make the selected local changes,
commit them, run checks, retain evidence, record implementation completion and
prepare the verification record through the released procedures. Human
verification acceptance and external delivery remain separate decisions.

Required commit-bound assurance is proposed. Its accountable human has not yet
been recorded. Approval must confirm that classification and the selected
editable-template replacement. This draft records no approval. When applying
the decision under 0.19.0, retain mmzen as the actual human and explain the
required legacy machine role in the transition reason; do not present that
role as a separate human or as an agent-granted decision.

## Constraints

Use locked public 0.19.0 for preparation, approval and start. Use public 0.20.0
for upgrade preview/apply. After successful apply, use the resulting 0.20.0
for governance. Both preview and apply select the same template replacement
and evidence destination. A mismatch outside the expected old-release delta
stops apply. Do not rebuild the published wheel or weaken required checks.

The installation already has no legacy AGENTS/CLAUDE harness block. The preview
requires no retirement receipt. The current chat's host directory is the parent
of the selected checkout; explicit repository selection and a manual root read
restore this session's context. This is not a claim of automatic host delivery.
An actual host-discovery repair or native consumer validation belongs to the
later cleanup preparation; preserve the pointers in this work.

## Expected change surface

The exact execution_scope contains the nine selected installer changes, its
lock, CI pin, two version declarations, four current documentation files, one
documentation test and this package's artifact/evidence destinations. No broad
source or test directory is authorized. The evidence directory admits only
adoption inputs, actual check results and review material for WO-HUP-024.

## Required verification

Complete cases A020-01 through A020-05 in VER-HUP-022. Run the full-scale source
suite, distribution and CLI checks, released identity/doctor/validation,
released-root qualification, predecessor assessment and selected scope/handoff
checks. Bind evidence to the exact candidate commit. Hosted Linux and Windows
checks remain required before integration.

## Evidence to record

Public wheel identity; prior root and lock; selected preview and template diff;
apply and transaction; owner-file comparisons; no-op replay; actual checks and
failed attempts; exact candidate commit; complete changed-path list; generated
verification record and evaluator companion. Retain prior evidence unchanged.

## Stop and escalate conditions

Stop the affected action on a different wheel, customized or unsafe input,
unexpected changed path, unrelated doctor failure, unapproved owner replacement,
failed required check or correction outside the listed paths. Report the exact
finding and prepare only the missing bounded correction for review. Do not
infer cleanup, host support, verification or publication from adoption success.

## Completion report format

Report the selected evaluator and development versions, installer changes,
owner-file preservation, transaction location, actual checks and limitations,
exact candidate and verification record. Obtain the next action from the
released evaluator. Do not claim adoption applied while this record is draft.
