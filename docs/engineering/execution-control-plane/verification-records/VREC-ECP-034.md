+++
id = "VREC-ECP-034"
type = "verification_record"
title = "Verification candidate for WO-ECP-028"
status = "verified"
owners = ["assurance-owner"]
created = "2026-09-07"
updated = "2026-09-07"
commit = "8d73205ae408fb271aedffbf4c926da74879d477"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-09-07T21:55:38Z"
prepared_by = "assurance-owner"
artifact_snapshot_sha256 = "b63d7a2d54fe8c51bee719d872d2c005fb84bd10541a5c6ff7d117d6e6cdd360"
evidence_paths = ["docs/engineering/execution-control-plane/evidence/WO-ECP-028/WO-ECP-028-handoff.md", "docs/engineering/execution-control-plane/evidence/WO-ECP-028/handoff.json"]
evaluator_evidence_path = "docs/engineering/execution-control-plane/evidence/VREC-ECP-034-evaluator.json"
evaluator_evidence_sha256 = "e2cd0929fd42d0634d3bf23a73408665bac8ae473b98c81439dbffb828bff951"

verified_at = "2026-09-07T22:00:23Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-ECP-028"]
conforms_to = ["VER-ECP-024"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-09-07T22:00:23Z"
decided_by = "assurance-owner"
reason = "Verified on 2026-09-07 by the accountable assurance owner with the words 'i verify both' (DR-VREC-DECIDE, together with VREC-ECP-033), after the record was presented: bound to candidate commit 8d73205 (WO-ECP-028 implemented), to the retained evidence WO-ECP-028-handoff.md and handoff.json, and to the exact 0.16.0 evaluator evidence. Hosted lanes on PR #393 at the record commit b602eb1: every lane that had finished passes, including the candidate-package lane; the Windows migration lane was running at the decision. The merge of PR #393 remains the owner's decision; main is merged into the branch first once PR #392 lands, since both touch cli.py and the domain index."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-ECP-028` to candidate commit `8d73205ae408fb271aedffbf4c926da74879d477`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
