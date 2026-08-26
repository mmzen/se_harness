+++
id = "VREC-RLO-007"
type = "verification_record"
title = "Verification candidate for WO-RLO-007"
status = "verified"
owners = ["engineering-owner"]
created = "2026-08-26"
updated = "2026-08-26"
commit = "91db950bff2f85c4a8de3fcea76c0d338e5cb70e"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-26T17:56:58Z"
prepared_by = "engineering-owner"
artifact_snapshot_sha256 = "3c71dcfbbdebcb427c709bd70e11eee78499a973399dba5cdd76a443d4186f03"
evidence_paths = ["docs/engineering/release-orchestration/evidence/WO-RLO-007/WO-RLO-007-verification.md"]
evaluator_evidence_path = "docs/engineering/release-orchestration/evidence/VREC-RLO-007-evaluator.json"
evaluator_evidence_sha256 = "fcfc14471cc373fce07ece222f6c03b2152dad2cf4cd5ae6e04cf147c4171962"

verified_at = "2026-08-26T17:58:17Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-RLO-007"]
conforms_to = ["VER-RLO-004"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-08-26T17:58:17Z"
decided_by = "assurance-owner"
reason = "Assurance owner accepted the retained evidence on 2026-08-26 with 'I verify VREC-RLO-007', after accepting interactively the five recorded deviations: chown inside the pinned image (1); Windows not measured, the hand-back being a no-op off POSIX (2); release-candidate-replay.yml not re-run for want of a ready record (3); two failed hosted attempts before the successful one, on test coverage and on reading root-owned outputs (4, 5). Hosted reading: run 32995876112 on pull request #174 completed the first recipe replay in the repository's history on a hosted runner, state exact, both builds byte-identical; every check green."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-RLO-007` to candidate commit `91db950bff2f85c4a8de3fcea76c0d338e5cb70e`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
