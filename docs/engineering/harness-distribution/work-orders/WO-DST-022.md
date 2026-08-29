+++
id = "WO-DST-022"
type = "work_order"
title = "Retire managed files that leave the managed set on upgrade"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[assurance]
commit_bound_verification = "required"
rationale = "The change alters the upgrade transaction every consumer root runs and the lock it writes; future adoption and release decisions rely on its correctness, so verification binds the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/installer.py",
  "tests/test_standard_repository_lifecycle.py",
  "docs/notes/harness-installation-and-upgrades.md",
  "docs/engineering/harness-distribution/README.md",
  "docs/engineering/harness-distribution/requirements/REQ-DST-066.md",
  "docs/engineering/harness-distribution/specifications/SPEC-DST-022.md",
  "docs/engineering/harness-distribution/specifications/SPEC-DST-001.md",
  "docs/engineering/harness-distribution/verification/VER-DST-022.md",
  "docs/engineering/harness-distribution/work-orders/WO-DST-022.md",
  "docs/engineering/harness-distribution/evidence/",
  "docs/engineering/harness-distribution/verification-records/",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-007.md",
]

[relations]
implements = ["REQ-DST-066"]
specifications = ["SPEC-DST-022"]
verification = ["VER-DST-022"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T18:07:11Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-08-29 with the words 'I approve WO-DST-022 and you can start', as a decision distinct from the approval of its definitions seconds earlier. Authorizes start preflight and then only the declared scope: the one product module, the one test module, the installation note, this domain's index, the SPEC-DST-001 and SPEC-ECP-007 amendment records and the evidence packet. It authorizes no change to a hash-locked root file, no verification record, no release and no publication. Start preflight has not been run over this approval."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-29T18:07:40Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's explicit start decision of 2026-08-29, 'I approve WO-DST-022 and you can start'. Start preflight PASS with no diagnostics over the approval commit 739a0fc carrying unmoved main d3b5a3f, run with the governing exact public 0.11.0 evaluator outside the checkout. Bounded to the declared execution scope. This start authorizes no verification record, no release and no publication."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-29T18:27:19Z"
decided_by = "engineering-owner"
reason = "Marked implemented by the accountable engineering owner on 2026-08-29 under DR-WO-COMPLETE, 'Mark WO-DST-022 implemented', on the handoff check reading Completed over the Git-derived change set of 12 paths from main d3b5a3f at its fixed point, result 0165cc7f, packet snapshot 3ff0291c, no scope amendment. plan_install classifies leaving-set managed and fragment paths as remove when bytes match and customized when they differ; apply deletes them with directory pruning inside the one rollback transaction, keeps the lock and replay clean, and records remove in the transaction evidence; the fifteen 0.10.0-to-0.11.0 retired skill paths are pinned in conformance tests; the installation note carries the rule and the manual remediation; SPEC-DST-001 and SPEC-ECP-007 carry the amendment records. Validate reads 0 errors; the released 0.11.0 doctor reads 0 FAIL; the Windows suite is at its one baseline error reproduced on an unmodified control at the same commit; the Linux lane settles hosted on the pull request opened after this transition. This authorizes no verification record, no release and no publication."
+++

# Work Order: Retire managed files that leave the managed set on upgrade

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above.

Commit-bound verification is `required`.

## Objective

Make `plan_install(mode="upgrade")` classify prior-lock managed paths absent
from the managed set as `remove` when their bytes match, `customized` when
they differ (`DST-UPR-001`); delete them in the one apply transaction with
directory pruning and rollback (`DST-UPR-002`, `DST-UPR-003`); keep the lock
and replay clean (`DST-UPR-004`), the refusal consistent (`DST-UPR-005`) and
the evidence complete (`DST-UPR-006`); pin the 0.10.0-to-0.11.0 pair in a
conformance test (`DST-UPR-007`); document the rule and the manual
remediation for already-orphaned 0.11.0 consumers (`DST-UPR-008`); record
the amendments on `SPEC-DST-001` and `SPEC-ECP-007`. Issue #271.

## Why now

Every consumer that upgrades 0.10.0 to 0.11.0 keeps three orphaned skill
directories whose `SKILL.md` instructs an agent to run a retired command and
whose `.claude` adapters still register with Claude Code; nothing reports
it, and this repository's own adoption had to delete the fifteen files by
hand as a recorded deviation (`WO-HUP-011`).

## In scope

- `se_harness/installer.py`: leaving-set classification in `plan_install`,
  deletion with pruning and rollback in `apply_changes`, `remove` in the
  evidence plan.
- `tests/test_standard_repository_lifecycle.py`: the `DST-UPR-007`
  conformance test and the seed, missing-path, customization, evidence and
  interrupted-apply cases.
- `docs/notes/harness-installation-and-upgrades.md`: the removal rule and
  the fifteen-path remediation list.
- The `## Amendment record` on `SPEC-DST-001` (action vocabulary) and on
  `SPEC-ECP-007` (`ECP-SKL-004`'s reporter is `upgrade`, not `doctor`); the
  domain index chain line; the evidence packet. No architecture is selected:
  no active architecture addresses `REQ-DST-066`, and the change stays
  inside the installer boundary `ARCH-DST-001` already draws.

## Out of scope

Any change to `doctor`'s checks; the released 0.11.0 evaluator's behaviour;
any hash-locked root file; retroactive cleanup of consumers already on
0.11.0; the release carrying this change; the lock and evidence schemas.

## Authorized decision envelope

Helper structure inside `installer.py`; fixture bytes and assertion shapes
in the tests; the wording of the plan line, the note and the amendment
records.

## Constraints

- Owner bytes are never deleted: a differing copy refuses, seed content is
  untouched, a fragment's owner remainder survives its block's removal.
- Leaving-set paths are untrusted input and resolve through the existing
  containment checks.
- The evidence document keeps its schema id and canonical form.

## Expected change surface

One product module, one test module, one note, two amendment records, this
packet, the domain index and the evidence.

## Required verification

Execute `VER-DST-022` in full; repository-required checks; the pull
request's lanes; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/harness-distribution/evidence/WO-DST-022/`.

## Stop and escalate conditions

A remove that would touch a path outside the target root; an owner byte
lost in any test; a needed change to `doctor`, the lock schema or a
hash-locked file; the replay postcondition failing after a removal.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
