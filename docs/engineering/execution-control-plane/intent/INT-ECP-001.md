+++
id = "INT-ECP-001"
type = "intent"
title = "Make the harness an execution control plane: state and boundary, not instructions"
status = "draft"
owners = ["product-owner", "domain-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[relations]
+++

# Intent: Make the harness an execution control plane: state and boundary, not instructions

## Problem

The 2026-08 agentic execution review (`docs/notes/agentic-execution-review-2026-08.md`,
tree `992fd73`) found that the harness computes a deterministic next step,
binds records to commits, and governs from a released evaluator outside the
checkout, yet asks the coding agent it is designed to bound to carry the
state and to be trusted at exactly the points where it claims not to trust it.

What an agent carries today, measured on `WO-REB-027` (review section 6):
the launcher path; the work-order identifier and a thirteen-entry scope;
twenty-two hand-typed changed paths; the current snapshot digest; commit
roles; verbally obtained decisions re-typed as `--reason`; `result_sha256`;
and the reserved record identifier. The mandatory reading set is a twelve-file
manifest of 49.5 KB, about 12.4k tokens, 30% of it repository-generic; the
realistic reading set when anything fails is about 41k tokens. Seventeen
commands separate `doctor` from the third human decision.

What the harness enforces against the agent today:

- Execution scope is checked only by `check --changed-path ... --changes-complete`
  against paths the agent types by hand, never against `git diff`
  (`se_harness/workflow_compliance.py:156-165`, `:316-322`); `transition`
  never checks scope; the template CI checks it only when a
  `Harness-Restitution:` trailer is volunteered
  (`templates/repository/standard/.github/workflows/engineering-harness.yml:56-89`).
  The `result_sha256` preimage renders restitution fields only, so identical
  digests cover different change sets (`se_harness/workflow_result.py:174-207`).
- Every transition needs `--decision ID=ACTOR`, but the actor is a string of
  at most 128 characters; no Git-author, `GITHUB_ACTOR`, `CODEOWNERS`, or
  signature check exists in `se_harness/` or `scripts/`
  (`se_harness/workflow.py:606`). Zero identity checks stand behind twelve
  declared decision rights.
- `check` and `transition` run different engines: `_recommend`
  (`se_harness/workflow.py:355-399`) beside `select_rule`
  (`se_harness/workflow_contract.py:554-595`); `_validate_preconditions`
  (`se_harness/workflow.py:685-750`) beside a `transition` gate checkpoint
  that `check_workflow` refuses (`se_harness/workflow_compliance.py:395`);
  schema 1 is still the default on `transition`, `capture-verification`, and
  `prepare-release` (complexity audit P0-6). The two can disagree on the same
  work order.
- Evidence is agent-authored prose matched by substring
  (`se_harness/workflow_compliance.py:266-291`); the snapshot digest it binds
  moves on any artifact edit, so `WO-HUP-007` re-bound its evidence twice
  (review section 5, weakness 6).

What ships to a consumer today: a fresh repository that runs `init`, commits,
and runs `doctor` exits 1 (`se_harness/hash_bound_classes.json:19-32`;
`templates/repository/standard/gitattributes.fragment:4-6`; complexity audit
P0-1). Six `RLS-SEH-*` identifiers of this repository's own releases are
hard-coded in three generic files (audit P1-2). Phase 4 delegated execution
is 8,766 lines, 39% of the package, reachable from the CLI and never run on a
real work order because no `[agentic_delegation]` table exists; its envelope
guards a token that never leaves the process that minted it
(`se_harness/cli.py:1259-1304`; audit P0-5, P1-3). Three shipped writing
skills print `"evaluator_invoked": false` while their `SKILL.md` says they
invoke the evaluator (`check_scope.py:190-199`).

Every agent failure mode this produces has precedent in the repository:
the in-tree CLI run as the evaluator (RCA 0.5.0), the wrong checkpoint
(reproduced live as a `WEX210` self-loop), a CRLF trailer (`REQ-ADS-004`),
stale evidence binding (`WO-HUP-007`), rebase orphaning a ready record
(PR #176), and an incomplete change set, which is unobservable by design.

## Desired outcomes

- An agent that opens a governed repository learns, from the harness and in
  one exchange, what is selected, what state it is in, what it may touch,
  what it must read, what it does next, and which human decision is pending.
  It carries none of that in its own context.
- The set of paths a work order changed is a Git fact the harness reads, not
  a list the agent recites. A change outside the declared scope cannot reach
  `main` through a pull request, whether or not the agent cooperated.
- A lifecycle decision is a record whose signer the harness can verify and
  whose role the harness can check against the decision rights. The claim
  "accountable humans retain authority" becomes a property of the system.
- Every workflow command reads the same state and reaches the same verdict
  for the same repository; `check` and `transition` cannot disagree.
- Evidence packets and identifiers are produced and re-bound by the harness,
  so the recurring agent failures become things an agent cannot get wrong.
- A consumer repository receives only the machinery it needs: a green
  `doctor` after `init`, no identifiers of this repository's releases, no
  skill that describes behaviour it does not have, and no second execution
  model to recognise and ignore.
- Delegation to an agent is an attribute a human sets on a work order and a
  gate that must be green, with nothing in between.

## Actors and stakeholders

- Coding agents executing a work order on any host: benefit from bounded
  state and bounded reading; bear no authority.
- The `product-owner` and `domain-owner`: decide this intent and the
  capabilities and requirements derived from it.
- The `technical-owner`, `quality-owner`, and `repository-owner`: decide the
  architecture, specifications, and decisions; bear the cost of retiring
  approved artifacts under `agentic-execution`, `released-evaluator-boundary`,
  and `legacy-release-evidence`.
- The `assurance-owner` and `engineering-owner`: decide verification and
  execution; bear the risk that an enforced boundary blocks work the
  honour-based one allowed.
- Consumer repositories governed by a released evaluator: benefit from a
  portable product; bear migration risk on managed-file updates.
- CI on the pull request: becomes the boundary that enforces scope, gates,
  and digest for anything reaching `main`.

## Success measures

| Measure | Baseline | Target | Observation window |
|---|---:|---:|---|
| Calls an agent needs to obtain selection, state, chain, scope, reading set, and next command (review section 6) | 3 (`focus`, `preflight`, a `check` chosen by inference) | 1 | First verified work order of the packet |
| Mandatory reading set for a start phase, tokens (review section 6) | ~12.4k (49.5 KB, twelve files) | <= 8.7k, none repository-generic | Per phase, measured by `preflight` |
| Changed paths typed by hand on a product-code work order (review section 5, weakness 2) | 22 (`WO-REB-027`) | 0 | Every handoff check |
| Pull requests whose scope is evaluated by CI without a volunteered trailer (`engineering-harness.yml:56-89`) | 0% | 100% | Every pull-request event after adoption |
| Identity checks behind a `--decision` actor (`se_harness/workflow.py:606`) | 0 | 1 per decision, role checked against decision rights | Every applied transition |
| Distinct next-step selectors and precondition engines in the workflow core (audit P0-6) | 2 selectors, 3 precondition engines, 2 result schemas | 1, 1, 1 | Package at the packet's completion commit |
| `doctor` exit status in a fresh consumer repository after `init` and a commit (audit P0-1) | 1 | 0 | Every release qualification |
| This repository's release identifiers in generic product code (audit P1-2) | 6 | 0 | Package at the packet's completion commit |
| Phase 4 lines in the package (audit P0-5) | 8,766 (39%) | Journaled apply and scope narrowing only | Package at the packet's completion commit |
| Shipped skills that describe an evaluator call they do not make (`check_scope.py:190-199`) | 3 | 0 | Distributed template at the packet's completion commit |
| Handoff evidence invalidated by a merge on an unrelated chain (review section 5, weakness 16) | Every merge to `main` | None | Every handoff check |

## Non-goals

- Changing what a lifecycle state means, which states exist, or which role
  holds which decision right.
- Changing the artifact schemas, the traceability relations, or the formal
  graph as sole authority (`HRN-001`).
- Replacing Markdown with TOML front matter as the store, or the released
  evaluator boundary (`MG001` to `MG006`).
- Building a selection algorithm that chooses a work order for an agent, an
  orchestration layer for several agents, or a session store.
- Enforcing anything against an agent runtime that ignores every instruction
  other than what a commit and a pull request expose.
- Rewriting the 138 historical verification records or any verified or
  released record.
- Changing `capture-verification` or `prepare-release` beyond their result
  schema.

## Principles and immutable constraints

Principles, stated by the 2026-08 agentic execution review, section 10:

1. State lives in the harness, not the agent: selection, scope, identifiers,
   evidence binding, and the next command.
2. Enforcement lives at Git boundaries: the diff for scope, the pull-request
   gate for gates, signature or actor for authority.
3. Instructions shrink to the router and the card; everything else is
   returned on demand.
4. Concurrency is branches; the snapshot that binds handoff evidence is
   scoped to the governing chain so a merge elsewhere does not invalidate it.
5. Delegation is a work-order attribute that unlocks transitions when the
   gate is green; no envelope, no broker.
6. Orchestration is host detail; the combined branch is what the gate
   validates.

Immutable constraints (review section 8):

- `HRN-001` to `HRN-008`, the stop-condition list, and the gate, router, and
  card structure stay.
- Verification and release records stay commit-bound and terminal; a record
  cannot contain the hash of its own commit; supersession and amendment are
  the only repairs.
- Only the released evaluator outside the checkout mutates state; the runtime
  and evaluator identity layers and the hash-bound classes stay.
- Gates fail closed; `not_assessable` stays an honest verdict.
- Automation prepares `ready` and never decides (`HRN-005`); nothing in this
  initiative moves a decision from a human to a machine.
- Provider neutrality: no runtime authority, no provider-specific behaviour.
- Every change to an approved artifact is an amendment under this
  repository's own rules.

## Risks and assumptions

Facts:

- The review re-verified each load-bearing claim by grep or execution at
  `992fd73`; the complexity audit measured at `f0ecd9b`.
- `REL-SEH-017`, the shipped release record, describes Phase 4 as active;
  the audit's "inert" line comes from rejected records (review, method).
- 116 of 117 verified records bind a commit reachable from `HEAD` (review
  section 4).

Assumptions:

- CI on the pull request is a boundary every agent path crosses before
  `main`; a repository that merges without pull requests is outside the
  guarantee.
- An identity source exists on every host that applies transitions: a commit
  signature locally, the actor in CI.
- Consumers accept managed-file updates that remove hash-bound classes and
  skills.
- The owner decides that Phase 4 is reduced rather than kept (audit P0-5);
  the review recommends reduction.

Risks:

- Retiring the envelope and broker touches approved artifacts under
  `agentic-execution`; each needs an amendment, and `ADR-AEX-004` to
  `ADR-AEX-007` already read `approved` in front matter and "Proposed" in
  body (review section 5, weakness 15).
- A mandatory scope gate blocks work that today passes on an incomplete
  change set; the first weeks will surface undeclared scope.
- Authenticated decisions add a signing step to every transition; without a
  usable identity source the transition path fails closed and work stops.
- Reducing the reading set below the manifest may drop an obligation that
  only prose stated; every dropped line must be either enforced or scoped.

Open decisions: none at intent level. Decisions on the Git boundary versus
the broker, on the identity source, on one kernel, and on eviction from the
product are recorded as proposed in `ADR-ECP-001` to `ADR-ECP-005`.
