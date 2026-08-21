+++
id = "ARCH-WEX-002"
type = "architecture"
title = "Stateless scoped workflow control plane"
status = "approved"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[relations]
addresses = ["REQ-WEX-007", "REQ-WEX-008", "REQ-WEX-009", "REQ-WEX-010"]
conforms_to = ["SPEC-WEX-002"]

[decision_assessment]
outcome = "adr_required"
triggers = ["system-boundary", "responsibility-or-dependency-direction", "public-interface-or-protocol", "data-ownership-or-persistence", "security-privacy-or-trust-boundary", "concurrency-consistency-reliability-or-failure-strategy", "cross-cutting-policy", "difficult-to-reverse", "material-alternatives"]
rationale = "Adding work-order execution-scope metadata, executable gate and procedure registries, a public checkpoint command, schema-2 restitution, and a strict agent-adapter boundary materially changes persistent contracts, dependency direction, public interfaces, trust and failure boundaries, and cross-cutting workflow policy. Stateless evaluation, persistent workflow sessions, provider-owned adapters, and an external coordinator are material alternatives, and the distributed schemas will be difficult to reverse after release."
assessed_by = "technical-owner"
+++

# Architecture: Stateless scoped workflow control plane

## Lifecycle

Approved on 2026-08-21 through the technical owner's explicit approval after
acceptance of `ADR-WEX-002`. This approval authorizes the architecture contract
for selection by a separately approved work order; it grants no implementation,
commit, assurance, release, or external-action authority.

## Context and scope

`ARCH-WEX-001` centralizes scope projection, lifecycle policy, atomic mutation,
preparation, and next-action selection in one provider-neutral local kernel.
`SPEC-WEX-002` extends that kernel from lifecycle mechanics to the complete
selected iteration: declared implementation paths, executable gate predicates,
typed procedures, and canonical restitution.

The scope begins with one selected artifact or explicit definition packet and a
repository snapshot. It ends with a read-only checkpoint result, an existing
governed mutation, or a canonical schema-2 restitution. It includes
`WORKFLOW.json`, `QUALITY_GATES.json`, work-order execution-scope metadata,
caller-declared change manifests, procedure resolution, evidence freshness,
gate evaluation, contract conformance, and supported-agent adapter output.

It excludes trusted-base lifecycle-diff validation under rejected
`REQ-WEX-006`, arbitrary editor interception, authenticated identity, a daemon
or workflow database, provider-specific lifecycle rules, Git writes, network
services, commits, pull requests, release, publication, deployment, and
operation.


## Components and responsibilities

- The existing formal index and scope projector provide selected artifacts,
  governing artifacts, dependencies, validation findings, and formal-snapshot
  digests.
- The execution-scope codec parses and validates exact file and directory-prefix
  declarations from work orders.
- The change-set codec normalizes caller paths, records completeness assertions,
  and never claims that an assertion proves an omitted change does not exist.
- The policy loader validates and loads versioned workflow and quality-gate JSON
  from the installed immutable distribution boundary.
- The workflow rule selector owns ordered rule selection. Callers cannot choose
  a later matching rule.
- The procedure resolver owns `PROC-*`, `STEP-*`, typed parameters, canonical
  argument arrays, decision stops, context-action references, depth limits, and
  cycle detection.
- The gate registry owns `QG-*` and `QGP-*` structures; a closed evaluator
  registry maps predicate keys to local pure evaluators.
- The evidence binder resolves artifact, command, path, and result references
  and evaluates snapshot-based freshness without treating time as proof.
- The checkpoint service composes selected scope, current workflow rule,
  procedure step, gate results, and final status for start, pre-action,
  transition, and handoff boundaries.
- The schema-2 result model owns compliance and restitution data. Human and JSON
  renderers consume only that model.
- Contract conformance validates JSON registries, Markdown bindings,
  repository-context action markers, schema compatibility, and packaged/runtime
  identity.
- Existing lifecycle planners, preparation adapters, and the transactional
  writer remain the only governed mutation boundary and call the checkpoint
  service before plan/apply.
- Supported agent adapters call public commands and return canonical restitution
  verbatim; they own no rules, gates, procedures, or prose extensions.

## Dependency direction

```text
CLI / supported agent adapter
  -> checkpoint application service
     -> formal index + existing WEX scope projector
     -> execution-scope + declared change-set codecs
     -> ordered workflow selector
        -> typed procedure resolver
        -> quality-gate registry -> closed predicate evaluators
           -> evidence binder
     -> schema-2 WorkflowResult
        -> canonical JSON renderer
        -> canonical human restitution renderer

existing transition/preparation application service
  -> checkpoint service
  -> existing planner + proposed-graph validator
  -> existing transactional writer only after pass and explicit authority
```

Policy, repository facts, and evidence flow inward as untrusted data. Gate
results, current procedure steps, and restitution flow outward as derived
evidence. Renderers, agent text, dashboards, and command success never flow back
as lifecycle authority.

## Data and control flow

For `start`, the service resolves the selected work order, execution scope,
first matching workflow rule, `PROC-WO-START`, start evidence, and every
`QG-G3-WORK-AUTHORIZATION` predicate. It exposes the next typed step only when
the checkpoint passes.

