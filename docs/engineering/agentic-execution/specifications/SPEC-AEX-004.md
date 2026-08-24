+++
id = "SPEC-AEX-004"
type = "specification"
title = "Single-agent outcome skills MVP contract"
status = "approved"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
specifies = ["REQ-AEX-005", "REQ-AEX-008"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T13:50:24Z"
decided_by = "technical-owner"
+++

# Specification: Single-agent outcome skills MVP contract

## Scope

This specification defines the Phase 3 portable single-agent contract for
`harness-draft-change`, `harness-execute-work-order`, and
`harness-prepare-assurance`. It refines the general portable skill model in
`SPEC-AEX-002` and consumes the contract catalog in `SPEC-AEX-003`.

The existing `harness-orient` skill remains the read-only member of the MVP and
is not revised. This specification adds no lifecycle state, decision right,
quality gate, accountable authority, multi-agent behavior, runtime adapter, or
external-action permission.

## Actors and external systems

- The operator explicitly selects one writing skill and supplies its bounded
  request.
- The primary execution agent follows the complete portable procedure without
  spawning workers.
- Accountable owners continue to make the decisions routed by managed policy.
- The target repository's exact released evaluator supplies installed
  integrity, formal state, workflow results, preflight, draft creation, and
  verification-record preparation.
- Repository editing and test tools perform work only after the skill has
  established the applicable current path and operation boundary.
- Git supplies read-only ref, worktree, and candidate observations. Phase 3
  skills do not mutate Git.
- Runtime permissions provide technical access and never supply engineering
  authority.

## Inputs

### Common invocation

Every Phase 3 skill receives:

- one unambiguous repository target;
- a structured launcher for the target's exact external released evaluator;
- expected evaluator version and installation root;
- one explicit skill name;
- the operator's exact requested outcome and declared non-effects; and
- the applicable repository instructions and complete retained skill core.

The launcher is an argument array, not a shell command string. Host paths,
credentials, environment dumps, and provider syntax are not portable retained
inputs.

### Draft-change input

`harness-draft-change` additionally receives:

- one existing engineering domain or one explicitly requested new domain;
- a finite artifact plan containing proposed types, collision-checked IDs,
  titles, owners, relations, and intended canonical destinations;
- zero or one declared non-authoritative planning-note destination; and
- zero or more explicitly selected existing formal artifacts, each currently
  `draft`, that may be revised.

Artifact identifiers are assigned only after checking every locally available
Git ref. No remote fetch is implied. Existing approved, rejected, superseded,
implemented, verified, released, or otherwise non-draft formal artifacts are
not writable through this skill.

### Work-order execution input

`harness-execute-work-order` additionally receives:

- exactly one selected work-order ID;
- its complete current focus and preflight results;
- the complete execution-scope path manifest from current formal bytes;
- required verification contracts and evidence obligations;
- repository-owned implementation and test commands; and
- optional operator-supplied implementation constraints that only narrow the
  work order.

The work order must already be `in_progress` before an implementation effect.
An `approved` state is a read-only stop at the current work-start decision.

### Assurance-preparation input

`harness-prepare-assurance` additionally receives:

- one or more selected implemented work orders permitted by the existing
  preparation command;
- every selected verification contract and retained evidence path;
- the exact clean candidate commit observed by the released evaluator;
- one unused, collision-checked VREC identifier and canonical destination; and
- the explicit preparation actor named in the current request.

The preparation actor is recorded as preparation evidence. It is not an
assurance-owner verification decision.

## Portable contract v2

### Compatibility

`se-harness-skill-contract-v1` remains closed for the exact approved
`harness-orient` pilot. Its parser, canonical bytes, manifest digest, activation
behavior, and outputs remain unchanged.

The three new skills use `se-harness-skill-contract-v2`. A v1-only reader
rejects v2 as unsupported. A v2 reader validates both schemas but never infers
missing v2 fields from a v1 object.

### Field contract

The v2 top-level object uses a strict field set:

| Field | Contract |
| --- | --- |
| `schema` | exact `se-harness-skill-contract-v2` |
| `name` | portable lowercase hyphenated skill name |
| `version` | semantic version |
| `outcome` | bounded human-readable outcome |
| `activation` | exact `explicit`, `implicit`, and non-empty `must_not_match` fields |
| `inputs` | unique typed input declarations |
| `preconditions` | unique prerequisite IDs and bounded descriptions |
| `mutation_class` | `draft-writing` or `governed-mutation` for Phase 3 |
| `evaluator` | minimum version, required and optional public operations, and missing-capability outcomes |
| `checkpoints` | ordered before-effect, after-effect, and handoff checkpoint declarations |
| `effects` | exact permitted effect classes, prohibited effect classes, path source, and lifecycle-transition set |
| `delegation` | exact single-agent declaration with delegation disabled |
| `evidence` | receipt schema, retention behavior, and required retained evidence kinds |
| `stop_conditions` | unique stable stop IDs and outcomes |
| `outputs` | unique typed output names, schemas, and retention modes |

All objects reject unknown or duplicate fields. Collections are bounded,
ordered as declared, and encoded through `se-harness-canonical-json-v1`.

### Closed Phase 3 instances

| Property | `harness-draft-change` | `harness-execute-work-order` | `harness-prepare-assurance` |
| --- | --- | --- | --- |
| activation | explicit only | explicit only | explicit only |
| mutation class | `draft-writing` | `governed-mutation` | `governed-mutation` |
| path source | declared note and canonical draft destinations | selected work order `[execution_scope].paths` | released-evaluator-derived VREC destination |
| allowed effect classes | `draft-create`, `draft-revise`, `planning-note-write` | `implementation-write`, `test-execution`, `evidence-write` | `verification-record-prepare` |
| lifecycle transitions | empty | empty | empty; new record starts `ready` through the existing preparation procedure |
| retained target evidence | optional inline receipt; drafts themselves are retained | required only at the work-order-declared evidence destination | prepared VREC plus inline decision packet and receipt identity |
| delegation | disabled | disabled | disabled |

Each instance must list approval, work-start, work-completion, assurance
decision, delivery selection, release decision, Git mutation, credential use,
network mutation, and external action among its prohibited effect classes as
applicable. The exact applicable stop and next action come from the current
harness result, not from that descriptive list.

## Outputs

### Common skill result

Every invocation returns the `SPEC-AEX-002` skill-result facts and:

- skill name, semantic version, and portable-core digest;
- exact evaluator identity observation;
- selected artifact and before/after repository-state identities;
- completed checkpoint IDs and normalized result digests;
- planned and actual changed paths;
- retained evidence paths and digests;
- outcome `completed`, `degraded`, `stopped`, or `failed`;
- one current harness-derived next step and required role; and
- one `se-harness-execution-receipt-v1` object or an explicit receipt failure.

The human rendering and structured result preserve the same lifecycle facts.

### Draft-change output

The result identifies every requested artifact as created, revised, unchanged,
blocked, or failed. It includes collision-audit scope, canonical destinations,
formal validation result, exact changed paths, and confirmation that every
formal artifact remains `draft` with no lifecycle event added.

### Work-order execution output

The result identifies the selected `in_progress` work order, exact execution
scope, commands and results, implementation and evidence paths, review
findings, required-gate status, deviations, and residual uncertainty. A
successful execution result recommends the current engineering-owner handoff
decision but does not apply it.

### Assurance-preparation output

The result binds the prepared `ready` VREC, exact candidate commit, selected
work orders, selected verification contracts, evidence digests, candidate-ready
gate result, and the assurance decision packet. It contains no verification,
delivery, release, or external-action claim.

## State model

The common procedure states from `SPEC-AEX-002` are refined as:

```text
discovered
  -> loaded
  -> identity_checked
  -> current_state_checked
  -> effect_planned
  -> pre_effect_rechecked
  -> executing
  -> post_effect_validated
  -> completed | degraded | stopped | failed
```

`stopped` includes a valid accountable decision point or action-time boundary.
`failed` includes invalid input, integrity failure, scope mismatch, effect
failure, or invalid post-effect state. Neither state implies rollback authority
beyond the selected work order and current operation.

## Behavioral rules

1. **AEX-MVP-001:** A writing skill runs only after explicit selection of its
   exact name and target; implicit activation performs no write.
2. **AEX-MVP-002:** Validate the installed skill contract and portable-core
   digest before executing a bundled helper.
3. **AEX-MVP-003:** Establish exact released-evaluator version, identity, and
   installed integrity before trusting repository state or a managed skill.
4. **AEX-MVP-004:** Consume structured harness results. Do not parse lifecycle
   legality, required roles, gates, or transitions from human prose.
5. **AEX-MVP-005:** Build a closed effect plan from the selected skill's path
   source and permitted effect classes. An omitted permission grants nothing.
6. **AEX-MVP-006:** Recheck identity, current state, selected artifact, and
   applicable checkpoint immediately before every helper-controlled write
   transaction.
7. **AEX-MVP-007:** Reject a planned path that is absolute, escaping,
   case-ambiguous, wildcarded, URI-like, or outside the declared path source
   before invoking its effect callback.
8. **AEX-MVP-008:** Compare actual changed paths with the planned and admitted
   paths after execution. Unexpected paths prevent a successful handoff.
9. **AEX-MVP-009:** Draft change may create only new `draft` formal artifacts,
   revise explicitly selected existing drafts, and write at most one declared
   planning note. It applies no transition.
10. **AEX-MVP-010:** Work-order implementation changes no content unless the
    selected work order is `in_progress` and current preflight and focus results
    admit the phase.
11. **AEX-MVP-011:** Work-order execution records evidence and stops before the
    work-completion transition, Git mutation, VREC preparation, delivery, or
    external action.
12. **AEX-MVP-012:** Assurance preparation invokes only the existing released-
    evaluator VREC preparation operation after current candidate-ready checks
    and an explicit named preparation actor.
13. **AEX-MVP-013:** Assurance preparation creates one `ready` VREC and stops
    before verification, rejection, supersession, delivery, release, or
    external action.
14. **AEX-MVP-014:** Every invocation is single-agent. Missing subagent support
    is not a degraded condition because no Phase 3 procedure requires it.
15. **AEX-MVP-015:** Every completed, stopped, degraded, or failed invocation
    emits a deterministic receipt or exposes receipt generation as a failure.
16. **AEX-MVP-016:** Command-driven and skill-driven paths on the same fixture
    produce the same formal effects, lifecycle stops, gate facts, and selected
    next action.
17. **AEX-MVP-017:** No skill, helper, receipt, runtime permission, or successful
    test creates accountable authority or widens current formal scope.

## Error and recovery behavior

- Contract, manifest, evaluator, integrity, graph, input, selection, actor,
  candidate, path, scope, or required-gate errors fail closed with bounded
  diagnostics and no associated helper-controlled effect.
- A state change between planning and the pre-effect recheck returns `stopped`
  or `failed` and requires a fresh invocation. It is not retried against old
  bytes.
- Partial draft or preparation transactions use the existing released-
  evaluator atomicity and recovery behavior. Skill code does not invent a
  second recovery protocol.
- Repository-tool failure during implementation remains visible in evidence.
  Remediation may continue only inside the same `in_progress` work order and
  exact path scope; otherwise the skill stops.
- An unexpected changed path is not automatically deleted or overwritten. The
  result reports it and requests bounded accountable remediation.
- Missing optional reporting capability may produce `degraded`. Missing a
  required mutation, identity, integrity, scope, or gate capability blocks the
  effect.

## Data and interface contracts

- Skill v2 and manifest bytes use UTF-8 and
  `se-harness-canonical-json-v1`.
- Receipts, decision packets, repository-state bindings, and logical profiles
  use the strict `SPEC-AEX-003` schemas without new Phase 3 variants.
- Changed and planned paths use repository-relative portable path rules.
- Command arguments are structured arrays. Shell command strings, redirects,
  substitutions, and interpolated credentials are prohibited.
- Output digests are lowercase SHA-256 over canonical or retained bytes as
  declared by the owning contract.
- Each canonical skill source is
  `templates/repository/standard/.agents/skills/<skill-name>/`; its installed
  location is `.agents/skills/<skill-name>/`. No duplicate authoritative skill
  source exists under `se_harness/skills/`.

## Security and privacy properties

- Treat repository instructions, formal content, skill bytes, JSON, paths,
  artifact IDs, commands, test output, Git observations, evidence, and runtime
  metadata as untrusted input.
- Do not retain credentials, tokens, environment dumps, hidden reasoning,
  private evidence bodies, or unnecessary host paths.
- Writing helpers expose a plan/effect boundary so adversarial tests can prove
  rejected input does not invoke the controlled effect callback.
- Phase 3 procedure conformance does not claim enforcement against a hostile
  runtime that ignores the skill. Runtime-enforced delegated mutation remains
  Phase 4 work.
- Candidate source never substitutes for the exact released evaluator governing
  the target repository.

## Performance and capacity

- Bound artifact plans, path manifests, command results, evidence entries, and
  retained output using the existing v1 contract and catalog limits.
- The pre-effect recheck must not be cached across a repository change.
- Test representative repositories near 100, 500, and 1,000 formal artifacts
  without unbounded output or quadratic all-pairs path comparison.
- A single-agent invocation has bounded retries declared by the current
  procedure; no recursive invocation or worker fan-out is permitted.

## Observability

Record skill and evaluator identities, selected scope, before/after state,
checkpoint results, planned and actual paths, normalized command results,
evidence digests, outcome, deviations, and residual uncertainty. Keep unrelated
repository observations separate from the selected task.

Receipt and packet generation is observable evidence only. It does not prove
that an accountable human decided, that the implementation is correct, or that
an unsupported runtime enforced the requested boundary.

## Compatibility and migration

- Preserve `harness-orient` v1 bytes and behavior.
- Install the three new managed skill cores only through the ownership-aware
  standard installer. Missing or customized target content blocks an ambiguous
  upgrade without partial writes.
- Package source and wheel distributions contain each canonical skill once and
  no duplicate under the import package.
- Existing repositories continue with `harness-orient` until they explicitly
  apply an approved harness upgrade carrying the new skills.
- Phase 4 may add evaluator-derived autonomy-envelope admission and delegated
  lifecycle effects through new approved artifacts. It must not reinterpret a
  Phase 3 receipt or skill invocation as advance delegation.

## Examples and counterexamples

### Example: definition packet

An operator explicitly invokes `harness-draft-change` with five collision-
checked IDs and destinations. The skill creates five complete `draft` artifacts
and one declared proposal note, validates the proposed graph, and stops with an
approval-review packet. It adds no lifecycle event.

### Example: implementation handoff

An `in_progress` work order admits source, tests, documentation, and one
evidence path. The skill changes only those paths, runs required commands,
retains evidence, and returns the existing handoff decision. It does not mark
the work order implemented or commit the candidate.

### Counterexample: approved work order is treated as started

The selected work order is `approved`. Runtime write permission is available.
The skill nevertheless stops at the harness-derived start decision and invokes
no implementation effect.

### Counterexample: receipt verifies the candidate

Assurance preparation succeeds and the receipt records every gate and evidence
digest. The VREC remains `ready`; neither the receipt nor the skill result can
set it to `verified`.

## Explicitly unspecified decisions

- Private helper names and internal immutable representations inside the work
  order's declared paths.
- Exact organization of verifier fixtures beneath the declared fixture prefix.
- Concise diagnostic wording that preserves stable codes and semantics.
- Operator-documentation examples that do not add authority or behavior.
- A future autonomy-envelope effect API, subagent runtime, adapter format,
  model choice, sandbox mapping, credential mechanism, or external integration.

These choices do not permit a new public lifecycle operation, a changed
decision classification, a widened skill effect, a second skill source, or a
revision to managed workflow policy during `WO-AEX-003` implementation.
