+++
id = "RLS-SEH-003"
type = "release_record"
title = "Release candidate 0.2.2"
status = "released"
owners = ["release-owner"]
created = "2026-08-12"
updated = "2026-08-12"
version = "0.2.2"
commit = "9ba0cec3710167ad4568931747ed5f4e48a63532"
git_object_format = "sha1"
released_at = "2026-08-12T17:00:26Z"
authorized_by = "release-owner"
tag = "v0.2.2"

[relations]
satisfies = ["REL-SEH-003"]
includes_verification = ["VREC-SEH-003"]
releases_work = ["WO-IAR-002", "WO-IAR-003", "WO-IAR-004", "WO-IAR-005", "WO-RLS-004"]
+++

# Release Record Candidate

This released record binds release `0.2.2` for `WO-IAR-002`, `WO-IAR-003`, `WO-IAR-004`, `WO-IAR-005`, `WO-RLS-004` to candidate commit `9ba0cec3710167ad4568931747ed5f4e48a63532`. The preparation command originally created a `ready` record and did not approve, commit, tag, release, or publish anything.

The release candidate commit may precede the governance commit retaining this record. Any release tag must be created and checked by the authorized release process.

On 2026-08-12, after `VREC-SEH-003` was verified, the accountable release owner explicitly instructed `i approve the release`. Exact-candidate artifact qualification was then repeated and retained in `docs/engineering/release-0.2.2/evidence/RLS-SEH-003-release.md`. That human decision transitioned this record from `ready` to `released`; no tag, GitHub release, PyPI publication, or deployment was performed.
