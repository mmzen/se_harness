+++
id = "WO-ECP-030"
type = "work_order"
title = "Wave 1, group C: retire renumber-artifacts, rehearse-recovery, the unwired journal and two unreachable contract entries"
status = "draft"
owners = ["engineering-owner"]
created = "2026-09-07"
updated = "2026-09-07"

[assurance]
commit_bound_verification = "required"
rationale = "The change removes two registered commands and a shipped module, edits the package contracts and their managed template copies that every consumer installs, and closes approved definitions by amendment; the release after it ships the result to every consumer."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/cli.py",
  "se_harness/mutation_guard.py",
  "se_harness/renumber.py",
  "se_harness/recovery_rehearsal.py",
  "se_harness/journaled_apply.py",
  "se_harness/quality_gates_contract.json",
  "se_harness/workflow_contract.json",
  "repository_tools/diagnostic_code_index.py",
  "templates/repository/standard/docs/engineering/QUALITY_GATES.json",
  "templates/repository/standard/docs/engineering/QUALITY_GATES.md",
  "templates/repository/standard/docs/engineering/WORKFLOW.json",
  "templates/repository/standard/docs/engineering/WORKFLOW.md",
  "tests/",
  "docs/notes/harnessctl-reference.md",
  "docs/notes/harnessctl-check.md",
  "docs/notes/diagnostic-codes.md",
  "docs/notes/evaluator-recovery-runbook.md",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/evidence/",
  "docs/engineering/execution-control-plane/verification-records/",
  "docs/engineering/execution-control-plane/requirements/REQ-ECP-017.md",
  "docs/engineering/execution-control-plane/requirements/REQ-ECP-033.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-006.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-016.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-022.md",
  "docs/engineering/execution-control-plane/verification/VER-ECP-014.md",
  "docs/engineering/execution-control-plane/verification/VER-ECP-024.md",
  "docs/engineering/execution-control-plane/work-orders/WO-ECP-030.md",
  "docs/engineering/harness-distribution/specifications/SPEC-DST-019.md",
  "docs/engineering/harness-distribution/requirements/REQ-DST-061.md",
  "docs/engineering/released-evaluator-boundary/specifications/SPEC-REB-001.md",
  "docs/engineering/released-evaluator-boundary/specifications/SPEC-REB-002.md",
  "docs/engineering/technical-communication/specifications/SPEC-TCM-002.md",
  "docs/engineering/decision-management/specifications/SPEC-DCM-001.md",
]

[relations]
implements = ["REQ-ECP-033"]
specifications = ["SPEC-ECP-022"]
verification = ["VER-ECP-024"]
+++

# Work Order: Wave 1, group C: retire renumber-artifacts, rehearse-recovery, the unwired journal and two unreachable contract entries

## Lifecycle

Draft. Approval is the engineering owner's decision; it approves no
definition. Commit-bound verification is `required`. No `architecture`
relation, as `WO-ECP-025` to `WO-ECP-027`. This group edits the candidate
template copies of `QUALITY_GATES.json`, `QUALITY_GATES.md`,
`WORKFLOW.json` and `WORKFLOW.md`; the root copies are the released 0.16.0
managed files and stay until the next root adoption, so the change reaches
this repository's own root only then. `tests/` is admitted whole because
three test modules are deleted and several pins move.

## Objective

Execute rules `ECP-DEL-020` to `ECP-DEL-032` of `SPEC-ECP-022`, on the
owner's decisions of 2026-09-07 recorded on issue #381: remove
`renumber-artifacts` and `rehearse-recovery`, retire `journaled_apply.py`,
delete the two contract entries no checkpoint can reach, regenerate the code
index, update the two notes and the runbook, and close every definition that
named the retired surface by dated amendment record.

## In scope

- Deleted: `se_harness/renumber.py`, `se_harness/recovery_rehearsal.py`,
  `se_harness/journaled_apply.py`, `tests/test_artifact_renumbering.py`,
  `tests/test_recovery_rehearsal.py`, `tests/test_journaled_apply.py`.
- `se_harness/cli.py`: both parser entries, handlers and imports out;
  `se_harness/mutation_guard.py`: `renumber-artifacts-apply` out of the
  operation set; `repository_tools/diagnostic_code_index.py`: the `REN`,
  `RR` and `JNL` prefixes out; `docs/notes/diagnostic-codes.md` regenerated.
- `se_harness/quality_gates_contract.json` and `workflow_contract.json`: the
  gate, its two predicates, the procedure and its step out; the four
  candidate template copies to match; the `QG-G0` row of
  `docs/notes/harnessctl-check.md`; "renumber apply" out of the template
  `WORKFLOW.md`.
- `tests/test_cli_shape.py`, `tests/test_mutation_guard.py`,
  `tests/test_release_build.py`, `tests/test_workflow_documentation_contract.py`,
  `tests/test_progressive_documentation.py`, `tests/test_diagnostic_code_index.py`
  and any pin on the deleted names; identity-aware comparison of the
  package contracts against the candidate template while the root lags.
- `docs/notes/harnessctl-reference.md`: the two rows, synopses and
  sections; `docs/notes/evaluator-recovery-runbook.md`: the retirement
  stated.
- Amendment records: `SPEC-DST-019` and `REQ-DST-061` (renumbering
  retired), `REQ-ECP-017`, `SPEC-ECP-006` and `VER-ECP-014` (the journal
  retired), `SPEC-REB-001` rules 6 and 8, `SPEC-REB-002` rule 14,
  `SPEC-ECP-016` `ECP-CLI-001`, `-003`, `-008`, `SPEC-TCM-002`,
  `SPEC-DCM-001`.
- The domain index; this work order's evidence packet and its record.

## Out of scope

- The root copies of the four managed documents: they move at the next
  root adoption, not here.
- Any other one-release acceptance, any tombstone guard (the `ECP-TMB`
  policy), the `hash_bound` declared-digest chain (#377).

## Authorized decision envelope

The wording of the amendment records, the runbook sentence and the
reference sections; whether one absence test replaces the three deleted
modules.

## Constraints

- The root managed set is untouched; `doctor` on this repository reads
  0.16.0's copies unchanged.
- `load_validated_contracts()` and the documentation-contract test pass on
  the candidate templates.
- The suite, `validate`, `doctor` and the handoff check pass before
  completion.

## Expected change surface

About two thousand lines out (three modules, three test modules), sixty
lines of contract JSON and template documentation, two parser blocks, one
operation set entry, three index prefixes, two notes and a runbook, eleven
amendment records, this packet.

## Required verification

Execute `VER-ECP-024` for group C; repository-required checks; the pull
request's lanes, including the candidate-package lane whose released
verifier must still accept the candidate; the handoff check; a verification
record bound to the candidate commit.

## Evidence to record

`docs/engineering/execution-control-plane/evidence/WO-ECP-030/`: the
`--help` reading, the wheel file list, the contract loader reading, the
suite reading, `validate` and `doctor` readings.

## Stop and escalate conditions

The released 0.16.0 verifier's acceptance invoking either retired command
(it does not today: its scenario list names `init`, `doctor`, `validate`,
`dashboard` and `upgrade`); a root managed path in the change set; any
consumer found to invoke either command from automation.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
