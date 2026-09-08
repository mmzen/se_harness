+++
id = "WO-PLG-009"
type = "work_order"
title = "Connect repositories without conflicting skill ownership"
status = "draft"
owners = ["engineering-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[assurance]
commit_bound_verification = "required"
rationale = "Proposed classification: future governed work relies on the correctness of this plugin behavior and its instructions."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "plugins/verity-plane/common/skills/setup/SKILL.md",
  "plugins/verity-plane/common/skills/setup/references/repository.md",
  "tests/plugin_integration/repository_connection/",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-009.md",
  "docs/engineering/plugin-integration/evidence/WO-PLG-009/",
]

[relations]
implements = ["REQ-PLG-015", "REQ-PLG-016"]
specifications = ["SPEC-PLG-009"]
verification = ["VER-PLG-009"]
+++

# Work Order: Connect repositories without conflicting skill ownership

## Lifecycle

Draft proposal only; no execution or delegation is authorized. Approval of this WO and its governing chain precedes work; later lifecycle decisions follow the installed rules.

## Objective

Add precise setup procedures for reviewed installer operations and compatible repository/plugin skill discovery.

## In scope

The setup entry's repository mode, its repository reference, and disposable-target connection/discovery tests.

## Out of scope

Core installer changes, manual locked-file edits/deletions, runtime setup changes, new migration flags and unrequested repository upgrades.

## Authorized decision envelope

After approval and DEC-PLG-004 resolution, choose procedure wording and fixtures within the supported compatibility decision. Existing installer and SPEC-AEX-005 contracts remain authoritative.

## Constraints

Use the inspected selected released CLI; never assume a unified-init alias. Reuse still-covered requests and decisions. A plugin update cannot independently change the repository lock.

## Expected change surface

Only the exact setup files listed above, tests, this WO and its evidence.

## Required verification

Satisfy VER-PLG-009 and applicable checks after runtime setup and relevant host activation. Test customized managed files and actual duplicate-skill selection.

## Evidence to record

Retain reviewed/applied operation, target diffs, lock/digest results, host discovery observations and failures with exact runtime identities.

## Stop and escalate conditions

DEC-PLG-004 blocks SPEC-PLG-009 approval, leaving this WO ineligible. If the chosen route needs unavailable installer behavior, record the blocker and request separate core work.

## Completion report format

Report connection results, discovered active skills, preserved files, test evidence, blockers, final state and one next step.
