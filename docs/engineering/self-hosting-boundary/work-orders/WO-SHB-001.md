+++
id = "WO-SHB-001"
type = "work_order"
title = "Implement isolated self-hosting governance and candidate qualification"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "technical-owner", "quality-owner", "security-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
implements = ["REQ-SHB-001", "REQ-SHB-002", "REQ-SHB-003", "REQ-SHB-004", "REQ-SHB-005", "REQ-SHB-006"]
specifications = ["SPEC-SHB-001"]
architecture = ["ARCH-SHB-001", "ADR-SHB-001"]
verification = ["VER-SHB-001"]
+++

# Work Order: Implement isolated self-hosting governance and candidate qualification

## Lifecycle

The accountable owner approved implementation on 2026-08-12 with the instruction `go for implementation`. Approval authorizes only the bounded local implementation and retained evidence described here. Commit, push, pull-request update, verification capture or transition, release decision, tag, publication, deployment, merge, and historical-record disposition require their applicable later decisions.

## Authorization

- Decision: implementation approved
- Accountable instruction: `go for implementation`
- Decision date: 2026-08-12
- Authorized scope: the `In scope` section of this work order

## Objective

Replace mixed candidate/governor self-hosting with explicit released-governor, candidate-source, and candidate-package planes; correct PR #28's false cross-version integrity gate; prevent import shadowing; and establish a repeatable post-release governor-promotion cycle.

## In scope

- Add explicit self-hosting governor metadata independent of candidate version metadata.
- Add deterministic runtime-role identity and resolved-origin checks.
- Refactor self-hosting CI into governor, candidate-source, and candidate-package gates.
- Run governor integrity only against a governor-created temporary target.
- Ensure installed-governor compatibility checks cannot import checkout source.
- Move candidate distribution parity and behavioral acceptance to fresh candidate-created targets.
- Redefine repository-specific root/canonical parity so only the self-hosting configuration and workflow differ, while governor same-version state remains external and consumer parity remains unchanged.
- Update the self-hosting workflow, owner instructions, repository context, installer/test helpers, canonical content where applicable, and schema-2 integrity behavior transactionally.
- Add one-time migration behavior from the current mixed 0.2.2 state and future post-publication governor-promotion procedure.
- Preserve closed PR #28 as the audit trail for `VREC-SEH-003` and `RLS-SEH-003`, exclude both files from the clean recovery branch, and make their ineligibility for a changed candidate visible.
- Execute `VER-SHB-001`, retain evidence, and stop for separate candidate commit and replacement aggregate verification authority.

## Out of scope

Consumer installation profiles; weakening exact-hash acquisition; treating candidate checks as independent authority; allowing old governors to approve unknown semantics; automatic host promotion; publishing or tagging; changing protected environments; mutating historical VREC/RLS identity or status; resolving every historical layout/legacy warning; force push; merge; and deployment.

## Expected change surface

- Self-hosting CI and its candidate template or repository-specific control split.
- Governor/candidate version and digest configuration.
- Runtime identity helpers and CLI/workflow integration.
- Installer, integrity, preflight, and package/test helpers needed for explicit target ownership.
- Repository-specific `AGENTS.md` constraints and `REPOSITORY_CONTEXT.md` commands/boundaries.
- Root host installation, canonical candidate templates, lock semantics, and parity tests.
- Focused self-hosting, security, workflow, public onboarding, release-build, and full regression tests.
- Retained evidence and current release recovery documentation.

## Implementation plan

1. Obtain approval for the complete SHB packet and record the significant decision in `ADR-SHB-001`.
2. Run start preflight and read the complete governing manifest.
3. Capture failing tests for cross-version `doctor`, local import shadowing, role substitution, checkout mutation, and reused release records.
4. Introduce the identity/role contract and isolated environments with fail-closed path checks.
5. Refactor CI into three non-substitutable gates and prove the true installed governor is used.
6. Separate host-governor integrity from candidate distribution parity and implement the one-time migration transactionally.
7. Add candidate-package acceptance and post-release governor-promotion fixtures.
8. Run `VER-SHB-001`, full supported-runtime regression, exact-candidate packaging, fresh-install smoke, formal graph, preflight, Explorer, and diff hygiene.
9. Retain evidence, move implementation artifacts to `implemented`, and stop for separate commit and commit-bound verification authority.

## Required verification

Execute every case in `VER-SHB-001`. Required evidence includes true package origins, process isolation, path-adversary matrices, no-write snapshots, three-lane workflow structure, candidate-source and package behavior, exact build hashes, managed-state ownership, transactional migration, prior-record preservation, and GitHub CI results after any separately authorized push.

## Migration and current PR

The current PR may not be made green by deleting a failing check, relabeling candidate execution as baseline, bypassing required CI, or adding a post-candidate workflow commit while continuing to release candidate `9ba0cec3710167ad4568931747ed5f4e48a63532`. Implementation produces a new candidate and later replacement VREC/RLS before any external release action.

## Stop and escalate conditions

Stop if implementation requires a consumer profile, cannot prove runtime origin, lets isolated lanes write the checkout, weakens governor immutability, loses candidate package acceptance, changes historical captured fields, treats a skipped lane as pass, cannot define a transactional migration, or needs authority beyond this work order.

## Completion report

Report the selected governor, identity model, host/candidate state ownership, CI lanes, migration behavior, changed components, dual-runtime and package results, exact origins and hashes, prior-record preservation, residual risks, evidence path, lifecycle state, and explicitly unperformed external actions.
