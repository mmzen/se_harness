+++
id = "SPEC-ECP-006"
type = "specification"
title = "Delegation at the Git boundary and the retained journaled apply"
status = "approved"
owners = ["technical-owner", "quality-owner", "repository-owner"]
created = "2026-08-27"
updated = "2026-08-28"

[relations]
specifies = ["REQ-ECP-011", "REQ-ECP-017", "REQ-ECP-018"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T12:03:40Z"
decided_by = "technical-owner"
reason = "Approved on 2026-08-28 by the accountable owner, 'I approve the ECP definitions and WO-ECP-005', as part of the execution-control-plane definition packet of #231 with the issue #212 amendments of #238 applied. Approval of a definition authorizes no work; each work order is approved separately."
+++

# Specification: Delegation at the Git boundary and the retained journaled apply

## Scope

This specification reduces Phase 4 delegated execution to its guarantee. A
delegation class on a work order lets a delegated actor apply three
transitions while the required pull-request gate is green; the envelope,
nonce ledger, lifetime, revocation, stability guard, and the
`delegated-workflow` subcommand leave the product; the journaled apply with
rollback and human-recovery stop is retained and used for every
harness-owned multi-file write. Today the envelope's nonce, five-minute
lifetime, revocation store, retry ordinal, and two-capture stability guard a
token that never leaves the process that minted it
(`se_harness/delegated_authority.py:25`, `:206-220`;
`se_harness/cli.py:1259-1304` accepts no envelope input), no work order
carries `[agentic_delegation]`, and gates reaching the broker are
caller-asserted JSON (`se_harness/delegated_workflow.py:399`;
`docs/notes/agentic-execution-review-2026-08.md`, section 5, weakness 3).

## Actors and external systems

- An accountable owner declares the delegation class on a work order at
  approval time.
- A delegated actor (a CI identity or a configured agent identity) applies
  the unlocked transitions.
- The configured CI status source reports the required check's conclusion
  for a commit.
- The released evaluator applies transitions and journaled writes.

## Terms

- **Delegation class:** the `[delegation] class = "execution"` table on a
  work order; `execution` is the only class this specification defines.
- **Candidate head:** the commit that `git rev-parse HEAD` returns in the
  checkout where `transition --apply` runs.
- **CI status source:** the `[ci_status]` table of
  `.engineering-harness.toml`: `source = "github-checks" |
  "local-file"`, with `check_name` and, for `github-checks`, `repository`.
- **Required gate:** the managed check of `SPEC-ECP-003` named by
  `check_name`.
- **Journaled apply:** the journal, staged-write, rollback, archive, and
  `human-recovery-stop` sequence of `apply_change_bundle`
  (`se_harness/effect_broker.py:800`, journal lifecycle at `:1029-1160`).

## Behavioral rules

### Delegation at the Git boundary

**ECP-DLG-001:** A work order may carry `[delegation]` with exactly one key,
`class`, whose value is `"execution"`; any other key or value is validator
error `E-ECP-001`, and a `[delegation]` table on a non-work-order artifact
is the same error.

**ECP-DLG-002:** When the selected work order carries `class = "execution"`,
`transition --apply` accepts a decision record whose `role` is
`delegated-executor` for exactly `DR-WO-START`, `DR-WO-COMPLETE`, and
`DR-VREC-PREPARE`; every other decision right with that role is
`WEX-ECP-022`.

**ECP-DLG-003:** Before applying a delegated transition, the evaluator
queries the CI status source for the candidate head and proceeds only when
the required gate's conclusion is `success`; any other conclusion, a missing
check, a head not found, or a source error is `WEX-ECP-040` naming the head
and the conclusion observed.

**ECP-DLG-004:** The `github-checks` source reads
`GET /repos/{repository}/commits/{sha}/check-runs` filtered by
`check_name`, authenticated by the `GITHUB_TOKEN` environment variable; the
`local-file` source reads a JSON file `{"sha": ..., "conclusion": ...}` and
exists for tests and rehearsals only, and a repository configured with
`local-file` outside a test rehearsal is `W-ECP-005`.

**ECP-DLG-005:** The delegated route writes a decision record per
`ECP-DEC-010` whose `reason` carries the gate's check-run id and head sha, so
the lifecycle event names the evidence that unlocked it.

**ECP-DLG-006:** A work order without `[delegation]` accepts no
`delegated-executor` record; delegation is never inferred from a CI
environment, a token, or an actor name.

**ECP-DLG-007:** The delegation class never unlocks `DR-VREC-DECIDE`,
`DR-RLS-PREPARE`, `DR-RLS-DECIDE`, `DR-WO-SELECT`, or any definition
decision; these remain human decision rights under `SPEC-ECP-004`.

**ECP-DLG-008:** The `delegated-workflow` subcommand, `[agentic_delegation]`
on work orders, `delegated_authority.issue_envelope`, the nonce ledger,
`MAX_ENVELOPE_LIFETIME`, `revoked`, `retry_ordinal`, and the two-observation
stability rule are removed from the package; `harnessctl --help` and the
public Python API (`se_harness.__all__`) name none of them, and a test
asserts it.

**ECP-DLG-009:** `resolve_delegation` (`se_harness/delegated_authority.py:127`)
is retained and narrows the change set an execution-class actor may declare
to the work order's `[execution_scope].paths`; its result feeds the same
`QGP-G4I-PATHS` predicate that `check` evaluates.

### The retained journaled apply

**ECP-JNL-001:** Every harness-owned write that touches more than one file
(`TransitionPlan.apply`, `evidence` rebinding with a retained record copy,
`capture-verification`, `prepare-release`, `create-artifact` with a
reservation, and `upgrade --apply` of managed files) runs through one
journaled apply that stages every target, writes a journal before the first
replace, and replaces in journal order.

**ECP-JNL-002:** A failure after the journal is written and before commit
rolls back every applied path to its pre-image; a failure during rollback
leaves the journal in state `human-recovery-stop` and the command exits with
`WEX-ECP-041` naming the journal path and every path not restored.

**ECP-JNL-003:** A command that finds a journal in `human-recovery-stop`
refuses every write with `WEX-ECP-042` until the journal is resolved by
`harnessctl recover --journal PATH --resolve`, which verifies each path's
current bytes against the journal's post-image or pre-image and archives the
journal.

**ECP-JNL-004:** The eleven-stage fault matrix of
`tests/test_effect_broker.py:308-344` is retained and re-pointed at the
shared apply, and every command of `ECP-JNL-001` has at least one fault
injection test at `after-journal-prepared` and one at `during-apply`.

**ECP-JNL-005:** The journaled apply keeps the stale-input check of
`TransitionPlan`: every staged target's current bytes are compared to the
bytes read at planning time and a difference aborts before the journal is
written, with the existing message.

**ECP-JNL-006:** `_DEFAULT_DENIED` is derived from the installer's managed
manifest, not from a hand-written list (`se_harness/effect_broker.py:50`),
and the journaled apply refuses to stage a managed path unless the caller is
`upgrade --apply`.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-ECP-011 | ECP-DLG-001 to ECP-DLG-007, ECP-DLG-009 |
| REQ-ECP-017 | ECP-JNL-001 to ECP-JNL-006 |
| REQ-ECP-018 | ECP-DLG-006, ECP-DLG-008 |

## Inputs and outputs

Inputs: the `[delegation]` table, the `[ci_status]` configuration,
`GITHUB_TOKEN`, decision records, and the existing transition arguments.
Outputs: schema-2 transition results, retained decision records, journals
under `.engineering-harness/journal/`, and the `recover` result. Example
work-order table:

```toml
[delegation]
class = "execution"
```

Example configuration:

```toml
[ci_status]
source = "github-checks"
repository = "example/repo"
check_name = "engineering-harness / pull-request-gate"
```

## Failure behaviour

`WEX-ECP-040` (gate not green), `WEX-ECP-041` (recovery stop), and
`WEX-ECP-042` (unresolved journal) are `blocked`, exit status 1. A gate
query never retries silently; the actor reruns after the check completes.
Rollback is attempted exactly once per journal.

## Compatibility and migration

`delegated-workflow` is removed without a compatibility window: no formal
work order has ever carried `[agentic_delegation]`, so no consumer
invocation exists (`docs/notes/complexity-audit-2026-08.md`, P0-5). The
`WORK_ORDER.template.md` replaces the `[agentic_delegation]` block with
`[delegation]`. `workflow_contract.json` drops the `agentic_operations`
block; `agent_contract.json` and `effect_contract.json` leave `pyproject`
package data. `ADR-AEX-006`, `ADR-AEX-007`, `ARCH-AEX-002`, and the
agentic-execution domain README receive amendment records under
`WO-ECP-006`. Installed `WORKFLOW.json` and `WORKFLOW.md` regenerate on
upgrade.

## Explicitly unspecified decisions

- The journal file format, provided it is the existing effect-broker
  journal shape or a strict subset.
- Additional CI status sources; `github-checks` and `local-file` are the
  minimum.
- Whether a second delegation class is ever added; this specification
  defines one.
- The retry cadence an orchestrating host uses while waiting for the gate;
  the harness never waits.

## Amendment record

**`ECP-DLG-010`: the restitution names a delegated decision, proposed
2026-08-29 under `WO-ECP-018`.** `ECP-DLG-002` to `ECP-DLG-007` say when a
delegated transition is accepted; nothing said how the actor learns that
the decision due is its own rather than a human's, and an actor that
cannot tell escalates every time, which defeats the class. Rule: for a
work order that carries `[delegation] class = "execution"` at the base of
the pull request, `check` and `next` set `decision_required` to
`delegated-executor` and emit the delegated command in
`command_or_response` when the decision due is one of `DR-WO-START`,
`DR-WO-COMPLETE` or `DR-VREC-PREPARE` and the configured gate reads
`success` for the current head; when the gate reads anything else they
emit a suggested-response naming the check, the head and the conclusion
observed; for every other decision right, and for a class present only on
the branch, the restitution is unchanged and names the human role.
Delegation is stated by the evaluator from the class and the gate, never
inferred by the actor. Nothing else in this specification changes.
