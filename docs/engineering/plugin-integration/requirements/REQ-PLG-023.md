+++
id = "REQ-PLG-023"
type = "requirement"
title = "Preserve repository version during maintenance"
status = "draft"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "WHEN plugin maintenance occurs, THE SETUP SKILL SHALL preserve the repository governing version unless an explicitly authorized repository upgrade applies the existing installer procedure."
verification_method = ["test", "inspection"]
priority = "must"
source = "PR #360 and owner plugin-installation feedback, 2026-09-08"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Preserve repository version during maintenance

## In plain words

Updating the plugin does not silently update the project rules. A repository upgrade remains a separate authorized change.

## Why

Later decisions depend on the recorded evaluator version. Plugin updates cannot silently replace that authority.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| Plugin update, repair, or removal | Preserve project version and retained governance | Stop incompatible use and identify the maintenance choice |

## Examples

### Normal

**Given** a project requiring an older evaluator.

**When** a newer plugin is installed.

**Then** ordinary governed use stops without changing the project lock.

### Failure

**Given** a managed file conflicts during authorized upgrade.

**When** the installer refuses.

**Then** owner content and historical evidence remain intact.
