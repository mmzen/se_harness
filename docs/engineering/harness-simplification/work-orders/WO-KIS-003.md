+++
id = "WO-KIS-003"
type = "work_order"
title = "Cut repeated identity proofs and locked guidance"
status = "approved"
owners = ["engineering-owner"]
created = "2026-09-13"
updated = "2026-09-13"

[delegation]
class = "execution"

[assurance]
commit_bound_verification = "required"
rationale = "Later decisions rely on changed behavior, tests or retained evidence policy."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  ".gitattributes",
  "MANIFEST.in",
  "docs/engineering/README.md",
  "docs/engineering/harness-simplification/README.md",
  "docs/engineering/harness-simplification/architecture/ARCH-KIS-001.md",
  "docs/engineering/harness-simplification/architecture/adr/ADR-KIS-001.md",
  "docs/engineering/harness-simplification/capabilities/CAP-KIS-001.md",
  "docs/engineering/harness-simplification/coverage.md",
  "docs/engineering/harness-simplification/evidence/WO-KIS-003/",
  "docs/engineering/harness-simplification/intent/INT-KIS-001.md",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-001.md",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-002.md",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-003.md",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-004.md",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-005.md",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-006.md",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-007.md",
  "docs/engineering/harness-simplification/specifications/SPEC-KIS-001.md",
  "docs/engineering/harness-simplification/verification-records/VREC-KIS-003.evaluator-evidence.json",
  "docs/engineering/harness-simplification/verification-records/VREC-KIS-003.md",
  "docs/engineering/harness-simplification/verification/VER-KIS-001.md",
  "docs/engineering/harness-simplification/work-orders/WO-KIS-003.md",
  "docs/notes/codebase-kiss-work-orders-2026-09-13.md",
  "docs/notes/developing-se-harness.md",
  "docs/notes/harness-installation-and-upgrades.md",
  "pyproject.toml",
  "scripts/check_portable_release_surface.py",
  "se_harness/cli.py",
  "se_harness/codes.py",
  "se_harness/engine/",
  "se_harness/evaluator_evidence.py",
  "se_harness/evaluator_identity.py",
  "se_harness/hash_bound.py",
  "se_harness/hash_bound_classes.json",
  "se_harness/installer.py",
  "se_harness/integrity.py",
  "se_harness/interpreter_safety.py",
  "se_harness/mutation_guard.py",
  "se_harness/preflight.py",
  "se_harness/provenance.py",
  "se_harness/release_qualification.py",
  "se_harness/runtime_identity.py",
  "se_harness/skill_ownership.py",
  "se_harness/skill_ownership_contract.json",
  "templates/repository/standard/.engineering-harness.toml.tpl",
  "templates/repository/standard/.github/workflows/engineering-harness.yml",
  "templates/repository/standard/AGENTS.md.fragment",
  "templates/repository/standard/CLAUDE.md.fragment",
  "templates/repository/standard/ENGINEERING_HARNESS.md.tpl",
  "templates/repository/standard/docs/engineering/ARTIFACT_AUTHORING.md",
  "templates/repository/standard/docs/engineering/DECISION_RIGHTS.md",
  "templates/repository/standard/docs/engineering/OPERATING_CARD.md",
  "templates/repository/standard/docs/engineering/QUALITY_GATES.json",
  "templates/repository/standard/docs/engineering/QUALITY_GATES.md",
  "templates/repository/standard/docs/engineering/TECHNICAL_COMMUNICATION.md",
  "templates/repository/standard/docs/engineering/TRACEABILITY.md",
  "templates/repository/standard/docs/engineering/WORKFLOW.json",
  "templates/repository/standard/docs/engineering/WORKFLOW.md",
  "templates/repository/standard/docs/engineering/templates/",
  "templates/repository/standard/gitattributes.fragment",
  "templates/repository/standard/gitignore.fragment",
  "tests/test_configuration_surface.py",
  "tests/test_evaluator_identity.py",
  "tests/test_governor_transition.py",
  "tests/test_harnessctl.py",
  "tests/test_hash_bound_integrity.py",
  "tests/test_instruction_architecture.py",
  "tests/test_integrity_primitives.py",
  "tests/test_interpreter_safety.py",
  "tests/test_managed_template_hygiene.py",
  "tests/test_managed_template_texts.py",
  "tests/test_mutation_guard.py",
  "tests/test_release_qualification.py",
  "tests/test_report_output_safety.py",
  "tests/test_revision_provenance.py",
  "tests/test_skill_ownership.py",
  "tests/test_standard_repository_lifecycle.py",
]

