+++
id = "VREC-REB-027"
type = "verification_record"
title = "Verification candidate for WO-REB-029"
status = "verified"
owners = ["engineering-owner"]
created = "2026-08-28"
updated = "2026-08-28"
commit = "0ee0f7bcb6c637a2fda0186a38859ca7f6b10133"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-28T05:29:09Z"
prepared_by = "engineering-owner"
artifact_snapshot_sha256 = "39e0879b99fb67af42f824a861ad72c6fa3eab267b5b9c342db9d42da82110e1"
evidence_paths = ["docs/engineering/released-evaluator-boundary/evidence/WO-REB-029-verification.md"]
evaluator_evidence_path = "docs/engineering/released-evaluator-boundary/evidence/VREC-REB-027-evaluator.json"
evaluator_evidence_sha256 = "150feaccd4cecd8ce88a42871dbda0de61caaea6ac8e6ca8493966cf2bb987fd"

verified_at = "2026-08-28T15:00:59Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-REB-029"]
conforms_to = ["VER-REB-013"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-08-28T15:00:59Z"
decided_by = "assurance-owner"
reason = "Verified on 2026-08-28 by the accountable assurance owner, 'I verify VREC-REB-026 and VREC-REB-027', as the entry condition of REL-SEH-019. Re-measured immediately before this transition: candidate commit 0ee0f7bcb6c637a2fda0186a38859ca7f6b10133 is an ancestor of main with a clean worktree; every bound evidence blob is byte-identical at the candidate and the tip; the evaluator packet matches its recorded raw digest; the work order's hosted lanes were green at its candidate and the graph reads 0 errors under the released 0.7.1 evaluator. Acceptance covers the evidence as recorded with its disclosures. It authorizes no merge, release, publication or deployment."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-REB-029` to candidate commit `0ee0f7bcb6c637a2fda0186a38859ca7f6b10133`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
