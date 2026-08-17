+++
id = "RLS-SEH-007"
type = "release_record"
title = "Release candidate 0.4.1"
status = "released"
owners = ["release-owner"]
created = "2026-08-17"
updated = "2026-08-17"
version = "0.4.1"
commit = "7fbbe5634e08edc2cf93f22dd7278e986407ec6e"
git_object_format = "sha1"
released_at = "2026-08-17T19:06:20Z"
authorized_by = "release-owner"
tag = "v0.4.1"

[relations]
satisfies = ["REL-SEH-006"]
includes_verification = ["VREC-SEH-007"]
releases_work = ["WO-DPG-001", "WO-DST-011", "WO-DST-012", "WO-DST-013", "WO-DST-014", "WO-DST-015", "WO-DST-016", "WO-RLS-007"]
+++

# Release Record Candidate

On 2026-08-17, after `RLS-SEH-007` was prepared in `ready` state with the exact version, candidate, verification record, release contract, tag, and eight-work-order scope shown above, the accountable release owner explicitly stated `I approve RLS-SEH-007 transitioning to released.` That human decision transitions this record from `ready` to `released`; automation did not grant release authority. All captured release fields and relations remain unchanged.

This record was prepared to release `0.4.1` for `WO-DPG-001`, `WO-DST-011`, `WO-DST-012`, `WO-DST-013`, `WO-DST-014`, `WO-DST-015`, `WO-DST-016`, and `WO-RLS-007` from candidate commit `7fbbe5634e08edc2cf93f22dd7278e986407ec6e`. The preparation command did not approve, commit, tag, release, or publish anything; the separate accountable decision above supplies the release authority.

The release candidate commit may precede the governance commit retaining this record. The separately authorized `v0.4.1` tag must be created only after this governance decision is merged, must resolve exactly to the candidate commit above, and must not be moved or replaced. This decision does not itself commit, push, merge, tag, create GitHub Release assets, publish to PyPI, deploy Pages, promote the governor, force-push, or rewrite history.