[relations]
implements = ["REQ-KIS-003"]
specifications = ["SPEC-KIS-001"]
verification = ["VER-KIS-001"]
architecture = ["ARCH-KIS-001", "ADR-KIS-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-13T16:40:43Z"
decided_by = "engineering-owner"
reason = "The owner accepted all 38 candidates in the retained 2026-09-13 codebase KISS review and requested the work orders: \"OK ! Let's create the work orders to implement all candidates\". Record the engineering-owner approval of WO-KIS-003 within that accepted scope and the established delegated route. SPEC-KIS-001 makes the replacement contracts and seven retained protections explicit; the coverage map assigns all candidates. This records definition approval or bounded execution delegation only, not implementation start, completion, verification, release, merge, publication, live adoption or historical evidence deletion."
+++

# Cut repeated identity proofs and locked guidance

## Lifecycle and sequence

The owner accepted all reviewed candidates and requested these work orders on 2026-09-13, continuing the selected delegated route.
Approval grants bounded execution delegation under the currently installed DR-015 rule; it does not start implementation.
Run after WO-KIS-002 implementation is integrated. Rebase and use the current approved shared contract; avoid simultaneous edits of shared modules.
Until a separately authorized root adoption, delegated start/completion/preparation still require the approved class at the PR base and its live successful required check.
Future behavior described by this packet is not a waiver of the current governing evaluator.

## Objective

Ordinary commands check the selected checker version and origin; full package checks happen at meaningful boundaries.

## In scope

| Accepted candidate | Change | Governing rule / check |
| --- | --- | --- |
| KISS-13 | Every new checksum field needs central classification | KIS-CUT-013 / K13 |
| KISS-14 | Correct Git attributes can still be in the wrong section | KIS-CUT-014 / K14 |
| KISS-15 | A normal Python environment under a linked directory is refused | KIS-CUT-015 / K15 |
| KISS-16 | The Python executable is hashed during runtime identity inspection | KIS-CUT-016 / K16 |
| KISS-17 | An ignored PYTHONPATH still causes refusal | KIS-CUT-017 / K17 |
| KISS-18 | A module command also requires the console launcher | KIS-CUT-018 / K18 |
| KISS-19 | Ordinary writes recompute the complete installed payload identity | KIS-CUT-019 / K19 |
| KISS-20 | A valid index install cannot prepare a release without an archive receipt | KIS-CUT-020 / K20 |
| KISS-21 | Formatting alone can invalidate evaluator evidence | KIS-CUT-021 / K21 |
| KISS-22 | Guidance, templates and policy are all treated as locked installation bytes | KIS-CUT-022 / K22 |

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
Read this work order, INT-KIS-001, CAP-KIS-001, REQ-KIS-003, SPEC-KIS-001, VER-KIS-001 and the selected architecture/ADR when listed.
The engine and candidate-template component prefixes are limited to this work order's listed behavior. New files at explicitly named prospective paths are allowed.
The reserved VREC-KIS-003 paths authorize later preparation only; no verification record or result is created by this packet.
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
Obtain the released evaluator's schema-2 handoff for WO-KIS-003 and report its actual state and one next action.
Leave assurance, release, publication, merge and live adoption decisions to their explicit accountable actions.
