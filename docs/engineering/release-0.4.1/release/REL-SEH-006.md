+++
id = "REL-SEH-006"
type = "release_contract"
title = "Qualify and release se-harness 0.4.1"
status = "approved"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-08-17"
updated = "2026-08-17"

[relations]
gates = ["WO-DPG-001", "WO-DST-011", "WO-DST-012", "WO-DST-013", "WO-DST-014", "WO-DST-015", "WO-DST-016", "WO-RLS-007"]
+++

# Release Contract: Qualify and release se-harness 0.4.1

## Lifecycle and authority

On 2026-08-17, after reviewing the post-0.4.0 work-order ledger and proposed release sequence, the repository owner instructed `go`, authorizing creation of the draft packet on `work/WO-RLS-007`. After reviewing the resulting exact allow-list, aggregate-verification boundary, compatibility policy, and release procedure, the owner explicitly stated `i validate`. That decision approves this contract and `WO-RLS-007` and authorizes their bounded 0.4.1 candidate implementation, qualification evidence, candidate commit, and later preparation of `VREC-SEH-007` as `ready`.

The approval does not authorize push, pull-request creation or merge, the VREC's verification transition, release-record preparation or transition, tag creation, GitHub or PyPI publication, Pages deployment, governor reconciliation, force push, or history rewriting.

## Release unit

One incremental `se-harness` 0.4.1 release derived from one clean candidate commit: reproducible wheel, normalized source distribution, checksum manifest, immutable `v0.4.1` tag, GitHub Release assets, and publication of the same qualified files to PyPI.

The historical release-bearing work added after the 0.4.0 candidate is exactly:

- `WO-DPG-001`: publish the repository-specific Explorer demonstration through GitHub Pages;
- `WO-DST-011`: refine Explorer Overview filtering, neighborhood context, labels, and status presentation;
- `WO-DST-012`: restructure Lineage as a navigable artifact-lane board;
- `WO-DST-013`: enrich selected-artifact details, relations, evidence, Markdown, and EARS presentation;
- `WO-DST-014`: emit a deterministic integrity-addressed progressive Explorer bundle;
- `WO-DST-015`: load and verify Explorer resources progressively and safely; and
- `WO-DST-016`: simplify consumer GitHub CI installation and upgrade around one exact package evaluator.

`WO-RLS-007` adds the 0.4.1 versioning, integrated qualification, reproducible-build, exact-candidate, and release evidence needed to form the final eight-work-order release unit. This contract is an explicit allow-list, not an inference from dates, statuses, branches, or every commit after `v0.4.0`.

## Baseline and exclusions

The previous release is `RLS-SEH-006`, version 0.4.0, candidate and tag target `2acc63af8933ee1dfa5ef78b67e2dbe6fb9a4e61`. The initial 0.4.1 packet starts from merged `main` commit `9f69e92a7de0befcea6d1f37b38402aa4183ad8f`.

`WO-RLS-006`, `VREC-SEH-006`, and `RLS-SEH-006` appear after the 0.4.0 tag target in repository history but belong to the already released 0.4.0 governance transaction and are excluded. Historical ready/verified-record maintenance, merge commits, and derived Pages publication runs are not independently added as release work. No other implemented work order is admitted without an accountable contract amendment.

## Entry criteria

- The seven historical work orders are implemented, active, have retained keyed evidence, and are covered by `VREC-DPG-001` or `VREC-DST-010..013` in `verified` state.
- No selected historical work order is named by an existing released RLS.
- `WO-RLS-007` is explicitly approved and its start preflight passes before versioning or build work.
- Repository, package, CLI, public guidance, candidate configuration, and self-hosting candidate declaration consistently identify 0.4.1 before the clean candidate commit.
- `.self-hosting/governor.toml` continues to select the independently released governor chosen before this transaction. Releasing 0.4.1 does not promote it to govern its own development.
- Formal validation, doctor, managed parity, self-hosting planes, supported-runtime tests, inspection, Explorer, archive safety, reproducibility, and fresh package acceptance pass for the final candidate.

## Required aggregate verification

`VREC-SEH-007` must bind one clean 0.4.1 candidate commit to exactly `WO-DPG-001`, `WO-DST-011..016`, and `WO-RLS-007`. Its verification-contract union must be exactly `VER-DPG-001`, `VER-DST-001`, and `VER-DST-010..015`. It must retain one repository-contained evidence path keyed to every selected work order.

The existing verified records demonstrate their historical candidates but cannot form the release manifest because their commit identities differ. The aggregate record reassesses the complete integrated payload at one commit without rewriting or extending those records.

Only after an accountable owner transitions `VREC-SEH-007` to `verified` may `RLS-SEH-007` be prepared as `ready`. The release record must name version 0.4.1, tag `v0.4.1`, the same candidate commit/object format, exactly the eight work orders, this contract, and only commit-compatible verification records.

## Compatibility and trust boundary

- Retain Python 3.11+ and the single standard consumer installation.
- The standard consumer workflow uses one exact released package evaluator, is additive beside repository-owned workflows, and upgrades only through the managed init/adopt/upgrade transaction.
- The SE Harness implementation repository retains its separate released-governor, candidate-source, and candidate-package planes. The consumer workflow must not replace that self-hosting boundary.
- Explorer progressive resources remain integrity-addressed, same-origin, deterministic, bounded, static-host compatible, and unavailable rather than implicitly trusted when verification fails.
- The repository-specific public demonstrator remains demonstration material, not package assurance or release authority.

## Reproducibility and promotion gates

- Build twice from exported candidate source at one explicit candidate epoch.
- Require byte-identical wheels and normalized sdists, safe and equivalent archive payloads, valid wheel RECORD metadata, and an offline wheel reconstruction matching the direct wheels.
- Install the reconstructed wheel in a fresh external Python 3.11 environment and run identity, init/adopt, doctor, validate, inspect, dashboard, safe upgrade, conflict refusal, and package-owned consumer-CI acceptance.
- Acquire the selected released governor only through its recorded immutable identity and digest; preserve runtime/source/package role evidence.
- Treat checkout, workflows, events, paths, archives, Markdown, TOML, evidence, and generated resources as untrusted.
- A candidate change after aggregate capture invalidates the proposal and requires a new candidate/VREC/RLS sequence.

## Authority and rollback

Approval of this contract and `WO-RLS-007` may authorize only bounded versioning, qualification, evidence, candidate commit, and later preparation of `VREC-SEH-007` as `ready`. Verification transition, release-record preparation/transition, merge, tag, GitHub Release, PyPI publication, Pages deployment, and governor reconciliation remain separate decisions.

Stop on scope drift, missing keyed evidence, incomplete contract union, historical-record mutation, version disagreement, protected-control ambiguity, governor drift, cross-role import, failed gate, unclassified warning, unsafe archive, nondeterministic artifact, or need for authority beyond the approved phase. Before publication, correct failure through a new candidate sequence; after publication, never move the tag or replace published files.

## Post-release observation

After separately authorized publication, confirm immutable tag/assets, PyPI metadata and hashes, fresh public Python 3.11 installation, `harnessctl --version`, clean-repository initialization, doctor, validate, inspect, dashboard, and consumer workflow rendering. Record failures without replacing published artifacts or treating publication automation as release authority.
