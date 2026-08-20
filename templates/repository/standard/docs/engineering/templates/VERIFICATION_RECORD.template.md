+++
id = "VREC-000"
type = "verification_record"
title = "Verification candidate for aggregate work"
status = "ready"
owners = ["quality-owner"]
created = "YYYY-MM-DD"
updated = "YYYY-MM-DD"
commit = "0000000000000000000000000000000000000000"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "YYYY-MM-DDTHH:MM:SSZ"
prepared_by = "quality-owner"
artifact_snapshot_sha256 = "0000000000000000000000000000000000000000000000000000000000000000"
evidence_paths = ["docs/engineering/DOMAIN/evidence/WO-001-verification.md", "docs/engineering/DOMAIN/evidence/WO-002-verification.md"]
# Verification decision fields; omit while status is ready:
# verified_at = "YYYY-MM-DDTHH:MM:SSZ"
# verified_by = "quality-owner"
# Supersession-only fields; omit unless an accountable owner retires a ready record:
# superseded_at = "YYYY-MM-DDTHH:MM:SSZ"
# supersession_authorized_by = "quality-owner"

[relations]
verifies_work_order = ["WO-001", "WO-002"]
conforms_to = ["VER-001", "VER-002"]
# Supersession-only relation; exactly one verified or released coverage-preserving successor:
# superseded_by = ["VREC-001"]
+++

# Verification Record Candidate

Identify the exact clean final candidate commit and retained evidence for every listed work order. The verification-contract set must equal the union declared by those work orders. A single work order remains valid. Keep status `ready` until the accountable assurance owner verifies the evidence. Preparation metadata records who assembled the candidate, not an assurance decision. Commit this governance record after the candidate commit it names.

If a later verified or released VREC fully covers this record's work, a separate accountable governance decision may change only a `ready` record to `superseded`, add the structured fields and one typed successor relation shown above, and retain a decision note. Preserve the original commit, object format, worktree state, capture timestamp, snapshot hash, evidence paths, work orders, and verification contracts. Superseded records remain historical and are not release-eligible.
