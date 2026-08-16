+++
id = "WO-OCA-002"
type = "work_order"
title = "Enforce operating assurance type and readiness"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
implements = ["REQ-OCA-002"]
specifications = ["SPEC-OCA-002"]
verification = ["VER-OCA-002"]
+++

# Work Order: Enforce operating assurance type and readiness

## Lifecycle and authorization

The repository owner approved correction points 1 and 2, explicitly withheld approval for the other proposed operating-model extensions, and on 2026-08-16 instructed the team to engage in the explicit OPS migration as the simplest approach. That instruction approves this packet and authorizes implementation of the exact `SPEC-OCA-002` boundary. It does not authorize a commit, push, pull-request mutation, VREC creation or transition, release, tag, publication, or deployment.

No architecture artifact or ADR applies. The work adds a local validation invariant and controlled migration within the existing validator, artifact graph, policy loader, and managed-distribution boundaries. It introduces no new component, dependency, interface, trust boundary, persistence model, or operating model.

## Objective

Make an active operating assurance claim structurally typed and demonstrably connected to active requirements, completed implementation, and configured commit-bound verification evidence.

## In scope

- Implement the exact target-type and readiness rules in `SPEC-OCA-002`.
- Add focused taxonomy, lifecycle, reachability, policy, and regression tests.
- Migrate only `OPS-DST-001` and `OPS-REV-001` to their original requirement scopes.
- Correct the scoped factual wording in `WO-OCA-001` evidence.
- Update concise managed policy text needed to make the executable rule discoverable.
- Synchronize root/canonical validator and managed integrity through the supported upgrade path.
- Retain work-order evidence and stop at an uncommitted implementation state.

## Out of scope

Every unapproved point from the prior proposal: release-to-OPS relations, release-contract changes, diagram redesign, operational assessment records, recurring-evidence schema, staleness monitoring, automatic remediation, or aggregate scoring. Also excluded are OPS status transitions, new assured requirements, release artifacts, VREC/RLS changes, commits, pushes, PR edits, releases, publication, and deployment.

## Authorized decision envelope

Implementation may choose helper names, deterministic iteration structure, and focused fixture organization. It may not weaken state eligibility, treat a ready VREC as evidence, infer domain-wide coverage, broaden the two migrations, or add another operating-model feature.

## Expected change surface

- Root and canonical artifact validators and managed lock.
- Focused validator, taxonomy, revision-policy, parity, package, and upgrade tests.
- Root and canonical `TRACEABILITY.md` wording, without changing its diagram or relation catalog.
- `OPS-DST-001`, `OPS-REV-001`, their domain indexes if needed, and the scoped OCA-001 evidence correction.
- This incremental OCA packet and implementation evidence.

## Required verification

Execute the complete `VER-OCA-002` matrix, Python 3.11 and 3.14 full suites, formal validation, doctor, start/review preflight, inspection determinism, root/canonical parity, fresh-install/upgrade checks, package-data checks, and `git diff --check`.

## Stop and escalate conditions

Stop if an accepted contract has no eligible path, the rules require a new formal relation or artifact type, current release records must change, repository policy cannot be reused, an unrelated validator result changes, or the two approved controls cannot be implemented without an unapproved extension.

## Completion record

Implementation completed on 2026-08-16 within the authorized envelope. The validator now enforces requirement-only targets and evidence-backed readiness for active OPS records; the two legacy contracts were explicitly migrated without expanding their accepted scopes. Evidence is retained in `../evidence/WO-OCA-002-verification.md`. This implemented state records completed work only and does not independently verify the candidate or authorize a commit, push, pull request, release, publication, or deployment.
