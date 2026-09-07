+++
id = "WO-ECP-027"
type = "work_order"
title = "Wave 0 correctness: uniform exit codes, one code per line, bounded launches, four latent defects"
status = "approved"
owners = ["engineering-owner"]
created = "2026-09-07"
updated = "2026-09-07"

[assurance]
commit_bound_verification = "required"
rationale = "The change alters the exit-code behaviour of the public CLI that agents and CI lanes branch on, and touches the mutation guard's exception type and two publication workflows; the release after it ships the result to every consumer."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/cli.py",
  "se_harness/mutation_guard.py",
  "se_harness/gate_source.py",
  "se_harness/artifact_layout.py",
  "se_harness/engine/generate_harness_dashboard.py",
  "repository_tools/evaluator_facts.py",
  "repository_tools/upgrade_rehearsal.py",
  ".github/workflows/pages-publication.yml",
  ".github/workflows/publish-pypi.yml",
  "tests/test_cli_shape.py",
  "tests/test_workflow_execution.py",
  "tests/test_mutation_guard.py",
  "tests/test_hash_bound_integrity.py",
  "tests/test_delegation_class.py",
  "tests/test_revision_provenance.py",
  "tests/test_decision_management.py",
  "tests/test_artifact_authoring.py",
  "tests/test_ci_pipeline.py",
  "tests/test_dashboard_publication.py",
  "tests/test_dashboard_webui.py",
  "tests/test_inspection.py",
  "tests/test_pypi_publishing.py",
  "tests/test_upgrade_rehearsal.py",
  "tests/test_workflow_procedures.py",
  "tests/test_workflow_restitution.py",
  "docs/notes/harnessctl-reference.md",
  "docs/notes/harnessctl-check.md",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/evidence/",
  "docs/engineering/execution-control-plane/verification-records/",
  "docs/engineering/execution-control-plane/requirements/REQ-ECP-032.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-021.md",
  "docs/engineering/execution-control-plane/verification/VER-ECP-023.md",
  "docs/engineering/execution-control-plane/work-orders/WO-ECP-027.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-016.md",
]

[relations]
implements = ["REQ-ECP-032"]
specifications = ["SPEC-ECP-021"]
verification = ["VER-ECP-023"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-07T19:33:14Z"
decided_by = "engineering-owner"
reason = "Approved on 2026-09-07 by the accountable owner with the words 'i approve', given after the packet PR #382 and its summary were presented, as a decision distinct from the approval of its definitions in the same transaction. Authorizes bounded execution of the declared scope only: the handlers and main() in cli.py, MutationGuardError, the three launchers, the regex, the CRLF parser, the projection, the two workflows, the sixteen test modules, the two notes, the two amendment records on SPEC-ECP-016, the domain index, the evidence packet and the verification record. Every decision stays human: no delegation table. It authorizes no registered command change, no managed path, no release, no publication and no merge; the merges remain the owner's decisions."
+++

# Work Order: Wave 0 correctness: uniform exit codes, one code per line, bounded launches, four latent defects

## Lifecycle

Draft. Approval is the engineering owner's decision and authorizes bounded
execution of the scope below; it approves no definition, which each
accountable owner approves separately. The owner may add
`[delegation] class = "execution"` before approval, as `WO-ECP-025` did;
without the table every decision stays human. Commit-bound verification is
`required`. No active architecture addresses `REQ-ECP-032`: a routine
correctness change, so no `architecture` relation, as `WO-ECP-025` and
`WO-ECP-026`.

## Objective

Close issue #375, wave 0 of the code health assessment of 2026-09-07: one
code splitter on every result path (`ECP-COR-001`), a typed mutation-guard
error re-raised uniformly and `transition` brought onto the exit-2 rule
(`ECP-COR-002`), the shared exception tuple in every result-building handler
and in `main()` (`ECP-COR-003`), `dashboard --json` and `pr-body` on the
rule (`ECP-COR-004`, `-005`), bounded launches (`ECP-COR-006`), the four
latent defects (`ECP-COR-007` to `-010`), the tests (`ECP-COR-011`) and the
documentation and amendment records (`ECP-COR-012`).

## In scope

- `se_harness/cli.py`: the handlers named in `ECP-COR-001` to `-005`,
  `main()`, the engine launchers' timeouts.
- `se_harness/mutation_guard.py`: `MutationGuardError`.
- `se_harness/gate_source.py`: `_git` timeout and start-failure handling.
- `se_harness/artifact_layout.py`: `REF_ARTIFACT_PATTERN` from `_REF_PREFIX`.
- `se_harness/engine/generate_harness_dashboard.py`: the
  `verification_method` projection.
- `repository_tools/evaluator_facts.py`: CRLF-safe front matter;
  `repository_tools/upgrade_rehearsal.py`: `run` timeout.
- `.github/workflows/pages-publication.yml`, `publish-pypi.yml`: the digest
  reads and the two `setup-python` steps.
- The test modules listed in the scope; the two notes; the two amendment
  records on `SPEC-ECP-016`; the domain index; the evidence packet and the
  verification record.

## Out of scope

- The `renumber-artifacts` human output on stderr (the command is removed
  under #376), the diagnostic-code registry and the single Git launcher
  (#377), any change to `CODE_PREFIX`'s code families, the dead workflow
  outputs (#376).
- Any registered command, option, result schema, contract file, managed
  template, release or publication.

## Authorized decision envelope

Test names and placement; the wording of the reference rows and the
amendment records; whether the engine timeout is a constant or a parameter;
the exact bound on the `error` member.

## Constraints

- No managed path moves; `doctor` reads the managed set unchanged.
- Each latent defect gets its failing test before the fix; both readings go
  in the evidence packet.
- The suite, `validate`, `doctor` and the handoff check over the Git-derived
  change set pass before completion; the hosted lanes, including the two
  publication workflows' pin tests, stay green.

## Expected change surface

About sixty lines in `cli.py`, ten in `mutation_guard.py`, ten in
`gate_source.py`, one regex, one projection branch, one parser, one
`timeout=` keyword, six workflow lines, about ten tests, two reference rows,
two amendment records, this packet.

## Required verification

Execute `VER-ECP-023` in full; repository-required checks; the pull
request's lanes; the handoff check over the Git-derived change set; a
verification record bound to the candidate commit.

## Evidence to record

`docs/engineering/execution-control-plane/evidence/WO-ECP-027/`: the
before-and-after readings for the doubled code and each latent defect, the
suite reading on both platforms, `validate` and `doctor` readings, the
`subprocess.run` timeout inspection.

## Stop and escalate conditions

A suite failure beyond the baseline that the change does not explain; any
consumer found to depend on `transition` exiting 1 for a guard refusal; any
need to touch a managed path or a result schema.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
