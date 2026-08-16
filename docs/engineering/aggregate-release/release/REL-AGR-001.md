+++
id = "REL-AGR-001"
type = "release_contract"
title = "Release aggregate provenance support"
status = "rejected"
owners = ["release-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-16"

[relations]
gates = ["WO-AGR-001"]
+++

# Release Contract: Release aggregate provenance support

## Release unit

The versioned `se-harness` wheel, source tag, canonical standard template, and documentation implementing aggregate verification and release manifests.

## Required evidence

Complete `VER-AGR-001` evidence; valid artifact graph; passing unit, CLI, dashboard, init/adopt/upgrade, and wheel-install tests; and an aggregate verification record bound to the exact release candidate.

## Compatibility and migration

Existing single-work-order records and commands remain valid. Installed customized files are preserved under existing ownership rules. No additional installation profile is introduced.

## Security and provenance

All scope and paths are explicit and validated. The released record, verification, tag, and wheel source agree on one full candidate commit. Preparation commands remain non-authorizing and do not mutate Git.

## Promotion policy

Promotion requires a verified candidate, zero blocking validation errors, retained evidence, a reproducible wheel and checksum, a clean fresh-environment smoke test, and explicit release-owner authorization.

## Human approval triggers

Quality owners approve aggregate verification. Release owners approve version, work scope, tag, and publication. Any scope inference, commit exception, or compatibility deviation requires escalation.

## Rollback criteria and procedure

Do not publish when provenance, scope, installation, or smoke verification fails. If already published, withdraw or mark the release affected according to hosting capabilities, preserve audit records, and prepare a separately verified corrective version rather than moving the tag.

## Post-release observation window

Review the first aggregate release installation, upgrade, dashboard, and provenance workflow before using the feature for the next production version.

## Disposition

This per-feature proposal was never selected as release authority. `WO-AGR-001` was released in `0.2.0` under aggregate contract `REL-DST-001` and released record `RLS-SEH-001` at tag `v0.2.0`. The rejected status disposes of this unused proposal; it does not reject the released implementation.
