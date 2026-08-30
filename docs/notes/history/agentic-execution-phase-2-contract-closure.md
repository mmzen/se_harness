# Phase 2 Agentic Execution Contract-Closure Proposal

> Historical record from 2026-08-24, at `65244b1`. Kept for the decision trail; it describes the tool as it was then.

<!-- Target expertise: 8/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

Prepared: 2026-08-24

Selected domain: `agentic-execution`

Baseline: merged Phase 1 candidate at `1cdc752`

Formal artifacts prepared from this proposal: `SPEC-AEX-003`, `ADR-AEX-003`,
and `WO-AEX-002` (all `draft`)

Lifecycle effect: none

Implementation effect: none

## Purpose

Phase 2 turns the already-approved AEX semantic contracts into a complete,
machine-testable, runtime-neutral contract boundary. It does not implement a
mutating skill, delegate work to subagents, materialize a runtime adapter, or
change who may make an accountable decision.

This document is non-authoritative planning input. Formal authority remains in
the approved requirements, specifications, architecture, ADRs, verification
contract, and lifecycle state of `WO-AEX-002`. Accepting this proposal does not
approve the work order or authorize implementation.

## Baseline established by Phase 1

Phase 1 delivered and independently accepted the read-only `harness-orient`
pilot. The merged state provides:

- approved authority and delegation requirements `REQ-AEX-001` through
  `REQ-AEX-005`;
- approved runtime-neutral semantics in `SPEC-AEX-001` and `SPEC-AEX-002`;
- approved authority, procedure, execution, adapter, and evidence boundaries in
  `ARCH-AEX-001`, `ADR-AEX-001`, and `ADR-AEX-002`;
- the independent matrix in `VER-AEX-001`;
- strict `se-harness-skill-contract-v1` and
  `se-harness-skill-manifest-v1` behavior;
- one canonical, portable, read-only skill and receipt instance; and
- verified commit-bound evidence in `VREC-AEX-001`.

Phase 1 intentionally did not implement an autonomy envelope usable for a
write, a general decision-packet projection, a general receipt validator,
multi-agent execution, or runtime adapters.

## Phase 2 exit-criteria assessment

| Contract or criterion | Approved baseline | Closure still required |
| --- | --- | --- |
| Autonomy envelope | `se-harness-autonomy-envelope-v1` fields, narrowing invariants, stop classes, and authority limits are defined | Exact repository-state binding and authoritative derivation or storage remain explicitly deferred; strict parsing and admission behavior are not implemented |
| Decision packet | `se-harness-decision-packet-v1` shape and lossless relationship to `se-harness-workflow-result-v2` are defined | Exact field-level catalog, strict validation, canonical vectors, and semantic projection equivalence are not implemented |
| Execution receipt | `se-harness-execution-receipt-v1` shape and canonical encoding are defined; `harness-orient` emits one read-only instance | General validation, complete operation/worker coverage, mutation-bound retention rules, and negative vectors remain unimplemented |
| Portable skill profile | The pilot skill contract, manifest, canonical source, and single-agent fallback are implemented | A reusable runtime-neutral logical-profile representation and shared compatibility checks remain to be closed without adding another skill |
| Threat model | `VER-AEX-001` names malformed, stale, hostile, scope-expanding, secret-bearing, and partial-failure cases | Verifier-owned vectors and an effect sentinel must prove invalid scope cannot reach a write boundary |
| Runtime neutrality | Approved architecture separates authority, procedure, execution, adapter, and evidence planes | The executable contract layer must have no provider, model, sandbox, tool, subagent, credential, or network dependency |

The key conclusion is that the semantic model is largely approved, but the
autonomy-envelope authority binding is not fully closed. `SPEC-AEX-001`
explicitly requires an approved refinement before an envelope can be used for
autonomous mutation.

## Recommended Phase 2 decisions

### D-AEX-P2-01 — one harness-owned contract catalog

Recommendation: maintain one versioned, machine-readable catalog distributed
with the harness. It defines strict fields, types, enums, bounds, ordering, and
schema compatibility for the autonomy envelope, decision packet, execution
receipt, and logical portable profile. A standard-library module consumes that
catalog and provides parsing, canonical encoding, digesting, narrowing, and
pure admission assessment.

This avoids copying policy into skills, adapters, prompts, or provider
configuration. The catalog describes the approved AEX data contracts; managed
workflow legality remains owned by the existing workflow and quality-gate
contracts.

### D-AEX-P2-02 — evaluator-derived envelope authority

Recommendation: an autonomy envelope usable for governed mutation is derived
by the exact released evaluator from:

- one selected approved or in-progress work order;
- the canonical bytes and digest of that work order;
- the complete formal snapshot identity;
- an immutable repository-state observation defined by the refinement;
- the selected procedure and permitted operation classes;
- the exact work-order path scope narrowed by any delegated subset;
- the released-evaluator payload digest; and
- explicit evidence, writer, retry, profile, and stop boundaries.

A skill, agent, model, runtime, or caller may request a narrower envelope but
cannot author authoritative bytes or widen the evaluator-derived result. The
canonical envelope may be passed in memory and its digest retained in the
receipt. Persisting the envelope itself is allowed only at a path declared by an
approved work order or evidence obligation; persistence does not create a new
lifecycle artifact or authority source.

