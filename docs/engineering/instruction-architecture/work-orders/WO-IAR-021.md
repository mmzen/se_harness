+++
id = "WO-IAR-021"
type = "work_order"
title = "Correct instruction references and context guidance"
status = "draft"
owners = ["engineering-owner"]
created = "2026-09-28"
updated = "2026-09-28"

# Assurance is proposed in the body. Add the complete decision table only
# after the accountable human confirms it, before approval.

[execution_scope]
paths = [
  "templates/repository/standard/docs/engineering/templates/WORK_ORDER.template.md",
  "templates/repository/standard/docs/engineering/README.md.seed",
  "templates/repository/standard/docs/engineering/harness/EXECUTE_WORK.md",
  "templates/repository/standard/docs/engineering/harness/DEFINE_CHANGE.md",
  "templates/repository/standard/docs/engineering/harness/DELIVER_RESULT.md",
  "templates/repository/standard/docs/engineering/harness/PULL_REQUEST.md",
  "templates/repository/standard/docs/engineering/harness/AUTHORITY.md",
  "templates/repository/standard/docs/engineering/harness/SKILL_PROVIDER.md",
  "repository_tools/explorer_design/sources/shell/explorer.js",
  "se_harness/engine/harness_explorer/index.template.html",
  "plugins/verity-plane/common/skills/change/SKILL.md",
  "plugins/verity-plane/common/skills/change/references/authority.md",
  "plugins/verity-plane/common/skills/evidence/SKILL.md",
  "tests/test_progressive_instruction_discovery.py",
  "tests/test_instruction_discovery.py",
  "tests/test_workflow_documentation_contract.py",
  "tests/test_instruction_architecture.py",
  "tests/test_dashboard_webui.py",
  "tests/plugin_integration/progressive_discovery/",
  "tests/plugin_integration/change_skill/",
  "tests/plugin_integration/evidence-skill/",
  "docs/engineering/instruction-architecture/acceptance/instruction-cleanup/",
  "docs/engineering/instruction-architecture/proposals/instruction-cleanup/",
  "docs/notes/instruction-reassessment-2026-09-28/",
  "docs/engineering/instruction-architecture/requirements/REQ-IAR-028.md",
  "docs/engineering/instruction-architecture/specifications/SPEC-IAR-015.md",
  "docs/engineering/instruction-architecture/verification/VER-IAR-015.md",
  "docs/engineering/instruction-architecture/verification/VER-IAR-016.md",
  "docs/engineering/instruction-architecture/verification/VER-IAR-017.md",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-020.md",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-022.md",
  "docs/engineering/instruction-architecture/decisions/DEC-IAR-002.md",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-021.md",
  "docs/engineering/instruction-architecture/evidence/WO-IAR-021/",
]

[relations]
implements = ["REQ-IAR-022", "REQ-IAR-023", "REQ-IAR-027"]
specifications = ["SPEC-IAR-014"]
verification = ["VER-IAR-015"]
architecture = ["ARCH-IAR-011", "ADR-IAR-011"]
+++

# Correct instruction references and context guidance

## Objective

Resolve F2-F6 and the compatible parts of F7/F8. Agents should find the current
action and its prerequisites from source instructions and generated surfaces.

## In scope

1. Correct the generated work-order approval anchor and assurance identity prompt.
2. Correct the README seed and both Explorer source/generated descriptions so
   they name the current instruction owner. Correct the PR guide's obsolete
   release-specific wording and unresolved Shared policy reference.
3. Align EXECUTE_WORK with conditional reading: reuse current required material
   still in context; reread changed or lost material; preserve all formal-input
   obligations and fresh evaluator checks after compaction.
4. Make the external-action provider prerequisite explicit in the procedure and
   affected skills, with one canonical rule location and exact conditional links.
   Preserve the existing independent-enforcement requirement and decision rights.
5. Permit one combined outcome/scope clarification when both are clear and both
   confirmations are retained. Shorten excess link/table formatting only in
   touched files. Keep action-point authority reminders and the CONTINUE index.
6. Extend focused regression coverage to generated templates, code-formatted
   anchors, Explorer, full delivery envelopes and six task reading paths. Retain
   measured before/after context cost; do not add a new scoring gate.
7. Integrate the reassessment and this reviewed draft package as supporting
   documentation. Their inclusion is not retroactive approval of source changes.

## Planned order

Fix active anchors first, then reading/provider wording, then focused regression
checks and the six reading demonstrations. WO-IAR-020 inventory may proceed
independently. Finish this correction before WO-IAR-022 removes shipped pointers.

## Out of scope

No hand-edit of the installed managed docs/engineering/harness collection or its
lock. Product changes occur in templates and plugin source; this repository
adopts them later through a selected released installer. No root invariant,
machine lifecycle/gate, result schema, approval identity evaluator, provider
control or accepted definition changes. No CONTINUE index removal, new retrieval
engine, generic duplicate-removal pass, host update, release or pointer deletion.

## Authorized decision envelope

After approval, the agent may choose precise equivalent wording and focused
test fixtures inside the declared paths. Rebuild Explorer output through its
existing process. Preserve exact commands and protected content. If resolving
the provider attribution changes which control applies, return that semantic
choice for review instead of silently weakening it.

## Expected change surface and stop conditions

The declared paths are the inspected source templates, affected plugin routes,
Explorer source/output, focused tests and this proposal/report. A missing test
module may be created only at its declared path. Stop for an additional source
component, changed authority meaning or an accepted-contract amendment. Existing
accepted artifacts and their lifecycle history remain unchanged. Other draft
records in the declared scope may change only to apply an actual matching human
decision or a reviewed correction to this proposal.

## Required verification and evidence

Apply VER-IAR-015. Retain requirement-by-requirement observations, reference
dispositions, full-envelope results, six read traces, complete diff and required
checks under evidence/WO-IAR-021/. Tests of edited source do not prove the current
installed plugin or root has adopted it.

## Assurance and completion

Commit-bound assurance is proposed as `required`: later discovery, adoption
and assurance decisions rely on the changed trusted content or retained host
evidence. Verification must bind the exact candidate commit.

The accountable human has not yet confirmed this classification. The optional
draft `[assurance]` table is therefore absent. Before approval, record the
confirmed classification, rationale and actual deciding human in that table.
Do not insert a placeholder identity. This draft grants no implementation,
approval, verification acceptance or release authority.

After approval, use the repository-selected released evaluator for the exact
WO's start, scope and handoff checks. Retain actual findings and the complete
declared change set. Prepare a VREC through the supported command for the exact
clean candidate commit; only a human may accept it.

The completion report gives the WO ID, candidate commit, changed files, contract
criteria and observed evidence, unresolved limitations, retained evidence paths,
actual evaluator result and its next typed step. A passing preview is not an
applied transition. No accepted definition or history is rewritten by this WO.
