+++
id = "REQ-HUP-013"
type = "requirement"
title = "Prove complete-graph operation under the 0.7.0 root"
status = "approved"
owners = ["repository-owner", "engineering-owner", "quality-owner"]
created = "2026-08-27"
updated = "2026-08-27"
statement = "WHEN the 0.7.0 root candidate is produced, THE SYSTEM SHALL prove exact public 0.7.0 doctor, integrity, complete-graph validation, inspection, dashboard, preflight and supported-runtime behavior on the complete checkout with zero formal errors and no compatibility view."
verification_method = "automated-test"
priority = "must"
source = "INT-HUP-004; REQ-HUP-006"
measure = "0 structure, governance and policy errors; 0 doctor FAIL; suites OK on the default runtime and Python 3.11"

[relations]
derives_from = ["CAP-HUP-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-27T14:37:56Z"
decided_by = "repository-owner"
reason = "Approved on 2026-08-27 by the accountable owner, 'i approve the packet, you can start WO-HUP-006', after the rehearsal of the transaction in a throwaway worktree and the owner's decision to move the candidate to development version 0.8.0 inside the work order. Adopts exact public 0.7.0 (wheel e8f4fdc9ad60879a3fa4627c063fa7bb9513e2bd109c47258cf7f7aa6ecf27f3, payload 26c11ec5e2363c3c0a9a416e69a3faa8bdf2d7a046710075bdeb661dd1003ee9) from the 0.6.0 lock 978cebb7824b7928d95ed43897b0f848441cc4ab7403a0cdd08a55a77df2b79e through one reviewed standard-root transaction of 43 add or update paths, no customization."
+++

# Requirement: Prove complete-graph operation under the 0.7.0 root

## Rationale

An adopted root that cannot judge the complete graph would block every
later act. The proof must come from the exact released evaluator run
directly on the checkout, not from candidate source and not through a
predecessor view, and it must show the managed CI gate selecting 0.7.0.

## Required response

- Run exact public 0.7.0, installed outside the checkout, directly against
  the complete checkout: `doctor`, `validate`, `inspect`, `dashboard`, and
  review preflight for `WO-HUP-006`.
- Require zero structure, governance and policy errors; account for every
  maintenance warning by code and count.
- Prove the managed Engineering Harness workflow selects exact 0.7.0.
- Run the complete repository suites on the default runtime and on Python
  3.11, and the repository-required checks.
- Compare product source and templates, package version, release records,
  tags, publication and Pages workflows and maintenance refs with the base
  commit: unchanged.

## Failure behavior

Any formal error, any doctor failure, a red suite, a managed lane that
selects another version, or a changed non-root byte is a stop condition for
`WO-HUP-006` and is reported, not worked around.
