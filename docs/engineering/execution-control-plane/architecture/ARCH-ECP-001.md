+++
id = "ARCH-ECP-001"
type = "architecture"
title = "The execution control plane: state in the harness, enforcement at Git boundaries"
status = "approved"
owners = ["technical-owner", "repository-owner"]
created = "2026-08-27"
updated = "2026-08-28"

[relations]
addresses = ["REQ-ECP-001", "REQ-ECP-002", "REQ-ECP-006", "REQ-ECP-007", "REQ-ECP-008", "REQ-ECP-009", "REQ-ECP-010", "REQ-ECP-011", "REQ-ECP-016", "REQ-ECP-017", "REQ-ECP-018", "REQ-ECP-020", "REQ-ECP-022"]
conforms_to = ["SPEC-ECP-001", "SPEC-ECP-003", "SPEC-ECP-004", "SPEC-ECP-005", "SPEC-ECP-006", "SPEC-ECP-009", "SPEC-ECP-011"]

[decision_assessment]
outcome = "adr_required"
triggers = ["system-boundary", "public-interface-or-protocol", "security-privacy-or-trust-boundary", "concurrency-consistency-reliability-or-failure-strategy", "cross-cutting-policy", "difficult-to-reverse", "material-alternatives"]
rationale = "The architecture moves the write boundary from a proposed-workspace broker to Git, adds a public command and result members, replaces free-text decision actors with verified identities, removes an execution model that approved artifacts still describe, and chooses one kernel over three engines. Each is a boundary or protocol change with a considered alternative and a cost to reverse once consumers upgrade."
assessed_by = "technical-owner"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T12:03:40Z"
decided_by = "technical-owner"
reason = "Approved on 2026-08-28 by the accountable owner, 'I approve the ECP definitions and WO-ECP-005', as part of the execution-control-plane definition packet of #231 with the issue #212 amendments of #238 applied. Approval of a definition authorizes no work; each work order is approved separately."
+++

# Architecture: The execution control plane: state in the harness, enforcement at Git boundaries

## Context and scope

The 2026-08 agentic execution review found that the kernel (`focus`,
`check`, `transition`, schema 2, commit-bound records) is sound at the
interface and that the guarantees which fail are the ones that ask the agent
to carry state or to be trusted: hand-typed change sets
(`se_harness/workflow_compliance.py:316-322`), a free-text decision actor
(`se_harness/workflow.py:606`), a CI scope check that runs only with a
volunteered trailer
(`templates/repository/standard/.github/workflows/engineering-harness.yml:56-89`),
and a Phase 4 broker that re-implements a version-control write boundary
inside the process and still stops before Git
(`docs/notes/agentic-execution-review-2026-08.md`, section 5, weakness 3).
This architecture assigns the eleven addressed requirements to ten
components, nine of which exist today, so that the harness owns state and
the boundary, and the agent owns only the work. The addressed set excludes
the routine requirements of `SPEC-ECP-002` and `SPEC-ECP-007`; they shape no
boundary.

## Components and responsibilities

### Kernel (`workflow.py`, `workflow_contract.py`, `workflow_result.py`, `workflow_compliance.py`)

Owns `select_rule`, `select_current_step`, `_gate_results`, `build_result`,
and `TransitionPlan`. After `SPEC-ECP-005` it is the only rule selector,
the only result builder, and the only precondition engine
(`ECP-KRN-001` to `ECP-KRN-010`). Addresses `REQ-ECP-009`, `REQ-ECP-010`.

### Next projection (`workflow_compliance.py`, `preflight.py`, `cli.py`)

Composes `focus_schema2` (`se_harness/workflow_compliance.py:551`),
`run_preflight` (`se_harness/preflight.py:321`), and `select_current_step`
into one read-only result carrying `context` (`ECP-NXT-001` to
`ECP-NXT-008`). Holds no rule of its own. Addresses `REQ-ECP-001`.

### Git change-set reader (`workflow_compliance.py`, shared Git wrapper)

Derives the change set from `git diff --name-only BASE` plus untracked
files, normalises with `normalize_path`
(`se_harness/workflow_compliance.py:71`), and feeds `CheckpointContext`
(`ECP-CHG-001` to `ECP-CHG-006`). Addresses `REQ-ECP-002`.

### Chain-scoped snapshot (`workflow_compliance.py`)

Computes `chain_snapshot_sha256` over `project_scope`
(`se_harness/workflow.py:304`) output with `formal_snapshot_digest`
(`se_harness/workflow_compliance.py:185`) so a merge elsewhere does not
invalidate handoff evidence (`ECP-SNP-001` to `ECP-SNP-004`). Addresses
`REQ-ECP-016`.

### Evidence writer (`cli.py`, `workflow_compliance.py`; `SPEC-ECP-002`)

Writes and rebinds packet headers through the journaled writer. Not an
addressed driver; listed because the CI gate reads its output.

### Identifier allocator (`artifact_layout.py`; `SPEC-ECP-002`)

Allocates across `git for-each-ref`. Not an addressed driver.

