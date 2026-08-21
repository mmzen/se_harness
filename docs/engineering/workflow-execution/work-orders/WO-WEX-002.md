+++
id = "WO-WEX-002"
type = "work_order"
title = "Implement scoped workflow compliance and restitution"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "quality-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[assurance]
commit_bound_verification = "required"
rationale = "The work changes executable workflow scope, gate evaluation, procedure resolution, public CLI and JSON contracts, managed policy and templates, and agent-facing restitution; future engineering, assurance, and release decisions rely on the correctness of the exact resulting trusted state."
decided_by = "repository-owner"

[execution_scope]
paths = [
  "MANIFEST.in",
  "README.md",
  "pyproject.toml",
  "se_harness/cli.py",
  "se_harness/installer.py",
  "se_harness/preflight.py",
  "se_harness/provenance.py",
  "se_harness/quality_gates_contract.json",
  "se_harness/workflow.py",
  "se_harness/workflow_compliance.py",
  "se_harness/workflow_contract.json",
  "se_harness/workflow_contract.py",
  "se_harness/workflow_procedures.py",
  "se_harness/workflow_result.py",
  "templates/repository/standard/AGENTS.md.fragment",
  "templates/repository/standard/CLAUDE.md.fragment",
  "templates/repository/standard/ENGINEERING_HARNESS.md.tpl",
  "templates/repository/standard/docs/engineering/QUALITY_GATES.json",
  "templates/repository/standard/docs/engineering/QUALITY_GATES.md",
  "templates/repository/standard/docs/engineering/README.md.seed",
  "templates/repository/standard/docs/engineering/REPOSITORY_CONTEXT.md.seed",
  "templates/repository/standard/docs/engineering/WORKFLOW.json",
  "templates/repository/standard/docs/engineering/WORKFLOW.md",
  "templates/repository/standard/docs/engineering/templates/WORK_ORDER.template.md",
  "templates/repository/standard/scripts/inspect_engineering_artifacts.py",
  "templates/repository/standard/scripts/validate_engineering_artifacts.py",
  "tests/fixtures/workflow_execution/",
  "tests/test_artifact_authoring.py",
  "tests/test_artifact_catalog.py",
  "tests/test_harnessctl.py",
  "tests/test_inspection.py",
  "tests/test_instruction_architecture.py",
  "tests/test_public_onboarding.py",
  "tests/test_standard_repository_lifecycle.py",
  "tests/test_validation_taxonomy.py",
  "tests/test_workflow_compliance.py",
  "tests/test_workflow_documentation_contract.py",
  "tests/test_workflow_execution.py",
  "tests/test_workflow_procedures.py",
  "tests/test_workflow_restitution.py",
  "docs/notes/harness-overview.md",
  "docs/notes/harnessctl-reference.md",
  "docs/engineering/workflow-execution/evidence/WO-WEX-002-verification.md",
]

[relations]
implements = ["REQ-WEX-007", "REQ-WEX-008", "REQ-WEX-009", "REQ-WEX-010"]
specifications = ["SPEC-WEX-002"]
architecture = ["ARCH-WEX-002", "ADR-WEX-002"]
verification = ["VER-WEX-002"]
+++

# Work Order: Implement scoped workflow compliance and restitution

## Lifecycle and authorization

REQ-WEX-007 through REQ-WEX-010, SPEC-WEX-002, and VER-WEX-002 are
approved. The technical owner accepted ADR-WEX-002 and approved ARCH-WEX-002.
The engineering owner explicitly approved this work order for implementation on
2026-08-21. The released-evaluator start preflight passed and the engineering
owner separately instructed the selected work to start on 2026-08-21. The work
order entered progress. On 2026-08-21, the engineering owner approved adding
`tests/test_artifact_catalog.py` to the execution scope so its candidate/released
template-isolation assertion could advance with the new work-order template.
The complete suite, selected implementation handoff gate, and isolated released
0.5.0 review preflight then passed. Under the approved instruction to implement
this work order, `WO-WEX-002` is now implemented and remains uncommitted.

Commit-bound verification is `required`. The work order does not authorize a
commit, push, pull request, VREC decision, release, tag, publication, deployment,
or operation.


## Objective

Make selected workflow execution and iteration closure repeatable across
supported agents by implementing the stateless scope, compliance, typed
procedure, and canonical restitution contracts in SPEC-WEX-002, while preserving
the transactional lifecycle behavior of SPEC-WEX-001 and the rejection of
trusted-base enforcement.

## In scope

- Add schema-v2 workflow policy with a typed `PROC-*` registry, step kinds,
  parameter contracts, canonical argument arrays, decision stops, fixed context
  actions, effects, non-effects, and declared alternatives.
- Add `QUALITY_GATES.json` and a packaged runtime copy containing exact gates,
  `QGP-*` predicates, checkpoints, evidence requirements, and closed evaluator
  keys.
