+++
id = "VREC-ECP-005"
type = "verification_record"
title = "Verification candidate for WO-ECP-005"
status = "verified"
owners = ["quality-owner"]
created = "2026-08-28"
updated = "2026-08-28"
commit = "32652b4dfe34ce6c2c919db998253b2f0529a963"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-28T12:32:06Z"
prepared_by = "quality-owner"
artifact_snapshot_sha256 = "aba2a9aeed3421a25513bb67491fe8ca771e39a781b37e734024c9d7133c6b60"
evidence_paths = ["docs/engineering/execution-control-plane/evidence/WO-ECP-005/WO-ECP-005-verification.md"]
evaluator_evidence_path = "docs/engineering/execution-control-plane/evidence/VREC-ECP-005-evaluator.json"
evaluator_evidence_sha256 = "1e713a859270491fe587d79b3b499a1a077d1c7dc9e588260ef8adc5b429f5cf"

verified_at = "2026-08-28T12:37:45Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-ECP-005"]
conforms_to = ["VER-ECP-005"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-08-28T12:37:45Z"
decided_by = "assurance-owner"
reason = "Verified on 2026-08-28 by the accountable assurance owner, 'I verify VREC-ECP-005'. Re-measured immediately before this transition: candidate commit 32652b4dfe34ce6c2c919db998253b2f0529a963 is an ancestor of the branch tip with a clean worktree; the evidence blob is byte-identical at the candidate and the tip; the evaluator packet matches its recorded raw digest; all thirteen hosted checks pass at f054a66 including the Windows legs; the graph reads 1059 artifacts and 0 errors under the released 0.7.1 evaluator; the released evaluator's golden focus digest is reproduced by the candidate. Acceptance covers the evidence as recorded with its six disclosures, including the deferral of ECP-KRN-008's per-predicate refusal labels to WO-ECP-009. It authorizes no merge, release, publication or deployment."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-ECP-005` to candidate commit `32652b4dfe34ce6c2c919db998253b2f0529a963`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
