+++
id = "REQ-KIS-001"
type = "requirement"
title = "Remove everyday input and writing blockers"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-13"
updated = "2026-09-13"

statement = "THE HARNESS SHALL accept ordinary equivalent input and concise engineering descriptions without rejecting them for writing style."
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
reason = "The owner accepted all 38 candidates in the retained 2026-09-13 codebase KISS review and requested the work orders: \"OK ! Let's create the work orders to implement all candidates\". Record the requirements-steward approval of REQ-KIS-001 within that accepted scope and the established delegated route. SPEC-KIS-001 makes the replacement contracts and seven retained protections explicit; the coverage map assigns all candidates. This records definition approval or bounded execution delegation only, not implementation start, completion, verification, release, merge, publication, live adoption or historical evidence deletion."
+++

# Remove everyday input and writing blockers

## In plain words

Normal Windows text, literal paths, clear notes and short risk descriptions work without special formatting.

## Why

The user should fix an actual ambiguity, not reformat harmless text to satisfy the checker.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| The owner uses the affected operation. | Normal Windows text, literal paths, clear notes and short risk descriptions work without special formatting. | An outside-project path or an ambiguous work-order identifier is still rejected. |

## Examples

### Normal

**Given** an approved task with the required inputs. **When** the affected operation runs. **Then** it meets the candidate-specific checks in VER-KIS-001.

### Failure

**Given** the actual failure described above. **When** the affected operation runs. **Then** it reports that failure without claiming a pass.