- Add conformance checks that bind workflow/gate JSON, Markdown policy,
  repository-context action markers, package data, and runtime-loaded contracts.
- Add work-order `[execution_scope]` validation using normalized exact-file and
  component-boundary directory-prefix matching.
- Add `se-harness-change-set-v1` parsing, repeated changed-path input, explicit
  completeness assertions, and honest `not_assessable` behavior when completeness
  is absent.
- Add one stateless checkpoint service for start, pre-action, transition, and
  handoff evaluation with the fixed repository-integrity blocker taxonomy.
- Add a closed local predicate-evaluator registry, snapshot-bound evidence
  freshness, complete tri-state predicate reporting, and
  `fail > not_assessable > pass` aggregation.
- Add the read-only public `harnessctl check` command and integrate the same
  checkpoint service with transition planning/apply and VREC/RLS preparation.
- Add `se-harness-workflow-result-v2`, exact human restitution headings,
  honest done/not-done/blocker fields, one primary next step, exact
  command/response, and schema-1 compatibility for existing commands.
- Label `inspect` explicitly as repository-wide and prevent its output from
  serving as selected restitution without changing its maintenance purpose.
- Update managed policy, work-order template, context action markers, agent
  entry fragments, public help/reference documentation, package data, and
  standard installation behavior.
- Add verifier-owned black-box fixtures, focused unit tests, hostile-input and
  boundary tests, adapter-parity tests, performance cases, and failure injection
  required by VER-WEX-002.
- Retain complete work-order-keyed evidence and stop at an uncommitted
  `implemented` candidate unless later authority is granted.

## Out of scope

- REQ-WEX-006, trusted-base resolution, Git-diff lifecycle validation, hidden
  changed-path detection, direct-edit interception, or CI transition-history
  enforcement.
- A persistent workflow session, journal, database, daemon, lock service, hosted
  coordinator, network API, telemetry, or new runtime dependency.
- A provider-specific ChatGPT, Claude, or Codex Skill or plugin; supported entry
  fragments remain thin adapters to canonical CLI output.
- Authentication or proof that an actor holds a role; automatic approval,
  verification, release, risk acceptance, or external action.
- Shell command execution from policy, dynamic evaluator imports, expression
  evaluation, or executable repository-context content.
- Automatic scope expansion when an undeclared path, artifact, finding, or
  procedure need is discovered.
- Direct modification of the root managed 0.5.0 installation; candidate managed
  changes belong in `templates/repository/standard/` until a later released
  upgrade applies them.
- Migration or rewriting of completed historical work orders or other
  repository-owned artifacts solely to add execution scope or schema-2 output.
- Commit, push, pull-request creation, merge, VREC verification, release
  authorization, tag, publication, deployment, or operation.
- Version change, promotable distribution build, governor activation, or release
  preparation.

## Authorized decision envelope

Implementation may choose internal class/function decomposition within the
explicitly listed Python files, immutable model representation, in-memory index
and cache structures, verifier fixture layout, private helper APIs, terminal
wrapping, and whether bound Markdown is generated or conformance-compared. A
listed anticipated new file may remain absent when its responsibility is kept in
another listed component.

Implementation may not add or modify a path outside `[execution_scope]`, change
the public command or schema contracts, alter path grammar, blocker taxonomy,
gate aggregation, evidence freshness, procedure limits, restitution fields or
order, compatibility window, authority boundary, or error-code meanings without
a revised governing artifact and explicit approval. It may not move rules into
an adapter, renderer, dashboard, or repository note.

## Constraints

- Preserve one standard installation and Python 3.11+ standard-library runtime.
- Treat policy, paths, manifests, evidence, context markers, procedure values,
  actor text, repository content, and terminal output as untrusted.
- Parse procedure commands as argument arrays and evaluator names through one
  closed registry; never use shell or dynamic evaluation.
- Build one formal index per checkpoint and keep repeated evaluation bounded by
  the performance contract in SPEC-WEX-002.
- Preserve existing plan/apply, proposed-final-graph, stale-input, atomic-write,
  rollback, VREC/RLS provenance, and lifecycle-plane independence guarantees.
- Keep selected and repository-wide modes disjoint and suppress unrelated
  details before restitution rendering.
- Treat caller completeness as an assertion, never proof; missing completeness
  is `not_assessable`.
- Keep human and JSON forms dependent on one semantic result and keep supported
  adapters byte-equivalent to canonical restitution.
- Keep the released governing evaluator outside the checkout; label candidate
  source, package, and released-evaluator evidence separately.
- Preserve owner content and do not build a promotable distribution.

## Expected change surface

The `[execution_scope]` metadata is the authoritative maximum path set. The
expected components are:

- CLI dispatch, workflow kernel, checkpoint service, procedure resolver, gate
  evaluators, schema-2 result, provenance integration, preflight, installer, and
  package-data declarations.
