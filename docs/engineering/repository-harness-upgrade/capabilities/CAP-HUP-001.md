+++
id = "CAP-HUP-001"
type = "capability"
title = "Upgrade the repository governor without self-governance"
status = "approved"
owners = ["repository-owner", "engineering-owner"]
created = "2026-08-20"
updated = "2026-08-20"

[relations]
derives_from = ["INT-HUP-001"]
+++

# Capability: Upgrade the repository governor without self-governance

## Actor and need

The repository owner needs to advance the standard root to a newer immutable evaluator while maintainers need proof that neither checkout source nor a candidate package governed the transition.

## Capability statement

`A repository owner can upgrade the standard root to exact released se-harness 0.5.0 through a managed, reviewable transaction while product candidates remain untrusted evidence.`

## Boundaries

- Applies only to the root standard-repository installation and its managed evaluator workflow.
- Consumes the immutable public 0.5.0 distribution from an isolated environment.
- Preserves repository-owned workflows, publication policy, product source, package version, formal history, and external state.
- Grants no approval, verification, merge, release, publication, deployment, or environment authority.

## Outcomes

- Root configuration, managed contract, lock, and hosted evaluator agree on 0.5.0.
- Managed integrity, formal validation, preflight, and role-separation checks pass.
- The candidate contains retained evidence sufficient for accountable verification.

## Candidate requirements

- `REQ-HUP-001`: prove the exact released evaluator identity.
- `REQ-HUP-002`: apply only a safe managed standard-root transaction.
- `REQ-HUP-003`: preserve role separation and provide fail-closed review and rollback evidence.
