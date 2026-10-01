+++
id = "WO-RLS-027"
type = "work_order"
title = "Prepare the bounded 0.20.1 acceptance compatibility release"
status = "implemented"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-09-30"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen confirmed required commit-bound verification by approving the reviewed 0.20.1 package. Independent qualification and release decisions rely on this executable correction."
decided_by = "mmzen"

[execution_scope]
paths = [
  "se_harness/candidate_acceptance.py",
  "tests/test_release_qualification.py",
  "pyproject.toml",
  "se_harness/__init__.py",
  "README.md",
  "docs/notes/release-qualification-roles.md",
  "docs/notes/developing-se-harness.md",
  "docs/notes/release-delivery-completion.md",
  "docs/engineering/release-0-20-1/",
]

[relations]
implements = ["REQ-SHB-008", "REQ-REB-020", "REQ-REB-031", "REQ-RLO-018", "REQ-RLO-020"]
specifications = ["SPEC-RLS-001", "SPEC-SHB-002", "SPEC-REB-010", "SPEC-REB-016", "SPEC-RLO-006"]
verification = ["VER-RLS-027"]
architecture = ["ARCH-SHB-002", "ADR-SHB-002", "ARCH-REB-009", "ADR-REB-009"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-30T19:43:46Z"
decided_by = "engineering-owner"
reason = "Human mmzen: Approve package and required verification. Approves reviewed SPEC-RLS-001, VER-RLS-027, WO-RLS-027 and REL-SEH-032 and required commit-bound verification. Includes bounded local implementation/preparation and the maintenance 0.19.0 role-label encoding, with mmzen retained as human decision-maker. Reviewed SHA256 3194607333f1cc4747e215fcf405466603907637f54b245eb52a6eeb598663f8; transition input SHA256 9618ac45645720d91a45e98e6d5c983ecb1a53e83b1bce4f82092808b581a4bd. Only confirmed assurance metadata was added to the work order. Codex applies the matching decision. Push/PR, dispatch, verification acceptance, release, publication, markers and adoption remain separate."
scope_paths = ["se_harness/candidate_acceptance.py", "tests/test_release_qualification.py", "pyproject.toml", "se_harness/__init__.py", "README.md", "docs/notes/release-qualification-roles.md", "docs/notes/developing-se-harness.md", "docs/notes/release-delivery-completion.md", "docs/engineering/release-0-20-1/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-30T19:44:15Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-30T20:23:52Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded engineering-owner approval; relevant local gates passed."
+++

# Prepare the bounded 0.20.1 acceptance compatibility release

## Objective

Produce a 0.20.1 maintenance candidate whose acceptance runner can assess the
minimal successor layout. Keep the 0.20 installer unchanged. Prepare retained
evidence and release inputs for later human verification and release decisions.
This implements the sequence selected by mmzen in DEC-IAR-004; that decision
approved preparation of this package, not its implementation.

## Baseline and execution location

The public release/0.20 branch and peeled v0.20.0 tag were both observed at
7253d13b212ad6f7df670021290fea32e81d66de on 2026-09-30. GitHub releases, remote
tags and PyPI showed no 0.20.1. Recheck these facts before starting. Use an
isolated maintenance checkout from that baseline; do not reset, rewrite or
merge the current minimal-resource branch into it.

The maintenance baseline selects released 0.19.0 in its installed root.
Reconfirm its own instructions and exact released evaluator there before any
lifecycle action. Preserve that root and CI selection. The current successor
checkout remains on 0.20.0. Exact public 0.20.0 separately qualifies the built
maintenance wheel; that role does not adopt an evaluator into either checkout.

Transport only this package and its matching recorded decisions. Existing
requirements, specifications and architecture records used here already exist
in the maintenance baseline. Do not transport the successor's formal graph or
product changes to satisfy unrelated findings. Retain DEC-IAR-004 as a decision
reference; its IAR relations are not new maintenance release members.

## In scope

1. Adapt only candidate_acceptance.py for the two layouts under SPEC-RLS-001.
   Use the reviewed successor correction as a source reference, not a whole
   commit cherry-pick. Keep the layout identifier local to the runner when the
   maintenance integrity module lacks it; do not import the successor resolver.
2. Add focused normal and refusal tests in test_release_qualification.py.
   Preserve all existing required scenarios, immutable identities and role checks.
3. Set pyproject.toml and se_harness/__init__.py to 0.20.1. No plugin source,
   installer, managed template, resource schema or lifecycle contract changes.
4. Update the four listed current documents for this maintenance candidate.
   Explain its bounded verifier change and separate successor adoption. Keep
   public availability claims at observed versions until publication succeeds.
5. Prepare the five-surface delivery plan and evidence under this domain.
   Identify downstream marketplace qualification/publication and current-main
   documentation work for separate bounded approval before release authorization.
6. Run VER-RLS-027, retain evidence, make local commits, record completion and
   prepare the commit-bound VREC. Prepare exact release-build inputs under the
   existing recipe. Subsequent RLS preparation follows the verified-candidate
   decision and release procedure; do not author a VREC or RLS by hand.

## Proposed assurance and authority

Commit-bound verification is proposed as required. Later independent candidate
qualification and release decisions will rely on this executable correction.
Human confirmation is pending; no assurance decision-maker is asserted in metadata.

Approval would authorize Codex to execute this unchanged local scope, including
start/completion transitions, tests, local commits, evidence retention and VREC
preparation. The human remains mmzen. When the maintenance-selected 0.19.0 CLI
requires its legacy role label, the approval proposal includes use of that label
only to apply mmzen's matching decision, with their identity, reviewed digest and
actual decision retained in the reason. It grants no role to the agent.

Push, PR creation, workflow dispatch, merge, human verification, RLS release,
publication, latest/last promotion and adoption require their separate decisions.
The present plan choice supplies none of them. Use ordinary local implementation
judgment within the approved rules; return scope changes for review.

## Required verification and evidence

Follow VER-RLS-027 on Windows and Linux. Retain the focused/full checks, actual
installed-wheel assessments, unchanged legacy footprint, exact minimal test input,
independent released qualification, build identities and limitations under
`evidence/WO-RLS-027/`. Preserve failures and retries. Future VREC, RLS and their
evaluator companions use this domain's normal directories and allocated IDs.

## Exclusions and stop conditions

Do not change the minimal branch, root installation, CI workflows, build recipe,
plugin code, credentials, accepted history or public refs. Do not relax a check
or import candidate code into the released verifier. Stop the affected action
on an advanced maintenance baseline, occupied version, missing fixed test input,
changed authority, unsupported transport, failed required check, or a correction
outside the exact paths. Preserve evidence and propose the bounded recovery.

## Completion report

Report the actual candidate and wheel identities, changed paths, completed
behavior, pass/fail/unassessed criteria, retained failures, remaining delivery
obligations and the selected evaluator's one next accountable decision. Local
preparation must not be presented as publication or completed successor assurance.
