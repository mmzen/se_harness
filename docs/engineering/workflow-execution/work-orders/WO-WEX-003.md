+++
id = "WO-WEX-003"
type = "work_order"
title = "Implement semantic-fidelity lifecycle handoffs"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[assurance]
commit_bound_verification = "required"
rationale = "The work changes managed cross-provider instructions and trusted presentation policy used for lifecycle, authority, and next-action handoffs; future engineering and release decisions will rely on the exact candidate state and its compatibility evidence."
decided_by = "repository-owner"

[execution_scope]
paths = [
  "templates/repository/standard/AGENTS.md.fragment",
  "templates/repository/standard/CLAUDE.md.fragment",
  "templates/repository/standard/ENGINEERING_HARNESS.md.tpl",
  "templates/repository/standard/docs/engineering/WORKFLOW.md",
  "tests/test_instruction_architecture.py",
  "tests/test_artifact_catalog.py",
  "tests/test_context_routing_retirement.py",
  "tests/test_public_onboarding.py",
  "tests/test_standard_repository_lifecycle.py",
  "tests/test_workflow_documentation_contract.py",
  "tests/test_workflow_restitution.py",
  "docs/notes/harness-overview.md",
  "docs/notes/harnessctl-reference.md",
  "docs/engineering/workflow-execution/evidence/WO-WEX-003-verification.md",
]

