+++
id = "REQ-KIS-002"
type = "requirement"
title = "Let local work progress on its own evidence"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-13"
updated = "2026-09-13"

statement = "THE HARNESS SHALL evaluate authorized local work using its selected scope, committed candidate and relevant evidence without requiring a live CI response."
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
reason = "The owner accepted all 38 candidates in the retained 2026-09-13 codebase KISS review and requested the work orders: \"OK ! Let's create the work orders to implement all candidates\". Record the requirements-steward approval of REQ-KIS-002 within that accepted scope and the established delegated route. SPEC-KIS-001 makes the replacement contracts and seven retained protections explicit; the coverage map assigns all candidates. This records definition approval or bounded execution delegation only, not implementation start, completion, verification, release, merge, publication, live adoption or historical evidence deletion."
+++

# Let local work progress on its own evidence

## In plain words

An approved local task can progress offline; unrelated work and dashboard generation do not block it.

## Why

GitHub outages and unrelated edits should not become local permission failures.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| The owner uses the affected operation. | An approved local task can progress offline; unrelated work and dashboard generation do not block it. | Missing owner approval, a changed governing input, or a real scope escape still blocks the affected action. |

## Examples

### Normal

**Given** an approved task with the required inputs. **When** the affected operation runs. **Then** it meets the candidate-specific checks in VER-KIS-001.

### Failure

**Given** the actual failure described above. **When** the affected operation runs. **Then** it reports that failure without claiming a pass.
