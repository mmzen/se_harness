+++
id = "CAP-RLO-002"
type = "capability"
title = "Separate portable release governance from repository publication"
status = "approved"
owners = ["product-owner", "release-owner"]
created = "2026-08-18"
updated = "2026-08-18"

[relations]
derives_from = ["INT-RLO-001"]
+++

# Capability: Separate portable release governance from repository publication

## Actor and need

A repository owner needs SE Harness to prepare accountable release decisions without imposing the `se_harness` project's Python packaging and publication mechanics on every consumer repository.

## Capability statement

`A repository owner can use portable SE Harness for format-neutral release governance while the target repository independently validates and executes its own release payload and publication policy.`

## Boundaries

- Portable SE Harness owns RLS identity, relations, lifecycle constraints, and commit-bound provenance.
- The `se_harness` repository owns its wheel, sdist, checksum, GitHub Release, PyPI, Pages, and replay contracts.
- Repository-specific scripts may consume core RLS facts, but portable runtime and managed consumer files may not depend on those scripts or encode their policy.
- Neither layer approves a release, commits a record, publishes software, or exercises an accountable lifecycle transition.

## Outcomes

- Consumer installations expose no SE Harness-package-specific release input, template guidance, or validation rule.
- The `se_harness` repository retains deterministic, exact distribution provenance and one-input last-mile publication.
- Dependency direction remains from repository policy to portable governance, never from portable governance to one repository's release mechanics.
- Previously released RLS artifacts remain valid and historical RLO-001 evidence remains unchanged.

## Candidate requirements

`REQ-RLO-009` through `REQ-RLO-011` define the portable boundary, repository-owned distribution binding, and preserved release-orchestration guarantees.

## Approval

On 2026-08-18 the accountable repository owner stated `I approve this plan, you can create the artifact pack for it`. This approves this capability and its linked definition artifacts. It authorizes creation of the packet only; `WO-RLO-002` remains `draft` and grants no implementation authority.
