+++
id = "REQ-PMI-007"
type = "requirement"
title = "Preserve installation and authority boundaries"
status = "implemented"
owners = ["repository-owner", "security-owner", "release-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN portable integrity support is introduced, THE SYSTEM SHALL preserve the single standard installation, path and symlink safety, atomic non-overwrite behavior, existing CLI compatibility, and separate human verification and release authority."
verification_method = "automated-test-and-review"

[relations]
derives_from = ["CAP-PMI-001"]
+++

# Requirement: Preserve installation and authority boundaries

## Rationale

A corrective integrity change must not broaden filesystem authority or couple diagnostics to governance actions.

## Preconditions and trigger

Any new lock schema, migration path, or diagnostic behavior is exercised.

## Required response

Keep one standard template and existing commands. Preserve target containment, symlink rejection, atomic writes, customized-file preservation, bounded diagnostics, and ready-record-only automation. No integrity result may approve verification, release, tags, publication, or deployment.

## Failure and boundary behavior

Unsafe paths, symlink traversal, malformed locks, unknown modes, and partial writes fail without mutation.

## Constraints

Python 3.11 or later and the standard library remain the runtime contract. Existing schema-1 repositories remain operable under the conservative migration rules.

## Acceptance examples

All existing init, adopt, upgrade, provenance, and path-safety regressions continue to pass unchanged.

## Open decisions

None when approved.