### PR-body renderer (`github_ci.py`; `SPEC-ECP-002`)

Emits the trailer and restitution line that the CI gate parses with
`select_work_order` (`se_harness/github_ci.py:49`). Not an addressed driver.

### CI gate (managed workflow, `github_ci.py`, `workflow_result.py`)

Runs the handoff check on the pull-request difference unconditionally and
fails on `WEX201` (`ECP-GTE-001` to `ECP-GTE-007`); the digest preimage
covers the change set and gate statuses (`ECP-DIG-001` to `ECP-DIG-004`).
Addresses `REQ-ECP-006`, `REQ-ECP-007`.

### Decision verifier (new `decision_record.py`, `workflow.py`)

Parses decision records, verifies the signer against the configured source,
and checks role against right (`ECP-DEC-001` to `ECP-DEC-010`); also serves
the delegated-actor route behind the CI gate (`ECP-DLG-001` to
`ECP-DLG-009`). Addresses `REQ-ECP-008`, `REQ-ECP-011`.

### Journaled writer (`effect_broker.py` reduced, `workflow.py`)

The retained journal, rollback, archive, and `human-recovery-stop` of
`apply_change_bundle` (`se_harness/effect_broker.py:800`, `:1029-1160`),
shared by every harness-owned multi-file write (`ECP-JNL-001` to
`ECP-JNL-006`). The envelope apparatus around it is removed (`ECP-DLG-008`).
Addresses `REQ-ECP-017`, `REQ-ECP-018`.

### Product boundary (`hash_bound.py`, `installer.py`, `repository_tools/`; `SPEC-ECP-007`)

Keeps self-hosting machinery out of the wheel. Not an addressed driver; it
constrains what the components above may import.

## Dependency direction

```text
WORKFLOW.json + QUALITY_GATES.json + .engineering-harness.toml
        |
        v
      kernel: select_rule -> select_current_step -> _gate_results -> build_result
        |            ^                    ^                 |
        |            |                    |                 v
  next projection    |          Git change-set reader   result_sha256
        |            |          chain-scoped snapshot        |
        v            |                    ^                 v
  reading manifest   |                    |          CI gate (pull request)
                     |                    |                 |
   decision verifier +--- transition -----+                 | conclusion
        ^                    |                              v
        |                    v                    delegated-actor route
   identity source     journaled writer  <------------------+
   (signature/actor)         |
                             v
                   artifacts, evidence packets, decision copies
```

Nothing below the contracts defines a rule. `next`, `check`, and
`transition` are three renderings of one kernel evaluation. The CI gate and
the decision verifier consume Git facts; neither consumes agent
declarations. The journaled writer is the only component that replaces
files.

## Data and control flow

1. An owner approves a work order carrying scope, assurance class, and
   optionally `[delegation]`; the decision is a verified record.
2. The agent runs `next`; the kernel selects the artifact, projects the
   chain, computes the manifest and the exact next argv, and returns them in
   one schema-2 result with `context`.
3. The agent works on a branch. No harness state is carried in the agent's
   context beyond the work-order id.
4. The agent runs `check --checkpoint handoff --from-git BASE`; the Git
   reader derives the change set; the kernel evaluates the handoff gates
   against the chain-scoped snapshot; `evidence` writes or rebinds the
   packet; the result carries `result_sha256` over change set and gates.
5. `pr-body` emits the trailer and restitution line; the pull request is
   opened.
6. The CI gate recomputes the same check at the head over `base.sha..HEAD`
   and fails on any out-of-scope path or gate failure.
7. An owner signs a decision record; `transition --apply` verifies signer
   and role, evaluates the `transition` checkpoint gates through
   `_gate_results`, and applies through the journaled writer. Where the work
   order declares `class = "execution"`, the delegated actor may apply the
   three unlocked transitions once the gate conclusion is `success`.
8. `capture-verification` and `prepare-release` are unchanged in role and
   bind a merge-reachable commit.

## Trust boundaries

- **Trusted:** Git facts (diff, untracked list, refs, commit signatures,
  `HEAD`), the released evaluator's own computation, the installed contracts
  hash-bound in the lock, and the CI status source's signed API response.
- **Untrusted:** every agent declaration (`--changed-path`,
  `--changes-complete`, evidence body text, a typed actor string), the
  pull-request body (parsed, never trusted; the work-order id it names is
  validated against the graph), environment variables other than
  `GITHUB_ACTOR` in a GitHub-hosted job, and any JSON passed to a writer.
- **Boundary rule:** enforcement runs where an agent cannot bypass it: the
  pull-request gate for scope and gates, the decision verifier for
  authority, the journaled writer for consistency. A proposed-workspace
  broker inside the process is not such a boundary and is removed
  (`ADR-ECP-002`).

## Required patterns

- One kernel evaluation per command; commands are renderings.
- Additive schema-2 extension; the schema identifier never changes for an
  additive member.
- Fail-closed predicates with `pass`, `fail`, or `not_assessable`; a Git
  source removes `not_assessable` from completeness, never from scope.
