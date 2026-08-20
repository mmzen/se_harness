+++
id = "WO-DST-020"
type = "work_order"
title = "Raise the topology acceptance target to two mebibytes"
status = "implemented"
owners = ["engineering-owner", "quality-owner", "technical-owner", "repository-owner"]
created = "2026-08-20"
updated = "2026-08-20"

[assurance]
commit_bound_verification = "required"
rationale = "The change alters an executable package capacity contract and the acceptance gate used by future governance, candidate, pull-request, and release decisions; those decisions require evidence bound to the exact candidate commit."
decided_by = "repository-owner"

[relations]
implements = ["REQ-DST-062", "REQ-DST-063", "REQ-DST-064"]
specifications = ["SPEC-DST-020"]
architecture = ["ARCH-DST-013"]
verification = ["VER-DST-020"]
+++

# Work Order: Raise the topology acceptance target to two mebibytes

## Lifecycle

On 2026-08-20, after merged HUP verification history caused the pull-request candidate-source check to report 525,689 topology bytes against the 524,288-byte target, the repository owner stated `merged. can you create the appriopriate artifact package to fix the topology limit and raise significantly`. This instruction authorizes drafting `REQ-DST-062` through `REQ-DST-064`, `SPEC-DST-020`, `ARCH-DST-013`, `VER-DST-020`, and this work order for review.

The instruction does not approve the packet, accept the architecture assessment, authorize implementation, create evidence, commit, push, open or modify a pull request, verify, merge, build a release distribution, change RCV or 0.5.1 artifacts, release, tag, publish, deploy, or update the installed governor.

On 2026-08-20, the repository owner explicitly approved `REQ-DST-062` through `REQ-DST-064`, `SPEC-DST-020`, `ARCH-DST-013` including its `no_significant_decision` assessment, `VER-DST-020`, and this work order for implementation, while requiring the RCV and 0.5.1 release artifacts to remain draft. The independently installed public 0.5.0 evaluator then passed start preflight for this approved work order, and the complete returned manifest was read before product implementation began. This records bounded implementation authority only; every excluded action remains excluded.

Bounded implementation and retained local evidence were completed on 2026-08-20. The candidate standard template now uses the exact 2 MiB target, focused and complete tests pass on Python 3.14 and 3.11, deterministic current-repository generation remains well below the target, a disposable nonpromotable candidate wheel installs the target, and public-0.5.0 managed-root integrity remains exact. Evidence is retained at `../evidence/WO-DST-020-verification.md`. This `implemented` transition does not grant commit-bound verification or any excluded candidate, pull-request, release, publication, deployment, issue, RCV, or 0.5.1 authority.

Commit-bound assurance is `required` because future repository and release decisions will rely on the exact executable target and preserved evaluator/product boundary.

## Objective

After separate approval, raise the candidate distribution's current-repository compact-topology acceptance target from 524,288 to exactly 2,097,152 UTF-8 bytes, align the governing definitions and tests, and prove substantial headroom without changing topology content, progressive integrity, other budgets, or the public-0.5.0 managed root.

## In scope

- Amend the candidate canonical standard generator template to use `TOPOLOGY_ACCEPTANCE_BYTES = 2_097_152`.
- Align the numeric target references in `REQ-DST-055`, `SPEC-DST-013`, `VER-DST-013`, `SPEC-DST-017`, and `VER-DST-017` while preserving their approved status, relations, and noncapacity meaning.
- Add or refine focused assertions for the exact target, current repository, deterministic repeat generation, target boundaries, and unchanged limits.
- Prove branch, pull-request merge-ref, merged-history, candidate-source, candidate-package, and external released-evaluator behavior required by `VER-DST-020`.
- Retain keyed evidence and transition only this work order through its authorized implementation lifecycle.

## Out of scope

- Active root `scripts/generate_harness_dashboard.py`, `.engineering-harness.lock`, `.engineering-harness.toml`, `ENGINEERING_HARNESS.md`, or `.github/workflows/engineering-harness.yml` changes.
- Topology sharding, schema revision, data omission, truncation, changed serialization, browser behavior, publisher behavior, new runtime origin, dependency, persistence, or network access.
- Any other shell, summary, source-document, total-content, security, or integrity limit.
- Package version, RCV packet, 0.5.1 release packet, release build, RLS, tag, GitHub Release, PyPI publication, Pages deployment, environment action, or issue edit.
- Candidate commit, VREC, push, pull request, merge, or external action without later explicit authority.

## Authorized decision envelope

After packet approval, implementation may choose focused test names, deterministic bounded fixture construction, evidence-table layout, and concise alignment wording. It may not choose a target other than 2,097,152, change included topology data or schemas, edit the active managed root, relax another limit, or expand release/external scope.

## Constraints

- Run start preflight under the independently installed public 0.5.0 evaluator and read the complete manifest before changing lifecycle state or product files.
- Use candidate source/package only in separately labeled test lanes; never as the released evaluator.
- Preserve `.engineering-harness.lock` integrity and a passing public-0.5.0 doctor result.
- Treat current baseline 525,689 bytes and hosted PR run 32388332548 as retained problem evidence, not as authorization to waive a gate.
- Keep unrelated RCV and 0.5.1 drafts outside the candidate.

## Expected change surface

- `templates/repository/standard/scripts/generate_harness_dashboard.py`.
- Focused dashboard capacity tests.
- The five explicitly named existing capacity-definition surfaces.
- `REQ-DST-062..064`, `SPEC-DST-020`, `ARCH-DST-013`, `VER-DST-020`, `WO-DST-020`, the harness-distribution index, and later keyed evidence.
- No active managed root, package version, release, publisher, or issue surface.

## Required verification

- Every acceptance, invariant, static, security, performance, manual, and retention obligation in `VER-DST-020`.
- Public-0.5.0 start and review preflight, doctor, validate, inspect, and dashboard observations.
- Focused current/boundary/determinism tests and complete supported-runtime suites.
- Candidate-source identity and nonpromotable candidate-package acceptance on the exact candidate commit.
- Hosted push and pull-request Engineering Harness and candidate-evidence checks.
- Managed-root and product/release changed-surface proof, `git diff --check`, and private-path/secret review.

## Evidence to record

Retain baseline/candidate commits, current graph and exact topology bytes, old/new targets, initial and remaining headroom, public evaluator version/origins, preflight manifests, complete changed-file ledger, amended-definition matrix, deterministic hashes, target boundary fixtures, other-budget equality, root doctor/lock proof, local runtime/test counts, candidate-package origins, hosted run URLs, deviations, residual risks, and all unperformed lifecycle, release, publication, deployment, and issue actions at `docs/engineering/harness-distribution/evidence/WO-DST-020-verification.md`.

## Stop and escalate conditions

Stop if the packet is not approved; the no-significant-decision assessment is not accepted; preflight fails; any manifest file is unread; required target differs from 2,097,152; the active root or lock changes; another budget/boundary changes; topology data is removed; deterministic, origin, managed-integrity, security, graph, or full-suite checks fail; unrelated drafts overlap; or commit, VREC, push, PR, merge, release, publication, deployment, or issue authority is required but absent.

## Completion report format

Report final work-order state; exact old/new target; baseline/candidate graph and topology bytes; headroom; public evaluator and candidate origins; changed surfaces; definition alignment; deterministic and boundary results; doctor/lock state; local and hosted tests; retained evidence; warnings/deviations/residual risks; and every unperformed commit, VREC, PR, merge, release, publication, deployment, and issue action.
