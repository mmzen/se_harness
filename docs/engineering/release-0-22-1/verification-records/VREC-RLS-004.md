+++
id = "VREC-RLS-004"
type = "verification_record"
title = "Verification candidate for WO-RLS-042"
status = "ready"
owners = ["Codex"]
created = "2026-10-05"
updated = "2026-10-05"
commit = "35fdd0712484145a763490846a96b7e8c63ca4bf"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-10-05T09:24:55Z"
prepared_by = "Codex"
artifact_snapshot_sha256 = "5b94571f3c9650dba24d13bfac3e8c2012b0bc1c4c29d487e2557f330ba764ab"
evidence_paths = ["docs/engineering/release-0-22-1/evidence/WO-RLS-042/claude-code-public-fresh.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/claude-code-public-update.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/closeout-assessment.md", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/closeout-checks.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/closeout-lifecycle.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/codex-public-fresh.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/codex-public-update.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/delivery-result.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/documentation-observations.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/evaluator-public-install.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/handoff.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/integration-receipts.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/maintenance-line.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/marketplace-public-ref.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/observations.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/pages-observations.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/publisher.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/release-marker-receipt.json"]
evaluator_evidence_path = "docs/engineering/release-0-22-1/evidence/VREC-RLS-004-evaluator.json"
evaluator_evidence_sha256 = "2a3aae71ccdfd0da1d3f604ea7064f242db682d8d6ef2620bf22169be719b905"

[relations]
verifies_work_order = ["WO-RLS-042"]
conforms_to = ["VER-RLS-038"]
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-RLS-042` to candidate commit `35fdd0712484145a763490846a96b7e8c63ca4bf`. Preparation uses each selected work order's recorded execution approval. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.

## Candidate test run

Commit: `35fdd0712484145a763490846a96b7e8c63ca4bf`. Exit status: 0.

Command arguments: `["C:\\Users\\mathi\\Documents\\Codex\\2026-09-20\\verity-plane-plugin-verity-plane-se\\work\\r221-final-20261005\\capture-source-env\\Scripts\\python.exe", "-B", "-X", "utf8", "C:\\Users\\mathi\\Documents\\Codex\\2026-09-20\\verity-plane-plugin-verity-plane-se\\work\\r221_closeout_capture.py", "35fdd0712484145a763490846a96b7e8c63ca4bf", "22349066ffb06d652a7f178b5a9dfddfafc883a0129c12b1e8224432d29043c5"]`.

```text
{"candidate_commit": "35fdd0712484145a763490846a96b7e8c63ca4bf", "delivery_report_sha256": "22349066ffb06d652a7f178b5a9dfddfafc883a0129c12b1e8224432d29043c5", "delivery_status": "complete", "surface_status": [{"id": "evaluator", "status": "satisfied"}, {"id": "marketplace", "status": "satisfied"}, {"id": "documentation", "status": "satisfied"}, {"id": "demonstration", "status": "satisfied"}, {"id": "release_markers", "status": "satisfied"}], "public_routes": 4, "scope": "Fresh assessment of the exact committed retained observations; public network tests were performed and captured at their recorded times. No replay of publication and no new human verification decision.", "limits": "Codex Windows desktop remains unverified under DEC-RLS-009 / RISK-RLS-007; hosted service and adoption excluded."}

```
