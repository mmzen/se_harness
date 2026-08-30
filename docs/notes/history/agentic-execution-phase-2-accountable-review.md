# Phase 2 Agentic Execution Accountable Content Review

> Historical record from 2026-08-24, at `65244b1`. Kept for the decision trail; it describes the tool as it was then.

<!-- Target expertise: 8/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

- Prepared: 2026-08-24
- Selected artifacts: `SPEC-AEX-003`, `ADR-AEX-003`, and `WO-AEX-002`
- Selected domain: `agentic-execution`
- Formal lifecycle state: all three artifacts are `approved`
- Review status: accountable revised content accepted; lifecycle approval applied atomically
- Lifecycle effect of this review record: none
- Implementation effect: none

## Purpose and authority boundary

This non-authoritative review record evaluates whether the three Phase 2 drafts
are complete enough for accountable approval and later independent
implementation. It records accountable content-review decisions but does not
approve or revise a formal artifact, authorize a lifecycle transition, or start
implementation.

The review uses the approved Phase 1 requirements, specifications,
architecture, ADRs, and `VER-AEX-001` as its authority baseline. The earlier
acceptance of the seven Phase 2 recommendations authorized preparation and
review of drafts only; it did not predetermine the content-review outcome.

## Entry evidence

| Check | Result |
| --- | --- |
| Selected metadata | All three selected artifacts contain `status = "draft"` and no lifecycle event. |
| Exact released evaluator | Isolated evaluator 0.6.0 is used from outside candidate source. |
| Managed integrity | Released-evaluator `doctor` passes every required and managed-integrity check. |
| Formal validation | Pass: 759 artifacts, zero errors, and 50 existing maintenance warnings. |
| Work-order focus | `WO-AEX-002` is reported as `draft`; no related transition is automatic. |
| Formal mutation during review | None. The selected formal files were read but not revised by this review. |
| Transition or implementation activity | None. No preview, apply, implementation command, Git action, credential use, network action, or external action was performed. |

The 50 maintenance warnings concern existing legacy locations and architecture
metadata outside this Phase 2 packet. They do not change the content findings
below. Unrelated worktree changes are excluded from the review.

## Initial review outcome

| Artifact | Facilitator recommendation | Reason |
| --- | --- | --- |
| `SPEC-AEX-003` | `revision-requested` | Four public contract decisions remain underspecified and would otherwise be selected during implementation. |
| `ADR-AEX-003` | `content-accepted-in-principle`, dependent on revision | Evaluator-derived authority with evidence-only persistence is the correct architecture direction, but the pure-library/evaluator boundary must be made exact. |
| `WO-AEX-002` | `revision-requested`, dependent on specification closure | The proposed pure contract scope is appropriately narrow, but its deliverable language must match the final derivation boundary and exact normative catalog. |

These were facilitator recommendations for the accountable reviewers, not
recorded role decisions. At that point, none of the three artifacts was ready
for a lifecycle preview while the blocking findings remained open.

## Blocking revision requests

### `P2-CR-001` — make the contract catalog normatively complete

- Affected artifacts: `SPEC-AEX-003`, then `WO-AEX-002` if its deliverables
  change
- Accountable review: technical owner, quality owner, and repository owner

`SPEC-AEX-003` says the future catalog defines the complete field tree, scalar
types, nullability, enums, collection semantics, and bounds. The specification
itself does not yet provide that complete definition. It gives resource bounds
and high-level shapes, while leaving implementation to choose entry structures,
field-level types, enum members, null handling, ordering, duplicate rules, and
several compatibility details.

This is material because `WO-AEX-002` expressly prohibits choosing a public
schema or widening a field during implementation. Independent verification
also cannot create canonical vectors without an implementation-independent
oracle.

Required result:

- add a normative field catalog or appendix for the autonomy envelope,
  repository-state binding, decision packet, execution receipt, and reusable
  logical profile;
- define every object and collection entry, required and nullable field,
  scalar type, enum, bound, identity key, ordering rule, duplicate rule, and
  compatibility identifier;
- state whether the logical profile is a separate schema or a closed reusable
  object inside `se-harness-skill-contract-v1`;
- define stable diagnostic classes precisely enough for independent negative
  vectors; and
- ensure the eventual machine-readable catalog is a direct encoding of the
  approved specification rather than a new design authority.

### `P2-CR-002` — specify the repository-state manifest algorithm exactly

- Affected artifacts: `SPEC-AEX-003` and `ADR-AEX-003`
- Accountable review: technical owner and repository owner, with quality review

The state-binding object is clear at its outer level, but
`worktree_state_sha256` is described as a digest of state "needed by the
selected procedure" with Git observations included "when applicable." Those
phrases do not determine one reproducible byte sequence.

Required result:

- choose and name the observation scope: complete visible repository state or
  an exact dependency-closed subset;
