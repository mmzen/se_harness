+++
id = "WO-KIS-011"
type = "work_order"
title = "Refresh the diagnostic index for planned-path preparation"
status = "implemented"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"

[assurance]
commit_bound_verification = "required"
rationale = "Engineering review and CI rely on the generated diagnostic reference; the human confirmed required commit-bound verification."
decided_by = "mmzen"

[execution_scope]
paths = [
  "docs/notes/diagnostic-codes.md",
  "docs/engineering/harness-simplification/work-orders/WO-KIS-011.md",
  "docs/engineering/harness-simplification/evidence/WO-KIS-011/",
]

[relations]
implements = ["REQ-KIS-010"]
specifications = ["SPEC-KIS-004"]
verification = ["VER-KIS-004"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T12:20:35Z"
decided_by = "mmzen"
reason = "mmzen replied \"I approve\" to the exact two-line generated-index correction and required commit-bound verification. Reviewed WO SHA-256 63456285024da8f9ddfe8a715f13a929718b72bde32ed062ff5248ec8e46eacd. Pending assurance fields were completed from that decision. This permits local execution and verification preparation; human verification acceptance and implementation publication remain separate."
scope_paths = ["docs/notes/diagnostic-codes.md", "docs/engineering/harness-simplification/work-orders/WO-KIS-011.md", "docs/engineering/harness-simplification/evidence/WO-KIS-011/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-02T12:21:31Z"
decided_by = "Codex agent"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed. Start the approved generated-index correction under mmzen approval; start preflight passed."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-10-02T12:29:01Z"
decided_by = "Codex agent"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed. Regenerated only the two reviewed diagnostic message counts. The generator check, diagnostic assertions in the full passing suite, review preflight and combined-scope handoff passed. Human verification and external delivery remain separate."
+++

# Refresh the diagnostic index for planned-path preparation

## Objective

Keep the generated diagnostic reference consistent with the planned-path
checks introduced by WO-KIS-010, so the full repository checks can pass.

## In scope

Regenerate docs/notes/diagnostic-codes.md from the candidate source using the
existing repository_tools.diagnostic_code_index command. The prepared diff
changes two message counts: WEX200 from 24 to 26 additional messages, and
WEX210 from 16 to 18. No diagnostic code or behavior is changed here.

## Out of scope

No new feature, diagnostic code, generator change, test change, workflow
rule, release or adoption. Preserve the approved WO-KIS-010 and its history.

## Authorized decision envelope

Approval authorizes local regeneration, inspection, checks, commits,
completion and preparation of required commit-bound verification for this
correction. Human verification acceptance and external delivery remain
separate. Use the combined-scope PR check for the complete change from the
original main baseline when both work orders share the branch.

## Constraints

The index was omitted from WO-KIS-010's exact paths. Do not alter approved
scope or suppress diagnostics to avoid this missing path. Reuse the
accepted definitions and VER-KIS-004; no new definition is necessary.
No active architecture addresses REQ-KIS-010.

## Expected change surface

| Path | Reason |
| --- | --- |
| docs/notes/diagnostic-codes.md | Generated reference must match source diagnostics. |
| This work order | Record the human's correction decision and execution. |
| docs/engineering/harness-simplification/evidence/WO-KIS-011/ | Retain regeneration, checks and handoff evidence. |

The generator and its three failing assertions were inspected. The generator,
tests, packaging and CI configuration need no change. Implementation remains
covered by WO-KIS-010. Retain the complete combined diff baseline
ccbfbdec811d722974336924125b070d91f111f4.

A future verification record may cover both work orders at the same exact
candidate. Its actual record and evaluator-evidence paths will be checked
after allocation under the existing relationship admission rule.

## Proposed assurance classification

Propose required commit-bound verification because engineering review and CI
rely on the generated reference. The human must confirm this classification
before the assurance metadata and approval transition are applied.

## Required verification

Run the generator in check mode and the diagnostic-index and compatibility
tests. Run the complete repository suite with the final WO-KIS-010 code.
Inspect the two-line generated diff. Apply VER-KIS-004 to the combined
candidate; retain skips and CI limitations. Use the selected released
evaluator for actual scope, handoff and verification preparation.

## Evidence to record

Retain the generated diff, exact commands, runtime, exit status and test
output. Keep the earlier failed suite under WO-KIS-010. Keep one combined
review; this correction does not require a separate review framework.

## Stop and escalate conditions

Stop if regeneration changes more than the two reviewed message counts or
requires generator, code, test, policy or additional file changes.

## Completion report format

Report the changed counts, checks, remaining limitations and evaluator's
next action. This completion does not accept verification or publish work.
