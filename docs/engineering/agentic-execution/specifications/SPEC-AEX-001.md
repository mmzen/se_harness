+++
id = "SPEC-AEX-001"
type = "specification"
title = "Agentic authority, delegation, and evidence contract"
status = "approved"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
specifies = ["REQ-AEX-001", "REQ-AEX-002", "REQ-AEX-003", "REQ-AEX-004"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T09:03:54Z"
decided_by = "technical-owner"
+++

# Specification: Agentic authority, delegation, and evidence contract

## Scope

This specification defines the runtime-neutral control contract for delegated
agent execution. It separates accountable decision roles from agent execution
profiles, classifies actions and decisions, constrains autonomous mutation with
an explicit envelope, stops at accountable decision points, and records deterministic
decision packets and execution receipts.

The contract extends the existing harness workflow rather than replacing it.
Formal artifacts, managed decision rights, quality gates, workflow rules,
installed integrity, and the target repository's exact released evaluator
remain authoritative. The contract does not prove real-world identity or the
quality of an accountable judgment.

## Actors and external systems

- Accountable product, requirements, technical, engineering, assurance,
  release, service, risk, and external-action owners exercise managed decision
  rights.
- A primary execution agent coordinates the selected procedure and returns the
  final result.
- Agent workers execute bounded tasks under named non-accountable execution
  profiles.
- Skills provide reusable procedures but do not calculate lifecycle legality.
- The installed released evaluator validates integrity, state, gates, scope,
  and mutation authority.
- Git supplies candidate and worktree observations without supplying approval.
- The filesystem contains untrusted repository content and must retain no
  partial governed mutation after failure.
- Runtime providers supply models, tools, sandboxes, permission modes, and
  optional subagent execution without becoming authority sources.

## Inputs

### Selected workflow scope

- repository target;
- exact selected artifact or work order;
- current formal graph and installed lock;
- exact released-evaluator identity required by the repository;
- phase-appropriate workflow procedure and quality gates.

### Actor and worker assertions

- `accountable_role`: the role required by the applicable decision right;
- `decision_actor`: an explicit actor assertion recorded by the managed
  lifecycle procedure;
- `execution_profile`: a non-accountable worker profile;
- `runtime_permissions`: observed technical permissions, never authority;
- `skill_identity`: stable name, version, and content digest when a skill is
  used.

An actor assertion is data. The harness validates required structure and
consistency but does not prove that the caller holds the real-world role.

### Autonomy envelope

The proposed versioned semantic object is
`se-harness-autonomy-envelope-v1`. Its logical fields are:

```json
{
  "schema": "se-harness-autonomy-envelope-v1",
  "selection": {
    "work_order": "WO-...",
    "work_order_sha256": "lowercase-sha256",
    "repository_state": "implementation-defined immutable observation",
    "evaluator_payload_sha256": "lowercase-sha256"
  },
  "delegation": {
    "asserted_by": "accountable-role-or-actor",
    "operations": ["operation-id"],
    "path_scope": ["repository-relative-path-or-component-prefix"],
    "execution_profiles": ["profile-name"],
    "max_parallel_writers": 1,
    "retry_limits": {"operation-id": 0},
    "stop_before": ["decision-class-or-decision-right-id"]
  },
  "evidence": {
    "required_receipt": true,
    "required_paths": ["repository-relative-path-or-component-prefix"]
  }
}
```

The exact repository-state observation and authoritative envelope storage or
derivation mechanism are deliberately deferred from the read-only pilot. A
later mutation work order must amend or refine this contract and obtain
accountable approval before it can use an envelope. Host-absolute paths,
environment secrets, runtime-only thread IDs, and conversation content are
prohibited authority inputs.

## Outputs

### Decision packet

The versioned semantic object is `se-harness-decision-packet-v1`:

```json
{
  "schema": "se-harness-decision-packet-v1",
  "decision": {
    "kind": "decision-right-or-stop-kind",
    "subject": "artifact-id-or-exact-action",
    "required_accountable_role": "role",
    "recommendation": "one-bounded-recommendation",
    "alternatives": []
  },
  "identity": {
    "repository": "portable-repository-identity",
    "candidate_commit": "full-commit-or-null",
    "evaluator_payload_sha256": "lowercase-sha256-or-null"
  },
  "assessment": {
    "gates": [],
    "evidence": [],
    "findings": [],
    "assumptions": [],
    "residual_uncertainty": []
  },
  "effect": {
    "preview": {},
    "effects": [],
    "non_effects": []
  },
  "handoff": {
    "command_or_suggested_response": {},
    "safe_to_defer": true
  }
}
```

Every packet contains exactly one primary decision. Alternatives are included
only when each is complete and authorized for the same current state. This is a
separate schema generated as a lossless decision-focused projection of
`se-harness-workflow-result-v2`; it does not extend or replace the workflow
result. Conformance tests must prove that selected state, blockers, gates,
decision, effects, non-effects, next step, and command or response retain the
same meaning in both objects. Human output renders this packet and cannot add a
different recommendation.

### Execution receipt

The versioned semantic object is `se-harness-execution-receipt-v1`:

```json
{
  "schema": "se-harness-execution-receipt-v1",
  "selection": {
    "repository": "portable-repository-identity",
    "artifact": "artifact-id-or-null",
    "autonomy_envelope_sha256": "lowercase-sha256-or-null"
  },
  "execution": {
    "profiles": [],
    "skills": [],
    "operations": [],
    "worker_results": []
  },
  "effects": {
    "changed_paths": [],
    "evidence": [],
    "state_before": [],
    "state_after": []
  },
  "validation": {
    "evaluator": {},
    "gates": [],
    "outcome": "completed-or-degraded-or-stopped-or-failed",
    "deviations": [],
    "residual_uncertainty": []
  }
}
```

For `harness-orient`, `profiles` contains only `single-agent-orientation`,
`skills` contains the name, version, and portable-core digest, `operations`
contains every attempted released-evaluator operation, `worker_results` is an
empty array, and `changed_paths`, `state_before`, and `state_after` prove the
read-only result. `SPEC-AEX-002` defines the evaluator capability fields and
degraded outcome for this profile.

### Canonical encoding and retention

Decision packets and execution receipts use the
`se-harness-canonical-json-v1` representation:

- UTF-8 without a byte-order mark;
- object keys sorted by Unicode code-point order;
- no insignificant whitespace and exactly one trailing LF;
- JSON strings, booleans, null, arrays, objects, and bounded base-10 integers;
  floating-point and non-finite values are prohibited;
- duplicate and unknown keys are rejected;
- every schema field is present; unavailable scalar values use `null` and
  unavailable collections use an empty array or object as declared by the
  schema; and
- arrays follow their declared semantic order; sets are normalized into stable
  unique order before encoding.

The object digest is lowercase SHA-256 over those canonical bytes and is stored
outside the object to avoid self-reference. Schema evolution requires a new
schema identifier; readers fail closed on an unknown identifier.

A read-only procedure returns its receipt to the caller and does not retain it
inside the target repository. A separately authorized work order may retain the
exact returned bytes and digest at its declared evidence path. Mutating work
must declare its receipt location in the selected work order or envelope before
the first governed write. Host paths, command launchers, timestamps, and runtime
thread IDs may appear in a local diagnostic wrapper but are excluded from the
portable canonical object. The receipt remains non-authoritative evidence even
when retained and hashed.

## State model

Agentic execution introduces no new formal lifecycle state in this proposal.
It classifies procedure boundaries:

| Class | Meaning | Autonomous handling |
| --- | --- | --- |
| `routine-read-only` | Read, calculate, validate, test, render, or otherwise observe without an accountable decision or write | May run when technically permitted and within selected scope |
| `advance-delegation-required` | A managed operation or decision that may run only when an accountable owner delegated it in advance | May run only under a valid autonomy envelope |
| `accountable-decision-required` | A decision requiring current accountable judgment | Stop and emit a decision packet |
| `action-time-authorization-required` | Merge, tag, publish, deploy, operate, use credentials, or affect an external system | Stop until exact action-time authority exists |

### Current decision-right classification

This table covers the complete decision-right catalog in the managed
`DECISION_RIGHTS.md` used by this proposal. A future catalog entry is
`accountable-decision-required` until an accountable amendment explicitly
classifies it.

| Decision right | Class | Advance delegation | Required boundary and evidence |
| --- | --- | --- | --- |
| `DR-DEFINITION-DECIDE` | `accountable-decision-required` | no | Stop before approval or rejection; present the selected definition, applicable G0-G2 results, exact target state, and accountable artifact owner |
| `DR-WO-SELECT` | `accountable-decision-required` | no | Stop before work-order approval or rejection; present the complete governing chain, assurance classification, scope, and engineering owner |
| `DR-WO-START` | `advance-delegation-required` | yes, only when explicitly named | Require an approved WO, passing G3 preflight, unchanged selected scope and evaluator identity, and an envelope recorded by the engineering owner before start |
| `DR-WO-COMPLETE` | `advance-delegation-required` | yes, only when explicitly named | Require complete declared implementation evidence, passing handoff checks, unchanged scope, and an engineering-owner envelope recorded before implementation |
| `DR-VREC-PREPARE` | `advance-delegation-required` | yes, preparation only | Require exact candidate, WO, VER, evidence, passing candidate-ready gate, and a named preparation actor; stop before `verified` |
| `DR-VREC-DECIDE` | `accountable-decision-required` | no | Stop with the ready VREC, exact candidate and evidence assessment for the assurance owner; verification, rejection, and supersession remain current human decisions |
| `DR-DELIVERY-SELECT` | `accountable-decision-required` | no | Stop after verified coverage and before choosing repository integration or release preparation; identify the repository or release owner |
| `DR-RLS-PREPARE` | `advance-delegation-required` | yes, preparation only | Require exact REL, eligible VREC and WO coverage, version, candidate, passing preparation gate, and a prior release-owner envelope; stop before `released` |
| `DR-RLS-DECIDE` | `accountable-decision-required` | no | Stop with the ready RLS, exact candidate, coverage, and release evidence for the release owner |
| `DR-EXTERNAL-ACTION` | `action-time-authorization-required` | no | Stop before merge, tag, publish, deploy, credential use, production operation, or other external effect; require exact action-time authorization for the named target |
| `DR-RELATED-RECORD-SELECT` | `routine-read-only` | not applicable | Read only the exact selected ID; selection changes no lifecycle state and grants no right over the selected record |
| `DR-REMEDIATION-SCOPE` | `accountable-decision-required` | no | Stop before creating or widening definition or work scope; present the failed criterion, proposed bounded remediation, and affected accountable owner |

Predelegation records the accountable owner, delegate identity, exact decision
right, selected artifact, allowed outcome, evidence obligation, expiry or state
binding, and narrower child-delegation rule. It never includes a later
`accountable-decision-required` or `action-time-authorization-required` effect.
The first pilot implements none of these advance-delegated mutations; it
consumes only the `routine-read-only` boundary.

## Behavioral rules

1. **AEX-AUTH-001:** An accountable role and an execution profile occupy
   different fields and cannot substitute for one another.
2. **AEX-AUTH-002:** Runtime permissions and model capabilities are observations,
   not engineering authority.
3. **AEX-ENV-001:** A mutation request without a valid selected work order and
   applicable envelope fails before planning writes.
4. **AEX-ENV-002:** An envelope may narrow but never broaden its work order.
5. **AEX-ENV-003:** Envelope identity is rechecked immediately before every
   governed write or transactional packet.
6. **AEX-ENV-004:** Child delegation inherits an equal or narrower operation,
   path, profile, writer, retry, evidence, and stop boundary.
7. **AEX-STOP-001:** `accountable-decision-required` decisions and
   `action-time-authorization-required` actions stop before their effects and
   produce a single decision packet.
8. **AEX-STOP-002:** Failed or not-assessable required gates cannot be converted
   into an approval recommendation.
9. **AEX-REC-001:** Every completed, stopped, or failed autonomous stage produces
   one receipt or an explicit receipt-generation failure.
10. **AEX-REC-002:** Aggregate receipts retain every requested worker outcome,
    including failure, timeout, cancellation, and missing output.
11. **AEX-REC-003:** A receipt cannot create a lifecycle event or accountable
    decision fact.
12. **AEX-ID-001:** Candidate, installed evaluator, candidate package, and
    runtime identities remain separately labeled.
13. **AEX-FAIL-001:** Invalid inputs, stale state, or write failure leave no
    unplanned or partial governed effect.

## Error and recovery behavior

- Validate field sets, types, identifiers, duplicates, path forms, scope
  relations, digests, decision classes, and evaluator identity before mutation.
- Return stable diagnostic codes for missing authority, stale envelope,
  operation denial, path denial, writer conflict, accountable-decision-required
  stop, failed gate, receipt incompleteness, and unsupported capability.
- A recoverable operation may retry only within its declared operation-specific
  limit and unchanged scope.
- Interrupted transactions follow the existing common mutation rollback
  boundary and expose restoration failure explicitly.
- A failed receipt or packet renderer cannot convert a failed operation into a
  completed handoff.
- Recovery never infers a wider envelope or reclassifies an
  `accountable-decision-required` decision.

## Data and interface contracts

- JSON objects reject duplicate keys and unknown fields unless a future schema
  explicitly defines extension behavior.
- Repository-relative paths use `/`, reject traversal and absolute forms, and
  apply exact-file or component-boundary directory-prefix matching.
- Digests use lowercase SHA-256 over explicitly defined canonical or raw bytes.
- IDs and decision-right names use closed registries or validated formal
  identities; free-form text cannot create an operation.
- Arrays use stable semantic ordering and reject duplicates where order is not
  meaningful.
- Timestamps, when retained, use UTC RFC 3339 seconds and are excluded from
  otherwise deterministic plan output.
- Host paths and runtime thread IDs may appear only in bounded diagnostic views,
  never in portable retained authority or evidence identity.

## Security and privacy properties

- Treat envelope content, actor assertions, profile names, skill metadata,
  paths, receipts, commands, outputs, and repository files as untrusted input.
- Never evaluate repository text, skill text, or model output as shell syntax.
- Store command arguments as structured arrays rather than reconstructed shell
  strings.
- Exclude secrets, credentials, environment dumps, hidden reasoning, private
  evidence bodies, and unrelated repository content from normal packets and
  receipts.
- Reject symlink or junction escape, case collision, reserved device names,
  alternate separators, wildcard expansion, URI forms, and control characters
  at supported path boundaries.
- Technical sandbox or permission changes cannot override a denied harness
  operation.

## Performance and capacity

- Envelope validation, packet generation, and receipt generation should remain
  linear or near-linear in selected scope and declared worker results.
- Normal human decision packets should remain concise enough to review without
  loading raw test logs or full evidence bodies.
- Large worker sets require an explicit configured bound; unbounded recursive
  delegation is unsupported.
- Receipt size limits and evidence indirection must preserve diagnosis without
  embedding arbitrarily large command output.

## Observability

- Report selected artifact, decision class, required accountable role,
  execution profile, envelope digest, skill digest, worker outcome, changed
  paths, gate result, and evaluator identity where applicable.
- Distinguish selected-scope blockers, repository blockers, and background
  observations.
- Record degraded capability and fallback use explicitly.
- Measurements aggregate workflow outcomes without exposing private prompt or
  reasoning content.

## Compatibility and migration

- Existing repositories without an autonomy envelope continue to use the
  current command-driven and explicitly authorized workflow; absence never
  grants autonomy.
- Existing workflow restitution remains valid. Decision-packet integration must
  provide a lossless mapping or an explicit schema migration.
- Existing artifacts are not rewritten automatically to add agentic metadata.
- Candidate source cannot become the locked evaluator through skill execution.
- Managed upgrades preserve owner content and fail on ambiguous or customized
  changes.

## Examples and counterexamples

### Example: valid predelegated operation

An approved work order and envelope allow one implementation worker to edit
`se_harness/` and `tests/`, run tests, and retain evidence. The worker may
perform those operations, but it stops before commit, VREC verification,
release, or publication because those effects are absent or require a separate
accountable decision or action-time authorization.

### Counterexample: permission implies authority

A runtime launches a worker with workspace-write and a profile named
`release-owner`. No formal release decision exists. The worker cannot prepare or
apply a release transition solely from those runtime facts.

### Counterexample: summary hides failure

An orchestrator requests three required reviewers and receives two successful
results plus one timeout. A receipt that lists only the successful reviewers is
invalid; the decision packet must expose incomplete coverage.

## Explicitly unspecified decisions

- The authoritative storage or derivation location of an autonomy envelope.
- Real-world actor authentication or cryptographic decision signatures.
- Runtime-specific model, tool, sandbox, and approval-mode selection.

The envelope-storage decision requires an approved specification amendment
before autonomous mutation. Authentication, signatures, and runtime-specific
selection require later bounded artifacts if adopted. None is required to
implement the read-only `harness-orient` pilot.
