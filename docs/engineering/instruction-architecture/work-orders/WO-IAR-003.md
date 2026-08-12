+++
id = "WO-IAR-003"
type = "work_order"
title = "Move review procedure into the focused workflow"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
implements = ["REQ-IAR-011"]
specifications = ["SPEC-IAR-003"]
architecture = ["ARCH-IAR-003", "ADR-IAR-003"]
verification = ["VER-IAR-003"]
+++

# Work Order: Move review procedure into the focused workflow

## Objective

Remove duplicated review procedure from the managed router, make `WORKFLOW.md` the owner of exact review and visualization commands, and preserve the evidence-versus-authority boundary.

## Authorization

The repository owner approved the `IAR-003` chain and this bounded implementation on 2026-08-12 with `ok, make the change accordingly then`. Commit, push, pull-request creation, verification capture or transition, release, tag, publication, and deployment remain unauthorized.

## In scope

- Change canonical router and workflow templates according to `SPEC-IAR-003`.
- Add focused content and exact-prior two-file migration tests.
- Apply the supported self-upgrade to reconcile both operational files and lock entries.
- Update acceptance/index material and retain `WO-IAR-003` evidence.

## Out of scope

CLI or lifecycle behavior, output schemas, quality-gate semantics, traceability, ownership modes, installation profiles, historical facts, commits, pushes, PRs, verification transitions, releases, tags, publication, and deployment.

## Authorized decision envelope

Implementation may refine assertion structure and minor prose without changing the accepted responsibility, command, evidence, or authority meanings.

## Expected change surface

Two canonical managed templates, two self-hosted managed files, schema-2 lock, focused tests, acceptance/index material, this formal chain, and retained evidence.

## Implementation plan

1. Run start preflight for this approved chain.
2. Add failing content and two-file upgrade tests.
3. Update canonical router and workflow templates.
4. Apply the supported self-upgrade and confirm no-op repetition.
5. Execute `VER-IAR-003`, retain evidence, mark implementation artifacts complete, and run review preflight.
6. Stop before any separately authorized commit or governance action.

## Required verification

Perform every check in `VER-IAR-003`, including focused and dual-runtime full tests, formal graph validation, doctor, CLI help, deterministic Explorer, managed parity, review preflight, and diff hygiene.

## Stop and escalate conditions

Stop if procedure or authority meaning changes, customized content could be overwritten, only one managed file would update, a lock digest requires hand editing, unrelated policy or historical facts would change, a check fails, or external authority is required.

## Completion report format

Report delivered responsibility, changed paths, test and migration results, evidence, lifecycle state, residual risk, and explicitly unperformed actions.

## Implementation result

The managed router now routes review readiness and visualization to the focused workflow and quality gates while retaining the evidence-versus-authority invariant. `WORKFLOW.md` owns the exact review-preflight and dashboard commands plus candidate consistency/anomaly inspection. The supported self-upgrade reconciled both operational files and both schema-2 lock entries transactionally. Complete results are retained in `docs/engineering/instruction-architecture/evidence/WO-IAR-003-verification.md`.
