+++
id = "REQ-KIS-004"
type = "requirement"
title = "Simplify verification and release records"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-13"
updated = "2026-09-13"

statement = "THE HARNESS SHALL bind assurance to the final tested candidate while retaining earlier work evidence without artificial commit or prose equality requirements."
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
reason = "The owner accepted all 38 candidates in the retained 2026-09-13 codebase KISS review and requested the work orders: \"OK ! Let's create the work orders to implement all candidates\". Record the requirements-steward approval of REQ-KIS-004 within that accepted scope and the established delegated route. SPEC-KIS-001 makes the replacement contracts and seven retained protections explicit; the coverage map assigns all candidates. This records definition approval or bounded execution delegation only, not implementation start, completion, verification, release, merge, publication, live adoption or historical evidence deletion."
+++

# Simplify verification and release records

## In plain words

One final candidate verification can use earlier work evidence; a harmless rebase and wording edit need no repeated proof.

## Why

A release needs evidence for its final contents, not identical commit numbers on every earlier work record.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| The owner uses the affected operation. | One final candidate verification can use earlier work evidence; a harmless rebase and wording edit need no repeated proof. | Changed relevant contents need fresh tests; unverified release contents and changed historical facts remain invalid. |

## Examples

### Normal

**Given** an approved task with the required inputs. **When** the affected operation runs. **Then** it meets the candidate-specific checks in VER-KIS-001.

### Failure

**Given** the actual failure described above. **When** the affected operation runs. **Then** it reports that failure without claiming a pass.
