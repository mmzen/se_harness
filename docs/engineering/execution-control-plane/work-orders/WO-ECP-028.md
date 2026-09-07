+++
id = "WO-ECP-028"
type = "work_order"
title = "Wave 1, group A: delete dead code, orphan fixtures, dead configuration and unconsumed workflow outputs"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-09-07"
updated = "2026-09-07"

[assurance]
commit_bound_verification = "required"
rationale = "The change removes code, tests, fixtures and workflow outputs from the shipped product and its lanes; that only nothing live was removed is a fact later decisions rely on, so verification binds the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/cli.py",
  "se_harness/workflow.py",
  "se_harness/workflow_compliance.py",
  "se_harness/workflow_procedures.py",
  "se_harness/workflow_contract.py",
  "se_harness/decisions.py",
  "se_harness/runtime_identity.py",
  "se_harness/interpreter_safety.py",
  "se_harness/release_unit.py",
  "se_harness/artifact_layout.py",
  "se_harness/integrity.py",
  "se_harness/installer.py",
  "se_harness/preflight.py",
  "se_harness/candidate_acceptance.py",
  "se_harness/engine/generate_harness_dashboard.py",
  "se_harness/engine/validate_engineering_artifacts.py",
  "se_harness/engine/inspect_engineering_artifacts.py",
  "repository_tools/release_build.py",
  "MANIFEST.in",
  "pyproject.toml",
  ".github/workflows/release-qualification.yml",
  ".github/workflows/publish-pypi.yml",
  ".github/workflows/pages-publication.yml",
  ".github/workflows/candidate-evidence.yml",
  "tests/",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/evidence/",
  "docs/engineering/execution-control-plane/verification-records/",
  "docs/engineering/execution-control-plane/requirements/REQ-ECP-033.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-022.md",
  "docs/engineering/execution-control-plane/verification/VER-ECP-024.md",
  "docs/engineering/execution-control-plane/work-orders/WO-ECP-028.md",
]

