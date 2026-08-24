+++
id = "WO-AEX-001"
type = "work_order"
title = "Implement the read-only harness-orient pilot"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[assurance]
commit_bound_verification = "required"
rationale = "The pilot changes trusted packaged skill, installer, managed-template, package-data, and distribution surfaces; future orientation and decision-point guidance will rely on the exact resulting candidate."
decided_by = "repository-owner"

[execution_scope]
paths = [
  "MANIFEST.in",
  "README.md",
  "pyproject.toml",
  "se_harness/installer.py",
  "se_harness/skill_contract.py",
  "templates/repository/standard/.agents/skills/harness-orient/",
  "tests/fixtures/agentic_execution/",
  "tests/test_agentic_execution.py",
  "tests/test_instruction_architecture.py",
  "tests/test_public_onboarding.py",
  "tests/test_release_build.py",
  "tests/test_standard_repository_lifecycle.py",
  "docs/notes/harness-orient.md",
  "docs/notes/harness-installation-and-upgrades.md",
  "docs/notes/README.md",
  "docs/engineering/agentic-execution/evidence/WO-AEX-001-verification.md",
]

[relations]
implements = ["REQ-AEX-006"]
specifications = ["SPEC-AEX-001", "SPEC-AEX-002"]
architecture = ["ARCH-AEX-001", "ADR-AEX-001", "ADR-AEX-002"]
verification = ["VER-AEX-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T09:03:54Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-24T09:11:31Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-24T09:46:24Z"
decided_by = "engineering-owner"
+++

# Work Order: Implement the read-only harness-orient pilot

## Lifecycle and authorization

The repository owner confirmed commit-bound verification as `required` during
accountable content review. Formal implementation authority is determined by
the front-matter lifecycle state, not by that review record alone. While this
work order is `draft`, no implementation, lifecycle transition, commit,
verification record, release preparation, publication, installation outside a
disposable fixture, or external action is authorized.

Before work starts, the accountable owners must approve the requirement,
specification, architecture, applicable ADR decisions, verification contract,
and this work order through the managed lifecycle procedure. The exact released
evaluator required by the target repository must then pass start preflight.

## Objective

Implement and distribute one portable, read-only `harness-orient` skill that
turns repository orientation into an outcome-oriented agent procedure. It must
inspect integrity and formal state through public harness interfaces, clearly
separate the exact released evaluator from candidate code, return a concise
decision-ready result, and prove that it changed no repository, Git, lifecycle,
environment, or external state.

This is the single-agent reference implementation for later skills. It does not
implement autonomous mutation, subagent orchestration, or runtime adapters.

## In scope

- Define the approved portable `harness-orient` package with `SKILL.md`, its
  machine-readable skill contract, and only the supporting references or
  standard-library scripts needed for deterministic execution.
- Use the single canonical source
  `templates/repository/standard/.agents/skills/harness-orient/` and managed
  installed location `.agents/skills/harness-orient/`; do not create a second
  copy under `se_harness/skills/`.
- Implement strict `se-harness-skill-contract-v1` parsing and the
  `se-harness-skill-manifest-v1` `utf8-text-lf-v1` digest in
  `se_harness/skill_contract.py` without creating a second workflow engine.
- Define narrow activation boundaries: explicit invocation and unambiguous
  repository-orientation requests, with negative examples that prevent the
  skill from matching implementation, approval, release, or external-action
  requests.
- Use the target repository's exact released evaluator for managed integrity
  and governing formal-state checks. Label candidate-source observations
  separately and never substitute them as governing results.
- Support exact released evaluator 0.5.0 and later compatible versions through
  the approved capability matrix: version, identity, doctor, validation JSON,
  and inspection JSON are required; focus JSON and explicitly requested
  preflight are optional and degrade only their named output.
- Produce the orientation and execution-receipt semantics defined by
  `SPEC-AEX-001` and `SPEC-AEX-002`, including lifecycle state, scoped blockers
  when supported, separately counted background observations, the next
  accountable decision point, accountable role, one recommended next step,
  exact command or suggested response, and an inline canonical receipt that
  writes nothing to the target.
- Preserve a complete deterministic single-agent path without runtime-specific
  model, tool, permission, hook, connector, memory, or subagent configuration.
- Add the skill to the canonical standard-repository distribution surface and
  update explicit package data and, only where the existing generic behavior is
  insufficient, installer logic. Managed integrity and safe-upgrade behavior
  must add exact prior managed content and block customized or ambiguous target
  content transactionally.
- Add verifier-owned fixtures and black-box tests for valid, invalid, missing-
  evaluator, version-skew, hostile-content, read-only-filesystem, fresh-install,
  upgrade, rollback, and no-write cases.
- Document the supported invocation, returned fields, authority limitations,
  exact-evaluator prerequisite, fallback behavior, and troubleshooting path.
- Retain independent verification evidence at the declared evidence path.
- Build only a clearly labeled, non-promotable ephemeral wheel outside the
  checkout when required to verify packaged skill data and fresh installation.

## Out of scope

- Implementing or applying an autonomy envelope, mutation authority, or any
  predelegated lifecycle decision.
- Adding implementation, verification, architecture, release, risk, deployment,
  credential, or other mutating skills.
- Spawning or coordinating subagents, parallel readers, parallel writers,
  worktrees, worker profiles, or an integration coordinator.
- Generating or modifying Codex, Claude, ChatGPT, IDE, CI, hosted-agent, or other
  provider-specific runtime adapters or defaults.
- Changing existing lifecycle states, decision rights, quality gates, workflow
  procedures, mutation rules, formal graph semantics, or accountable roles.
- Inferring authority from skill activation, agent/profile names, model choice,
  sandbox state, tool access, or operating-system permissions.
- Installing a missing evaluator into the user's environment, accessing the
  network, using credentials, modifying Git, or affecting any external system.
- Creating a verification record, release record, commit, tag, branch, pull
  request, promotable package distribution, publication, deployment, or managed
  root-file refresh.

## Authorized decision envelope

After accountable approval and successful start preflight, the implementation
agent may choose private function and diagnostic names inside
`se_harness/skill_contract.py`, exact fixture layout within the declared paths,
bounded receipt-rendering details already fixed by approved semantics, and
concise reference-document structure. It may add no dependency outside the
Python standard library and no second skill runtime or policy engine.

The agent may not change the portable schema or public result semantics; add an
operation, path, permission, decision class, or side effect; make the skill
authoritative; widen activation; persist runtime-specific configuration; or
resolve an explicitly unspecified architecture decision informally. If an
approved contract cannot be implemented inside this envelope, work stops for a
revised artifact and accountable decision.

## Constraints

- Preserve Python 3.11+ standard-library runtime behavior and one standard
  installation path.
- Treat the target repository, skill content, paths, command output, evaluator
  metadata, and model-generated text as untrusted input.
- Preserve candidate-source, candidate-package, installed-harness, and exact
  released-evaluator identity as distinct labeled observations.
- Use structured command arguments; do not evaluate repository or skill text as
  shell syntax.
- Run without network access or credentials and remain correct when the
  filesystem is read-only.
- Keep the standard repository template canonical. Do not directly overwrite
  root managed files or bypass managed upgrade behavior.
- Preserve owner-controlled files and report customization conflict rather than
  silently replacing content.
- Preserve unrelated user changes and historical formal records.
- Do not build or publish a promotable distribution under this work order. A
  non-promotable ephemeral wheel may be built outside the checkout only for the
  declared package-data and fresh-install evidence.

## Expected change surface

The exact authorized paths are declared in `[execution_scope]`. They cover one
portable skill source, one standard-library contract and digest module, the
existing generic installer if needed, package metadata, user-facing orientation
and upgrade documentation, focused installation and distribution tests, and
retained verification evidence. No new CLI command, Python skill runtime,
provider adapter, workflow contract, managed policy file, or root managed copy
is authorized.

## Implementation plan

1. Approve or revise the requirement, specification, architecture assessment,
   ADRs, verification contract, assurance classification, and work order.
2. Run exact released-evaluator identity, integrity, validation, inspection, and
   start preflight for the approved work order; record the identities and stop
   on any blocker. Use focus only when that exact evaluator supports it.
3. Build verifier-owned black-box fixtures and pre/post state manifests before
   implementing the portable skill.
4. Implement strict skill-contract parsing and canonical portable-core identity
   in `se_harness/skill_contract.py`, with stable diagnostics and no duplicate
   workflow, runtime-specific rule, or binary pilot asset.
5. Implement `harness-orient` as a thin procedure over supported public harness
   results, including explicit capability degradation and single-agent fallback.
6. Integrate the canonical standard-repository skill directory, explicit
   package data, managed integrity, and ownership-aware upgrade behavior
   transactionally. Change existing installer code only when required by a
   failing verifier-owned case.
7. Add negative activation, hostile-input, no-write, exact-evaluator,
   fresh-install, upgrade, rollback, help, documentation, and compatibility
   tests.
8. Execute the applicable `VER-AEX-001` matrix and complete repository checks;
   retain evidence against the exact candidate and stop for independent
   verification and separate commit authority.

## Required verification

- Every `VER-AEX-001` method applicable to `REQ-AEX-006`, plus negative proof
  that this work order implements none of the deferred mutation,
  multi-agent, or adapter behavior.
- Black-box semantic comparison between direct public harness commands and the
  portable skill result on the same verifier-owned repositories.
- Byte and Git-reference manifests proving valid and failed orientation runs
  are read-only, including missing evaluator and read-only filesystem cases.
- Candidate-source focused tests and the complete repository test suite.
- Candidate-source help, validation, doctor, integrity, package-data,
  installation, upgrade, rollback, and distribution-parity checks, labeled as
  candidate evidence.
- Separately identified exact released-evaluator identity, doctor, validation,
  inspection, and review preflight supported by that version; for 0.5.0, prove
  that unavailable focus yields only the specified degraded selected-scope
  result.
- Canonical skill-manifest vectors covering ordering, LF/CRLF/CR equivalence,
  changed bytes, missing required files, unknown contract fields, invalid
  UTF-8, symlinks, traversal, case collision, and runtime-overlay exclusion.
- Fresh installation and safe upgrade into disposable repositories, including
  customized owner content and managed-file conflict cases.
- One non-promotable ephemeral-wheel inspection and fresh installation proving
  the canonical skill files occur exactly once in package data and at the
  installed target.
- Hostile path, content, argument, encoding, schema, symlink/junction, output,
  secret-exclusion, interruption, and deterministic-order cases.
- `git diff --check` and an exact changed-path manifest proving every changed
  path is admitted by `[execution_scope]`.

## Evidence to record

Retain exact commands, exit codes, runtimes, released-evaluator and candidate
identities, formal snapshot and skill-package digests, fixture and expected-
result manifests, pre/post repository and Git digests, skill manifest and
canonical receipt vectors, semantic output comparisons, activation and
non-match cases, the complete 0.5.0 capability matrix, hostile-input results,
read-only and interruption results, test counts and duration, fresh-install and
upgrade observations, ephemeral-wheel inventory and hash, package/managed
parity, changed paths, deviations, manual assessments, and residual risks under
`docs/engineering/agentic-execution/evidence/WO-AEX-001-verification.md`.

## Stop and escalate conditions

Stop before changing a path outside `[execution_scope]`; selecting a different
canonical skill location or adding a duplicate skill copy; changing a public
schema, workflow rule, gate,
decision right, authority boundary, or compatibility promise; adding a
dependency, network access, credential, mutation, subagent, worker profile,
runtime adapter, hosted service, or dynamic evaluator; using candidate source
as the governor; weakening no-write, integrity, path, rollback, or owner-content
guarantees; modifying root managed files directly; building a promotable
distribution or retaining an ephemeral wheel as a release candidate;
performing Git or external actions; or encountering a verification failure that
cannot be corrected inside the approved contracts. Any such need requires a
revised artifact and accountable approval.

## Completion report format

Report `Outcome`, `Done`, `Not done`, conditional `Blocked by`, `Current
lifecycle state`, `Decision required`, `Next`, `Command or response`, and
conditional `Alternatives`. Name `WO-AEX-001`, exact changed paths, implemented
requirement, skill and evaluator identities, verification results, evidence
path, deviations, residual uncertainty, and intentionally unperformed
mutation, subagent, adapter, Git, assurance, release, network, credential, and
external actions. Recommend exactly one next authorized step.
