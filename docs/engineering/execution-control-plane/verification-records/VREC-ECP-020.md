+++
id = "VREC-ECP-020"
type = "verification_record"
title = "Verification candidate for WO-ECP-017"
status = "verified"
owners = ["assurance-owner"]
created = "2026-08-29"
updated = "2026-08-29"
commit = "94991fe38cca7982a5214ff57e554af4895adbde"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-29T12:48:02Z"
prepared_by = "assurance-owner"
artifact_snapshot_sha256 = "472e4ee6b3cc7b0eefee64177d6c111f340fb39948f8017a5161067d326d3d04"
evidence_paths = ["docs/engineering/execution-control-plane/evidence/WO-ECP-017/WO-ECP-017-handoff.md", "docs/engineering/execution-control-plane/evidence/WO-ECP-017/handoff.json"]
evaluator_evidence_path = "docs/engineering/execution-control-plane/evidence/VREC-ECP-020-evaluator.json"
evaluator_evidence_sha256 = "41578bab531e143cd9864870c9af1495aed7465eff512571387403aa734a1f26"

verified_at = "2026-08-29T12:53:56Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-ECP-017"]
conforms_to = ["VER-ECP-011", "VER-ECP-013"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-08-29T12:53:56Z"
decided_by = "assurance-owner"
reason = "Verified by the accountable assurance owner on 2026-08-29, 'I verify VREC-ECP-020 as assurance owner'. Re-measured immediately before this transition: bound commit 94991fe is an ancestor of the branch tip with a clean worktree; WO-ECP-017 is implemented; the evaluator packet matches its recorded digest 41578bab. The retained evidence shows harnessctl without a focus subcommand and refusing it with check named, the projection under one name, the template harness-orient core probing check for an optional --checkpoint and invoking it (ECP-ONE-007 of SPEC-ECP-011, deferred at WO-ECP-015, now met), the phase-1, phase-3 and phase-4 vector fixtures byte-unchanged with the new identity in a phase-5 row, the Windows workstation at its two baseline failures, and the moved core degrading with AEXORI030 against the released 0.10.0 evaluator whose check still requires a checkpoint. At the bound commit the managed Engineering Harness lane and the governor assessment completed success while the Publication Rehearsal and Candidate Evidence workflows were cancelled by the record push; at the record head d477aff, which carries the identical product tree, all thirteen lanes pass. The three deviations the packet records are accepted with this verification: the focus_schema2 wrapper kept for its Phase 4 caller, the probe beyond ECP-RMV-004's text, and the scope amendment. VER-ECP-013's and VER-ECP-011's pass conditions are met. This verifies WO-ECP-017 only; it releases and publishes nothing."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-ECP-017` to candidate commit `94991fe38cca7982a5214ff57e554af4895adbde`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