- Runtime and standard-installation workflow/gate JSON plus bound human policy,
  router, context, agent fragments, work-order template, validator, and
  inspection script.
- Focused workflow, procedure, restitution, validation, installation,
  inspection, onboarding, compatibility, security, performance, and public CLI
  tests and fixtures.
- Public overview/reference documentation and
  `docs/engineering/workflow-execution/evidence/WO-WEX-002-verification.md`.

No other Python package, test, formal domain, root managed file, CI workflow,
release tool, or external integration is expected to change.

## Implementation plan

1. Obtain engineering-owner approval and an explicit start instruction; run the
   released evaluator's start preflight and read its complete manifest.
2. Add verifier-owned schema-2, scope, gate, procedure, restitution, and adapter
   fixtures before production behavior.
3. Introduce versioned workflow-v2 and quality-gate contracts plus strict
   conformance validation, closed IDs, limits, and packaged/template parity.
4. Implement execution-scope and change-set codecs with hostile-path cases and
   honest completeness reporting.
5. Implement evidence freshness, predicate evaluators, tri-state aggregation,
   and the stateless checkpoint service.
6. Implement typed procedure resolution for every workflow rule, including
   exact commands, context actions, alternatives, and decision stops.
7. Add `harnessctl check`; route transition and preparation checkpoints through
   the same service without weakening existing transaction controls.
8. Add schema-2 JSON and canonical human restitution; preserve schema-1
   compatibility and label Inspector output repository-wide.
9. Reconcile managed candidate templates, work-order authoring, package data,
   public help/reference documentation, entry fragments, and fresh-install and
   upgrade behavior.
10. Execute VER-WEX-002 and the complete repository suite, retain exact evidence,
    run released-evaluator review preflight, and stop for separate commit
    authority.

## Required verification

- Every matrix row, acceptance scenario, invariant, static check, security
  check, resilience check, manual assessment, and retained-evidence obligation
  in VER-WEX-002.
- Focused candidate-source tests for scope/change manifests, gates/evidence,
  procedures, restitution, CLI, transition/preparation integration, inspection,
  preflight, installation, package data, validation, and compatibility.
- `python -m unittest discover -s tests -p "test_*.py"`.
- `python -m se_harness --help` and focused help for every changed command.
- Candidate-source validation and doctor results, labeled as candidate evidence
  rather than governing evaluation.
- Separately identified released-evaluator `identity`, `validate`, `doctor`, and
  start/review preflight for WO-WEX-002.
- Runtime/template JSON identity, Markdown-policy conformance, managed lock,
  package-data, fresh-install, safe-upgrade, root/candidate separation, and
  `git diff --check`.
- Exact permitted-path manifest showing every changed path is admitted by
  `[execution_scope]` and no selected restitution contains unrelated finding
  details.
- Explicit negative proof that no source, help, test, template, interface, or CI
  behavior implements REQ-WEX-006, persistent sessions, provider-owned rules,
  shell evaluation, or external action.

## Evidence to record

Retain exact commands, runtimes, evaluator identities, test counts and duration,
scope and change-set fixtures, blocker taxonomy coverage, gate/predicate and
evidence-freshness matrices, procedure graph/parameter/decision coverage,
canonical JSON and human digests, supported-agent adapter parity, pre/post/failure
repository digests, hostile path/policy/content cases, performance results,
schema-1 compatibility, inspection isolation, transition/preparation no-partial
writes, managed/package parity, fresh-install and upgrade results, validation,
doctor and preflight outputs, changed paths, deviations, manual assessments, and
residual risks under
`docs/engineering/workflow-execution/evidence/WO-WEX-002-verification.md`.

## Stop and escalate conditions

Stop before changing a path outside `[execution_scope]`; broadening scope,
procedure behavior, gate semantics, public schemas, compatibility, or the
repository-integrity blocker taxonomy; adding a session, service, dependency,
dynamic evaluator, shell execution, hidden-change claim, or provider-owned rule;
modifying the released root installation directly; weakening selected-scope
filtering, decision stops, existing transactional guarantees, or authority
separation; implementing REQ-WEX-006; encountering an unprovable rollback or
unsupported compatibility break; building a distribution; or performing any Git
or external action. Any such need requires a revised artifact and accountable
approval.

## Completion report format

Emit the schema-2 canonical headings in order: `Outcome`, `Done`, `Not done`,
conditional `Blocked by`, `Current lifecycle state`, `Decision required`,
`Next`, `Command or response`, and conditional `Alternatives`. Report
WO-WEX-002, exact changed paths, implemented requirements, gate and verification
results, evidence path, released/candidate evaluator identities, deviations,
residual uncertainty, and intentionally unperformed Git, assurance, release,
Skill, trusted-base, session, and external actions. Recommend exactly one next
authorized step.
