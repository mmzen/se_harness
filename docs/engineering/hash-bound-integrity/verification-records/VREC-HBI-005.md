+++
id = "VREC-HBI-005"
type = "verification_record"
title = "Verification candidate for WO-HBI-005"
status = "verified"
owners = ["quality-owner"]
created = "2026-08-28"
updated = "2026-08-28"
commit = "fb401a3271ecc6031fdb679f35706c7f9d2f6a9c"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-28T10:56:47Z"
prepared_by = "quality-owner"
artifact_snapshot_sha256 = "f8297b4961565e31062a6a5978060f4d3a8067c2fcd90fb2b2a65f7be75dceae"
evidence_paths = ["docs/engineering/hash-bound-integrity/evidence/WO-HBI-005-verification.md"]
evaluator_evidence_path = "docs/engineering/hash-bound-integrity/evidence/VREC-HBI-005-evaluator.json"
evaluator_evidence_sha256 = "1e713a859270491fe587d79b3b499a1a077d1c7dc9e588260ef8adc5b429f5cf"

verified_at = "2026-08-28T11:42:55Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-HBI-005"]
conforms_to = ["VER-HBI-001"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-08-28T11:42:55Z"
decided_by = "assurance-owner"
reason = "Verified on 2026-08-28 by the accountable assurance owner, 'I verify VREC-HBI-005'. Re-measured immediately before this transition: candidate commit fb401a3271ecc6031fdb679f35706c7f9d2f6a9c is an ancestor of the branch tip with a clean worktree; the evidence blob is byte-identical at the candidate and the tip; the evaluator packet matches its recorded raw digest; all thirteen hosted checks pass at 7e317e5 including the Windows legs; the graph reads 1057 artifacts and 0 errors under the released 0.7.1 evaluator; a fresh consumer's doctor exits 0 on both checkout configurations. Acceptance covers the evidence as recorded with its six disclosures, including the scope amendment for the lifecycle test and the absence of local Windows readings. It authorizes no merge, release, publication or deployment."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-HBI-005` to candidate commit `fb401a3271ecc6031fdb679f35706c7f9d2f6a9c`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
