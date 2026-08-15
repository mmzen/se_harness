+++
id = "WO-SHB-002"
type = "work_order"
title = "Protect self-hosting upgrades, reconcile governors, and add replayable acceptance"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "technical-owner", "quality-owner", "security-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
implements = ["REQ-SHB-007", "REQ-SHB-008", "REQ-SHB-009"]
specifications = ["SPEC-SHB-002"]
architecture = ["ARCH-SHB-002", "ADR-SHB-002"]
verification = ["VER-SHB-002"]
+++

# Work Order: Protect self-hosting upgrades, reconcile governors, and add replayable acceptance

## Lifecycle

The repository owner requested the Phase 1 governance packet on 2026-08-15 after reviewing the discovered standard-upgrade defect, clarifying the consumer versus self-hosting distinction, affirming the released-governor/candidate-evidence principles, and reviewing the proposed implementation plan. The owner subsequently clarified that intentional reconciliation must safely migrate documented TOML policy and replace role-correct workflow mechanics from an immutable published target rather than merely refreshing lock hashes. On 2026-08-15 the owner approved the packet and explicitly instructed `go for implementation`; the work order therefore transitioned through `approved` to `in_progress` and authorized the bounded implementation below. The implementation, local source and package qualification, Python 3.11 compatibility run, protected-root plan, recovery tests, and retained evidence then completed, so the work order transitioned to `implemented` for the authorized candidate commit.

`implemented` records completed work and retained implementation evidence; it does not assert independent correctness. Exact candidate-commit acceptance, hosted CI, VREC capture or transition, push, pull request, release, publication, deployment, root reconciliation, and governor promotion remain separate decisions.

## Objective

Prevent ordinary repository upgrade from replacing the `se-harness` implementation repository's two valid self-hosting controls, provide a bounded current-governor-driven reconciliation path for published governor, configuration-schema, and role-specific workflow changes, and add replayable verifier-owned functional acceptance that separates candidate evidence from released-governor assessment.

## In scope

- Introduce one shared fail-closed self-hosting policy and exact protected-path definition.
- Correct normal upgrade planning and application for protected controls while preserving consumer behavior.
- Add visible protected dispositions and bounded diagnostics in text and JSON plans.
- Add plan-first `reconcile-governor` with exact work-order and immutable published-target selection, current-governor execution, and target-code non-execution.
- Add a versioned data-only migration contract and structured TOML migration with release-managed, repository-identity, and repository-policy ownership, safe defaults, explicit decision requirements, and compatible bridge-release failure behavior.
- Add release-owned self-hosting workflow material with documented inputs or extension points; replace its mechanics without generic YAML merge and reject consumer-role substitution or unrecognized local deltas.
- Reconcile the governor descriptor, TOML configuration, self-hosting workflow, and matching lock metadata through one bounded recoverable transaction.
- Refactor doctor, preflight, self-hosting validation, installer, and tests to consume the shared policy without circular dependencies.
- Add a released-governor-compatible black-box functional acceptance runner and canonical replay manifest.
- Exercise candidate source and exact installed package in separate environments and retain distinct authority labels.
- Add required functional scenarios, malicious inputs, deterministic replay, fresh Python 3.11 package acceptance, and two-release activation evidence.
- Update current self-hosting operations, repository context, CI workflow, package content, and domain index where required by the approved specification.
- Retain complete work-order-keyed implementation evidence and stop for separate candidate-commit authority.

## Out of scope

- Promoting 0.2.2 or the implementation candidate as governor.
- Actually changing `.self-hosting/governor.toml` or either protected root control to a new published version; this work implements and tests the mechanism but does not execute a governor promotion.
- Version selection, release record preparation, tagging, GitHub Release creation, PyPI publication, deployment, or branch protection.
- Treating candidate source or its tests as independent authority.
- Replacing the three-plane workflow with the consumer workflow or creating a public self-hosting profile.
- Expanding the protected set beyond the exact two controls.
- Generic YAML merging, undocumented preservation of root workflow deltas, or automatic selection of consumer workflow material for repository-specific CI.
- Mutating historical VRECs, release records, evidence, commits, tags, or closed-PR facts.
- Activating the new runner as governor before immutable publication and a separate promotion work order.
- Unrelated Explorer, documentation, legacy-location, or architecture-migration changes.

## Authorized decision envelope

