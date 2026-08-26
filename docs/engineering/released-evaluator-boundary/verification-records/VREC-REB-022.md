+++
id = "VREC-REB-022"
type = "verification_record"
title = "Verification candidate for WO-REB-025"
status = "ready"
owners = ["quality-owner"]
created = "2026-08-26"
updated = "2026-08-26"
commit = "01ba6b32aac9a858180e4017203db887e8aac4b3"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-26T22:28:35Z"
prepared_by = "quality-owner"
artifact_snapshot_sha256 = "dffd139e4c88040f814f7cb060a24e8c0977cac8e7fc71c4686ecd6de05b3055"
evidence_paths = ["docs/engineering/released-evaluator-boundary/evidence/WO-REB-025-verification.md"]
evaluator_evidence_path = "docs/engineering/released-evaluator-boundary/evidence/VREC-REB-022-evaluator.json"
evaluator_evidence_sha256 = "fcfc14471cc373fce07ece222f6c03b2152dad2cf4cd5ae6e04cf147c4171962"

[relations]
verifies_work_order = ["WO-REB-025"]
conforms_to = ["VER-REB-006"]
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-REB-025` to candidate commit `01ba6b32aac9a858180e4017203db887e8aac4b3`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.

## Scope

`WO-REB-025` at the bound commit `01ba6b32aac9a858180e4017203db887e8aac4b3`:
the resolve job of `.github/workflows/publish-pypi.yml` and the build job of
`.github/workflows/pages-publication.yml` exercise `qualify predecessor-view`
only when the named record's contract declares a `[bootstrap]` table, as
`REQ-REB-015`'s condition requires, and otherwise retain an `excluded`
observation at the same path naming the resolved evaluator; the packet index
line; the keyed evidence. No `se_harness/`, `tests/`, `repository_tools/` or
`templates/` byte, so `REL-SEH-017`'s allow-list and the released
`RLS-SEH-015` are untouched.

## Readings at the bound commit

Governing exact public 0.6.0 evaluator outside the checkout, isolated:
`validate` PASS, 958 artifacts, 0 errors; `doctor` 87 PASS, 0 FAIL; review
preflight PASS; handoff check Completed at formal snapshot `c394d159…` on
both evaluators. Candidate: both workflows parse under PyYAML with their
pinned string counts unchanged; both patched `run` blocks, extracted from the
YAML and executed with `bash` against the real catalog, take the `absent`
branch for `RLS-SEH-015` (writing the excluded observation) and the
`declared` branch for `RLS-SEH-012`; the three workflow suites OK; full suite
`Ran 995 tests … OK (skipped=24)` on Windows CPython 3.14 at full scale.

The hosted lanes on pull request #186 are recorded, with their run identifiers, in the hosted row of `WO-REB-025`'s evidence.

## Disclosed limitations

Two deviations accepted by the owner on 2026-08-27: no new fixture test (a
case for the exclusion branch follows after 0.7.0), and `SPEC-RLO-005` rule
37's `release-record` clause left to a later amendment. The decisive reading
of this change — the re-dispatched last mile for `RLS-SEH-015` — is the
release owner's separate act after merge and is not evidence bound here.

## What this record does not do

It is `ready`. It verifies nothing until the assurance owner's decision and
authorizes no merge, dispatch, tag, publication or deployment.
