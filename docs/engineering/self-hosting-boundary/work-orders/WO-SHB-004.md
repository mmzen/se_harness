+++
id = "WO-SHB-004"
type = "work_order"
title = "Promote published governor 0.3.0 through bootstrap reconciliation"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "technical-owner", "quality-owner", "security-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
implements = ["REQ-SHB-005", "REQ-SHB-007", "REQ-SHB-008", "REQ-SHB-009"]
specifications = ["SPEC-SHB-001", "SPEC-SHB-002"]
architecture = ["ARCH-SHB-001", "ADR-SHB-001", "ARCH-SHB-002", "ADR-SHB-002"]
verification = ["VER-SHB-001", "VER-SHB-002"]
+++

# Work Order: Promote published governor 0.3.0 through bootstrap reconciliation

## Lifecycle and decision boundary

The repository owner requested the start of the operational governor transition from released version 0.2.1 to released version 0.3.0 after 0.3.0 had been separately verified, released, published on GitHub and PyPI, and installed for consumer use. On 2026-08-15, after reviewing the exact identities, bootstrap authority model, transaction boundary, verification, and rollback conditions in this packet, the owner explicitly stated `i approve`. The work order therefore transitioned through `approved` to `in_progress` and authorizes the bounded execution below.

This approval authorizes only the bounded bootstrap reconciliation, verification, candidate commit, and later review workflow described below. It does not itself assert that the target is accepted as governor. The current 0.2.1 governor remains authoritative until the reconciled candidate passes the required evidence and accountable review and the resulting change is merged.

## Objective

Promote the exact published 0.3.0 release as the repository's operational governor while preserving the separation between released-governor authority and candidate evidence. Reconcile the descriptor, repository configuration, self-hosting workflow, and integrity lock as one reviewable control transaction, without executing 0.3.0 as authority for its own promotion.

## Selected immutable identities

| Role | Version | Release record | Candidate commit | Wheel | SHA-256 |
| --- | --- | --- | --- | --- | --- |
| Current governor and rollback provenance | 0.2.1 | `RLS-SEH-002` | `94e13e31b81333e1f80f5a7dfd86ed5dbfc1e3e5` | `se_harness-0.2.1-py3-none-any.whl` | `533f6f87f5a1060d5d0070702969f643525ca3b91e2ecdbbd029f1530d093454` |
| Target published governor | 0.3.0 | `RLS-SEH-005` | `dd06660a94f06d934adb1df0352b81e709f2ffd3` | `se_harness-0.3.0-py3-none-any.whl` | `260e22371b05e5bb6c59143a1f0229855305a6bf7994984be50aa147a02ea516` |

The current wheel is retained at `https://github.com/mmzen/se_harness/releases/download/v0.2.1/se_harness-0.2.1-py3-none-any.whl`. The target wheel is selected at `https://github.com/mmzen/se_harness/releases/download/v0.3.0/se_harness-0.3.0-py3-none-any.whl`; tag `v0.3.0` must resolve to the target candidate commit, and the GitHub release must remain immutable, non-draft, and non-prerelease.

## Bootstrap authority model

This is the first adoption of the released reconciler introduced by 0.3.0. Version 0.2.1 cannot execute `reconcile-governor`, while running the 0.3.0 command against this repository would let the target authorize its own activation. The transition therefore uses the one-time previously trusted bootstrap process permitted by the compatibility section of `SPEC-SHB-002`:

1. Treat 0.2.1 as the pre-change authoritative governor and retain its exact descriptor and protected-control state as rollback provenance.
2. Verify the 0.3.0 release identity and wheel digest independently, then inspect its data-only migration manifest and role-specific workflow material without importing or executing target code as migration authority.
3. Construct the same bounded target state deterministically and review the complete plan before any write.
4. Apply the four-file control set transactionally and prove that no unrelated path changed.
5. Use the published 0.3.0 package only for post-change candidate acceptance and future-governor qualification. Its success is evidence for accountable review, not retroactive authority.

After this promotion is accepted, the selected 0.3.0 governor may execute `reconcile-governor` for compatible later releases. This work order establishes no recurring manual exception.

## In scope

- Verify the current 0.2.1 descriptor, exact released wheel, digest, control bytes, root integrity entries, and clean semantic baseline.
- Verify the target 0.3.0 tag, release record, candidate commit, GitHub release asset, wheel digest, packaged migration protocol, configuration schema, workflow template, and reusable workflow identity.
- Produce and retain a deterministic read-only bootstrap plan before modification.
- Reconcile exactly `.self-hosting/governor.toml`, `.engineering-harness.toml`, `.github/workflows/engineering-harness.yml`, and `.engineering-harness.lock` as one bounded transaction.
- Preserve repository identity and policy values in `.engineering-harness.toml`; its current schema-2 and 0.3.0 values may remain byte-identical when already conforming.
- Replace the root workflow with the published 0.3.0 implementation-repository wrapper, pinned to reusable workflow commit `dd06660a94f06d934adb1df0352b81e709f2ffd3`, and supply the exact selected governor and candidate inputs.
- Update only lock entries whose accepted target bytes change, using schema-2 `utf8-text-lf-v1` hashing.
- Update repository-specific self-hosting tests that intentionally bind the selected governor identity or root workflow topology so they validate the 0.3.0 descriptor, the pinned wrapper, and the released reusable three-plane workflow without weakening the underlying invariants.
- Retain before/after bytes, hashes, plan, commands, runtime origins, acceptance results, and rollback evidence under `docs/engineering/self-hosting-boundary/evidence/WO-SHB-004-verification.md`.
- Complete a candidate commit, commit-bound verification record, accountable verification decision, push, and pull request only through separately requested workflow steps.

