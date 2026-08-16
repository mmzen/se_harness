+++
id = "RLS-SEH-006"
type = "release_record"
title = "Release candidate 0.4.0"
status = "released"
owners = ["release-owner"]
created = "2026-08-16"
updated = "2026-08-16"
version = "0.4.0"
commit = "2acc63af8933ee1dfa5ef78b67e2dbe6fb9a4e61"
git_object_format = "sha1"
released_at = "2026-08-16T10:57:17Z"
authorized_by = "release-owner"
tag = "v0.4.0"

[relations]
satisfies = ["REL-SEH-005"]
includes_verification = ["VREC-SEH-006"]
releases_work = ["WO-DOC-012", "WO-IAR-006", "WO-IAR-007", "WO-IAR-008", "WO-IAR-009", "WO-IAR-010", "WO-OCA-001", "WO-OCA-002", "WO-RLS-006", "WO-WAC-001"]
+++

# Release Record Candidate

This released record authorizes release `0.4.0` for `WO-DOC-012`, `WO-IAR-006`, `WO-IAR-007`, `WO-IAR-008`, `WO-IAR-009`, `WO-IAR-010`, `WO-OCA-001`, `WO-OCA-002`, `WO-RLS-006`, `WO-WAC-001` from candidate commit `2acc63af8933ee1dfa5ef78b67e2dbe6fb9a4e61`. The preparation command originally created a `ready` proposal and did not approve, commit, tag, release, or publish anything.

The release candidate commit may precede the governance commit retaining this record. Any release tag must be created and checked by the authorized release process.

On 2026-08-16, after the exact ready proposal was retained in governance commit `2432c0b01165f34e679edde0c39ee48b81e69ffe` and pull request #60 run `31943073763` passed the released-governor, candidate-source, and candidate-package planes, the accountable release owner explicitly instructed `I approve RLS-SEH-006 transitioning to released.` That human decision transitions this record from `ready` to `released`; automation did not grant the authority. The candidate commit, object format, release timestamp, authorized owner, version, tag, release contract, included verification record, and work-order scope remain unchanged. This decision does not itself create `v0.4.0`, merge the pull request, publish a GitHub Release or PyPI package, deploy, promote the governor, force-push, or rewrite history.
