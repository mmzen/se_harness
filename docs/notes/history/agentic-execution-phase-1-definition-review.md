# Phase 1 Agentic Execution Definition-Review Decision Packet

> Historical record from 2026-08-24, at `6268821`. Kept for the decision trail; it describes the tool as it was then.

<!-- Target expertise: 8/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> **Historical review record:** Accountable content review is complete. The
> current decision point and corrected evaluator interpretation are in
> [`agentic-execution-phase-1-approval-decision.md`](agentic-execution-phase-1-approval-decision.md).
> The isolated 0.5.0 findings retained below are predecessor-compatibility
> observations, not a request to investigate or alter the 0.6.0 release records.

Prepared: 2026-08-24\
Selected domain: `agentic-execution`\
Selected formal packet: `INT-AEX-001` through `WO-AEX-001`\
Current formal state: all 16 selected artifacts are `draft`\
Packet status: non-authoritative review input\
Lifecycle effect: none

This packet records accountable content review of the Phase 1 Agentic Execution
proposal. It summarizes the decisions, records the applied revision
dispositions, and retains the earlier read-only candidate transition preview as
historical preparation evidence. It does not approve an
artifact, assert that a named person holds a role, apply a lifecycle transition,
authorize implementation, or replace the formal artifacts.

The formal packet is indexed in
[`docs/engineering/agentic-execution/README.md`](../../engineering/agentic-execution/README.md).
The planning context is
[`agentic-execution-roadmap.md`](../agentic-execution-roadmap.md).
Accountable reviewers should execute the role-specific checks in
[`agentic-execution-phase-1-accountable-review-checklist.md`](agentic-execution-phase-1-accountable-review-checklist.md).

## Primary decision

Should SE Harness adopt the proposed Agentic Execution direction as the basis
for governed implementation?

The direction is:

- the harness remains the only source of lifecycle legality, accountable
  decision rights, quality gates, and governed mutation authority;
- skills package reusable outcome-oriented procedures but do not duplicate or
  override harness policy;
- accountable roles, non-accountable execution profiles, runtime permissions,
  and model capabilities remain separate concepts;
- agents may operate autonomously only inside an explicit, narrowing autonomy
  envelope;
- accountable decisions and action-time-authorized external actions stop before
  their effects and produce one decision-ready packet for the accountable
  human;
- execution produces attributable receipts without treating receipts or
  conversation history as authority;
- every skill has a deterministic single-agent path before optional bounded
  multi-agent execution;
- runtime adapters are derived, replaceable, ownership-aware configuration;
  they cannot change formal state or authority; and
- the first implementation pilot is a read-only `harness-orient` skill.

## Recommendation

**Accountable content review is complete. Keep every artifact in `draft` and do
not prepare or apply transitions yet.**

The requested technical revisions are now incorporated: the decision-right
classification is complete, the portable source and installed location are
fixed, the digest and canonical receipt are specified, the evaluator capability
matrix has a 0.5.0 baseline, verification covers those choices, and
`WO-AEX-001` has a reconciled implementation scope.

Accountable content acceptance and the `required` commit-bound assurance
classification are now recorded in the review checklist. Lifecycle approval
has deliberately not been applied, so the draft work order retains its pending
metadata marker until a later authorized transition. The exact released
evaluator still cannot validate the repository's pre-existing 0.6.0 release
records. This condition blocks transition application, not completed content
review.

## Decision breakdown

The `D-*` labels below are local review labels only. They are not formal artifact
IDs or new decision rights.

