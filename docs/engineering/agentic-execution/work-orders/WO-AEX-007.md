+++
id = "WO-AEX-007"
type = "work_order"
title = "Integrate delegated workflow advancement and assurance preparation"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "technical-owner", "quality-owner", "assurance-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[assurance]
commit_bound_verification = "required"
rationale = "The work permits advance-delegated lifecycle advancement and verification-record preparation, integrates effect receipts into completion proof, and projects accountable decision packets; assurance must bind the exact workflow and stop-boundary implementation."
decided_by = "repository-owner"

[execution_scope]
paths = [
  "MANIFEST.in",
  "pyproject.toml",
  "se_harness/agent_contract.py",
  "se_harness/agent_contract.json",
  "se_harness/cli.py",
  "se_harness/delegated_workflow.py",
  "se_harness/mutation_guard.py",
  "se_harness/provenance.py",
  "se_harness/workflow.py",
  "se_harness/workflow_contract.py",
  "se_harness/workflow_contract.json",
  "templates/repository/standard/docs/engineering/DECISION_RIGHTS.md",
  "templates/repository/standard/docs/engineering/QUALITY_GATES.json",
  "templates/repository/standard/docs/engineering/QUALITY_GATES.md",
  "templates/repository/standard/docs/engineering/WORKFLOW.json",
  "templates/repository/standard/docs/engineering/WORKFLOW.md",
  "templates/repository/standard/scripts/validate_engineering_artifacts.py",
  "tests/fixtures/agentic_execution/phase4/workflow/",
  "tests/fixtures/workflow_execution/scenarios.json",
  "tests/mutation_guard_support.py",
  "tests/test_agent_contract.py",
  "tests/test_agentic_execution.py",
  "tests/test_delegated_workflow.py",
  "tests/test_lifecycle_state_contract.py",
  "tests/test_mutation_guard.py",
  "tests/test_workflow_compliance.py",
  "tests/test_workflow_documentation_contract.py",
  "tests/test_workflow_execution.py",
  "tests/test_workflow_procedures.py",
  "tests/test_workflow_restitution.py",
  "docs/notes/harnessctl-reference.md",
  "docs/engineering/agentic-execution/README.md",
  "docs/engineering/agentic-execution/evidence/WO-AEX-007-verification.md",
  "docs/notes/agentic-execution-phase4-workflow.md",
  "docs/notes/agentic-execution-roadmap.md",
  "docs/notes/README.md",
]

