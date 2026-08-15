+++
id = "RLS-SEH-005"
type = "release_record"
title = "Release candidate 0.3.0"
status = "released"
owners = ["release-owner"]
created = "2026-08-15"
updated = "2026-08-15"
version = "0.3.0"
commit = "dd06660a94f06d934adb1df0352b81e709f2ffd3"
git_object_format = "sha1"
released_at = "2026-08-15T10:31:32Z"
authorized_by = "release-owner"
tag = "v0.3.0"

[relations]
satisfies = ["REL-SEH-004"]
includes_verification = ["VREC-SEH-005"]
releases_work = ["WO-DOC-007", "WO-DOC-008", "WO-DOC-009", "WO-DOC-010", "WO-DOC-011", "WO-DST-007", "WO-DST-009", "WO-RLS-005", "WO-SHB-002"]
+++

# Release Record Candidate

This released record authorizes release `0.3.0` for `WO-DOC-007`, `WO-DOC-008`, `WO-DOC-009`, `WO-DOC-010`, `WO-DOC-011`, `WO-DST-007`, `WO-DST-009`, `WO-RLS-005`, `WO-SHB-002` from candidate commit `dd06660a94f06d934adb1df0352b81e709f2ffd3`. The preparation command originally created a `ready` proposal and did not approve, commit, tag, release, or publish anything.

The release candidate commit may precede the governance commit retaining this record. Any release tag must be created and checked by the authorized release process.

On 2026-08-15, after reviewing the verified aggregate record and exact-candidate qualification, the accountable release owner explicitly instructed `ok, now transition the release record to released then commit, push an PR`. That human decision transitioned this record from `ready` to `released`; automation did not grant the authority. The same instruction authorizes retaining this transition in a governance commit and sending the branch for pull-request review. It does not itself create `v0.3.0`, a GitHub Release, a PyPI file, a deployment, a merge, or a governor promotion.