| Review item | Formal artifacts | Accountable review | Decision requested | Recommendation |
| --- | --- | --- | --- | --- |
| `D-AEX-01` target outcome | `INT-AEX-001`, `CAP-AEX-001` | product owner and repository owner | Accept governed autonomy between accountable decisions as the product direction | Content accepted for the next lifecycle preview |
| `D-AEX-02` normative behavior | `REQ-AEX-001` through `REQ-AEX-007` | product owner and requirements steward | Accept authority separation, bounded delegation, decision packets, receipts, portable skills, read-only orientation, and bounded orchestration as observable requirements | Content accepted with the clearer decision-class vocabulary |
| `D-AEX-03` authority architecture | `SPEC-AEX-001`, `ARCH-AEX-001`, `ADR-AEX-001` | technical owner, with repository and quality review | Keep authority in formal harness contracts and make skills, profiles, agents, and adapters non-authoritative clients | Content accepted with the revised class mapping and authority boundary |
| `D-AEX-04` execution architecture | `SPEC-AEX-002`, `ARCH-AEX-001`, `ADR-AEX-002` | technical owner, with quality review | Require a complete single-agent baseline before bounded read parallelism and later isolated disjoint writers | Content accepted; multi-agent mutation remains outside the first work order |
| `D-AEX-05` verification sufficiency | `VER-AEX-001` | assurance owner and quality owner | Accept the independent black-box, failure, equivalence, security, and no-write evidence obligations | Content accepted against the closed pilot contracts and revised class names |
| `D-AEX-06` pilot authorization | `WO-AEX-001` | engineering owner and repository owner, with quality review | Approve the read-only `harness-orient` implementation boundary and commit-bound assurance classification | Content accepted with 16 paths and `required` assurance; lifecycle approval and marker replacement remain unapplied |
| `D-AEX-07` lifecycle transaction | all 16 artifacts | each accountable owner for their artifact | Apply one complete `draft -> approved` packet after all decisions and prerequisites are satisfied | Do not authorize while released-evaluator validation remains blocked; no transition authority was granted |

## Decisions that should be accepted in principle

### Harness-owned authority

Accept the choice in `ADR-AEX-001`: formal artifacts, managed policy, the
released evaluator, quality gates, and the mutation guard remain authoritative.
Skills and runtime agents consume those decisions; they do not reproduce them
as prompt rules.

This is the most important boundary in the proposal. It prevents behavior from
changing merely because an operator uses a different model, runtime, plugin,
agent definition, or permission mode.

### Single-agent baseline before orchestration

Accept the choice in `ADR-AEX-002`: every skill must work correctly through one
agent. Optional parallel execution begins with read-only work. Later concurrent
writers require disjoint scopes, isolated worktrees, bounded worker contracts,
and one integration coordinator that validates the combined repository.

This makes delegation an optimization and coverage mechanism, not a prerequisite
for correctness.

### Human at the decision point

Accept the distinction between:

- `routine-read-only`: read, calculate, validate, test, and render without a
  write or accountable decision;
- `advance-delegation-required`: a bounded operation that may run only under an
  explicit prior delegation envelope;
- `accountable-decision-required`: a current accountable product, architecture,
  assurance, release, risk, or similar decision; and
- `action-time-authorization-required`: merge, tag, publish, deploy, use
  credentials, or affect an external system.

The safe default remains `accountable-decision-required`. Technical access or
successful execution does not change the class.

## Revision disposition

### 1. Current decision-right classification — resolved in draft

`SPEC-AEX-001` now maps all 12 current managed decision rights, identifies the
accountable boundary and required evidence, and fails future unknown rights to
`accountable-decision-required`. Only WO start/completion and VREC/RLS
preparation are `advance-delegation-required`. Related-record selection is
`routine-read-only`. Definition, work selection, assurance, delivery selection,
release, and remediation are `accountable-decision-required`; external actions
are `action-time-authorization-required`. The pilot implements only the
`routine-read-only` boundary.

### 2. Portable-skill location and identity — resolved in draft

`SPEC-AEX-002`, `ARCH-AEX-001`, and `ADR-AEX-001` now select
`templates/repository/standard/.agents/skills/harness-orient/` as the canonical
source and `.agents/skills/harness-orient/` as the managed target. The retained
contract and every portable text file are bound by
`se-harness-skill-manifest-v1` using `utf8-text-lf-v1` and canonical JSON. No
duplicate `se_harness/skills/` copy is permitted. Provider adapters remain out
of scope and bind the portable digest separately if introduced later.

### 3. Minimum evaluator and reduced-capability matrix — resolved in draft

The minimum is exact released evaluator 0.5.0. Version, released identity,
doctor, validation JSON, and inspection JSON are required. Focus JSON and
explicitly requested preflight are optional. Missing focus yields a `degraded`
result with selected scope `not_assessable`; missing required behavior blocks or
fails as specified. Candidate source and ambient `PATH` discovery cannot
substitute for the structured external evaluator input.

