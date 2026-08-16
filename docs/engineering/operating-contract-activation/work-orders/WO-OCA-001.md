+++
id = "WO-OCA-001"
type = "work_order"
title = "Activate the six current operating contracts"
status = "implemented"
owners = ["service-owner", "repository-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
implements = ["REQ-OCA-001"]
specifications = ["SPEC-OCA-001"]
verification = ["VER-OCA-001"]
+++

# Work Order: Activate the six current operating contracts

## Lifecycle and authorization

The repository owner explicitly approved the ready intent-through-verification chain and authorized this bounded work order on 2026-08-16, with one later aggregate VREC planned for the completed maintenance candidate. The bounded work and retained evidence are complete, so this work order is now `implemented`. That state records completion, not independent assurance. No commit, VREC creation or transition, push, pull request, merge, release, tag, publication, or deployment is authorized.

No architecture artifact or ADR applies: this work changes governance definitions and a managed authoring example, introduces no software structure, and no active architecture addresses `REQ-OCA-001`.

## Objective

Turn the six applicable draft operating proposals into explicit, usable, human-approved continuing obligations while preserving the independent draft status and authority of every release proposal.

## In scope

- Normalize and activate the exact six contracts in `SPEC-OCA-001`.
- Complete the two partial contracts and review the four detailed contracts against current behavior.
- Update the six affected domain indexes.
- Correct root and canonical operating-contract authoring examples and synchronize managed integrity through the supported path.
- Retain exact work-order evidence and stop at an uncommitted implementation state.

## Out of scope

Changing or superseding `REL-*`; changing validator relation typing; altering CLI, workflow, dashboard, package version, VREC, RLS, source code, tests unrelated to managed parity, releases, tags, publication, or deployment.

## Authorized decision envelope

Implementation may refine wording and select concrete existing commands or evidence paths. It may not reduce accountable ownership, add an unimplemented service guarantee, broaden automation authority, change the contract set, or add executable behavior.

## Expected change surface

- Six `OPS-*.md` records and six domain `README.md` indexes.
- Root and canonical `OPERATING_CONTRACT.template.md` plus `.engineering-harness.lock` through supported synchronization.
- This packet and its retained evidence.

## Required verification

Perform the complete `VER-OCA-001` matrix, formal validation, doctor, start and review preflight, deterministic inspection, managed parity checks, full tests if the managed synchronization affects packaged distribution, and `git diff --check`.

## Stop and escalate conditions

Stop if any activation requires new runtime behavior, a release decision, a validator semantic change, an unsupported external service, owner-content overwrite, or a seventh contract.

## Completion report format

Report the six final statuses and exact requirement sets, before/after queue counts, managed-template synchronization, verification results, unchanged release artifacts, deviations, and the deferred validator-enforcement gap.
