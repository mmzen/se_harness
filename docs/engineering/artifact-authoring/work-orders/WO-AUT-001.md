+++
id = "WO-AUT-001"
type = "work_order"
title = "Implement the authoring policy, requirement template, statement signals, attributes, and checklist"
status = "draft"
owners = ["engineering-owner"]
created = "2026-08-25"
updated = "2026-08-25"
[assurance]
commit_bound_verification = "required"
rationale = "The work adds a managed policy, changes a managed template and the validator, and touches a portable skill core; later engineering and assurance decisions depend on exact candidate behaviour."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "templates/repository/standard/docs/engineering/ARTIFACT_AUTHORING.md",
  "templates/repository/standard/ENGINEERING_HARNESS.md.tpl",
  "templates/repository/standard/docs/engineering/templates/REQUIREMENT.template.md",
  "templates/repository/standard/docs/engineering/templates/README.md",
  "templates/repository/standard/scripts/validate_engineering_artifacts.py",
  "templates/repository/standard/.agents/skills/harness-draft-change/",
  "se_harness/preflight.py",
  "se_harness/artifact_layout.py",
  "se_harness/cli.py",
  "se_harness/skill_contract.py",
  "pyproject.toml",
  "tests/",
  "docs/notes/artifact-authoring.md",
  "docs/notes/README.md",
  "docs/notes/harnessctl-reference.md",
  "docs/engineering/artifact-authoring/evidence/",
]

[relations]
implements = ["REQ-AUT-001", "REQ-AUT-002", "REQ-AUT-004", "REQ-AUT-006"]
specifications = ["SPEC-AUT-001"]
architecture = ["ARCH-AUT-001", "ADR-AUT-001"]
verification = ["VER-AUT-001"]
+++

# Work Order: Implement the authoring policy, requirement template, statement signals, attributes, and checklist

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification, the assurance decision, integration, and release are separate
decisions by the roles that own them.

## Objective

Land the first increment of `SPEC-AUT-001`: the managed policy and its
route, the requirement template with the five shapes and six headings, the
statement signals `W-AUT-001..003`, the optional attributes, and the
`create-artifact` checklist. The vocabulary migration and the approval
predicates are `WO-AUT-002`.

## In scope

- `ARTIFACT_AUTHORING.md` (`AUT-POL-001..002`), router row, preflight
  path sets, wheel data file.
- `create-artifact` checklist printing with `--quiet` (`AUT-POL-003`).
- `harness-draft-change` sentence, contract version, vectors (`AUT-POL-004`).
- Validator: `AUT-STM-001..002`, `AUT-ATT-001`, and `W-AUT-004` for the
  string-form `verification_method` (the warning half of `AUT-VOC-002`).
- Requirement template per `AUT-TPL-001..002`; templates README line.
- Tests per `VER-AUT-001` rows 1, 2, 4, 6; one note; reference update;
  evidence.

## Out of scope

- The vocabulary migration and `E-AUT-001` (`WO-AUT-002`); the approval
  predicates (`WO-AUT-002`); any other template's body; new skills.

## Authorized decision envelope

Checklist wording that preserves the spec's rules; diagnostic numbers within
the reserved `AUT` family; test names; note structure. Not: the opener set,
the thresholds, the attribute vocabulary, the heading set, or any path
outside scope.

## Constraints

Use the exact external released evaluator for identity, integrity, graph,
focus, and preflight; keep the template under 2,500 bytes; regenerate skill
vectors without writing bytecode into the core; LF line endings.

## Expected change surface

One new managed policy, router template, requirement template, validator,
preflight, artifact layout, CLI, skill contract parser, one skill core and
its vectors, tests, one note, evidence.

## Required verification

`VER-AUT-001` rows 1, 2, 4, 6 and scenarios 1-3, 6; repository-required
checks; full suite on Windows and Linux; released-evaluator validation and
review preflight; handoff check with the complete changed-path set.

## Evidence to record

Under `docs/engineering/artifact-authoring/evidence/WO-AUT-001/`.

## Stop and escalate conditions

Stop if the template cannot carry the five shapes and six headings under
2,500 bytes, if a warning would have to become an error to pass an existing
test, or if any path outside scope must change.

## Completion report format

The `harnessctl check . --artifact WO-AUT-001 --checkpoint handoff` schema-2
block verbatim with the complete changed-path set, and its `result_sha256`.
