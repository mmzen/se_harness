+++
id = "WO-HUP-029"
type = "work_order"
title = "Recognize recorded human release identities during adoption"
status = "in_progress"
owners = ["mmzen"]
created = "2026-10-03"
updated = "2026-10-03"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen confirmed required commit-bound verification because adoption CI relies on release decision identity matching and preserved release and transaction checks."
decided_by = "mmzen"

[execution_scope]
paths = [
  "scripts/validate_governor_transition.py",
  "tests/test_governor_transition.py",
  "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-029.md",
  "docs/engineering/repository-harness-upgrade/verification/VER-HUP-024.md",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-029/",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-029-evaluator.json",
  "docs/engineering/repository-harness-upgrade/verification-records/VREC-HUP-027.md",
  "docs/engineering/repository-harness-upgrade/evidence/VREC-HUP-027-evaluator.json",
]

[relations]
implements = ["REQ-REB-027", "REQ-IAR-031"]
specifications = ["SPEC-REB-012", "SPEC-IAR-016"]
architecture = ["ARCH-REB-011", "ADR-REB-011", "ARCH-IAR-012", "ADR-IAR-012"]
verification = ["VER-HUP-024"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-03T07:27:59Z"
decided_by = "mmzen"
reason = "Human mmzen replied \"I approve\" to the reviewed WO-HUP-029 / VER-HUP-024 two-file CI correction, required commit-bound verification in VREC-HUP-027 and inclusion in the existing review PR grant. Reviewed file SHA256 72610ee7a1a72a639f47dbdfda3dea45a352b3c2554b5a4e6c80c8ff933b27b9; patch SHA256 10fd74e48ab683ff1e85e5735a40aa027047164f72db4260e616ccf4ff3bc3a5. Human verification acceptance and merge remain separate. Codex applies the recorded decision."
scope_paths = ["scripts/validate_governor_transition.py", "tests/test_governor_transition.py", "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-029.md", "docs/engineering/repository-harness-upgrade/verification/VER-HUP-024.md", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-029/", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-029-evaluator.json", "docs/engineering/repository-harness-upgrade/verification-records/VREC-HUP-027.md", "docs/engineering/repository-harness-upgrade/evidence/VREC-HUP-027-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-03T07:28:36Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed. Start the reviewed correction under human mmzen approval."
+++

# Recognize recorded human release identities during adoption

## Objective

Let the repository's predecessor assessment recognize the actual human recorded
in an otherwise valid released record. Preserve the release and transaction checks.
This unblocks the approved 0.22.0 adoption without rewriting release history.

## Observed blocker

The assessment of commit e5bdb392ea97120ff950c9e160675418cd35fab8 against
trusted base b9821e3a3ef3f821f36cc92da7fa4ce900f7e750 rejects RLS-SEH-032.
It requires the literal label `release-owner` in two fields. The valid record
names human `mmzen` in both `authorized_by` and its ready-to-released event.
The selected evaluator accepts that record; its identity, doctor, validation
and released-root qualification pass. This script is outside WO-HUP-028.

## In scope and expected change surface

- `scripts/validate_governor_transition.py`: require a non-empty string
  authorizer and a matching ready-to-released decision identity. Preserve
  legacy `release-owner` records, trusted-base selection, unique released
  record, version, tag, archive digest and canonical transaction checks.
- `tests/test_governor_transition.py`: cover named humans, the legacy label,
  absent/empty/malformed authorizers and mismatched decision identities.
- This work order, VER-HUP-024 and the listed review/evidence outputs: retain
  the defect, proposed diff, observed checks and exact candidate assessment.
- VREC-HUP-027 and its fixed companion: combine this correction with the
  approved adoption, including both verification contracts. Recheck ID
  availability before capture; it is not a prepared record yet.

Reuse the existing simple-upgrade and resource-compatibility definitions and
architecture. This repairs an obsolete repository consumer assumption. It
does not introduce a new decision right or change evaluator lifecycle rules.

## Required verification and evidence

VER-HUP-024 defines the checks. Propose required commit-bound verification
because CI relies on this script when accepting evaluator adoption. Record
the confirming human in assurance metadata only after approval. Retain raw
tests, the real predecessor assessment and review under evidence/WO-HUP-029/.
Keep failed results alongside corrected results.

## Authorized decision envelope

Proposed approval covers the two implementation/test files, local checks,
commits, completion and combined verification preparation. It also extends
the existing review-publication grant to this bounded correction in
`mmzen/se_harness`, branch `work/adopt-0-22-0`, target `main`: push/update the
draft PR and later publish the matching human verification decision. Human
verification acceptance and merge remain separate.

## Out of scope and stop conditions

Do not edit RLS-SEH-032, any historical release decision, the released wheel,
installer behavior, provider configuration or host authentication. Do not
skip required checks. A missing or mismatched release decision still fails.
Stop if another behavior, file, definition or authority is needed.

## Simplicity and completion

Compare the two existing identity fields; add no actor registry or role map.
Report the passed and refused identity cases, real adoption assessment,
remaining checks, exact candidate and pending human verification.
