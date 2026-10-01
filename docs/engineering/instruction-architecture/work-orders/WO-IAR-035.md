+++
id = "WO-IAR-035"
type = "work_order"
title = "Validate empty external-resource installations"
status = "implemented"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-10-01"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen confirmed required commit-bound verification with approval of WO-IAR-035, included in VREC-IAR-020. Lifecycle consumers and CI rely on this validator."
decided_by = "mmzen"

[execution_scope]
paths = [
  "se_harness/engine/validate_engineering_artifacts.py",
  "tests/test_resources.py",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-035.md",
  "docs/engineering/instruction-architecture/evidence/WO-IAR-035/",
  "docs/engineering/instruction-architecture/verification-records/VREC-IAR-020.md",
  "docs/engineering/instruction-architecture/evidence/VREC-IAR-020-evaluator.json",
]

[relations]
implements = ["REQ-IAR-031"]
specifications = ["SPEC-IAR-016"]
architecture = ["ARCH-IAR-012", "ADR-IAR-012"]
verification = ["VER-IAR-022"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-30T18:38:11Z"
decided_by = "mmzen"
reason = "Human mmzen: Approve WO-IAR-035 and verification. Confirms required commit-bound verification in VREC-IAR-020. Reviewed draft SHA256 f18f07328a5b84eafc7ddb83db3fc42f03c3aacdd48523ff71ee4aabb83d6ef5; only confirmed assurance metadata was added before preview."
scope_paths = ["se_harness/engine/validate_engineering_artifacts.py", "tests/test_resources.py", "docs/engineering/instruction-architecture/work-orders/WO-IAR-035.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-035/", "docs/engineering/instruction-architecture/verification-records/VREC-IAR-020.md", "docs/engineering/instruction-architecture/evidence/VREC-IAR-020-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-30T18:38:42Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-10-01T17:49:35Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed. Completed the approved local scope and retained integrated tests, review and complete Git handoff. Codex desktop remains explicitly unverified under the existing human instruction to continue; no assurance acceptance or external action is inferred."
+++

# Validate empty external-resource installations

## Objective and observed defect

Minimal initialization deliberately creates no docs/engineering directory.
The validator currently leaves authoring_advisories unassigned when that
directory is absent and then raises UnboundLocalError while constructing its
report. The retained install030-focused-02.json run reproduces this in the
two minimal CLI scenarios. This validator file is outside WO-IAR-030 and
WO-IAR-034.

## Bounded correction

Initialize the advisory list before either branch. Treat an absent default
artifact directory as an empty collection only for a validated external-resource
selection. Resolve the selected package before applying that exception.
An absent explicit alternate artifact root, a legacy missing artifact root,
invalid selection and malformed existing artifacts must retain their refusal.

Add focused regressions in tests/test_resources.py. Retain the already exposed
CLI regressions under WO-IAR-034; do not skip or weaken them. No directory is
created merely to satisfy validation. No state, scope, approval or evidence
rule changes.

## Proposed assurance

Required commit-bound verification. Lifecycle consumers and CI rely on this
validator. Classification awaits human confirmation; no decision-maker is
recorded in assurance metadata yet.

## Authority and boundaries

After approval, execute this correction, local tests and commits, evidence
retention and verification preparation. Include this work with the integrated
candidate in VREC-IAR-020, subject to its existing ID availability check.
Do not edit accepted definitions, installed harness files or historical records.
CI verifier compatibility, release, adoption, push and PR remain outside this
work order. A new path or changed requirement returns for review.

## Verification and evidence

Apply VER-IAR-022. Run current minimal CLI validation and focused validator tests,
then the full integrated suite and installed-wheel checks. Confirm zero default
repository additions beyond the two selection files, unchanged bytes on refusal,
empty external selection success and preserved legacy/custom-root failure.
Record actual commands, failures and results under the declared evidence prefix.

## Completion

Report the exact changed files, candidate, checks, remaining limitations and
released evaluator next step. This draft does not authorize implementation,
verification acceptance or external actions.
