+++
id = "WO-AEX-005"
type = "work_order"
title = "Implement live observation and delegated authority derivation"
status = "in_progress"
owners = ["repository-owner", "engineering-owner", "technical-owner", "security-owner", "quality-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[assurance]
commit_bound_verification = "required"
rationale = "The work creates the state fingerprint and authority derivation used to admit future repository effects; verification must bind the exact observer, evaluator identity, delegation schema, nonce, expiry, and state-chain implementation bytes."
decided_by = "repository-owner"

[execution_scope]
paths = [
  "MANIFEST.in",
  "pyproject.toml",
  "se_harness/agent_contract.py",
  "se_harness/agent_contract.json",
  "se_harness/delegated_authority.py",
  "se_harness/repository_state.py",
  "se_harness/runtime_state.py",
  "templates/repository/standard/docs/engineering/templates/WORK_ORDER.template.md",
  "templates/repository/standard/scripts/validate_engineering_artifacts.py",
  "tests/fixtures/agentic_execution/phase4/authority/",
  "tests/test_agent_contract.py",
  "tests/test_agentic_execution.py",
  "tests/test_artifact_catalog.py",
  "tests/test_delegated_authority.py",
  "tests/test_repository_state.py",
  "docs/engineering/agentic-execution/README.md",
  "docs/engineering/agentic-execution/evidence/WO-AEX-005-verification.md",
  "docs/notes/agentic-execution-phase4-authority.md",
  "docs/notes/agentic-execution-roadmap.md",
  "docs/notes/README.md",
]

[relations]
implements = ["REQ-AEX-002", "REQ-AEX-004", "REQ-AEX-010"]
specifications = ["SPEC-AEX-001", "SPEC-AEX-003", "SPEC-AEX-006"]
architecture = ["ARCH-AEX-001", "ADR-AEX-001", "ADR-AEX-003", "ARCH-AEX-002", "ADR-AEX-006"]
verification = ["VER-AEX-001", "VER-AEX-004"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T09:08:48Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-25T09:09:21Z"
decided_by = "engineering-owner"
+++

# Work Order: Implement live observation and delegated authority derivation

## Lifecycle and readiness

This work order is `draft`. It authorizes no implementation, lifecycle
transition, package mutation, test claim, Git operation, network access,
credential use, release, installation, or external action.

Before approval, accountable owners must approve `REQ-AEX-010`,
`SPEC-AEX-006`, `ARCH-AEX-002`, `ADR-AEX-006`, `VER-AEX-004`, and this work
order through the exact existing released evaluator. Approval still does not
start work. A separate engineering-owner start decision and exact 0.6.0 start
checkpoint are required before any declared path changes.

Phase 4 capability does not exist while this work is performed. Candidate code
must not label its own observations stable, derive authority for its own work,
or govern its own repository changes.

## Objective

Implement the evaluator-owned live repository observer, formal maximum-
delegation schema, autonomy-envelope v2, external runtime nonce/session state,
least-authority derivation, fresh-state admission preparation, and verified-
receipt state-chain logic defined by `SPEC-AEX-006`. Keep the implementation
pure or read-only with respect to the target repository; target effects belong
to `WO-AEX-006`.

## In scope

- Add canonical observation and envelope-v2 definitions to the existing agent
  contract catalog while preserving every v1 canonical vector.
- Implement bounded read-only Git, worktree, formal, lock, evaluator, and
  filesystem observation with link/reparse and case-ambiguity detection.
- Implement stable two-observation comparison and a fresh-observation API for a
  later caller holding the exclusive effect lock.
- Add candidate work-order template and validator support for the optional exact
  `se-harness-agentic-delegation-v1` table.
- Implement maximum-delegation parsing, cross-checking against execution scope
  and managed right/operation/profile catalogs, and fail-closed narrowing.
- Implement short-lived autonomy-envelope v2 derivation with unique nonce,
  expiry, evaluator binding, current-state binding, and optional previous-
  receipt link.
- Implement restricted external runtime-state primitives for target-session
  identity, exclusive ownership, nonce admission, revocation, terminal outcome,
  and recovery-required blocking. This work does not invoke an effect.
- Implement receipt-to-next-state validation using existing receipt semantics
  and the new live observation digest.
- Add reference vectors, property cases, adversarial repository fixtures,
  evaluator substitution, clocks, nonces, races, and Windows/POSIX path cases.
- Update bounded architecture notes, domain index, roadmap, and commit-bound
  work-order evidence.

## Out of scope

- Applying, replacing, creating, or deleting a target repository path.
- Change-bundle construction, content object stores, transaction journals,
  backups, rollback, recovery execution, or effect receipts.
- Lifecycle transitions, VREC creation, decision-right activation, workflow
  contract changes, skill changes, provider adapter changes, or host testing.
- Editing hash-locked root managed templates, workflow, decision-right, gate,
  traceability, instruction, lock, validator, or released evaluator files.
- Direct worker target writes, provider permission enforcement, multi-agent
  work, child delegation, parallel writers, Git mutation, credentials, network,
  release, delivery, publication, deployment, or external action.
- Building or publishing a promotable distribution or upgrading a real target.

## Authorized decision envelope

After separate approval and start, the implementer may choose private Python
type and helper names, bounded caching that cannot change results, fixture
subdivision within the declared prefix, stable diagnostic wording behind
closed codes, and a cryptographically secure standard-library nonce primitive.

The implementer may not change public schema IDs or fields, canonical encoding,
observation coverage, five-minute maximum expiry, clean-start rule, delegation
meaning, mandatory stops, single-writer limit, evaluator identity source,
receipt continuity, runtime-directory boundary, or any declared path. Such a
need requires revised approved artifacts and work order.

## Constraints

- Preserve Python 3.11+ and standard-library-only runtime behavior.
- Preserve all v1 accepted bytes, canonical digests, diagnostics, and pure no-
  effect behavior.
- Invoke Git only through bounded argument vectors with no shell and no Git
  mutation command.
- Stream repository content; enforce existing artifact, entry, file, document,
  and collection bounds before unbounded work.
- Follow no links or reparse points and expose no absolute user path, secret,
  environment dump, or hidden reasoning.
- Store runtime state outside the target checkout under an explicitly supplied,
  verified, access-restricted directory.
- Make candidate APIs incapable of proving their own released identity.
- Preserve unrelated user changes and stop on an undeclared changed path.

## Expected change surface

`repository_state.py` owns observation and stable-pair logic.
`delegated_authority.py` owns formal delegation resolution, narrowing, envelope
v2 derivation, expiry, and receipt-chain input. `runtime_state.py` owns bounded
external session and nonce primitives without target effects. The existing
agent catalog gains the versioned public definitions and reference encoding.

The standard candidate work-order template and candidate artifact validator add
the optional delegation table. Root managed copies remain unchanged until a
future released upgrade. If another package, template, validator, CLI,
workflow, test, or documentation path is required, stop and revise scope.

## Scope amendment, 2026-08-25

Accepted on 2026-08-25 through the explicit governed amendment requested
during implementation. `tests/test_artifact_catalog.py` is added to
`[execution_scope]` for one purpose only: replace the obsolete assertion that
the released and candidate work-order templates are byte-identical with an
exhaustive assertion that the candidate equals the released template plus the
one exact optional `agentic_delegation` block and its exact guidance paragraph
required by this work order.

The amendment authorizes that compatibility assertion and nothing else. The
released root template remains unchanged, parity for the traceability copies
remains exact, and no skip, suppression, wildcard exception, or relaxation of
the candidate-template check is authorized.

## Required verification

- Execute all `VER-AEX-004` methods applicable to `REQ-AEX-010` and all
  `VER-AEX-001` authority/state methods implicated by the changed catalog.
- Prove exact v1 byte and behavior compatibility before evaluating v2 vectors.
- Cross-check implementation observation bytes against an independent reference
  encoder on supported Windows and POSIX fixtures.
- Exercise two-pass races, fresh-state races, unmerged index, submodules, links,
  reparse points, case collisions, ignored/untracked inputs, over-bound trees,
  evaluator substitutions, formal and lock drift, and Git failures.
- Exhaust delegation intersections, missing fields, unknown rights/operations,
  path mismatch, wrong delegate/profile, stop removal, expiry, revocation,
  retries, writer counts, nonce reuse, session collision, and receipt gaps.
- Prove all functions before the broker boundary have zero target repository,
  Git, lifecycle, credential, network, and external effects.
- Run the complete repository suite, candidate distribution validation,
  non-promotable wheel acceptance if needed, exact 0.6.0 doctor and formal
  validation, CLI help, phase preflight, `git diff --check`, and exact changed-
  path comparison.

## Evidence to record

Retain exact source candidate and commit; 0.6.0 external evaluator identity;
candidate package when used; platform, filesystem, Git, clock, and nonce test
identities; all v1/v2 vectors; observation reference comparisons; delegation
matrices; race, path, object, expiry, revocation, replay, and state-chain results;
runtime-state permission and corruption tests; before/after repository and Git
manifests; test and gate outputs; changed paths; manual assessments; deviations;
and residual uncertainty at
`docs/engineering/agentic-execution/evidence/WO-AEX-005-verification.md`.

## Stop and escalate conditions

Stop while this artifact is `draft`. After approval and start, stop before any
target effect, lifecycle change, skill change, workflow activation, root managed
file change, undeclared path, schema relaxation, provider-specific permission,
Git mutation, credential use, network access, package release, install, or
external action.

Stop if live observation cannot be deterministic and bounded on a supported
platform, if current evaluator identity cannot be proven without candidate
trust, if runtime state cannot be kept outside the target, if v1 compatibility
breaks, or if any required verification fails outside the exact correction
scope.

## Completion report format

Report `Outcome`, `Done`, `Not done`, conditional `Blocked by`, `Current
lifecycle state`, `Decision required`, `Next`, `Command or response`, and
conditional `Alternatives`. Name `WO-AEX-005`, exact changed paths, schema and
catalog IDs, observation and delegation matrices, evaluator identity, evidence
path, deviations, residual uncertainty, and intentionally unperformed effect,
lifecycle, skill, Git, network, release, credential, and external actions.
Recommend exactly one next authorized step.
