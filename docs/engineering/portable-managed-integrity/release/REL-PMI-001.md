+++
id = "REL-PMI-001"
type = "release_contract"
title = "Release portable managed-file integrity"
status = "rejected"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-16"

[relations]
gates = ["WO-PMI-001"]
+++

# Release Contract: Release portable managed-file integrity

## Release unit

The versioned `se-harness` source, wheel, canonical standard template, lock schema documentation, and migration behavior implementing portable managed-text integrity.

## Required evidence

Complete `VER-PMI-001` evidence; valid artifact graph; passing full test suite; passing source-repository doctor; LF/CRLF and legacy migration matrices; source/canonical parity; inspected wheel; fresh installation; and a verified record bound to the exact corrected candidate.

## Compatibility and migration

Schema-1 locks remain readable and migrate only under the proven-safe rules. Existing customized files and fragments remain untouched. Existing command names, single standard installation, Python version, and standard-library runtime remain compatible.

## Security and provenance

Canonicalization is limited to text line terminators. Non-newline changes, paths, fragments, symlinks, atomicity, and commit-bound provenance remain strict. The source, wheel, verification record, release record, and tag must agree on one candidate commit.

## Promotion policy

Promotion requires zero blocking diagnostics, no unexplained doctor deviation, deterministic schema-2 locks, a reproducible wheel and checksum, fresh LF/CRLF smoke tests, retained migration evidence, and explicit release-owner authorization.

## Human approval triggers

Quality and security owners approve integrity and migration evidence. Repository owners approve any legacy ambiguity resolution. Release owners approve version, tag, package publication, and rollout. Binary support or weaker equivalence requires a new ADR.

## Rollback criteria and procedure

Do not publish if real customization is missed, newline-only content fails after safe migration, lock generation is nondeterministic, the source doctor fails, or wheel behavior differs. If already published, preserve affected evidence, withdraw or mark the version affected where supported, and publish a separately verified corrective version without moving an existing tag.

## Post-release observation window

Observe the first installations and upgrades on Windows and a LF-native platform through one subsequent release cycle. Review customized classifications and legacy migration advisories before closing the change.

## Disposition

This per-feature proposal was never selected as release authority. `WO-PMI-001` was released in `0.2.0` under aggregate contract `REL-DST-001` and released record `RLS-SEH-001` at tag `v0.2.0`. The rejected status disposes of this unused proposal; it does not reject the released implementation.
