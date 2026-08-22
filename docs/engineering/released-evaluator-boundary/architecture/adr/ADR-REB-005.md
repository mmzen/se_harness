+++
id = "ADR-REB-005"
type = "adr"
title = "Retain exact legacy refusal and add a released-evaluator assessment-view lane"
status = "approved"
owners = ["technical-owner", "security-owner", "quality-owner", "release-owner"]
created = "2026-08-22"
updated = "2026-08-22"

[relations]
decides = ["ARCH-REB-005"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-22T07:15:02Z"
decided_by = "technical-owner"
+++

# ADR: Retain exact legacy refusal and add a released-evaluator assessment-view lane

## Status

Accepted for bounded local implementation and qualification under `WO-REB-007`. Candidate commit, hosted dispatch, credential, lifecycle, release, publication, maintenance, external-policy, and root-evaluator actions remain separately governed.

## Context

The managed Engineering Harness workflow correctly installs exact 0.5.0 and validates the full checkout. Once rejected `RLS-SEH-009` became immutable history, that evaluator could no longer parse the graph. C4 already proves the same evaluator can safely prepare through a two-artifact view, but hosted qualification did not use it. Changing history or the evaluator is forbidden; changing the managed workflow would mutate the root boundary before publication.

## Decision drivers

- Preserve exact released 0.5.0 and root-managed bytes.
- Preserve rejected history and the failed C4 candidate/run identities.
- Obtain meaningful hosted predecessor evidence without claiming full-graph 0.5 acceptance.
- Reject generic CI suppression and unexpected failures.
- Keep candidate orchestration bounded by independently reproducible Git/hash evidence.
- Repair Linux failure injection without weakening production exclusivity.

## Considered options

1. **Edit or delete rejected records.** Rejected as historical rewrite.
2. **Patch or upgrade released 0.5.0.** Rejected as reversal of the predecessor trust direction.
3. **Modify the root-managed Engineering Harness workflow.** Rejected for C5 because it changes the schema-2 managed boundary and lock before release.
4. **Treat every old-workflow failure as expected.** Rejected because it could hide identity, integrity, or unrelated graph failures.
5. **Skip hosted predecessor evidence.** Rejected because `REL-SEH-010` requires hosted qualification.
6. **Add an exact-view released-evaluator evidence lane and require the old lane to fail in one exact way.** Selected because it preserves all facts, executes the immutable predecessor, and makes the compatibility boundary explicit and testable.

## Decision

Add a candidate-owned, read-only hosted workflow that installs and identifies exact released 0.5.0, invokes shared predecessor-view logic, runs fixed `doctor`, `validate`, and dashboard commands against the exact two-artifact view, emits canonical evidence, and proves the complete checkout unchanged. Candidate validation independently covers the full graph.

The unchanged legacy workflow remains red. Qualification accepts only its exact `E009` on rejected `RLS-SEH-009` after successful identity and managed-integrity checks, together with a green assessment-view lane. Any additional or changed failure blocks. Reports must never describe the legacy workflow or complete graph as predecessor-accepted.

Refactor exclusive-create injection behind an adapter-local seam and patch only that seam in tests. Production `O_EXCL`, permissions, rollback, and command behavior remain unchanged.

## Consequences

### Positive

- Released 0.5.0 and root-managed state remain immutable.
- Hosted evidence exercises real predecessor behavior on the same exact compatibility boundary as preparation.
- The otherwise confusing red workflow is retained and precisely dispositioned rather than hidden.
- Linux and Windows failure evidence become comparable.

### Negative

- GitHub will continue displaying the legacy Engineering Harness workflow as failed for this transitional candidate.
- Release review must reconcile one exact expected-red observation plus a green replacement lane.
- A new hosted workflow and canonical evidence schema increase transitional machinery.
- C4 is invalidated; C5 and new aggregate identities are required.

### Operational and security consequences

- Workflow/job URLs, logs, artifacts, action pins, evaluator acquisition, and view construction become governed evidence.
- No external required-check or branch policy is changed by this decision.
- Any ambiguity stops before credentials, verification, release preparation, or publication.

## Validation

Execute `VER-REB-005`. Require exact reproduction of both C4 failures, green local 0.5 view prototype, diagnostic mutation negatives, Git/path/object adversarial cases, Linux/Windows full suites, candidate package evidence, hosted assessment artifacts, and zero diff to root-managed state and rejected history.
