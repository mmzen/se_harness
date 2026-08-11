+++
id = "RLS-SEH-002"
type = "release_record"
title = "Release candidate 0.2.1"
status = "released"
owners = ["release-owner"]
created = "2026-08-11"
updated = "2026-08-11"
version = "0.2.1"
commit = "94e13e31b81333e1f80f5a7dfd86ed5dbfc1e3e5"
git_object_format = "sha1"
released_at = "2026-08-11T16:45:07Z"
authorized_by = "release-owner"
tag = "v0.2.1"

[relations]
satisfies = ["REL-SEH-002"]
includes_verification = ["VREC-SEH-002"]
releases_work = ["WO-IAR-001", "WO-PYP-001", "WO-RLS-002", "WO-WLC-001"]
+++

# Release Record Candidate

This released record binds release `0.2.1` for `WO-IAR-001`, `WO-PYP-001`, `WO-RLS-002`, `WO-WLC-001` to candidate commit `94e13e31b81333e1f80f5a7dfd86ed5dbfc1e3e5`. The preparation command originally created a `ready` record and did not approve, commit, tag, release, or publish anything.

The release candidate commit precedes the governance commits retaining this record. The immutable release tag must identify that candidate rather than a later governance commit.

After pull request #18 merged the exact candidate and ready aggregate verification, the accountable release owner reviewed the final artifacts and explicitly instructed `i merged, you can perform the next steps` on 2026-08-11. That decision, authorized by `WO-RLS-003` and retained in `docs/engineering/release-0.2.1/evidence/RLS-SEH-002-release.md`, transitioned this record from `ready` to `released` and authorized immutable tag `v0.2.1`, GitHub release publication, and protected exact-asset PyPI promotion; automation did not grant the authority.
