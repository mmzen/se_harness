+++
id = "WO-KIS-014"
type = "work_order"
title = "Index the review-publication procedure"
status = "implemented"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"

[execution_scope]
paths = [
  "templates/repository/standard/docs/engineering/harness/CONTINUE.md",
  "docs/engineering/harness-simplification/work-orders/WO-KIS-014.md",
  "docs/engineering/harness-simplification/evidence/WO-KIS-014/",
]

[assurance]
commit_bound_verification = "required"
rationale = "Agents rely on the procedure index to discover governed instructions; verification must cover the two index additions with WO-KIS-013."
decided_by = "mmzen"

[relations]
implements = ["REQ-KIS-012"]
specifications = ["SPEC-KIS-006"]
verification = ["VER-KIS-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T15:39:35Z"
decided_by = "mmzen"
reason = "mmzen replied I approve to the reviewed two-row CONTINUE.md index correction, required commit-bound verification under VER-KIS-006 with WO-KIS-013, and the same bounded review-PR publication scope on 2026-10-02. Reviewed bytes after recording confirmed assurance: 0fb45fa5f70b19d56332c92dad0f3d9c2980be1df7892c2d4ef87db050fbfec9"
scope_paths = ["templates/repository/standard/docs/engineering/harness/CONTINUE.md", "docs/engineering/harness-simplification/work-orders/WO-KIS-014.md", "docs/engineering/harness-simplification/evidence/WO-KIS-014/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-02T15:40:44Z"
decided_by = "Codex agent"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed. Start the approved two-row procedure index correction under mmzen approval, with required verification and the bounded review-PR grant."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-10-02T15:48:35Z"
decided_by = "Codex agent"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed. Added exactly two procedure index rows; 55 instruction tests and the shared full suite pass; released preflight and combined Git-derived handoff passed."
+++

# Index the review-publication procedure

## Objective

Keep the human procedure and typed-step indexes aligned with the new
review-publication route delivered by WO-KIS-013.

## In scope

Add the new procedure and typed-step rows to CONTINUE.md, pointing to the
PULL_REQUEST.md review-publication heading. This file was omitted from the
WO-KIS-013 path list. The existing instruction-discovery test requires each
catalogue procedure and step to have its matching index destination.

## Out of scope

No new behavior, decision right, command, gate, startup instruction or change
to the already approved requirement, specification and verification contract.

## Authorized decision envelope

Approval permits this bounded index edit, local checks and commits, completion
and required commit-bound verification together with WO-KIS-013. The proposed
publication grant covers the same work/review-before-verification branch and
PR to main in mmzen/se_harness, including the recorded verification decision.
Merge, force-push, release and installed adoption remain excluded.

## Constraints and expected change surface

Only add the two required index rows. Keep unrelated rows and anchors intact.
Use the exact procedure and step IDs returned by the new catalogue. Do not
relax the index-completeness test to avoid updating the index.

## Required verification

Proposed assurance classification: required. Agents use this index to discover
the governed procedure. Record the actual human's confirmation before applying
approval. Reuse VER-KIS-006 and the combined candidate for WO-KIS-013; no
separate acceptance or duplicate test run is required.

## Evidence to record

Retain the index diff review and applicable check results in
evidence/WO-KIS-014/. Reuse the combined test capture from WO-KIS-013 by explicit
reference. Generate any required handoff outputs at this work order's normal
evidence paths.

## Stop and escalate conditions

Stop if a change beyond these two index rows is needed. Required instruction
discovery and integrity checks must pass.

## Completion report format

Report the two index additions, actual discovery checks and the shared
verification candidate. No installed delivery or merge is inferred.