After explicit implementation approval, the agent may choose internal module and enum names, stable diagnostic codes, exact JSON and migration-manifest field names, bounded policy-input syntax, transaction-recovery representation, temporary-directory organization, subprocess adapters, documented workflow extension syntax, and focused fixture structure consistent with `SPEC-SHB-002`. It may choose whether the acceptance runner uses a narrow public subcommand or internal module invoked by CI. It may not weaken fail-closed classification, change the normal-upgrade protected set, broaden reconciliation writes beyond the declared control transaction, infer repository policy, generically merge YAML, execute target code during reconciliation, conceal consumer-template divergence, let candidate code own the sole oracle, or collapse publication and promotion.

## Constraints

- Preserve Python 3.11+ and standard-library runtime behavior.
- Preserve ordinary `init`, `adopt`, `upgrade`, and `doctor` interfaces and outcomes except for the new self-hosting-specific disposition and command.
- Preserve the current root governor descriptor and protected bytes; this implementation work may exercise changes only in disposable fixtures. A later separately approved promotion work order may invoke the published mechanism against the root.
- Plan all writes before apply and remain failure-atomic.
- Keep repository strings, workflow contents, package archives, paths, subprocess output, and environment values untrusted.
- Preserve the one-standard-consumer-installation model and current formal artifact authority.
- Do not use normal upgrade to refresh a protected mismatch.
- Do not use candidate source or an unpublished candidate package to reconcile root governor controls.
- Preserve unrelated user work and stop if the branch or worktree changes unexpectedly.

## Expected change surface

- Shared self-hosting policy and descriptor validation components.
- Installer planning/apply and CLI plan rendering.
- Doctor and preflight integrity inspection.
- Bounded governor-reconciliation command, immutable release resolver, data-only migration protocol, field-ownership registry, policy-input validation, and recoverable control transaction.
- Published self-hosting workflow material, minimal repository wrapper or equivalent delimited generated material, and documented extension inputs.
- Runtime identity and candidate-package acceptance adapters where required.
- Repository-specific and standard consumer GitHub workflow tests. Add candidate self-hosting workflow material where required, but do not activate it in the protected root workflow during this work order.
- Functional acceptance runner, fixtures, canonical manifest serializer, and package-data declarations.
- Focused installer, self-hosting, instruction-architecture, security, CLI, packaging, and regression tests.
- Self-hosting operations guide, repository context, domain index, acceptance feature, and retained `WO-SHB-002` evidence.
- Managed lock entries only through supported candidate-integrity mechanisms.

## Required verification

Execute every case in `VER-SHB-002`, the existing `VER-SHB-001` regressions affected by the change, complete Python tests, formal artifact validation, exact CLI help, doctor, start/review preflight, deterministic Explorer generation, package build and inspection, fresh Python 3.11 source and wheel acceptance, consumer upgrade fixtures, current-root protected plan/apply fixtures, GitHub CI, and `git diff --check`.

## Evidence to record

Retain the pre-fix root upgrade plan, post-fix protected plan, exact protected bytes and lock digests, consumer before/after fixtures, every blocking case, current and target governor identities, immutable target resolution, migration-contract and workflow hashes, field-ownership and decision matrices, reconciliation plans, descriptor/control/lock snapshots, fault-injection recovery results, module dependency checks, source/package identities, wheel and acceptance-contract hashes, canonical replay manifests, commands, test counts, runtimes, CI links, deviations, residual risks, and explicitly unperformed external actions under `docs/engineering/self-hosting-boundary/evidence/WO-SHB-002-verification.md`.

## Stop and escalate conditions

Stop if the implementation cannot distinguish consumer and self-hosting targets without ambiguity; requires a circular installer/self-hosting dependency; changes protected bytes through normal upgrade; blesses mismatched controls; cannot prove immutable target publication; imports or executes target code during reconciliation; cannot express field ownership without policy loss; silently chooses an authority-bearing value; requires generic YAML merge or consumer workflow substitution; writes outside the declared descriptor/control/lock transaction; cannot recover from an interrupted write; changes consumer semantics unexpectedly; lets candidate source supply the sole acceptance oracle; cannot isolate the candidate wheel; produces nondeterministic canonical evidence; requires actual root governor promotion or publication; conflicts with concurrent work; or needs authority outside this draft.

## Completion report format

Report the selected current governor, target-resolution and migration protocol, classification and field-ownership models, protected-path behavior, consumer compatibility, reconciliation interface and exact transaction scope, workflow role and extension boundary, recovery evidence, verifier ownership, source/package identities, replay schema and hashes, required scenario outcomes, tests and CI, changed paths, deviations, residual risks, evidence path, lifecycle status, and explicitly unperformed root reconciliation, commit, release, publication, and promotion actions.
