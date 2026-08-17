+++
id = "WO-DST-014"
type = "work_order"
title = "Emit and validate the progressive Explorer bundle"
status = "implemented"
owners = ["engineering-owner", "technical-owner", "security-owner", "quality-owner"]
created = "2026-08-17"
updated = "2026-08-17"

[assurance]
commit_bound_verification = "required"
rationale = "The work changes the generated dashboard data protocol, deterministic provenance, output transaction, managed distribution, public Pages packaging, path and integrity trust boundaries, and performance limits used by future review and publication decisions."
decided_by = "repository-owner"

[relations]
implements = ["REQ-DST-048", "REQ-DST-049", "REQ-DST-054", "REQ-DST-055"]
specifications = ["SPEC-DST-013"]
verification = ["VER-DST-013"]
architecture = ["ARCH-DST-010", "ADR-DST-010"]
+++

# Work Order: Emit and validate the progressive Explorer bundle

## Lifecycle

On 2026-08-17 the repository owner challenged the approximately 2.6 MB generated page and accepted the proposal for deterministic static sharding, coarse view resources, per-artifact details, explicitly expanded evidence, integrity verification, and two coordinated implementation scopes by instructing `ok, go for the artifact packet`. Packet authoring was interrupted after the requirement layer. The owner then instructed `go for implementation`, accepting the completed `REQ-DST-048..055`, `SPEC-DST-013..014`, `ARCH-DST-010`, `ADR-DST-010`, `VER-DST-013..014`, and both bounded work orders once structural validation passes.

This work order is therefore approved to enter `in_progress`; it does not authorize a candidate commit, VREC, push, pull request, release, package publication, public demonstrator deployment, or mutation of open PR 63. The ready `VREC-DST-011` for the prior candidate is isolated separately and must remain unchanged.

## Objective

Replace the duplicated monolithic dashboard output with a deterministic, integrity-addressed, transactionally verified static bundle and make the existing explicit Pages packager validate and publish only that exact bundle.

## In scope

- Partition the existing canonical in-memory projection into bounded shell, summary, compact topology, readiness, per-artifact detail, and shared evidence resources.
- Introduce the versioned v2 manifest/bootstrap/resource schemas and deterministic serialization.
- Enforce controlled/content-addressed paths, size/hash descriptors, exact recursive sets, and noncyclic manifest binding.
- Extend transactional nested output verification and rollback across the complete resource tree.
- Enforce shell/summary/content hard budgets and current-repository topology acceptance target; report resource counts and bytes.
- Update the repository-specific Pages packager for independent manifest/revision/path/size/hash/exact-set validation.
- Preserve explicit publication authority and update directly applicable generation/publication/local-serving documentation.
- Reconcile canonical and active managed copies and retain evidence keyed to `WO-DST-014`.

## Out of scope

- Browser progressive loading and UI state beyond the minimal bootstrap contract; that is `WO-DST-015`.
- Changing formal artifacts or graph semantics, validation/inspection/preflight rules, evidence meaning, lifecycle, VREC/RLS eligibility, release policy, or aggregate scores.
- Topology sharding, backend/API/database, service worker, persistent browser storage, authentication, telemetry, secret scanning, redaction, or automatic deployment.
- Releasing or publishing a new package or demonstrator, changing the accepted graph CDN URL, or modifying self-hosting governor controls.

## Authorized decision envelope

The implementation agent may select internal data classes, deterministic helper structure, exact compact property names, controlled resource directory names, and summary partition details within `SPEC-DST-013`. It may update the existing Pages packager only to validate/copy manifest-declared v2 resources. It must not weaken validation, infer authority, add a server/dependency/origin, or retain the full embedded snapshot as a compatibility shortcut.

## Constraints

- Python 3.11+ standard-library runtime only unless separately reviewed and authorized.
- Preserve one standard managed installation and canonical/active parity through supported upgrade.
- Treat repository, target, manifest, generated files, and publication inputs as untrusted.
- Preserve prior candidate commit `d5b8d0e369f339923700445d68d084888b560657`, PR 63, and stashed `VREC-DST-011` unchanged.
- No output publication or network action during generation/tests except explicit local/browser test serving.

## Expected change surface

- canonical and active dashboard generators and Explorer bootstrap template;
- repository-specific Pages packager;
- focused dashboard generation/publication/distribution tests;
- managed lock entries through supported reconciliation;
- dashboard/publication/CLI reference notes where behavior changes;
- DST-014 artifacts, domain index, and retained evidence.

No formal validator, inspector, governance workflow, governor descriptor, release automation, or public deployment is expected.

## Required verification

Execute all cases in `VER-DST-013`, applicable regressions from `VER-DST-008`, `VER-DST-012`, and current publication tests, formal validation, start/review preflight, deterministic twice-generation and recursive diff, exact manifest/hash/path/security failures, rollback, size budgets, current-repository and consumer generation, Pages packager tamper/revision/exact-set cases, managed upgrade plan/apply/idempotence, canonical/active/lock parity, package contents if changed, full tests, doctor, inspect, and `git diff --check`.

## Evidence to record

Retain baseline and resulting bytes; resource schemas and recursive hash lists; commands/versions/exit codes; tamper/path/collision/race/rollback fixtures; publication selection and exact output set; static-server behavior; managed/package parity; deterministic digests; changed paths; deviations; residual risks; and actions not performed in `docs/engineering/harness-distribution/evidence/WO-DST-014-verification.md`.

## Stop and escalate conditions

Stop if the design requires a server, new runtime dependency/origin, unverified or ID-derived path, manifest self-cycle, partial output/publication, weakened Pages governance, persistent cache, topology sharding, formal semantic change, protected-control change, failed hard budget/test, or any commit/VREC/PR/release/publication/deployment action without explicit authority.

## Completion report format

Report requirement/architecture mapping; v2 schemas and partition; deterministic tree/digests; path/hash/transaction security; budgets and before/after size; Pages validation; static serving; managed/package parity; tests; documentation; changed paths; deviations; residual risks; and all external actions not performed.

## Completion

The deterministic v2 bundle, independent Pages validation, recursive transaction checks, managed distribution, verification-capture manifest binding, documentation, tests, and retained evidence are complete. This state records completed implementation only; commit-bound assurance remains required and no commit, VREC, push, pull request, release, package publication, or Pages deployment was performed.
