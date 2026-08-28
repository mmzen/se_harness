+++
id = "VREC-ECP-010"
type = "verification_record"
title = "Verification candidate for WO-ECP-010"
status = "verified"
owners = ["quality-owner"]
created = "2026-08-28"
updated = "2026-08-28"
commit = "f9ca5d86e97e718cc9777b176a0a8629f89e487f"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-28T14:00:36Z"
prepared_by = "quality-owner"
artifact_snapshot_sha256 = "9d4603c20b463311d73cd2704f143767e37c1f63670bb90d0b95d6f3b30120ec"
evidence_paths = ["docs/engineering/execution-control-plane/evidence/WO-ECP-010/WO-ECP-010-verification.md"]
evaluator_evidence_path = "docs/engineering/execution-control-plane/evidence/VREC-ECP-010-evaluator.json"
evaluator_evidence_sha256 = "1e713a859270491fe587d79b3b499a1a077d1c7dc9e588260ef8adc5b429f5cf"

verified_at = "2026-08-28T14:04:42Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-ECP-010"]
conforms_to = ["VER-ECP-007"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-08-28T14:04:42Z"
decided_by = "assurance-owner"
reason = "Verified on 2026-08-28 by the accountable assurance owner, 'Verify it', on the record as prepared. Re-measured immediately before this transition: candidate commit f9ca5d86e97e718cc9777b176a0a8629f89e487f is an ancestor of the branch tip with a clean worktree; the evidence blob is byte-identical at the candidate and the tip; the evaluator packet matches its recorded raw digest; all thirteen hosted checks pass at eb53ff5 including the real upgrade rehearsal on Linux and on Windows with agreeing lock digests; the graph reads 1062 artifacts and 0 errors under the released 0.7.1 evaluator. Acceptance covers the evidence as recorded with its nine disclosures, including the owner's amendment that the stage-machine files stay tracked and dead until the root advances past 0.7.1, the retained interpreter-safety module under ARCH-REB-010, and the two intermediate red pushes before eb53ff5. It authorizes no merge, release, publication or deployment."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-ECP-010` to candidate commit `f9ca5d86e97e718cc9777b176a0a8629f89e487f`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