### 4. Pilot receipt contract — resolved in draft

`SPEC-AEX-001` now defines `se-harness-canonical-json-v1`, required/empty field
behavior, SHA-256 identity, schema evolution, and retention. Orientation returns
`se-harness-execution-receipt-v1` inline and writes nothing to the target. Only a
separately authorized work order may retain the returned bytes at its evidence
path. The receipt remains non-authoritative.

### 5. Work-order body and execution scope — resolved in draft

`WO-AEX-001` now authorizes the exact canonical template directory,
`se_harness/skill_contract.py`, the existing generic installer if verifier-owned
tests require a change, package metadata, user documentation, focused package
and installation tests, and retained evidence across 16 exact paths. It removes
the publication-workflow test, speculative `skill_runtime.py`, and duplicate
Python skill directory. It explicitly excludes new CLI, workflow-policy,
adapter, subagent, and second-runtime surfaces.

### 6. Assurance classification — accountable content decision recorded

The draft retains `required`, the conservative classification for trusted
installer, managed-template, package, and agent-facing behavior. The field now
uses `pending-repository-owner-decision` rather than implying a completed
proposal-author decision. The repository owner accepted the classification for
content review. The marker remains intentionally unchanged while the work order
is `draft`; replacing it belongs to a later authorized lifecycle approval.

### 7. Resolve the governing evaluator graph blocker outside AEX

The exact released 0.5.0 evaluator passes managed-integrity checks but fails
formal validation on three existing release-history findings:

- `E009`: `RLS-SEH-009` has a status the 0.5.0 validator does not accept;
- `E010`: `RLS-SEH-009` and `RLS-SEH-012` both declare version `0.6.0`; and
- the duplicate-version finding is reported against both records.

These findings predate and are unrelated to the AEX proposal. They still block
a claim that the governing evaluator validates the graph. Resolve them through
the repository's separately governed evaluator-upgrade or release-history path;
do not hide them in the AEX work order and do not use candidate validation as a
replacement authority.

## Review sequence after revision

1. Product and requirements owners review the outcome and seven normative
   requirements.
2. The technical owner accepts or revises both ADRs, the architecture trigger
   assessment, complete decision classification, portable skill layout,
   evaluator capability matrix, canonical packet/receipt rules, and remaining
   deferred mutation decisions.
3. The assurance and quality owners review the revised `VER-AEX-001` against
   those contracts.
4. The engineering and repository owners review `WO-AEX-001`, confirm
   commit-bound verification, and decide whether its exact scope is
   implementation-ready.
5. Resolve the exact released-evaluator graph blocker outside AEX.
6. Regenerate governing validation evidence and the read-only transition
   preview from the then-current state.
7. Only then may each accountable owner authorize an actual lifecycle
   transaction through the managed procedure.

Review may proceed in parallel, but actual transition should preserve a valid
intermediate graph. Because the definitions are mutually connected, the
candidate planner recommends one explicit atomic transition packet once every
decision has been made.

## Read-only transition preview

### Evaluator boundary

| Observation | Result |
| --- | --- |
| Candidate source | `se-harness 0.6.0` |
| Exact released evaluator | `se-harness 0.5.0` |
| Preview provider | candidate source only |
| Governing status of preview | non-authoritative observation |
| `--apply` used | no |
| Files written by preview | none |

The exact released 0.5.0 evaluator does not provide `transition`. Therefore this
is a candidate-interface preview, not the governing transition gate.

### Actual state before and after the preview

The actual state remained unchanged:

| Artifact group | Artifacts | Actual state before | Actual state after |
| --- | --- | --- | --- |
| Intent and capability | `INT-AEX-001`, `CAP-AEX-001` | `draft` | `draft` |
| Requirements | `REQ-AEX-001` through `REQ-AEX-007` | `draft` | `draft` |
| Specifications | `SPEC-AEX-001`, `SPEC-AEX-002` | `draft` | `draft` |
| Architecture and decisions | `ARCH-AEX-001`, `ADR-AEX-001`, `ADR-AEX-002` | `draft` | `draft` |
| Verification | `VER-AEX-001` | `draft` | `draft` |
| Work authorization | `WO-AEX-001` | `draft` | `draft` |

