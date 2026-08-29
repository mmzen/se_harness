+++
id = "REQ-ECP-019"
type = "requirement"
title = "Evaluator-derived artifact paths resolve on every host"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-29"
updated = "2026-08-29"
statement = "WHEN `harnessctl evidence` or `harnessctl check` derives a work order's domain from the artifact path the evaluator itself computed, THE SYSTEM SHALL resolve the same domain and packet path on every host while still refusing a backslash in a path supplied as untrusted text."
verification_method = ["test"]
priority = "must"
source = "issue #254; WO-HUP-009 evidence, measured 2026-08-29 on Windows 11 with released 0.9.0"

[relations]
derives_from = ["CAP-ECP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T07:45:09Z"
decided_by = "requirements-steward"
reason = "Approved on 2026-08-29 by the accountable owner, 'i approve the artifact packet', for the repair of issue #254: render the evaluator's own artifact path as POSIX before the domain resolver's text guard, prove it with PureWindowsPath tests on the Linux lane, and add the plain-English reference for harnessctl check. Measured before this transition over branch state 88d1a1f carrying unmoved main aa99773: validate PASS at 0 errors under the governing 0.9.0 root; start preflight reads only the draft signature. Approval of a definition authorizes no work; the work order is approved separately."
+++

# Requirement: Evaluator-derived artifact paths resolve on every host

## Rationale

Released 0.9.0 refuses `harnessctl evidence` and every `harnessctl check`
that builds a checkpoint context on Windows, for every work order, with
`WEX-ECP-010: <WO> is not under a domain directory` (issue #254).
`artifact_layout.artifact_domain_from_relative_path` returns `None` for any
value whose string form contains a backslash
(`se_harness/artifact_layout.py:147-150`), a sound guard for a path that
arrives as untrusted text; `workflow_compliance.evidence_packet_path` hands
it `artifact.path.relative_to(root)` (`se_harness/workflow_compliance.py:372`),
a `WindowsPath` whose string form uses backslashes on Windows. The value is
the evaluator's own, not input. `WO-HUP-009` had to run its handoff check
from a Linux runtime; ~60 tests of `test_workflow_compliance`,
`test_workflow_execution` and `test_delegated_workflow` fail on a Windows
workstation for the same reason, and the suite runs hosted on Linux only, so
nothing caught it before release.

## Behavior

- Trigger: `harnessctl evidence` or `harnessctl check` runs on a host whose
  native path separator is not `/`.
- Response: the work order's domain resolves from its artifact path exactly as
  on a POSIX host; the packet path is
  `DOMAIN/evidence/WO-ID/WO-ID-CHECKPOINT.md` (`ECP-EVD-001`); the command
  proceeds to its ordinary outcome.
- On failure: a path supplied as text (`--changed-path`, a manifest entry,
  a lock entry) that contains a backslash is still refused as before; the
  guard is not weakened, only the evaluator's own `PurePath` values bypass
  the text guard by being rendered POSIX first.

## Assumptions and dependencies

- The managed template copy of the resolver
  (`templates/repository/standard/scripts/artifact_layout_registry.py`) is
  hash-locked in every installed root and never receives a `PurePath`; it is
  not changed.
- Regression tests use `PureWindowsPath` values, so the defect and the fix are
  observable on the Linux lane where the suite runs.

## Acceptance examples

### Example: normal behavior

**Given** a checkout with an `in_progress` work order under
`docs/engineering/<domain>/work-orders/`, and the released evaluator on
Windows.

**When** `harnessctl evidence . --artifact WO-X --checkpoint handoff` runs.

**Then** the packet is written under `docs/engineering/<domain>/evidence/WO-X/`
and the result is `Completed`.

### Example: failure behavior

**Given** the same checkout.

**When** `harnessctl check . --artifact WO-X --checkpoint handoff
--changed-path "docs\engineering\x.md" --changes-complete` runs.

**Then** the path is refused as a non-normalized path exactly as on a POSIX
host.

## Open decisions

None.
