+++
id = "WO-KIS-006"
type = "work_order"
title = "Keep new evidence small and assess historical archives"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-09-13"
updated = "2026-09-14"

[delegation]
class = "execution"

[assurance]
commit_bound_verification = "required"
rationale = "Later decisions rely on changed behavior, tests or retained evidence policy."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  ".github/workflows/candidate-evidence.yml",
  ".github/workflows/predecessor-evaluator-assessment.yml",
  ".github/workflows/publication-rehearsal.yml",
  ".github/workflows/publish-pypi.yml",
  ".github/workflows/release-candidate-replay.yml",
  ".github/workflows/release-qualification.yml",
  "docs/engineering/README.md",
  "docs/engineering/harness-simplification/README.md",
  "docs/engineering/harness-simplification/architecture/ARCH-KIS-001.md",
  "docs/engineering/harness-simplification/architecture/adr/ADR-KIS-001.md",
  "docs/engineering/harness-simplification/capabilities/CAP-KIS-001.md",
  "docs/engineering/harness-simplification/coverage.md",
  "docs/engineering/harness-simplification/evidence/WO-KIS-006/",
  "docs/engineering/harness-simplification/intent/INT-KIS-001.md",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-001.md",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-002.md",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-003.md",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-004.md",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-005.md",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-006.md",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-007.md",
  "docs/engineering/harness-simplification/specifications/SPEC-KIS-001.md",
  "docs/engineering/harness-simplification/verification-records/VREC-KIS-006.evaluator-evidence.json",
  "docs/engineering/harness-simplification/verification-records/VREC-KIS-006.md",
  "docs/engineering/harness-simplification/verification/VER-KIS-001.md",
  "docs/engineering/harness-simplification/work-orders/WO-KIS-006.md",
  "docs/notes/codebase-kiss-work-orders-2026-09-13.md",
  "docs/notes/developing-se-harness.md",
  "docs/notes/evidence-retention.md",
  "repository_tools/release_distribution.py",
  "scripts/inventory_evidence.py",
  "scripts/record_evidence.py",
  "scripts/validate_release_distributions.py",
  "se_harness/release_qualification.py",
  "tests/test_ci_pipeline.py",
  "tests/test_evidence_inventory.py",
  "tests/test_release_evidence_audit.py",
  "tests/test_release_qualification.py",
]

[relations]
implements = ["REQ-KIS-006"]
specifications = ["SPEC-KIS-001"]
verification = ["VER-KIS-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-13T16:40:43Z"
decided_by = "engineering-owner"
reason = "The owner accepted all 38 candidates in the retained 2026-09-13 codebase KISS review and requested the work orders: \"OK ! Let's create the work orders to implement all candidates\". Record the engineering-owner approval of WO-KIS-006 within that accepted scope and the established delegated route. SPEC-KIS-001 makes the replacement contracts and seven retained protections explicit; the coverage map assigns all candidates. This records definition approval or bounded execution delegation only, not implementation start, completion, verification, release, merge, publication, live adoption or historical evidence deletion."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-14T18:07:00Z"
decided_by = "engineering-owner"
reason = "The owner confirmed PR #471 merged and continues the approved sequential implementation route. Start the next approved WO-KIS-006 after WO-KIS-005 integration at d52e6a88efb819bc36d082503813d55a995f6aa8. Implement concise future evidence and assess historical archives within the accepted K31 scope; no archive deletion, release or owner assurance is authorized."
+++

# Keep new evidence small and assess historical archives

## Lifecycle and sequence

The owner accepted all reviewed candidates and requested these work orders on 2026-09-13, continuing the selected delegated route.
Approval grants bounded execution delegation under the currently installed DR-015 rule; it does not start implementation.
Run after WO-KIS-005 implementation is integrated. Rebase and use the current approved shared contract; avoid simultaneous edits of shared modules.
Until a separately authorized root adoption, delegated start/completion/preparation still require the approved class at the PR base and its live successful required check.
Future behavior described by this packet is not a waiver of the current governing evaluator.

## Objective

New runs retain useful summaries and downloadable logs; the owner gets an inventory of existing large bundles.

## In scope

| Accepted candidate | Change | Governing rule / check |
| --- | --- | --- |
| KISS-31 | Historical evidence dominates the current checkout | KIS-CUT-031 / K31 |

Implement the listed replacements, delete obsolete checks/tests for those replacements, and update current explanatory notes and candidate templates together.
Use SPEC-KIS-001's concrete choices and compatibility table. Keep KIS-KEEP-039 through KIS-KEEP-045 where applicable.


## Out of scope

- Other work orders' implementation outcomes, except reuse of their already integrated changes.
- Editing installed root managed copies, changing the root evaluator, publishing a release or applying changes to live user repositories.
- Rewriting historical approvals, VRECs, RLS records or their bound evidence, and deleting Git history.
- New locks, signature services, approval receipts, competing-editor protocols or synthetic threat matrices.

## Authorized decision envelope

Choose straightforward helper names, public diagnostics and small fixtures within the contract.
Remove obsolete assertions together with their behavior. Do not keep them as another mode merely to satisfy old tests.
Use exact files or named component directories in execution_scope. Candidate policy changes belong in templates/repository/standard, never this root's locked copies.
Historical records remain unchanged; the new applicability table states which older expectations this delivery replaces.
Any additional required implementation file needs a bounded scope amendment, not a blanket repository-wide allowance.

## Constraints and expected change surface

The reviewed baseline is 93677e69dacb08367a7079e3372118c5064087c8. The isolated governing evaluator is released 0.17.0.
Read this work order, INT-KIS-001, CAP-KIS-001, REQ-KIS-006, SPEC-KIS-001, VER-KIS-001 and the selected architecture/ADR when listed.
The engine and candidate-template component prefixes are limited to this work order's listed behavior. New files at explicitly named prospective paths are allowed.
The reserved VREC-KIS-006 paths authorize later preparation only; no verification record or result is created by this packet.
For WO-KIS-006, historical archive implementation means the accepted assessment and future-run retention changes; an irreversible archive move is a separate exact action.

## Required verification

Meet the selected checks in VER-KIS-001 and the repository's current required checks.
Use a disposable target and non-promotable candidate wheels outside the checkout when installed acceptance is necessary.
Keep expected results independent of candidate output and retain actual failures rather than weakening assertions to obtain green CI.

## Evidence to record

Retain a concise result for every selected acceptance outcome, the exact candidate, commands and useful CI/raw-result references.
Report what code, tests, blocking conditions or repeated CI work disappeared. Measure speed only when it is actually compared.
Store this work order's evidence under its named directory; do not copy an entire checkout there.

## Stop and escalate conditions

Stop for a real failed retained boundary, a required failing gate, an unresolved material contract conflict or a necessary change beyond scope.
An old test of an explicitly retired restriction is an expected test update, not a reason to resurrect the restriction.
An unavailable platform is untested; a proposed record is not verified; a green candidate cannot approve itself.

## Completion report format

State the simpler behavior, accepted candidates completed, checks run, observed reduction and material remaining limitation.
Obtain the released evaluator's schema-2 handoff for WO-KIS-006 and report its actual state and one next action.
Leave assurance, release, publication, merge and live adoption decisions to their explicit accountable actions.

## Bounded implementation scope amendment — 2026-09-14

The accepted K31 implementation uses `scripts/record_evidence.py` beside the inventory command to capture a short summary and a separate full test log. Add this exact repository-owned helper to the execution scope under the approved decision envelope. It implements the existing retention contract without changing assurance, publication, or historical archive authority.
