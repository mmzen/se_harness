+++
id = "REQ-HUP-037"
type = "requirement"
title = "Adopt the published 0.18.0 evaluator"
status = "approved"
owners = ["repository-owner", "engineering-owner"]
created = "2026-09-15"
updated = "2026-09-15"
statement = "THE INSTALLER SHALL adopt published evaluator 0.18.0 through one recorded transaction that preserves repository-owned content."
verification_method = ["test", "inspection"]
priority = "must"
source = "Owner request on 2026-09-15 to upgrade the current evaluator to 0.18.0; published release RLS-SEH-027."

[relations]
derives_from = ["CAP-HUP-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-15T11:01:51Z"
decided_by = "repository-owner"
reason = "The owner replied \"i approve evaluator upgrade\" to the reviewed WO-HUP-019 scope and its five governing drafts on 2026-09-15. This records approval of the selected artifact, including the proposed architecture assessment and required assurance classification where applicable. The accepted scope authorizes start, completion only after passing checks, and ready verification-record preparation; independent verification and external integration remain separate."
+++

# Adopt the published 0.18.0 evaluator

## In plain words

This repository will use the published 0.18.0 checker. Its installation record will identify the exact downloaded package.

## Why

The repository still uses 0.17.0. The owner requested the published successor, including its simpler workflow and file ownership rules.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| An authorized upgrade uses the verified public package | One recorded transaction installs the selected checker and preserves owner content | Stop before application when integrity, package identity or the reviewed plan differs |

## Examples

### Normal

**Given** the approved scope and verified package, **when** the upgrade runs, **then** the installation names 0.18.0 and a repeat changes nothing.

### Failure

**Given** a package with a different checksum, **when** preparation checks it, **then** installation stops before repository changes.
