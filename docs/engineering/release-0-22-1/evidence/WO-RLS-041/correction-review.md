# Correction needed before release qualification can complete

The real Claude walkthrough found a transition-planning defect in preparation
source `89c69748fcc5fc2578acef5cbf48f0734ef1b732`, wheel
`0a9f87f235839689dbbca3b10013b5df2a71dc134b53795248f78de8e1cfec49`.
An unrelated unapproved draft declares evidence that will be written later.
Validation and start preflight pass, but starting a separate approved work order
crashes when the planner snapshots that absent file. No file changes occur.

The failure is reproduced with the installed wheel on
[Windows](missing-evidence-windows.json) and [Linux](missing-evidence-linux.json).
The native trace, unsuccessful attempts and independent readback remain in
[native-walkthroughs.zip](native-walkthroughs.zip). The second Claude checkout
cycle is pending, not passed. Codex's two completed walkthroughs used drafts
without that optional evidence declaration and do not disprove this failure.

## Proposed bounded correction

[WO-RLS-043](../../work-orders/WO-RLS-043.md) and
[VER-RLS-004](../../verification/VER-RLS-004.md) reuse accepted REQ-WEX-002,
SPEC-WEX-001 and ARCH-WEX-001/ADR-WEX-001. Both records remain draft.

- Change `se_harness/workflow.py` to capture absence explicitly and recheck it
  before apply. Preserve existing bytes, input coverage, path safety and rollback.
- Extend `tests/test_workflow_execution.py` for the real case, appearance or
  disappearance between plan/apply, missing required evidence and read failures.
- Run installed Windows/Linux probes and resume the failed native scenario
  without removing the draft or creating dummy evidence. Requalify changed
  release inputs and retain original evidence with its original identities.

No new lifecycle, authority, schema, dependency, plugin, CI or installer behavior
is proposed. Required evidence remains required. No product code has changed.

## Authority and release inclusion

WO-RLS-040 authorizes integration of the already-reviewed fixes and explicitly
excludes new product corrections. A new work approval is therefore needed.
Proposed assurance is required and tied to the exact commit. Approval would
also extend the bounded review publication grant to this correction in PR #536.
Verification, merge, complete release and adoption remain separate.

REL-SEH-035 still selects the original five work orders. Its proposed amendment
adds WO-RLS-043 and VER-RLS-004 to the final aggregate qualification while retaining
versions, destinations and every other release condition. The exact proposed
diff is in the PR review request; it remains transient and unapplied. The selected
release has no supported linked-revision command, so applying that amendment
requires explicit human authority for the reviewed manual revision and preservation
of the accepted bytes. Ordinary correction approval must not imply this exception.

The correction drafts validate with zero errors and 61 existing warnings. Eight
planned paths are submitted to the released evaluator for scope assessment.
Preparation and these passing planning checks are not approval or verification.

Codex Windows desktop evidence, PyPI Trusted Publisher confirmation and the
separate live reviewer-setting change remain unresolved. This correction
proposal accepts none of those omissions.
