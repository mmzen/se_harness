+++
id = "WO-REB-009"
type = "work_order"
title = "Use candidate semantics for immutable release-archive qualification"
status = "implemented"
owners = ["engineering-owner", "quality-owner", "release-owner"]
created = "2026-08-22"
updated = "2026-08-22"

[assurance]
commit_bound_verification = "required"
rationale = "A trusted publication gate selects which validator qualifies the immutable release archive immediately before privileged publication jobs."
decided_by = "engineering-owner"

[relations]
implements = ["REQ-REB-015"]
specifications = ["SPEC-REB-007"]
architecture = ["ARCH-REB-006", "ADR-REB-006"]
verification = ["VER-REB-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-22T19:51:14Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-22T19:51:15Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-22T20:00:23Z"
decided_by = "engineering-owner"
+++

# Work Order: Use candidate semantics for immutable release-archive qualification

## Lifecycle

This bounded corrective work is implemented with exact qualification retained in `../evidence/WO-REB-009-candidate-validator.md`. Commit-bound assurance remains required before a publication retry may reach privileged jobs; implementation status does not itself grant assurance or publication authority.

## Objective

Make the release workflow's credential-free exact-candidate qualification validate the exported candidate with that candidate's own package semantics, while leaving the independently released predecessor responsible for the separate publication compatibility view.

## In scope

- Retain failed run `32594814369`, qualification job `97084046727`, and its exact E009 boundary.
- Replace only the release-archive qualification invocation of the locked root validation script with `python -m se_harness validate .` inside the exact exported candidate.
- Add a static regression assertion that the credential-free qualification job uses candidate semantics and does not invoke the locked root script.
- Reproduce both commands on immutable C6, run focused and complete tests, and retain the result.

## Out of scope

- Changing candidate C6, `v0.6.0`, `RLS-SEH-012`, distributions, rejected history, the publication-view adapter, root lock or managed files, release status, or external policy.
- Skipping validation, accepting E009, moving credentials upstream, bypassing the trusted workflow, or changing any privileged publication job.

## Required verification

- Prove the locked root script fails exact C6 with only retained E009.
- Prove exact C6 `python -m se_harness validate .` passes with 645 artifacts and zero errors.
- Prove candidate `doctor` remains advisory and the complete candidate tests pass.
- Prove workflow permissions and job dependencies remain unchanged.
- Prepare and verify a later commit-bound VREC before publication retry.

## Evidence

Retain results in `../evidence/WO-REB-009-candidate-validator.md`.
