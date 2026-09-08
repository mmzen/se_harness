+++
id = "WO-TST-004"
type = "work_order"
title = "Wave 4: one run per test, shared support modules, one retired-surface table, cited pins"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[assurance]
commit_bound_verification = "required"
rationale = "The suite is trusted engineering state: every later handoff, verification and release reading relies on its verdict, so that the verdict on the exact candidate commit equals main's is a fact to bind."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "tests/",
  ".github/workflows/candidate-evidence.yml",
  "docs/notes/ci-pipeline.md",
  "docs/engineering/test-suite/README.md",
  "docs/engineering/test-suite/evidence/",
  "docs/engineering/test-suite/verification-records/",
  "docs/engineering/test-suite/requirements/REQ-TST-004.md",
  "docs/engineering/test-suite/specifications/SPEC-TST-002.md",
  "docs/engineering/test-suite/verification/VER-TST-002.md",
  "docs/engineering/test-suite/work-orders/WO-TST-004.md",
]

[relations]
implements = ["REQ-TST-004"]
specifications = ["SPEC-TST-002"]
verification = ["VER-TST-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-08T12:53:14Z"
decided_by = "engineering-owner"
reason = "Approved on 2026-09-08 by the accountable owner by selecting the presented option 'Approve all four (Recommended)', given after the wave 4 packet for issue #379 (code health assessment 2026-09-07, section 5 and the wave 4 plan) was presented: one run per test, shared support modules, one retired-surface table, cited pins. Approval of a definition authorizes no work. WO-TST-004 carries no delegation class: its start, completion and record preparation are the engineering owner's explicit decisions, after the wave 2 work orders and WO-TCM-011 merge."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-08T13:27:20Z"
decided_by = "engineering-owner"
reason = "Started on 2026-09-08 by the accountable engineering owner with the word 'start' (DR-WO-START), after PR #401 merged the approved packet to main at 13a70218. Start preflight and the start checkpoint passed at that commit with the released 0.16.0 evaluator. The owner starts before the wave 2 work orders (WO-ECP-031, WO-ECP-032, WO-ECP-033, PRs #398 to #400) and WO-TCM-011 merge, accepting the merge burden as the work order's Lifecycle section allows; those branches touch seven test modules and add two. Execution on branch wo/tst-004-test-suite-hygiene within the declared scope only."
+++

# Work Order: Wave 4: one run per test, shared support modules, one retired-surface table, cited pins

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. Commit-bound verification is `required`.

Start preflight runs after `WO-ECP-031`, `WO-ECP-032`, `WO-ECP-033` and
`WO-TCM-011` have merged: all four declare `tests/`, and this work order
edits about forty test modules. The owner may start it earlier in the start
decision's reason and accept the merge burden.

## Objective

Execute rules `TST-HYG-001` to `TST-HYG-020` of `SPEC-TST-002`: every
defined test runs once, five support modules replace the copied helpers, one
table holds the tombstones, un-cited prose pins become structural checks, the
fixture cache collapses to one initialisation, and the hosted suite step
keeps its timings.

## In scope

- The mixin conversion of the inheritance chains measured on 2026-09-08 on
  `main` at `50f9cda5`: four classes in `tests/test_workflow_execution.py`,
  the three-level chain in `tests/test_workflow_compliance.py`, one class
  each in `tests/test_decision_management.py` and
  `tests/test_artifact_authoring_policy.py`. The loader reads 1,029 defined
  and 1,282 discovered today: 253 re-runs.
- The loader-count test.
- `tests/artifact_support.py` from the helpers of
  `tests/test_revision_provenance.py` (13 importing modules today);
  `tests/cli_support.py` with one `invoke` (22 definitions today);
  `tests/git_support.py` with `git` and `init_repository` (12 helpers today,
  four of which turn `commit.gpgsign` off);
  `patch_mutation_authority` in `tests/mutation_guard_support.py`;
  `load_evaluator_module` in `tests/root_identity_support.py`; the 13
  import-time `sys.path` inserts removed.
- `tests/test_retired_surface.py` and the removal of every tombstone
  outside it; the two tests that read another test's source.
- The prose pins in `tests/test_progressive_documentation.py`,
  `tests/test_public_onboarding.py`,
  `tests/test_workflow_documentation_contract.py` and
  `tests/test_instruction_architecture.py`, each cited or converted; the
  three specification-cited tests kept.
- The managed count per root derived at run time; the fixture-count literal
  in `tests/test_fixture_support.py`; the three self-length assertions; the
  mid-file `unittest.main()` in `tests/test_public_onboarding.py`.
- The default fixture project name and the direct `init` calls that only
  need a fresh repository.
- The `--timings` argument of the suite step in
  `.github/workflows/candidate-evidence.yml` and its persistence.
- The measurement in `docs/notes/ci-pipeline.md`; the domain index; this
  work order's evidence packet and its record.

## Out of scope

- Product code under `se_harness/` and `repository_tools/` (waves 2 and 3,
  issues #377 and #378); `scripts/run_tests.py` and the runner's contract in
  `SPEC-TST-001`.
- Every other edit of `.github/workflows/candidate-evidence.yml` (wave 5,
  issue #380).
- `tests/skill_contract_support.py` beyond what the support-module rules
  require.
- Any change to what the suite asserts about product behaviour: a helper
  consolidation keeps every caller's verdict.

## Expected change surface

About forty test modules edited, three support modules created and two
extended, one test module created, one lane line, one note, this packet.

## Evidence to record

`docs/engineering/test-suite/evidence/WO-TST-004/`: the loader counts before
and after, the readings `VER-TST-002` names before and after, the serial and
parallel verdicts, the wall times with their lane ids, `validate` and
`doctor` readings.

## Authorized decision envelope

Mixins versus `__init_subclass__`; helper names beyond those the
specification fixes; the persistence mechanism of the timings file on the
lane; the order of edits and the number of commits.

## Constraints

- No product module and no managed path changes; `doctor` reads the managed
  set unchanged.
- The suite's failure set equals the baseline before completion
  (`TST-HYG-020`); the scale tests and the runner are untouched.
- Every specification-cited pin remains (`TST-HYG-014`).
- The suite, `validate`, `doctor` and the handoff check over the Git-derived
  change set pass before completion.

## Required verification

Execute `VER-TST-002` in full; repository-required checks; the pull
request's lanes; the handoff check; a verification record bound to the
candidate commit.

## Stop and escalate conditions

A helper consolidation that changes a verdict: two copies disagreed and a
test depended on the difference, stop and report. A pin believed cited whose
rule cannot be found: keep it and disclose. Any need to change a product
module, a managed path, or the runner. A merge conflict with a wave 2 branch
that needs a product edit to resolve.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.

## Scope amendment, 2026-09-08

`docs/engineering/test-suite/requirements/REQ-TST-004.md`,
`docs/engineering/test-suite/specifications/SPEC-TST-002.md` and
`docs/engineering/test-suite/verification/VER-TST-002.md` are added to
`[execution_scope].paths`. The managed scope lane reads every pull request
carrying this work order's identifier against the declared scope, the packet
pull request #401 carries the three definitions, and the wave 2 work orders
listed their sibling definitions for that reason; the paths were missed when
the scope was drafted, and the lane refused with `WEX201`. The one purpose of
the widening is that the packet and its later amendment records pass the
lane; the execution of the work order does not edit the definitions except
by dated amendment record. Decided by the accountable engineering owner on
2026-09-08 by selecting the presented option "Widen the scope by amendment
(Recommended)". Nothing else is widened.
