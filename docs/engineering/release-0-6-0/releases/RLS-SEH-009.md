+++
id = "RLS-SEH-009"
type = "release_record"
title = "Release candidate 0.6.0"
status = "rejected"
owners = ["release-owner"]
created = "2026-08-21"
updated = "2026-08-21"
version = "0.6.0"
commit = "b033827cc9f8357a7afb1d82f336c6fe2fc16e26"
git_object_format = "sha1"
released_at = "2026-08-21T17:28:10Z"
authorized_by = "release-owner"
tag = "v0.6.0"
rejected_at = "2026-08-21T21:49:26Z"
rejected_by = "release-owner"
rejection_reason = "Retained CRLF checkout qualification failure invalidates candidate C2 for release."

preparation_schema = "se-harness-predecessor-bootstrap-v1"
evaluator_evidence_path = "docs/engineering/release-0-6-0/evidence/RLS-SEH-009-evaluator.json"
evaluator_evidence_sha256 = "11a4aec338f1da102a112faca6589d18541e115e139e695e8d66e4d509125404"

[relations]
satisfies = ["REL-SEH-008"]
includes_verification = ["VREC-SEH-009"]
releases_work = ["WO-DST-019", "WO-DST-020", "WO-REB-001", "WO-REB-002", "WO-REB-003", "WO-REB-004", "WO-RLS-008", "WO-WEX-001", "WO-WEX-002"]

[[lifecycle_events]]
from = "ready"
to = "rejected"
decided_at = "2026-08-21T21:49:26Z"
decided_by = "release-owner"
reason = "Retained CRLF checkout qualification failure invalidates candidate C2 for release."
+++

# Release Record Candidate

This ready record proposes release `0.6.0` for `WO-DST-019`, `WO-DST-020`, `WO-REB-001`, `WO-REB-002`, `WO-REB-003`, `WO-REB-004`, `WO-RLS-008`, `WO-WEX-001`, `WO-WEX-002` from candidate commit `b033827cc9f8357a7afb1d82f336c6fe2fc16e26`. An accountable release owner must review and transition it to `released`; this command did not approve, commit, tag, release, or publish anything.

The release candidate commit may precede the governance commit retaining this record. Any release tag must be created and checked by the authorized release process.