[relations]
implements = ["REQ-AEX-003", "REQ-AEX-004", "REQ-AEX-005", "REQ-AEX-012"]
specifications = ["SPEC-AEX-001", "SPEC-AEX-003", "SPEC-AEX-006", "SPEC-AEX-007", "SPEC-AEX-008"]
architecture = ["ARCH-AEX-001", "ADR-AEX-001", "ADR-AEX-002", "ADR-AEX-003", "ARCH-AEX-002", "ADR-AEX-006", "ADR-AEX-007"]
verification = ["VER-AEX-001", "VER-AEX-004"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T09:08:48Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-25T12:53:25Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-25T14:33:27Z"
decided_by = "engineering-owner"
+++

# Work Order: Integrate delegated workflow advancement and assurance preparation

## Lifecycle and readiness

This work order is `in_progress` after its separate approval and start
decisions. `WO-AEX-005` and `WO-AEX-006` were implemented and independently
verified at their exact commits before this work order started. The governing
Phase 4 artifact pack and both implementation-scope amendments were separately
approved.

Candidate Phase 4 code must not authorize or perform this work order's own
lifecycle transition. The existing released evaluator and accountable human
decisions continue to govern it through implementation and verification.

## Objective

Integrate the verified observer, envelope authority, effect broker, receipt
chain, mutation guard, workflow contract, lifecycle engine, provenance
preparation, CLI, quality gates, and decision packets so one logical worker can
exercise only delegated `DR-WO-START`, work-order execution,
`DR-WO-COMPLETE`, and `DR-VREC-PREPARE`, then stop for independent assurance.

## In scope

- Version the candidate workflow contract and standard workflow projection to
  register the closed four-operation Phase 4 catalog and its existing decision-
  right mappings.
- Update candidate decision-right and quality-gate projections only as needed
  to make delegation prerequisites, receipt continuity, recovery state, exact
  changed paths, and assurance-preparation gates machine-checkable.
- Implement `delegated_workflow.py` as the single coordinator for resolving
  current delegation, invoking guarded operations, binding receipts, and
  restoring canonical state.
- Register delegated start, delegated complete, and delegated VREC preparation
  as public mutation operations; reuse the broker's separately guarded effect
  operation without bypass.
- Implement clean-baseline delegated start and its session/start receipt.
- Implement completion proof across uninterrupted effect receipts, live state,
  exact work-order scope, tests, gates, retained evidence, deviations, and
  residual uncertainty.
- Integrate draft verification-record preparation with commit-bound behavior.
  If a required commit is absent, produce the Git-action stop rather than
  creating a commit.
- Project lossless v2 decision packets with exactly one next action at all
  success, failure, stop, and recovery boundaries.
- Add CLI entry points that accept argument-vector inputs, exact evaluator and
  runtime locations, artifact IDs, and machine-readable output. They do not
  execute packet commands automatically.
- Add model, transition, gate, receipt-gap, prohibited-action, and restitution
  fixtures plus bounded documentation and commit-bound evidence.

## Out of scope

- Requirement, architecture, ADR, specification, verification, work-order,
  verification-record, or release-record approval or decision.
- `DR-RLS-PREPARE`, release-record preparation, release decision, delivery
  selection, package release, installation, or target pilot.
- Git add, restore, checkout, clean, reset, commit, branch, merge, rebase, tag,
  push, pull, fetch, or another Git mutation.
- Skill procedure, skill contract, `.agents`, `.claude`, provider adapter, or
  host behavior changes; those belong to `WO-AEX-008`.
- Editing hash-locked root managed workflow, decisions, gates, templates,
  validator, instructions, lock, or released evaluator files.
- Direct worker target writes, provider-defined authority, multi-agent work,
  child delegation, parallel writers, credentials, network access, publication,
  deployment, or external action.

## Authorized decision envelope

After separate approval and start, the implementer may choose private
coordinator types, bounded CLI option names consistent with existing style,
fixture subdivision, and stable diagnostic messages behind closed codes.

The implementer may not add or activate another right or operation, change an
accountable role, legal transition, state, gate meaning, decision packet schema,
completion proof, commit-bound requirement, assurance terminal stop, mutation-
guard requirement, canonical restitution rule, or declared path. Stop and
revise the formal packet for any such need.

## Constraints

- Preserve Python 3.11+ and standard-library-only runtime behavior.
- Treat exact verified `WO-AEX-005` and `WO-AEX-006` commits and schemas as
  fixed dependency inputs.
- Require current formal delegation independently for each delegated operation.
- Perform target effects only through the broker and lifecycle effects only
  through existing legal transition/provenance operations guarded by the exact
  evaluator.
- Keep workflow JSON authoritative and Markdown a deterministic projection.
- Preserve all current nonagentic workflow behavior and default unknown rights
  to the accountable-decision stop.
- Restore canonical formal state or expose an explicit recovery block before
  yielding.
- Preserve unrelated user changes and stop on an undeclared changed path.

## Expected change surface

`delegated_workflow.py` orchestrates existing authority, effect, workflow,
provenance, and packet modules. It does not duplicate their contracts.
`workflow_contract.json` and candidate standard managed projections add the
closed mappings and checks. Existing modules receive only integration hooks and
new guarded public operation registrations.

If implementation needs a root managed file, artifact-template schema change,
skill path, provider path, installer, release module, another lifecycle state or
transition, another operation/right, or undeclared test/documentation path,
stop and revise scope.

## Scope amendment, 2026-08-25

Accepted on 2026-08-25 through the explicit governed amendment requested
during implementation. The following paths are added to `[execution_scope]`
for workflow-v4 compatibility only:

- `templates/repository/standard/scripts/validate_engineering_artifacts.py` may
  recognize the exact `se-harness-workflow-v4` managed contract while
  preserving its strict lifecycle-registry validation and v3 rejection tests;
  and
- `tests/test_lifecycle_state_contract.py` may update its exact schema fixtures
  and prove the standalone validator accepts v4 while rejecting older,
  duplicate-key, and malformed contracts.

The amendment authorizes no lifecycle, right, gate, validator-semantic, root
installed-file, wildcard, compatibility fallback, or error-suppression change.

## Scope amendment, 2026-08-25: CLI reference parity

Accepted on 2026-08-25 through the explicit governed amendment requested after
candidate-source documentation verification. The following path is added to
`[execution_scope]` for exact CLI/reference parity only:

- `docs/notes/harnessctl-reference.md` may document the new top-level
  `delegated-workflow` command and its closed `catalog`, `execute`, and
  `prepare-vrec` subcommands.

The amendment authorizes no additional command, subcommand, operation, right,
lifecycle transition, Git action, assurance decision, external effect, or
unrelated documentation change.

## Required verification

- Execute every `VER-AEX-004` method applicable to `REQ-AEX-012` and all
  affected `VER-AEX-001` lifecycle, authority, packet, restitution, and
  command-equivalence methods.
- Model-check every current state/right/operation/outcome combination. Prove only
  the three activated delegated rights can advance and all other rights stop.
- Prove start requires clean state, exact delegation, prerequisites, gates, no
  session conflict, and no recovery marker.
- Prove completion requires complete receipts, exact current state and paths,
  required tests/gates/evidence, explicit deviations/uncertainty, and no false
  claim for missing work.
- Prove VREC preparation creates reviewable undecided material, handles required
  commit presence/absence exactly, and never decides assurance or mutates Git.
- Inject stale, missing, altered, skipped, and foreign receipts; failed and not-
  assessable gates; undeclared paths; expired/wrong delegation; transition
  conflicts; and canonical-restoration failures.
- Prove prohibited release, Git, credential, network, publish, deploy, merge,
  external, child-agent, and parallel-writer requests produce zero effect and
  one exact next action.
- Prove CLI, Python, and existing command-driven workflow outcomes agree for
  equivalent nonagentic inputs.
- Run complete suite, distribution validation, candidate package acceptance,
  exact 0.6.0 doctor/formal validation, CLI help, phase preflight,
  `git diff --check`, root managed-integrity check, and changed-path comparison.

## Evidence to record

Retain exact dependency and candidate commits; candidate and 0.6.0 external
evaluator identities; workflow/decision/gate before and after contracts;
right-operation-state model results; start, effect, completion, and VREC receipt
chains; test/gate/evidence/path matrices; prohibited action results; CLI/API and
command-driven parity; canonical restitution and recovery cases; before/after
repository, formal, and Git manifests; full tests; changed paths; manual
assessments; deviations; and residual uncertainty at
`docs/engineering/agentic-execution/evidence/WO-AEX-007-verification.md`.

## Stop and escalate conditions

Stop while `draft`, before dependency verification, or without a separate start
decision. After start, stop before another path, right, operation, lifecycle
state, transition, gate meaning, skill, root managed file, Git action, release,
installation, credential, network call, or external effect.

Stop if workflow advancement can bypass live admission or mutation guard, if a
receipt gap can complete work, if VREC preparation makes an assurance decision,
if canonical restitution cannot be proved, if existing command behavior
regresses, or if a failing required verification cannot be corrected within
scope.

## Completion report format

Report `Outcome`, `Done`, `Not done`, conditional `Blocked by`, `Current
lifecycle state`, `Decision required`, `Next`, `Command or response`, and
conditional `Alternatives`. Name `WO-AEX-007`, dependency/evaluator identities,
exact changed paths, activated rights and operations, lifecycle and receipt
matrices, VREC/commit behavior, prohibited effects, evidence path, deviations,
residual uncertainty, and intentionally unperformed skills, Git, release,
network, credentials, and external actions. Recommend exactly one next step.
