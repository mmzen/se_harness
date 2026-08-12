+++
id = "RLS-SEH-004"
type = "release_record"
title = "Release candidate 0.2.2"
status = "released"
owners = ["release-owner"]
created = "2026-08-12"
updated = "2026-08-12"
version = "0.2.2"
commit = "8ffb5e9386c3dc75b637092f93d372936ae7a290"
git_object_format = "sha1"
released_at = "2026-08-12T18:47:10Z"
authorized_by = "release-owner"
tag = "v0.2.2"

[relations]
satisfies = ["REL-SHB-001"]
includes_verification = ["VREC-SEH-004"]
releases_work = ["WO-IAR-002", "WO-IAR-003", "WO-IAR-004", "WO-IAR-005", "WO-RLS-004", "WO-SHB-001"]
+++

# Release Record Candidate

This released record authorizes release `0.2.2` for `WO-IAR-002`, `WO-IAR-003`, `WO-IAR-004`, `WO-IAR-005`, `WO-RLS-004`, `WO-SHB-001` from candidate commit `8ffb5e9386c3dc75b637092f93d372936ae7a290`. The preparation command originally created a `ready` record and did not approve, commit, tag, release, or publish anything.

The release candidate commit may precede the governance commit retaining this record. Any release tag must be created and checked by the authorized release process.

On 2026-08-12, after reviewing the verified aggregate record and the green released-governor, candidate-source, and candidate-package checks, the accountable release owner explicitly instructed `approved`. That human decision transitioned this record from `ready` to `released`; automation did not grant the authority. This governance transition does not itself create `v0.2.2`, a GitHub Release, a PyPI file, a deployment, a merge, or a governor promotion.
