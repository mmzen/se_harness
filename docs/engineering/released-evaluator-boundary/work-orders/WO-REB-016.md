+++
id = "WO-REB-016"
type = "work_order"
title = "Retain the proven predecessor view for Pages generation"
status = "implemented"
owners = ["engineering-owner", "quality-owner", "release-owner"]
created = "2026-08-22"
updated = "2026-08-22"

[assurance]
commit_bound_verification = "required"
rationale = "The public Explorer must be generated from the exact predecessor-compatible view already proven by the immutable released evaluator, not from the rejected-history-bearing checkout that evaluator cannot parse."
decided_by = "engineering-owner"

[relations]
implements = ["REQ-REB-015"]
specifications = ["SPEC-REB-007"]
architecture = ["ARCH-REB-006", "ADR-REB-006"]
verification = ["VER-REB-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-22T21:28:00Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-22T21:28:01Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-22T21:57:58Z"
decided_by = "engineering-owner"
+++

# Work Order: Retain the proven predecessor view for Pages generation

## Lifecycle

This bounded post-release correction is implemented with exact qualification retained in `../evidence/WO-REB-016-pages-generation-view.md`. Commit-bound assurance remains required before trusted-main integration and Pages recovery.

## Objective

Let the existing predecessor-publication adapter retain its already validated exact sparse checkout at an absent external directory, and make both release publication and standalone recovery generate the Explorer from that read-only checkout.

## In scope

- Retain publication run `32599307612`, Pages build job `97095372576`, and its exact E009/two-E010 full-checkout generation refusal.
- Add one closed `--view-output` owned by the existing adapter; derive omissions only from released governance and retained preparation evidence.
- Prove the retained checkout has the selected governance commit, exact sparse specification, clean status, no unexpected omissions, and external location.
- Use the retained checkout only as the root of deterministic dashboard generation in both Pages workflows.
- Preserve GitHub Release, PyPI, maintenance, C6, tag, RLS, distributions, rejected history, and root evaluator identities.

## Out of scope

No release candidate, tag, RLS/VREC/REL, distribution, root evaluator, rejected-history artifact, maintenance policy, package byte, or published package mutation is permitted by this correction. No caller-supplied omission or expected diagnostic is accepted.

## Required verification

- Run adapter, release-orchestration, and Pages workflow-policy regressions.
- Run the complete suite and current graph, distribution, portable-surface, whitespace, and clean-checkout checks.
- Replay the exact released 0.5 evaluator against the retained view, then generate and package the Explorer from that same view.
- Prepare and verify a commit-bound VREC before pushing trusted main and dispatching the bounded standalone Pages recovery.

## Evidence

Retain results in `../evidence/WO-REB-016-pages-generation-view.md`.
