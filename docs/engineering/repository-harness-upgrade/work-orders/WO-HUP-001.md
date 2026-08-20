+++
id = "WO-HUP-001"
type = "work_order"
title = "Upgrade the standard root evaluator to released 0.5.0"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "quality-owner", "security-owner"]
created = "2026-08-20"
updated = "2026-08-20"

[assurance]
commit_bound_verification = "required"
rationale = "Every later 0.5.1 artifact, CI gate, assurance decision, and release decision will rely on the exact installed governor, managed integrity, and evaluator/candidate separation established by this change."
decided_by = "repository-owner"

[relations]
implements = ["REQ-HUP-001", "REQ-HUP-002", "REQ-HUP-003"]
specifications = ["SPEC-HUP-001"]
architecture = ["ARCH-HUP-001"]
verification = ["VER-HUP-001"]
+++

# Work Order: Upgrade the standard root evaluator to released 0.5.0

## Lifecycle

On 2026-08-20 the accountable owner explicitly approved `INT-HUP-001`, `CAP-HUP-001`, `REQ-HUP-001` through `REQ-HUP-003`, `SPEC-HUP-001`, `ARCH-HUP-001` including its no-significant-decision assessment, `VER-HUP-001`, and this work order for implementation. The same instruction keeps the RCV and 0.5.1 release artifacts draft.

This approval authorizes start preflight, the exact external public 0.5.0 identity proof, review of the already observed three-file managed plan, the supported bounded apply if that plan remains exact, verification, evidence retention, and transition of this work order through `in_progress` to `implemented`. It does not authorize a candidate commit, VREC preparation or transition, push, PR, merge, release, publication, deployment, protected-environment decision, issue #81 edit, force push, or history rewrite.

Start preflight then passed under the currently installed released `0.5.0a1` evaluator with `ready: true`, no diagnostics, and the complete 16-file governing manifest. The implementation actor read every manifest file before changing the work order to `in_progress` or applying managed-root changes.

Implementation then used the independently installed immutable public `0.5.0` evaluator to apply the exact reviewed three-file managed plan and transactional lock reconciliation. No-op replay, managed integrity, doctor, graph validation, inspection, dashboard generation, changed-surface review, and both 263-test supported-runtime suites passed on an exact HUP-only projection from the base revision. The separately drafted RCV and 0.5.1 packets remain draft and outside that projected candidate. Evidence is retained at `docs/engineering/repository-harness-upgrade/evidence/WO-HUP-001-verification.md`; candidate commit, candidate-package and hosted acceptance, VREC, and all remote or release actions remain pending separate authority.

## Objective

Use the independently installed immutable public 0.5.0 evaluator to upgrade the repository's standard managed root from 0.5.0a1 to 0.5.0, retain complete evidence, and produce one minimal reviewable candidate without changing product or release state.

## In scope

- Verify public 0.5.0 evaluator version, distribution root, entry point, checkout exclusion, and wheel SHA-256.
- Run start preflight under the current installed governor and read the complete manifest.
- Capture and review the public 0.5.0 `harnessctl upgrade .` plan.
- If separately approved and the plan remains exact, run `harnessctl upgrade . --apply` from the external 0.5.0 environment.
- Update repository-owned context only where necessary to truthfully name the installed final evaluator.
- Reconcile managed lock/integrity and prove safe no-op replay.
- Run `VER-HUP-001`, retain keyed evidence, and transition only this work order to `implemented` after completion.
- After separate authority, create one clean candidate commit and later prepare a ready VREC for `WO-HUP-001`.

## Out of scope

Any `se_harness/` behavior, package/template change, package version bump, RCV implementation, 0.5.1 release work, retroactive 0.5.0 RLS, historical record mutation, issue #81 edit, publisher or Pages change, tag, GitHub Release, PyPI upload, environment approval, deployment, merge, force push, or history rewrite.

## Authorized decision envelope

After approval, implementation may choose disposable directories, evidence formatting, and ordering of independent checks. It may not choose a different evaluator, accept an expanded upgrade plan, hand-edit partial managed state, alter product/release scope, waive a gate, or exercise accountable/external authority.

## Constraints

- Current governor 0.5.0a1 remains authoritative until a verified candidate is merged.
- The applying runtime must be exact external public 0.5.0 with wheel SHA-256 `974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f`.
- The observed managed plan is limited to `.engineering-harness.toml`, `.github/workflows/engineering-harness.yml`, and `ENGINEERING_HARNESS.md`, plus installer-owned lock reconciliation.
- Any other changed surface stops for an amendment.
- No candidate code or candidate wheel may execute as the released evaluator.

## Expected change surface

- Managed root configuration, Engineering Harness workflow, managed contract, and lock only as produced by the supported upgrade.
- `docs/engineering/REPOSITORY_CONTEXT.md` only if required to align owner-curated evaluator facts.
- `docs/engineering/repository-harness-upgrade/evidence/WO-HUP-001-verification.md`.
- This work order's status/lifecycle narrative during later authorized implementation.

## Required verification

- Exact released-evaluator identity and digest.
- Start and review preflight, doctor, validate, inspect, and dashboard.
- Managed-file and lock integrity, plan/apply equivalence, no-op replay, and changed-surface proof.
- Repository default and Python 3.11 unit suites, workflow parsing, candidate-source and candidate-package acceptance.
- Hosted Engineering Harness and candidate evidence on the exact candidate commit.
- `git diff --check`, secret/path review, and base/candidate product/release hash comparison.

## Evidence to record

Retain `docs/engineering/repository-harness-upgrade/evidence/WO-HUP-001-verification.md` with base/candidate identities, public wheel identity and hash, runtime origins, complete plan and apply outcomes, pre/post managed hashes, lock schema/digests, changed paths, graph planes, test counts, hosted URLs, rollback observation, deviations, residual risks, and every unperformed lifecycle/external action.

## Stop and escalate conditions

Stop on wrong identity, digest or origin; invalid graph; preflight failure; customized/ambiguous managed content; plan expansion; partial transaction; repository-owned overwrite; product/release change; failing required check; unexplained warning; candidate mutation after evidence; or need for commit, transition, push, PR, merge, release, publication, deployment, issue edit, force push, or history rewrite without separate authority.

## Completion report format

Report final work-order state, evaluator identity and origins, exact changed surfaces, managed/lock hashes, plan/apply/no-op results, graph planes, test counts, hosted checks, product/release unchanged proof, evidence path, warnings/deviations/residual risks, candidate-commit recommendation, and every unperformed VREC, PR, merge, release, publication, deployment, and issue action.
