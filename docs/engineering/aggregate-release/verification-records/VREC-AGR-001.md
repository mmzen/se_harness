+++
id = "VREC-AGR-001"
type = "verification_record"
title = "Verification candidate for WO-AGR-001"
status = "superseded"
owners = ["quality-owner"]
created = "2026-08-11"
updated = "2026-08-16"
commit = "3f3ba521d7b19455e1f2eacb9aeea42928806aef"
git_object_format = "sha1"
worktree_state = "clean"
verified_at = "2026-08-11T10:29:11Z"
artifact_snapshot_sha256 = "3be8b892749d72f3099b1a74ffa6527db90f589be57f3fd13652070a8b5c27ad"
evidence_paths = ["docs/engineering/aggregate-release/evidence/WO-AGR-001-verification.md"]
superseded_at = "2026-08-16T06:33:06Z"
supersession_authorized_by = "repository-owner"

[relations]
verifies_work_order = ["WO-AGR-001"]
conforms_to = ["VER-AGR-001"]
superseded_by = ["VREC-PMI-001"]
+++

# Superseded Verification Record

This historical record remains bound to candidate commit `3f3ba521d7b19455e1f2eacb9aeea42928806aef` and its retained evidence for `WO-AGR-001`. Verified corrected candidate `VREC-PMI-001` covers that work plus `WO-PMI-001` on later commit `505e889777c3c50f544b7e6d6fe58e2f765c1fea`. On 2026-08-16, the accountable repository owner explicitly authorized resolution of this stale candidate; `WO-VSP-004` records why the repository-defined direct successor is selected instead of the later release aggregate.

The record is retained rather than deleted or falsely verified. Its candidate, object format, clean-worktree state, capture timestamp, artifact snapshot, evidence path, original work-order relation, and original verification-contract relation remain unchanged. `superseded_by` identifies the single authoritative successor; this record is terminal and no longer contributes active verification or release readiness.