This recommendation materially resolves the storage-or-derivation decision
deferred by `SPEC-AEX-001`. It therefore needs an approved specification
refinement and architecture decision before implementation.

### D-AEX-P2-03 — pure contract layer before mutation integration

Recommendation: `WO-AEX-002` implements strict parsing and pure admission only.
It does not connect the envelope to `mutation_guard`, add a CLI command, or
perform a real write. Failure-before-effect is verified with an injected test
sentinel. A later Phase 3 work order must separately authorize the first real
mutation integration and skill.

This creates a testable safety boundary without allowing a draft contract to
become operational authority.

### D-AEX-P2-04 — lossless packet projection

Recommendation: a decision packet is a deterministic, decision-focused
projection of `se-harness-workflow-result-v2`. It contains exactly one primary
decision and may neither add nor remove a blocker, gate, recommendation,
complete alternative, effect, non-effect, next step, or command/response
meaning. Human output renders the same semantic packet.

### D-AEX-P2-05 — receipts remain evidence only

Recommendation: the general receipt validator requires complete requested
operation and worker coverage, even for failures, cancellation, timeout, or
missing output. It rejects authority assertions, secrets, hidden reasoning, and
unbounded host metadata. A receipt digest binds evidence but cannot approve,
verify, release, expand scope, or prove substantive correctness.

### D-AEX-P2-06 — preserve the Phase 1 pilot identity

Recommendation: shared canonical behavior may be factored only if the installed
`harness-orient` portable-core digest and public results remain unchanged. Phase
2 adds no skill and does not widen implicit activation.

### D-AEX-P2-07 — commit-bound assurance required

Recommendation: classify `WO-AEX-002` as requiring commit-bound verification.
The executable contract layer is a trusted dependency for later mutation and
decision-point behavior. Candidate self-tests alone are insufficient.

## Formalization required before work-order approval

The recommended decisions exposed one material definition gap. Draft
`SPEC-AEX-003` now defines the exact core-contract catalog, repository-state
binding, evaluator-derived envelope semantics, field bounds, and compatibility
rules. Draft `ADR-AEX-003` records the decision to derive authoritative
envelopes through the exact released evaluator, pass canonical bytes in memory
by default, and retain only declared evidence and digests. Draft `WO-AEX-002`
now traces to both artifacts; its executable scope and verification obligation
did not require expansion.

All three drafts require accountable content review. `SPEC-AEX-003` and
`ADR-AEX-003` must be approved before `WO-AEX-002` can be approved. A review
revision that changes relations, executable scope, or verification obligations
must be reflected in the work order before its approval.

No approved Phase 1 artifact should be edited in place merely to avoid this
decision. New draft artifacts preserve the approved baseline and make the new
choice reviewable.

`VER-AEX-001` already covers the required requirement families and adversarial
methods. A new verification contract is not recommended unless the formal
refinement introduces a method or acceptance obligation that cannot be stated
as a bounded `VER-AEX-001` application.

## Proposed `WO-AEX-002` boundary

The draft work order implements `REQ-AEX-001` through `REQ-AEX-005` through a
contract catalog, strict standard-library parser, canonical encoder, digest,
envelope narrowing and pure admission assessment, decision-packet projection,
general receipt validation, portable-profile validation, adversarial fixtures,
documentation, and retained evidence.

It explicitly excludes:

- real repository or lifecycle mutation;
- `mutation_guard` integration;
- new CLI or workflow operations;
- Phase 3 skills;
- VREC or RLS preparation automation;
- subagent or worker execution;
- parallel writers or worktrees;
- runtime adapters or provider files;
- credentials, network access, Git, publication, deployment, and release; and
- real-world actor authentication or cryptographic signatures.

## Verification strategy

Independent verification should use verifier-maintained semantic objects and
expected results rather than importing candidate constants as the oracle. At
minimum it should prove:

- exact canonical bytes and digests for all four contract families;
- rejection of duplicate, unknown, malformed, excessive, non-canonical, and
  hostile data;
- monotonic child-envelope restriction across every scope dimension;
- stale and mismatched identity rejection;
- zero effect-sentinel calls for every denied case;
- semantic equivalence between workflow result, decision packet, and human
  rendering;
- complete receipt coverage for successful and unsuccessful work;
- secret and hidden-reasoning exclusion;
- Phase 1 skill identity and behavior remain unchanged;
- source, package, and installed catalog parity; and
- full repository and exact released-evaluator validation.

## Human decision point

The seven recommendations have been accepted as planning input and formalized
in three draft artifacts. The next accountable action is content review of
`SPEC-AEX-003`, `ADR-AEX-003`, and the traceability-revised `WO-AEX-002`.
Starting review must not approve an artifact, apply a lifecycle transition, or
start implementation.

Recommended response:

```text
Begin accountable content review of draft SPEC-AEX-003, ADR-AEX-003, and
WO-AEX-002; keep every artifact draft and do not apply transitions or start
implementation.
```

Alternatives:

- request exact revisions to one or more draft artifacts;
- keep `WO-AEX-002` draft and defer Phase 2; or
- reject the proposed contract-closure boundary and prepare a replacement
  proposal without changing approved Phase 1 artifacts.
