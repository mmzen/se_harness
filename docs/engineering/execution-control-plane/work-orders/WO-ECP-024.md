+++
id = "WO-ECP-024"
type = "work_order"
title = "Remove the dead .gitattributes tail, by the delegated route"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-08-31"
updated = "2026-08-31"

[assurance]
commit_bound_verification = "required"
rationale = "First production use of the delegation class: the delegated lifecycle events and the byte-rule file are trusted state later audits read, so verification binds the exact candidate commit."
decided_by = "engineering-owner"

[delegation]
class = "execution"

[execution_scope]
paths = [
  ".gitattributes",
  ".engineering-harness.delegation.toml",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/evidence/",
  "docs/engineering/execution-control-plane/requirements/REQ-ECP-029.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-018.md",
  "docs/engineering/execution-control-plane/verification/VER-ECP-020.md",
]

[relations]
implements = ["REQ-ECP-029"]
specifications = ["SPEC-ECP-018"]
verification = ["VER-ECP-020"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-31T14:22:20Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-08-31 by selecting the presented option 'Approve WO-ECP-024 and delegate', as a decision distinct from the approval of its definitions in the same transaction. The work order carries [delegation] class = execution: this approval is the act of delegating DR-WO-START, DR-WO-COMPLETE and DR-VREC-PREPARE to the delegated-executor role, each unlocked only while the required validate check is success for the exact candidate head, per REQ-ECP-011 and SPEC-ECP-006, effective when this work order is at the base of the execution pull request. It authorizes only the declared scope: the seven dead .gitattributes lines out, the delegation gate configuration, the packet and the domain index. The verification of the prepared record and every merge remain human decisions. Start preflight has not been run; the start itself is the delegated route's."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-31T14:32:20Z"
decided_by = "delegated-executor"
reason = "Delegated DR-WO-START under [delegation] class 'execution': required check 'validate' success at 3ce230208d7504b219aca3beca125c5e8fdc46a7 (check-run 99523603905, source github-checks)."
+++

# Work Order: Remove the dead .gitattributes tail, by the delegated route

## Lifecycle

This work order carries `[delegation] class = "execution"`: approving it is
the act of delegating `DR-WO-START`, `DR-WO-COMPLETE` and `DR-VREC-PREPARE`
to the `delegated-executor` role, each unlocked only while the required
`validate` check is `success` for the exact candidate head (`REQ-ECP-011`,
`SPEC-ECP-006` `ECP-DLG-001` to `ECP-DLG-010`; the default branch's ruleset
requires the check since 2026-08-31). The approval below, the verification
of the record it prepares, and every merge stay human decisions.

This is the hosted delegation demonstration issue #284 names, on the real
remaining work of issue #285 item #285b.

## Objective

Delete the two dead remnants from `.gitattributes` — the retained
`WO-ECP-010` comment whose promise `WO-ECP-011` fulfilled, and the
`se_harness/agent_contract.json` rule whose file `WO-ECP-006` deleted
(`ECP-GAT-001`, `ECP-GAT-002`) — prove every remaining rule live
(`ECP-GAT-003`), and take the three mechanical lifecycle decisions by the
delegated route under the enforced green gate (`ECP-GAT-004`).

## In scope

- `.gitattributes`: the seven dead lines out; nothing else moves.
- `.engineering-harness.delegation.toml`: the gate configuration
  (`github-checks`, `check_name = "validate"`, `base_ref = "origin/main"`),
  committed as owner content beside the managed configuration.
- The evidence packet with the liveness measurement, the suite readings and
  the delegated lifecycle events quoted back; the domain index.

## Out of scope

The managed block between the `se-harness` markers; every live byte rule;
any test, product or template byte; the verification decision on the
prepared record; the merges.

## Authorized decision envelope

The delegated actor decides when each of its three transitions runs, bound
by the gate; the wording of the evidence. Nothing else.

## Constraints

- A delegated act is taken only on the evaluator's restitution naming
  `delegated-executor` with a command; a `WEX-ECP-040` refusal is waited
  out or repaired, never bypassed.
- `doctor` must read the managed block unchanged after the edit.

## Expected change surface

`.gitattributes` (−7 lines), the new delegation gate configuration, the
packet, this domain's index.

## Required verification

Execute `VER-ECP-020` in full; repository-required checks; the pull
request's lanes; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/execution-control-plane/evidence/WO-ECP-024/`.

## Stop and escalate conditions

Any managed-block byte moving; any live rule matching nothing after the
edit; a delegated transition the evaluator refuses for a reason other than
a not-yet-green gate; any need for a decision outside the three delegated
rights.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the delegated route's, recorded
with the class, the check-run id and the head sha.
