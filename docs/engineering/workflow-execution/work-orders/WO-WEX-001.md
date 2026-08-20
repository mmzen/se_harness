+++
id = "WO-WEX-001"
type = "work_order"
title = "Implement deterministic scoped workflow execution"
status = "in_progress"
owners = ["repository-owner", "engineering-owner", "quality-owner"]
created = "2026-08-20"
updated = "2026-08-20"

[assurance]
commit_bound_verification = "required"
rationale = "The work changes public CLI behavior, formal lifecycle mutation, persistent governance metadata, validation, managed templates, and agent-facing workflow output; future engineering, assurance, and release decisions rely on the correctness of the exact resulting trusted state."
decided_by = "repository-owner"

[relations]
implements = ["REQ-WEX-001", "REQ-WEX-002", "REQ-WEX-003", "REQ-WEX-004", "REQ-WEX-005"]
specifications = ["SPEC-WEX-001"]
architecture = ["ARCH-WEX-001", "ADR-WEX-001"]
verification = ["VER-WEX-001"]
+++

# Work Order: Implement deterministic scoped workflow execution

## Lifecycle and authorization

The technical owner accepted `ADR-WEX-001` and approved `ARCH-WEX-001`, and the engineering owner explicitly approved this work order for implementation on 2026-08-20. The isolated released `0.5.0a1` evaluator passed start preflight, its complete manifest was read, and the owner's instruction `Begin implementation of WO-WEX-001` moved this work order to `in_progress`. Execution remains bounded to the scope below.

Commit-bound verification is `required` because this packet changes executable workflow policy and the formal state used by later engineering, assurance, and release decisions. The work order does not authorize a commit, push, pull request, VREC decision, release, tag, publication, deployment, or operation.

## Objective

Make one selected governance scope execute predictably across supported agents by implementing the provider-neutral focus, transition, preparation, metadata, atomicity, and canonical handoff contracts in `SPEC-WEX-001` without adding trusted-base diff enforcement.

## In scope

- Add one shared workflow kernel and typed plan/result models inside the Python package.
- Add the read-only `harnessctl focus` interface for selected WO, VREC, and RLS scope.
- Add the plan-by-default, explicit-apply `harnessctl transition` interface with graph-valid multi-artifact transactions.
- Implement the lifecycle registry, state preconditions, terminal-state behavior, actor assertions, exact permitted field sets, and derived assurance/release projections.
- Route `capture-verification` and `prepare-release` through the shared planning and result boundary while enforcing the approved stricter preconditions.
- Separate preparation metadata from accountable verification, release, rejection, and supersession decision metadata.
- Add append-only lifecycle-event metadata and validator invariants for new transitions while preserving unchanged legacy records.
- Ensure VREC and RLS transitions do not implicitly mutate related work orders or provenance records.
- Implement one versioned `WorkflowResult`, canonical JSON output, compact human rendering, and closed next-step mapping.
- Implement repository-contained staging, stale-input detection, whole-packet proposed-final-graph validation, atomic replacement, and rollback.
- Update public help/reference documentation, practical workflow examples, formal templates, canonical standard repository templates, and managed content where required.
- Add focused unit, black-box CLI, failure-injection, hostile-input, fresh-install, upgrade, integrity, parity, and supported-agent adapter conformance tests.
- Retain complete work-order-keyed evidence and stop at an uncommitted implemented candidate unless later authority is granted.

## Out of scope

- `REQ-WEX-006`, trusted-base comparison, lifecycle-diff validation, direct-edit enforcement, or a new CI transition-history gate.
- A provider-specific ChatGPT, Claude, or Codex Skill; plugin packaging; or making prompt text an enforcement boundary.
- Authentication or proof that a supplied actor holds an accountable role.
- Automatic migration, normalization, or reopening of historical repository-owned artifacts.
- Automatic WO changes during VREC decisions or automatic VREC/WO changes during RLS decisions.
- A hosted service, daemon, database, network API, telemetry, new runtime dependency, or installation profile.
- Inferring work scope from a branch, commit message, pull-request prose, filename, or conversation.
- Commit, push, pull-request creation, merge, VREC verification, release authorization, tag, publication, deployment, or operational action.
- Version change, promotable distribution build, governor activation, or release preparation.

## Authorized decision envelope

Implementation may choose internal Python module and class names, immutable model representation, private helper boundaries, repository-contained temporary naming, locking primitive, rollback journal representation, test fixture organization, and compact terminal layout. It may refactor existing parser or validator helpers when necessary to create one kernel and retain existing public behavior outside the selected contract.

Implementation may not change the public command shapes, transition table, scope traversal, metadata names or semantics, `WorkflowResult` fields, one-primary-recommendation rule, authority boundary, legacy compatibility rule, or explicit exclusions without a revised governing artifact and accountable approval. It may not weaken no-partial-write behavior or add a second workflow rule source in an adapter, renderer, or command.

## Constraints

