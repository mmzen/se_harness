+++
id = "CAP-HUP-002"
type = "capability"
title = "Adopt the independently released current governor"
status = "approved"
owners = ["repository-owner", "engineering-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[relations]
derives_from = ["INT-HUP-002"]
+++

# Capability: Adopt the independently released current governor

## Actor and need

The repository owner needs to advance the standard root from the released predecessor evaluator to the independently published product release without allowing checkout source or candidate packages to govern their own adoption.

## Capability statement

`A repository owner can adopt exact released se-harness 0.6.0 through one identity-bound, transactional, reviewable standard-root upgrade while preserving owner content and evaluator/candidate separation.`

## Boundaries

- Applies only to the repository's standard managed root, evaluator workflow, integrity lock, and keyed upgrade evidence.
- Consumes the immutable public 0.6.0 wheel from an isolated environment outside the checkout.
- Preserves product source, canonical package templates, release history, repository-specific workflows, publication policy, and external state.
- Retires harness ownership of repository context without changing the owner file's bytes.
- Grants no approval, verification, commit, merge, release, publication, deployment, or operating authority.

## Outcomes

- Root configuration, managed contract, workflow, lock, and external runtime agree on 0.6.0.
- The lock uses schema 3 and binds the exact public evaluator payload and archive.
- Managed integrity, complete-graph validation, release-distribution validation, tests, and no-op replay pass.
- Retained evidence is sufficient for later independent commit-bound verification.

## Candidate requirements

- `REQ-HUP-004`: prove the exact released 0.6.0 evaluator identity.
- `REQ-HUP-005`: apply only the exact reviewed schema-3 standard-root transaction.
- `REQ-HUP-006`: preserve owner content, formal history, and evaluator/candidate role separation.
