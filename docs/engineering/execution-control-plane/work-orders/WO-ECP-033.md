+++
id = "WO-ECP-033"
type = "work_order"
title = "Wave 2, group C: the diagnostic-code registry and the four contract tables read at run time"
status = "implemented"
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
  "docs/engineering/execution-control-plane/decisions/",
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

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-08T09:17:36Z"
decided_by = "engineering-owner"
reason = "Approved on 2026-09-08 by the accountable owner by selecting the presented option 'Approve all six (Recommended)', given after the stacked packet pull requests #395, #396 and #397 and their summary were presented: wave 2 of the code health assessment of 2026-09-07 (issue #377) with the owner decision of issue #381 item 4, one primitive per family and the four contract tables read at run time. Approval of a definition authorizes no work. WO-ECP-033 carries no delegation class: its start, completion and record preparation are the engineering owner's explicit decisions."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-08T12:21:17Z"
decided_by = "engineering-owner"
reason = "Started on 2026-09-08 by the accountable engineering owner, by selecting the presented option 'Complete, prepare the record, start group C' after WO-ECP-032 was marked implemented and VREC-ECP-036 prepared at c829bdd5: wave 2, group C, the diagnostic-code registry and the four contract tables read at run time (SPEC-ECP-023 ECP-PRM-016 to ECP-PRM-023 and ECP-PRM-026). Start preflight PASS. Stacked on the group B branch because the two groups edit the same modules."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-08T13:54:03Z"
decided_by = "engineering-owner"
reason = "Marked implemented by the accountable engineering owner on 2026-09-08 under DR-WO-COMPLETE, by selecting the presented option 'Complete and prepare the record': se_harness/codes.py names every code the package raises once (118 constants), CodedError is the one base of a coded refusal and every refusal class exposes code and message, 270 literal sites in 19 modules are gone with the standard-library-only loader excepted, the CLI reads the two attributes and keeps one split, the index reads the registry through the parser and the page is regenerated; agentic_operations, restitution_fields, aggregation and the declared hash mode drive the gate, the guard, the result validator, the aggregator and the two writers at run time, each section validated at load and refusing with WEX-ECP-031, the Python copies gone. No recorded digest moved (CONTRACT_SHA256 a443e93d unchanged). Windows suite at its baseline (1324 tests, the one workstation error, 26 skips) at 2cd0e671 and the 13 pull-request checks of #400 green at dfa0bb7f; validate 1399 artifacts, 0 errors, 0 advisories; doctor 0 FAIL; the handoff check over the Git-derived change set from 76dc6859 passes all nine predicates over 32 paths. DEC-ECP-002 (ECP-PRM-027, three engine blocks for wave 3) accepted by the technical owner with revisit at the merge of wave 3; scope amended under DR-REMEDIATION-SCOPE for decisions/. SPEC-ECP-006 carries the ECP-PRM-026 amendment record. Evidence: docs/engineering/execution-control-plane/evidence/WO-ECP-033/WO-ECP-033-handoff.md."
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

## Scope amendment, 2026-09-08

`docs/engineering/execution-control-plane/decisions/` is added to
`[execution_scope].paths`. The execution met a rule that cannot be met by this
wave: `ECP-PRM-027` counts three cross-file blocks that each pair a copy inside
`se_harness/engine/`, which the specification and this work order leave to wave
3 (#378). The work order's stop condition for such a rule is a deviation
decision, `DEC-ECP-002`, raised in this domain's `decisions/` directory, which
the scope did not name. Decided by the accountable engineering owner on
2026-09-08 by selecting the presented option "Accept, and widen the scope".
Nothing else is widened.
