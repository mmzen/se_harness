+++
id = "WO-PLG-026"
type = "work_order"
title = "Prepare and qualify the 0.2.1 marketplace candidate"
status = "implemented"
owners = ["mmzen"]
created = "2026-09-28"
updated = "2026-09-28"

[assurance]
commit_bound_verification = "required"
rationale = "Later assurance and delivery decisions rely on the changed content and evidence; human mmzen confirmed required commit-bound verification when approving this exact package."
decided_by = "mmzen"

[execution_scope]
paths = [
  "README.md",
  "plugins/verity-plane/codex/.codex-plugin/plugin.json",
  "plugins/verity-plane/claude-code/.claude-plugin/plugin.json",
  "plugins/verity-plane/codex/README.md",
  "plugins/verity-plane/claude-code/README.md",
  "release/plugin-marketplace/README.md",
  "release/plugin-marketplace/submissions/README.md",
  "release/plugin-marketplace/submissions/reviewer-test-cases.md",
  "docs/notes/plugin-installation-guide.md",
  "docs/notes/plugin-marketplace-publication.md",
  "tests/test_public_onboarding.py",
  "tests/plugin_integration/package_assembly/",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-039.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-040.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-041.md",
  "docs/engineering/plugin-integration/specifications/SPEC-PLG-023.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-026.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-027.md",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-027.md",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-028.md",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-026.md",
  "docs/engineering/plugin-integration/evidence/",
  "docs/engineering/plugin-integration/verification-records/",
]