## Explicit policy decisions

- Repository policy in `.engineering-harness.toml` remains unchanged: full clean commit provenance is required for verified work and release, and prepared VREC/RLS status remains `ready`.
- Workflow permissions remain `contents: read`; no secret, environment, deployment, or write permission is introduced.
- `main` remains the repository integration source. This promotion changes governor identity and workflow mechanics only; it changes no branch, release, or publication policy.
- The target reusable workflow is pinned to the full released candidate commit, never to a mutable branch or tag.
- The prior 0.2.1 identity remains recoverable from Git history and retained evidence.

## Out of scope

Changing harness runtime implementation source, consumer templates, formal requirements, specifications, architecture, ADRs, or verification contracts; changing repository tests beyond the exact selected-governor and root-workflow assertions; modifying a fifth control path; executing the 0.3.0 reconciler as its own authority; weakening current repository policy; accepting unrecognized local workflow customization; creating a compatibility bridge; changing version 0.3.0 artifacts; preparing another product release; tagging; GitHub Release or PyPI publication; deployment; merging; force pushing; or rewriting history.

## Required verification

- Prove the current and target release identities, full candidate commits, asset names, download URLs, wheel SHA-256 values, and target tag resolution.
- Confirm the current descriptor agrees with the inline root workflow and the protected workflow/configuration bytes agree with the existing lock under canonical text hashing.
- Confirm the target wheel contains the expected protocol-1 migration manifest, schema-2 field ownership declarations, implementation-repository workflow template, and reusable workflow; inspect these entries as data without importing target modules.
- Review a deterministic plan showing dispositions for all four bounded paths and no others. Stop on a decision-required field, unsupported migration, mutable or mismatched identity, unrecognized workflow delta, lock mismatch, or policy change.
- Fault-test or otherwise prove all-or-nothing restoration of descriptor, configuration, workflow, and lock before applying the real transaction.
- After the candidate change, run formal artifact validation, managed-integrity doctor, start and review preflight, focused self-hosting/reconciliation/acceptance tests, the complete unit suite, deterministic Harness Explorer generation, `git diff --check`, and exact diff-scope review.
- Install the exact 0.3.0 wheel in a fresh external Python 3.11 environment; attest version, distribution, template, and executable origins outside the checkout; then run its replayable acceptance contract against the reconciled candidate without treating that execution as the authority that approved the change.
- Require hosted CI to prove all three planes with 0.3.0 as the downloaded checksum-verified released governor before accountable verification or merge.

## Rollback and failure behavior

Before commit, any failed identity, migration, integrity, test, or scope check restores the exact prior four-file state and leaves 0.2.1 selected. No partial control set may remain. After a candidate commit or merge, recovery uses a normal revert or a new governed work order and commit; history is never rewritten. A failed 0.3.0 post-change assessment blocks verification and merge and does not imply that 0.3.0 became authoritative.

## Evidence and completion

The evidence record must distinguish current-governor observations, data-only target inspection, candidate-source evidence, exact target-package evidence, hosted CI, and accountable decisions. It must record all deviations and residual risks. When the authorized control transaction and local verification pass, mark this work order `implemented` and commit the candidate plus evidence. `implemented` records completed work only; it does not assert independent correctness or governor acceptance.

## Stop and escalate conditions

Stop if 0.2.1 is not the exact current governor, the target release or digest differs, the target commit is not the released tag object, target code would need to execute as migration authority, the migration contract is incompatible with the documented bootstrap path, repository policy would change, the workflow is not the implementation-repository variant, any unrecognized local delta exists, the four-file transaction cannot be made failure-atomic, a check fails, the worktree changes unexpectedly, or an action exceeds the approved lifecycle step.

## Implementation result

The bounded bootstrap transaction now selects exact published governor 0.3.0 in the working-tree candidate. The descriptor records `RLS-SEH-005`, candidate `dd06660a94f06d934adb1df0352b81e709f2ffd3`, and wheel SHA-256 `260e22371b05e5bb6c59143a1f0229855305a6bf7994984be50aa147a02ea516`. Repository policy remains byte-identical. The root workflow is the published 0.3.0 implementation-repository wrapper pinned to the reusable three-plane workflow at that full commit, and the schema-2 lock records its exact canonical digest.

Repository-specific tests now follow the selected descriptor and validate the wrapper plus released reusable workflow without weakening plane separation. Formal validation, candidate and exact-package doctor and preflight, isolated Python 3.11 identity, 24 focused tests, 160 complete tests, 11 published acceptance scenarios, two deterministic repository Explorer renders, rendered-template equality, integrity checks, and an injected rollback fixture pass. Exact commands, hashes, deviations, authority boundaries, and residual hosted-CI risk are retained in `docs/engineering/self-hosting-boundary/evidence/WO-SHB-004-verification.md`.

`implemented` records completed local work and evidence only. The accepted `main` branch remains governed by 0.2.1 until a later candidate commit, commit-bound verification record, accountable assurance decision, successful hosted CI, review, and merge accept this promotion. No VREC transition, merge, tag, release, publication, deployment, force push, or history rewrite is claimed.
