+++
id = "VER-RLS-001"
type = "verification"
title = "Verify the bounded README length correction"
status = "draft"
owners = ["mmzen"]
created = "2026-10-03"
updated = "2026-10-03"

[relations]
verifies = ["REQ-DST-069"]
+++

# Verify the bounded README length correction

## Independence

REQ-DST-069 and SPEC-DST-024 PUB-BUDGET-001 supply the 650-word limit.
SPEC-DST-029 supplies the current plugin-onboarding rules. Preserve the public
identities and accepted untested-host disclosure retained in VREC-PLG-033.
The proposed README must not supply its own expected claims or acceptance limit.

## Requirement-to-evidence matrix

| Requirement | Method | Evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-DST-069 | test, inspection | Final README diff; existing public-onboarding and documentation checks | At most 650 whitespace-separated source words, 200 physical lines and seven level-two headings. Remove only the second duplicate host-limit paragraph; retain its first copy beside installation, all commands, links, versions, images and remaining text. |

## Checks and retained evidence

1. Inspect the diff against the reviewed one-paragraph deletion. Keep test
   thresholds and source tests unchanged. Confirm the remaining warning still
   identifies Claude Code and Codex Windows desktop as not tested/unverified.
2. Run the existing tests with Python 3.11 or newer on Windows:
   `python -m unittest tests.test_public_onboarding tests.test_progressive_documentation tests.plugin_integration.package_assembly.test_refresh_guidance`.
3. Retain the existing Linux CI failure and require the complete candidate-source
   CI run to pass on the corrected PR head before merge. Preserve actual skips.
4. Use the selected released 0.21.0 evaluator for validation, scope, preflight,
   handoff and commit-bound capture. Candidate source is not the governing evaluator.
5. Capture a new verification record against the clean corrected candidate;
   preserve VREC-PLG-032/033 and their evidence. Publish the review in PR #530
   before requesting the separate human verification decision.

Retain actual inputs, command arrays, runtime identities, exit codes, failures,
and file hashes in `evidence/WO-RLS-037/` in this domain. Reserve VREC-PLG-034
and its canonical `evidence/VREC-PLG-034-evaluator.json` after checking availability
across local refs again before capture. Later CI/public observations remain
separate from frozen candidate evidence.

## Limits

This contract assesses the README correction. It does not requalify packages,
claim omitted host tests passed, waive CI or move release markers. The current
release's Claude/desktop omissions and remaining delivery steps stay explicit.
