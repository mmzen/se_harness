+++
id = "VER-ECP-006"
type = "verification"
title = "Independent evidence for delegation at the Git boundary, the retained journaled apply, and the absent envelope apparatus"
status = "approved"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-27"
updated = "2026-08-28"

[relations]
verifies = ["REQ-ECP-011", "REQ-ECP-017", "REQ-ECP-018"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T12:03:40Z"
decided_by = "assurance-owner"
reason = "Approved on 2026-08-28 by the accountable owner, 'I approve the ECP definitions and WO-ECP-005', as part of the execution-control-plane definition packet of #231 with the issue #212 amendments of #238 applied. Approval of a definition authorizes no work; each work order is approved separately."
+++

# Verification Contract: Independent evidence for delegation at the Git boundary, the retained journaled apply, and the absent envelope apparatus

## Independence

Expected behaviour derives from `REQ-ECP-011`, `REQ-ECP-017`, `REQ-ECP-018`,
and the `ECP-DLG-` and `ECP-JNL-` rules of `SPEC-ECP-006`, read against
`ARCH-ECP-001` and the proposed outcome of `ADR-ECP-002`. Gate status is
supplied to the tests by a fixture check-run reader whose outcomes the test
sets, so the candidate cannot assert its own gate. The fault matrix is
written from the requirement (every stage of a multi-file write must either
roll back or stop for a human), reusing the eleven-stage structure the
existing broker tests already enumerate
(`tests/test_effect_broker.py:308-344`) as a list of stages, not as expected
values. Public-API absence is checked by importing the packaged wheel, not
the source tree.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-ECP-011` delegation class unlocks transitions behind the gate | test: `transition --apply` by a delegated actor for each of `DR-WO-START`, `DR-WO-COMPLETE`, `DR-VREC-PREPARE` with the fixture gate passing, failing, and absent; demonstration: one delegated `DR-WO-START` on a throwaway branch with the real required check | work order declaring a delegation class; the same work order without one; a delegated actor attempting `DR-WO-APPROVE` | each of the three rights applies only when the gate is `passing`; `failing` and `absent` are refused with the gate state in the diagnostic; a work order without the class refuses the delegated actor on every right; a right outside the three is refused regardless of gate state |
| `REQ-ECP-017` journaled apply with rollback and human-recovery stop | test: fault injection at every stage of a harness-owned multi-file write (`transition --apply` over three artifacts; `evidence` writing a packet and rebinding another) | crash before journal, after journal prepared, mid-write, before commit, after commit; retry after each | before commit, every target byte equals its pre-write value after the crash; after commit, the write is complete; a retry after a crash either completes the journal or stops with `human-recovery-stop` naming the journal path and never produces a third state |
| `REQ-ECP-018` no envelope apparatus in the product surface | analysis: symbol inventory of the wheel's public API and the CLI parser; test: import and `--help` assertions | the built wheel; `harnessctl --help` and every subcommand's `--help` | no public name, argument, or help text contains `envelope`, `nonce`, `revoked`, `revocation`, `lifetime`, or `retry_ordinal`; `harnessctl delegated-workflow` is absent or refuses with a retirement diagnostic |

## Acceptance scenarios

### Scenario 1: green gate unlocks start

Approve a work order carrying a delegation class. Set the fixture gate to
`passing`. As the delegated actor, apply `DR-WO-START`. Assert
`in_progress` and a lifecycle event naming the delegation class.

### Scenario 2: failure path, red gate

Set the gate to `failing` and repeat. Assert refusal naming the gate and no
write.

### Scenario 3: failure path, gate state asserted by the caller

Supply a request body claiming `gates_passed: true` while the fixture reader
says `failing` (today the broker accepts caller-asserted gates,
`se_harness/delegated_workflow.py:399`). Assert refusal.

### Scenario 4: failure path, right outside the class

As the delegated actor, attempt `DR-WO-APPROVE` with a passing gate. Assert
refusal naming the right.

### Scenario 5: crashed journaled apply, retry recovers or stops

For each injected fault stage, crash a three-artifact `transition --apply`,
assert the pre-commit stages leave every artifact byte-equal to before,
then run the retry. Assert either completion with all three artifacts in
the target state, or a `human-recovery-stop` naming the journal, and never
a mixed state.

### Scenario 6: Windows mid-bundle replace failure

On Windows, hold one target file open during the write. Assert the apply
rolls back or stops, and that no target is partially written (the case the
existing fault tests exist for; complexity audit,
`docs/notes/complexity-audit-2026-08.md:345-347`).

### Scenario 7: the wheel carries no envelope

Build the wheel, install it into a disposable environment, import
`se_harness` and every public submodule, and walk `harnessctl --help`
recursively. Assert none of the listed names appears.

## Property and invariant tests

- For any sequence of interleaved crashes and retries, the set of artifact
  states observed is a subset of {all-before, all-after}.
- Delegated acceptance is monotone in gate state: no request accepted at
  `failing` is refused at `passing` for the same right.

## Static and architecture checks

- `grep -rn "revoked=" se_harness` returns nothing (today 0 product callers
  already; complexity audit P1-3).
- `grep -rnE "nonce|MAX_ENVELOPE_LIFETIME|retry_ordinal" se_harness` returns
  nothing outside the journal module's own tests.
- `se_harness/delegated_authority.py` retains `resolve_delegation` narrowing
  or its replacement in one module; `se_harness/skill_contract.py`,
  `se_harness/agent_contract.json`, and `se_harness/effect_contract.json`
  are absent from the wheel's `RECORD`.
- `pyproject.toml` package data lists no removed JSON mirror.

## Security and privacy checks

- The gate reader takes the check-run outcome for the candidate commit from
  the CI provider, keyed by commit id, never from a request body.
- A delegated actor cannot widen the delegation class by editing the work
  order in the same pull request: the class read for the decision is the
  one at the base of the pull request.

## Performance and resilience checks

- A three-artifact journaled apply completes within twice the time of
  today's `TransitionPlan` apply on both platforms; figures recorded.

## Manual assessments

The technical owner reads the amendment records on `ADR-AEX-006`,
`ADR-AEX-007`, and `ARCH-AEX-002` and confirms each states what is
superseded and what is retained, without altering front matter.

## Evidence retention

Under `docs/engineering/execution-control-plane/evidence/WO-ID/`: the
fault matrix with per-stage outcomes on each platform, the journal files
from stopped retries, the symbol inventory of the wheel and the `--help`
walk, the demonstration pull request and check-run identifiers, and
per-platform test figures.

## Pass criteria

Every deterministic test passes on Linux and on Windows, figures labelled per
platform, including Scenario 6 on Windows. The demonstration of Scenario 1
runs against the real required check installing the exact released
evaluator, se-harness 0.7.1, outside the checkout. Graph and integrity
readings come from that evaluator.

## Residual uncertainty

The gate reader trusts the CI provider's check-run API; a compromised
provider is outside this contract. The demonstration can only be run once a
work order carrying a delegation class has been approved by its owner.
