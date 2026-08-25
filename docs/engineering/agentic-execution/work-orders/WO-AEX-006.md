+++
id = "WO-AEX-006"
type = "work_order"
title = "Implement the transactional change-bundle effect broker"
status = "approved"
owners = ["repository-owner", "engineering-owner", "technical-owner", "security-owner", "quality-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[assurance]
commit_bound_verification = "required"
rationale = "The work introduces the sole Phase 4 target-write boundary, public change-bundle and effect-receipt schemas, durable transaction recovery, and mutation-guard integration; assurance must bind the exact effect and recovery implementation commit."
decided_by = "repository-owner"

[execution_scope]
paths = [
  "MANIFEST.in",
  "pyproject.toml",
  "se_harness/agent_contract.py",
  "se_harness/agent_contract.json",
  "se_harness/change_bundle.py",
  "se_harness/effect_broker.py",
  "se_harness/effect_contract.json",
  "se_harness/mutation_guard.py",
  "se_harness/runtime_state.py",
  "tests/fixtures/agentic_execution/phase4/broker/",
  "tests/mutation_guard_support.py",
  "tests/test_agent_contract.py",
  "tests/test_change_bundle.py",
  "tests/test_effect_broker.py",
  "tests/test_mutation_guard.py",
  "docs/engineering/agentic-execution/README.md",
  "docs/engineering/agentic-execution/evidence/WO-AEX-006-verification.md",
  "docs/notes/agentic-execution-phase4-effects.md",
  "docs/notes/agentic-execution-roadmap.md",
  "docs/notes/README.md",
]

[relations]
implements = ["REQ-AEX-002", "REQ-AEX-004", "REQ-AEX-011"]
specifications = ["SPEC-AEX-001", "SPEC-AEX-003", "SPEC-AEX-006", "SPEC-AEX-007"]
architecture = ["ARCH-AEX-001", "ADR-AEX-001", "ADR-AEX-003", "ARCH-AEX-002", "ADR-AEX-006", "ADR-AEX-007"]
verification = ["VER-AEX-001", "VER-AEX-004"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T09:08:48Z"
decided_by = "engineering-owner"
+++

# Work Order: Implement the transactional change-bundle effect broker

## Lifecycle and readiness

This work order is `draft` and authorizes no implementation or effect.
`WO-AEX-005` must first be implemented, commit-bound verified, and accepted as
the exact dependency input. The accountable owners must separately approve all
new Phase 4 requirements, specifications, architecture, ADRs, verification,
and this work order, then separately start it through the existing released
evaluator.

The implementation must run under the existing command-driven evaluator. It
must not use candidate observer, envelope, broker, or workflow code to authorize
its own repository changes.

## Objective

Implement canonical change-bundle v1, evaluator-owned isolated session delta
construction, immutable content objects, the single-writer transactional target
effect broker, durable external journals and backups, deterministic rollback
and restart recovery, effect-receipt v1, and mandatory mutation-guard admission
defined by `SPEC-AEX-007`.

## In scope

- Add one authoritative packaged effect-contract catalog for bundle, journal-
  relevant portable values, and effect-receipt schemas.
- Implement duplicate-key-safe bounded parsing, canonical JSON encoding,
  canonical digesting, semantic validation, and reference vectors.
- Construct bundles only through the evaluator by comparing an evaluator-owned
  session baseline and proposed workspace plus explicit intended deletions.
- Materialize immutable digest-addressed regular-file objects in the external
  runtime session and revalidate them before apply.
- Register `change-bundle-apply` as a public mutation operation and require both
  released-evaluator mutation authority and current live envelope admission.
- Implement exclusive target locking, complete path/scope/deny-policy preflight,
  expected-before validation, temp replacement preparation, durable journal and
  recovery checksums, canonical apply order, result observation, receipt, and
  terminal journal state.
- Implement reverse-order ordinary rollback, restart recovery to proved prior
  or proved complete result, and explicit human-recovery stop on ambiguity.
- Exercise supported create/replace/delete, parent creation, content sharing,
  race/path/object attacks, permissions, disk faults, locked files, injected
  failures, process termination at each journal phase, and concurrent writers.
- Update bounded domain, design, roadmap, and evidence documentation.

## Out of scope

- Delegated lifecycle start/completion, VREC creation, decision packets, workflow
  contract changes, skill changes, adapters, or host activation.
- Editing hash-locked root managed files or the currently executing external
  evaluator payload.
- File modes, executable bits, directory delete, empty-directory preservation,
  links, junctions, reparse points, hard-link creation, special files,
  submodules, `.git`, or cross-repository effects.
- Direct target writes by the worker, provider-defined authority, multi-agent
  execution, child delegation, parallel writers, Git operations, credentials,
  network access, release, delivery, publication, deployment, or external
  action.
- Claiming whole-bundle instantaneous visibility or hardware durability beyond
  independently tested platform guarantees.
- Building or publishing a promotable release or running a real target pilot.

## Authorized decision envelope

After separate approval and start, the implementer may choose private module
internals, safe same-filesystem temp names, bounded buffer sizes, recovery-
material compression, backup retention within the closed policy, and fixture
subdivision inside the declared prefix.

The implementer may not change public bundle or receipt bytes, SHA-256, content
object addressing, operation set, size/entry bounds, canonical order, external
runtime boundary, target deny policy, preflight-before-write rule, nonce
consumption, journal terminal states, recovery proof, single-writer policy, or
declared paths. Escalate any such need.

## Constraints

- Preserve Python 3.11+ and standard-library-only runtime behavior.
- Depend on the exact verified `WO-AEX-005` live authority interfaces; do not
  add an alternate observer or admission path.
- Use regular files and normal directories only; follow no link or reparse
  point and prevent time-of-check/time-of-use path swaps.
- Use same-filesystem atomic single-path replacement where supported and fail
  closed where required containment or durability primitives are unavailable.
- Persist recovery material before the first target-path change and block all
  continuation on a nonterminal or corrupt journal.
- Do not execute proposed content or interpret bundle strings as commands,
  templates, URLs, credentials, or provider instructions.
- Preserve unrelated user changes and stop on any unexplained current-state
  difference or undeclared changed path.

## Expected change surface

`change_bundle.py` owns bundle construction, parsing, canonicalization, content
objects, and semantic validation. `effect_broker.py` owns preflight, locking,
journaling, target effects, validation, rollback, recovery, and receipts.
`runtime_state.py` extends the verified external session primitives without
changing authority semantics. `mutation_guard.py` recognizes the one new public
mutation operation.

If implementation requires workflow, CLI, provenance, installer, skill,
provider adapter, root managed policy, another target operation, or another
undeclared file, stop and revise scope.

## Required verification

- Execute every `VER-AEX-004` method applicable to `REQ-AEX-011`, plus relevant
  `VER-AEX-001` effect, authority, failure, and portability methods.
- Cross-check all public bytes and digests against an independent encoder.
- Prove bundles contain only deltas and the three governance foreign keys.
- Exhaust create/replace/delete invariants, order, duplicate keys and paths,
  entry/file/total bounds, object sharing, stale before state, missing/corrupt
  objects, current-state drift, and cross-context substitutions.
- Exercise traversal, case, Unicode, device, alternate stream/separator, URI,
  wildcard, link, junction, reparse, hard-link alias, submodule, special file,
  `.git`, managed deny, and external-runtime alias attacks.
- Inject failures at every preflight, journal, temp, replace, observation,
  receipt, rollback, and cleanup step. Kill the process after every durable
  journal transition and independently prove restart behavior.
- Prove direct target writes are detected and never converted into receipts.
- Prove exactly one writer can admit and no new operation continues with a
  nonterminal or corrupt journal.
- Run complete suite, distribution validation, non-promotable wheel acceptance,
  exact 0.6.0 evaluator doctor/formal validation, CLI help, phase preflight,
  `git diff --check`, and exact changed-path comparison.

## Evidence to record

Retain exact dependency and candidate commits; candidate package and external
0.6.0 evaluator identities; effect-contract vectors; bundle and object
inventories; platform filesystem capabilities; path, race, alias, permission,
disk, and lock matrices; every injected failure and journal transition; all
ordinary rollback and restart recovery proofs; receipt/live-state comparisons;
mutation-guard results; before/after repository and Git manifests; tests and
gates; changed paths; manual assessments; deviations; and residual uncertainty
at `docs/engineering/agentic-execution/evidence/WO-AEX-006-verification.md`.

## Stop and escalate conditions

Stop while this artifact is `draft` or while `WO-AEX-005` lacks verified exact-
commit evidence. After approval and start, stop before changing another path,
operation, schema, authority source, lifecycle surface, skill, root managed
file, Git state, credential, network, release, installation, or external target.

Stop if a supported platform cannot provide safe target containment or single-
path replacement, if ordinary failure cannot prove prior-state restoration, if
restart cannot reliably expose recovery-required state, if journal ambiguity is
silently resolved, or if any verification failure cannot be corrected inside
the exact scope.

## Completion report format

Report `Outcome`, `Done`, `Not done`, conditional `Blocked by`, `Current
lifecycle state`, `Decision required`, `Next`, `Command or response`, and
conditional `Alternatives`. Name `WO-AEX-006`, exact changed paths, bundle and
receipt schema IDs, operation/bound matrix, mutation guard, rollback/recovery
results, evaluator and dependency identities, evidence path, deviations,
residual uncertainty, and all intentionally unperformed lifecycle, skill, Git,
network, release, credential, and external actions. Recommend one next step.
