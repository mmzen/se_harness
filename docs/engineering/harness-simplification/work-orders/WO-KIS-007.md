+++
id = "WO-KIS-007"
type = "work_order"
title = "Delete tests for the restrictions we removed"
status = "implemented"
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
  "docs/engineering/README.md",
  "docs/engineering/harness-simplification/README.md",
  "docs/engineering/harness-simplification/architecture/ARCH-KIS-001.md",
  "docs/engineering/harness-simplification/architecture/adr/ADR-KIS-001.md",
  "docs/engineering/harness-simplification/capabilities/CAP-KIS-001.md",
  "docs/engineering/harness-simplification/coverage.md",
  "docs/engineering/harness-simplification/evidence/WO-KIS-007/",
  "docs/engineering/harness-simplification/intent/INT-KIS-001.md",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-001.md",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-002.md",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-003.md",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-004.md",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-005.md",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-006.md",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-007.md",
  "docs/engineering/harness-simplification/specifications/SPEC-KIS-001.md",
  "docs/engineering/harness-simplification/verification-records/VREC-KIS-007.evaluator-evidence.json",
  "docs/engineering/harness-simplification/verification-records/VREC-KIS-007.md",
  "docs/engineering/harness-simplification/verification/VER-KIS-001.md",
  "docs/engineering/harness-simplification/work-orders/WO-KIS-007.md",
  "docs/notes/codebase-kiss-work-orders-2026-09-13.md",
  "docs/notes/developing-se-harness.md",
  "docs/notes/test-suite.md",
  "scripts/run_tests.py",
  "tests/fixture_support.py",
  "tests/test_configuration_surface.py",
  "tests/test_engine_import_surface.py",
  "tests/test_evaluator_identity.py",
  "tests/test_hash_bound_integrity.py",
  "tests/test_instruction_architecture.py",
  "tests/test_integrity_primitives.py",
  "tests/test_interpreter_safety.py",
  "tests/test_managed_template_hygiene.py",
  "tests/test_managed_template_texts.py",
  "tests/test_module_seams.py",
  "tests/test_mutation_guard.py",
  "tests/test_one_validation.py",
  "tests/test_report_output_safety.py",
  "tests/test_suite_hygiene.py",
  "tests/test_workflow_compliance.py",
  "tests/test_workflow_execution.py",
]

[relations]
implements = ["REQ-KIS-007"]
specifications = ["SPEC-KIS-001"]
verification = ["VER-KIS-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-13T16:40:43Z"
decided_by = "engineering-owner"
reason = "The owner accepted all 38 candidates in the retained 2026-09-13 codebase KISS review and requested the work orders: \"OK ! Let's create the work orders to implement all candidates\". Record the engineering-owner approval of WO-KIS-007 within that accepted scope and the established delegated route. SPEC-KIS-001 makes the replacement contracts and seven retained protections explicit; the coverage map assigns all candidates. This records definition approval or bounded execution delegation only, not implementation start, completion, verification, release, merge, publication, live adoption or historical evidence deletion."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-14T18:37:40Z"
decided_by = "engineering-owner"
reason = "The owner confirmed PR #472 merged and continues the approved sequential KISS implementation route. Start the final approved WO-KIS-007 after WO-KIS-006 integration at c3d361353d0e5dea00078dd2413544395d593652. Remove internal-name and obsolete runtime/checkout test restrictions within K32-K34 while retaining public behavior, package import boundaries and real file safety checks."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-14T18:59:26Z"
decided_by = "delegated-executor"
reason = "Delegated DR-WO-COMPLETE under [delegation] class 'execution': required check 'validate' success at 9f734ab129d2328c89baddb549c4c40d60b8bec3 (check-run 104108101360, source github-checks). K32-K34 are implemented in source 9f734ab129d2328c89baddb549c4c40d60b8bec3. Removed 650 net test lines and 33 methods, internal-name inventories, the three-setting checkout matrix and aggressive Git GC. Real checkout and interpreter path checks passed on Windows and Linux; full local and hosted source suites each ran 1063 tests. All hosted checks are successful or intentionally skipped; both raw artifacts were downloaded and matched to the candidate. Record delegated completion under the approved scope; owner verification and integration remain pending."
+++

# Delete tests for the restrictions we removed

## Lifecycle and sequence

The owner accepted all reviewed candidates and requested these work orders on 2026-09-13, continuing the selected delegated route.
Approval grants bounded execution delegation under the currently installed DR-015 rule; it does not start implementation.
Run after WO-KIS-006 implementation is integrated. Rebase and use the current approved shared contract; avoid simultaneous edits of shared modules.
Until a separately authorized root adoption, delegated start/completion/preparation still require the approved class at the PR base and its live successful required check.
Future behavior described by this packet is not a waiver of the current governing evaluator.

## Objective

Tests check supported behavior and real failures without internal-name inventories, synthetic capability matrices or aggressive Git cleanup.

## In scope

| Accepted candidate | Change | Governing rule / check |
| --- | --- | --- |
| KISS-32 | Tests enforce internal call shapes and variable names | KIS-CUT-032 / K32 |
| KISS-33 | Checkout matrices and aggressive Git cleanup preserve the checksum design | KIS-CUT-033 / K33 |
| KISS-34 | The runtime test matrix models combinations rather than supported installations | KIS-CUT-034 / K34 |

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
Read this work order, INT-KIS-001, CAP-KIS-001, REQ-KIS-007, SPEC-KIS-001, VER-KIS-001 and the selected architecture/ADR when listed.
The engine and candidate-template component prefixes are limited to this work order's listed behavior. New files at explicitly named prospective paths are allowed.
The reserved VREC-KIS-007 paths authorize later preparation only; no verification record or result is created by this packet.
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
Obtain the released evaluator's schema-2 handoff for WO-KIS-007 and report its actual state and one next action.
Leave assurance, release, publication, merge and live adoption decisions to their explicit accountable actions.
