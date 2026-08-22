+++
id = "WO-REB-006"
type = "work_order"
title = "Implement predecessor preparation view and qualify successor candidate"
status = "implemented"
owners = ["engineering-owner", "repository-owner", "quality-owner", "security-owner", "release-owner"]
created = "2026-08-22"
updated = "2026-08-22"

[assurance]
commit_bound_verification = "required"
rationale = "Release decisions will rely on changed version-cardinality policy, a new security-sensitive Git compatibility adapter, canonical preparation evidence, and successor-candidate provenance."
decided_by = "engineering-owner"

[relations]
implements = ["REQ-REB-011", "REQ-REB-012"]
specifications = ["SPEC-REB-005"]
architecture = ["ARCH-REB-004", "ADR-REB-004"]
verification = ["VER-REB-004"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-21T22:17:21Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-21T22:19:07Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-22T16:29:22Z"
decided_by = "engineering-owner"
+++

# Work Order: Implement predecessor preparation view and qualify successor candidate

## Lifecycle

Bounded implementation is complete in exact C6 `3b339e9fc70cc634e6dc6bda07ea6a9b1a465798` ancestry. Core local C4 implementation evidence remains at `docs/engineering/released-evaluator-boundary/evidence/WO-REB-006-local-qualification.md`; exact successor and hosted closure is retained at `docs/engineering/released-evaluator-boundary/evidence/WO-REB-007-corrective-proposal.md`. This implemented state does not prepare or transition a VREC or RLS and does not authorize another push, credential use, tag, publication, deployment, maintenance mutation, external-policy change, or root-evaluator upgrade.

## Objective

Allow exact rejected release attempts to remain audit history without consuming an unpublished version, and let exact released 0.5.0 prepare a successor through one deterministic two-artifact compatibility view while the complete graph remains candidate-validated and unchanged.

## In scope

- Update candidate/template version-cardinality validation so valid rejected records do not claim a version and at most one ready/released record does.
- Update candidate ordinary `prepare-release` semantics and tests to apply the same lifecycle rule for future schema-3 repositories.
- Implement one repository-owned plan/apply adapter conforming to `SPEC-REB-005`.
- Derive the exact rejected bootstrap pair; create/prove an exact-commit sparse worktree; run isolated external predecessor preparation; validate and atomically import only its output plus canonical view evidence.
- Extend RLS candidate validation, binder/replay, distribution/publication resolution, and operator guidance only as required to bind and enforce preparation-view evidence.
- Add deterministic lifecycle, Git/path/object, canonical-schema, isolation, TOCTOU, partial-write, rollback, Windows/LF, and publication-authority negative tests from `VER-REB-004`.
- Retain complete local evidence suitable for a later thirteen-work-order aggregate and C4 qualification.

## Out of scope

- Editing, moving, deleting, repointing, or reinterpreting C1/C2/C3, any VREC, any RLS, either rejected historical artifact, or their evidence.
- Using candidate code as the operational root evaluator or changing `.engineering-harness.toml`, `.engineering-harness.lock`, root managed files, released 0.5.0, or maintenance state.
- Preparing or deciding `RLS-SEH-010` or `RLS-SEH-011`, changing `REL-SEH-009`, approving `REL-SEH-010`, or transitioning any VREC/RLS/REL under this work order.
- Creating a candidate commit, pushing, using credentials, dispatching hosted lanes, tagging, publishing, deploying, or changing external policy without separate authority.

## Authorized decision envelope

After approval, implementation may choose internal helper names, temporary-directory naming, subprocess decomposition, and structured diagnostic detail. It may not change lifecycle cardinality, exact omission count/selection, manifest schema obligations, predecessor ownership, atomicity, rollback, or trust direction.

## Constraints

- Preserve Python 3.11+ standard-library runtime behavior.
- Treat Git, environment, paths, processes, repository bytes, metadata, JSON, and hashes as untrusted.
- Use bounded explicit paths and refuse linked/escaped/ambiguous targets.
- Preserve exact historical and candidate identities and prove recursive before/after state on negatives.
- Never report compatibility-view preparation as full predecessor validation.

## Expected change surface

- Candidate canonical validator and provenance version-cardinality logic.
- Repository-owned predecessor preparation adapter and bootstrap binding/replay support.
- Candidate template, release/distribution/publication checks strictly needed to validate the new RLS evidence binding.
- Focused and full tests, release/operator documentation, and one `WO-REB-006` evidence file.

The operational root configuration, lock, managed files, released evaluator, existing governance records, maintenance refs, and external systems are not expected change surfaces.

## Required verification

- Execute every method in `VER-REB-004` and unchanged `VER-REB-002`/`VER-REB-003` regressions.
- Prove full active-version and bootstrap lifecycle matrices.
- Prove exact sparse-view determinism, omitted Git/raw identities, predecessor isolation/output ownership, canonical evidence, and atomic rollback.
- Run candidate and released-evaluator boundary checks, full tests on Python 3.11/current runtime, formal graph, inspection, dashboard, distribution, portability, archive, recovery, diff, and secret/path checks.
- After separate candidate authority, build twice from exact C4, reproduce wheel/sdist/bundle/offline artifacts, run candidate package acceptance, and retain exact identities.
- Run hosted lanes only after separate branch/credential authority.

## Evidence to record

- Original RLS preparation command and exact failure.
- Approved preflight manifest and exact changed paths.
- All lifecycle/view/schema/path/isolation/TOCTOU/rollback test matrices.
- Exact source/view commits, trees, sparse bytes, omitted blob/raw hashes, evaluator/wheel/lock identities, command arguments, generated output, and canonical evidence hashes.
- Complete local/candidate/package/build/bundle/hosted identities when separately authorized.
- Exact list of lifecycle, commit, credential, external, maintenance, and root actions not performed.

## Stop and escalate conditions

- The view cannot be derived without arbitrary omission or historical mutation.
- Released 0.5.0 does not generate the exact requested RLS in the valid view.
- Candidate validation cannot accept terminal history plus one active successor without weakening multiple-active rejection.
- Atomic rollback, canonical evidence, runtime isolation, candidate/template parity, or any required qualification fails.
- Any solution requires root upgrade, credentials, external mutation, or scope beyond the approved packet.

## Completion report format

Report exact version-cardinality behavior, view schema and omissions, predecessor command/output, changed surfaces, root/history preservation, complete qualification, retained evidence, candidate identity when separately authorized, lifecycle state, and one next accountable decision.
