+++
id = "REL-PYP-001"
type = "release_contract"
title = "Activate governed PyPI publication automation"
status = "draft"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
gates = ["WO-PYP-001"]
+++

# Release Contract: Activate governed PyPI publication automation

## Release unit

The repository-specific publication workflow, its static tests, formal contract, GitHub `pypi` environment configuration, and retained implementation evidence. This release unit configures capability; it is not a Python distribution version or authorization to dispatch the workflow.

## Required evidence

Complete `VER-PYP-001` implementation evidence, a valid graph, passing full unit suite and CLI/doctor checks, reviewed immutable action SHA, GitHub workflow parsing, inspected environment state, and owner confirmation that PyPI trusts the exact workflow/environment identity.

## Compatibility and migration

No CLI, package runtime, installed template, version, or existing release artifact changes. Existing `RLS-SEH-001` and `v0.2.0` remain immutable. Removing or renaming the workflow/environment requires coordinated PyPI publisher changes.

## Security and provenance

Activation retains no PyPI secret and grants no publication authority. Each later publication must name an already released tag, exact independent hashes, target PyPI project, and separate accountable owner decision.

## Promotion policy

Merge only after required checks and security review. Do not dispatch until the workflow exists on the trusted default branch, the environment protection and PyPI publisher match, and a separate publication authorization is retained.

## Human approval triggers

Security owner approves action pin, permissions, shell/input handling, and external identity configuration. Quality owner approves invariant tests. Release owner separately approves every production workflow dispatch and its exact artifacts.

## Rollback criteria and procedure

Disable the workflow and PyPI trusted publisher if identity, permissions, action integrity, or environment protection diverges. Preserve published PyPI history and evidence. A defective package requires a new verified version, not replacement.

## Post-release observation window

Review the first authorized publication end to end and inspect configuration before each subsequent release until at least two successful versions establish stable operation.
