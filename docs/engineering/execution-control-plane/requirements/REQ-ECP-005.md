+++
id = "REQ-ECP-005"
type = "requirement"
title = "The pull-request body is generated"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-27"
updated = "2026-08-28"
statement = "WHEN an actor runs `harnessctl pr-body` for a work order, THE SYSTEM SHALL emit an LF-terminated pull-request body carrying the standalone `Harness-Work-Order:` line and, when a handoff result exists, the `Harness-Restitution:` line."
verification_method = ["test"]
priority = "must"
source = "REQ-ADS-004; W-ADS-001"

[relations]
derives_from = ["CAP-ECP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T12:03:40Z"
decided_by = "requirements-steward"
reason = "Approved on 2026-08-28 by the accountable owner, 'I approve the ECP definitions and WO-ECP-005', as part of the execution-control-plane definition packet of #231 with the issue #212 amendments of #238 applied. Approval of a definition authorizes no work; each work order is approved separately."
+++

# Requirement: The pull-request body is generated

## Rationale

The pull-request body is the transport CI reads to select the work order and
recompute the restitution digest, and it is typed by the agent. A carriage
return inside the trailer line breaks selection while the local round trip hides
it; `REQ-ADS-004` exists because that recurred, and `W-ADS-001` reports the byte
offset after the fact (docs/engineering/agent-directive-
surface/requirements/REQ-ADS-004.md:9, :34-37). Commit and trailer discipline is
still left to inference (docs/notes/agentic-execution-review-2026-08.md:286).
Generating the body removes the defect instead of diagnosing it.

## Behavior

- Trigger: `harnessctl pr-body REPO --artifact WO` runs, optionally with
  `--handoff-result FILE`.
- Response: standard output, or the `--output` file, is a body whose every line
  ends in `\n` alone, containing a standalone line `Harness-Work-Order: WO`
  and, when a handoff result is supplied or found for the work order, a
  standalone line `Harness-Restitution: RESULT_SHA256` equal to the digest in
  that result.
- On failure: when the work order does not exist, or the supplied handoff result
  is not a schema-2 result for that work order, nothing is emitted and the
  command fails closed with a coded predicate.

## Assumptions and dependencies

- `select-work-order` keeps parsing the `Harness-Work-Order:` and
  `Harness-Restitution:` lines in their current shape.
- The pull-request template seed under `templates/repository/standard/.github/`
  is the body's prose frame.
- `--output` writes with `newline="\n"` regardless of platform.

## Acceptance examples

Executable scenarios live in `acceptance/REQ-ECP-005.feature` and are named by
the verification contract that covers this requirement.

### Example: normal behavior

**Given** `WO-X-004` has a handoff result whose `result_sha256` is `ab12…`.

**When** `harnessctl pr-body . --artifact WO-X-004 --output body.md` runs on
Windows.

**Then** `body.md` contains no `\r`, one line `Harness-Work-Order: WO-X-004`,
and one line `Harness-Restitution: ab12…`, and `select-work-order --pull-
request-body body.md` selects `WO-X-004`.

### Example: failure behavior

**Given** `--handoff-result` names a file that is a schema-1 result.

**When** the command runs.

**Then** no body is emitted, and the result names the schema mismatch as the
failed predicate.

## Open decisions

None.
