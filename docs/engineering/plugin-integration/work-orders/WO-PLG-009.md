+++
id = "WO-PLG-009"
type = "work_order"
title = "Connect and maintain projects with plugin skills"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-09-14"
updated = "2026-09-15"

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
  "repository_tools/plugin_distribution.py",
  "tests/plugin_integration/repository_connection/",
  "tests/plugin_integration/test_simple_plugin.py",
  "tests/test_skill_ownership.py"
]

[relations]
implements = ["REQ-PLG-015", "REQ-PLG-016"]
specifications = ["SPEC-PLG-009"]
verification = ["VER-PLG-009"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-14T22:05:14Z"
decided_by = "engineering-owner"
reason = "The owner reviewed and approved completion of the KISS backlog amendment and explicitly said \"you can start WO-PLG-009 and WO-PLG-016\" on 2026-09-15. This accepts the selected rewritten definition chain and authorizes its bounded routine execution, checks and evidence under the installed evaluator. No result-specific assurance, merge, release or live host/project installation is inferred."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-14T22:06:01Z"
decided_by = "engineering-owner"
reason = "The owner explicitly authorized starting this rewritten work order on 2026-09-15. Record that selected start; use existing mechanisms and retain the KISS scope."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-15T05:22:53Z"
decided_by = "engineering-owner"
reason = "The owner reviewed the completed implementations and said \"i approve WO-PLG-009 and WO-PLG-016\" in response to the explicit completion request. Record that engineering-owner completion approval for WO-PLG-009. Its full local suite and documented walkthroughs passed; the implementation PR checks passed or were intentionally skipped. This approval does not verify a record, merge, release, publish or change a live project."
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

The authorized connection walkthrough exposed a valid Windows-built wheel rejected
by the existing development assembler because its metadata uses CRLF. The bounded
execution scope includes normalizing that metadata read in plugin_distribution.py,
with one regression check in the already selected test_simple_plugin.py. This is
a necessary compatibility repair for the existing route, not a new packaging design.

Deliver the short instructions and evidence of the three VER-PLG-009 outcomes.
Record missing live-host/release evidence honestly; WO-PLG-016 covers native use.


## Execution and acceptance

The owner authorized this selected scope on 2026-09-15. Its approval authorizes the normal execution
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
