+++
id = "VREC-AUT-006"
type = "verification_record"
title = "Verification candidate for WO-AUT-006"
status = "verified"
owners = ["delegated-executor"]
created = "2026-09-09"
updated = "2026-09-09"
commit = "ff451be0c7154e754d2919865d6cc1dbbb45c190"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-09-09T18:46:14Z"
prepared_by = "delegated-executor"
artifact_snapshot_sha256 = "d18a62c20f7005abe34a4b933d660a5030f2b02ab14cb39f2f9c2d0d2489237c"
evidence_paths = ["docs/engineering/artifact-authoring/evidence/WO-AUT-006/WO-AUT-006-handoff.md", "docs/engineering/artifact-authoring/evidence/WO-AUT-006/WO-AUT-006-verification.md", "docs/engineering/artifact-authoring/evidence/WO-AUT-006/handoff.json"]
evaluator_evidence_path = "docs/engineering/artifact-authoring/evidence/VREC-AUT-006-evaluator.json"
evaluator_evidence_sha256 = "44d4b74d9febe03a0828dfeee8cd8322fd02db74ff866d7191440e17164e7abb"

verified_at = "2026-09-09T19:44:43Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-AUT-006"]
conforms_to = ["VER-AUT-004"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-09-09T19:44:43Z"
decided_by = "assurance-owner"
reason = "Verified by the assurance owner on 2026-09-09 by selecting the presented option. Re-measured immediately before this transition: bound commit ff451be0 is an ancestor of the record head f0e4e7bc with a clean worktree, WO-AUT-006 is implemented, the evaluator packet matches its recorded digest 44d4b74d, and the three retained evidence files are tracked. Every VER-AUT-004 row passes. Retired relation: constrains reads E016 naming it retired for an approved and an implemented architecture, for every target set and beside typed relations, W015 nowhere. Unassessed architecture: E014 with no W019, E015 kept for adr_required without a deciding ADR. Dashboard: the typed pair, no legacy state. Header-less packet: not assessable, naming harnessctl evidence, nothing retained, the packet untouched. V1 schema: the loader's own error; WEX-ECP-030 kept for a missing binding. Registry: the four codes gone, the kept ones present, the index matching the source. Permanent branches: commented, counted in the note. Amendments: four records, rule text verbatim. Baseline: released 0.17.0 and the candidate both 1,461 artifacts, 0 errors, 46 W013 with the record present. Scope: 27 changed paths inside the amended scope, no template, root byte or corpus artifact. Regression: 1,126 tests at the Windows baseline, the hosted suite passing, doctor and the review preflight PASS, five of five lanes green at ff451be0 and f0e4e7bc. The five acceptance scenarios were reproduced in a scratch worktree at ff451be0, the header-less packet one through the two fixture tests since the work order's own handoff checkpoint no longer applies once implemented. Disclosed: the shared fixture corpus took the typed shape, the scope amendment for validation_lifecycle.py, the TRC-008 template sentence owed to the next managed-template work order. This verifies WO-AUT-006 only; it releases and publishes nothing, and the merge is a separate decision under DR-DELIVERY-SELECT."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-AUT-006` to candidate commit `ff451be0c7154e754d2919865d6cc1dbbb45c190`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything. Delegated DR-VREC-PREPARE under [delegation] class 'execution': required check 'validate' success at ff451be0c7154e754d2919865d6cc1dbbb45c190 (check-run 102595488022, source github-checks).

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