- Every multi-file write is staged, journaled, applied in order, and either
  committed or rolled back; a failed rollback stops for a human.
- Decision authority is a verified identity plus a role holding the right;
  the lifecycle event records the record digest.
- Delegation is a work-order attribute read from the graph and unlocked by
  the gate's conclusion for a named head.
- The evaluator installed from the lock runs every CI evaluation.

## Prohibited patterns

- Command-private precondition sets: no command evaluates a gate outside
  `_gate_results`, and no Python check duplicates a predicate the gate
  contract can express.
- Agent-typed change sets as sole scope evidence: `--changed-path` may
  never satisfy `QGP-G4I-PATHS` in CI, and after the compatibility window
  not locally either.
- Unauthenticated decision actors: no transition applies on a role string
  alone; no default identity source; no honour-based fallback once the
  table exists.
- Envelope tokens: no nonce, lifetime, revocation, retry ordinal, or
  stability observation in the product CLI or public API.
- A second result schema, a second rule selector, or a second next-step
  computation anywhere, including skills and prose.
- Product code that names this repository's own release records.
- Inferring a work order, a base, or a delegation from branch names,
  commit messages, or environment variables.

## Quality attributes

- **Determinism:** the same tree, base, and contracts yield byte-identical
  `next`, `check`, and CI blocks and one `result_sha256`.
- **Enforceability:** scope and gate outcomes are decided by the CI gate on
  Git facts; authority by verified identity; both survive an agent ignoring
  every instruction.
- **Boundedness:** the reading set is the router, the card, a 2048-byte
  command block, and the chain; the agent-carried state is one identifier.
- **Consistency:** `check` and `transition` cannot disagree; multi-file
  writes are atomic or stopped.
- **Isolation:** two agents on two work orders are two branches; a merge
  outside the chain does not move `chain_snapshot_sha256`.
- **Portability:** standard library only; no provider marker; a fresh
  consumer passes `doctor`.

## Conformance checks

- `ECP-NXT-004`, `ECP-KRN-003`, and `ECP-KRN-007` equality tests across
  commands.
- `ECP-DIG-003` distinct-digest tests and the CI re-computation of
  `ECP-GTE-001`.
- Grep tests for the prohibited strings of `ECP-DLG-008` and
  `ECP-PRD-004` over the built wheel.
- The `ECP-JNL-004` fault matrix on every multi-file writer.
- A test that `transition --apply` without `[decision_identity]` refuses
  (`ECP-DEC-007`) and that a typed actor is refused after the window.
- An installed-contract byte-identity test for every regenerated managed
  file.

## Related ADRs

`ADR-ECP-001` (state and boundary over instructions; `next` as a
projection), `ADR-ECP-002` (scope enforcement at the Git boundary, not a
proposed-workspace broker), `ADR-ECP-003` (authenticated decision records
consumed by `transition`), `ADR-ECP-004` (one result schema, one selector,
one precondition engine), and `ADR-ECP-005` (eviction of self-hosting
machinery from the shipped product). Each carries `decides =
["ARCH-ECP-001"]`.

## Amendment record

**`REQ-ECP-020` addressed and `SPEC-ECP-009` conformed to, accepted 2026-08-29 under `WO-ECP-013` (issue #255).** The pull-request gate this architecture places at the Git boundary was implemented at the `handoff` checkpoint, which the evaluator binds to an `in_progress` work order; the boundary therefore enforced scope as a function of lifecycle state, red after completion and absent for a draft packet. The amendment names the state-independent `scope` checkpoint of `SPEC-ECP-009` as the binding the boundary uses, and records `ADR-ECP-006`, which decides it among the alternatives. It removes a way the implementation departed from this architecture's principle that enforcement sits on the diff; it introduces no new boundary, and `decision_assessment` stands as assessed with `ADR-ECP-006` added to the deciding records.

Accepted after the approval of `REQ-ECP-020`, because `E016` refuses an active architecture that addresses an inactive requirement, and before the approval of `WO-ECP-013`, because `W021` refuses a selected architecture unrelated to the selected requirement; the same ordering `ARCH-RLO-004` recorded.

## Amendment record

**`REQ-ECP-022` addressed and `SPEC-ECP-011` conformed to, accepted 2026-08-29 under `WO-ECP-015`.** This architecture's control plane exposes its rule selection through three read-only commands (`focus`, `check`, `next`) for one selection, and its contract names `focus` as the selector while the Git-boundary gate and the transition engine run `check`. The amendment names checkpoint-less `check` as the one projection of the selection and records `ADR-ECP-007`, which decides it among the alternatives; `next` keeps its distinct purpose. It removes a way two commands could drift from one another; it introduces no new boundary, and `decision_assessment` stands as assessed with `ADR-ECP-007` added to the deciding records.

Accepted after the approval of `REQ-ECP-022` and before the approval of `WO-ECP-015`, the ordering `ARCH-RLO-004` and the `REQ-ECP-020` amendment recorded.
