+++
id = "WO-IAR-025"
type = "work_order"
title = "Correct the CLI note's retired workflow link"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-09-28"
updated = "2026-09-28"

[assurance]
commit_bound_verification = "required"
rationale = "Human-approved commit-bound verification of the instruction link used for retirement and subsequent release review."
decided_by = "mmzen"

[execution_scope]
paths = [
  "docs/notes/harnessctl-reference.md",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-025.md",
  "docs/engineering/instruction-architecture/evidence/WO-IAR-025/",
]

[relations]
implements = ["REQ-IAR-027", "REQ-IAR-028"]
specifications = ["SPEC-IAR-014", "SPEC-IAR-015"]
verification = ["VER-IAR-017"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-28T09:02:41Z"
decided_by = "engineering-owner"
reason = "Human repository owner mmzen: \"Approve WO-IAR-025 and required verification\". Approval includes the reviewed two-line note correction and the existing 0.19.0 engineering-owner encoding. Reviewed draft SHA-256 0660627163ff6ec1322d86d4d30a33be577dcf1a0188d0e44c041428bb918345. Only the supplied assurance decision was added before transition; input SHA-256 36d5023f13187f2e51fd9620c0502ffd6641e05fa12c83be1721a8ca0d042180. Codex applies the human decision."
scope_paths = ["docs/notes/harnessctl-reference.md", "docs/engineering/instruction-architecture/work-orders/WO-IAR-025.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-025/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-28T09:03:09Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed. Codex starts the unchanged approved scope under mmzen's recorded approval after passing start checks."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-28T09:18:21Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded engineering-owner approval; relevant local gates passed. Codex completed the unchanged approved scope. VER-IAR-017 evidence, full Windows/Linux suites, installed-package checks and combined complete-change handoff pass. Human commit-bound verification remains pending."
+++

# Correct the CLI note's retired workflow link

## Objective and observed failure

Keep the CLI reference usable when WO-IAR-022 removes the WORKFLOW.md source
template. The full Linux run completed 1,140 tests and reported one failure:
test_progressive_documentation.ProgressiveDocumentationTests.test_all_local_note_links_resolve
found the missing target from docs/notes/harnessctl-reference.md, line 144.
The note is outside the approved paths of WO-IAR-022 and WO-IAR-024.

## Exact proposed edit

In docs/notes/harnessctl-reference.md, replace:

```markdown
[`WORKFLOW.md`](../../templates/repository/standard/docs/engineering/WORKFLOW.md)
defines the procedure, and
```

with:

```markdown
[`CONTINUE.md`](../../templates/repository/standard/docs/engineering/harness/CONTINUE.md#continue-selected-work)
routes to the selected procedure, and
```

Keep the adjacent WORKFLOW.json link, command arguments, examples and all other
text unchanged. Do not reintroduce a retired template or weaken the link test.

## Scope, authority and stops

The only product edit is the two-line replacement above. No source-code,
test, accepted-definition, installed-instruction, evaluator, host-profile or
historical-evidence change is authorized by this work order.

After approval, apply this edit under the selected released evaluator's normal
start and scope checks. Complete it with WO-IAR-022 and WO-IAR-024. Their existing
authority stays unchanged; this approval supplies only the missing note scope.
No push, PR mutation, merge, release or adoption is included.

Stop if the replacement heading is unavailable or fixing the reported link
requires another path or a change to command meaning. Preserve the initial
failure and any subsequent failures.

## Verification and evidence

Reuse VER-IAR-017 at the combined candidate. Run the unchanged local-note link
test and the full Windows/Linux suite. Preserve the initial Linux failure,
the exact applied diff, the resolved replacement heading and final test results
under evidence/WO-IAR-025/, or explicitly bind shared results retained by
WO-IAR-022 in the same VREC. No additional test or verification contract is needed.

Record completion only after checks pass. Prepare verification bound to the
exact clean candidate, explicitly covering WO-IAR-022, WO-IAR-024 and WO-IAR-025.
Only the human may accept that verification.

## Assurance proposal and completion

Human repository owner mmzen confirmed required commit-bound verification with
"Approve WO-IAR-025 and required verification". The corrected instruction route
supports retirement and later release decisions. The selected 0.19.0
approval encoding is engineering-owner; retain the actual human and decision.

The completion report names the corrected link, actual checks, remaining
limitations, candidate commit and evaluator-selected next typed step.
