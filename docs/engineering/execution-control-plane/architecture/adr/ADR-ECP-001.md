+++
id = "ADR-ECP-001"
type = "adr"
title = "State and boundary over instructions: `next` is a projection of the existing kernel"
status = "draft"
owners = ["technical-owner", "repository-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[relations]
decides = ["ARCH-ECP-001"]
+++

# ADR: State and boundary over instructions: `next` is a projection of the existing kernel

## Status

Proposed.

## Context

A fresh agent on a work order today carries the launcher path, the work-order
id and its scope, the changed paths, the snapshot digest, commit roles, the
`result_sha256`, and a reserved record id in its own context, and decides
alone which `check` invocation fits the state, the change set, and the
evidence body (`docs/notes/agentic-execution-review-2026-08.md`, section 6).
The next step is emitted only after an operation; `focus` gives the decision
step, not the `check` command; no `next` command exists (section 7). The
prose that asks the agent to carry this well was already found unenforceable
by `ADR-IAR-001` and `ADR-WEX-003`. The kernel that could answer the
question in one call exists: `focus_schema2`, `run_preflight`,
`select_rule`, and `select_current_step`.

## Decision drivers

- `HRN-004`: only `harnessctl` computes the canonical next action.
- Principle 1 of the review: state lives in the harness, not the agent.
- Principle 3: instructions shrink to router and card; everything else is
  returned on demand.
- The reproduced `WEX210` self-loop must become impossible, not documented.
- No second rule engine (`ADR-ECP-004`).
- Concurrency as branches: a merge outside the chain must not invalidate
  handoff evidence (principle 4).

## Considered options

### Option A: `next` as a read-only projection of the kernel with a `context` block

`next` composes the existing functions and renders one schema-2 result
carrying manifest, chain, scope, state, exact argv, and decision required.
Consequences: one call replaces `doctor`, `focus`, `preflight`, and the
choice of `check`; the argv is byte-identical to what `focus` and `check`
render, so no divergence is possible; the change is additive to schema 2.
Costs one command, one schema member, and a `Context` section in the
digest.

### Option B: a session file written by the harness and read by every command

The harness persists selection, scope, and change set in
`.engineering-harness/session.json`. Consequences: removes the same carried
state, but introduces mutable state outside the artifact graph, a second
source of truth that `HRN-001` forbids, a locking problem for two agents,
and a stale-session failure mode; resumability by recomputation, a listed
strength, is lost.

### Option C: richer prose in the router and skills

Document the mapping from state to command in `WORKFLOW.md` and the
operating card. Consequences: cheapest; unverifiable; the same inference the
agent already gets wrong; `ADR-WEX-003` recorded that prose cannot enforce
exact behaviour.

## Decision

Select Option A. Ship `harnessctl next` as a projection of the kernel
(`SPEC-ECP-001`, `ECP-NXT-*`), derive change sets from Git rather than from
the agent (`ECP-CHG-*`), scope the evidence-binding snapshot to the
governing chain (`ECP-SNP-*`), and drop the `AGENTS.md` owner narrative from
the manifest in favour of a bounded generated command block (`ECP-MAN-*`).
State that an agent needs is returned by the harness; instructions carry
nothing the tool can compute.

## Consequences

- Positive: the agent-carried state reduces to one identifier; the self-loop
  cannot occur because the corrective names `next`; two agents on two
  branches keep their evidence bound through unrelated merges.
- Negative: every `result_sha256` changes at the upgrade because the
  canonical block gains sections; one more command in the surface.
- Operational: installed `WORKFLOW.json`, `WORKFLOW.md`, `OPERATING_CARD.md`
  regenerate on upgrade; `AGENTS_COMMANDS.md` is a new managed file;
  `--changed-path` survives one release.
- Security: `next` writes nothing and grants nothing; the Git-derived change
  set removes the agent's ability to omit a path from what `check` sees.
- Migration: `WO-ECP-001` ships `next` and `--from-git`; `WO-ECP-008` trims
  the manifest and scopes the snapshot; no amendment to an approved artifact
  is required by this decision alone.

## Validation

`ECP-NXT-004` byte-equality across `next`, `focus`, and `check`;
`ECP-NXT-008` corrective test on an `implemented` fixture; `ECP-SNP-003`
unchanged-chain-digest test; the `ECP-MAN-002` byte regeneration of the
command block; and a review-lane reading of `next` on a fresh clone with
only the lock-resolved evaluator.
