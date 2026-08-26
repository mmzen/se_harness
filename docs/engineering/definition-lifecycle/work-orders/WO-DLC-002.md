+++
id = "WO-DLC-002"
type = "work_order"
title = "Terminate the definition lifecycle at approved and derive realization"
status = "draft"
owners = ["engineering-owner"]
created = "2026-08-26"
updated = "2026-08-26"

[assurance]
commit_bound_verification = "required"
rationale = "The work retires a reachable state from the managed lifecycle contract that every consumer repository pins, retires a managed procedure and step, re-points a published recommendation identifier, and adds a coverage report over 630 definitions. An unmatched artifact-type and status pair raises in the workflow resolver at runtime. Future engineering, assurance, and release decisions depend on exact candidate behaviour."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/workflow_contract.json",
  "se_harness/workflow_contract.py",
  "se_harness/workflow.py",
  "se_harness/workflow_procedures.py",
  "se_harness/workflow_compliance.py",
  "se_harness/definition_realization.py",
  "se_harness/governance_migration.py",
  "se_harness/cli.py",
  "templates/repository/standard/docs/engineering/WORKFLOW.json",
  "templates/repository/standard/docs/engineering/WORKFLOW.md",
  "templates/repository/standard/docs/engineering/TRACEABILITY.md",
  "templates/repository/standard/scripts/inspect_engineering_artifacts.py",
  "tests/",
  "docs/notes/harnessctl-reference.md",
  "docs/notes/definition-lifecycle.md",
  "docs/engineering/definition-lifecycle/evidence/",
]

[relations]
implements = ["REQ-DLC-002", "REQ-DLC-003", "REQ-DLC-005"]
specifications = ["SPEC-DLC-002"]
architecture = ["ARCH-DLC-001", "ADR-DLC-001"]
verification = ["VER-DLC-001"]
+++

# Work Order: Terminate the definition lifecycle at approved and derive realization

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification, the assurance decision, integration, and release are separate
decisions by the roles that own them.

## Objective

Implement `SPEC-DLC-002` so that the reachable definition lifecycle ends at
`approved` with `rejected` as its only outgoing edge, so that every definition
already carrying `implemented` remains valid, visible, authority-granting, and
byte-unchanged, and so that the question the retired edge answered is answered
instead by a read-only derivation over work orders and the verification records
bound to them.

The two halves are one work order because the derivation exists only to replace
what the termination removes. Delivering the termination without the derivation
would remove an answer and supply nothing.

This increment must land after `WO-DLC-001` and before `WO-DLC-003`.

## In scope

- `lifecycles.definition.approved.transitions_to` set to `["rejected"]` in both
  byte-identical contract copies.
- The `implemented` row retained with `grants_authority: true`,
  `must_remain_visible: true`, `transitionable: false`, `transitions_to: []`, and
  a deliberately chosen `predecessor_adapter`.
- `WORKFLOW.md` state-table row changed to `| Definition | approved | rejected |`,
  with surrounding text stating that `implemented` remains accepted, visible, and
  authority-granting on existing definitions.
- `PROC-DEFINITION-COMPLETE` and `STEP-DEFINITION-COMPLETE` retired.
- `WFL-DEFINITION-COMPLETE` re-pointed at the work-selection procedure with
  `DR-WO-SELECT` and `QG-G3-WORK-AUTHORIZATION`, keeping its identifier and its
  `approved` match, with a handoff that covers the case where no work order names
  the definition yet.
- `WFL-DEFINITION-WORK` left matching `implemented`.
- Conformance test enumerating all nine definition families against every status
  in `ALLOWED_STATUSES`, asserting no pair occurring in the graph reaches
  `_recommend`'s `RuntimeError`, and asserting the reachable graph matches the
  `WORKFLOW.md` state table.
- New pure read-only derivation module: covering work-order collection over
  `implements`, `specifications`, and `architecture`; the three-way covered,
  partially covered, and uncovered classification; verification-record and bound
  commit citation; `I-DLC-001` and `W-DLC-001` joining the existing shared
  finding family, rendered in `inspect` only, with the derivation held
  surface-independent so the deferred dashboard work adds a renderer and no logic.
- Independent write sentinel asserting byte-identical files after every
  derivation run.
- Governance-migration scenario for the version pair this increment lands in,
  including the predecessor adapter path for a consumer whose evaluator still
  admits the retired edge.
- Tests and fixtures per `VER-DLC-001` scenarios 6 to 13.
- One non-authoritative note; reference updates; work-order-keyed evidence.

## Out of scope