- define the manifest schema and canonical bytes being hashed;
- define handling for tracked, staged, unstaged, deleted, renamed, untracked,
  ignored, executable, symlink/junction, submodule, and case-colliding entries;
- define the content-byte and mode rules, path normalization, ordering, empty
  repository behavior, and unsupported Git object or entry behavior;
- define how the formal snapshot and managed lock are identified without
  self-reference; and
- state which concurrent change invalidates admission and how a fresh
  observation is compared before a later effect.

The recommended Phase 2 default is a complete, non-ignored repository
observation plus every tracked path, with `.git` internals excluded and Git
index/worktree state represented explicitly. A narrower dependency-closed
observation is viable only if all dependencies and invalidation rules are
enumerated in the specification.

### `P2-CR-003` — define the lossless decision-packet projection field by field

- Affected artifact: `SPEC-AEX-003`
- Accountable review: technical owner, quality owner, and assurance owner

The draft lists the meanings that projection must preserve, but it does not map
the exact `se-harness-workflow-result-v2` fields into
`se-harness-decision-packet-v1`. Several packet facts, such as candidate and
evaluator identity or evidence digests, are not necessarily present in every
workflow result. Implementers would have to decide whether to use `null`, stop,
or obtain a separate input.

Required result:

- provide an exact source-to-target mapping for every packet field;
- define the permitted separately supplied identity and evidence bindings;
- define behavior when the workflow result has no decision, conflicting
  decisions, no complete alternative, or missing identity evidence;
- state which arrays are ordered sequences and which are normalized sets;
- define the semantic-equivalence oracle for JSON and human rendering; and
- prove that a projection cannot add a recommendation or hide a blocker,
  failed/not-assessable gate, effect, non-effect, next step, or command/response.

### `P2-CR-004` — separate pure construction from authoritative derivation

- Affected artifacts: `SPEC-AEX-003`, `ADR-AEX-003`, and `WO-AEX-002`
- Accountable review: technical owner, engineering owner, and repository owner

The drafts correctly reserve authoritative envelope derivation for the exact
released evaluator. They also correctly restrict `WO-AEX-002` to a pure module
with no filesystem, Git, workflow command, mutation-guard, or real effect
integration. The current wording nevertheless asks the Phase 2 output to derive
repository state and produce a `derived` envelope, which requires precisely the
evaluator integration excluded from the work order.

Required result:

- keep the accepted pure Phase 2 boundary;
- define pure functions as validating and canonicalizing explicitly supplied
  observations, constructing a candidate binding/envelope, narrowing it, and
  assessing admission without claiming authority;
- reserve the `derived` authority label for a later evaluator orchestration
  path that obtains current managed observations and invokes those pure
  functions;
- make tests use verifier-owned observation fixtures and an effect sentinel,
  not live mutation or an implied authority source; and
- revise `WO-AEX-002` wording only where needed so it does not claim to deliver
  the separately deferred evaluator integration.

If Phase 2 is instead intended to implement released-evaluator orchestration,
the work-order execution scope and accepted no-integration recommendation would
need material reconsideration. That is not the recommended resolution.

## Revision disposition — 2026-08-24

The reviewer accepted all four bounded revision requests. The formal drafts
were revised without changing lifecycle metadata:

| Finding | Draft disposition |
| --- | --- |
| `P2-CR-001` | Closed in draft: `SPEC-AEX-003` now defines the catalog meta-schema, shared scalar/path rules, every schema field tree and compatibility variant, logical-profile schema, collection ordering, and the closed `AEXCON001` through `AEXCON018` diagnostic set. |
| `P2-CR-002` | Closed in draft: the specification now selects a complete tracked plus non-ignored worktree observation, defines every manifest entry and Git/index edge case, fixes formal/lock/work-order digests, and requires two identical observations before later derivation. |
| `P2-CR-003` | Closed in draft: the specification now defines `se-harness-decision-packet-context-v1`, an exact source-to-target map, complete alternative and preview shapes, and deterministic human equivalence. Because v1 cannot carry selected state and scope, the generated packet is the compatible new `se-harness-decision-packet-v2`; v1 remains validation-only compatibility. |
| `P2-CR-004` | Closed in draft: Phase 2 returns only non-authoritative `constructed` and `admissible` outcomes from supplied typed observations. A later separately authorized released-evaluator integration alone may collect live state and label bytes `derived` or an operation `admitted`. |

`ADR-AEX-003` and `WO-AEX-002` were revised only to align with this pure
boundary and the exact schema/verification obligations. Their selected
architecture option, execution paths, assurance classification, and exclusion
of implementation effects did not change.

The findings and resulting revised content were subsequently accepted by all
accountable owners in the decision recorded below. The formal artifacts remain
draft, and any lifecycle decision remains a separate, future action.

## Accountable content decision — 2026-08-24

The user explicitly acted as technical, quality, assurance, engineering, and
repository owners and accepted the revised content of `SPEC-AEX-003`,
`ADR-AEX-003`, and `WO-AEX-002`.

That decision:

