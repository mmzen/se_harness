+++
id = "WO-AUT-002"
type = "work_order"
title = "Migrate the verification-method vocabulary and add the approval predicates"
status = "draft"
owners = ["engineering-owner"]
created = "2026-08-25"
updated = "2026-08-25"
[assurance]
commit_bound_verification = "required"
rationale = "The work rewrites metadata in every requirement of this repository and adds gate predicates; later assurance and release decisions depend on exact candidate behaviour."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "templates/repository/standard/scripts/validate_engineering_artifacts.py",
  "templates/repository/standard/docs/engineering/QUALITY_GATES.json",
  "templates/repository/standard/docs/engineering/QUALITY_GATES.md",
  "templates/repository/standard/docs/engineering/WORKFLOW.json",
  "templates/repository/standard/docs/engineering/WORKFLOW.md",
  "se_harness/quality_gates_contract.json",
  "se_harness/workflow_contract.json",
  "se_harness/workflow_contract.py",
  "se_harness/workflow_compliance.py",
  "scripts/migrate_verification_methods.py",
  "docs/engineering/",
  "tests/",
  "docs/notes/artifact-authoring.md",
]

[relations]
implements = ["REQ-AUT-003", "REQ-AUT-005"]
specifications = ["SPEC-AUT-001"]
architecture = ["ARCH-AUT-001", "ADR-AUT-001"]
verification = ["VER-AUT-001"]
+++

# Work Order: Migrate the verification-method vocabulary and add the approval predicates

## Lifecycle

Approval authorizes only the scope below; this work order depends on
`WO-AUT-001` being `implemented` and should be started after it. Start,
completion, commit-bound verification, the assurance decision, integration,
and release are separate decisions.

## Objective

Land the second increment of `SPEC-AUT-001`: the closed vocabulary as an
error, the one-time migration of this repository's requirements with its
retained mapping and steward decisions, and the two approval predicates.

## In scope

- `E-AUT-001` replacing `W-AUT-004` (`AUT-VOC-002`); the migration script
  and its run over `docs/engineering/**/requirements/` (`AUT-VOC-003`),
  touching only `verification_method` and `verification_notes` of each file.
- Evaluator `authoring_ready`, predicates `QGP-G1-AUTHORING` and
  `QGP-G2-AUTHORING`, corrective forms (`AUT-GTE-001..002`).
- Tests per `VER-AUT-001` rows 3 and 5; scenarios 4 and 5; evidence with the
  mapping table and the steward's decisions.

## Out of scope

- Any change to requirement bodies or statuses; any other template; the
  policy text beyond the vocabulary paragraph.

## Authorized decision envelope

Mapping of values that match one rule unambiguously. Not: unmatched values
(steward decision), thresholds, predicate semantics, or paths outside scope.

## Constraints

The migration is idempotent and refuses a file whose front matter it cannot
parse; verified and released records are never touched; run under the
external released evaluator's validation before and after.

## Expected change surface

Validator, both machine contracts and their prose, compliance evaluator,
one migration script, every requirement's front matter, tests, note, evidence.

## Required verification

`VER-AUT-001` rows 3 and 5 and scenarios 4-5; repository-required checks;
full suite on both platforms; released-evaluator validation before and
after the migration; handoff check with the complete changed-path set.

## Evidence to record

Under `docs/engineering/artifact-authoring/evidence/WO-AUT-002/`, including
the mapping table and the steward's decisions on unmatched values.

## Stop and escalate conditions

Stop if any requirement fails to parse, if a mapped value is ambiguous
under two rules, or if the migration would touch anything but the two fields.

## Completion report format

The `harnessctl check . --artifact WO-AUT-002 --checkpoint handoff` schema-2
block verbatim with the complete changed-path set, and its `result_sha256`.
