+++
id = "WO-PLG-028"
type = "work_order"
title = "Confirm the published marketplace and reconcile availability claims"
status = "implemented"
owners = ["mmzen"]
created = "2026-09-28"
updated = "2026-09-29"

[assurance]
commit_bound_verification = "required"
rationale = "Later assurance and delivery decisions rely on the changed content and evidence; human mmzen confirmed required commit-bound verification when approving this exact package."
decided_by = "mmzen"

[execution_scope]
paths = [
  "README.md",
  "docs/notes/plugin-installation-guide.md",
  "docs/notes/plugin-marketplace-publication.md",
  "docs/notes/developing-se-harness.md",
  "docs/notes/README.md",
  "docs/engineering/plugin-integration/README.md",
  "tests/test_public_onboarding.py",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-028.md",
  "docs/engineering/plugin-integration/evidence/",
  "docs/engineering/plugin-integration/verification-records/",
]

[relations]
implements = ["REQ-PLG-041"]
specifications = ["SPEC-PLG-023"]
verification = ["VER-PLG-027"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-28T20:39:06Z"
decided_by = "engineering-owner"
reason = "Human repository owner mmzen: \"I approve\", responding to the nine-artifact marketplace refresh package and required commit-bound verification for WO-PLG-026, WO-PLG-027 and WO-PLG-028. The selected pairing is plugin 0.2.1 with the unchanged released evaluator 0.19.0. Reviewed SHA-256 9c49fe5136fb75f31f22ae2d0d84e8ee59c9aa27b87f09df0d0bb21435eebc51; transition input SHA-256 ab58b8d47ef95138f527de4f83e07041ce85eb37a3adeafce37f233cdf4e9e32. Legacy 0.19.0 role engineering-owner encodes the right; mmzen is the human decision-maker and Codex applies it. Only confirmed assurance fields and confirmation prose were added to the three draft WOs. WO-PLG-026 and WO-PLG-027 may start after required checks. WO-PLG-028 waits for human-verified preparation coverage and separately authorized, observed publication. No external mutation is authorized."
scope_paths = ["README.md", "docs/notes/plugin-installation-guide.md", "docs/notes/plugin-marketplace-publication.md", "docs/notes/developing-se-harness.md", "docs/notes/README.md", "docs/engineering/plugin-integration/README.md", "tests/test_public_onboarding.py", "docs/engineering/plugin-integration/work-orders/WO-PLG-028.md", "docs/engineering/plugin-integration/evidence/", "docs/engineering/plugin-integration/verification-records/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-29T06:05:18Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-29T16:27:51Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded engineering-owner approval; relevant local gates passed."
+++

# Confirm the published marketplace and reconcile availability claims

## Objective

Confirm the separately published 0.2.1 marketplace from its public ref and bring
current availability claims into agreement with actual fresh/update observations.

## Entry conditions

Do not start until WO-PLG-026 and WO-PLG-027
have human-verified coverage and the exact public marketplace operation has
separate authorization and an observed result. Approval of this draft alone
does not satisfy those conditions or authorize publication.

## In scope

1. Inspect public commit ancestry and byte identity against the accepted package.
2. Run the four actual public fresh/update routes and native delivery observations
   in disposable Windows profiles on both hosts.
3. Update the listed current source documents' availability/status paragraphs and
   evidence links after the matching observations pass.
4. Recheck public-onboarding assertions and retain final delivery plan versions,
   observations and completion results using the existing format/checker.
5. Prepare commit-bound verification for this changed guidance/evidence. After
   its separately authorized integration, retain public documentation readback
   as a new delivery receipt; preserve all VREC-bound evidence unchanged.

## Out of scope

The actual publication mutation; package reassembly or generated-tree edits;
new features, broad prose rewrites, changes to previously accepted evidence,
evaluator/version markers, provider submissions and real user profile adoption.

## Expected change surface

Only the listed source status documents and public-onboarding test may change,
plus new evidence and records for this work. Do not modify immutable archives
or their package-facing documents to point them at a later source commit.
The evidence directory scope includes append-only post-integration receipts.

## Completion boundary

Implementation and a VREC may complete with a reviewed source status update and
its public-package observations. Report documentation integration as pending
until separately authorized and observed. Overall delivery remains incomplete
until that last readback satisfies VER-PLG-027 PUB-03/PUB-04.

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

Apply VER-PLG-027 for
this WO's selected requirement. Run required graph, scope, handoff and transition
checks. Retain a requirement-to-evidence assessment and actual commands/results
under `docs/engineering/plugin-integration/evidence/WO-PLG-028/`. Prepare a clean exact-commit VREC. Record unavailable checks
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
