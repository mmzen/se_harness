+++
id = "WO-ECP-033"
type = "work_order"
title = "Wave 2, group C: the diagnostic-code registry and the four contract tables read at run time"
status = "draft"
owners = ["engineering-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[assurance]
commit_bound_verification = "required"
rationale = "This group changes how every coded refusal is named and makes four contract sections drive the delegation gate, the guard, the result renderer, the aggregator and two digest producers; that behaviour on the unchanged contracts equals main's is a fact every later gate reading relies on, so verification binds the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/codes.py",
  "se_harness/artifact_layout.py",
  "se_harness/candidate_acceptance.py",
  "se_harness/cli.py",
  "se_harness/decisions.py",
  "se_harness/evaluator_evidence.py",
  "se_harness/evaluator_identity.py",
  "se_harness/gate_source.py",
  "se_harness/github_ci.py",
  "se_harness/hash_bound.py",
  "se_harness/installer.py",
  "se_harness/integrity.py",
  "se_harness/interpreter_safety.py",
  "se_harness/mutation_guard.py",
  "se_harness/preflight.py",
  "se_harness/provenance.py",
  "se_harness/release_qualification.py",
  "se_harness/release_unit.py",
  "se_harness/risks.py",
  "se_harness/runtime_identity.py",
  "se_harness/workflow.py",
  "se_harness/workflow_compliance.py",
  "se_harness/workflow_contract.py",
  "se_harness/workflow_procedures.py",
  "se_harness/workflow_result.py",
  "repository_tools/diagnostic_code_index.py",
  "docs/notes/diagnostic-codes.md",
  "tests/",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/evidence/",
  "docs/engineering/execution-control-plane/verification-records/",
  "docs/engineering/execution-control-plane/requirements/REQ-ECP-034.md",
  "docs/engineering/execution-control-plane/verification/VER-ECP-025.md",
  "docs/engineering/execution-control-plane/work-orders/WO-ECP-033.md",
  "docs/engineering/execution-control-plane/specifications/",
  "docs/engineering/workflow-execution/specifications/",
  "docs/engineering/hash-bound-integrity/specifications/",
]

[relations]
implements = ["REQ-ECP-034"]
specifications = ["SPEC-ECP-023"]
verification = ["VER-ECP-025"]
+++

# Work Order: Wave 2, group C: the diagnostic-code registry and the four contract tables read at run time

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. Commit-bound verification is `required`.

## Objective

Execute rules `ECP-PRM-016` to `ECP-PRM-023` and `ECP-PRM-026` of
`SPEC-ECP-023`: every diagnostic code of the package named once in
`se_harness/codes.py`, one `CodedError` base, the code index reading that
module; and, on the owner's decision of 2026-09-07 recorded on issue #381,
the four declarative contract sections read at run time with their Python
copies removed.

## In scope

- `se_harness/codes.py`: a constant per code the package raises today
  (`WEX*`, `WEX-ECP-*`, `MG00*`, `RID0*`, `CC00*`, `CP00*`, `RR00*`,
  `E-RSK-*`, `W-RSK-*` and the rest), grouped by family; `CodedError` with
  `code` and `message`; the five carriage idioms and the five splitting
  idioms reduced to the class and one split.
- `repository_tools/diagnostic_code_index.py` reading the registry for the
  package and keeping its scan of the engine until wave 3; the page
  regenerated and compared.
- `gate_source.py` and `mutation_guard.py` reading `agentic_operations`
  from `workflow_contract.json`: the three delegated operations, their
  rights and transitions; `DELEGATED_RIGHTS`, `DELEGATED_TRANSITIONS` and
  the three delegated names in `PUBLIC_MUTATION_OPERATIONS` derived from it.
- `workflow_result.py` reading `restitution_fields`; the aggregator of
  `workflow_compliance.py` reading `aggregation`; the evaluator-evidence
  writer and the lock writer hashing through `declared_digest` under the
  declared mode.
- Validation of each read section at load, with one refusal code in the
  `WEX-ECP-030` family; the sync tests that pinned the copies retired.
- Amendment records where `SPEC-ECP-018`, `SPEC-ECP-006` or a
  hash-bound-integrity specification names a Python table as operative.
- Tests, the domain index, this work order's evidence packet and its
  record.

## Out of scope

- The engine's code literals (wave 3, #378); the lane scripts.
- Groups A and B (`WO-ECP-031`, `WO-ECP-032`).
- Any change to a contract JSON byte; any code text, so the committed
  diagnostic-code page changes only where the index's attribution moves.

## Expected change surface

One new package module, about twenty-five modules touched at their raise
sites, four readers wired, the sync tests retired, the page regenerated,
two or three amendment records, this packet.

## Evidence to record

`docs/engineering/execution-control-plane/evidence/WO-ECP-033/`: the
literal grep before and after, the regenerated page comparison, the four
throwaway refusals, the scan readings, the suite reading, `validate` and
`doctor` readings.

## Authorized decision envelope

The order of edits inside the group; helper names beyond those the
specification fixes; whether the group lands as one commit or several.

## Constraints

- No managed path moves; `doctor` reads the managed set unchanged.
- No contract JSON byte and no candidate template byte changes
  (`ECP-PRM-025`); no engine file changes (wave 3, #378).
- Every recorded digest equals `main`'s before completion (`ECP-PRM-024`).
- The scan readings before and after go in the evidence packet.
- The suite, `validate`, `doctor` and the handoff check over the Git-derived
  change set pass before completion.

## Required verification

Execute `VER-ECP-025` in full for this group; repository-required checks;
the pull request's lanes; the handoff check; a verification record bound to
the candidate commit.

## Stop and escalate conditions

A recorded digest that differs from `main`; a suite failure beyond the
baseline that a consolidation explains: two copies disagreed and a caller
depended on the difference, stop and report; a need to change a contract
JSON byte; any managed or engine path in the change set.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
