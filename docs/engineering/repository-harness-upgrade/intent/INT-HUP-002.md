+++
id = "INT-HUP-002"
type = "intent"
title = "Adopt released se-harness 0.6.0 as the repository governor"
status = "approved"
owners = ["repository-owner", "engineering-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T17:17:09Z"
decided_by = "repository-owner"

[relations]
+++

# Intent: Adopt released se-harness 0.6.0 as the repository governor

## Problem

The product release `0.6.0` is independently published and verified, but this repository is still governed by released `0.5.0` with a schema-2 lock. Consequently the managed root CI cannot interpret the complete retained 0.6.0 history and the repository still needs transitional predecessor views.

## Desired outcomes

- Exact public `se-harness==0.6.0` becomes the standard root evaluator through the supported upgrade transaction.
- Root configuration, managed files, workflow, and a schema-3 lock agree on the exact public evaluator identity.
- Complete-graph root validation succeeds without a predecessor compatibility view.
- Repository-owned content, post-release migration byte rules, product code, releases, tags, and external state remain unchanged.

## Non-goals

This intent does not change product version or source, rewrite governance history, retire repository-specific transitional workflows, release or publish anything, move a tag, deploy Pages, change maintenance state, or approve a VREC or merge.

## Immutable identity

- wheel: `se_harness-0.6.0-py3-none-any.whl`
- wheel SHA-256: `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`
- installed payload SHA-256: `c233678548fe742b7a7a5a8bd65de10156ff233edc65b68e2ed0333fbe4dea42`

## Approval boundary

The repository owner's instruction to proceed authorizes preparation and review of this draft packet. The exact packet, managed plan, `.gitattributes` integration adjustment, and `--apply` transaction require explicit approval before mutation.
