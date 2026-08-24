+++
id = "WO-AEX-002"
type = "work_order"
title = "Implement runtime-neutral AEX core contract validation"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "technical-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[assurance]
commit_bound_verification = "required"
rationale = "The work will add trusted executable validation, canonical encoding, scope-narrowing, decision-packet, receipt, and portable-profile behavior that later skills and mutation controls will rely on."
decided_by = "repository-owner"

[execution_scope]
paths = [
  "MANIFEST.in",
  "pyproject.toml",
  "se_harness/agent_contract.json",
  "se_harness/agent_contract.py",
  "se_harness/skill_contract.py",
  "tests/fixtures/agentic_execution/contracts/",
  "tests/test_agent_contract.py",
  "tests/test_agentic_execution.py",
  "tests/test_release_build.py",
  "docs/engineering/agentic-execution/README.md",
  "docs/engineering/agentic-execution/evidence/WO-AEX-002-verification.md",
  "docs/notes/agentic-execution-contracts.md",
  "docs/notes/README.md",
]

[relations]
implements = ["REQ-AEX-001", "REQ-AEX-002", "REQ-AEX-003", "REQ-AEX-004", "REQ-AEX-005"]
specifications = ["SPEC-AEX-001", "SPEC-AEX-002", "SPEC-AEX-003"]
architecture = ["ARCH-AEX-001", "ADR-AEX-001", "ADR-AEX-002", "ADR-AEX-003"]
verification = ["VER-AEX-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T11:49:36Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-24T12:07:22Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-24T12:55:45Z"
decided_by = "engineering-owner"
+++

# Work Order: Implement runtime-neutral AEX core contract validation

## Lifecycle and readiness

The repository owner confirmed commit-bound verification as `required` during
accountable content review. Formal implementation authority is determined by
the front-matter lifecycle state, not by the review record alone. Approval does
not start implementation; implementation starts only after the required focus
and start preflight have been read and the engineering owner gives an explicit
start decision.

`SPEC-AEX-003` and `ADR-AEX-003` formalize and govern the Phase 2 decisions
identified in
`docs/notes/agentic-execution-phase-2-contract-closure.md`. Their authoritative
lifecycle states are recorded in their front matter and lifecycle events. If a
future accountable decision changes the applicable relations, executable
surface, repository-state binding, or authoritative envelope derivation and
persistence boundary, revise or replace the applicable formal artifacts before
implementation continues.

Commit-bound verification is `required` because later skills and mutation
controls will rely on this executable contract layer. The classification does
not start implementation or establish an assurance result.

## Objective

Implement a small, runtime-neutral, harness-owned contract layer for strict
validation, canonical encoding, digesting, non-authoritative candidate
construction, and pure admission assessment of the
approved AEX autonomy-envelope, decision-packet, execution-receipt, and portable
skill-profile semantics. The result must make malformed, ambiguous, stale, or
scope-expanding inputs fail before a caller-side effect sentinel can run, while
granting no authority and performing no repository mutation itself. Successful
Phase 2 outcomes are `constructed` and `admissible`, never `derived` or
`admitted`.

## In scope

- Add one versioned machine-readable catalog for the four approved Phase 2
  contract families and their auxiliary repository-state, worktree-state, and
  packet-context schemas. Encode the exact field sets, scalar types, bounds,
  enum values, semantic ordering, set normalization, compatibility variants,
  and closed diagnostics from `SPEC-AEX-003` without adding design choices.
- Add a standard-library Python module that strictly parses the catalog and
  semantic objects, rejects duplicate or unknown fields, validates portable
  paths and lowercase SHA-256 identities, and returns stable diagnostics.
- Implement `se-harness-canonical-json-v1` encoding and digest behavior shared
  by autonomy envelopes, decision packets, execution receipts, and logical
  portable skill profiles without changing the already distributed
  `harness-orient` identity.
- Construct canonical repository-state-binding and envelope candidates only
  from complete typed observation values supplied to the pure API. Do not read
  Git, the filesystem, managed policy, or the evaluator installation, and do
  not claim that supplied values are current or authoritative.
- Implement a pure autonomy-envelope narrowing and admission assessment that
  proves a child is equal to or narrower than its parent and that a requested
  operation, path, profile, writer count, retry, evidence obligation, and stop
  boundary is contractually admissible. Do not label the operation admitted.
- Validate exact consistency among selected work-order identity, formal
  snapshot, repository-state observation, released-evaluator payload, and
  optional parent as fixed by `SPEC-AEX-003`. A caller-supplied observation,
  string, prompt, runtime permission, or model output cannot become authority.
- Implement a deterministic, lossless decision-focused projection validator
  for `se-harness-workflow-result-v2` plus one exact
  `se-harness-decision-packet-context-v1`. It may validate or render one
  canonical `se-harness-decision-packet-v2`, and must retain validation-only
  compatibility for `se-harness-decision-packet-v1`, but may not invent a
  decision, identity, role, state, scope, recommendation, alternative, effect,
  or gate result.
- Implement execution-receipt validation for complete operation and worker
  coverage, before/after state, changed paths, evidence digests, evaluator
  identity, gates, deviations, outcome, and residual uncertainty.
- Generalize portable logical-profile validation only as needed for the
  approved runtime-neutral contract. Preserve the Phase 1 `harness-orient`
  package, digest, activation boundary, installed location, and read-only
  behavior.
- Add verifier-owned canonical vectors and adversarial fixtures, including an
  injected effect sentinel proving that rejected input cannot reach a write.
- Add concise contributor documentation and retain work-order-keyed evidence.

## Out of scope

- Adding, revising, or invoking an outcome-oriented Phase 3 skill.
- Letting an autonomy envelope authorize or execute a real repository write,
  lifecycle transition, VREC or RLS preparation, Git operation, credential use,
  network call, publication, deployment, or other external action.
- Adding a workflow command, workflow engine, decision right, lifecycle state,
  quality gate, mutation-guard integration, or managed root-policy change.
- Spawning or coordinating subagents, workers, parallel readers, parallel
  writers, worktrees, leases, conflict resolution, or an integration owner.
- Creating Codex, Claude, ChatGPT, IDE, CI, or other runtime-specific adapters,
  profiles, model defaults, hooks, MCP configuration, or permission settings.
- Real-world identity authentication, cryptographic signatures, credential
  management, or proof that an accountable decision is substantively correct.
- Selecting a new public schema, repository-state algorithm, envelope storage
  boundary, or compatibility policy informally during implementation.
- Changing the approved authority classification or treating contract
  validation, a receipt, a skill, a profile, or successful execution as an
  accountable decision.

## Authorized decision envelope

After separate approval and start authorization, the implementation actor may
choose private helper names, immutable in-memory representations, bounded
diagnostic wording, and fixture organization inside the declared paths. It may
use dataclasses, enums, mappings, and other Python standard-library facilities.

The actor may not add a dependency; widen a field, enum, path, operation,
profile, retry, writer, or decision class; choose an unresolved public or
architecture decision; integrate with a real mutation; change a managed policy
file; or create any Phase 3 skill or runtime adapter. Contract ambiguity is a
stop condition, not implementation discretion.

## Constraints

- Preserve Python 3.11+ behavior and use only the standard library.
- Preserve `se-harness-canonical-json-v1`, every approved schema and auxiliary
  schema identifier listed in `SPEC-AEX-003`, and existing
  `se-harness-skill-contract-v1` compatibility.
- Treat catalog bytes, JSON, paths, artifact IDs, digests, workflow results,
  repository observations, worker results, and runtime metadata as untrusted.
- Parse JSON with duplicate-key detection and fail on unknown schemas, fields,
  types, invalid Unicode, floats, excessive nesting or size, and non-canonical
  identities.
- Keep validation, candidate construction, and admission assessment pure: no
  filesystem, Git, lifecycle, credential, process, network, or external-system
  effect occurs from parsing, validation, construction, projection, encoding,
  or digesting.
- A child envelope is valid only if every dimension is equal to or narrower
  than its parent. Defaults, normalization, retries, and fallback cannot widen
  it.
- Decision packets and human renderings must preserve the same semantic facts
  as the source workflow result and exact packet context. Adding the required
  v2 context must not reinterpret a v1 field.
- Receipts remain non-authoritative evidence and must expose failed, timed-out,
  cancelled, or missing required work rather than summarize it away.
- Preserve the canonical Phase 1 skill source and do not create a second skill
  copy under `se_harness/`.

## Expected change surface

The exact authorized paths are declared in `[execution_scope]`. The new Python
module and contract catalog form the executable core. Existing skill-contract
code may change only for shared canonical behavior or reusable logical-profile
validation that leaves `harness-orient` byte and semantic identity unchanged.
Package metadata may change only to distribute the new catalog. Tests, fixtures,
documentation, and evidence are restricted to the declared paths.

Approval of this work order is bounded implementation authority, not an
implementation change or start decision. If inspection shows another
executable or packaging path is necessary, revise or replace the applicable
formal artifacts and obtain accountable approval before touching that path.

## Required verification

- Execute every applicable `VER-AEX-001` case for `REQ-AEX-001` through
  `REQ-AEX-005` without claiming coverage for Phase 3 orchestration or adapters.
- Use verifier-owned positive and negative vectors for every schema, field,
  type, enum, null rule, collection order, compatibility variant, bound,
  canonical byte sequence, closed `AEXCON` code, and digest.
- Prove duplicate keys, unknown fields, malformed UTF-8, floats, non-finite
  values, invalid integers, excessive size or nesting, invalid paths, invalid
  identifiers, malformed digests, and unknown schema versions fail closed.
- Exercise equal, narrower, and wider envelope matrices across work-order and
  repository binding, operations, paths, profiles, writer count, retries, stop
  boundaries, and evidence obligations.
- Prove exact worktree-state and repository-binding bytes from independently
  constructed fixtures covering staged, unstaged, deleted, renamed, untracked,
  ignored, executable, symlink, clean-gitlink, case-collision, special-entry,
  unstable-observation, and resource-bound cases. Do not inspect a live
  repository from the candidate module.
- Wrap pure assessment with a verifier-owned caller-side effect sentinel and
  prove every invalid, stale, ambiguous, or expanded case returns before the
  sentinel is called. Prove the pure API itself has no effect callback.
- Prove deterministic canonical bytes under key insertion, filesystem
  enumeration, locale, line-ending, and set-order permutations.
- Prove the exact field mapping from independently encoded workflow-result and
  packet-context fixtures, including selected scope, lifecycle state, all
  blockers, gates, context identities, evidence, recommendation, complete
  alternatives, preview, effects, non-effects, next step, and command or
  response. Missing or conflicting decisions and incomplete contexts must
  produce no packet.
- Prove receipt coverage includes every requested operation and worker outcome,
  rejects missing required entries, excludes secrets and hidden reasoning, and
  cannot assert accountable authority.
- Re-run the Phase 1 `harness-orient` focused tests and portable-core digest
  check unchanged.
- Run the complete repository suite, source and package validation, exact
  released-evaluator doctor and validation, `git diff --check`, and exact
  changed-path comparison against this work order.

## Evidence to record

Retain exact candidate and released-evaluator identities, contract-catalog and
canonical-vector digests, parser and diagnostic matrices, repository-state and
worktree-state vectors, envelope construction, narrowing, and admissibility
results, effect-sentinel counts, workflow-result/context projection
equivalence, receipt completeness and redaction results, Phase 1 regression
identity, package inventory, full-suite counts and duration, exact changed
paths, deviations, manual assessments, and residual uncertainty at
`docs/engineering/agentic-execution/evidence/WO-AEX-002-verification.md`.

## Stop and escalate conditions

Stop before implementation while this artifact is `draft`. After approval,
stop before selecting or changing the authoritative envelope derivation or
storage mechanism, repository-state representation, public schema, canonical
encoding, decision classification, workflow-result semantics, authority
boundary, managed policy, real mutation interface, additional dependency,
runtime adapter, skill, worker, Git action, credential use, network call, or
external effect. `SPEC-AEX-003` closes those public decisions; any ambiguity or
need to depart from them is a stop, not implementation discretion. Stop on any
required verification failure that cannot be
corrected inside the approved contracts and exact path scope.

## Completion report format

Report `Outcome`, `Done`, `Not done`, conditional `Blocked by`, `Current
lifecycle state`, `Decision required`, `Next`, `Command or response`, and
conditional `Alternatives`. Name `WO-AEX-002`, the implemented requirements,
contract and evaluator identities, exact changed paths, verification results,
evidence path, deviations, residual uncertainty, and intentionally unperformed
skills, mutation, orchestration, adapter, Git, release, credential, network,
and external actions. Recommend exactly one next authorized step.
