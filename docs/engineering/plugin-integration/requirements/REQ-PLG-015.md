+++
id = "REQ-PLG-015"
type = "requirement"
title = "Repository connection through the released installer"
status = "draft"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "WHEN connecting or upgrading a repository, THE SETUP SKILL SHALL use the selected released installer's reviewed operation within existing authority."
verification_method = ["test"]
priority = "must"
source = "PR #360 at 9e894e99; plugin implementation request, 2026-09-08"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Repository connection through the released installer

## In plain words

The plugin uses the existing installer to connect a repository. Its user-facing setup flow does not recreate file ownership or upgrade rules.

## Why

A second installer would drift from managed-file protections and could overwrite owner content. Reviewing the real operation also makes the affected target and changed files explicit. Plugin updates alone do not authorize changes to a repository's evaluator lock.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| Setup connects a repository or performs an explicitly requested repository upgrade. | Use the selected release's inspected preview and application forms for the reviewed operation. | Stop on installer conflict, changed scope, absent authority or unavailable command. |

## Examples

### Normal

**Given** an intact target and an existing request covering the proposed installation,

**When** setup previews the selected released installer's operation,

**Then** it applies only that still-covered operation and checks the resulting installation.

### Failure

**Given** a customized managed file blocks a requested upgrade,

**When** the installer reports the conflict,

**Then** setup preserves the file and reports the blocker instead of replacing it manually.
