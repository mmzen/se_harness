+++
id = "SPEC-KIS-003"
type = "specification"
title = "Make approved execution the single route"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-14"
updated = "2026-09-14"

[relations]
specifies = ["REQ-KIS-009"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-14T20:38:27Z"
decided_by = "technical-owner"
reason = "The owner requested the delegated route as the only route, reviewed the complete proposal and accepted it with \"yes: go\" on 2026-09-14. Record technical-owner approval of SPEC-KIS-003 for that bounded scope, including its retained acceptance boundaries and prospective adoption. No completion, verification, merge, release or live adoption result is inferred."
+++

# Make approved execution the single route

## Rules

- **KIS-EXE-001:** New WO approval expressly authorizes start, approved implementation,
  local edits/commits/checks/evidence, completion recording and required VREC preparation.
  Approval leaves the WO approved until the executor applies start. Only selected eligible
  WOs proceed. Honor the existing assurance classification and dependencies.
- **KIS-EXE-002:** Human and agent executors use one authorization check and existing
  transition/capture commands. Check the recorded engineering-owner approval and unchanged
  approved scope for every executor, independent of the supplied actor name. A status or
  actor label alone is not approval. Record the actual supplied actor. The executor role
  grants none of the reserved definition, assurance, release or external decision rights.
- **KIS-EXE-003:** Remove optional delegation from new templates and runtime route selection.
  Keep historical fields readable with their recorded meaning. New approvals record scope
  in their existing event, without the legacy delegation-class field. Old events with
  explicit execution delegation already authorize these three operations; other old events
  need an explicit approval of remaining work through the existing amendment process.
  Do not fabricate historical grants, add approval receipts or retain a second execution engine.
- **KIS-EXE-004:** Workflow recommendations directly describe the executor procedure and
  its actual local checks. Remove the owner-result delegation overlay/fallback. Failure
  reports the affected missing approval or condition; it never offers an owner bypass.
  No local authorization depends on a PR-base merge or live CI. Integration/publication
  checks still apply to those actions.
- **KIS-EXE-005:** Capture accepts its existing explicitly selected WO list for any executor.
  Check approval, scope, eligibility, verification coverage and evidence for every selected
  WO. Remove the delegated-only one-WO limit. Do not add automatic batching or selection.
- **KIS-EXE-006:** DECISION_RIGHTS owns the approval meaning; WORKFLOW.json and WORKFLOW.md
  own ordering and executable next steps. Update their template, instructions, common change
  and evidence skills and current notes together. Skills read installed policy and follow
  its results without duplicating version-specific PR-base/CI rules or requesting already
  granted execution rights. Reuse existing tests and normal review evidence.
- **KIS-EXE-007:** Completion does not verify work. Preparing a VREC leaves it ready.
  Owner scope changes, assurance, release and external actions remain explicit. Existing
  authority for a concrete delivery action is reused; execution itself grants no merge or
  publication. Project-required role separation remains applicable within the same procedure.

## Compatibility and implementation limits

This scope replaces optional execution-class and owner-route behavior in SPEC-ECP-006,
SPEC-ECP-003/017 and their workflow procedures; it extends KIS-CUT-005/006 of SPEC-KIS-001
without restoring CI authorization. Historic records and unrelated decisions are unchanged.
Existing operation IDs may remain stable; they do not select a second execution mode.
An existing approval event distinguishes prospectively granted execution from old grants;
do not add a new configuration mode, lifecycle state, service, signature or receipt.
Ship candidate policies through normal release/adoption. The current real repository
continues using its installed 0.17.0 governor until an authorized adoption.

## Example

After the owner approves a selected hook simplification, the executor performs it, runs
the agreed checks, records completion and prepares required verification. The owner then
accepts or rejects the result. A new out-of-scope behavior needs a scope decision; an
in-scope test repair does not require renewed execution permission.