[relations]
implements = ["REQ-ECP-033"]
specifications = ["SPEC-ECP-022"]
verification = ["VER-ECP-024"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-07T20:27:10Z"
decided_by = "engineering-owner"
reason = "Approved on 2026-09-07 by the accountable owner with the words 'i approve', given after the packet PR #385 and its summary were presented, as a decision distinct from the approval of its definitions in the same transaction. Authorizes bounded execution of group A only: the dead symbols, pyflakes clean, the eight orphan fixtures, the manifest line and pyproject table, the vacuous environment test and self-referential pins, the nine unconsumed workflow outputs and the candidate_version consumption, the evidence packet and the verification record. Every decision stays human: no delegation table. No managed path, no release, no publication, no merge."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-07T21:09:53Z"
decided_by = "engineering-owner"
reason = "Started on 2026-09-07 by the accountable engineering owner with the words 'you can start both' (DR-WO-START, together with the other remaining wave 1 work order), after PR #390 delivered group B. Start preflight passed at the approval commit. Execution on branch wo/ecp-028-cleanup within the declared scope only (group A)."
+++

# Work Order: Wave 1, group A: delete dead code, orphan fixtures, dead configuration and unconsumed workflow outputs

## Lifecycle

Draft. Approval is the engineering owner's decision and authorizes bounded
execution of the scope below; it approves no definition. The owner may add
`[delegation] class = "execution"` before approval; without the table every
decision stays human. Commit-bound verification is `required`. No active
architecture addresses `REQ-ECP-033`: a routine removal, so no
`architecture` relation, as `WO-ECP-025` to `WO-ECP-027`. The `tests/`
directory is admitted whole because twelve test modules carry only unused
imports and the fixtures to delete sit under it.

## Objective

Execute rules `ECP-DEL-001` to `ECP-DEL-014` and `ECP-DEL-033`, `-034` of
`SPEC-ECP-022`: the dead symbols out, `pyflakes` clean on production and
tests, the eight orphan fixtures, the manifest line, the `pyproject` table,
the vacuous environment test, the self-referential pins, the nine
unconsumed workflow outputs, and the `candidate_version` re-derivation.

## In scope

- The dead symbols, each verified `1/0` on 2026-09-07: `workflow.py`
  `_finding_key`, `_status`, the `closing_ending` local;
  `workflow_compliance.py` `focus_schema2`, `_DEFINITION_TYPES`,
  `CheckpointContext.report`; `workflow_procedures.py` `ensure_validated`;
  `workflow_contract.py` `OPERATING_CARD_PATH`, `render_operating_card` and
  its constants (with its test in `tests/test_workflow_execution.py`);
  `decisions.py` the five unused constants; `runtime_identity.py`
  `assert_runtime_identity` and the unreachable `except`;
  `interpreter_safety.py` `InterpreterSafetyError`, `OUTCOMES`,
  `EVALUATION_ORDER`; `release_unit.py` `_catalog_lookup` and its branch;
  `artifact_layout.py` the unreachable `raise` and the unused
  `artifact_type` parameter; `integrity.py` the unused `lock` parameter of
  `compare_lock_entry` (five call sites in `installer.py` and
  `preflight.py`) and the always-true conditional;
  `candidate_acceptance.py` `write_acceptance_manifest`;
  `engine/generate_harness_dashboard.py` `compute_impact` and
  `--artifact-root`; `engine/validate_engineering_artifacts.py`
  `ALLOWED_STATUSES`, `risk_acceptance`, `--artifact-root`, the unused
  `release_version` local, the `field` loop-variable shadowing;
  `engine/inspect_engineering_artifacts.py` the unreachable plane fallback.
- `pyflakes` findings: eight unused imports and three unused locals in
  production code, including `repository_tools/release_build.py`; the
  twenty-three findings in tests and the invalid escape.
- `tests/fixtures/publication_rehearsal/` (four files),
  `tests/fixtures/agentic_execution/contracts/canonical-vectors.json`,
  `phase4/authority/canonical-vectors.json`,
  `phase4/broker/canonical-vectors.json`, `phase4/workflow/model-cases.json`.
- `MANIFEST.in` line 4 and its pin in `tests/test_release_build.py`;
  `pyproject.toml` `[tool.unittest]`.
- `tests/test_workflow_execution.py` the `SE_HARNESS_AGENT_HOST` test and
  the `agent_hosts` key of `tests/fixtures/workflow_execution/scenarios.json`;
  the `len()` pins in `tests/test_context_routing_retirement.py` and
  `tests/test_predecessor_bootstrap_retirement.py`; the `41` count in
  `tests/test_fixture_support.py`; `unittest.main()` moved to the end of
  `tests/test_public_onboarding.py`.
- The `workflow_call` outputs of `release-qualification.yml` and
  `pages-publication.yml`, the five outputs of `publish-pypi.yml`, and the
  `candidate_version` consumption in `candidate-evidence.yml`; the tests
  that pin those workflows.
- The domain index; this work order's evidence packet and its record.

## Out of scope

- The declared-digest chain of `hash_bound.py`, `POLICY_PATHS`,
  `TRANSITIONS`, `RETIRED_CHECK_CODES`, the `evaluator_facts` aliases and
  the `interpreter_safety` test-only helpers: used by tests or reserved for
  #377.
- The `adopt` alias (`WO-ECP-029`); `renumber-artifacts`,
  `rehearse-recovery`, `journaled_apply.py` and the contract entries
  (`WO-ECP-030`).
- Any managed path, any behaviour a caller can reach today.

## Authorized decision envelope

The order of deletions; whether the twelve test-module import cleanups land
in one commit or several; the wording of test docstrings that mention the
removed items.

## Constraints

- No managed path moves; `doctor` reads the managed set unchanged.
- The `vulture` and `pyflakes` readings before and after go in the evidence
  packet.
- The suite, `validate`, `doctor` and the handoff check over the Git-derived
  change set pass before completion.

## Expected change surface

About three hundred lines out of the package and engine, eleven `pyflakes`
lines in production and twenty-three in tests, eight fixture files, two
configuration lines, about twenty workflow lines, this packet.

## Required verification

Execute `VER-ECP-024` in full for group A; repository-required checks; the
pull request's lanes; the handoff check; a verification record bound to the
candidate commit.

## Evidence to record

`docs/engineering/execution-control-plane/evidence/WO-ECP-028/`: the two
scan readings, the suite reading, `validate` and `doctor` readings.

## Stop and escalate conditions

A suite failure beyond the baseline that a deletion explains: the symbol was
live, stop and report; any managed path in the change set.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
