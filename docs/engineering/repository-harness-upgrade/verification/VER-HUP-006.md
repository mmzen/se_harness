+++
id = "VER-HUP-006"
type = "verification"
title = "Verify standard-root adoption of exact public 0.7.0"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[relations]
verifies = ["REQ-HUP-012", "REQ-HUP-013"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-27T14:37:56Z"
decided_by = "quality-owner"
reason = "Approved on 2026-08-27 by the accountable owner, 'i approve the packet, you can start WO-HUP-006', after the rehearsal of the transaction in a throwaway worktree and the owner's decision to move the candidate to development version 0.8.0 inside the work order. Adopts exact public 0.7.0 (wheel e8f4fdc9ad60879a3fa4627c063fa7bb9513e2bd109c47258cf7f7aa6ecf27f3, payload 26c11ec5e2363c3c0a9a416e69a3faa8bdf2d7a046710075bdeb661dd1003ee9) from the 0.6.0 lock 978cebb7824b7928d95ed43897b0f848441cc4ab7403a0cdd08a55a77df2b79e through one reviewed standard-root transaction of 43 add or update paths, no customization."
+++

# Verification Contract: Verify standard-root adoption of exact public 0.7.0

## Independence

Every authoritative upgrade, doctor, integrity and root-validation command
runs from the isolated 0.7.0 wheel installation outside the checkout.
Checkout source provides non-authoritative comparison tests only.

## Requirement-to-evidence matrix

| Requirement | Method | Pass condition |
| --- | --- | --- |
| REQ-HUP-012 | identity proof, plan review, apply, no-op replay, lock and transaction evidence | only the reviewed paths and the lock change; lock schema 3 names 0.7.0 with the exact archive and payload digests; canonical evidence written; replay is a no-op |
| REQ-HUP-013 | complete-root doctor, validate, inspect, dashboard, preflight; suites on two runtimes; diff ledger; hosted lanes | zero formal errors; 0 doctor FAIL; suites OK; managed CI selects 0.7.0; non-root bytes unchanged |

## Required cases

- A wrong wheel digest, payload digest, runtime origin, work order, prior
  lock or evidence path fails before any write.
- The plan lists exactly the reviewed paths and reports no `customized` and
  no `conflict`.
- Apply succeeds atomically; the plan replay reads all files unchanged.
- The lock reads schema 3, `tool_version = "0.7.0"`, the exact archive and
  installed-payload digests.
- Exact 0.7.0 validates the complete graph, including every retained
  rejected record, without a compatibility view.
- The repository suites pass on the default runtime and on Python 3.11.
- Product source and templates, package version, release, verification and
  contract records, tags, publication and Pages workflows and maintenance
  refs are byte-identical to the base commit.

## Hosted evidence

After the candidate commit is pushed, the managed Engineering Harness lane
and the candidate lanes run on the pull request. Hosted success verifies no
record and authorizes no merge.

## Evidence retention

Canonical transaction JSON at
`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-006-evaluator-upgrade.json`
and the human-readable ledger at
`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-006-verification.md`.
