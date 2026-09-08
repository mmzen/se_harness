+++
id = "WO-ECP-035"
type = "work_order"
title = "Wave 3, group B: one validation per governance command"
status = "draft"
owners = ["engineering-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[assurance]
commit_bound_verification = "required"
rationale = "This group changes when every governance command validates the repository and how the report travels to preflight, the snapshot builder, provenance and qualification; that each command's result is byte-identical on the unchanged graph is a fact every later gate reading relies on, so verification binds the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/engine/",
  "se_harness/cli.py",
  "se_harness/codes.py",
  "se_harness/installer.py",
  "se_harness/preflight.py",
  "se_harness/provenance.py",
  "se_harness/release_qualification.py",
  "se_harness/risks.py",
  "se_harness/workflow.py",
  "se_harness/workflow_compliance.py",
  "se_harness/workflow_contract.py",
  "tests/",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/decisions/",
  "docs/engineering/execution-control-plane/evidence/",
  "docs/engineering/execution-control-plane/verification-records/",
  "docs/engineering/execution-control-plane/requirements/REQ-ECP-035.md",
  "docs/engineering/execution-control-plane/specifications/",
  "docs/engineering/execution-control-plane/verification/VER-ECP-026.md",
  "docs/engineering/execution-control-plane/work-orders/WO-ECP-035.md",
  "docs/engineering/instruction-architecture/specifications/",
  "docs/engineering/workflow-execution/specifications/",
]

[relations]
implements = ["REQ-ECP-035"]
specifications = ["SPEC-ECP-024"]
verification = ["VER-ECP-026"]
+++

# Work Order: Wave 3, group B: one validation per governance command

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. Commit-bound verification is `required`.

## Objective

Execute rules `ECP-ENG-010` to `ECP-ENG-016` and `ECP-ENG-023` to
`ECP-ENG-026` of `SPEC-ECP-024`: each governance command validates the
repository at most once and passes the report on; `doctor` and `inspect`
stop running work they discard; one skew classifier serves `preflight` and
`check`; every recorded output is byte-identical.

## In scope

- `run_preflight(report=...)`, the snapshot builder, `provenance` and
  `release_qualification` taking the in-process `ValidationReport`; no
  re-parse of artifact TOML from the validator's dicts.
- `check --checkpoint start` and `--from-git` validating once;
  `capture-verification` and `prepare-release` building the snapshot from
  the validation they hold; `doctor` reading `W013` from the layout pass
  alone; `inspect` deriving its queues from one validation and the
  in-process snapshot without writing the Explorer bundle.
- One skew classifier for `preflight` and `check --checkpoint start`; the
  evidence names every artifact whose preflight verdict changes on this
  repository.
- A counting test: every governance command on a fixture repository under a
  patch on `validate_repository`, one call or none.
- Amendment records on any approved specification `ECP-ENG-025` reaches.
- Tests, the domain index, this work order's evidence packet and its record.

## Out of scope

- The import surface and the twins (group A, `WO-ECP-034`); any split of a
  module (group C, `WO-ECP-036`).
- Any change to an engine argument, output format, exit code or diagnostic
  code, message or order; any contract JSON or template byte.
- The hosted lanes' own duplicate runs (wave 5, #380).

## Expected change surface

About eight package modules touched at their validation sites; the engine's
snapshot and inspection builders given a report parameter; one new test
module; one or two amendment records; this packet.

## Evidence to record

`docs/engineering/execution-control-plane/evidence/WO-ECP-035/`: the
per-command validation counts before and after, the byte-identity readings
at the base and at the candidate, the wall-clock reading of `check
--checkpoint start` and `capture-verification` before and after, the
preflight verdict changes, the suite reading, `validate` and `doctor`
readings.

## Authorized decision envelope

The order of edits inside the group; the parameter shape by which the
report travels; whether `inspect` keeps an opt-in to write the bundle;
whether the group lands as one commit or several.

## Constraints

- No managed path moves; `doctor` reads the managed set unchanged.
- No contract JSON byte and no candidate template byte changes
  (`ECP-ENG-024`); every recorded digest equals `main`'s (`ECP-ENG-023`).
- Every recorded output byte-identical at completion (`ECP-ENG-016`).
- The suite, `validate`, `doctor` and the handoff check over the Git-derived
  change set pass before completion.

## Required verification

Execute `VER-ECP-026` in full for this group; repository-required checks;
the pull request's lanes; the handoff check; a verification record bound to
the candidate commit.

## Stop and escalate conditions

A recorded output or digest that differs from `main`'s; a command whose
result depends on validating twice: stop and report; a need to change an
engine argument, output, exit code or diagnostic; a rule that cannot be met
as written, which is a deviation decision in this domain's `decisions/`.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
