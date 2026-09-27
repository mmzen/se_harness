+++
id = "WO-HUP-021"
type = "work_order"
title = "Adopt public 0.19.0 and its progressive instruction delivery"
status = "implemented"
owners = ["repository-owner", "engineering-owner"]
created = "2026-09-27"
updated = "2026-09-27"

[assurance]
commit_bound_verification = "required"
rationale = "Later decisions depend on the adopted evaluator, instruction delivery, ownership migration and retained upgrade evidence."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  ".engineering-harness.lock",
  ".engineering-harness.toml",
  "AGENTS.md",
  "CLAUDE.md",
  "ENGINEERING_HARNESS.md",
  "docs/engineering/DECISION_RIGHTS.md",
  "docs/engineering/OPERATING_CARD.md",
  "docs/engineering/QUALITY_GATES.md",
  "docs/engineering/TECHNICAL_COMMUNICATION.md",
  "docs/engineering/TRACEABILITY.md",
  "docs/engineering/WORKFLOW.md",
  "docs/engineering/harness/",
  "docs/engineering/repository-harness-upgrade/README.md",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-021/",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-021-evaluator-upgrade.json",
  "docs/engineering/repository-harness-upgrade/verification/VER-HUP-021.md",
  "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-021.md",
  "docs/engineering/repository-harness-upgrade/verification-records/VREC-HUP-021.md",
  "docs/engineering/repository-harness-upgrade/verification-records/VREC-HUP-021.evidence.json",
  "docs/notes/developing-se-harness.md",
  "docs/notes/harness-installation-and-upgrades.md",
  "docs/notes/harness-overview.md",
  "docs/notes/harness-uml-model.md",
  "pyproject.toml",
  "se_harness/__init__.py",
  "tests/test_artifact_catalog.py",
  "tests/test_context_routing_retirement.py",
  "tests/test_instruction_architecture.py",
]

