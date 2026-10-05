+++
id = "WO-HAG-004"
type = "work_order"
title = "Transport approved decision-attribution definitions with the review"
status = "implemented"
owners = ["mmzen"]
created = "2026-10-04"
updated = "2026-10-04"

[assurance]
commit_bound_verification = "not_required"
rationale = "mmzen confirmed that this work only transports unchanged approved records and the explicitly authorized review-publication decision. VREC-HAG-002 separately assesses the implemented correction; transport changes no implementation, definitions or bound evidence."
decided_by = "mmzen"

[execution_scope]
paths = ["docs/engineering/hosted-artifact-graph/requirements/REQ-HAG-010.md", "docs/engineering/hosted-artifact-graph/specifications/SPEC-HAG-005.md", "docs/engineering/hosted-artifact-graph/architecture/ARCH-HAG-002.md", "docs/engineering/hosted-artifact-graph/architecture/adr/ADR-HAG-002.md", "docs/engineering/hosted-artifact-graph/verification/VER-HAG-003.md", "docs/engineering/hosted-artifact-graph/evidence/WO-HAG-004/"]

[relations]
implements = ["REQ-HAG-010"]
specifications = ["SPEC-HAG-005"]
architecture = ["ARCH-HAG-002", "ADR-HAG-002"]
verification = ["VER-HAG-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-04T17:41:22Z"
decided_by = "mmzen"
reason = "mmzen explicitly answered Approve scope correction and draft PR update to the exact reviewed WO-HAG-004 request. Approval confirms not_required commit-bound assurance for unchanged record transport only. It grants bounded publication of the WO-HAG-001 continuation, WO-HAG-003 correction, ready VREC-HAG-002 and WO-HAG-004 records to mmzen/se_harness branch codex/hosted-artifact-phase1 and draft PR #535 targeting codex/hosted-artifact-graph-inputs, including a later push of the separately given VREC-HAG-002 decision. Keep the PR draft and disclose open DEC-HAG-001 and its failed gate. This supplies no verification, merge, release, retargeting or live decision-disposition authority."
scope_paths = ["docs/engineering/hosted-artifact-graph/requirements/REQ-HAG-010.md", "docs/engineering/hosted-artifact-graph/specifications/SPEC-HAG-005.md", "docs/engineering/hosted-artifact-graph/architecture/ARCH-HAG-002.md", "docs/engineering/hosted-artifact-graph/architecture/adr/ADR-HAG-002.md", "docs/engineering/hosted-artifact-graph/verification/VER-HAG-003.md", "docs/engineering/hosted-artifact-graph/evidence/WO-HAG-004/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-04T17:42:15Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed. Codex executes only the unchanged record transport under mmzen approval and bounded review-publication grant."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-10-04T17:44:53Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed. Unchanged approved records are prepared for the authorized draft publication. Byte comparisons, review preflight and Git-derived handoff pass. External effects will be confirmed separately."
+++

# Transport approved decision-attribution definitions with the review

## Objective

Include the five approved governing records in the same review as WO-HAG-003.
The combined PR check found their paths absent from the selected work orders.
Their approval is already recorded; no repeat definition approval is sought.

## In scope

Transport the exact five approved files from commit
`6fe137a7c4af08307f3bbe72d4cda6bbefed0617`. Compare their bytes before publication.
Record this work order's own approved execution and retain its scope and
publication observations. Reuse VREC-HAG-002 and its unchanged bound evidence.

## Out of scope

No definition amendment, code change, new test result, new assurance decision,
owner rewrite, live decision disposition, evaluator adoption, release or merge.
The original aggregate `docs/engineering/README.md` scope finding remains a
separate issue. The hosted work remains incomplete.

## Proposed assurance classification

`not_required`: this work only transports existing approval records and the
publication decision requested below. It creates no new implementation claim.
VER-HAG-003 remains the governing verification contract; VREC-HAG-002 is its
separate ready record for WO-HAG-003. A new verification record for transporting
those same decisions is not proposed. The human must confirm this classification.

## Authorized decision envelope, effective only after explicit approval

Local authority covers byte comparisons, scope and preflight checks, this
record's execution transitions, evidence and commits. These operations do not
edit the five approved files or VREC-HAG-002's candidate and evidence.

The accompanying request also proposes one bounded review-publication grant:
repository `mmzen/se_harness`, source `codex/hosted-artifact-phase1`, existing
draft PR #535, target `codex/hosted-artifact-graph-inputs`. Publish the existing
WO-HAG-001 continuation, the approved WO-HAG-003 package and correction,
VREC-HAG-002, this transport record and their retained evidence. The reviewed
content starts at `6fe137a7c4af08307f3bbe72d4cda6bbefed0617`; later additions
are limited to WO-HAG-004 and its packet, plus the actual human decision on
VREC-HAG-002 if separately given. Confirm the full head and complete diff
before each write. No force push, branch retarget or comparison-base change.

This grant includes updating the PR body and a later decision-only push for
VREC-HAG-002. Keep the PR in draft while WO-HAG-001 is unfinished. Its known
QGP-G4I-DECISION failure from open DEC-HAG-001 must remain visible; publication
does not clear it or make the PR mergeable. The request is publication of an
unfinished review/handoff, as in the original handoff authorization, not a
request to accept the failed gate. Any additional uncovered path or changed
failure needs assessment before publication.

## Constraints and expected change surface

| Exact path below docs/engineering/hosted-artifact-graph/ | Purpose |
| --- | --- |
| requirements/REQ-HAG-010.md | Carry the approved outcome unchanged. |
| specifications/SPEC-HAG-005.md | Carry the approved command and attribution rules unchanged. |
| architecture/ARCH-HAG-002.md | Carry the approved component and trust boundary unchanged. |
| architecture/adr/ADR-HAG-002.md | Carry the approved design decision unchanged. |
| verification/VER-HAG-003.md | Carry the approved independent verification contract unchanged. |
| evidence/WO-HAG-004/ | Retain byte comparisons, required checks and actual publication observations. |

This work order's own file and generated packet use existing automatic
admission. Other code, tests, instructions, packaging and CI files belong to
the already approved work; no new implementation change is planned here.
Proposed PR text stays outside the repository until authorized publication.

## Required checks and evidence

Compare the five complete file bytes with the stated committed source.
Confirm VREC-HAG-002's candidate and bound evidence remain unchanged. Run
released validation, start/review preflight, scope and required handoff checks.
Check the combined PR against its original target and retain every finding.
Use the declared ready-record publication route for VREC-HAG-002. Read back
the exact remote head, target and draft state if publication is authorized.
No skipped or failed check becomes a pass through this transport operation.

## Stop conditions

Stop for changed approved bytes, candidate or bound evidence; missing
publication authority; new uncovered paths; or new failed gates. Do not
rewrite WO-HAG-003's approved history or use this record to widen its behavior.

## Completion report

Report byte equality, actual checks, this record's state, publication effects,
the still-open hosted blocker and the evaluator's current next step. Human
verification of VREC-HAG-002 remains a separate decision after remote review.
