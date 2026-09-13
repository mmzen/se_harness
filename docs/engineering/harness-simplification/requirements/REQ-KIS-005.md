+++
id = "REQ-KIS-005"
type = "requirement"
title = "Shorten CI and resume interrupted publication"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-13"
updated = "2026-09-13"

statement = "THE PIPELINE SHALL run qualification when relevant and resume an incomplete unpublished draft without weakening checks on required release artifacts."
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
reason = "The owner accepted all 38 candidates in the retained 2026-09-13 codebase KISS review and requested the work orders: \"OK ! Let's create the work orders to implement all candidates\". Record the requirements-steward approval of REQ-KIS-005 within that accepted scope and the established delegated route. SPEC-KIS-001 makes the replacement contracts and seven retained protections explicit; the coverage map assigns all candidates. This records definition approval or bounded execution delegation only, not implementation start, completion, verification, release, merge, publication, live adoption or historical evidence deletion."
+++

# Shorten CI and resume interrupted publication

## In plain words

Normal pull requests avoid release rehearsals; an unpublished draft resumes by uploading only missing required assets.

## Why

Repeated release builds and an all-or-nothing draft upload cost time without helping ordinary changes.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| The owner uses the affected operation. | Normal pull requests avoid release rehearsals; an unpublished draft resumes by uploading only missing required assets. | Conflicting required assets, missing release authority and candidate access to publication credentials still fail. |

## Examples

### Normal

**Given** an approved task with the required inputs. **When** the affected operation runs. **Then** it meets the candidate-specific checks in VER-KIS-001.

### Failure

**Given** the actual failure described above. **When** the affected operation runs. **Then** it reports that failure without claiming a pass.
