+++
id = "WO-RLS-007"
type = "work_order"
title = "Qualify the integrated se-harness 0.4.1 candidate"
status = "implemented"
owners = ["repository-owner", "release-owner", "quality-owner", "engineering-owner", "security-owner"]
created = "2026-08-17"
updated = "2026-08-17"

[assurance]
commit_bound_verification = "required"
rationale = "Release, package, installation, public demonstrator, consumer CI, and future governor decisions will rely on the exact integrated candidate, protected controls, retained evidence, and reproducible distributions."
decided_by = "repository-owner"

[relations]
implements = ["REQ-DST-006"]
specifications = ["SPEC-DST-001"]
architecture = ["ARCH-DST-001", "ADR-DST-001"]
verification = ["VER-DST-001"]
+++

# Work Order: Qualify the integrated se-harness 0.4.1 candidate

## Lifecycle and authorization

On 2026-08-17 the repository owner requested release 0.4.1, reviewed how release-bearing work is selected, and instructed `go`, authorizing creation of the draft packet. After reviewing `REL-SEH-006` and this exact work order, the owner explicitly stated `i validate`. That decision approves both artifacts and authorizes bounded 0.4.1 versioning, integrated qualification, retained evidence, one clean candidate commit, and later preparation of `VREC-SEH-007` as a `ready` proposal after exact-commit replay.

The approval does not authorize push, pull-request creation or merge, the VREC's verification transition, release-record preparation or transition, tag creation, GitHub Release, PyPI publication, Pages deployment, governor reconciliation, force push, or history rewriting.

Start preflight passed with this work order in `approved`, so the bounded 0.4.1 candidate implementation is now `in_progress`.

The bounded implementation and preliminary qualification completed on 2026-08-17. Candidate identity is consistently 0.4.1, protected candidate controls and their lock agree, the selected released governor remains exactly 0.3.0, both supported-runtime suites pass, deterministic graph and Explorer payload checks pass, reproducible distributions agree, and a fresh external Python 3.11 installation passes the consumer workflow. Evidence is retained at `docs/engineering/release-0.4.1/evidence/WO-RLS-007-verification.md`. This transition to `implemented` records completed work and retained evidence only; exact-commit replay and the later `VREC-SEH-007` proposal remain after the clean candidate commit and do not assert verification or release.

## Objective

Produce one clean and fully qualified 0.4.1 candidate containing the seven selected historical work orders plus this release-integration work order, with consistent identity, reproducible artifacts, protected self-hosting separation, and exact aggregate evidence. After the separately authorized candidate commit, prepare `VREC-SEH-007` as a ready proposal for the eight-work-order set.

## Exact aggregate scope

- Work orders: `WO-DPG-001`, `WO-DST-011`, `WO-DST-012`, `WO-DST-013`, `WO-DST-014`, `WO-DST-015`, `WO-DST-016`, and `WO-RLS-007`.
- Verification contracts: `VER-DPG-001`, `VER-DST-001`, `VER-DST-010`, `VER-DST-011`, `VER-DST-012`, `VER-DST-013`, `VER-DST-014`, and `VER-DST-015`.
- Evidence: the seven existing work-order-keyed evidence files plus `docs/engineering/release-0.4.1/evidence/WO-RLS-007-verification.md`.
- Planned aggregate VREC: `docs/engineering/release-0.4.1/verification-records/VREC-SEH-007.md`.
- Planned release record after verified assurance: `docs/engineering/release-0.4.1/releases/RLS-SEH-007.md`.
- Proposed public version and immutable tag: `0.4.1` and `v0.4.1`.

The work-order set is fixed by `REL-SEH-006`. `WO-RLS-006` and its 0.4.0 governance records are explicitly excluded as already released. Existing historical VRECs support scope discovery and evidence lineage but do not replace the new candidate-bound aggregate VREC.

## In scope after explicit approval