- closes `P2-CR-001` through `P2-CR-004` as content-review findings;
- accepts Option C in `ADR-AEX-003`, including the pure contract layer and the
  separately deferred released-evaluator orchestration boundary;
- confirms that `WO-AEX-002` contains only the pure contract-layer scope,
  leaves no public contract or architecture decision to its implementer, and
  retains commit-bound verification as `required`;
- confirms that `VER-AEX-001` is sufficient for the bounded verification
  application described by `WO-AEX-002`;
- confirms the independent-oracle, stale-state, narrowing, packet-equivalence,
  zero-effect-sentinel, and Phase 1 regression obligations; and
- preserves the separation of the five accountable role authorities even
  though one person exercised all five roles for this decision.

This is a content-review decision only. It does not approve any formal
lifecycle state, prepare or apply a transition, authorize work-order start,
start implementation, or authorize a Git, network, credential, or external
action.

## Non-blocking review conclusions

- The selected ADR option is sound: authority remains harness-owned, callers
  can only narrow, and persistence does not create authority.
- Evidence-only persistence is compatible with the approved Phase 1 receipt
  boundary and avoids creating an ephemeral formal-artifact class.
- Mandatory stops for accountable decisions and action-time external authority
  remain intact.
- The work order correctly excludes a new skill, CLI command, mutation guard,
  lifecycle transition, runtime adapter, subagent execution, parallel writers,
  credentials, network use, Git action, and external effect.
- Commit-bound verification should remain `required` because this module will
  become a trusted dependency for later governed mutation.
- The declared implementation paths are sufficient for the recommended pure
  module if `P2-CR-004` is resolved without evaluator integration.
- Existing `VER-AEX-001` provides the applicable independence, adversarial,
  canonical-vector, failure-injection, security, performance, and manual-review
  methods. A new verification artifact is unnecessary if the revisions above
  remain expressible as bounded applications in `WO-AEX-002`.
- Preserving the exact Phase 1 `harness-orient` portable-core identity remains
  an appropriate regression constraint.

## Accountable review checklist

### Technical owner

- [x] Decide the complete public field catalog in `P2-CR-001`.
- [x] Decide the exact repository-state observation and manifest algorithm in
  `P2-CR-002`.
- [x] Decide the exact decision-packet mapping in `P2-CR-003`.
- [x] Confirm the pure-library/evaluator-orchestration split in `P2-CR-004`.
- [x] Accept or reject Option C in `ADR-AEX-003` after those revisions.

### Quality and assurance owners

- [x] Confirm every public field and error class has an independent oracle.
- [x] Confirm stale-state and narrowing matrices cover every scope dimension.
- [x] Confirm packet equivalence is testable without importing candidate
  projection constants.
- [x] Confirm denied inputs make zero effect-sentinel calls.
- [x] Confirm `VER-AEX-001` remains sufficient after revision or request one
  exact additional verification artifact.

### Engineering and repository owners

- [x] Confirm `WO-AEX-002` implements only the pure contract layer.
- [x] Confirm its execution scope remains complete after the wording revision.
- [x] Confirm no public or architecture decision is left to the implementer.
- [x] Confirm commit-bound verification remains `required`.
- [x] Confirm Phase 1 skill identity and behavior remain unchanged.

The completed boxes record the accountable content-review conclusions. They do
not approve an artifact lifecycle state or create implementation authority; the
explicit accountable decision above controls their meaning.

## Current decision point

Accountable content review is complete, and the non-authoritative
[Phase 2 definition-approval decision packet](agentic-execution-phase-2-definition-approval-decision.md)
has been prepared. All three formal artifacts remain draft, no transition has
been prepared or applied, and implementation has not started.

The separately authorized read-only lifecycle compatibility assessment passed
for exactly the three selected artifacts with zero blockers and no files
written. The accountable owners then approved the exact packet, and evaluator
0.6.0 applied all three transitions atomically. Implementation has not started.

The next decision is how to disposition the stale draft-time explanatory prose
that remains in `ADR-AEX-003` and `WO-AEX-002` after their authoritative
front-matter lifecycle states changed to `approved`. The
[bounded consistency-correction proposal](agentic-execution-phase-2-consistency-correction-proposal.md)
defines the exact body-only correction and alternatives.

Recommended response:

```text
As technical owner, authorize exactly the proposed body-only correction to
ADR-AEX-003. As engineering owner, authorize exactly the three proposed
body-only corrections to WO-AEX-002. As repository owner, confirm that all
front matter, lifecycle state, relations, assurance, and execution scope must
remain unchanged. As quality owner, accept the corrections as non-semantic.
Apply only those four replacements, validate them, and stop. Do not start
implementation or perform any Git, network, or external action.
```

Alternatives:

- retain the accepted drafts without further action;
- reopen a named content finding with an exact revision request; or
- explicitly accept the statements as historical draft-time context; or
- defer further Phase 2 work without changing the approved states.
