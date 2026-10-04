+++
id = "WO-RLS-043"
type = "work_order"
title = "Handle absent draft evidence in transition snapshots"
status = "draft"
owners = ["mmzen"]
created = "2026-10-04"
updated = "2026-10-04"

[execution_scope]
paths = ["se_harness/workflow.py", "tests/test_workflow_execution.py", "docs/engineering/release-0-22-1/"]

[relations]
implements = ["REQ-WEX-002"]
specifications = ["SPEC-WEX-001"]
architecture = ["ARCH-WEX-001", "ADR-WEX-001"]
verification = ["VER-RLS-004"]
+++

# Handle absent draft evidence in transition snapshots

## Objective and observed defect

An authorized transition must retain its existing atomic checks without crashing
because an unrelated draft names evidence that has not been produced.
The native Claude walkthrough found this defect in the exact 0.22.1 wheel.
Independent Windows and Linux probes confirm it: validation and start preflight
pass; the start preview raises FileNotFoundError and changes no file.

## In scope

Correct the existing input snapshot and stale-input comparison. Record absent
declared evidence as absence; do not create a file or forget the input. Recheck
that absence before apply, as existing bytes are rechecked. Evidence required
by the selected action must still pass its existing gates. Use the existing
structured workflow failure path for relevant filesystem read errors. An
unreadable file is not an absent file.

Add regression tests and actual installed-package probes. Requalify changed
release inputs through WO-RLS-040/041, keeping original failed observations.
Reuse PlannedInput, plan_transition and apply_transition; no new framework.

## Out of scope

No lifecycle edge, decision right, schema, public option, graph rule, evidence
waiver, dependency or host behavior changes. Do not remove the failing draft or
invent its evidence. No hosted service, HAG ownership/pin changes, provider
settings, release publication, adoption or merge.

## Proposed authority and assurance

This draft grants no execution authority. Propose required commit-bound
verification because later lifecycle and release decisions rely on this code.
The human must confirm the classification; no assurance decision is recorded.

After approval, Codex may implement, test, commit locally and prepare verification
within this scope. Propose review pushes and updates to existing draft PR #536,
mmzen/se_harness:codex/release-0-22-1 to main, including a later separately given
verification decision. No force push, protection bypass or merge.

REL-SEH-035 currently excludes this work order. Its exact linked amendment is
presented separately in the review request. Released 0.22.0 has no supported
definition-revision command. Preserve the accepted record unless the human
explicitly authorizes the reviewed manual amendment, its preserved accepted
bytes and revision link. Ordinary work approval alone is not that exception.

## Constraints

Released 0.22.0 governs outside the checkout. Candidate packages are tested in
isolation. Preserve path safety, full input coverage, exact-byte comparison,
selected writes, required gates and rollback. Treat only FileNotFoundError as
absence; directories, unsafe links and permission errors must not become absence.

## Expected change surface

| Path | Purpose |
| --- | --- |
| se_harness/workflow.py | Existing input snapshot and atomic apply boundary. |
| tests/test_workflow_execution.py | Extend existing CLI, stale-input and rollback tests. |
| docs/engineering/release-0-22-1/ | This package, correction evidence under evidence/WO-RLS-043/, release qualification evidence, generated verification companions, and the separately authorized REL amendment/preserved accepted bytes if approved. |

The inspected CLI already converts HarnessError to a structured failure. No
CLI grammar, templates, installer, dependency, builder, plugin source or CI edit
is needed. ARCH-WEX-001/ADR-WEX-001 still apply; no structural decision changes.
VREC IDs remain unresolved until capture; assess actual returned record and
fixed evaluator-evidence paths before writes. This domain covers those bounded
qualification outputs, not unrelated product work.

## Required verification and evidence

Follow VER-RLS-004. Retain commands, runtimes, raw failures/recoveries, source and
archive identities, before/after digests, review and handoff under
evidence/WO-RLS-043/. Original native and independent failed-wheel observations
remain under evidence/WO-RLS-041/. Rebuild changed archives/packages and rerun
affected final qualification. Do not relabel earlier results as new-byte tests.

## Stop conditions and completion

Stop on changed policy, required evidence rules, uncovered implementation files
or lost stale-input/atomicity guarantees. Desktop/provider gaps remain pending;
this correction approval accepts no omission. Report the exact candidate,
observed checks, original failures, remaining release criteria and evaluator
next step. Completion is not verification or release.
