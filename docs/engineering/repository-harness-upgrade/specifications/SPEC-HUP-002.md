+++
id = "SPEC-HUP-002"
type = "specification"
title = "Standard-root 0.6.0 evaluator adoption contract"
status = "approved"
owners = ["technical-owner", "engineering-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[relations]
specifies = ["REQ-HUP-004", "REQ-HUP-005", "REQ-HUP-006"]
+++

# Specification: Standard-root 0.6.0 evaluator adoption contract

## Scope

Define one repository-local, plan-first transition from the installed immutable public 0.5.0 governor and schema-2 lock to the independently published 0.6.0 governor and schema-3 lock, without changing product, release, publication, historical, or external state.

## Actors and external systems

- Accountable repository, engineering, technical, assurance, and security owners.
- Immutable PyPI/GitHub distribution state selected by `RLS-SEH-012`.
- The external 0.6.0 Python environment and `harnessctl` entry point.
- The repository worktree, managed lock, GitHub Actions, and candidate evidence workflow.

## Inputs

- Clean baseline commit `cccbaa70a6c5a33e19decec0d78f26afd87d5f9e` and current `.engineering-harness.lock` SHA-256 `c4c4191998cad431620324dba2ad205c190fcf2802847278cabec92e853989af`.
- Public wheel `se_harness-0.6.0-py3-none-any.whl`, archive SHA-256 `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`, and installed payload SHA-256 `c233678548fe742b7a7a5a8bd65de10156ff233edc65b68e2ed0333fbe4dea42`.
- Approved HUP-002 definition chain, approved or in-progress `WO-HUP-002`, and exact read-only plan review.

## Outputs

- A reviewable candidate whose managed standard root consistently identifies 0.6.0 and whose schema-3 lock binds the exact evaluator.
- Canonical evaluator-transition evidence at `docs/engineering/repository-harness-upgrade/evidence/WO-HUP-002-evaluator-upgrade.json`.
- Implementation evidence at `docs/engineering/repository-harness-upgrade/evidence/WO-HUP-002-verification.md` after authorized apply and checks.
- No product, release, tag, publication, deployment, owner-content, or external-policy mutation.

## State model

`draft packet -> accountable approval -> read-only plan recheck -> in-progress bounded apply -> implemented evidence -> separately authorized candidate commit -> ready VREC -> assurance decision -> merge`

This specification authorizes none of those transitions by itself.

## Behavioral rules

1. Acquire the already-published target wheel outside the repository and reconcile its SHA-256 with `RLS-SEH-012` before installation.
2. Prove released-evaluator identity in isolated mode, including exact payload and archive identity and complete checkout exclusion.
3. Retain the current 0.5.0 full-root start-preflight result and require it to contain only the declared `A-E009`/`A-E010` predecessor diagnostics for `RLS-SEH-009` and `RLS-SEH-012`; any other diagnostic stops.
4. Under the four-owner deadlock declaration, run the no-network recovery rehearsal and require complete rollback, restoration, negative-case, absence, and external-action invariants before the real transaction.
5. Require `[evaluator_upgrade]` to bind the exact prior lock bytes and immutable target identity.
6. Re-run read-only planning immediately before apply and require exact membership and action agreement with `REQ-HUP-005`.
7. Apply only with the external target evaluator, explicit work order, and repository-relative keyed evidence output.
8. Preserve owner-controlled marker surroundings and the complete bytes of `docs/engineering/REPOSITORY_CONTEXT.md`.
9. Regenerate one schema-3 lock containing the evaluator version, payload manifest/digest, archive name/digest, and managed file inventory.
10. Require no-op replay, doctor, complete-graph validation, inspection, dashboard, release-distribution validation, tests, CLI help, and diff/scope checks.
11. Treat candidate source/package results as evidence only; do not import them into the governor runtime.
12. Stop before commit, VREC, push, PR, merge, tag, release, publication, deployment, or other external action without separate authority.

## Error and recovery behavior

- Identity or digest mismatch: stop before plan reliance or mutation.
- Any current-governor preflight output beyond the exact declared predecessor `A-E009`/`A-E010` set: stop before mutation.
- Failed recovery rehearsal or any credential signal: stop before mutation.
- Invalid or expanded plan: retain output and request an amendment without applying.
- Customized, ambiguous, or concurrently changed managed state: stop atomically.
- Write or postcondition failure: restore the complete pre-write snapshot and retain failure evidence.
- Verification failure: leave `WO-HUP-002` in its current state and remediate only within approved scope.

## Data and interface contracts

The resulting `.engineering-harness.toml`, `ENGINEERING_HARNESS.md`, and managed workflow select 0.6.0. The lock conforms to schema 3 and embeds the exact target evaluator identity. `QUALITY_GATES.json` and `WORKFLOW.json` are present and managed. The lock contains no `docs/engineering/REPOSITORY_CONTEXT.md` entry or tombstone.

## Security and privacy properties

No credential is required. Public hashes, normalized origins, commands, and results may be retained; usernames, disposable absolute paths, tokens, environment dumps, and private host data must not enter committed evidence.

## Compatibility and migration

The transaction uses the normal upgrade path shipped by public 0.6.0. It implements the repository-context retirement described by `WO-DST-021`: the existing file is untouched and becomes owner content, the C diagnostic family and preflight repository-commands payload are retired, and repository facts remain in the owner-controlled `AGENTS.md` region.

## Examples and counterexamples

- Valid: exact public 0.6.0 plans the approved surface, matches `WO-HUP-002`, applies atomically, retains evidence, and reports a no-op replay.
- Invalid: running checkout `python -m se_harness upgrade --apply`.
- Invalid: deleting `REPOSITORY_CONTEXT.md` because its lock entry is retired.
- Invalid: accepting a plan with one extra managed update without amending and reapproving the work order.
- Invalid: combining root adoption with product changes, release history, publication, or external actions.

## Explicitly unspecified decisions

Implementation may choose disposable external directory names and the ordering of independent read-only checks. It may not select another evaluator identity, alter the plan, waive a gate, or exercise lifecycle or external authority.