- Any change to a definition's status, `lifecycle_events`, relations, or bytes.
  The 165 `implemented` definitions are not migrated, normalized, superseded, or
  re-decided in either direction.
- Removing `implemented` from `ALLOWED_STATUSES`, deleting the `implemented`
  contract row, or renaming `WFL-DEFINITION-COMPLETE`.
- `DR-DEFINITION-DECIDE`, which already describes only the decision that
  survives, and every other decision right, role, and quality gate.
- Any new artifact field, relation type, or artifact type in which a coverage
  result could be stored.
- The dashboard and explorer rendering of the coverage findings. Deferred to
  separately approved work by an owner decision of 2026-08-26.
  `generate_harness_dashboard.py` and `harness_explorer/` are outside this scope.
  The consequence — a finding family present in `inspect` and absent from the
  dashboard, unlike `W-HEX-*`, `W-REB-*`, and `W-REV-*` — is disclosed in the
  completion report and recorded as a residual in `VER-DLC-001`.
- The architecture-generation exemption, `E014`, `W014`, `E015`, and `W015`.
  Those belong to `WO-DLC-001` or are unchanged.
- The `lifecycle_events` obligation, `E022`, and `W025`. Those belong to
  `WO-DLC-003`.
- Editing root managed copies or `.engineering-harness.lock` of this repository.
- Approving or transitioning any definition or this work order.
- Building a release or upgrading the governor.

## Authorized decision envelope

The implementation agent may decide the derivation module's placement, function
and dataclass names, the finding message wording, the rendering order within the
existing finding family, the conformance test's organization, and the note
structure. It selects the `predecessor_adapter` value the migration contract
requires and records why.

It may not retain the `approved -> implemented` edge under any flag, delete the
`implemented` row, store the derived result anywhere, read a definition's own
status in the derivation, change the three-way classification, introduce a new
decision right, role, or gate, or change any path outside scope.

The contract-schema question is already decided and is not inside this envelope:
the retirement is a within-`se-harness-workflow-v3` change, decided 2026-08-26 by
the repository owner. The agent does not take a generation bump.

## Constraints

- Use the exact external released evaluator, invoked from outside the checkout,
  for identity, integrity, graph, focus, and preflight results. Use the candidate
  for implementation and tests.
- Keep the packaged and template contract copies byte-identical.
- The managed policy documents change in `templates/repository/standard/`. The
  root managed copies belong to the released version and are not edited.
- LF line endings.

## Expected change surface

Two byte-identical machine contracts, one managed narrative document, one managed
traceability document, five package modules, one new package module, one managed
reader script, tests and fixtures, one note, reference updates, evidence.

## Required verification

Execute `VER-DLC-001` scenarios 6 to 13 completely, plus the repository-required
checks. Full suite on Windows and Linux with figures labelled per platform.
Paired released-lineage measurement at the merge base and at the candidate,
asserting exact identifier-set equality for `W013`, `W014`, and `W015` and zero
errors at both ends. All 165 existing `implemented` definitions validated,
focused, and displayed with unchanged bytes. Review preflight and a handoff check
with the complete changed-path set.

## Evidence to record

Under `docs/engineering/definition-lifecycle/evidence/WO-DLC-002/`: exact
commands with evaluator identity and version; the transition-plan enumeration
over nine families in both directions; the recommendation-exhaustiveness
enumeration; the byte comparison of the two contract copies and the derived
reachable graph against the state table; the 165-record regression result; the
coverage classification corpus including `REQ-DST-006` and its 16 naming work
orders; write-sentinel results; the recorded `predecessor_adapter` choice and its
rationale; the migration scenario; the complete changed-path set; the disclosed
`WFL-DEFINITION-COMPLETE` name-versus-behaviour residue; material deviations.

## Stop and escalate conditions

Stop if any `(definition family, status)` pair occurring in the repository loses
its recommendation rule; if the two contract copies cannot be kept
byte-identical; if the reachable graph and the `WORKFLOW.md` state table
disagree; if the paired measurement moves any diagnostic identifier set; if the
derivation cannot be made to leave every file byte-identical; if a
`predecessor_adapter` value cannot express the retired edge without re-admitting
it; if the retirement turns out to require an `se-harness-workflow-v4` bump after
all, since the owner decided a within-`v3` change and reversing that is not inside
the envelope; if the derivation cannot be kept surface-independent, since the
deferred dashboard work depends on it; or if any path outside scope must change.

## Completion report format

Return the `harnessctl check . --artifact WO-DLC-002 --checkpoint handoff`
schema-2 block verbatim with the complete changed-path set asserted, and its
`result_sha256`.
