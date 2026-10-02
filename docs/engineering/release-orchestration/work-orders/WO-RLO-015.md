+++
id = "WO-RLO-015"
type = "work_order"
title = "Automate complete delivery and safe recovery"
status = "in_progress"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"

[assurance]
commit_bound_verification = "required"
rationale = "Required verification confirmed by mmzen: release and publication decisions depend on this changed authority, preparation, workflow or activation evidence; assess the exact implemented commit."
decided_by = "mmzen"

[execution_scope]
paths = [
  ".github/workflows/publish-pypi.yml",
  ".github/workflows/release-qualification.yml",
  ".github/workflows/pages-publication.yml",
  ".github/workflows/release-candidate-replay.yml",
  ".github/workflows/publication-rehearsal.yml",
  ".github/scripts/publish_release.py",
  ".github/scripts/publish_dashboard.py",
  ".github/scripts/reconcile_maintenance_branch.py",
  "repository_tools/release_distribution.py",
  "repository_tools/plugin_distribution.py",
  "scripts/check_release_delivery.py",
  "scripts/build_plugin_marketplace.py",
  "tests/test_release_orchestration.py",
  "tests/test_release_delivery.py",
  "tests/test_release_qualification.py",
  "tests/test_ci_pipeline.py",
  "tests/plugin_integration/package_assembly/",
  "tests/fixtures/release_delivery/",
  "docs/notes/developing-se-harness.md",
  "docs/notes/plugin-marketplace-publication.md",
  "docs/notes/release-delivery-completion.md",
  "docs/notes/release-publication-rehearsal.md",
  "README.md",
  "docs/engineering/release-orchestration/intent/INT-RLO-002.md",
  "docs/engineering/release-orchestration/capabilities/CAP-RLO-005.md",
  "docs/engineering/release-orchestration/requirements/REQ-RLO-021.md",
  "docs/engineering/release-orchestration/requirements/REQ-RLO-022.md",
  "docs/engineering/release-orchestration/requirements/REQ-RLO-023.md",
  "docs/engineering/release-orchestration/specifications/SPEC-RLO-007.md",
  "docs/engineering/release-orchestration/architecture/ARCH-RLO-006.md",
  "docs/engineering/release-orchestration/architecture/adr/ADR-RLO-006.md",
  "docs/engineering/release-orchestration/verification/VER-RLO-011.md",
  "docs/engineering/release-orchestration/work-orders/WO-RLO-014.md",
  "docs/engineering/release-orchestration/work-orders/WO-RLO-015.md",
  "docs/engineering/release-orchestration/work-orders/WO-RLO-016.md",
  "docs/engineering/release-orchestration/evidence/WO-RLO-015/",
  "docs/engineering/release-orchestration/verification-records/",
  "docs/engineering/release-orchestration/risks/RISK-RLO-001.md",
]