### Proposed atomic transaction

The candidate planner regenerated the preview after the formal revisions and
successfully previewed these 16 proposed changes:

```text
INT-AEX-001   draft -> approved   accountable role: product-owner
CAP-AEX-001   draft -> approved   accountable role: product-owner
REQ-AEX-001   draft -> approved   accountable role: requirements-steward
REQ-AEX-002   draft -> approved   accountable role: requirements-steward
REQ-AEX-003   draft -> approved   accountable role: requirements-steward
REQ-AEX-004   draft -> approved   accountable role: requirements-steward
REQ-AEX-005   draft -> approved   accountable role: requirements-steward
REQ-AEX-006   draft -> approved   accountable role: requirements-steward
REQ-AEX-007   draft -> approved   accountable role: requirements-steward
SPEC-AEX-001  draft -> approved   accountable role: technical-owner
SPEC-AEX-002  draft -> approved   accountable role: technical-owner
ARCH-AEX-001  draft -> approved   accountable role: technical-owner
ADR-AEX-001   draft -> approved   accountable role: technical-owner
ADR-AEX-002   draft -> approved   accountable role: technical-owner
VER-AEX-001   draft -> approved   accountable role: assurance-owner
WO-AEX-001    draft -> approved   accountable role: engineering-owner
```

Observed candidate result:

- operation outcome: `completed`;
- compatibility result: `pass`;
- planned transitions: 16;
- scoped blockers: 0;
- repository blockers seen by the candidate planner: 0;
- proposed fields per artifact: `status`, `updated`, and `lifecycle_events`;
- explicit result: `Planned 16 explicit lifecycle transition(s); no files were written.`

The zero candidate-planner blockers do not erase the released-evaluator
validation failure described above.

### Reproducible preview command

The following PowerShell command is intentionally read-only. It uses synthetic
`PENDING-*` actor assertions so the output cannot be mistaken for an accountable
approval. It intentionally omits `--apply`.

```powershell
$transitionArgs = @(
  '-m', 'se_harness', 'transition', '.',
  '--set', 'INT-AEX-001=approved',  '--decision', 'INT-AEX-001=PENDING-product-owner',
  '--set', 'CAP-AEX-001=approved',  '--decision', 'CAP-AEX-001=PENDING-product-owner',
  '--set', 'REQ-AEX-001=approved',  '--decision', 'REQ-AEX-001=PENDING-requirements-steward',
  '--set', 'REQ-AEX-002=approved',  '--decision', 'REQ-AEX-002=PENDING-requirements-steward',
  '--set', 'REQ-AEX-003=approved',  '--decision', 'REQ-AEX-003=PENDING-requirements-steward',
  '--set', 'REQ-AEX-004=approved',  '--decision', 'REQ-AEX-004=PENDING-requirements-steward',
  '--set', 'REQ-AEX-005=approved',  '--decision', 'REQ-AEX-005=PENDING-requirements-steward',
  '--set', 'REQ-AEX-006=approved',  '--decision', 'REQ-AEX-006=PENDING-requirements-steward',
  '--set', 'REQ-AEX-007=approved',  '--decision', 'REQ-AEX-007=PENDING-requirements-steward',
  '--set', 'SPEC-AEX-001=approved', '--decision', 'SPEC-AEX-001=PENDING-technical-owner',
  '--set', 'SPEC-AEX-002=approved', '--decision', 'SPEC-AEX-002=PENDING-technical-owner',
  '--set', 'ARCH-AEX-001=approved', '--decision', 'ARCH-AEX-001=PENDING-technical-owner',
  '--set', 'ADR-AEX-001=approved',  '--decision', 'ADR-AEX-001=PENDING-technical-owner',
  '--set', 'ADR-AEX-002=approved',  '--decision', 'ADR-AEX-002=PENDING-technical-owner',
  '--set', 'VER-AEX-001=approved',  '--decision', 'VER-AEX-001=PENDING-assurance-owner',
  '--set', 'WO-AEX-001=approved',   '--decision', 'WO-AEX-001=PENDING-engineering-owner',
  '--json', '--result-schema', '2'
)
python @transitionArgs
```

