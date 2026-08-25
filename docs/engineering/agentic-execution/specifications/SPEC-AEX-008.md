+++
id = "SPEC-AEX-008"
type = "specification"
title = "Delegated single-agent workflow and assurance-preparation contract"
status = "approved"
owners = ["technical-owner", "engineering-owner", "quality-owner", "repository-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
specifies = ["REQ-AEX-003", "REQ-AEX-005", "REQ-AEX-008", "REQ-AEX-012"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T09:08:48Z"
decided_by = "technical-owner"
+++

# Specification: Delegated single-agent workflow and assurance-preparation contract

## Scope

This specification defines how Phase 4 advances an approved work order through
start, admitted implementation effects, completion, and verification-record
preparation under recorded advance delegation. It defines the closed operation
catalog, delegation checks, skill/evaluator boundary, completion proof,
decision packet, and terminal stop.

It does not authorize artifact approval, verification judgment, release
judgment, delivery selection, Git mutation, credentials, network access,
publication, deployment, external actions, child delegation, multi-agent work,
or parallel writers. `DR-RLS-PREPARE` remains classified as advance-delegable
by `SPEC-AEX-001` but is not activated by the Phase 4 work orders.

## Actors and external systems

- An accountable owner approves the formal artifacts and work-order delegation.
- One logical `single-agent-executor` operates through repository skills.
- The exact released evaluator owns workflow transitions, live admission,
  effect application, evidence validation, and decision-packet projection.
- An independent verifier receives the prepared assurance packet and retains
  the verification decision.

## Closed Phase 4 operation catalog

| Operation | Decision right | Required current state | Result |
| --- | --- | --- | --- |
| `delegated-work-order-start` | `DR-WO-START` | work order `approved` | work order `in_progress` plus start receipt |
| `change-bundle-apply` | none beyond started work execution | work order `in_progress` | effect receipt and new state anchor |
| `delegated-work-order-complete` | `DR-WO-COMPLETE` | work order `in_progress` | work order `implemented` plus completion receipt |
| `delegated-vrec-prepare` | `DR-VREC-PREPARE` | work order `implemented` | ready draft verification record and decision packet |

Every operation except bundle construction runs through an evaluator operation
registered with `require_mutation_authority()`. The bundle effect additionally
runs through `SPEC-AEX-006` and `SPEC-AEX-007`.

## Inputs

- approved requirement, specification, architecture/ADR, verification, and work
  order graph required by the selected work order;
- the work order's valid Phase 4 delegation declaration;
- exact evaluator, managed lock, workflow, decision-right, and gate identities;
- live repository observations and uninterrupted effect receipts;
- declared tests, evidence paths, deviations, and residual uncertainty; and
- explicit requested operation and worker profile.

## Outputs

- evaluator workflow results and lifecycle receipts for valid delegated start
  and completion operations;
- admitted effect receipts for implementation changes;
- a draft verification record whose relations, evidence bindings, commit
  expectation, and review state are complete but undecided;
- `se-harness-decision-packet-v2` projected from the applicable workflow result;
  and
- canonical end-of-procedure state with exactly one next accountable action.

## Delegated start

Start requires approved prerequisites, work order `approved`, clean initial Git
index and worktree, valid exact evaluator and lock, no active or recovery-
required session, all start gates, and an exact unexpired `DR-WO-START`
delegation. The evaluator performs the existing managed transition, records the
work-order and delegation digests and initial observation, then creates the
single Phase 4 session.

The start receipt does not authorize paths or operations absent from the formal
delegation and does not authorize Git or external effects.

## Implementation execution

The worker receives the approved work order, relevant contracts, isolated
session workspace, exact evaluator interface, admitted logical profile, and
explicit non-effects. It may propose multiple sequential bundles within retry
and expiry limits. Each bundle receives a new envelope and must extend the
verified receipt chain.

Writing skills become evaluator clients. Their prose and host metadata may
guide the worker but cannot admit, apply, transition, or attest. They prohibit
direct target writes and stop when the released evaluator lacks Phase 4
capability, the formal delegation is absent, or canonical restitution fails.

## Delegated completion proof

`delegated-work-order-complete` requires all of the following:

- exact work-order status `in_progress` and valid `DR-WO-COMPLETE` delegation;
- no active broker operation or nonterminal journal;
- a continuous receipt chain from the start observation to a fresh stable
  current observation;
- every changed path admitted by execution scope, delegation, envelopes, and
  bundles, with no unexplained target change;
- all work-order required verification executed with normalized results;
- all applicable current gates passed;
- required evidence retained at declared paths with verified digests;
- deviations and residual uncertainty explicitly recorded; and
- no unperformed task described as complete.

The evaluator performs only the existing legal `in_progress -> implemented`
transition and records a completion receipt. Commit-bound verification remains
required when the work order says so; completion does not create or authorize a
Git commit.

## Verification-record preparation

`delegated-vrec-prepare` requires work order `implemented`, valid
`DR-VREC-PREPARE` delegation, applicable verification contract, complete
implementation evidence, exact current observation, and no recovery marker.
The evaluator creates or validates one draft verification record with:

- `verifies` relations required by the work order;
- `verifies_work_orders` containing the selected work order;
- `verification_commit` set only when a separately authorized existing commit
  is required and present, otherwise the packet names the missing action;
- normalized evidence paths and digests;
- deviations and residual uncertainty; and
- no pass, fail, waiver, or approval lifecycle event.

If a required commit does not exist, preparation stops with a canonical packet
requesting the separately authorized Git action; it does not create the commit.
After a ready verification record exists, Phase 4 stops for the independent
verification decision.

## Behavioral rules

1. **AEX-FLW-001:** Formal advance delegation is resolved for every delegated
   workflow operation; a prior successful operation supplies no standing right.
2. **AEX-FLW-002:** Rights, operations, target artifacts, outcomes, delegate,
   state, expiry, evidence, and stop boundaries must match exactly.
3. **AEX-FLW-003:** Only evaluator operations guarded by released-evaluator
   mutation authority may change lifecycle or governed repository state.
4. **AEX-FLW-004:** Skills, adapters, prompts, providers, tests, and model output
   remain non-authoritative clients and evidence sources.
5. **AEX-FLW-005:** A bundle effect is legal only while its selected work order
   is `in_progress` and its full state chain is current.
6. **AEX-FLW-006:** Completion requires positive proof of scope, gates,
   receipts, evidence, and current state; missing or not-assessable is not pass.
7. **AEX-FLW-007:** Preparation may create reviewable material but never record
   the accountable review outcome.
8. **AEX-FLW-008:** Stop before every non-delegated or reserved decision and
   before every Git, credential, network, release, delivery, or external action.
9. **AEX-FLW-009:** Produce one lossless decision packet and exactly one next
   authorized step at success, stop, or recoverable failure boundaries.
10. **AEX-FLW-010:** Restore canonical formal state and clear temporary target-
    side material before yielding; unresolved recovery blocks restitution.
11. **AEX-FLW-011:** No Phase 4 operation creates a child worker, child
    delegation, concurrent writer, or integration coordinator.
12. **AEX-FLW-012:** `DR-RLS-PREPARE` and later workflow remain disabled until a
    separate approved work order explicitly activates them.

## Decision packet and stop behavior

The packet uses approved `se-harness-decision-packet-v2` and names outcome,
done, not done, blocking condition when present, current lifecycle state,
decision right, required accountable role, exact subject, recommendation,
effects, non-effects, evidence, gates, deviations, residual uncertainty, one
next action, and an argument-vector command or exact suggested response.

At the terminal Phase 4 boundary the packet requests an independent
verification decision, or requests the separately authorized Git commit needed
before commit-bound verification can be prepared. It never recommends
publication or claims the implementation is verified.

## Error and recovery behavior

Stable errors distinguish invalid delegation, illegal transition, stale state,
session conflict, effect-chain gap, unexplained changed path, incomplete
evidence, failed or not-assessable gate, recovery-required target, invalid VREC
projection, reserved decision, prohibited action, and failed canonical
restitution. No failure is relabeled as completion or readiness.

On recoverable failure, retain receipts and evidence, restore canonical state,
and name one corrective next step. On uncertain broker recovery, stop all
workflow advancement for accountable human recovery.

## Security, privacy, performance, and observability

- Validate all formal, skill, provider, test, and receipt input as untrusted.
- Do not expose credentials, environment dumps, private content, or hidden
  reasoning in packets or evidence.
- Do not execute packet commands automatically.
- Bound one session, one worker, one broker transaction, retries, evidence size,
  and operation duration according to managed policy.
- Record exact evaluator, work order, delegation, observation, envelope, bundle,
  receipt, test, gate, lifecycle, changed-path, VREC, and decision-packet
  identities plus deviations and residual uncertainty.

## Compatibility and activation

- Preserve command-driven 0.6.0 workflow and all approved Phase 3 skill behavior
  until a successor release and explicit repository upgrade activate Phase 4.
- Existing skills receive a major contract version for the new direct-write
  prohibition and evaluator-client behavior; old skill digests remain valid
  only for their non-agentic procedures.
- Phase 4 must be built and verified using the existing released evaluator,
  then released separately, installed outside a disposable target, piloted, and
  only afterward considered for low-risk self-hosted execution.
- Multi-agent and release-preparation activation require later approved work.

## Explicitly unspecified decisions

- Provider model, prompt wording, visual presentation, and private session UI.
- Fixture and evidence subdivision inside approved prefixes.
- Whether a ready VREC is initially created through a Python API or CLI wrapper.

These choices cannot alter rights, stops, state checks, effect ownership,
completion proof, terminal boundary, or activation sequence.
