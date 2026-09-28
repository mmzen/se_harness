+++
id = "WO-PLG-027"
type = "work_order"
title = "Correct current engineering and installation guidance"
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
  "docs/notes/getting-started.md",
  "docs/notes/harnessctl-reference.md",
  "docs/notes/harness-operational-phasing.md",
  "docs/notes/harness-uml-model.md",
  "docs/notes/harness-overview.md",
  "docs/notes/harness-lineage-example.md",
  "docs/notes/technical-communication.md",
  "docs/notes/developing-se-harness.md",
  "docs/notes/harness-installation-and-upgrades.md",
  "docs/notes/agentic-execution-host-adapters.md",
  "docs/notes/README.md",
  "docs/engineering/plugin-integration/README.md",
  "tests/test_progressive_documentation.py",
  "tests/test_public_onboarding.py",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-027.md",
  "docs/engineering/plugin-integration/evidence/",
  "docs/engineering/plugin-integration/verification-records/",
]

[relations]
implements = ["REQ-PLG-040"]
specifications = ["SPEC-PLG-023"]
verification = ["VER-PLG-026"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-28T20:39:06Z"
decided_by = "engineering-owner"
reason = "Human repository owner mmzen: \"I approve\", responding to the nine-artifact marketplace refresh package and required commit-bound verification for WO-PLG-026, WO-PLG-027 and WO-PLG-028. The selected pairing is plugin 0.2.1 with the unchanged released evaluator 0.19.0. Reviewed SHA-256 683de2f044926e4b5ae49d16710e093bc98fb6ca06f93866da53ddd40493823b; transition input SHA-256 721fab4c640b22b68b707dcacd13ebf46bf9b4f40c6dcdb26c12a124256c2476. Legacy 0.19.0 role engineering-owner encodes the right; mmzen is the human decision-maker and Codex applies it. Only confirmed assurance fields and confirmation prose were added to the three draft WOs. WO-PLG-026 and WO-PLG-027 may start after required checks. WO-PLG-028 waits for human-verified preparation coverage and separately authorized, observed publication. No external mutation is authorized."
scope_paths = ["docs/notes/getting-started.md", "docs/notes/harnessctl-reference.md", "docs/notes/harness-operational-phasing.md", "docs/notes/harness-uml-model.md", "docs/notes/harness-overview.md", "docs/notes/harness-lineage-example.md", "docs/notes/technical-communication.md", "docs/notes/developing-se-harness.md", "docs/notes/harness-installation-and-upgrades.md", "docs/notes/agentic-execution-host-adapters.md", "docs/notes/README.md", "docs/engineering/plugin-integration/README.md", "tests/test_progressive_documentation.py", "tests/test_public_onboarding.py", "docs/engineering/plugin-integration/work-orders/WO-PLG-027.md", "docs/engineering/plugin-integration/evidence/", "docs/engineering/plugin-integration/verification-records/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-28T21:02:43Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed. Begin approved guidance scope after WO-PLG-026 package edits. Execution entry commit cc6901a215b6f23febb1d918591c0c4ddc6a3d08; shared proposal baseline c4d9036fdaab378f08fe2db68978126f66ab961e retained. No earlier WO-PLG-027 implementation is excluded."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-28T21:14:14Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded engineering-owner approval; relevant local gates passed."
+++

# Correct current engineering and installation guidance

## Objective

Correct the audited current learning and operator guidance while preserving
historical records, public status accuracy and the existing package architecture.

## In scope

1. Replace current authority routes to old compatibility files with the exact
   current file and heading needed for that task.
2. Correct whole-file AGENTS ownership, evaluator invocation examples and the
   getting-started glossary target.
3. Distinguish repository-owned providers, native hooks and selected release
   behavior; retain clearly dated historical explanations.
4. Correct navigation and current installed-version facts in the listed indexes.
5. Add focused link/command/ownership tests and retain a file-by-file assessment.

## Out of scope

Manifest or archive changes; edits to managed harness instructions, historical
formal artifacts, evaluator code, publisher workflows, demo application code,
credentials or user profiles; claims that an unobserved public update succeeded.

## Expected change surface

Only the listed operator/learning documents, the plugin domain index and the
two documentation test files may change, plus this WO's new evidence and records.
The development guide changes its current setup/release routes and temporary
workaround description; preserve the release-delivery procedure already merged.
The UML guide changes stale references only, not its underlying architecture.

## Ordering

Apply this work after the package-facing edits to the shared onboarding test
file. A combined final VREC may cover both preparation WOs at the same exact
commit. Availability remains based on the last actual public observation.

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
under `docs/engineering/plugin-integration/evidence/WO-PLG-027/`. Prepare a clean exact-commit VREC. Record unavailable checks
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