- Preserve one standard installation and Python 3.11+ standard-library runtime behavior.
- Treat paths, target content, TOML metadata, IDs, actor/reason text, evidence, Git observations, lock data, and terminal content as untrusted.
- Resolve and validate the complete plan before writes; apply only the exact plan after stale-input checks.
- Keep staged files outside formal discovery paths, constrain every path to the repository, and prove rollback or stop with an explicit restoration failure.
- Preserve unrelated owner content and every immutable VREC/RLS candidate, evidence, coverage, snapshot, supersession, and release fact.
- Keep human and JSON rendering dependent on one semantic result and keep CLI/Skill adapters free of domain rules.
- Preserve repository-wide `inspect` output and suggestion behavior; selected-scope behavior belongs to `focus`.
- Keep the released governing evaluator separate from candidate source and candidate-package evidence.
- Reconcile root managed files only through the supported transaction and keep canonical standard templates consistent with the candidate package.
- Do not build a promotable release distribution.

## Expected change surface

- Public CLI parser and command dispatch.
- Formal artifact indexing, lifecycle policy, scope projection, transaction planning/writing, metadata encoding, and result rendering components in the Python package.
- Snapshot validator rules for lifecycle-event, preparation, decision, and immutable-field consistency.
- VREC/RLS preparation implementations and public command documentation.
- Formal artifact templates and canonical standard repository templates.
- Managed workflow/router content only where needed to route agents to the executable contract.
- Focused public CLI, artifact-authoring, provenance, lifecycle, inspection-regression, installer/upgrade, integrity, and distribution tests.
- Workflow-execution domain documentation and `docs/engineering/workflow-execution/evidence/WO-WEX-001-verification.md`.

No Git workflow, release orchestration, publication, external service, dependency, or provider-specific Skill change is expected.

## Implementation plan

1. Obtain accountable approval of `ARCH-WEX-001`, acceptance of `ADR-WEX-001`, and approval of this work order; run start preflight and read its complete manifest.
2. Add verifier-owned black-box fixtures for scope, transition packets, preparation, metadata timing, lifecycle independence, canonical handoffs, and every prohibited behavior.
3. Introduce the typed workflow plan/result boundary and declarative lifecycle/next-step registries behind existing parsing and validation.
4. Implement read-only focus and plan-only transition paths before adding the transaction writer.
5. Implement atomic apply, stale-state detection, rollback, and exhaustive boundary failure injection.
6. Route VREC/RLS preparation through the kernel and add the approved metadata/legacy behavior.
7. Add human/JSON renderers and thin public CLI adapters; confirm repository-wide Inspector behavior is unchanged.
8. Reconcile templates, managed files, help/reference documentation, public examples, and package data through supported processes.
9. Execute `VER-WEX-001`, retain evidence, update honest implementation statuses, run review preflight and inspection, and stop for separate candidate-commit authority.

## Required verification

- Every matrix row, acceptance scenario, invariant, static check, security check, resilience check, and manual assessment in `VER-WEX-001`.
- Focused candidate-source tests for CLI, scope, lifecycle, provenance, validation, writer failure, rendering, installation, upgrade, and integrity behavior.
- Black-box candidate-package acceptance through the separately identified released evaluator where applicable.
- `python -m se_harness validate .`
- `python -m unittest discover -s tests -p "test_*.py"`
- `python -m se_harness --help` and focused help for every changed command.
- `python -m se_harness doctor .`
- Start and review preflight for `WO-WEX-001` at the appropriate phases.
- Root/canonical template parity, package-data coverage, standard fresh installation, safe upgrade, schema-2 lock proof, and `git diff --check`.
- Explicit negative proof that no source, parser option, test expectation, template, documentation, or CI behavior implements rejected `REQ-WEX-006`.

## Evidence to record

Retain exact commands, runtimes, evaluator identities, test counts and durations, scenario and transition coverage, canonical JSON digests, human/JSON equivalence, before/after/rollback file-digest manifests, concurrent-change results, hostile path and content cases, preparation/decision metadata examples, lifecycle-plane independence, supported-agent adapter results, fresh-install and upgrade outputs, managed lock and parity results, validation and preflight outputs, changed paths, deviations, residual risks, manual assessments, and diff hygiene under `docs/engineering/workflow-execution/evidence/WO-WEX-001-verification.md`.

## Stop and escalate conditions

Stop if implementation requires changing a governed public command or schema beyond `SPEC-WEX-001`, implementing trusted-base/direct-edit enforcement, broadening scope traversal, weakening atomicity or authority separation, synchronizing related lifecycle states, migrating historical records, modifying Inspector semantics, adding a runtime dependency or installation profile, moving rules into a provider adapter, bypassing the released-evaluator boundary, building a distribution, or exercising any Git or external action. Stop for any unresolved rollback failure, incompatible legacy behavior, or architecture change not decided by `ADR-WEX-001`.

## Completion report format

Report `WO-WEX-001`, implemented requirements, current lifecycle state, exact public and managed surfaces changed, scope and transition behavior, verification results, evidence path, evaluator identity, deviations, residual risks, recommended next authorized step, required human authority, exact command or suggested response, valid alternatives, and every intentionally unperformed Git, assurance, release, Skill, trusted-base, and external action.