[relations]
implements = ["REQ-IAR-022", "REQ-IAR-024", "REQ-IAR-025", "REQ-IAR-026"]
specifications = ["SPEC-IAR-014"]
verification = ["VER-HUP-021"]
architecture = ["ARCH-IAR-011", "ADR-IAR-011"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-27T20:07:47Z"
decided_by = "engineering-owner"
reason = "User: I approve both wo-hup-021 and ver-hup-021"
scope_paths = [".engineering-harness.lock", ".engineering-harness.toml", "AGENTS.md", "CLAUDE.md", "ENGINEERING_HARNESS.md", "docs/engineering/DECISION_RIGHTS.md", "docs/engineering/OPERATING_CARD.md", "docs/engineering/QUALITY_GATES.md", "docs/engineering/TECHNICAL_COMMUNICATION.md", "docs/engineering/TRACEABILITY.md", "docs/engineering/WORKFLOW.md", "docs/engineering/harness/", "docs/engineering/repository-harness-upgrade/README.md", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-021/", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-021-evaluator-upgrade.json", "docs/engineering/repository-harness-upgrade/verification/VER-HUP-021.md", "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-021.md", "docs/engineering/repository-harness-upgrade/verification-records/VREC-HUP-021.md", "docs/engineering/repository-harness-upgrade/verification-records/VREC-HUP-021.evidence.json", "docs/notes/developing-se-harness.md", "docs/notes/harness-installation-and-upgrades.md", "docs/notes/harness-overview.md", "docs/notes/harness-uml-model.md", "pyproject.toml", "se_harness/__init__.py", "tests/test_artifact_catalog.py", "tests/test_context_routing_retirement.py", "tests/test_instruction_architecture.py"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-27T20:08:54Z"
decided_by = "Codex executor under approved WO-HUP-021"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed. Start the approved bounded adoption and native delivery preparation under DR-015."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-27T20:41:33Z"
decided_by = "Codex executor under recorded human approval"
reason = "Execution of DR-WO-COMPLETE under recorded engineering-owner approval; relevant local gates passed. Completed the approved scope under DR-015. Full-scale suite: 1125 tests, zero failures, 16 skips. Released integrity, qualification, predecessor assessment, review preflight and complete combined handoff passed. Native evidence is limited to Windows Codex CLI startup and manual compaction; hosted CI remains required before integration."
+++

# Adopt public 0.19.0 and its progressive instruction delivery

## Objective

Adopt RLS-SEH-028's public wheel as this repository's governing evaluator.
Install the compact root and conditional guides, establish native delivery,
and leave AGENTS.md entirely repository-owned. This is the separate adoption
required by SPEC-IAR-014 and DEC-IAR-001, with no new product behavior.

## In scope

1. Use public `se_harness-0.19.0-py3-none-any.whl`, SHA-256
   `43419a0c5e7711e7888ed69c207d5599dcd39a4aeb706c8827e7bb33c46573d8`.
   Reuse the existing private evaluator environment.
2. Rehearse the exact planned root with the released-wheel Verity Plane 0.2.0
   package. Configure the selected native host for this repository. Retain
   real startup and post-compaction traces. Review them before authorizing
   retirement of the old entry blocks.
3. Apply the reviewed installer plan: 25 added guides, 8 updated supplied
   files, 24 unchanged files, 2 retired fragments, and the resulting lock.
   Retain the transaction at the exact evidence path in execution_scope.
   No editable-file replacement is selected by the observed preview.
4. Apply the separately reviewed owner edits in
   `../evidence/WO-HUP-021/AGENTS.proposed.md` and its owner-edit map.
   Remove CLAUDE.md only when fragment retirement leaves no owner content.
5. Advance only the two development version declarations to 0.20.0, as the
   existing evaluator-facts contract requires a candidate newer than the root.
6. Update current adoption/setup facts and moved links in the selected notes
   and domain index. Preserve historical accounts and accepted records.
7. Correct the three selected test modules' old-root assumptions: the AGENTS
   fragment, long router and inline TRACEABILITY catalog. Preserve legacy
   fixture coverage and test the adopted ownership and routed catalog.
8. Complete VER-HUP-021, retain results and prepare a commit-bound VREC.

## Out of scope

New evaluator behavior, source-template changes, historical amendments,
exception evaluation, generic accepted-definition revisions, weaker checks,
plugin marketplace publication, package publication, tags, merge and release.
Codex CLI/app-server evidence does not establish Codex desktop support.

## Authorized decision envelope

After approval, the executor may perform local edits, scoped commits, checks,
evidence capture, completion and verification preparation under DR-015.
This draft records no approval.

Local delivery setup may use the exact assembled 0.2.0 package. Inspect existing
host settings first. Preserve unrelated settings and record the selected host,
package path and installation scope. Do not replace the global marketplace or
publish the package. Native test contexts receive read-only delivery probes.

Removal approval requires the real startup/compaction traces and reviewed
owner bytes. Work-order approval does not replace that missing evidence. If
those inputs remain unreviewed, complete delivery preparation and present them
before installer apply. Human verification and integration remain separate.
This work order adds no push, PR, merge or publication authority.

## Constraints

Use governing 0.18.0 for initial lifecycle decisions and start. Use the target
released 0.19.0 for its preview and upgrade; after successful installation,
use resulting 0.19.0 governance. Never edit managed files or states by hand.

Pre-upgrade target doctor failures must be limited to expected version,
payload, new-guide and retired-entry differences. An unrelated failure blocks
apply. Missing native delivery leaves the actual root and old blocks unchanged.

## Expected change surface

The installer controls root, supplied-guide and lock migration. The separate
owner edit, version declarations, notes and test changes use the exact paths
above. The harness/ prefix admits only the 25 released files in the preview.
The machine WORKFLOW.json and QUALITY_GATES.json remain unchanged.

## Required verification

All ADOPT01-ADOPT06 cases in VER-HUP-021, full-scale source tests, distribution
validation, CLI smoke checks, released doctor/validate/qualification, and scope
and handoff checks. Hosted Linux and Windows checks are required before
integration. Corrections must not weaken checks or exceed this scope.

## Evidence to record

Reviewed owner proposal and map; wheel and plugin identities; native traces
and receipt; installer preview and apply; one upgrade transaction; no-op
replay; actual checks and failures; candidate identity; generated VREC.

## Stop and escalate conditions

Stop the affected action on changed release identity, plan conflicts,
unreviewed owner changes, unavailable or stale native delivery, failed gates,
unexpected lifecycle changes or remediation outside the selected paths.
Present the bounded correction and the evaluator's next action.

## Completion report format

Report evaluator and source versions, owner changes, hosts demonstrated,
transaction path, checks, limitations and VREC identity. Use the evaluator's
result for the next decision. Complete only after work and evidence are ready.
