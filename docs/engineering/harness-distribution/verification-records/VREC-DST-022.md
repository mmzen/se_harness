+++
id = "VREC-DST-022"
type = "verification_record"
title = "Verification candidate for WO-DST-025"
status = "verified"
owners = ["engineering-owner"]
created = "2026-09-07"
updated = "2026-09-07"
commit = "8bf3e4c7bcc8071deaf54561aec9a475b4b1114d"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-09-07T19:23:12Z"
prepared_by = "engineering-owner"
artifact_snapshot_sha256 = "7a26fb68ce623232eac4cf8ab74189cae3cd9306f537b5f38e947e87ef4bc33c"
evidence_paths = ["docs/engineering/harness-distribution/evidence/WO-DST-025-verification.md", "docs/engineering/harness-distribution/evidence/WO-DST-025/WO-DST-025-handoff.md", "docs/engineering/harness-distribution/evidence/WO-DST-025/handoff.json"]
evaluator_evidence_path = "docs/engineering/harness-distribution/evidence/VREC-DST-022-evaluator.json"
evaluator_evidence_sha256 = "e2cd0929fd42d0634d3bf23a73408665bac8ae473b98c81439dbffb828bff951"

verified_at = "2026-09-07T19:32:31Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-DST-025"]
conforms_to = ["VER-DST-026"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-09-07T19:32:31Z"
decided_by = "assurance-owner"
reason = "Verified by the accountable assurance owner on 2026-09-07 by selecting the presented option 'Verify it (Recommended)'. The record binds candidate 8bf3e4c7 on pull request #373 with a clean worktree, and all four hosted lanes are green on that commit and on the record commit 95ebd0e: SE Harness Candidate Evidence read Ran 1270 tests, OK (skipped=4), which is main's 1265 plus this work order's five with main's own four skips. VER-DST-026 is satisfied in full: the reader inventory names the module that reads each of the five surviving keys and finds no reader for any of the seven removed ones; the two remaining name collisions, an always-called require_clean_worktree function and a derived artifact_root projection, are inspected and recorded; scenarios A to C ran from a candidate wheel installed in a virtual environment outside the checkout, giving a five-key install, an upgrade of a released 0.16.0 repository planned as a safe rewrite that preserved project_name and installed_at, and a refusal on an owner-edited configuration with configuration and lock bytes unchanged; the hosted lane additionally rehearsed the real predecessor-to-successor upgrade twice on Linux and Windows. Released 0.16.0 readings are clean: validate 1358 artifacts, 0 errors, 0 advisories; review preflight PASS; the handoff checkpoint all nine gates. The local Windows control carried only its two known failures, the CRLF owner-region bound and a shutil.rmtree teardown error, both reproducing on main. The root configuration and its lock are byte-identical to main, and DST-CFG-015 carries the root adoption forward. Integration, release and publication remain separate decisions."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-DST-025` to candidate commit `8bf3e4c7bcc8071deaf54561aec9a475b4b1114d`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
