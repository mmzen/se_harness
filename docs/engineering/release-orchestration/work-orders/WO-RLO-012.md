+++
id = "WO-RLO-012"
type = "work_order"
title = "Correct publication provenance for the 0.20.1 maintenance release"
status = "implemented"
owners = ["mmzen"]
created = "2026-10-01"
updated = "2026-10-01"

[assurance]
commit_bound_verification = "required"
rationale = "The approved corrections change publication checks and the tag binding. Publication must rely on verification of the exact correction commit."
decided_by = "mmzen"

[execution_scope]
paths = [
  ".github/scripts/publish_release.py",
  ".github/scripts/publish_dashboard.py",
  "tests/test_release_orchestration.py",
  "tests/test_dashboard_publication.py",
  "docs/notes/developing-se-harness.md",
  "docs/engineering/release-0-20-1/releases/RLS-SEH-030.md",
  "docs/engineering/release-orchestration/work-orders/WO-RLO-012.md",
  "docs/engineering/release-orchestration/verification/VER-RLO-009.md",
  "docs/engineering/release-orchestration/evidence/WO-RLO-012/",
  "docs/engineering/release-orchestration/verification-records/VREC-RLO-012.md",
  "docs/engineering/release-orchestration/evidence/VREC-RLO-012-evaluator.json",
]

[relations]
implements = ["REQ-RLO-001"]
specifications = ["SPEC-RLO-001"]
verification = ["VER-RLO-009"]
architecture = ["ARCH-RLO-001", "ADR-RLO-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-01T06:47:33Z"
decided_by = "mmzen"
reason = "Human mmzen: Ok i approve corrections. Applies the expressly approved two-issue publication correction under WO-RLO-012 and VER-RLO-009, authored to record that instruction; required commit-bound assurance applies to changed publisher checks. No claim of earlier review of these newly authored files. The verified 0.20.1 candidate, release decision and existing evidence remain preserved; only the missing tag binding is corrected. Verification acceptance and external actions remain separate."
scope_paths = [".github/scripts/publish_release.py", ".github/scripts/publish_dashboard.py", "tests/test_release_orchestration.py", "tests/test_dashboard_publication.py", "docs/notes/developing-se-harness.md", "docs/engineering/release-0-20-1/releases/RLS-SEH-030.md", "docs/engineering/release-orchestration/work-orders/WO-RLO-012.md", "docs/engineering/release-orchestration/verification/VER-RLO-009.md", "docs/engineering/release-orchestration/evidence/WO-RLO-012/", "docs/engineering/release-orchestration/verification-records/VREC-RLO-012.md", "docs/engineering/release-orchestration/evidence/VREC-RLO-012-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-01T06:48:02Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-10-01T07:02:49Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed."
+++

# Correct publication provenance for the 0.20.1 maintenance release

## Objective and authority

Human mmzen approved the two reported publication corrections on 2026-10-01:
"Ok i approve corrections". This work records that bounded instruction;
it does not claim that the human reviewed these subsequently authored bytes.
Required commit-bound assurance applies because the correction changes trusted
publication checks. Human verification remains a separate decision.

Baseline: a0e91f65f7ead24a14d9a9c65d54ee9b05e9b7e0 on main. The verified
0.20.1 candidate remains b9af631b850c495eace9807361ed3ec3e36a10b2.
The selected governing evaluator is independently released 0.20.0.

## In scope

1. Add only the missing tag = "v0.20.1" metadata line to RLS-SEH-030.
   Preserve its release decision, candidate, distribution table, relations,
   timestamps, lifecycle history and evaluator evidence. Retain the original
   bytes and prove that removing the one added line recreates them exactly.
2. Make both publication resolvers find the first main-history commit that
   contains the complete matching released identity. A metadata correction
   does not repeat a lifecycle transition. Search binding changes as well as
   status changes; later unrelated commits must not replace this identity.
3. Keep the existing evaluator-evidence validation. If the evidence does not
   match the valid lock at the release's integration commit, check the lock
   in its exact recorded candidate. Accept only an exact identity match.
   This supports maintenance releases prepared with that candidate's selected
   released evaluator while main has adopted a later one. Read Git objects as
   data; do not import or execute candidate code. Malformed governance locks,
   damaged evidence and identities matching neither lock still fail.
4. Add focused Git-history and failure tests in the existing suites. Document
   explicit --tag during preparation and a real publication resolver check
   after integration and before dispatch. Retain the original failure.

These corrections implement SPEC-RLO-001 rules 3-5 without changing its
one-RLS interface, candidate identity, main-only governance or independent
validation. The candidate lock is already part of the candidate selected by
the released record; no new operator override or mutable branch lookup is added.

## Decision envelope and limits

The implementer may choose helper names, local factoring, test fixtures,
evidence file names and local commits within the listed paths. Start, local
implementation, checks, completion and VREC preparation follow the recorded
work approval. No new release decision, push, PR, merge, publication, live tag,
marketplace change, profile change or evaluator adoption is authorized here.

Do not modify the verified wheel source, VREC-SEH-030, its evidence, any existing
definition, managed instruction, workflow permission or package. Do not regenerate
RLS-SEH-030, relabel its evaluator evidence, remove a required check, permit a
force/skip flag, or accept a tag absent from the record. This is repository
publication work, not a new member of the 0.20.1 wheel release.

## Verification and evidence

Pass VER-RLO-009. Retain commands, results, reviewed bytes, failed attempts,
preservation comparisons and publication-plan readback under evidence/WO-RLO-012/.
Use source tests for this repository-owned helper correction and released
0.20.0 for lifecycle, integrity and scope. VREC-RLO-012 is a proposed unused
destination; confirm availability before supported capture. No candidate
assurance is claimed until the human verifies that exact record.

## Stop conditions and completion

Stop on a failed required check, unresolved history ambiguity, altered frozen
evidence, a moved baseline, or needed work beyond the listed paths. Preserve
all observations. Report the exact correction commit, actual test results,
publication readiness and the one next accountable decision. A passing local
resolver is not publication and cannot substitute for protected workflow gates.
