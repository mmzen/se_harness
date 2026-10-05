+++
id = "VREC-SEH-033"
type = "verification_record"
title = "Verification candidate for 6 work orders"
status = "ready"
owners = ["Codex"]
created = "2026-10-05"
updated = "2026-10-05"
commit = "4f640284ec496b88cd7aa4ba88ca537d9374a2f8"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-10-05T04:10:30Z"
prepared_by = "Codex"
artifact_snapshot_sha256 = "6e9fdec66fbc40550571338be9438dda8ad1174c804f5f2602fa0970bab602a8"
evidence_paths = ["docs/engineering/release-0-22-1/evidence/WO-RLS-040/preparation-completion-observations.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/provider-activation-observations.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/provider-configuration-applied.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-041/desktop-acceptance-observations.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-041/desktop-deferral-review.md", "docs/engineering/release-0-22-1/evidence/WO-RLS-043/amendment.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-043/corrected-native.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-043/corrected-qualification-review.md", "docs/engineering/release-0-22-1/evidence/WO-RLS-043/corrected-runtime.zip"]
evaluator_evidence_path = "docs/engineering/release-0-22-1/evidence/VREC-SEH-033-evaluator.json"
evaluator_evidence_sha256 = "2a3aae71ccdfd0da1d3f604ea7064f242db682d8d6ef2620bf22169be719b905"

[relations]
verifies_work_order = ["WO-DST-028", "WO-HAG-002", "WO-HAG-003", "WO-RLS-040", "WO-RLS-041", "WO-RLS-043"]
conforms_to = ["VER-DST-030", "VER-HAG-002", "VER-HAG-003", "VER-IAR-021", "VER-RLS-004", "VER-RLS-036", "VER-RLS-037"]
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-DST-028`, `WO-HAG-002`, `WO-HAG-003`, `WO-RLS-040`, `WO-RLS-041`, `WO-RLS-043` to candidate commit `4f640284ec496b88cd7aa4ba88ca537d9374a2f8`. Preparation uses each selected work order's recorded execution approval. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.

## Standing deviations

Accepted deviations standing on the selected work at this candidate; each names the rule it departs from and is retained here for the assurance decision:

- `DEC-RLS-009` against `SPEC-IAR-016#IAR-EXT-010`

## Candidate test run

Commit: `4f640284ec496b88cd7aa4ba88ca537d9374a2f8`. Exit status: 0.

Command arguments: `["C:\\Users\\mathi\\Documents\\Codex\\2026-09-20\\verity-plane-plugin-verity-plane-se\\work\\r221-final-20261005\\capture-source-env\\Scripts\\python.exe", "-B", "-X", "utf8", "C:\\Users\\mathi\\Documents\\Codex\\2026-09-20\\verity-plane-plugin-verity-plane-se\\work\\r221_final_capture_checks_clean.py", "4f640284ec496b88cd7aa4ba88ca537d9374a2f8", "C:\\Users\\mathi\\Documents\\Codex\\2026-09-20\\verity-plane-plugin-verity-plane-se\\work\\r221-final-20261005\\final-evidence-receipt.json", "1552249eca44eff719615f57152e52064d8dc1f7f70ab17d946616ca02a71da2"]`.

```text
{"archive_digests": {"final-qualification.zip": "ec57e2e8585a76523a033e32cd2d63a34de02926c6904dd3e8616d8db0ce11b1"}, "assessment": {"desktop": "not run / unverified; accepted release-only omission DEC-RLS-009 / RISK-RLS-007", "equivalence": "125 expanded wheel members and executable/resource host inputs match 061307929c94314ccd2beb4a53f174e536fceba8; earlier isolation and two-checkout walkthrough observations are retained at that original identity, not claimed rerun", "exact_builds": "two local and two GitHub pinned builds have identical wheel and sdist bytes", "fixture_recoveries": "completed original fixture refused a second start; restored immutable pre-execution fixture passes both platforms. Duplicate Linux draft-probe setup also refused; original successful draft/topology probes reused, remaining checks completed. All failures retained.", "hosted_service": "not tested; excluded", "linux_source": "1293 tests; 2 reported skips; exit 0", "native": "fresh final-package Codex CLI 0.159.2 and Claude Code 2.1.273 startup/activation/resume/manual+automatic compaction passed", "public_delivery": "not performed; later WO-RLS-042 / VER-RLS-038", "release_readiness": "exact RLS, final plan and complete-release decision follow human verification; not executable-ready yet", "required_automated_and_cli_checks_passed": true, "windows_source": "1293 tests; 23 reported skips; exit 0"}, "candidate": "4f640284ec496b88cd7aa4ba88ca537d9374a2f8", "fresh_complete_candidate": {"authority": "evidence-only; no lifecycle or external action authorized", "checks": [{"id": "CC001", "message": "candidate runtime is bound to the checkout", "passed": true, "subject": "candidate-runtime"}, {"id": "CC002", "message": "HEAD and tracked tree match the candidate", "passed": true, "subject": "candidate-commit"}, {"id": "CC003", "message": "artifacts=1952; errors=0; warnings=61", "passed": true, "subject": "engineering-graph"}, {"id": "CC004", "message": "target state is unchanged", "passed": true, "subject": "repository-state"}], "completion": "completed", "evaluator": {"candidate_commit": "4f640284ec496b88cd7aa4ba88ca537d9374a2f8", "diagnostics": [], "distribution": "se-harness", "identity_sha256": "bf000ab3c7570a8b2df735c67cbc136125929fe78353cc5f92a1c23d51209b26", "isolated_python": false, "pythonpath_present": false, "role": "candidate-source", "user_site_enabled": false, "version": "0.22.1"}, "independence": "candidate-controlled", "operation": "complete-candidate", "passed": true, "schema": "se-harness-release-qualification-v1", "target": {"commit": "4f640284ec496b88cd7aa4ba88ca537d9374a2f8", "identity_sha256": "c2b1029acd423f63ee66965cd981299976e8760855c4854d98f63f19057d6e83", "kind": "complete-candidate", "tree": "7e8f944c10e6cc04f7ef13280c871ccf6429906e"}}, "limits": "Evidence was collected at this exact candidate after it was committed. Its digest is bound by this test invocation and the generated VREC; the byte-identical receipt and raw archive are retained in the later review commit. Source-equivalent earlier native boundary/walkthrough evidence keeps its original identity. No human verification, release, desktop or hosted-service pass is supplied.", "retained_final_receipt_sha256": "1552249eca44eff719615f57152e52064d8dc1f7f70ab17d946616ca02a71da2"}

```

## Final assessment for the assurance owner

See [the final verification review](../evidence/WO-RLS-040/final-verification-review.md)
for every contract, exact package identity, actual check and retained failure.
The byte-identical [final receipt](../evidence/WO-RLS-040/final-evidence-receipt.json)
and [raw archive](../evidence/WO-RLS-040/final-qualification.zip) match the digests
checked by the candidate test run above. These post-candidate observations are
retained in this later review commit, not represented as files in the candidate.

Codex Windows desktop remains **not run / unverified** under mmzen's accepted
release-only DEC-RLS-009 / RISK-RLS-007 boundary. The required CLI tests passed.
Hosted service and public publication are not verified by this record. Prior
native boundary/walkthrough evidence retains its original identity and is reused
only through the explicit unchanged-byte comparison in the review.

Preparation supplies no human verification, merge, release or adoption decision.
