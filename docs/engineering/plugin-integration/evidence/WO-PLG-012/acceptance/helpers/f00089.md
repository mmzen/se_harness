+++
id = "WO-ROF-001"
type = "work_order"
title = "Evidence preparation fixture WO"
status = "approved"
owners = ["engineering-owner"]
created = "2026-09-10"
updated = "2026-09-10"

[assurance]
commit_bound_verification = "required"
rationale = "The fixture captures exact committed implementation evidence."
decided_by = "engineering-owner"

[execution_scope]
paths = ["src/feature.py", "docs/engineering/retained-demo/work-orders/WO-ROF-001.md", "docs/engineering/retained-demo/evidence/WO-ROF-001/"]

[relations]
implements = ["REQ-ROF-001"]
specifications = ["SPEC-ROF-001"]
verification = ["VER-ROF-001"]
+++

# Work order

## Objective

Retain the greeting implementation and its actual local evidence.

## In scope

The feature file and this work order's evidence directory.

## Out of scope

Every source worktree and every real external action.

## Authorized decision envelope

Synthetic preexisting engineering-owner approval forms the initial approved read-only test fixture state. They authorize no assurance, release, or external action.

## Stop conditions

Missing authority, unavailable current context, changed inputs or a failed required gate.

## Required verification

Exact greeting assertion, actual installed doctor and selected review preflight.

## Completion report format

Report observed commands, effects, selected state and typed next action.

