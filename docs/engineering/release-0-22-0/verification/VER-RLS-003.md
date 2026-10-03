+++
id = "VER-RLS-003"
type = "verification"
title = "Verify the concise Claude coverage notice"
status = "approved"
owners = ["mmzen"]
created = "2026-10-03"
updated = "2026-10-03"

[relations]
verifies = ["REQ-DST-069", "REQ-RLO-020"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-03T10:20:02Z"
decided_by = "mmzen"
reason = "Human mmzen replied I approve to the reviewed WO-RLS-039 and VER-RLS-003 request: shorten only the new README paragraph from 690 to 644 total words, preserve its evidence link and unverified areas, run unchanged documentation tests and the full suite, and prepare required commit-bound verification. Approval also covers correction and later verification-decision pushes to existing PR 533, mmzen/se_harness, work/claude-025-evidence-followup to main. Human acceptance of the corrected candidate and merge remain separate. Codex applies this decision. Reviewed SHA-256 77495b1d163a1479b65abfd9567ef54c6d462d36b1de30ae238bea8152e47be1; transition input SHA-256 77495b1d163a1479b65abfd9567ef54c6d462d36b1de30ae238bea8152e47be1. Only confirmed WO assurance metadata was added."
+++

# Verify the concise Claude coverage notice

## Independence

Use SPEC-DST-024 PUB-BUDGET-001 for the size limits and SPEC-DST-029 for current
plugin-first presentation. Expected coverage comes from the immutable
WO-RLS-038 observations and original release evidence, not the new paragraph.
The proposal preview is not final-candidate verification.

## Requirement-to-evidence matrix

| Requirement | Method | Pass condition |
| --- | --- | --- |
| REQ-DST-069 | Source counts, diff inspection and unchanged onboarding tests. | At most 650 whitespace-separated source words, 200 lines and seven level-two headings; valid links and the existing onboarding content preserved. |
| REQ-RLO-020 | Compare the paragraph with WO-RLS-038 evidence and decisions. | Keep the evidence link, observed Windows subset, all three unverified areas and unchanged historical authority; no broader host verification claim. |

## Checks

1. Confirm the implementation matches proposed-readme.patch and changes only the
   selected README paragraph, apart from declared governance and evidence files.
2. Count words, lines and headings from the actual README. Read the paragraph
   and follow its evidence link; verify its local path and factual limits.
3. Run `python -B -X utf8 -m unittest tests.test_public_onboarding
   tests.test_progressive_documentation
   tests.plugin_integration.package_assembly.test_refresh_guidance` as one command.
4. Run `python scripts/run_tests.py --workers 4 --scale full`. Retain failures
   and corrected results. These tests remain unchanged.
5. Run released validation, start/review preflight, complete scope and handoff
   checks, and `git diff --check`. Confirm prior evidence and accepted records
   remain byte-identical to the baseline.
6. Capture the exact clean combined candidate for WO-RLS-038/039 with VER-RLS-002
   and this contract. Reuse unchanged native observations; reassess their claims.
   Publish the ready record in PR #533 before requesting human verification.
   CI on the final review head must pass before calling the correction merge-ready.

## Evidence retention and environment

Retain actual command arrays, runtime versions, exits, outputs, hashes and review
under docs/engineering/release-0-22-0/evidence/WO-RLS-039/. Use Windows local tests
and selected released evaluator 0.22.0; retain hosted Linux CI results separately.
Do not modify VREC-RLS-001, its candidate or its bound evidence.

## Residual uncertainty

This correction verifies a documentation change. It adds no native host coverage.
Codex Windows desktop, the full Claude work-order walkthrough and the earlier
long-path failure remain unverified. Existing accepted risks remain unchanged.
