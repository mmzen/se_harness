+++
id = "REL-SEH-007"
type = "release_contract"
title = "Qualify and release se-harness 0.6.0"
status = "approved"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[relations]
gates = ["WO-DST-019", "WO-DST-020", "WO-WEX-001", "WO-WEX-002", "WO-REB-001", "WO-REB-002", "WO-REB-003", "WO-RLS-008"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-21T13:48:00Z"
decided_by = "release-owner"
+++

# Release Contract: Qualify and release se-harness 0.6.0

## Lifecycle and authority

On 2026-08-21, after reviewing the `v0.5.0`-to-`main` ledger, proposed release notes, exact release-bearing allow-list, exclusions, and readiness gaps, the repository owner instructed `ok, launch the release process`. That instruction authorizes creation and completion of this draft contract and `WO-RLS-008` for accountable review.

After reviewing the completed packet, the accountable owner stated `I approve REL-SEH-007 and WO-RLS-008 for bounded 0.6.0 versioning, integration, qualification, reproducible distribution builds, and retained evidence under their exact eight-work-order scope.` That decision transitions this contract to `approved` and authorizes only the bounded implementation and build work defined here and in `WO-RLS-008`.

The approval explicitly does not authorize the candidate commit, VREC or RLS preparation or transitions, tag creation or movement, GitHub or PyPI publication, Pages deployment, maintenance-line mutation, credential use, external policy change, or root-evaluator upgrade.

## Release unit

One incremental `se-harness` 0.6.0 release derived from one clean candidate commit: a reproducible wheel, normalized source distribution, checksum manifest, immutable `v0.6.0` tag, GitHub Release assets, publication of the same qualified files to PyPI, and a release-bound static Explorer demonstration.

The historical release-bearing work added after the immutable `v0.5.0` baseline is exactly:

- `WO-DST-019`: safe explicit pre-assurance artifact renumbering;
- `WO-DST-020`: raise the compact-topology acceptance ceiling from 512 KiB to 2 MiB;
- `WO-WEX-001`: deterministic selected-scope focus, atomic lifecycle transitions, and canonical workflow results;
- `WO-WEX-002`: executable workflow/gate contracts, scoped compliance checks, typed procedures, and schema-2 restitution;
- `WO-REB-001`: align publication with the standard released-evaluator identity;
- `WO-REB-002`: reject unauthorized runtimes before installed-root mutation and bind evaluator identity into readiness evidence; and
- `WO-REB-003`: separately authorize evaluator upgrades and provide bounded recovery inspection, runbook, and rehearsal.

`WO-RLS-008` adds the 0.6.0 versioning, integrated qualification, reproducibility, exact-candidate evidence, and aggregate-VREC preparation needed to form the final eight-work-order release unit. This contract is an explicit allow-list, not an inference from dates, branches, merge order, lifecycle status, or every commit after the baseline.

## Baseline and exclusions

The previous public release baseline is immutable annotated tag `v0.5.0`, whose tag object is `b4a1b7956c6d78ea808997eed027800a8b973f4a` and whose released candidate commit is `c42bbac20f14268ef162c9628dd1d2b45ea843af`. The initial 0.6.0 packet was drafted from clean `main` commit `cd80f0bde9f24a069d15ba461d1257261d744e9c`.

The 0.5.0 publication used an exceptional recovery sequence and has no ordinary `RLS-SEH-*` record. This contract preserves that fact and relies on the factual 0.5.0 incident RCA as learning, not as reusable release authority.

The following are explicitly excluded from `releases_work`:

- `WO-HUP-001`, which upgraded this repository's root evaluator from released 0.5.0a1 to released 0.5.0;
- `WO-RCA-001`, which produced the factual 0.5.0 release-governance RCA;
- the emergency 0.5.0 publication and revert commits;
- merge-only commits, VREC preparation and transition commits, supersession bookkeeping, and derived publication observations; and
- every other implemented work order not named in this contract.

Repository-governance and RCA documents may remain in the source tree and source distribution without converting their work orders into release-bearing payload.

## Required evidence

### Entry criteria

- The seven selected historical work orders are active, `implemented`, retain work-order-keyed evidence, and have existing verified assurance coverage.
- No selected historical work order is named by an existing released RLS.
- `VREC-WEX-001`, `VREC-WEX-002`, and `VREC-WEX-003` receive explicit accountable supersession or other disposition before the final candidate; automation must not infer it.
- This contract and `WO-RLS-008` are separately reviewed and approved before start preflight, versioning, code or documentation edits, or a promotable build.
- Formal validation, released-evaluator doctor, managed-root integrity, and start preflight pass without structure, governance, or policy errors.
- The two observed Windows direct-checkout regression failures are corrected or explicitly reproduced and dispositioned through the approved work before candidate qualification.

### Exact aggregate verification

`VREC-SEH-008` must bind one clean 0.6.0 candidate commit to exactly `WO-DST-019`, `WO-DST-020`, `WO-WEX-001`, `WO-WEX-002`, `WO-REB-001`, `WO-REB-002`, `WO-REB-003`, and `WO-RLS-008`.

Its verification-contract union must be exactly `VER-DST-001`, `VER-DST-019`, `VER-DST-020`, `VER-WEX-001`, `VER-WEX-002`, and `VER-REB-001`. It must retain one repository-contained evidence path keyed to every selected work order.

The existing verified records demonstrate historical candidates whose commit identities differ. They support lineage and scope discovery but cannot form the 0.6.0 release manifest. The aggregate record must reassess the complete integrated payload at one exact candidate commit without rewriting or extending historical records.

Only after an accountable assurance owner transitions `VREC-SEH-008` to `verified` may `RLS-SEH-008` be prepared as `ready`. The release record must name version `0.6.0`, tag `v0.6.0`, this contract, the same candidate commit, exactly the eight selected work orders, and only commit-compatible verified records.

## Compatibility and migration

- Retain Python 3.11 or later and standard-library-only runtime behavior.
- Retain exactly one standard consumer installation and no installation profiles.
- Preserve existing owner content outside managed markers and refuse customized or ambiguous upgrades without partial writes.
- Installing the 0.6.0 package does not update managed content already installed in a repository.
- Upgrading an installed repository from 0.5.0 to 0.6.0 requires the exact independently published 0.6.0 wheel outside the checkout, a separate approved evaluator-upgrade work order, a reviewed read-only plan, and explicitly authorized transactional apply.
- Candidate source, editable installs, contaminated environments, mismatched entry points, and ambiguous evaluator identities cannot mutate an installed root.
- Standard installations add machine-readable `WORKFLOW.json` and `QUALITY_GATES.json` contracts plus managed Git attributes for canonical evidence bytes.
- Active `governor` runtime roles and `.self-hosting/governor.toml` publication dependencies are retired. Historical records retain their original terminology and bytes.
- Existing workflow result consumers retain the documented schema-1 compatibility window; `harnessctl check` emits canonical schema 2.

## Security and provenance

- Treat repository content, paths, Git state, events, archives, Markdown, TOML, JSON, evidence, workflow inputs, and pull-request text as untrusted.
- Run root doctor, preflight, lifecycle mutation, capture, and release preparation only with the exact external released evaluator selected by the repository lock.
- Prove candidate-source, candidate-package, and released-evaluator origins independently and reject checkout import fallback.
- Bind evaluator payload and archive identity into verification and release-readiness evidence as required by the candidate contract.
- Require a clean candidate worktree and exact full Git object identity for aggregate capture and release preparation.
- Preserve historical VREC, RLS, evidence, tag, and published-file facts byte-for-byte.
- A candidate change after aggregate capture invalidates the proposal and requires a new candidate, evidence, VREC, and RLS sequence.

## Promotion policy

- Run the complete source regression, formal graph, release-distribution, CLI, doctor, inspection, Explorer, managed-parity, lock, mutation-guard, archive-safety, recovery, and package-surface checks.
- Run the supported Python matrix including Python 3.11 and retain exact versions, counts, skips, failures, and deviations.
- Build twice from exported candidate source at one explicit candidate epoch.
- Require byte-identical wheels and normalized sdists, safe and equivalent archive payloads, valid wheel RECORD metadata, and an offline wheel reconstruction matching the direct wheels.
- Install the reconstructed wheel in a fresh external Python 3.11 environment and run identity, init, adopt, doctor, validate, inspect, dashboard, safe upgrade, conflict refusal, mutation-authority refusal, workflow execution, renumber planning, and verifier-owned candidate acceptance.
- Require hosted released-evaluator, candidate-source, and candidate-package lanes to pass without mutating the checkout.
- Require `VREC-SEH-008` to be verified before release preparation and `RLS-SEH-008` to be released before any external promotion.
- Require the release record, aggregate VREC, tag, candidate commit, version, distribution manifest, wheel, sdist, checksums, GitHub assets, PyPI files, and Pages provenance to agree exactly.

## Human approval triggers

- Release, quality, security, and engineering owners approve this contract and `WO-RLS-008` before implementation.
- A repository owner separately authorizes the clean candidate commit after review evidence is complete.
- An assurance owner alone verifies or rejects `VREC-SEH-008`.
- A release owner separately authorizes preparation of `RLS-SEH-008` and later alone releases or rejects it.
- Tag creation, GitHub Release publication, PyPI publication, Pages deployment, maintenance-branch reconciliation, and post-publication root upgrade each require the separately governed authority applicable at action time.
- Automation can prepare observations and `ready` proposals but cannot supply any accountable decision.

## Rollback criteria and procedure

Before publication, stop on scope drift, missing keyed evidence, unresolved historical ready records, version disagreement, evaluator or lock drift, candidate contamination, failed required check, unexplained warning, unsafe archive, nondeterminism, package/template divergence, provenance mismatch, or need for authority beyond the approved phase. Correct the issue through a new reviewed candidate sequence; do not waive or conceal the failed criterion.

After publication, never move `v0.6.0`, replace immutable GitHub or PyPI files, rewrite evidence, or reinterpret `RLS-SEH-008`. Record the defect, preserve the affected release, block unsafe promotion or upgrade as needed, and prepare a separately governed corrective release.

## Post-release observation window

After separately authorized publication, confirm the immutable tag and GitHub assets, PyPI metadata and hashes, a fresh public Python 3.11 installation, `harnessctl --version`, clean init and adopt, doctor, validate, focus, check, inspect, dashboard, renumber plan, mutation-authority refusal, consumer workflow rendering, Pages manifest/provenance, and maintenance-line state. Record failures without replacing published artifacts or treating observation automation as release authority.