[relations]
implements = ["REQ-PLG-039"]
specifications = ["SPEC-PLG-023"]
verification = ["VER-PLG-026"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-28T20:39:06Z"
decided_by = "engineering-owner"
reason = "Human repository owner mmzen: \"I approve\", responding to the nine-artifact marketplace refresh package and required commit-bound verification for WO-PLG-026, WO-PLG-027 and WO-PLG-028. The selected pairing is plugin 0.2.1 with the unchanged released evaluator 0.19.0. Reviewed SHA-256 f3b3d9239fa983c30f514a430a6545e885fbaee6bb4b9d7213e866e841035c97; transition input SHA-256 ce72209bd9814627f7744b5e516d72e315f8ec752b58df6c916b392a5ddac5d0. Legacy 0.19.0 role engineering-owner encodes the right; mmzen is the human decision-maker and Codex applies it. Only confirmed assurance fields and confirmation prose were added to the three draft WOs. WO-PLG-026 and WO-PLG-027 may start after required checks. WO-PLG-028 waits for human-verified preparation coverage and separately authorized, observed publication. No external mutation is authorized."
scope_paths = ["README.md", "plugins/verity-plane/codex/.codex-plugin/plugin.json", "plugins/verity-plane/claude-code/.claude-plugin/plugin.json", "plugins/verity-plane/codex/README.md", "plugins/verity-plane/claude-code/README.md", "release/plugin-marketplace/README.md", "release/plugin-marketplace/submissions/README.md", "release/plugin-marketplace/submissions/reviewer-test-cases.md", "docs/notes/plugin-installation-guide.md", "docs/notes/plugin-marketplace-publication.md", "tests/test_public_onboarding.py", "tests/plugin_integration/package_assembly/", "docs/engineering/plugin-integration/requirements/REQ-PLG-039.md", "docs/engineering/plugin-integration/requirements/REQ-PLG-040.md", "docs/engineering/plugin-integration/requirements/REQ-PLG-041.md", "docs/engineering/plugin-integration/specifications/SPEC-PLG-023.md", "docs/engineering/plugin-integration/verification/VER-PLG-026.md", "docs/engineering/plugin-integration/verification/VER-PLG-027.md", "docs/engineering/plugin-integration/work-orders/WO-PLG-027.md", "docs/engineering/plugin-integration/work-orders/WO-PLG-028.md", "docs/engineering/plugin-integration/work-orders/WO-PLG-026.md", "docs/engineering/plugin-integration/evidence/", "docs/engineering/plugin-integration/verification-records/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-28T20:43:02Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed. Codex starts the unchanged scope approved by mmzen; plugin 0.2.1 and released evaluator 0.19.0, baseline c4d9036fdaab378f08fe2db68978126f66ab961e."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-28T21:01:12Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded engineering-owner approval; relevant local gates passed. Completed approved package scope with 89 passing focused tests, independent composition checks, both Windows native routes and instruction boundary evidence; public delivery remains pending."
+++

# Prepare and qualify the 0.2.1 marketplace candidate

## Objective

Prepare and locally qualify the exact plugin 0.2.1/SE Harness 0.19.0 marketplace
candidate, including accurate package-facing instructions and consistency tests.

## In scope

1. Update the two native manifest versions and the listed package-facing guides.
2. Correct current submission draft behavior descriptions without submitting them.
3. Extend existing offline identity/onboarding and package-context link tests.
4. Assemble from one exact commit; run existing build/check and native local
   fresh/update/replacement routes under SPEC-PLG-023 MREF-006.
5. Prepare the delivery plan with marketplace, documentation and demonstration
   pending; retain unchanged evaluator/marker identities for later review.
6. Retain qualification and prepare commit-bound verification.

## Out of scope

Public publication and its later readback; wider learning-guide cleanup; changes
to builder code, assembly mapping, catalogs, skill behavior, hooks, workflow, CI,
managed instructions, evaluator selection, release markers or real user profiles.
Do not claim that merged candidate instructions are already publicly delivered.

## Expected change surface

The two manifest files change only the selected plugin version. The root README,
host READMEs, marketplace README, submission drafts and two plugin guides receive
the facts and routes defined by MREF-003 to MREF-006. Existing test files and the
package-assembly test directory receive bounded identity/link/status checks.
Generated distributions remain outside the source checkout.

The exact nine new package artifacts are included for retention of the reviewed
proposal and its authorized lifecycle events. Their presence does not authorize
execution of WO-PLG-028 or changes to accepted definition meaning. A later
definition change must follow the separate amendment procedure.

## Ordering

Coordinate the shared onboarding test file with the documentation WO through
sequential edits. Complete both preparation WOs before final combined candidate
capture. This WO does not wait for actual public publication to be verified.

## Confirmed assurance

Commit-bound verification: **required**. Later assurance and delivery decisions
rely on the correctness of the changed content and retained evidence. This is the
classification confirmed by human mmzen with "I approve" in response to the
nine-artifact review and explicit required-verification request on 2026-09-28.

## Authorized decision envelope

After approval and start, Codex may perform this bounded work, choose internal
test organization and prose, make local commits, retain evidence and prepare the
required VREC. The human repository owner mmzen decides approval, verification
and external actions. No push, PR, merge, publication, tag change or real profile
adoption is granted by this draft. Disposable qualification may require the
human to complete login or trust steps; credentials are not copied into evidence.

## Constraints

- Govern with the repository-selected released evaluator 0.19.0, outside the
  checkout. Candidate source 0.20.0 is not authority or the wheel to bundle.
- Preserve all accepted definitions and historical records. Evidence-directory
  scope admits only new files for this WO, its selected VREC and evaluator
  companions. It does not permit rewriting another work order's evidence.
- The source baseline is `c4d9036fdaab378f08fe2db68978126f66ab961e`. Reuse the existing builders, hooks,
  evaluator and delivery checker without changing their behavior.
- No active architecture directly addresses the newly selected requirements;
  the existing trust and deployment boundaries are preserved. No architecture
  or ADR link is fabricated. A needed boundary change requires new reviewed scope.

## Required verification and evidence

Apply VER-PLG-026 for
this WO's selected requirement. Run required graph, scope, handoff and transition
checks. Retain a requirement-to-evidence assessment and actual commands/results
under `docs/engineering/plugin-integration/evidence/WO-PLG-026/`. Prepare a clean exact-commit VREC. Record unavailable checks
and failed attempts explicitly; do not relax pass criteria to finish the work.

## Stop and escalate conditions

Stop affected work if a selected definition must change, an unlisted path is
needed, a required check fails, a public ref or reviewed package differs, or
required native access is missing. Compare changed inputs before reusing authority.
Do not repair scope by editing accepted definitions or completed work orders.

## Completion report format

Report actual changed behavior, selected source/package/candidate identities,
observed checks, retained evidence, limitations and the evaluator's next decision.
Keep local qualification, human verification, public delivery and overall
completion separate. No lifecycle state is inferred from a Git action.
