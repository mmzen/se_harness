+++
id = "WO-REB-011"
type = "work_order"
title = "Remove inapplicable candidate-root doctor gate"
status = "implemented"
owners = ["engineering-owner", "quality-owner", "release-owner"]
created = "2026-08-22"
updated = "2026-08-22"

[assurance]
commit_bound_verification = "required"
rationale = "The trusted publication workflow must distinguish complete candidate validation from the intentionally separate released-root compatibility assessment before privileged jobs."
decided_by = "engineering-owner"

[relations]
implements = ["REQ-REB-015"]
specifications = ["SPEC-REB-007"]
architecture = ["ARCH-REB-006", "ADR-REB-006"]
verification = ["VER-REB-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-22T20:15:00Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-22T20:15:01Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-22T20:20:02Z"
decided_by = "engineering-owner"
+++

# Work Order: Remove inapplicable candidate-root doctor gate

## Lifecycle

This bounded corrective work is implemented with exact qualification retained in `../evidence/WO-REB-011-candidate-doctor-boundary.md`. Commit-bound assurance remains required before another publication retry; implementation status does not itself grant assurance or publication authority.

## Objective

Remove the candidate-source `doctor` invocation from the exact release qualification job because it tests 0.6 templates against the intentionally locked 0.5 repository root, while retaining complete candidate validation and the resolver's independently released predecessor doctor/view gate.

## In scope

- Retain failed run `32596026852`, job `97087055231`, and the exact expected root/template drift.
- Remove only `python -m se_harness doctor .` from the credential-free candidate qualification step.
- Assert statically that candidate validation/tests/help remain and candidate-root doctor is absent.
- Preserve the resolver's exact released-0.5 `doctor` plus publication-view validation unchanged.

## Out of scope

- Ignoring candidate graph errors, removing either publication-view plane, changing C6/tag/RLS/distributions/history/root, changing build inputs or privileged jobs, or accepting arbitrary doctor failures.
- Root upgrade, template installation, or any external mutation.

## Required verification

- Prove candidate validation and all C6 tests passed before the hosted doctor failure.
- Reproduce C6 doctor exit 1 with only documented root/template drift.
- Prove the resolver's predecessor doctor/view command remains mandatory.
- Run focused policy, complete suite, graph, distribution, and portable-surface checks.
- Prepare and verify a later commit-bound VREC before retry.

## Evidence

Retain results in `../evidence/WO-REB-011-candidate-doctor-boundary.md`.