For `pre-action`, the service confirms that the requested procedure is the
selected rule or a declared alternative, binds typed parameters, evaluates the
step's gates, and emits either its exact command/decision/reference or one exact
blocker.

For `transition`, the existing planner invokes the same service during planning
and immediately before apply. Passing compliance does not replace the explicit
decision or proposed-final-graph validation. Stale evidence, policy, or formal
state blocks application without writes.

For `handoff`, the service consumes the selected final state and an explicit
complete change-set assertion or manifest. It checks path scope and applicable
completion gates, records what occurred and what expected effect remains, and
selects one current procedure step. Failure still produces a blocked canonical
restitution.

Repository-wide `inspect` bypasses selected checkpoint composition, labels its
mode explicitly, and has no primary artifact. Its findings cannot enter a
selected restitution.

## Trust boundaries

Repository files, paths, links, policy JSON, context markers, work-order scope,
change manifests, completeness assertions, evidence references, command values,
actor text, and agent output are untrusted. Managed package identity and the
current formal-snapshot digest anchor evaluation but do not establish product or
human authority.

Procedure argument arrays are data and never pass through a shell in the
kernel. Evaluator keys resolve only through a closed code registry; repository
policy cannot name arbitrary imports or executable code. Context actions are
fixed references, not code executed during validation.

The caller's complete-change assertion is an auditable claim, not proof. This
architecture can reject a declared out-of-scope path but cannot detect a path
the caller hides without the separately rejected trusted observation boundary.

The supported-adapter boundary is conformance-tested but not a security sandbox
for arbitrary hosts. The canonical CLI result remains the authoritative derived
output when a host adds or changes prose.

## Required patterns

- Stateless checkpoint evaluation from explicit repository state and inputs;
  no hidden session state.
- One immutable semantic result spanning scope, compliance, procedure, and
  restitution.
- Separate machine owners for workflow/procedure and gate/predicate data, with
  conformance-bound human documentation.
- Closed typed registries for procedures, step kinds, parameters, decision
  rights, gates, predicate evaluators, evidence kinds, and error codes.
- Canonical command argument arrays; platform quoting only in the human renderer.
- Tri-state predicates and gates with `fail > not_assessable > pass` precedence.
- Snapshot-bound evidence freshness and exact failed-predicate reporting.
- Component-boundary path matching after safe normalization.
- Explicit decision stops that cannot expose a later command before authority is
  supplied.
- Selected-result filtering before rendering, followed by byte-stable adapter
  conformance.
- Existing plan/apply, stale-input, graph-validation, rollback, and independent
  lifecycle-plane controls from `ARCH-WEX-001`.

## Prohibited patterns

- Persistent workflow sessions, journals, databases, or daemons as correctness
  state.
- Provider prompts, Skills, adapters, or Markdown prose owning workflow rules,
  gate predicates, procedure steps, or next-action selection.
- Shell command strings, shell evaluation, dynamic imports, expression
  evaluation, or repository-provided evaluator code.
- String-prefix path authorization, implicit scope expansion, or treating a
  completeness assertion as proof.
- Merging repository-wide inspection into selected findings or restitution.
- Gate health scores, warning counts, or dashboards substituting for exact
  predicate status.
- Free-form actionable directives without an exact command, fixed procedure or
  context-action reference, or exact decision request.
- Renderer or adapter additions before or after canonical restitution.
- Gate success interpreted as actor authentication, approval, verification,
  release, risk acceptance, or external authority.
- Trusted-base diff/history enforcement or direct-edit interception in this
  packet.

## Quality attributes

The architecture prioritizes cross-agent determinism, bounded attention,
explainable compliance, fail-closed mutation, honest uncertainty, auditability,
hostile-input safety, portability, and concise operation. It accepts larger
versioned policy schemas, repeated read-only validation at explicit boundaries,
and a compatibility window to remove provider interpretation.

For repositories near 1,000 formal artifacts and change sets up to 10,000 paths,
each checkpoint is bounded by one formal validation plus indexed scope, policy,
evidence, and path traversal. Runtime remains offline and Python 3.11+
standard-library only.

## Conformance checks

`VER-WEX-002` black-box tests path-scope boundaries, completeness assertions,
repository-blocker taxonomy, gate aggregation and freshness, procedure graph
and parameter safety, decision stops, schema-2 field equivalence, concise human
rendering, and supported-adapter byte parity. Failure injection confirms that a
checkpoint or transition recheck never leaves a partial mutation.

Architecture review additionally proves that the checkpoint service is
stateless, the evaluator registry is closed, command templates remain argument
arrays, policy has one owner per subject, `inspect` stays repository-wide,
existing WEX transaction guarantees remain authoritative, and no component
implements rejected `REQ-WEX-006`.

## Related ADRs

`ADR-WEX-001` owns the existing provider-neutral transactional workflow kernel.
`ADR-WEX-002` proposes the additive stateless checkpoint engine, typed workflow
and gate registries, explicit declared-change boundary, and canonical
restitution as one coherent significant decision. It must be accepted before
this architecture or an implementation work order can be approved.
