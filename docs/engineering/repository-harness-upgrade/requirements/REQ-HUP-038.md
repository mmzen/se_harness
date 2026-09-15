+++
id = "REQ-HUP-038"
type = "requirement"
title = "Keep repository development consistent with the adopted evaluator"
status = "approved"
owners = ["repository-owner", "engineering-owner"]
created = "2026-09-15"
updated = "2026-09-15"
statement = "THE REPOSITORY SHALL retain consistent development, guidance and continuous-integration identities after adopting evaluator 0.18.0."
verification_method = ["test", "inspection"]
priority = "must"
source = "Owner upgrade request; rehearsal showing a retained 0.17.0 workflow and equal evaluator/candidate versions."

[relations]
derives_from = ["CAP-HUP-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-15T11:01:51Z"
decided_by = "repository-owner"
reason = "The owner replied \"i approve evaluator upgrade\" to the reviewed WO-HUP-019 scope and its five governing drafts on 2026-09-15. This records approval of the selected artifact, including the proposed architecture assessment and required assurance classification where applicable. The accepted scope authorizes start, completion only after passing checks, and ready verification-record preparation; independent verification and external integration remain separate."
+++

# Keep repository development consistent with the adopted evaluator

## In plain words

Local instructions and automated checks will use the adopted checker. Development will identify the next candidate separately.

## Why

The default upgrade retains the old workflow and human guidance. Equal candidate and released versions also prevent the existing upgrade rehearsal.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| The repository adopts the new evaluator | Instructions, supplied workflow and candidate identity agree with the new installation | Stop for a bounded correction if checks expose a mismatch |

## Examples

### Normal

**Given** the completed adoption, **when** the repository derives its identities, **then** it reports evaluator 0.18.0 and candidate 0.19.0.

### Failure

**Given** an unchanged 0.18.0 candidate, **when** identity derivation runs after adoption, **then** it refuses the equal versions.