[relations]
implements = ["REQ-RLO-021", "REQ-RLO-022", "REQ-RLO-023"]
specifications = ["SPEC-RLO-007"]
verification = ["VER-RLO-011"]
architecture = ["ARCH-RLO-006", "ADR-RLO-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T20:17:28Z"
decided_by = "mmzen"
reason = "Human repository owner mmzen answered \"Approve package, verification and review PR\" to the exact package review for WO-RLO-014/015/016 and their governing definitions, with required commit-bound verification under VER-RLO-011. This authorizes bounded implementation, local checks and commits, completion and verification preparation, ordinary review-branch push and draft PR from work/complete-release-approval to mmzen/se_harness:main, and its later verification-decision update. Human verification acceptance, merge, actual releases and the exact live configuration change remain separate. The selected released evaluator 0.21.0 governs this work. Reviewed draft SHA-256 f4a079479f2191d6c238fd4af5e3ed3b13d73f365dc5b95140d4cfe52f2e8b4c; approved transition input SHA-256 f8e4d0c322d45eca4626b8380a5037397445427a2ed91197286d26ee2532596e. Only the confirmed WO assurance fields were added before this transition."
scope_paths = [".github/workflows/publish-pypi.yml", ".github/workflows/release-qualification.yml", ".github/workflows/pages-publication.yml", ".github/workflows/release-candidate-replay.yml", ".github/workflows/publication-rehearsal.yml", ".github/scripts/publish_release.py", ".github/scripts/publish_dashboard.py", ".github/scripts/reconcile_maintenance_branch.py", "repository_tools/release_distribution.py", "repository_tools/plugin_distribution.py", "scripts/check_release_delivery.py", "scripts/build_plugin_marketplace.py", "tests/test_release_orchestration.py", "tests/test_release_delivery.py", "tests/test_release_qualification.py", "tests/test_ci_pipeline.py", "tests/plugin_integration/package_assembly/", "tests/fixtures/release_delivery/", "docs/notes/developing-se-harness.md", "docs/notes/plugin-marketplace-publication.md", "docs/notes/release-delivery-completion.md", "docs/notes/release-publication-rehearsal.md", "README.md", "docs/engineering/release-orchestration/intent/INT-RLO-002.md", "docs/engineering/release-orchestration/capabilities/CAP-RLO-005.md", "docs/engineering/release-orchestration/requirements/REQ-RLO-021.md", "docs/engineering/release-orchestration/requirements/REQ-RLO-022.md", "docs/engineering/release-orchestration/requirements/REQ-RLO-023.md", "docs/engineering/release-orchestration/specifications/SPEC-RLO-007.md", "docs/engineering/release-orchestration/architecture/ARCH-RLO-006.md", "docs/engineering/release-orchestration/architecture/adr/ADR-RLO-006.md", "docs/engineering/release-orchestration/verification/VER-RLO-011.md", "docs/engineering/release-orchestration/work-orders/WO-RLO-014.md", "docs/engineering/release-orchestration/work-orders/WO-RLO-015.md", "docs/engineering/release-orchestration/work-orders/WO-RLO-016.md", "docs/engineering/release-orchestration/evidence/WO-RLO-015/", "docs/engineering/release-orchestration/verification-records/", "docs/engineering/release-orchestration/risks/RISK-RLO-001.md"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-02T20:28:34Z"
decided_by = "Codex agent"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed. Start under mmzen approved package; WO-RLO-014 staging interfaces implemented and 19 package tests pass."
+++

# Automate complete delivery and safe recovery

## Objective

The existing release workflow carries the complete approved delivery through public checks and latest/last promotion, with resumable partial failure.

## In scope

Implement RLO-ONE-004, RLO-ONE-005 and the repository parts of RLO-ONE-001/007. Extend existing plan/receipt handling, marketplace promotion and credential-free rehearsal. Include bounded release-only integration and marker reconciliation. Update current release instructions and examples; preserve historical evidence and older contract behavior.

## Constraints and dependencies

Depends on WO-RLO-014's implemented interfaces. Complete integration checks before verification. This work does not remove the live pypi reviewer; WO-RLO-016 prepares that exact activation review.

Use SPEC-RLO-007 and ARCH-RLO-006/ADR-RLO-006. Preserve historical formal records,
published bytes and unrelated repository content. Every listed path is a ceiling,
not a request to modify files without need. Approved definition files are included
only for transport of this reviewed package and evaluator-applied transitions;
their accepted meaning must not be rewritten.

## Out of scope

No production release, package publication, marketplace or marker mutation,
live provider-setting change, credential refresh, repository adoption or force
push. No new formal artifact type or general orchestration service. No rewriting
accepted older definitions or treating draft instructions as current authority.

## Authorized decision envelope

When this exact work order is approved, the agent may implement the listed scope,
perform checks, make local commits, record completion and prepare commit-bound
verification under the selected released evaluator. This draft proposes required
assurance; its human classification is not yet recorded. Human verification and
any external action require actual matching authority.

The proposed review-delivery grant covers ordinary branch updates and a draft PR
from work/complete-release-approval to main in mmzen/se_harness, then the final
verification-decision update. It excludes merge and publication. This grant is
part of the package to review; no push is authorized merely by this draft.

## Proposed assurance classification

Required commit-bound verification. Later release and publication decisions rely
on this changed authority, preparation, workflow or activation evidence. The human
must confirm this classification with the package approval; only then will the
`[assurance]` fields name that human. No decision-maker is fabricated in this draft.

## Required verification

Run VER-RLO-011 ONE05, ONE06 and integrated ONE07/ONE08 on Windows and Linux. Exercise absent/exact/partial/conflicting/unknown external state, all five surfaces, credential isolation and incomplete readbacks. Run applicable full-suite and CI checks. Rehearsals use fixtures and disposable repositories, not production publication.

## Evidence to record

Store the review, commands, outputs, identities and results in
`docs/engineering/release-orchestration/evidence/WO-RLO-015/`. Generated VREC files and their evaluator JSON belong
only under `docs/engineering/release-orchestration/verification-records/` for this work. Reserve those destinations
in scope so preparation does not need a later paperwork-only scope correction.

## Stop and escalate conditions

Stop the affected operation on mismatched scope, changed reviewed definitions,
failed required checks, unavailable required inputs or a missing provider control.
Inspect uncertain writes before retrying. Report changed scope before editing it.
Do not solve an implementation gap by weakening required verification.

## Completion report format

State implemented behavior, exact candidate, checks and limitations; link retained
evidence and the prepared verification record; report the evaluator's current next
action. Distinguish local readiness from live delivery or configuration completion.
