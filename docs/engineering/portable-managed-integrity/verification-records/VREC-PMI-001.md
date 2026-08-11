+++
id = "VREC-PMI-001"
type = "verification_record"
title = "Verification candidate for 2 work orders"
status = "verified"
owners = ["quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
commit = "505e889777c3c50f544b7e6d6fe58e2f765c1fea"
git_object_format = "sha1"
worktree_state = "clean"
verified_at = "2026-08-11T11:24:51Z"
artifact_snapshot_sha256 = "cca3139c2c274683e2a85dcba41eaed793d8810f15c91ac1404cf4c35d97c635"
evidence_paths = ["docs/engineering/aggregate-release/evidence/WO-AGR-001-verification.md", "docs/engineering/portable-managed-integrity/evidence/WO-PMI-001-verification.md"]

[relations]
verifies_work_order = ["WO-AGR-001", "WO-PMI-001"]
conforms_to = ["VER-AGR-001", "VER-PMI-001"]
+++

# Verification Record Candidate

This verified record binds retained evidence for `WO-AGR-001`, `WO-PMI-001` to candidate commit `505e889777c3c50f544b7e6d6fe58e2f765c1fea`. The capture command originally prepared it as `ready` and did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.

The accountable repository owner reviewed both retained evidence files and explicitly instructed `i validate, then transition and governance commit` on 2026-08-11. That human decision, authorized and recorded by `WO-REV-004`, transitioned this record from `ready` to `verified`; automation did not grant the authority.
