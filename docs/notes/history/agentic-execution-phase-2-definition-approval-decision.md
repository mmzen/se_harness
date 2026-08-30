# Phase 2 Agentic Execution Definition-Approval Decision Packet

> Historical record from 2026-08-24, at `65244b1`. Kept for the decision trail; it describes the tool as it was then.

<!-- Target expertise: 8/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

- Prepared: 2026-08-24
- Selected domain: `agentic-execution`
- Selected artifacts: `SPEC-AEX-003`, `ADR-AEX-003`, and `WO-AEX-002`
- Content-review outcome: accepted by all accountable owners
- Formal lifecycle state: all three artifacts are `approved`
- Formal decision status: approved and applied
- Transition material: read-only preview passed; exact atomic application completed
- Lifecycle effect: three `draft` to `approved` transitions
- Implementation effect: none

## Purpose and authority boundary

This non-authoritative packet consolidated the inputs for the Phase 2
definition-approval decision and now records its application result. The
formal artifacts and managed lifecycle events, not this note, carry approval
authority. This packet does not authorize work-order start or start
implementation.

The accepted pre-application files and resulting approved files are bound below
by SHA-256 so a later reviewer can distinguish the reviewed content from the
expected lifecycle-metadata changes.

## Decision summary

Accountable content review is complete. The four blocking content findings are
closed, the governing Phase 1 chain is approved, the work-order scope and
assurance classification are explicit, and evaluator 0.6.0 accepts the formal
graph.

The separately authorized read-only atomic lifecycle preview passed for all
three selected artifacts with zero scoped or repository blockers and no files
written. The accountable owners then approved the three exact artifacts and
authorized only that previewed packet. Evaluator 0.6.0 applied the three
transitions atomically. Implementation start remains a separate later decision
point and was not authorized.

## Exact reviewed and approved content

The accepted content is the repository-local file content with these digests:

| Artifact | Pre-application SHA-256 | Pre-application state |
| --- | --- | --- |
| `SPEC-AEX-003` | `106cfaac2fd28cae79b952e5de9a3f5562c96862cf53bc7096d48ff4c7fd9b63` | `draft` |
| `ADR-AEX-003` | `a7eb4bce096818078a25ef7dd93b1144adffb314f5ab2d80846284ce9c65097d` | `draft` |
| `WO-AEX-002` | `5dc72f1ae6e3b995cc4fefdd175b75677c95aad3a9064a7ee1ae49c74891817e` | `draft` |

Before application, all three files contained no lifecycle event. The
repository baseline is commit `1cdc75259da8156e93ad8c32110ee196296b8cea`;
the selected candidate content is identified by its file digests rather than
claimed as content of that baseline commit.

The evaluator changed only `status`, `updated`, and `lifecycle_events`. The
resulting approved files have these current digests:

| Artifact | Approved-file SHA-256 | Current state |
| --- | --- | --- |
| `SPEC-AEX-003` | `1d93264d9a87d436d22b515e9f799f4faeb28857646a1b7890201f10e63d152b` | `approved` |
| `ADR-AEX-003` | `29e95f724316b72ce7edd109fa6aef2df6e6fb36016500cdc5364b38a601b987` | `approved` |
| `WO-AEX-002` | `f1976750ca26f584ac445afbdb7044362b439cfcbd59d2f12db092f4007241bc` | `approved` |

## Accepted accountable decisions

One person explicitly exercised each role, but the role authorities remain
separate:

| Role | Accepted content decision | Formal result or remaining authority |
| --- | --- | --- |
| Technical owner | Accept the exact public catalog, repository-state algorithm, packet projection, pure/evaluator split, and Option C in `ADR-AEX-003` | Approval lifecycle events recorded for `SPEC-AEX-003` and `ADR-AEX-003` |
| Quality owner | Accept the independent oracle, adversarial matrices, packet equivalence, and zero-effect-sentinel obligations | No separate lifecycle authority over the selected artifact types |
| Assurance owner | Accept `VER-AEX-001` as sufficient for the bounded Phase 2 verification application | Later assessment of commit-bound evidence and any resulting VREC |
| Repository owner | Accept the 13-entry execution scope and confirm commit-bound verification is `required` | Classification retained; any repository integration remains separately governed |
| Engineering owner | Accept the bounded, pure contract-layer content of `WO-AEX-002` | Approval lifecycle event recorded; implementation start remains pending |

