+++
id = "SPEC-HUP-001"
type = "specification"
title = "Standard-root 0.5.0 evaluator upgrade contract"
status = "approved"
owners = ["technical-owner", "engineering-owner"]
created = "2026-08-20"
updated = "2026-08-20"

[relations]
specifies = ["REQ-HUP-001", "REQ-HUP-002", "REQ-HUP-003"]
+++

# Specification: Standard-root 0.5.0 evaluator upgrade contract

## Scope

Define one repository-local, plan-first transition from the currently installed standard root `0.5.0a1` to the immutable public evaluator `0.5.0`, without changing product, release, publication, or historical compliance state.

## Actors and external systems

- Accountable repository, engineering, assurance, and security owners.
- Public PyPI/GitHub distribution state for exact 0.5.0.
- The external 0.5.0 Python environment and `harnessctl` entry point.
- The repository worktree, managed lock, GitHub Actions, and candidate evidence workflow.

## Inputs

- Current clean main-derived root and `.engineering-harness.lock`.
- Public wheel `se_harness-0.5.0-py3-none-any.whl` with SHA-256 `974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f`.
- Exact public evaluator environment outside the checkout.
- Approved `WO-HUP-001` and phase-appropriate preflight.

## Outputs

- A reviewable candidate whose managed root consistently identifies 0.5.0.
- Retained evidence at `docs/engineering/repository-harness-upgrade/evidence/WO-HUP-001-verification.md`.
- No package, release, tag, publication, deployment, issue, or external configuration mutation.

## State model

`draft packet -> approved work order -> read-only plan -> in-progress bounded apply -> implemented evidence -> candidate commit -> ready VREC -> accountable verification -> merge`

This specification authorizes none of those transitions by itself.

## Behavioral rules

1. Use only an externally installed public 0.5.0 evaluator whose role identity passes before repository mutation.
2. Record the dry-run plan and require it to remain limited to the three currently observed version-divergent managed files plus transactional lock maintenance.
3. Apply only with `harnessctl upgrade . --apply`; do not hand-edit generated managed content as a substitute.
4. Compare pre/post managed inventory, lock digests, changed paths, and repository-owned hashes.
5. Update repository-owned contextual prose only when separately listed in the approved work order; it remains outside managed installation.
6. Run doctor, validate, preflight, inspect, dashboard, repository tests, workflow parsing, source/package acceptance, and identity checks.
7. Treat all candidate code and packages as untrusted evidence; never import them into the evaluator process.
8. A candidate change after exact qualification requires renewed evidence and, after capture, a new VREC.
9. Stop before commit, push, PR, merge, verification transition, or any release action unless separately authorized.

## Error and recovery behavior

- Identity mismatch: stop before plan/apply.
- Unsafe or expanded plan: retain output and escalate without mutation.
- Transaction failure: prove resulting lock/worktree state, restore only through supported recovery or an authorized reviewed revert.
- Check failure: keep formal state unchanged and remediate only within approved scope.

## Data and interface contracts

The managed root must report `tool_version = "0.5.0"`; the Engineering Harness workflow must install exact `se-harness==0.5.0`; `ENGINEERING_HARNESS.md` must name the same version; the integrity lock must match their canonical rendered bytes.

## Security and privacy properties

No credential is required. Network acquisition occurs only for the public immutable distribution. Logs retain hashes and paths but no tokens, environment secrets, or private host-specific paths in committed evidence.

## Performance and capacity

The operation is bounded to the existing managed installation and normal test suite; no runtime capacity behavior changes.

## Observability

Retain evaluator identity, dry-run/apply result, changed-file ledger, lock/integrity results, graph planes, tests, workflow checks, and hosted run URLs when later available.

## Compatibility and migration

The transition uses the ordinary standard-repository upgrade path shipped by public 0.5.0. It removes no artifact, moves no repository-owned content, and creates no self-hosting profile. Prior 0.5.0a1 files remain recoverable from Git history.

## Examples and counterexamples

- Valid: external public 0.5.0 plans three safe updates, applies them transactionally, and candidate CI imports no checkout module.
- Invalid: changing only `SE_HARNESS_VERSION` in YAML.
- Invalid: running checkout `python -m se_harness upgrade`.
- Invalid: combining the root change with a 0.5.1 version bump or RLS preparation.

## Explicitly unspecified decisions

Implementation may select disposable directory names, evidence table layout, and ordering of independent read-only checks. It may not select a different evaluator artifact, expand changed surfaces, or alter lifecycle/production state.
