+++
id = "WO-ECP-014"
type = "work_order"
title = "Canonicalize line endings in the formal snapshot"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[assurance]
commit_bound_verification = "required"
rationale = "The change alters the digest every evidence packet and verification record binds; it is trusted engineering state later decisions rely on, so verification binds the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/workflow_compliance.py",
  "tests/test_workflow_compliance.py",
  "docs/notes/harnessctl-check.md",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/evidence/",
  "docs/engineering/execution-control-plane/requirements/REQ-ECP-021.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-010.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-001.md",
  "docs/engineering/execution-control-plane/verification/VER-ECP-010.md",
]

[relations]
implements = ["REQ-ECP-021"]
specifications = ["SPEC-ECP-010"]
verification = ["VER-ECP-010"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T09:09:09Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-08-29 with the words 'i approve the artifact packet and you can start WO-ECP-014', as a decision distinct from the approval of its definitions seconds earlier. Authorizes start preflight and then only the declared scope: the one product module, the one test module, the check note, this domain's index, the SPEC-ECP-001 amendment record and the evidence packet. It authorizes no change to a hash-locked root file, no verification record, no release and no publication. Start preflight has not been run."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-29T09:09:16Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's explicit start decision of 2026-08-29, 'you can start WO-ECP-014'. Start preflight PASS with no diagnostics over the approval commit 9220f97 carrying unmoved main 741a774, run with the governing exact public 0.9.0 evaluator outside the checkout. Bounded to the declared execution scope. This start authorizes no verification record, no release and no publication."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-29T09:20:52Z"
decided_by = "engineering-owner"
reason = "Marked implemented by the accountable engineering owner on 2026-08-29 under DR-WO-COMPLETE, 'Mark WO-ECP-014 implemented', on the handoff check reading Completed over the Git-derived change set of 11 paths at its fixed point, result 9ab56eda, no scope amendment. formal_snapshot_digest now hashes each artifact's utf8-text-lf-v1 canonical bytes through the one function every snapshot comes from; the LF digest of the fixture chain is pinned at the raw-rule value measured before the change; candidate evidence on the CRLF Windows worktree and on the LF Linux clone at c066269 both read 51b08822; Linux suite OK; Windows workstation at its two baseline failures; SPEC-ECP-001 carries the amendment record. At the moment of this decision the pull-request lanes on #259 at e932993 were still running, 3 passing and 3 pending with none failed; the settled readings are appended to the evidence packet after this transition, and the managed lane is expected red from it on, by issue #255 on the 0.9.0 root. This authorizes no further act."
+++

# Work Order: Canonicalize line endings in the formal snapshot

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above.

Commit-bound verification is `required`.

## Objective

Make `formal_snapshot_digest` hash each artifact's `utf8-text-lf-v1`
canonical bytes (`ECP-CSN-001`), keeping every LF-bound digest unchanged
(`ECP-CSN-002`) and making a CRLF checkout compute the runner's digest
(`ECP-CSN-003`), through the one function every snapshot comes from
(`ECP-CSN-004`); say so in the check reference (`ECP-CSN-005`); record the
amendment on `SPEC-ECP-001`. Issue #256.

## Why now

Every evidence packet written on this repository's Windows checkout has had
to be rebound from a Linux clone (`WO-HUP-009`, `WO-ECP-012`,
`WO-ECP-013`), and a consumer on Windows meets the same wall on every pull
request under the 0.9.0 gate.

## In scope

- `se_harness/workflow_compliance.py`: `formal_snapshot_digest` canonicalizes
  content with the `utf8-text-lf-v1` helper of `se_harness/integrity.py`.
- `tests/test_workflow_compliance.py`: the LF-unchanged digest fixed before
  the change, the CRLF-equals-LF case, the one-character change.
- `docs/notes/harnessctl-check.md`: one sentence on the canonical snapshot.
- The `## Amendment record` on `SPEC-ECP-001` (`ECP-SNP-001`); the domain
  index; the evidence packet with the Windows-versus-Linux reading. No
  architecture is selected: the change is a byte rule inside one function
  and touches no boundary `ARCH-ECP-001` draws.

## Out of scope

The chain-scoped digest of `REQ-ECP-016`; the lock's own canonicalization;
any hash-locked root file; the release carrying this change.

## Authorized decision envelope

Whether the helper is imported or the two-line canonicalization is written
locally; the fixture used for the fixed digest; the wording of the note's
sentence and of the amendment records.

## Constraints

- No digest of an LF tree moves; the test pins one against a value fixed
  before the change.
- No other caller computes a snapshot.

## Expected change surface

One product module, one test module, one note, the amendment record, the
packet, the domain index and the evidence.

## Required verification

Execute `VER-ECP-010` in full; repository-required checks; the pull
request's lanes; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/execution-control-plane/evidence/WO-ECP-014/`.

## Stop and escalate conditions

An LF-tree digest that moves under the canonical rule; a snapshot computed
outside `formal_snapshot_digest`; any need to touch a hash-locked file.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