The content decisions close `P2-CR-001` through `P2-CR-004`. The later explicit
approval and application authority changed only the three formal lifecycle
states.

## Definition and architecture closure

### `SPEC-AEX-003`

The revised specification closes the implementation-time choices that were
previously ambiguous:

- one normative catalog meta-schema and complete field catalog;
- stable `AEXCON001` through `AEXCON018` diagnostic classes;
- complete tracked plus non-ignored worktree observation and canonical
  repository-state manifest rules;
- exact workflow-result and packet-context mapping into the lossless
  `se-harness-decision-packet-v2` representation, with v1 validation
  compatibility retained; and
- a pure Phase 2 boundary that produces only `constructed` and `admissible`
  assessments from supplied observations.

### `ADR-AEX-003`

Option C is accepted in content: a later exact released-evaluator integration
is the only component allowed to collect live managed state and label an
envelope `derived` or an operation `admitted`. Canonical envelope bytes are
normally passed in memory, and declared evidence may retain digests without
turning an envelope or receipt into an authority source.

### `WO-AEX-002`

The work order is bounded to a standard-library, runtime-neutral contract
layer across 13 declared path entries. It implements catalog parsing,
canonicalization, candidate construction from supplied observations,
narrowing, pure admission assessment, packet projection, receipt validation,
portable-profile validation, tests, documentation, and retained evidence.

It excludes live repository observation, real mutation, lifecycle integration,
new commands or skills, subagent execution, runtime adapters, credentials,
network use, Git actions, publication, deployment, and release activity.

## Governing-chain and readiness evidence

| Check | Result |
| --- | --- |
| Content findings | `P2-CR-001` through `P2-CR-004` closed by explicit accountable acceptance |
| Upstream requirements | `REQ-AEX-001` through `REQ-AEX-005` are `approved` |
| Upstream specifications | `SPEC-AEX-001` and `SPEC-AEX-002` are `approved` |
| Architecture baseline | `ARCH-AEX-001`, `ADR-AEX-001`, and `ADR-AEX-002` are `approved` |
| Verification contract | `VER-AEX-001` is `approved` and accepted as sufficient for the bounded application |
| Assurance classification | `WO-AEX-002` records commit-bound verification as `required`, decided by the repository owner |
| Execution scope | 13 explicit path entries; scope expansion requires revision and renewed approval |
| Exact evaluator | Isolated released evaluator 0.6.0 |
| Formal graph | Pass: 759 artifacts, zero errors, and 50 pre-existing maintenance warnings |
| Managed integrity | Released-evaluator `doctor` passes all required and managed-integrity checks |
| Selected formal states | All three selected artifacts are `approved` with one `draft` to `approved` lifecycle event each |
| Lifecycle compatibility preview | Pass: three planned changes, compatibility pass, zero scoped blockers, zero repository blockers, and no files written |
| Applied lifecycle transaction | Pass: three transitions applied atomically with zero partial application |
| Implementation activity | None |

The 50 maintenance warnings concern existing legacy paths and architecture
metadata outside this packet. They do not alter the accepted AEX content.

## Read-only lifecycle preview — 2026-08-24

The released evaluator 0.6.0 evaluated one atomic proposal containing exactly
these three artifact and actor assertions:

| Artifact | Actual state before preview | Projected state | Actor assertion used for compatibility |
| --- | --- | --- | --- |
| `SPEC-AEX-003` | `draft` | `approved` | `technical-owner` |
| `ADR-AEX-003` | `draft` | `approved` | `technical-owner` |
| `WO-AEX-002` | `draft` | `approved` | `engineering-owner` |

