+++
id = "VREC-DST-006"
type = "verification_record"
title = "Verification candidate for WO-DOC-009"
status = "superseded"
owners = ["quality-owner"]
created = "2026-08-13"
updated = "2026-08-16"
commit = "1e3790f746e0a8fa75a00ab6b0db371a39a63675"
git_object_format = "sha1"
worktree_state = "clean"
verified_at = "2026-08-13T08:18:03Z"
artifact_snapshot_sha256 = "4a85706cbdf3d57f0d1556d55a1b5bb3b6f09a5eb9a85c62a32ce2ef961906cd"
evidence_paths = ["docs/engineering/harness-distribution/evidence/WO-DOC-009-verification.md"]
superseded_at = "2026-08-16T06:27:28Z"
supersession_authorized_by = "repository-owner"

[relations]
verifies_work_order = ["WO-DOC-009"]
conforms_to = ["VER-DST-006"]
superseded_by = ["VREC-SEH-005"]
+++

# Superseded Verification Record

This historical record remains bound to candidate commit `1e3790f746e0a8fa75a00ab6b0db371a39a63675` and its retained evidence for `WO-DOC-009`. Verified aggregate `VREC-SEH-005` covers that work on the later release candidate. On 2026-08-16, the accountable repository owner explicitly instructed that `VREC-DST-006` be superseded by `VREC-SEH-005`; `WO-VSP-003` records the bounded governance decision, and automation only validates and presents it.

The record is retained rather than deleted or falsely verified. Its candidate, object format, clean-worktree state, capture timestamp, artifact snapshot, evidence path, original work-order relation, and original verification-contract relation remain unchanged. `superseded_by` identifies the single authoritative successor; this record is terminal and no longer contributes active verification or release readiness.
