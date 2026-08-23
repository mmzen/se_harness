+++
id = "INT-HUP-002"
type = "intent"
title = "Govern the standard root with released se-harness 0.6.0"
status = "approved"
owners = ["repository-owner", "engineering-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[relations]
+++

# Intent: Govern the standard root with released se-harness 0.6.0

## Problem

The repository's product release is 0.6.0, but its installed standard root and managed evaluator workflow remain pinned to released 0.5.0 under a schema-2 lock. That predecessor boundary was required while 0.6.0 was a candidate. Now that the exact 0.6.0 wheel is independently published, leaving the root on 0.5.0 preserves known full-graph incompatibility, keeps retired repository-context ownership in the lock, and prevents the repository from using the released schema-3 mutation and evidence controls it ships to consumers.

## Desired outcomes

- The installed standard root, managed workflow, managed contract, and lock select the exact immutable public `se-harness==0.6.0` evaluator.
- The applying evaluator is isolated outside the checkout and its version, payload, archive, origins, entry point, and checkout exclusion are proven before mutation.
- The supported transaction installs the reviewed 0.6.0 managed surface, advances the lock from schema 2 to schema 3, and retains work-order-keyed evaluator-upgrade evidence.
- Existing owner content, including `docs/engineering/REPOSITORY_CONTEXT.md`, is preserved while withdrawn harness ownership of that path is removed from the lock.
- Candidate source and package roles remain non-governing evidence, and no product release or external action is combined with root adoption.

## Actors and stakeholders

- The repository owner decides whether the governing baseline may change.
- The technical and engineering owners approve the exact managed transition and no-significant-decision assessment.
- The security and assurance owners assess evaluator identity, transaction integrity, role separation, and retained evidence.
- Contributors and hosted CI rely on the resulting exact released governor.

## Success measures

| Measure | Baseline | Target | Observation window |
|---|---:|---:|---|
| Installed evaluator | exact public 0.5.0 | exact public 0.6.0 | apply and review |
| Integrity lock | schema 2 | schema 3 with exact evaluator identity | apply and no-op replay |
| Candidate graph errors | 0 under released 0.6.0 | 0 | pre/post apply |
| Owner-content overwrites | 0 | 0 | entire transaction |
| Cross-role imports | prohibited | 0 | every evaluator check |

## Non-goals

- Changing `se_harness/`, `templates/repository/standard/`, package metadata, release records, published artifacts, or product version.
- Deleting, moving, or rewriting `docs/engineering/REPOSITORY_CONTEXT.md`; after upgrade it remains ordinary owner content.
- Creating a candidate commit, VREC, pull request, merge, tag, release, publication, deployment, protected-environment decision, or other external action.
- Using the maintainer-only recovery path while the normal published-evaluator transaction remains available.

## Principles and immutable constraints

- The governor is the independently installed public 0.6.0 wheel, never checkout source, an editable install, or a locally built candidate.
- The 0.5.0 lock remains authoritative until this packet is approved and the exact target evaluator applies the supported transaction.
- Customized, conflicting, ambiguous, or expanded managed state stops without partial mutation.
- Governor adoption and product release remain separate work and separate decisions.

## Risks and assumptions

- Fact: public wheel `se_harness-0.6.0-py3-none-any.whl` has SHA-256 `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`.
- Fact: its installed payload SHA-256 is `c233678548fe742b7a7a5a8bd65de10156ff233edc65b68e2ed0333fbe4dea42` under `se-harness-installed-payload-v1`.
- Fact: the reviewed read-only plan contains 18 additions or updates and 18 unchanged managed paths.
- Risk: the root validator and policy surface changes materially between 0.5.0 and 0.6.0; exact plan review, schema-3 identity binding, post-apply validation, and no-op replay mitigate it.
- Open decision: accountable owners must approve the complete HUP-002 packet and exact plan before implementation.

## Approval

On 2026-08-23 the accountable owner explicitly approved `INT-HUP-002`, the complete HUP-002 definition chain, `ARCH-HUP-002` including its `no_significant_decision` assessment, the exact 18-change managed plan, and `WO-HUP-002` for implementation. The decision authorizes only the bound standard-root transition to released 0.6.0; candidate commit, VREC, push, pull request, merge, release, publication, deployment, and every other external action remain unauthorized.
