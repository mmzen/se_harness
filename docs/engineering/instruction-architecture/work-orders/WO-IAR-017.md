+++
id = "WO-IAR-017"
type = "work_order"
title = "Align regression coverage with the approved instruction evolution"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-09-27"
updated = "2026-09-27"

[assurance]
commit_bound_verification = "required"
rationale = "Proposed classification for human review: future acceptance relies on regression and fixture correctness."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "tests/",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-017.md",
  "docs/engineering/instruction-architecture/evidence/WO-IAR-017/",
]

[relations]
implements = ["REQ-IAR-022", "REQ-IAR-023", "REQ-IAR-024", "REQ-IAR-025", "REQ-IAR-026", "REQ-IAR-027"]
specifications = ["SPEC-IAR-014"]
verification = ["VER-IAR-014"]
architecture = ["ARCH-IAR-011", "ADR-IAR-011"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-27T08:45:51Z"
decided_by = "engineering-owner"
reason = "Human decision: I approve, answering the explicit request to approve WO-IAR-017. Apply the reviewed test-only scope and required assurance classification; no production or external delivery scope added."
scope_paths = ["tests/", "docs/engineering/instruction-architecture/work-orders/WO-IAR-017.md", "docs/engineering/instruction-architecture/evidence/WO-IAR-017/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-27T08:46:19Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed. Execute the human-approved test-only regression correction under the recorded WO-IAR-017 approval."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-27T08:58:53Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded engineering-owner approval; relevant local gates passed. Completed the approved test-only correction. Full-scale suite: 1118 tests, no failures or errors, 16 skips; released Git-derived handoff passed. Broader host/platform qualification remains outside this completion."
+++

# Align regression coverage with the approved instruction evolution

## Objective

Update the existing regression suite for the accepted instruction layout,
discovery fields, owner-only AGENTS and host delivery. This is the concrete
work order for the pending test-only scope proposal. It is not approved.
The assurance classification above is proposed for the same human decision.

## In scope

Change only tests and fixtures whose expectations are affected by
SPEC-IAR-014. Replace assertions for retired routes with assertions for the
accepted current route. Preserve archived release expectations and prior
skill identity vectors; record successor vectors rather than rewriting
historical evidence. Keep fresh-install and prior-release fixtures distinct.

The tests/ component scope reflects the observed distribution of installer,
preflight, provenance, artifact, policy, skill and lifecycle regressions.
It does not authorize unrelated test maintenance or weaker acceptance.

## Dependencies and constraints

Use WO-IAR-013 through WO-IAR-016's implementation and VER-IAR-014. Expected
behavior comes from the accepted specification and independent fixtures,
not copied candidate output. Preserve lifecycle states, exact command
arguments, required gates, decision authority, owner-byte preservation,
refusal-before-write and transactional recovery assertions.

## Out of scope

No production code, changed product requirements, accepted history edits,
installed repository policy or lock edits, host settings, release build,
push, PR, merge, publication or self-adoption. Do not disable failing tests,
weaken a gate or remove unrelated coverage to obtain a passing result.

## Authorized decision envelope

If approved, choose the smallest necessary regression and fixture changes.
Routine scoped implementation, checks, local commits, completion and
verification preparation require no duplicate approval. Human verification
acceptance remains separate. This draft grants no execution authority.

## Required verification

Run each affected test module, then the canonical full test runner at full
scale. Retain failures as well as corrected reruns. Confirm historical vectors
remain unchanged and new expectations cover the accepted behavior. Apply
released validation, scoped preflight and handoff checks before completion.

## Evidence and completion

Retain actual commands, exit codes, changed test paths, input identities,
coverage rationale and limitations in ../evidence/WO-IAR-017/. Prepare any
VREC through the supported evaluator procedure at the exact candidate commit.

## Stop conditions

Stop on scope expansion, an implementation defect requiring a new production
path, changed accepted semantics, unavailable required evidence, or failed
required checks. Report the bounded blocker and preserve earlier evidence.
