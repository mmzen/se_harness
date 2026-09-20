+++
id = "VER-KIS-008"
type = "verification"
title = "Verify recovery PR admission and distinct onboarding routes"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-20"
updated = "2026-09-20"

[relations]
verifies = ["REQ-DST-069"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-20T15:28:22Z"
decided_by = "assurance-owner"
reason = "On 2026-09-20 the owner instructed \"you can resolve this\" after the PR #488 scope blocker was reported, continuing the authorized push and PR. Record the bounded corrective scope and applicable check plan for carrying the already reviewed recovery package, preserving accepted README bytes, and reconciling the upstream onboarding test. This uses the supplied correction authority; it does not claim the owner separately reviewed these newly authored record bytes, accept the future corrected candidate, or authorize merge/release. Draft bytes recorded for reproducibility: aa5f967c1945d4d54433da5154a21cb652a3f6947825baaa9667ef7d041a412c"
+++

# Verify recovery PR admission and distinct onboarding routes

## Independent expectations

Use REQ-DST-069, SPEC-DST-024 and SPEC-DST-029. Native command expectations
remain the four commands in the retained published marketplace instructions;
they are not derived from the changed test's output. The already accepted
README SHA-256 is 6566a636021d3aaa29345094ad19362289cd26efe01b3684a26da57e7c2d2c9d.
Owner review applies; no independent human reviewer is claimed.

## Requirement-to-evidence matrix

| Requirement | Method | Pass condition |
| --- | --- | --- |
| REQ-DST-069 | Test and inspection | The plugin subsection matches all four published commands exactly even when the separate accepted CLI subsection is present. Missing commands or wrong native arguments still fail. Existing manual-guide parser, link, presentation and authority checks continue passing. |

## Integration and preservation checks

- Compare the unchanged README and each carried formal definition, decision and
  source-evidence file with its pre-correction hash. Only the two untyped index
  summaries may be brought up to date. Existing verified VRECs and their retained
  evidence keep their bytes and earlier candidate commits.
- Inspect the full Git diff against main through released 0.18.0 check-pr with
  WO-KIS-014, WO-DOC-017 and WO-KIS-015. Every changed path must be admitted.
  Never add an unrelated completed order merely because it admits a filename.
- Run existing public-onboarding and progressive-documentation tests. Also
  demonstrate that removing a native install command or changing its marketplace
  argument still fails the corrected test. Do not delete the expected command
  count or replace equality with substring presence.
- Run the full Windows source suite and the existing hosted Linux Python 3.11
  full-scale candidate lane; record actual skips. Run the required distribution
  validator, CLI help, released doctor/graph/review and whitespace checks.
- Obtain passing hosted checks on the pushed correction before marking the
  integration repair complete. Reuse the normal evidence and handoff routes.

## Retention and limits

Retain concise results and raw logs under evidence/WO-KIS-015/. Record actual
argument arrays, input hashes, candidate and runtime identities; preserve both
original CI failures. This plan does not accept a new candidate, merge a PR,
publish a package, or change the three unstarted recovery orders.
