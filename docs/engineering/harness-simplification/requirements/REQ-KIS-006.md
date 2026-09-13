+++
id = "REQ-KIS-006"
type = "requirement"
title = "Keep new evidence small and assess historical archives"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-13"
updated = "2026-09-13"

statement = "THE PIPELINE SHALL retain concise current evidence with retrievable raw results instead of committing copied repositories and repeated raw trees."
verification_method = ["test", "inspection"]
priority = "must"
source = "Accepted 2026-09-13 codebase KISS review; evidence/WO-KIS-001/governance/owner-request.md"

[relations]
derives_from = ["CAP-KIS-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-13T16:40:43Z"
decided_by = "requirements-steward"
reason = "The owner accepted all 38 candidates in the retained 2026-09-13 codebase KISS review and requested the work orders: \"OK ! Let's create the work orders to implement all candidates\". Record the requirements-steward approval of REQ-KIS-006 within that accepted scope and the established delegated route. SPEC-KIS-001 makes the replacement contracts and seven retained protections explicit; the coverage map assigns all candidates. This records definition approval or bounded execution delegation only, not implementation start, completion, verification, release, merge, publication, live adoption or historical evidence deletion."
+++

# Keep new evidence small and assess historical archives

## In plain words

New runs retain useful summaries and downloadable logs; the owner gets an inventory of existing large bundles.

## Why

Historical evidence is 232.53 MiB of the reviewed 250.44 MiB checkout; new runs should not continue that growth.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| The owner uses the affected operation. | New runs retain useful summaries and downloadable logs; the owner gets an inventory of existing large bundles. | A missing or expired raw artifact is reported as unavailable; a short-lived download link is not claimed to be permanent evidence. |

## Examples

### Normal

**Given** an approved task with the required inputs. **When** the affected operation runs. **Then** it meets the candidate-specific checks in VER-KIS-001.

### Failure

**Given** the actual failure described above. **When** the affected operation runs. **Then** it reports that failure without claiming a pass.
