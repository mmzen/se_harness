+++
id = "WO-RLS-030"
type = "work_order"
title = "Restore the README offline setup clarification"
status = "implemented"
owners = ["mmzen"]
created = "2026-10-01"
updated = "2026-10-01"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen approved required commit-bound verification for this README correction because current setup instructions are trusted information used by consumers and later integration decisions."
decided_by = "mmzen"

[execution_scope]
paths = [
  "README.md",
  "docs/engineering/release-0-20-1/work-orders/WO-RLS-030.md",
  "docs/engineering/release-0-20-1/evidence/WO-RLS-030/",
  "docs/engineering/release-0-20-1/verification-records/VREC-PLG-029.md",
  "docs/engineering/release-0-20-1/evidence/VREC-PLG-029-evaluator.json",
]

[relations]
implements = ["REQ-RLO-019"]
specifications = ["SPEC-RLO-006"]
verification = ["VER-RLS-029"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-01T10:50:43Z"
decided_by = "engineering-owner"
reason = "Human mmzen: i approve, responding to the reviewed one-sentence WO-RLS-030 correction and required commit-bound verification. Reviewed artifact SHA256 f684ffca6b525deb3b420f7c5247bb1722579131e4707327a5aadc127035a9a0; transition input SHA256 8a4e30e936f0486dc5ed14d2ff339b3efe475c3cbcbdc0f0cb609786d2958c03. Only the human-confirmed assurance fields were added before preview. Existing VER-RLS-029 is reused unchanged. Approval includes local execution, aggregate VREC-PLG-029 preparation, and the stated ordinary branch/PR #513 updates after human verification and passing gates. Codex applies the human decision using the selected evaluator's engineering-owner label. Merge, publication, markers and adoption remain separate."
scope_paths = ["README.md", "docs/engineering/release-0-20-1/work-orders/WO-RLS-030.md", "docs/engineering/release-0-20-1/evidence/WO-RLS-030/", "docs/engineering/release-0-20-1/verification-records/VREC-PLG-029.md", "docs/engineering/release-0-20-1/evidence/VREC-PLG-029-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-01T10:51:31Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-10-01T10:58:59Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed."
+++

# Restore the README offline setup clarification

## Objective and observed failure

Restore the explicit offline setup statement omitted during WO-RLS-029.
PR #513 at fe048340d39461cde161bfafd7f486b51a4c9ca6 fails the existing
PublicOnboardingTests.test_plugin_setup_uses_a_released_wheel_and_keeps_project_changes_explicit
check. CI run 36849457709 ran 1,189 tests with one failure and two skips.
The local reproduction confirms the same missing sentence. No product failure
or marketplace package mismatch was observed.

## In scope

After the README sentence ending "into a private environment.", restore:

> It does not download the harness from PyPI.

This is the complete proposed implementation change. Keep the current versions,
public receipts, installation commands and support limits. Reuse the approved
REQ-RLO-019, SPEC-RLO-006 and VER-RLS-029 without changing their definitions.
No new mechanism or architecture is needed.

## Required verification

Keep the existing tests unchanged. Run the public-onboarding suite and the
relevant documentation and delivery checks, then the complete source regression
with the repository's existing runner. Retain actual skips and failures.
Check that the README still meets its bounded-entry size and link rules.

Follow VER-RLS-029 for the combined documentation candidate. Prepare
VREC-PLG-029 covering WO-RLS-029 and WO-RLS-030 at one exact clean commit.
Reuse the already verified public package, installation and native-delivery
observations only after confirming their unchanged inputs and evidence bytes.
Do not rerun publication or infer new host support. Preserve VREC-PLG-028 and
its frozen candidate and evidence. The new record requires a separate human
verification decision.

## Proposed assurance and decision envelope

Commit-bound verification is proposed as required: current setup instructions
are trusted information used by consumers and later integration decisions.
The accountable human must confirm this classification with work-order approval;
no assurance decision has been supplied by the drafting agent.

Approval authorizes the one-sentence edit, local checks and commits, evidence
retention, completion recording and aggregate verification preparation. It also
covers ordinary updates to work/public-marketplace-0-2-3 and existing draft
PR #513 in mmzen/se_harness once the relevant gates and human verification pass.
The original review-branch authority remains applicable. No force push, merge,
release-marker change, publication, adoption or accepted-definition amendment
is included.

## Evidence and stops

Retain the failed CI summary, run/artifact identity and expiry, local reproduction,
exact proposed diff, actual test results, review and generated handoff evidence
under evidence/WO-RLS-030/. Keep raw temporary files outside the repository;
retain the available CI artifact link and download command. Preserve prior
failures and existing verified evidence without rewriting them.

Stop if the correction needs another implementation edit, changed tests,
changed published bytes or another path. Report the new finding rather than
expanding this work order. Do not reset WO-RLS-029 from implemented.

## Completion report

Report the restored statement, exact candidate, actual test results, remaining
limitations and prepared verification record. CI success, human verification,
merge and overall release-delivery completion remain distinct results.
