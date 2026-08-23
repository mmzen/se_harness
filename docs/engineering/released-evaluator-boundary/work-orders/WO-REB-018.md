+++
id = "WO-REB-018"
type = "work_order"
title = "Implement the predecessor-to-successor governance migration rehearsal"
status = "implemented"
owners = ["engineering-owner", "repository-owner", "quality-owner", "security-owner", "release-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[assurance]
commit_bound_verification = "required"
rationale = "Future release, assurance, publication, and root-adoption decisions will rely on the new machine-readable migration contract, dual-runtime runner, authority boundaries, candidate CI gate, and retained cross-version evidence."
decided_by = "engineering-owner"

[relations]
implements = ["REQ-REB-016", "REQ-REB-017"]
specifications = ["SPEC-REB-008"]
architecture = ["ARCH-REB-007", "ADR-REB-007"]
verification = ["VER-REB-007"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T07:56:21Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-23T07:56:22Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-23T09:18:22Z"
decided_by = "engineering-owner"
+++

# Work Order: Implement the predecessor-to-successor governance migration rehearsal

## Lifecycle

The bounded issue #101 implementation is complete with retained local, package, adversarial, and hosted Windows/Linux evidence. Commit-bound verification remains a separate ready-record preparation and assurance-owner decision; implementation does not verify, release, publish, deploy, or adopt an evaluator.

## Objective

Deliver one machine-readable and executable N-1-to-N governance migration rehearsal that proves the full handover before an incompatible successor release, while preserving predecessor authority, candidate non-authority, immutable rejected history, honest complete/compatibility claims, and separately governed post-publication adoption.

## In scope

- Add and package the canonical `se-harness-governance-migration-v1` contract and strict parser/validator.
- Add a read-only `harnessctl rehearse-migration` operation conforming to `SPEC-REB-008`.
- Resolve predecessor and successor runtimes independently outside the operational checkout and enforce their typed roles.
- Implement the closed nine-stage runner, authority oracle, snapshot/effect checks, canonical success/failure result, deterministic replay, bounded subprocesses, and disposable cleanup/rollback.
- Adapt existing predecessor preparation, complete candidate validation, assessment, release/publication planning, rendering, and ordinary upgrade behavior behind test-only or internal typed stage interfaces without changing their production authority.
- Add one immutable 0.5.0-to-0.6.0 incident-regression scenario and one version-neutral synthetic N-1-to-N scenario.
- Cover attributed rejection, corrected same-version succession, exact compatibility-view claims, read-only publication/rendering, and separately simulated adoption.
- Add positive and adversarial Windows/Linux tests, package-data checks, candidate-source/package qualification, and one unprivileged hosted exact-predecessor lane.
- Document the migration contract, operator interpretation, authority boundary, failure handling, and how future scenarios or contract versions are added.
- Retain exact `WO-REB-018` preflight, implementation, local, package, cross-platform, hosted, and non-mutation evidence.

## Out of scope

- Changing the lifecycle state source of truth or rejected-record rules tracked by #103 / RC-060-03.
- Consolidating production compatibility-view implementations tracked by #104 / RC-060-04.
- Replacing production raw validator invocations with role-specific release commands tracked by #109 / RC-060-09.
- Rewriting historical REQ/REL/VREC/RLS records, 0.5.0/0.6.0 candidates, distributions, tags, RCA facts, or rejected history.
- Performing or authorizing a real candidate commit, VREC/RLS transition, release, tag, publication, deployment, maintenance mutation, credential use, external policy change, or operational root-evaluator upgrade.
- Adding a diagnostic allowlist, arbitrary omission input, candidate-as-root path, special self-hosting profile, or emergency bypass.
- Expanding the ordinary upgrade, publication, rendering, or lifecycle semantics beyond the adapters needed to observe them in disposable rehearsal.

## Authorized decision envelope

After approval and explicit start, implementation may choose internal module/class/helper names, diagnostic suffixes, fixture implementation, temporary layout, and process-wrapper decomposition. It may choose whether the hermetic synthetic evaluators are subprocess shims or minimal local packages.

It may not change the stage/role catalog, authority effects, exact identity requirements, complete-versus-compatible claim separation, candidate non-authority, no-credential/no-network runner boundary, separately attributed decisions, final-only adoption, historical immutability, cross-platform requirement, or stop conditions.

## Constraints

- Python 3.11+ standard library only for the product runner unless a separately approved dependency change exists.
- Treat contract/scenario data, formal artifacts, Git state, paths, environments, evaluators, adapters, reports, and fixture decisions as untrusted.
- The operational checkout is read-only; all permitted writes occur under one external disposable output root.
- The core runner receives no credential and opens no network connection. Hosted public-wheel acquisition happens before the runner in an unprivileged digest-verifying step.
- Exact predecessor and successor environments must exclude the checkout, user site, inherited `PYTHONPATH`, and shared imports.
- Managed root copies remain locked to the released evaluator; candidate template changes follow the documented candidate-source boundary and cannot upgrade the root.
- Every failure retains bounded diagnostics, proves non-disposable state unchanged, and prevents later stages.

## Expected change surface

- Candidate package: migration contract JSON, strict loader/validator, rehearsal engine, typed stage boundary, canonical result, and CLI registration/help.
- Package configuration and candidate package-surface tests for the new contract.
- Repository-owned migration scenarios/adapters and operator documentation.
- Focused migration, authority, path/security, deterministic, packaging, and Windows/Linux tests.
- Repository-owned candidate-evidence workflow wiring for the unprivileged historical lane.
- `docs/engineering/released-evaluator-boundary/evidence/WO-REB-018-governance-migration.md`.

No release artifact, lifecycle record, root lock/configuration, released distribution, tag, maintenance ref, or public service is an expected change.

## Required verification

- Execute every method and case in `VER-REB-007`.
- Prove source and wheel contract bytes agree and the public CLI parser accepts only the declared interface.
- Run focused unit/integration tests plus the full supported Python suite.
- Run exact released-evaluator `doctor` and graph validation, candidate complete validation, release-distribution checks, portable-surface checks, CLI help, whitespace/diff checks, and candidate source/package lanes appropriate to the reviewed phase.
- Run hermetic rehearsal twice on Windows and Linux and reconcile normalized semantic results.
- Run one hosted unprivileged exact-predecessor/non-promotable-successor scenario and retain its logs/artifacts even on failure.
- Independently prove the operational source, refs, lifecycle state, root evaluator, credential state, and external services unchanged.
- After a separately authorized candidate commit, capture commit-bound verification in a later governance commit; do not infer assurance or release from passing tests.

## Evidence to record

Record all evidence required by `VER-REB-007`, including exact contract/scenario paths and hashes; evaluator/package/commit/tree identities; isolated origins; per-stage inputs, commands, views, decisions, outputs, mutations, durations, and result hashes; failure matrices; rollback/cleanup; platform identities; full checks; candidate and hosted run identities; changed paths; and explicit actions not performed.

## Stop and escalate conditions

- The exact historical scenario cannot pass without changing lifecycle semantics that belong to #103, centralizing production view behavior that belongs to #104, or replacing production evaluator commands that belongs to #109.
- Any stage needs candidate root authority, an unattributed decision, accepted-error text, caller-supplied omission, shared runtime imports, credentials, network access inside the runner, operational Git/root/lifecycle mutation, or external publication/deployment.
- Exact predecessor/successor identity, source immutability, result determinism, cross-platform agreement, cleanup, rollback, complete validation, or package conformance cannot be proven.
- Implementation would change managed root files, historical governance facts, or current public release identities.

When stopped, retain the failing case and request a bounded scope decision; do not absorb another RCA issue or create a bypass.

## Completion report format

Report the contract/schema and scenario IDs; exact predecessor/successor identities; all stage results and authority effects; rejected/corrected succession behavior; complete/compatible claim separation; source/root/external non-mutation proofs; Windows/Linux/local/hosted checks; changed paths; evidence path; candidate/VREC state; actions not performed; residual risks; and one next accountable decision.