[relations]
implements = ["REQ-WEX-011"]
specifications = ["SPEC-WEX-003"]
architecture = ["ARCH-WEX-003", "ADR-WEX-003"]
verification = ["VER-WEX-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T17:31:43Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-24T17:33:06Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-24T18:22:51Z"
decided_by = "engineering-owner"
+++

# Work Order: Implement semantic-fidelity lifecycle handoffs

## Lifecycle

The governing packet and this work order were approved on 2026-08-24. The
released-evaluator start preflight passed, the engineering owner explicitly
instructed `WO-WEX-003` implementation to start, and the work order entered
`in_progress`.

During full-suite review, the implementation exposed two regression baselines
that directly cover the changed candidate router and managed `AGENTS.md`
fragment but were absent from the original execution scope. On 2026-08-24, the
engineering owner explicitly approved adding `tests/test_artifact_catalog.py`
and `tests/test_context_routing_retirement.py` to `[execution_scope].paths`.

This work order does not authorize a Git operation, completion decision,
assurance decision, release, publication, deployment, or external action.

Commit-bound verification is required because the exact candidate managed
policy and tests will be relied upon by later installations and lifecycle
decisions.

## Objective

Replace the ineffective requirement that models reproduce lifecycle
restitution byte for byte with a precise semantic-fidelity contract for agent
handoffs, while preserving schema-2 as the authority and keeping deterministic
direct rendering for exact consumers.

## In scope

- Replace verbatim-agent-output language in the candidate standard
  `ENGINEERING_HARNESS.md`, `WORKFLOW.md`, `AGENTS.md`, and `CLAUDE.md`
  templates with the two-path contract from `SPEC-WEX-003`.
- State that adaptive agent handoffs may change wording and structure but must
  preserve artifact IDs, outcome, observed effects, incomplete work, material
  non-effects, blockers, final state, accountable decision, one next action,
  and command/response semantics.
- State that exact format consumers must call the existing deterministic
  renderer directly without model transcription.
- Keep the current schema-2 restitution object, lifecycle computation,
  procedure selection, gate evaluation, direct renderer, and human heading
  order compatible.
- Update instruction-architecture and documentation-contract tests so they
  enforce the new responsibility boundary rather than the old verbatim phrase.
- Retain direct renderer exact tests and clearly label what those tests prove.
- Add positive and negative instruction fixtures or assertions needed by
  `VER-WEX-003` within the admitted test files.
- Update public overview and CLI reference language to distinguish canonical
  structured semantics, deterministic direct rendering, and adaptive agent
  presentation.
- Exercise fresh-install and standard repository lifecycle tests to prove the
  candidate distribution is internally consistent and the current managed root
  remains unchanged.
- Retain work-order-keyed verification evidence and stop at an uncommitted
  implementation candidate unless later authority is separately granted.

## Out of scope

- Changing `se-harness-workflow-result-v2`, restitution fields, field
  cardinality, `WORKFLOW.json`, quality-gate policy, lifecycle transitions,
  procedure ordering, decision rights, or scope classification.
- Removing or changing the deterministic `harnessctl` human renderer.
- Adding a prose parser, semantic-scoring model, provider SDK, network service,
  runtime dependency, persistent session, or telemetry.
- Creating provider-specific lifecycle rules or requiring identical natural
  language across Claude Code, Codex, ChatGPT, or other hosts.
- Editing approved historical WEX artifacts; this packet records the new rule
  while preserving their implementation history.
- Editing root managed `AGENTS.md`, `CLAUDE.md`, `ENGINEERING_HARNESS.md`,
  `WORKFLOW.md`, lock, configuration, or managed scripts directly. Candidate
  changes belong only in `templates/repository/standard/`.
- Releasing a distribution, upgrading this repository's installed harness, or
  claiming that candidate template changes are already active.
- Approval, start, work completion, commit, push, pull request, merge, VREC
  preparation or decision, release, tag, publication, deployment, credentials,
  or any other external action.

## Authorized decision envelope

The implementation agent may choose concise wording and section layout inside
the admitted candidate instruction and public-note files, and may choose test
helper decomposition inside the admitted test files. It may reuse existing
fixtures in those tests or add inline cases when no new path is needed.

The implementation agent may not change the semantic-fidelity matrix, material
non-effect rule, one-next-action constraint, exact-command boundary, direct
renderer behavior, schema or workflow contracts, authority boundary, managed
root, execution scope, or compatibility claims. Any discovered need for a new
runtime component, new file, schema change, provider-specific rule, or natural-
language evaluator requires a revised packet and accountable review.

## Constraints

- Treat schema-2 structured data as the only lifecycle presentation authority.
- Keep `harnessctl` as the only workflow legality and recommendation engine.
- Preserve exact argument arrays; displayed commands remain data, not shell
  expressions.
- Make candidate instruction language consistent across all four managed entry
  points without creating a second policy owner.
- Keep the router concise and route detailed procedure rules to
  `WORKFLOW.md`.
- Do not claim repository instructions can guarantee arbitrary external model
  output.
- Keep exact rendering deterministic, local, dependency-free, and model-free.
- Preserve owner-controlled repository content and unrelated user changes.
- Use the separately installed exact released evaluator for governed checks.

## Expected change surface

The authoritative maximum is `[execution_scope].paths`. Expected changes are
the four candidate managed instruction templates, focused instruction and
documentation tests, two public notes, and the retained verification evidence.

No Python runtime module, JSON contract, root managed file, formal artifact
outside this packet, CI workflow, package metadata, Skill core, release tool,
or external integration is expected to change.

## Required verification

- Every automated and manual obligation in `VER-WEX-003`.
- Focused instruction-architecture, workflow-documentation, restitution,
  onboarding, and standard-installation tests.
- The complete repository unit-test suite.
- Candidate-source `validate` and `doctor`, labeled separately from governing
  released-evaluator results.
- Released-evaluator identity, `doctor`, formal `validate`, start preflight,
  and review preflight for this work order at their eligible lifecycle stages.
- Candidate managed-template consistency, fresh-install behavior, package-data
  inclusion, distribution parity, and proof that root managed bytes remain
  unchanged.
- `git diff --check` and an exact changed-path comparison against
  `[execution_scope].paths`.
- Static proof that no network/model dependency, natural-language parser,
  schema change, renderer removal, root managed edit, or provider-specific
  workflow rule was introduced.
- Representative Claude Code and Codex handoff review for completed, blocked,
  and decision-required cases, explicitly labeled as supported-adapter evidence
  rather than universal host enforcement.

## Evidence to record

Retain exact evaluator identity and wheel digest, candidate identity when
available, commands, runtimes, test counts, exit status, direct-renderer
snapshots, adaptive positive and negative cases by semantic field, instruction
consistency findings, fresh-install and root-non-change results, dependency and
network-absence checks, changed paths, scope comparison, manual assessments,
deviations, and residual uncertainty in
`docs/engineering/workflow-execution/evidence/WO-WEX-003-verification.md`.

Also record that draft preparation, validation, and evidence do not approve,
start, implement, commit, verify, release, publish, deploy, or perform an
external action.

## Stop and escalate conditions

Stop before changing a path outside `[execution_scope]`; changing schema-2,
`WORKFLOW.json`, gates, procedures, lifecycle or authority semantics, direct
renderer behavior, or root managed files; adding a runtime component,
dependency, network/model call, prose parser, or provider-owned rule; weakening
material non-effect, blocker, decision, exact-command, or one-next-action
preservation; claiming enforcement for unsupported hosts; or performing any
lifecycle, Git, release, credential, or external operation.

Any such need requires a revised governing artifact and the corresponding
accountable approval before work continues.

## Completion report format

Report the outcome, `WO-WEX-003` state, exact changed paths, implemented
requirement, verification results, evidence path, evaluator identities,
deviations, residual uncertainty, and the non-effects relevant to approval,
Git, assurance, release, publication, deployment, and external action. Present
one accountable decision and exactly one recommended next action using the
semantic-fidelity contract; do not require the old verbatim heading block.
