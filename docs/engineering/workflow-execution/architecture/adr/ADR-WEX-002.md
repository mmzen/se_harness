+++
id = "ADR-WEX-002"
type = "adr"
title = "Stateless checkpoint engine with typed policy registries"
status = "approved"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[relations]
decides = ["ARCH-WEX-002"]
+++

# ADR: Stateless checkpoint engine with typed policy registries

## Status

Accepted on 2026-08-21 through the technical owner's explicit instruction `I
accept ADR-WEX-002`. Acceptance decides `ARCH-WEX-002`; it does not itself
authorize implementation or grant commit, assurance, release, or
external-action authority.

## Context

`ADR-WEX-001` moved lifecycle scope, transition, preparation, and next-action
mechanics from agent prose into one local transactional kernel. The next problem
is broader: agents can still run repository-wide inspection during bounded
work, interpret gate names rather than evaluate predicates, follow vague
procedure wording, change undeclared paths, and add provider-specific prose or
actions to the final handoff.

`SPEC-WEX-002` requires exact/prefix execution scope, caller-declared change
sets, fixed compliance checkpoints, executable gate predicates, typed procedure
steps, exact decision stops, and one schema-2 restitution returned consistently
by supported agents. The architecture must add these controls without turning
the harness into a stateful orchestrator, restoring rejected trusted-base
enforcement, or allowing repository data to become executable code.

## Decision drivers

- The same snapshot and explicit inputs must produce the same scope,
  compliance, current step, and restitution for every supported agent.
- Repository-wide maintenance findings must not become selected-work actions.
- Gate evaluation must expose every exact predicate as `pass`, `fail`, or
  `not_assessable`; a score or agent judgment is insufficient.
- Procedure wording must resolve to exact argument arrays, fixed references, or
  exact decision requests.
- Human decisions must remain explicit stops, not commands inferred from gate
  success.
- Changed-path enforcement must be honest about caller-declared completeness and
  must not claim trusted-base observation.
- The solution must preserve local, offline, repository-native, Python 3.11+
  standard-library operation and the existing atomic writer.
- Policy, documentation, package data, and adapter behavior must be testable as
  one distributed public contract.

## Considered options

### Option A — Strengthen Markdown and prompts only

Replace vague phrases with exact commands and add stronger agent instructions.
This improves readability but does not make gate predicates executable, prevent
policy duplication, validate path scope, or stop providers adding unrelated
findings and next actions.

### Option B — Put orchestration in provider-specific Skills or adapters

Create rich ChatGPT, Claude, and Codex adapters that track current work, run
checks, and compose output. This can improve each host quickly, but duplicates
governance logic, depends on model activation and compliance, and makes parity
and version migration difficult to prove.

### Option C — Add a persistent local workflow session or journal

Start a session for a selected work order, record touched files and completed
steps, and close it with a receipt. This provides stronger continuity but adds a
second persistent state model, crash and concurrency recovery, stale sessions,
cleanup, identity questions, and new authority ambiguity. Session state can
diverge from formal artifacts and Git without solving caller honesty.

### Option D — Add a stateless checkpoint engine with typed registries

Evaluate each boundary from the current formal snapshot and explicit inputs.
Store workflow and procedures in versioned `WORKFLOW.json`, gate predicates in
versioned `QUALITY_GATES.json`, and execution paths in the work order. Accept a
caller-declared complete change manifest, produce tri-state gate evidence, and
return one schema-2 restitution. Keep adapters thin and existing mutation
planning authoritative.

### Option E — Use a hosted workflow service

Move sessions, identity, policy, and gate evidence to an external coordinator.
This could authenticate users and observe more actions, but replaces the local
repository-native boundary, introduces availability and deployment concerns,
and conflicts with offline adoption and the single standard installation.

## Decision

Choose Option D.

Extend the existing provider-neutral kernel with one stateless checkpoint
application service. Each invocation receives a selected artifact, checkpoint,
optional procedure, current repository state, evidence references, and an
explicit complete change set or completeness assertion. It rebuilds the formal
index once, resolves the first matching workflow rule, binds the current typed
procedure step, evaluates every required gate predicate, and creates one
immutable schema-2 result.

Make `WORKFLOW.json` schema v2 the executable owner of rule order, procedure
graphs, typed parameters, exact argument arrays, decision steps, effects,
non-effects, and alternatives. Add `QUALITY_GATES.json` as the executable owner
of gate/predicate structure, evidence requirements, and closed evaluator keys.
Keep `WORKFLOW.md` and `QUALITY_GATES.md` as conformance-bound human policy and
explanation, not duplicate execution engines.

Represent commands as argument arrays and resolve predicates only through a
closed local evaluator registry. Repository-context actions are fixed marked
references and are never executed by contract validation. Procedure references
are finite, acyclic, and bounded. Decision steps stop until the named decision
right is explicitly exercised.

Add a read-only public `harnessctl check` boundary for start, pre-action, and
handoff checkpoints. Existing transition and preparation commands invoke the
same service during plan and again before apply. Preserve their existing
explicit decision, proposed-final-graph, stale-input, transactional writer, and
rollback controls.

Use `[execution_scope].paths` on new or resumed implementation work orders and a
caller-supplied `se-harness-change-set-v1` manifest or equivalent complete path
list. Treat completeness as an assertion and report `not_assessable` when it is
absent. Reject declared out-of-scope paths, but do not claim detection of hidden
paths or implement trusted-base lifecycle-diff enforcement.

Emit `se-harness-workflow-result-v2` and one canonical human restitution with
done, not done, exact blockers, state, decision, one next step, exact
command/response, and only declared alternatives. Supported adapters return the
human block verbatim and own no surrounding workflow prose.

## Consequences

### Positive

- Selected findings, gates, procedures, and restitution become deterministic
  and independently testable across supported agents.
- Every actionable workflow row is bound to an exact machine procedure; vague
  prose cannot silently become behavior.
- Tri-state predicate evidence makes missing information visible instead of
  turning it into a pass or generic quality judgment.
- Stateless invocations avoid session cleanup, crash recovery, concurrency
  ownership, and a second persistent lifecycle model.
- Existing atomic transition and preparation guarantees remain the sole mutation
  path.

### Negative and operational

- The package gains two versioned policy schemas, an execution-scope schema, a
  change-manifest schema, a procedure graph, a predicate registry, and a
  schema-2 public result that must evolve compatibly.
- Checkpoints repeat validation and policy resolution; indexing and performance
  tests are required for large repositories and path sets.
- New or resumed implementation work orders need explicit path declarations.
  Existing free-form workflow rules and schema-1 consumers require a published
  migration window.
- Documentation, managed locks, package data, runtime policy, public help,
  verifier fixtures, and supported adapters must advance together.
- A long but exact canonical receipt may be necessary when completeness and
  concision conflict; required effects and blockers cannot be truncated.

### Security and trust

- Argument arrays and a closed evaluator registry prevent policy files from
  injecting shell commands, imports, or expressions into execution.
- Path, reference, manifest, and policy parsing becomes a larger hostile-input
  surface requiring strict limits and boundary tests.
- Caller-declared change completeness remains unauthenticated. The result must
  never describe it as proof or equivalent to a trusted diff.
- Passing gates remain derived evidence, not identity, approval, verification,
  release, or external authority.
- Unsupported hosts can still add prose; the canonical CLI result and supported
  adapter conformance define the enforceable boundary.

### Migration

- Existing schema-1 focus, transition, and preparation output remains available
  during one published compatibility window; the new `check` command is
  schema-2 only.
- Existing completed work orders remain readable without execution scope. A new
  or resumed implementation without it is `not_assessable` until accountable
  scope is declared.
- Existing unbound workflow directives remain readable only during the same
  window; every new or changed rule requires a typed procedure immediately.
- No installer or upgrade rewrites repository-owned historical artifacts.
- Direct-edit or trusted-base enforcement requires a new requirement and ADR;
  this decision does not revive `REQ-WEX-006`.

## Validation

- Execute every independent black-box case in `VER-WEX-002` through installed
  public entry points and verifier-owned expectations.
- Prove equivalent selected state and inputs produce identical rule, procedure,
  gate, error, and restitution results across supported Python runtimes and
  agent adapters.
- Mutate workflow, gate, procedure, context-action, scope, manifest, and evidence
  contracts through every invalid reference, type, cycle, depth, path, and
  freshness boundary.
- Confirm commands remain argument arrays, evaluator keys resolve through one
  closed registry, and no repository text is executed or imported.
- Confirm transition and preparation checkpoints run before planning/apply and
  retain existing stale-state, final-graph, atomic-write, and rollback behavior.
- Compare complete repository digests for every read-only or failed path.
- Confirm selected restitution contains no unrelated ID, finding, decision, or
  action, while true repository-integrity blockers remain visible.
- Confirm `WORKFLOW.md`, `QUALITY_GATES.md`, JSON policy, managed locks, package
  data, help, fresh installs, upgrades, and runtime-loaded contracts conform.
- Confirm no source, test, interface, or work-order scope implements rejected
  `REQ-WEX-006`, persistent workflow sessions, or provider-owned governance
  rules.
