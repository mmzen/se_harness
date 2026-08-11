+++
id = "VREC-PYP-002"
type = "verification_record"
title = "Verification candidate for WO-PYP-004"
status = "verified"
owners = ["quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
commit = "ce7243a74bd268dcadfde9b6d42f6818913e1795"
git_object_format = "sha1"
worktree_state = "clean"
verified_at = "2026-08-11T16:59:00Z"
artifact_snapshot_sha256 = "b8029507f7391b729446af533f569f28fa044f28ab5ec43ea1d7b44ce4f01770"
evidence_paths = ["docs/engineering/pypi-publication/evidence/WO-PYP-004-verification.md"]

[relations]
verifies_work_order = ["WO-PYP-004"]
conforms_to = ["VER-PYP-001"]
+++

# Verification Record Candidate

This verified record binds retained evidence for `WO-PYP-004` to candidate commit `ce7243a74bd268dcadfde9b6d42f6818913e1795`. The capture command originally prepared it as `ready` and did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.

The accountable owner authorized completion of the exact PyPI promotion with `i merged, you can perform the next steps`. After the first run exposed the annotated-tag-object defect, that authorization and `WO-PYP-004` bounded the separately verified immutable-commit correction. The ready record was retained in commit `d300ea46d39ac95e76cb32ae419e092c85bfe4cc` with SHA-256 `bd9a472dc65c428f7d4129cc83b7633b0f60cd45d68cae2db4178ded5734a300`; this later governance decision transitioned only its status to `verified`.
