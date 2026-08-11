+++
id = "RLS-SEH-001"
type = "release_record"
title = "Release candidate 0.2.0"
status = "released"
owners = ["release-owner"]
created = "2026-08-11"
updated = "2026-08-11"
version = "0.2.0"
commit = "1329c7a4472f323c4b21d869545cad3c647fe568"
git_object_format = "sha1"
released_at = "2026-08-11T13:29:25Z"
authorized_by = "release-owner"
tag = "v0.2.0"

[relations]
satisfies = ["REL-DST-001"]
includes_verification = ["VREC-SEH-001"]
releases_work = ["WO-AGR-001", "WO-DOC-001", "WO-DOC-002", "WO-DST-001", "WO-DST-002", "WO-DST-003", "WO-PMI-001", "WO-REV-001", "WO-RLS-001", "WO-VSP-001"]
+++

# Release Record Candidate

This released record binds release `0.2.0` for `WO-AGR-001`, `WO-DOC-001`, `WO-DOC-002`, `WO-DST-001`, `WO-DST-002`, `WO-DST-003`, `WO-PMI-001`, `WO-REV-001`, `WO-RLS-001`, `WO-VSP-001` to candidate commit `1329c7a4472f323c4b21d869545cad3c647fe568`. The preparation command originally created a `ready` record and did not approve, commit, tag, release, or publish anything.

The release candidate commit precedes the governance commits retaining this record. The immutable release tag must identify that candidate rather than a later governance commit.

The accountable repository and release owner reviewed the verified aggregate candidate and final artifact evidence and explicitly instructed `make the release` on 2026-08-11. That human decision, authorized by `WO-RLS-001` and recorded in `docs/engineering/release-0.2.0/evidence/RLS-SEH-001-release.md`, transitioned this record from `ready` to `released` and authorized immutable tag `v0.2.0` plus GitHub release publication; automation did not grant the authority.
