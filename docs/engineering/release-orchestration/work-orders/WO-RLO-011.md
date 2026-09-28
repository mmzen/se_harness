+++
id = "WO-RLO-011"
type = "work_order"
title = "Add release delivery completion procedure and checks"
status = "draft"
owners = ["mmzen"]
created = "2026-09-28"
updated = "2026-09-28"

[execution_scope]
paths = [
  "scripts/check_release_delivery.py",
  "tests/test_release_delivery.py",
  "tests/fixtures/release_delivery/",
  "docs/notes/release-delivery-completion.md",
  "docs/notes/developing-se-harness.md",
  "docs/notes/plugin-marketplace-publication.md",
  "docs/engineering/release-orchestration/capabilities/CAP-RLO-004.md",
  "docs/engineering/release-orchestration/requirements/REQ-RLO-018.md",
  "docs/engineering/release-orchestration/requirements/REQ-RLO-019.md",
  "docs/engineering/release-orchestration/requirements/REQ-RLO-020.md",
  "docs/engineering/release-orchestration/specifications/SPEC-RLO-006.md",
  "docs/engineering/release-orchestration/verification/VER-RLO-008.md",
  "docs/engineering/release-orchestration/work-orders/WO-RLO-011.md",
  "docs/engineering/release-orchestration/evidence/",
  "docs/engineering/release-orchestration/verification-records/",
]

[relations]
implements = ["REQ-RLO-018", "REQ-RLO-019", "REQ-RLO-020"]
specifications = ["SPEC-RLO-006"]
verification = ["VER-RLO-008"]
+++

# Work Order: Add release delivery completion procedure and checks

## Lifecycle

The user approved the release-procedure correction plan on 2026-09-28. This
packet turns that plan into exact proposed definitions and implementation scope.
All records remain draft until the reviewed package and required commit-bound
assurance receive the applicable human decision. The assurance table will be
recorded from that confirmation before approval is previewed.

## Proposed assurance

Commit-bound verification: **required**. Later release closeout depends on the
correctness of this reporting code and required procedure. Human confirmation
of the classification is pending; no assurance decision-maker is recorded yet.

## Objective

Make overall delivery status expose a missing marketplace update or stale
current guidance after evaluator publication, before the repository claims
delivery is complete.

## In scope

1. Implement one read-only local delivery reporting script to SPEC-RLO-006.
2. Add its focused regression cases and synthetic fixtures.
3. Write the release delivery guide with concrete inputs, outputs and commands.
4. Correct the completion criterion in the existing release sequence and add
   the bounded handoff link in the marketplace publication guide.
5. Retain checks and review evidence, record implementation completion and
   prepare an exact-commit verification record under VER-RLO-008.

## Out of scope

- Updating the current marketplace package, selecting its next version or
  correcting the broader documentation inventory from the 2026-09-28 audit.
- Changes to publisher workflows, credentials, native host profiles, portable
  evaluator code, managed instructions or required lifecycle gates.
- Publication, tag changes, branch pushes, PR creation, merge or deployment.
- Rewriting accepted definitions, earlier work orders, VRECs, RLSs or evidence.

## Authorized decision envelope

Once approved and started through the released evaluator, the implementing
agent may choose internal code layout, documented JSON field names, fixture
organization and local commits within this contract. It may perform the
required checks, retain evidence and prepare verification without another
execution approval. Human assurance acceptance remains separate.

The evidence and verification-record directory entries permit only new records
and evidence for this work, including evaluator-generated companion files.
They do not permit changes to existing records or evidence. Formal definitions
remain subject to the accepted-definition amendment rules after approval.

No active architecture directly addresses the new selected requirements.
This work preserves the existing trust boundary and introduces no new service,
credential boundary or portable interface; no architecture link is invented.

## Constraints

- Use the selected released 0.19.0 evaluator for governance. Candidate 0.20.0
  source is not the governing evaluator.
- Preserve PR #494's work and its accepted evidence. This proposal starts on a
  separate local branch from 3d483ef8f8d1eeb8dea2a6a2fd8958e0f2b50ac1.
- Keep the existing publisher output contract intact. Report supplied-evidence
  limits clearly; a local summary is not proof of unobserved public behavior.
- Update only the release-sequence completion/handoff text in the existing
  development guide and the handoff section in the marketplace publication
  guide. Leave unrelated historical and version-specific prose for later work.

## Expected change surface

| File or component | Change |
| --- | --- |
| `scripts/check_release_delivery.py` | Standard-library local reader, validation, identity comparison and completion report. |
| `tests/test_release_delivery.py`, `tests/fixtures/release_delivery/` | Independent normal, incomplete, stale-identity and invalid-input cases. |
| `docs/notes/release-delivery-completion.md` | Procedure, data format, complete example, evidence requirements and limits. |
| `docs/notes/developing-se-harness.md` | Correct release completion definition and route to the new procedure. |
| `docs/notes/plugin-marketplace-publication.md` | Link evaluator-to-plugin handoff and public-route closeout. |
| The seven selected formal drafts and new work evidence | Reviewed definitions, authorized lifecycle records and verification preparation. |

## Required verification

Apply VER-RLO-008 cases DLV-01 through DLV-07. Run the focused new suite and
the existing `test_release_orchestration.py` and `test_dashboard_publication.py`
regression suites. Run required graph, scope, handoff and transition checks.
Record actual commands, results and untested platform limits.

## Evidence to record

Use `docs/engineering/release-orchestration/evidence/WO-RLO-011/` for test
outputs, the documented example, review, requirement assessment and retained
evaluator results. Retain any evaluator-generated verification companions in
their supported locations. The final VREC must bind the exact clean commit.

## Stop and escalate conditions

- An accepted definition must change or another path is needed.
- The reporting design would require privileged execution, network access,
  publication or changes to the portable lifecycle.
- Missing authority, evidence or failed gates prevent the affected action.
- Actual scope or reviewed inputs differ from this approved proposal.

## Completion report format

Report implemented behavior, actual checks, exact candidate, retained evidence,
limitations and the evaluator's next accountable decision. State explicitly
that marketplace delivery itself remains subsequent work.
