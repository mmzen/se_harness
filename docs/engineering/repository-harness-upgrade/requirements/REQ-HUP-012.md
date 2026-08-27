+++
id = "REQ-HUP-012"
type = "requirement"
title = "Apply one bounded standard-root transaction to exact public 0.7.0"
status = "approved"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-08-27"
updated = "2026-08-27"
statement = "WHEN exact public se-harness 0.7.0 is authorized to replace the 0.6.0 root, THE SYSTEM SHALL apply only the reviewed standard-root plan, bound to the prior lock and the target evaluator, through one approved evaluator-upgrade work order, atomically and with canonical evidence."
verification_method = "automated-test"
priority = "must"
source = "INT-HUP-004; RLS-SEH-015"
measure = "one transaction; zero unplanned paths; a no-op replay after apply"

[relations]
derives_from = ["CAP-HUP-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-27T14:37:56Z"
decided_by = "repository-owner"
reason = "Approved on 2026-08-27 by the accountable owner, 'i approve the packet, you can start WO-HUP-006', after the rehearsal of the transaction in a throwaway worktree and the owner's decision to move the candidate to development version 0.8.0 inside the work order. Adopts exact public 0.7.0 (wheel e8f4fdc9ad60879a3fa4627c063fa7bb9513e2bd109c47258cf7f7aa6ecf27f3, payload 26c11ec5e2363c3c0a9a416e69a3faa8bdf2d7a046710075bdeb661dd1003ee9) from the 0.6.0 lock 978cebb7824b7928d95ed43897b0f848441cc4ab7403a0cdd08a55a77df2b79e through one reviewed standard-root transaction of 43 add or update paths, no customization."
+++

# Requirement: Apply one bounded standard-root transaction to exact public 0.7.0

## Rationale

The root is the evaluator every later lifecycle act is judged by. Moving it
is safe only as one reviewed, atomic, evidence-bound transaction whose inputs
(prior lock, target wheel and payload) are pinned before it runs, so a wrong
evaluator or a drifted plan stops before any managed byte is written.

## Required response

- Bind the transaction to the prior lock SHA-256
  `978cebb7824b7928d95ed43897b0f848441cc4ab7403a0cdd08a55a77df2b79e` and to
  the target identity `INT-HUP-004` states.
- Require approved or in-progress `WO-HUP-006` and its exact
  `[evaluator_upgrade]` table.
- Apply only the paths the reviewed 0.7.0 plan lists (`SPEC-HUP-006`) and the
  installer-owned lock, through the 0.7.0 evaluator installed outside the
  checkout.
- Write canonical `WO-HUP-006` evaluator-upgrade evidence and require a
  no-op replay of the plan afterwards.

## Failure behavior

Unexpected paths, `customized` or `conflict` results, identity drift, a lock
mismatch, partial output, an evidence-path collision, or a replay that is not
a no-op stops the transaction and leaves the pre-write state.
