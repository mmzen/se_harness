+++
id = "VREC-HUP-026"
type = "verification_record"
title = "Verification candidate for WO-HUP-027"
status = "ready"
owners = ["Codex"]
created = "2026-10-02"
updated = "2026-10-02"
commit = "6a9c8dababcc3e0542e0e709b394f3c0b3afafef"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-10-02T09:37:46Z"
prepared_by = "Codex"
artifact_snapshot_sha256 = "613ed9d6e37a23eb4f08870faf84445acad723d985dcf966552b0fe000594c25"
evidence_paths = ["docs/engineering/repository-harness-upgrade/evidence/WO-HUP-003/acceptance-assessment.md", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/WO-HUP-027-handoff.md", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/assessment.md", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/combined-handoff.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/diagnostic-log-index.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/pr520-file-check-pr.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/pr520-file-root-qualification-local.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/pr520-file-root-qualification.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/pr520-index-reproduction.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/pr520-proposal-review-identity.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/pr520-proposed-real-rehearsal-1.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/pr520-proposed-real-rehearsal-2.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/pr520-prototype-regressions.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/pr520-rehearsal-prototype-tests-v2.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/pr520-rehearsal-prototype-tests.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/wo027-approval-apply.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/wo027-approval-preview.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/wo027-cli-smoke.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/wo027-completion-apply.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/wo027-completion-preview.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/wo027-distribution.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/wo027-doctor.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/wo027-full-source-suite.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/wo027-full-timings.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/wo027-identity-corrected.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/wo027-identity.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/wo027-implementation-identity.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/wo027-planned-scope.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/wo027-predecessor-assessment-result.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/wo027-predecessor-assessment.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/wo027-real-rehearsal-1.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/wo027-real-rehearsal-2.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/wo027-review-preflight.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/wo027-root-qualification.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/wo027-start-apply.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/wo027-start-preflight.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/wo027-start-preview.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-027/wo027-validate.json", "docs/engineering/repository-harness-upgrade/verification-records/VREC-HUP-025.md"]
evaluator_evidence_path = "docs/engineering/repository-harness-upgrade/evidence/VREC-HUP-026-evaluator.json"
evaluator_evidence_sha256 = "aba3bcc3d778a9209c591cce9beaa278b9dcebf58e091bd56fcc91b2225be157"

[relations]
verifies_work_order = ["WO-HUP-027"]
conforms_to = ["VER-HUP-003"]
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-HUP-027` to candidate commit `6a9c8dababcc3e0542e0e709b394f3c0b3afafef`. Preparation uses each selected work order's recorded execution approval. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.

## Candidate test run

Commit: `6a9c8dababcc3e0542e0e709b394f3c0b3afafef`. Exit status: 0.

Command arguments: `["C:\\Users\\mathi\\Documents\\Codex\\2026-09-20\\verity-plane-plugin-verity-plane-se\\work\\rls031-capture-python\\Scripts\\python.exe", "-B", "scripts/run_tests.py", "--scale", "full", "--timings", "C:\\Users\\mathi\\Documents\\Codex\\2026-09-20\\verity-plane-plugin-verity-plane-se\\work\\adoption021-evidence\\vrec026-candidate-timings.json"]`.

```text
Evaluator Python: C:\Users\mathi\AppData\Local\Temp\simple-plugin-jj6dmgqr\private\evaluators\0.0.0\d394929409cde9c1838c080aeddcda18be104363fcb377f8518bb733f3ae25dd\Scripts\python.exe
Evaluator Python: C:\Users\mathi\AppData\Local\Temp\simple-plugin-jj6dmgqr\private\evaluators\0.0.0\d394929409cde9c1838c080aeddcda18be104363fcb377f8518bb733f3ae25dd\Scripts\python.exe
WEX_SCALE artifacts=100 validation=0.172509s focus=0.406153s plan=0.331224s
WEX_SCALE artifacts=500 validation=0.763723s focus=1.016364s plan=1.477830s
WEX_SCALE artifacts=1000 validation=1.505469s focus=1.766955s plan=3.138099s
0.21.1
docs/notes/diagnostic-codes.md matches the source
----------------------------------------------------------------------
Ran 1222 tests in 159.983s (182 classes, 8 workers)

OK (skipped=21)
--workers must be at least 1

```
