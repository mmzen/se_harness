+++
id = "VREC-RLO-008"
type = "verification_record"
title = "Verification candidate for WO-RLO-008"
status = "verified"
owners = ["quality-owner"]
created = "2026-08-27"
updated = "2026-08-27"
commit = "0dfdc648521799ba8499687a9611120bcfeb44ac"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-27T17:05:05Z"
prepared_by = "quality-owner"
artifact_snapshot_sha256 = "f67b5cbf990b82d2fd8ecd472163e0459f0bea462c87fb17b770e2381ee5cd1c"
evidence_paths = ["docs/engineering/release-orchestration/evidence/WO-RLO-008/WO-RLO-008-verification.md"]
evaluator_evidence_path = "docs/engineering/release-orchestration/evidence/VREC-RLO-008-evaluator.json"
evaluator_evidence_sha256 = "fcfc14471cc373fce07ece222f6c03b2152dad2cf4cd5ae6e04cf147c4171962"

verified_at = "2026-08-27T17:35:55Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-RLO-008"]
conforms_to = ["VER-RLO-004"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-08-27T17:35:55Z"
decided_by = "assurance-owner"
reason = "Assurance owner decision 2026-08-27 under DR-VREC-DECIDE: I verify VREC-RLO-008. Its own fields were re-measured immediately before this transition, because a verified record can never afterwards be corrected: candidate 0dfdc648521799ba8499687a9611120bcfeb44ac exists as a commit object, object format sha1, pushed to origin and an ancestor of pull request #202's head 2623635, and not an ancestor of main; the bound evidence is tracked at that candidate as blob b9a9d7f5e482566db2c3556a39411dbc42862dba; the evaluator sidecar fcfc1447 is absent at the candidate and tracked in the record's own commit above it, the ordinary shape. WO-RLO-008 is implemented and VER-RLO-004 is approved. artifact_snapshot_sha256 f67b5cbf is a capture-time dashboard-manifest figure that HEAD, checkout basename and clone depth all move, so it is not re-asserted from another checkout. All five recorded deviations are accepted as written, unsoftened, including deviation 3, the absence of any POSIX or hosted reading at retention. Since retention that gap is substantially closed and the record cannot be edited, so it is recorded here: pull request #202's rehearsal supplied this producer code from merged tree 6e2ed4a2 and replayed RLS-SEH-016's bound candidate 58efcaa on ubuntu-latest, reaching state exact with both builds at the record's bound wheel ddd403cd and sdist e687c43f and the rebuilt bundle verified against the record, so an already bound record still replays to its bound bytes on a POSIX host with this change. Two limits on that reading: it is not the RLS-SEH-015 that VER-RLO-004's row names, and the candidate lane's expected hashes are null so it proves only self-agreement. All fourteen checks pass. This covers VREC-RLO-008 only and authorizes no release, tag, publication or deployment. The pull request must be merged as a true merge; a rebase or squash orphans the bound candidate and this record with it."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-RLO-008` to candidate commit `0dfdc648521799ba8499687a9611120bcfeb44ac`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
