+++
id = "WO-PLG-016"
type = "work_order"
title = "Document installation and check ordinary host use"
status = "in_progress"
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
  "docs/engineering/plugin-integration/evidence/WO-PLG-016/",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-027.md",
  "docs/engineering/plugin-integration/specifications/SPEC-PLG-016.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-016.md",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-016.md",
  "docs/notes/plugin-installation-guide.md",
  "tests/plugin_integration/onboarding/"
]

[relations]
implements = ["REQ-PLG-027"]
specifications = ["SPEC-PLG-016"]
verification = ["VER-PLG-016"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-14T22:16:55Z"
decided_by = "engineering-owner"
reason = "The owner reviewed and approved completion of the KISS backlog amendment and explicitly said \"you can start WO-PLG-009 and WO-PLG-016\" on 2026-09-15. This accepts the selected rewritten definition chain and authorizes its bounded routine execution, checks and evidence under the installed evaluator. No result-specific assurance, merge, release or live host/project installation is inferred."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-14T22:20:07Z"
decided_by = "engineering-owner"
reason = "The owner explicitly authorized starting this rewritten work order on 2026-09-15. Record that selected start; use existing mechanisms and retain the KISS scope."
+++

# Document installation and check ordinary host use

## Result

Deliver one short installation guide and evidence that its claimed route works.
Follow SPEC-PLG-016 and VER-PLG-016. Start after WO-PLG-009 has settled the connection
instructions. Reuse current package/discovery/setup checks rather than rebuilding them.

## Scope

This rewrites the reserved WO-PLG-016 and absorbs WO-PLG-015's useful walkthrough
evidence. Write and test the development guide now. Before making a public-install
claim, select an available release and check that actual route. A public release
is not a prerequisite for drafting useful instructions.

There is no separate performance qualification project, workflow, signing scheme,
supported-version census or optional-helper dependency. If an actual defect needs
runtime changes outside this documentation/test scope, record the concrete defect
and amend the scope; do not expand this into a new installation framework.

## Completion

Present the guide, actual walkthrough results and limits of the support claims.
Public release, installation in the owner's host and live project adoption are
separate actions. A development-only result must remain labeled as such.


## Execution and acceptance

Approval of this selected scope authorizes the normal execution
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
