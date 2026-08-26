+++
id = "WO-CIP-004"
type = "work_order"
title = "Freeze the release unit by candidate commit and derive its census"
status = "approved"
owners = ["engineering-owner"]
created = "2026-08-26"
updated = "2026-08-26"
[assurance]
commit_bound_verification = "required"
rationale = "The work changes the release-contract template and adds a validator error and a CLI command that release approvals will rely on."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "templates/repository/standard/docs/engineering/templates/RELEASE_CONTRACT.template.md",
  "templates/repository/standard/scripts/validate_engineering_artifacts.py",
  "se_harness/cli.py",
  "se_harness/release_unit.py",
  "docs/notes/harnessctl-reference.md",
  "docs/notes/ci-pipeline.md",
  "docs/notes/developing-se-harness.md",
  "docs/notes/README.md",
  "docs/engineering/ci-pipeline/evidence/",
  "tests/",
]

[relations]
implements = ["REQ-CIP-004"]
specifications = ["SPEC-CIP-001"]
architecture = ["ARCH-CIP-001", "ADR-CIP-001", "ADR-CIP-002"]
verification = ["VER-CIP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-26T15:17:28Z"
decided_by = "engineering-owner"
+++

# Work Order: Freeze the release unit by candidate commit and derive its census

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification and any release decision are separate accountable acts.
`ADR-CIP-002` must be accepted before start.

## Objective

P4: `candidate_commit` and `previous_release_tag` on the release-contract
template; `harnessctl release-unit`; `E-CIP-001` in the candidate
validator; the stop-condition prose rewritten; the release sequences
updated so the next contract is drafted this way.

## In scope

`CIP-RLU` 1–4; `CIP-DOC`: `developing-se-harness.md` "Release sequences"
(the contract step, the late-fix route on `candidate/X.Y.Z`),
`harnessctl-reference.md`, `ci-pipeline.md`; scenario 4 of `VER-CIP-001`
run over `v0.6.0..e98b788` and recorded.

## Out of scope

Approved and released contracts; the root's 0.6.0 validator and templates,
which follow at the governor upgrade; lifecycle families and decision
rights; the tag and publication mechanics.

## Authorized decision envelope

The exemption syntax for trailer-less commits (a front-matter array or a
section); the JSON field names of the census.

## Constraints

The command mutates nothing and needs no network. The template change is
in `templates/` only.

## Expected change surface

One template, the candidate validator, one module, the CLI, notes, tests,
evidence.

## Required verification

`VER-CIP-001` row 4 and scenario 4; repository-required checks; full suite;
handoff check.

## Evidence to record

Under `docs/engineering/ci-pipeline/evidence/WO-CIP-004/`: the fixture
derivation, the 0.7.0 census comparison with each difference explained.

## Stop and escalate conditions

Stop if the 0.6.0 root validator rejects the new front-matter fields, or if
the first-parent walk cannot attribute a commit to a work order and no
exemption form is decided.

## Completion report format

The `harnessctl check . --artifact WO-CIP-004 --checkpoint handoff` schema-2
block verbatim with the complete changed-path set, and its `result_sha256`.
