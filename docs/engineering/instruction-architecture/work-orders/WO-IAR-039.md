+++
id = "WO-IAR-039"
type = "work_order"
title = "Validate verification evidence with external-resource locks"
status = "in_progress"
owners = ["mmzen"]
created = "2026-10-01"
updated = "2026-10-01"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen confirmed required commit-bound verification in VREC-IAR-020 with approval of WO-IAR-039. Later assurance and release decisions rely on this validator."
decided_by = "mmzen"

[execution_scope]
paths = [
  "se_harness/engine/validation_evidence.py",
  "tests/test_revision_provenance.py",
  "tests/test_resources.py",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-039.md",
  "docs/engineering/instruction-architecture/evidence/WO-IAR-039/",
  "docs/engineering/instruction-architecture/verification-records/VREC-IAR-020.md",
  "docs/engineering/instruction-architecture/evidence/VREC-IAR-020-evaluator.json",
]

[relations]
implements = ["REQ-IAR-029", "REQ-IAR-031"]
specifications = ["SPEC-IAR-016"]
architecture = ["ARCH-IAR-012", "ADR-IAR-012"]
verification = ["VER-IAR-020", "VER-IAR-022"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-01T17:32:09Z"
decided_by = "mmzen"
reason = "Human mmzen: Approve WO-IAR-039 and required verification. Confirms required commit-bound verification in VREC-IAR-020 and bounded local implementation, checks and preparation. Reviewed draft SHA256 69d239bc74c06df93330c6da34bfec54829951205d4c6294a136afa1137811a8; only confirmed assurance metadata and its explanatory paragraph were added before approval."
scope_paths = ["se_harness/engine/validation_evidence.py", "tests/test_revision_provenance.py", "tests/test_resources.py", "docs/engineering/instruction-architecture/work-orders/WO-IAR-039.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-039/", "docs/engineering/instruction-architecture/verification-records/VREC-IAR-020.md", "docs/engineering/instruction-architecture/evidence/VREC-IAR-020-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-01T17:32:45Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."
+++

# Validate verification evidence with external-resource locks

## Objective and observed defect

A verification record created in a valid minimal installation must remain usable
by the existing validation and lifecycle checks. The installed 0.21.0 candidate
created VREC-QAL-001 in ready on both Windows and Linux, then rejected it with
E012: standard evaluator lock identity is invalid.

The evidence validator accepts only lock schemas 3 and 4 in its evaluator binding.
Minimal installation uses schema 5. Full reproductions are retained under
evidence/WO-IAR-030/integrated-lifecycle-and-migration.json in this domain.
This implementation file is outside the approved active work-order paths.

## Bounded correction and simplicity

Update the existing evaluator-evidence binding to recognize a valid schema-5
external-resource lock. Reuse the existing lock validator before accepting that
identity. Keep version, layout, digest, environment, canonical-evidence and path
checks. Do not accept an arbitrary schema merely because it contains evaluator
fields. Preserve legacy schema-3/4 behavior and existing evidence semantics.

Extend the existing provenance and resource tests. No new command, evidence
format, resource registry, dependency or parallel validator is needed. Do not
change the ordinary origin-version versus full-payload inspection policy.

## Confirmed assurance

Required commit-bound verification, included in VREC-IAR-020 if still unused,
with VER-IAR-020 and VER-IAR-022. Later assurance and release decisions rely on
this validator. Human mmzen confirmed this classification: "Approve WO-IAR-039 and required verification".

## Required verification

1. Preserve the current installed-wheel Windows and Linux failures.
2. Prove that a schema-5 fixture can capture a ready verification record and
   immediately pass validation and its applicable assurance checks. Leave the
   record ready; a passing check is not human acceptance.
3. Retain schema-3/4 acceptance and rejection coverage. Check malformed or unknown
   layouts, mismatched evaluator identity, changed evidence and unsafe evidence
   paths at the existing validation boundary. Refusals must not mutate records.
4. Run the focused resource and provenance suites. Run the full integrated suite
   and distribution validation after the correction. Build an independent wheel
   from the committed candidate and rerun the complete installed lifecycle on
   Windows and Linux, including byte preservation and evidence identity checks.
5. Reassess earlier integrated package and native evidence against the new wheel.
   Rerun affected checks; reuse a result only with retained input-equivalence
   evidence. Do not claim the untested Codex desktop path as passed.

## Authority and exclusions

After approval, execute only this correction, its local checks and commits,
evidence retention, completion and required aggregate verification preparation.
The selected repository remains governed by its released 0.20.1 evaluator;
candidate behavior is exercised only through the separate qualification route.

Do not change accepted definitions, authority rules, gates, the installed harness,
historical records or the inspection policy. Do not reopen completed work orders.
No adoption, credentials change, push, PR, merge, publication or tagging is
authorized. Human verification acceptance remains a separate decision.

## Evidence and completion

Retain commands, environments, exact candidates, outputs, failures and criterion
assessment under the declared WO-IAR-039 evidence prefix. Prepare VREC-IAR-020
only through the released procedure, with all required work orders, contracts
and explicit evidence files, after the integrated criteria and gates pass.
Preserve the earlier failed runs and existing verification records.

Stop affected execution if a correction needs another file, changed behavior,
missing decision or failing required check. Report the exact change, checks,
limitations and the evaluator's next typed step. This draft grants no execution
or assurance authority.
