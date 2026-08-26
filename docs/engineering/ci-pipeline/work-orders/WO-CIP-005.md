+++
id = "WO-CIP-005"
type = "work_order"
title = "Refuse the approval of a release contract whose census differs from the derivation"
status = "implemented"
owners = ["engineering-owner", "release-owner"]
created = "2026-08-26"
updated = "2026-08-26"
[assurance]
commit_bound_verification = "required"
rationale = "The predicate decides whether a release contract may leave draft; release approvals depend on the exact candidate behaviour."
decided_by = "engineering-owner"
[relations]
implements = ["REQ-CIP-004"]
specifications = ["SPEC-CIP-001"]
architecture = ["ARCH-CIP-001", "ADR-CIP-002"]
verification = ["VER-CIP-001"]
[execution_scope]
paths = [
  "se_harness/quality_gates_contract.json",
  "se_harness/workflow_contract.py",
  "se_harness/workflow_compliance.py",
  "se_harness/release_unit.py",
  "templates/repository/standard/docs/engineering/QUALITY_GATES.json",
  "templates/repository/standard/docs/engineering/QUALITY_GATES.md",
  "tests/",
  "docs/notes/ci-pipeline.md",
  "docs/notes/developing-se-harness.md",
  "docs/engineering/ci-pipeline/evidence/",
]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-26T20:22:53Z"
decided_by = "engineering-owner"
reason = "Owner decision 2026-08-26: i approve WO-CIP-005, you can start it."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-26T20:22:55Z"
decided_by = "engineering-owner"
reason = "Owner decision 2026-08-26: start."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-26T20:32:26Z"
decided_by = "engineering-owner"
reason = "Owner decision 2026-08-26: mark WO-CIP-005 implemented, after accepting interactively the three recorded deviations (bound to QG-G5-RELEASE-PREPARATION; exemptions in release_unit.untraced_exemptions; two-segment work-order ids admitted)."
+++

# Work Order: Refuse the approval of a release contract whose census differs from the derivation

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification and any release decision are separate accountable acts.

## Objective

The follow-up recorded in `WO-CIP-004`'s deviation 1. `CIP-RLU` 3 placed
`E-CIP-001` in the candidate validator; the managed validator is git-free,
so the comparison lives in `harnessctl release-unit --contract`. The
approval-time refusal belongs where `authoring_ready` lives: a quality-gate
predicate evaluated when a release contract leaves `draft`.

## In scope

- Evaluator `release_unit_ready` in `se_harness/workflow_compliance.py`,
  added to `workflow_contract.EVALUATORS`: for a `release_contract` that
  declares `candidate_commit`, derive the census with
  `se_harness.release_unit.derive_release_unit` (previous release tag from
  `previous_release_tag`, exemptions from the contract's
  `[release_unit] untraced_exemptions` array) and fail with the
  `E-CIP-001` findings of `compare_with_contract`; `not_assessable` when
  git or the tag is unavailable; `pass` for a contract that declares no
  `candidate_commit` (the allow-list form stays valid for retained
  contracts).
- Predicate `QGP-G5-RELEASE-UNIT` on the gate that governs a release
  contract's `draft -> approved` transition, in
  `se_harness/quality_gates_contract.json` and the byte-identical standard
  `QUALITY_GATES.json`; `QUALITY_GATES.md` rows; the hook in
  `ensure_governed_checkpoint` refusing the transition with the findings.
- `tests/test_release_unit.py` or a new module: a fixture repository with
  a tagged history and a draft contract approved through `transition
  --apply`: refused with `E-CIP-001` when `gates` differ, approved when they
  match; the allow-list form unaffected; `test_validation_taxonomy`'s
  declared exception for the new predicate.
- Notes: `ci-pipeline.md` ("After WO-CIP-005"), `developing-se-harness.md`
  ("Release sequences": the approval refusal).

## Out of scope

The managed validator; the release-contract template (already carries the
fields); lifecycle families and decision rights; the root's 0.6.0 copies,
which follow at the upgrade.

## Authorized decision envelope

The gate the predicate binds to (the one governing `release_contract`
approval in `WORKFLOW.json`); the exemption field's exact name.

## Constraints

The predicate never mutates and never touches the network; a repository
without git history yields `not_assessable`, not `fail`.

## Expected change surface

One evaluator, two contract files, one policy document, the compliance
hook, tests, two notes, evidence.

## Required verification

`VER-CIP-001` row 4; repository-required checks; full suite; handoff
check.

## Evidence to record

Under `docs/engineering/ci-pipeline/evidence/WO-CIP-005/`.

## Stop and escalate conditions

Stop if `WORKFLOW.json` has no single gate governing the transition, or if
the released 0.6.0 evaluator refuses the new predicate identifiers.

## Completion report format

The `harnessctl check . --artifact WO-CIP-005 --checkpoint handoff` schema-2
block verbatim with the complete changed-path set, and its `result_sha256`.