An apply command is deliberately omitted. If the packet is later approved,
regenerate the preview from the then-current repository, substitute actual
accountable actor assertions through the authorized procedure, and obtain
separate transition authority.

## Complete decision alternatives

### Alternative A: retain the completed content review in draft — current

Keep every artifact in `draft` while the repository resolves the exact
released-evaluator blocker through separate governance.

Expected effects:

- the revised design retains its recorded role-appropriate content acceptance;
- no implementation starts;
- no lifecycle event is recorded; and
- transition remains unavailable until the graph is governable and every owner
  decision is explicit.

### Alternative B: approve the packet after governing validation

After resolution of the evaluator blocker, each owner may separately approve
their artifacts and authorize one exact atomic transition packet.

Expected effects:

- the 15 definitions and one work order become `approved`;
- `WO-AEX-001` authorizes only its exact bounded read-only pilot;
- implementation still does not begin until successful start preflight; and
- Git, assurance, release, runtime-adapter, subagent, network, credential, and
  external actions remain unauthorized.

### Alternative C: reject part or all of the direction

Reject only the affected artifacts with an exact reason and identify whether
dependent drafts should be revised, superseded later, or rejected as well. Do
not apply a blanket rejection when the concern is limited to the pilot scope or
one architecture decision.

Expected effects:

- rejected artifacts cannot authorize implementation;
- dependent artifacts remain draft or require explicit disposition; and
- a replacement direction requires a new coherent formal chain.

## Suggested accountable responses

### Recommended response now

```text
Accountable content review of the revised Phase 1 AEX packet is complete. Keep
all 16 artifacts in draft. Resolve the governing 0.5.0 evaluator graph blocker
through a separate release-history or evaluator-upgrade decision. Do not
prepare or apply an AEX transition until that blocker is resolved and separate
preview authority is granted.
```

### Approval responses after governing review and validation

These responses express decisions but do not themselves run a transition:

```text
Product owner: Approve INT-AEX-001 and CAP-AEX-001.
Requirements steward: Approve REQ-AEX-001 through REQ-AEX-007.
Technical owner: Accept ADR-AEX-001 and ADR-AEX-002 and approve SPEC-AEX-001,
SPEC-AEX-002, and ARCH-AEX-001.
Assurance owner: Approve VER-AEX-001.
Engineering owner: Approve the revised WO-AEX-001 for its exact bounded scope.
Repository owner: Confirm commit-bound verification is required for WO-AEX-001
and authorize only the exact reviewed lifecycle transaction.
```

Actual actor identities and authority must be established outside this packet.
Role labels and runtime profiles are not proof of identity.

## Evidence available after revision

| Check | Result |
| --- | --- |
| Candidate 0.6.0 graph validation | pass: 688 artifacts, 0 errors, 50 pre-existing maintenance warnings |
| Focused artifact, traceability, ADR, documentation, assurance, and workflow tests | pass: 60 tests, 1 skipped |
| Instruction architecture, onboarding, publication-boundary, and source-distribution tests | pass: 50 tests |
| Expanded baseline including standard repository lifecycle | 128 passed, 1 skipped, 1 host-environment `RID018` failure because system Python exposes old 0.4.1 distribution metadata outside the checkout |
| `git diff --check` | pass |
| Exact released 0.5.0 managed-integrity doctor | pass |
| Exact released 0.5.0 graph validation | fail: three pre-existing `RLS-SEH-009`/`RLS-SEH-012` governance findings |
| Fresh post-review transition preview | not run; not authorized by this review |
| Actual AEX lifecycle states | all remain `draft` |

## Current handoff

**Completed:** Closed accountable content review, applied the accepted taxonomy
and 16-path scope revisions, and revalidated the exact draft packet.

**Current lifecycle state:** Every selected AEX artifact remains `draft`.

**Recommended next step:** Use the current Phase 1 approval decision packet to
make or defer the exact 16-artifact lifecycle decision.

**Human decision or approval required:** Explicit authorization to apply the
exact reviewed atomic transaction. No AEX content revision or release-history
investigation is required by this historical record.

**Command or suggested response:** See
`agentic-execution-phase-1-approval-decision.md`. Do not apply a transition
without the exact accountable response recorded there.
