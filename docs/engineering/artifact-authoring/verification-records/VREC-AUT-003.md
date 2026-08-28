+++
id = "VREC-AUT-003"
type = "verification_record"
title = "Verification candidate for WO-AUT-003"
status = "verified"
owners = ["quality-owner"]
created = "2026-08-28"
updated = "2026-08-28"
commit = "7a2a3649da276d0f31d11997a361232b8c16fa29"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-28T10:42:58Z"
prepared_by = "quality-owner"
artifact_snapshot_sha256 = "1d05d6b950fe2c54e75b067cb044c47b2b669b974b55d0ecc38d8b9145ff006b"
evidence_paths = ["docs/engineering/artifact-authoring/evidence/WO-AUT-003-verification.md"]
evaluator_evidence_path = "docs/engineering/artifact-authoring/evidence/VREC-AUT-003-evaluator.json"
evaluator_evidence_sha256 = "1e713a859270491fe587d79b3b499a1a077d1c7dc9e588260ef8adc5b429f5cf"

verified_at = "2026-08-28T10:47:55Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-AUT-003"]
conforms_to = ["VER-AUT-001"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-08-28T10:47:55Z"
decided_by = "assurance-owner"
reason = "Verified on 2026-08-28 by the accountable assurance owner, 'I verify VREC-AUT-003'. Re-measured immediately before this transition: candidate commit 7a2a3649da276d0f31d11997a361232b8c16fa29 is an ancestor of the branch tip with a clean worktree; the evidence blob at the candidate is byte-identical to the tip; the evaluator packet matches its recorded raw digest; all thirteen hosted checks pass at 8d67924 including the Windows legs; the graph reads 1053 artifacts and 0 errors under the released 0.7.1 evaluator. Acceptance covers the evidence as recorded with its two disclosures. It authorizes no merge, release, publication or deployment."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-AUT-003` to candidate commit `7a2a3649da276d0f31d11997a361232b8c16fa29`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