The structured result reports:

```text
operation: transition
outcome: completed
checkpoint: compatibility
compatibility: pass
planned transitions: 3
scoped blockers: 0
repository blockers: 0
files written: 0
```

The planner identified only the expected future changes to `status`, `updated`,
and `lifecycle_events` in the three selected formal files. Its `state.after`
values are projections, not current state. A post-preview file check confirms
that all three actual files remain `draft`, contain no lifecycle event, and
retain the exact SHA-256 values recorded in this packet.

This technical preview is not an accountable approval assertion and creates no
authority to apply the projected changes.

## Accountable approval and atomic application — 2026-08-24

The accountable decision was:

```text
As technical owner, approve SPEC-AEX-003 and accept and approve ADR-AEX-003.
As repository owner, confirm commit-bound verification remains required for
WO-AEX-002. As engineering owner, approve WO-AEX-002 for its exact declared
scope. Authorize applying exactly the three previewed draft-to-approved
transitions. Do not start implementation or perform any external action.
```

Immediately before application, the three pre-application digests matched the
preview binding, every selected artifact was still `draft`, managed integrity
passed, and the isolated evaluator reported version 0.6.0. The exact previewed
packet was then applied with no additional artifact or target:

```text
operation: transition
outcome: completed
compatibility: pass
applied transitions: 3
scoped blockers: 0
repository blockers: 0
partial application: 0
```

Each formal file now records one lifecycle event at
`2026-08-24T11:49:36Z`. `SPEC-AEX-003` and `ADR-AEX-003` name
`technical-owner`; `WO-AEX-002` names `engineering-owner`. Post-application
graph validation and managed-integrity checks pass.

## Material tradeoffs accepted

- Exact, closed schemas make independent verification possible but make future
  public changes explicit compatibility decisions rather than informal code
  changes.
- Complete repository observation gives one reproducible later authority
  binding but can be more expensive than observing a narrow subset.
- The lossless v2 packet adds selected state and scope that v1 cannot carry;
  v1 remains compatibility input rather than the generated projection.
- The pure Phase 2 layer can prove fail-closed contract behavior without
  granting mutation authority, but live evaluator integration is deferred to a
  separately governed work order.
- Commit-bound verification adds delivery steps because this code will become
  a trusted dependency for later governed mutation.

## Effects of approval and application

- `SPEC-AEX-003` is now an authoritative definition of the Phase 2 core
  contract catalog and pure authority-assessment boundary;
- `ADR-AEX-003` makes Option C the accepted architecture decision; and
- `WO-AEX-002` is bounded implementation authority for only its
  declared pure contract-layer scope.

Implementation did not start automatically. The engineering owner still needs
a separate start decision after the required focus and start-preflight evidence
has been read.

## Explicit non-effects

The approval and application do not:

- authorize implementation or change executable source;
- derive an autonomy envelope or admit an operation;
- add or invoke a skill, subagent, worker, adapter, or mutation path;
- create a branch, commit, push, pull request, merge, release, publication, or
  deployment; or
- authorize credentials, network use, or another external action.

## Current human decision point

Content review, lifecycle preview, approval, and atomic application are
complete. `WO-AEX-002` is approved but implementation has not started.

Two accepted formal bodies still contain draft-time explanatory wording:
`ADR-AEX-003` says its lifecycle remains `draft`, and `WO-AEX-002` says the
proposal remains `draft` and awaits approval. Front-matter status and lifecycle
events are authoritative, and evaluator validation passes, but the prose now
disagrees with that state. It was not changed because the authorization covered
only the exact lifecycle fields.

The non-authoritative
[bounded consistency-correction proposal](agentic-execution-phase-2-consistency-correction-proposal.md)
now defines four exact, body-only replacements and three disposition options.
Resolve or explicitly disposition that proposal before implementation start.

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

- explicitly accept the two statements as historical draft-time context while
  keeping front-matter lifecycle state authoritative; or
- defer further Phase 2 work without changing the approved states.
