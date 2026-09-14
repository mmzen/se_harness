+++
id = "WO-PLG-009"
type = "work_order"
title = "Connect and maintain projects with plugin skills"
status = "draft"
owners = ["engineering-owner"]
created = "2026-09-14"
updated = "2026-09-14"

[assurance]
commit_bound_verification = "required"
rationale = "Later project use will rely on the changed plugin instructions and demonstrated behavior."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "docs/engineering/plugin-integration/README.md",
  "docs/engineering/plugin-integration/evidence/WO-PLG-009/",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-015.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-016.md",
  "docs/engineering/plugin-integration/specifications/SPEC-PLG-009.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-009.md",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-009.md",
  "plugins/verity-plane/common/scripts/setup.py",
  "plugins/verity-plane/common/skills/setup/SKILL.md",
  "plugins/verity-plane/common/skills/setup/references/maintenance.md",
  "plugins/verity-plane/common/skills/setup/references/repository.md",
  "tests/plugin_integration/repository_connection/",
  "tests/plugin_integration/test_simple_plugin.py",
  "tests/test_skill_ownership.py"
]

[relations]
implements = ["REQ-PLG-015", "REQ-PLG-016"]
specifications = ["SPEC-PLG-009"]
verification = ["VER-PLG-009"]
+++

# Connect and maintain projects with plugin skills

## Result

One setup route explains how to connect a project, repair its checker and request
a version upgrade. Implement SPEC-PLG-009 and meet VER-PLG-009. Start with the
instructions: the existing installer and repair operation already do most work.
Any additional code must address a demonstrated missing outcome.

## Scope and dependencies

This rewrites the reserved WO-PLG-009 from PR #416 and absorbs WO-PLG-013.
WO-PLG-020/021 and WO-KIS-001 through 009 are merged inputs, not work to rebuild.
Develop against those capabilities in labeled disposable fixtures. A real migration
must use a released compatible checker and the owner's selected target/action.
Do not wait for a public plugin release merely to improve development instructions.
No DEC-PLG-004 compatibility decision, new ownership engine, second environment,
activation hook, CI job or publication pipeline belongs in this scope.

## Completion

Deliver the short instructions and evidence of the three VER-PLG-009 outcomes.
Record missing live-host/release evidence honestly; WO-PLG-016 covers native use.


## Execution and acceptance

This packet is draft. Approval of its selected scope authorizes the normal execution
procedure: start, implement, check, record completion and prepare required verification.
Use the installed evaluator and its actual returned commands; do not add a delegation
class, separate routine permission, forced subagent or live-CI condition for local work.
SPEC-KIS-003 describes the accepted single route. An older installed governor may require
an explicit remaining-work approval through its existing amendment route until adoption;
candidate code cannot grant itself authority. Accountable verification, release, merge
and changes to live host/project settings retain their existing authorization requirements.

Reuse the repository's normal test and package jobs. Keep one concise summary identifying
the candidate, actual checker/host versions, outcomes and any unavailable evidence.
Use existing relevant tests and evidence before adding a missing outcome check.
Change only the named scope. A real failed check or required scope change stops the
affected action; unrelated edits and optional measurements do not become new gates.
