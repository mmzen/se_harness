+++
id = "REQ-ECP-023"
type = "requirement"
title = "The change set admits the selected work order's own records by construction"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-29"
updated = "2026-08-29"
statement = "WHEN a scope or handoff check evaluates a change set for a selected work order, THE SYSTEM SHALL admit the verification and release records that name that work order, and their evaluator-evidence files, as it admits the work order's own file, so that a pull request carrying its own records passes the scope gate without listing a records directory."
verification_method = ["test"]
priority = "must"
source = "issue #264; pull requests #262 and #263, 2026-08-29"

[relations]
derives_from = ["CAP-ECP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T11:40:51Z"
decided_by = "requirements-steward"
reason = "Approved by the requirements steward on 2026-08-29 with the words 'Approve and start WO-ECP-016': the change set admits the selected work order's own verification and release records by construction (issue #264)."
+++

# Requirement: The change set admits the selected work order's own records by construction

## Rationale

`ECP-CHG-007` admits the selected work order's own artifact file, and
`ECP-PRB-002` its evidence directory, because the harness writes them and
they are in every Git diff. The verification record that verifies the work
order, and the release record that releases it, are written the same way —
`capture-verification` and `prepare-release` derive their paths from the
work order's own identity — and this repository lands them on the same
branch. Yet they are judged against the declared scope: on pull request
#263 the managed lane passed at the `implemented` head and failed at the two
record heads with "the pull request's diff leaves the work order's declared
scope", naming `VREC-ECP-018.md`; #262 stayed green only because its scope
listed the whole domain directory. A scope that must list a records
directory to keep the gate honest is a scope that says less than it means.

## Behavior

- Trigger: `check --checkpoint scope` or `--checkpoint handoff` evaluates a
  change set for a selected work order.
- Response: a verification record whose `verifies_work_order` names the
  selected work order, a release record whose `releases_work` names it, and
  each such record's `evaluator_evidence_path` are admitted to the scope by
  construction, at their catalog paths; `QGP-G4I-PATHS` passes on a diff
  that carries them; `scope.declared_paths` continues to carry only what the
  work order declares.
- On failure: a record that names a different work order, or any other file
  under a `verification-records/` or `releases/` directory, is judged
  against the declared scope as today.

## Assumptions and dependencies

- The catalog exposes each record's relations and its
  `evaluator_evidence_path`; a record absent from the catalog (an invalid
  file) admits nothing.
- A release record's bundle manifest keeps its own path under the release
  work order's declared scope, as the release work orders declare it.

## Acceptance examples

### Example: normal behavior

**Given** an `implemented` work order whose scope lists `src/` only, and a
ready verification record for it under `verification-records/` with its
evaluator-evidence file under `evidence/`.

**When** `check --checkpoint scope --from-git BASE` runs over a diff that
adds both files.

**Then** the check completes and `QGP-G4I-PATHS` passes.

### Example: failure behavior

**Given** the same work order and a ready verification record for another
work order added in the same diff.

**When** the same check runs.

**Then** `QGP-G4I-PATHS` fails naming that record with `WEX201`.

## Open decisions

None.
