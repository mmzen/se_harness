+++
id = "WO-HUP-026"
type = "work_order"
title = "Support schema-5 adoption in the predecessor assessment"
status = "implemented"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen approved the two-file schema-5 correction with required commit-bound verification in VREC-HUP-025; integration relies on this assessment of the exact evaluator transition."
decided_by = "mmzen"

[execution_scope]
paths = [
  "scripts/validate_governor_transition.py",
  "tests/test_governor_transition.py",
  "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-026.md",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-026/",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-026-evaluator.json",
  "docs/engineering/repository-harness-upgrade/verification-records/VREC-HUP-025.md",
  "docs/engineering/repository-harness-upgrade/evidence/VREC-HUP-025-evaluator.json",
]

[relations]
implements = ["REQ-IAR-031"]
specifications = ["SPEC-IAR-016"]
architecture = ["ARCH-IAR-012", "ADR-IAR-012"]
verification = ["VER-HUP-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T08:48:30Z"
decided_by = "mmzen"
reason = "Human mmzen: Approve WO-HUP-026 and required verification. Approves the reviewed two-file schema-5 assessment correction and required commit-bound verification in VREC-HUP-025. Reviewed SHA256 91890e5c8b23dadb4bd7b8e6005c4d98e4e793551e3312c5087ed5ecb98718b9; exact patch SHA256 8ee8fb98c5add07e06054a56e8507a900ca642a88a2ede56b25bcf98e25070e5. Existing adoption authority is retained. Human verification acceptance and external actions remain separate."
scope_paths = ["scripts/validate_governor_transition.py", "tests/test_governor_transition.py", "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-026.md", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-026/", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-026-evaluator.json", "docs/engineering/repository-harness-upgrade/verification-records/VREC-HUP-025.md", "docs/engineering/repository-harness-upgrade/evidence/VREC-HUP-025-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-02T08:49:32Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-10-02T08:57:30Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed."
+++

# Support schema-5 adoption in the predecessor assessment

## Objective

The repository-owned predecessor assessment can validate the approved schema-5
external-resource adoption without relaxing release identity or transaction checks.
Reuse SPEC-IAR-016 IAR-EXT-002, IAR-EXT-004 and IAR-EXT-009 and the existing
VER-HUP-003 A0210-04 acceptance case. No new product contract is proposed.

## Observed blocker

The actual assessment at clean commit 9108c4f8f953c925aa6a99ee8f57f83c8ea8393a
fails with: "target lock schema is unsupported (minimum schema 3)". The script
accepts only schemas 3 and 4. Released 0.21.0 creates schema 5 with the
released-resources-v1 discriminator. The adopted released evaluator's identity,
doctor, validation and qualification pass. The 1,215-test source suite and 49
focused tests pass; they did not cover this script against a schema-5 root.

The script and its tests are outside WO-HUP-003 and WO-HUP-005. Those work orders
remain in progress. Preserve their recorded approvals and completed operations.
This correction joins the same planned VREC-HUP-025; it does not redo migration.

## In scope

- Accept integer lock schema 5 in the existing read-only assessment script.
- Require released-resources-v1 in both schema-5 configuration and lock.
  Reject external-resource declarations on older schemas and preserve the
  existing prohibition on repository skill ownership in schema 5.
- Keep the released-record, exact prior-lock, wheel/payload, transaction,
  clean-worktree and same-version drift checks unchanged.
- Extend the existing test module for migration from supported predecessor
  layouts, ordinary unchanged schema-5 roots, invalid layout/ownership,
  unknown schemas, mismatched prior receipts and unexplained lock drift.
- Run the real assessment on a clean committed adoption candidate, retain
  evidence and complete verification together with WO-HUP-003 and WO-HUP-005.

## Out of scope

Released evaluator code, installer behavior, machine lifecycle policy, CI job
selection, other files, lock editing, new versions, further retirements,
credentials, host tests, publishing, push/PR and merge. No required gate is
removed or waived. Accepted definitions and historical evidence remain unchanged.

## Proposed assurance and decision envelope

Required commit-bound verification is proposed because the script judges the
identity transition relied on by later integration decisions. The human has
not yet approved this work order or classification. Record no invented approver.

After approval and start, the agent may apply the reviewed correction, run
checks, retain evidence, make local commits, record implementation and prepare
VREC-HUP-025 with all three work orders. Human verification and external actions
remain separate. No additional execution approval is needed inside this scope.

## Constraints and expected change surface

One script and its existing test module change. Keep the script stdlib-only and
usable with Python -S. Use the exact public 0.21.0 evaluator outside the checkout
for governed actions. Proposed script runs are diagnostic evidence, not proof
that the current committed script has passed. The adoption baseline remains
695d6773dc86f25691a9799e969bcca014207837.

This is the smallest correction: extend the script's declared layout recognition
and preserve its independent assessment checks. Do not import candidate package
code into that trust boundary or add a second resource resolver.

## Required verification

1. The focused governor-transition tests pass, including prior refusal tests
   and the new schema-5 normal and boundary cases.
2. The actual corrected script assesses the clean committed adoption candidate
   against the original main base, using the exact released 0.21.0 Python,
   entry point and wheel. Identity, doctor and validation pass through that
   assessment, with the original upgrade transaction bound to the base lock.
3. Full-scale source tests, distribution checks, evaluator checks and complete
   combined handoff pass. All VER-HUP-003 criteria remain required; hosted
   Linux and Windows checks must pass before integration.
4. VREC-HUP-025 binds all three work orders and VER-HUP-003 to one exact clean
   candidate. Verification acceptance remains a separate human decision.

## Evidence to record

Retain the original assessment refusal, reviewed patch, prototype findings,
actual corrected assessment, focused and full check summaries, review and
completion evidence in this work order's evidence directory. Raw logs may stay
outside the repository with exact retrieval paths and digests. Use the named
WO-HUP-026-evaluator.json and shared VREC destinations for generated evidence.
Preserve failed prototype tests alongside corrected results.

## Stop and escalate conditions

Stop the affected action for failed required checks, changed accepted meaning,
missing release or transaction identity, or a necessary path outside this scope.
Do not use the prototype to declare the committed script fixed or to complete
the pending adoption. Do not hand-edit lifecycle state or evidence bindings.

## Completion report format

Report the corrected recognition rule, preserved refusals, actual test and
assessment results, exact candidate and current states. Name remaining human
verification and integration decisions. Drafting claims no approval or completion.