- Reconfirm the `v0.4.0`-to-main ledger and retain the exact inclusion/exclusion rationale.
- Set authoritative package, CLI, repository candidate, workflow candidate, template, test, and public-documentation identity to 0.4.1.
- Preserve `.self-hosting/governor.toml` and every immutable selected-governor identity/digest field.
- Update protected candidate controls only through the supported self-hosting boundary; retain repository policy, three-plane CI roles, and lock integrity.
- Prove the simplified standard consumer workflow renders one isolated exact 0.4.1 evaluator without executing checkout copies as assessment authority.
- Preserve the accepted Explorer Overview, Lineage, detail, progressive-bundle, integrity, caching, static-hosting, and demonstration behavior.
- Run the complete `REL-SEH-006` qualification matrix on local Python and Python 3.11, released governor, candidate source, and fresh candidate package.
- Build and compare two wheels, two normalized sdists, one reconstructed wheel, safe payload manifests, and fresh external installation.
- Retain version inventory, exact commands/results, candidate/source/package/governor origins, hashes, manifests, protected-control diffs, graph-plane counts, warnings, deviations, residual risks, and unperformed external actions.
- Transition this work order to `implemented`, create one clean candidate commit, replay exact-commit qualification, and only then prepare `VREC-SEH-007` as `ready`.

## Out of scope

Adding product behavior; changing the selected governor; using candidate behavior as independent governance; changing the allow-list without approval; mutating historical VRECs/RLS records; preparing or transitioning a release record before verified aggregate assurance; transitioning `VREC-SEH-007`; merging; tagging; publishing; deploying; configuring external GitHub policy; promoting a governor; force pushing; or rewriting history.

## Authorized decision envelope

After explicit approval, implementation may choose deterministic temporary directories, the candidate epoch, evidence layout, safe mechanical version updates, and test helpers required by existing contracts. It may not reinterpret scope, change accepted behavior, weaken gates, add dependencies or profiles, alter the governor identity, make accountable transitions, or perform external release actions.

## Required verification

- Start/review preflight and formal graph validation pass with no structure, governance, or policy errors or warnings.
- Complete local and Python 3.11 suites pass with only documented conditional skips.
- Released-governor, candidate-source, and candidate-package lanes prove exact origin and role separation.
- All authoritative version-bearing sources and package metadata equal 0.4.1; selected governor fields remain unchanged.
- Doctor, managed parity, lock integrity, workflow parsing, validation, inspection, Explorer generation, Pages exact-set validation, and consumer install/adopt/upgrade/conflict fixtures pass.
- Event selection and package-owned evaluator commands remain bounded, isolated, and fail closed under checkout and environment manipulation.
- Explorer bundle generation and browser acquisition remain deterministic, integrity-addressed, bounded, progressively loaded, same-origin, and safe under failure/race cases.
- Two direct wheels and normalized sdists are reproducible at one epoch; archives are safe; reconstructed wheel equals direct wheels and passes fresh Python 3.11 operation outside the checkout.
- Aggregate VREC inputs contain exactly eight work orders, eight verification contracts, eight keyed evidence paths, one clean candidate commit, and one artifact snapshot.
- Candidate ancestry, changed-path ledger, protected-control diff, and `git diff --check` pass.

## Evidence and completion

Retain implementation and exact-candidate evidence at `docs/engineering/release-0.4.1/evidence/WO-RLS-007-verification.md`. The evidence must clearly distinguish preliminary working-tree checks, the later candidate commit, independent released-governor results, candidate-owned evidence, hosted CI, and actions not performed.

`implemented` records completion and evidence, not correctness or release authority. The candidate cannot contain a truthful VREC naming its own not-yet-created commit, so aggregate capture must occur in a later governance commit.

## Stop conditions

Stop on scope change, missing evidence, contract mismatch, version drift, protected-policy loss, governor-field change, self-governance ambiguity, cross-role import, failed required check, unexplained warning, package/repository divergence, unsafe archive, nondeterminism, candidate mutation after exact evidence, or need for unapproved authority.

## Completion report format

Report the eight-work-order scope and exclusions, version inventory, exact candidate commit/tree/epoch, governor identity, protected-control changes and hashes, source/package/evaluator origins, test counts, graph planes, inspection/Explorer manifests, package hashes, reproducibility and fresh-install results, warnings/deviations/residual risks, evidence path, planned aggregate VREC inputs, and every unperformed verification transition, release record, merge, tag, publication, deployment, and governor promotion.
