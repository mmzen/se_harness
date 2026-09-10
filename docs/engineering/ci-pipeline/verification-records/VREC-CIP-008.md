+++
id = "VREC-CIP-008"
type = "verification_record"
title = "Verification candidate for WO-CIP-008"
status = "verified"
owners = ["delegated-executor"]
created = "2026-09-10"
updated = "2026-09-10"
commit = "84e761e78cc0de73616e4952cedf210f4442c27b"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-09-10T12:41:26Z"
prepared_by = "delegated-executor"
artifact_snapshot_sha256 = "10f6ebdcfa5e9192ea342454f78a81513c2f2dfe6a2c4b8a1feeeaf568ad7949"
evidence_paths = ["docs/engineering/ci-pipeline/evidence/WO-CIP-008/WO-CIP-008-handoff.md", "docs/engineering/ci-pipeline/evidence/WO-CIP-008/handoff.json", "docs/engineering/ci-pipeline/evidence/WO-CIP-008/readings.md"]
evaluator_evidence_path = "docs/engineering/ci-pipeline/evidence/VREC-CIP-008-evaluator.json"
evaluator_evidence_sha256 = "44d4b74d9febe03a0828dfeee8cd8322fd02db74ff866d7191440e17164e7abb"

verified_at = "2026-09-10T12:51:40Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-CIP-008"]
conforms_to = ["VER-CIP-004"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-09-10T12:51:40Z"
decided_by = "assurance-owner"
reason = "Verified by the assurance owner on 2026-09-10 by selecting the presented option 'Verify both and merge both (Recommended)'. Re-measured immediately before this transition: bound commit 84e761e7 is an ancestor of the record head f8f3932d with a clean worktree, WO-CIP-008 is implemented, the evaluator packet matches its recorded digest 44d4b74d, and the three retained evidence files are tracked. Every VER-CIP-004 row passes: in the artifact bodies the grep of acceptance 2 returns the old name only inside the two amendment records of ARCH-CIP-001 and REQ-CIP-002; DefinitionNamesTests pins it and names file and line on a reinserted name (negative control ARCH-CIP-001.md:43); each record names the former name, WO-CIP-007 and the date, the requirement's also the reconcile job's removal under WO-CIP-001; only updated differs in either front matter; the index names the repair and no workflow, script or managed path is in the change set. Regression: validate 1,480 artifacts and 0 errors under the released 0.17.0 evaluator, doctor 99 PASS, 1,127 tests at the Windows baseline, 17 of 17 lanes green at 1602fcb4, 84e761e7 and f8f3932d. Delegation: the start, implemented and preparation events name delegated-executor with the class, check-run and sha. Accepted with the disclosures: the front-matter measure of REQ-CIP-009 and the source and measure of REQ-CIP-010 name the retired name as retired and are pinned by the test, so CIP-AMD-004 is read over artifact bodies; REQ-CIP-002's Rationale names the two jobs without their retired names; one intermediate commit's test syntax error was repaired before completion. This verifies WO-CIP-008 only; it releases and publishes nothing, and the merge is a separate decision under DR-DELIVERY-SELECT."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-CIP-008` to candidate commit `84e761e78cc0de73616e4952cedf210f4442c27b`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything. Delegated DR-VREC-PREPARE under [delegation] class 'execution': required check 'validate' success at 84e761e78cc0de73616e4952cedf210f4442c27b (check-run 102872699894, source github-checks).

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
