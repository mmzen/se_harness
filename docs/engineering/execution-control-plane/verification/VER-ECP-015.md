+++
id = "VER-ECP-015"
type = "verification"
title = "Independent evidence for the delegation class at the Git boundary"
status = "approved"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[relations]
verifies = ["REQ-ECP-011"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T17:42:15Z"
decided_by = "assurance-owner"
reason = "Approved by the assurance owner on 2026-08-29 with the words 'Approve and start WO-ECP-018': the delegation-class subset of VER-ECP-006 - scenarios 1 to 4, the security checks, the validator and source rows, the narrowing row and the ECP-DLG-010 restitution row; the hosted demonstration deferred to the release carrying the class."
+++

# Verification Contract: Independent evidence for the delegation class at the Git boundary

## Independence

Expected behaviour derives from `REQ-ECP-011` and `ECP-DLG-001` to
`ECP-DLG-007` and `ECP-DLG-009` of `SPEC-ECP-006`. `VER-ECP-006` remains
the contract for the whole of that specification; this contract is the
subset a delegation-class work order can execute — its scenarios 1 to 4
and its security checks — so that the record binding the class covers
exactly what the class did. The tests write the fixture work order, the
fixture gate file and the fixture configuration themselves and drive the
CLI; the gate reader is exercised against a recorded HTTP transcript and,
for the `github-checks` source, against a stub server that answers the
documented endpoint; the hosted demonstration is read on this
repository's own pull requests once a release carrying the class governs
the root.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-ECP-011` green gate unlocks | test: a work order with `[delegation] class = "execution"`, the `local-file` gate at `success`; `transition --apply` with `--decision WO=delegated-executor` for `DR-WO-START` and later `DR-WO-COMPLETE`; `capture-verification --owner delegated-executor` for `DR-VREC-PREPARE` | `tests/test_delegation_class.py` | each applies; the lifecycle event's `reason` names the check-run id and head sha (`ECP-DLG-005`) |
| `REQ-ECP-011` red or absent gate refuses | test: the same with the gate at `failure`, `neutral`, `cancelled`, a missing check, a head not found, and a reader error | same | `WEX-ECP-040` naming the head and the conclusion observed; no write |
| `ECP-DLG-003` gate never from the caller | test: any request-side assertion of gate state is ignored; only the configured source decides | same | refusal when the source says otherwise, whatever the caller supplies |
| `ECP-DLG-002`, `ECP-DLG-007` rights outside the class | test: `delegated-executor` on `DR-WO-APPROVE`, `DR-VREC-DECIDE`, `DR-RLS-DECIDE` and a definition approval with the gate at `success` | same | `WEX-ECP-022` naming the right; no write |
| `ECP-DLG-006` no class, no delegation | test: the same work order without `[delegation]`; a CI-like environment (`GITHUB_ACTIONS`, a token) present | same | the delegated role is refused on every right |
| `ECP-DLG-001` validator | test: `[delegation]` with a second key, another value, or on a requirement | template validator tests | `E-ECP-001` |
| `ECP-DLG-004` sources | test: `github-checks` against a stub server answering `GET /repos/{r}/commits/{sha}/check-runs` with and without `GITHUB_TOKEN`; `local-file` outside a rehearsal | same | the documented request shape and filter; `W-ECP-005` for `local-file` outside a rehearsal |
| security: class read at the base | test: the class added to the work order in the same branch only | same | refused: the base's copy carries no class |
| `ECP-DLG-009` narrowing | test: a delegated `DR-WO-COMPLETE` whose Git-derived change set leaves `[execution_scope].paths` | same | `QGP-G4I-PATHS` fails with `WEX201` before the gate is consulted |
| `ECP-DLG-010` the actor is told | test: `check --artifact WO` on a class-bearing work order at each of the three rights with the fixture gate `success`, `pending` and `failure`, and on a right outside the class; the same work order with the class only on the branch | same | `decision_required` is `delegated-executor` with a command only when the gate is `success`; a suggested-response naming check, head and conclusion otherwise; the human role and no delegation for other rights and for a class absent at the base |
| `REQ-ECP-011` hosted | demonstration: one delegated `DR-WO-START` on a throwaway branch of this repository with the real required check | deferred: read on the first work order carrying the class after the release with this change governs the root; until then the fixture source is the evidence |

## Acceptance scenarios

### Scenario 1: green gate unlocks start

Approve a work order carrying the class. Set the fixture gate to `success`
for the candidate head. As `delegated-executor`, apply `DR-WO-START`.
Assert `in_progress` and a lifecycle event whose reason names the class,
the check-run id and the head sha.

### Scenario 2: failure path, red gate

Set the gate to `failure` and repeat. Assert refusal naming the gate's head
and conclusion and no write.

### Scenario 3: failure path, gate state asserted by the caller

Supply any request-side claim that the gate passed while the fixture reader
says `failure`. Assert refusal.

### Scenario 4: failure path, right outside the class

As `delegated-executor`, attempt `DR-WO-APPROVE` with a passing gate. Assert
refusal naming the right.

## Evidence retention

Under `docs/engineering/execution-control-plane/evidence/WO-ECP-018/`.

## Pass criteria

Every deterministic test passes on the Linux lane; the Windows workstation
reading is at its baseline. Graph and integrity readings come from the
exact released evaluator installed outside the checkout.

## Residual uncertainty

The hosted demonstration waits for the release carrying the class and its
adoption as root, and for a branch-protection rule on `main` naming the
managed check, which the harness cannot set; until the rule exists the gate
reports and the class enforces, but a human merge without a green check is
still possible.
