+++
id = "WO-ECP-036"
type = "work_order"
title = "Wave 3, group C: the validator, the generator and the compliance module split along their seams"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[assurance]
commit_bound_verification = "required"
rationale = "This group moves most of the engine's and the compliance module's code into new modules and removes the workflow cycle; that every recorded output is byte-identical on the unchanged graph is a fact every later gate reading relies on, so verification binds the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/",
  "repository_tools/diagnostic_code_index.py",
  "docs/notes/diagnostic-codes.md",
  "tests/",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/decisions/",
  "docs/engineering/execution-control-plane/evidence/",
  "docs/engineering/execution-control-plane/verification-records/",
  "docs/engineering/execution-control-plane/requirements/REQ-ECP-035.md",
  "docs/engineering/execution-control-plane/specifications/",
  "docs/engineering/execution-control-plane/verification/VER-ECP-026.md",
  "docs/engineering/execution-control-plane/work-orders/WO-ECP-036.md",
  "docs/engineering/workflow-execution/specifications/",
]

[relations]
implements = ["REQ-ECP-035"]
specifications = ["SPEC-ECP-024"]
verification = ["VER-ECP-026"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-08T15:14:16Z"
decided_by = "engineering-owner"
reason = "Approved on 2026-09-08 by the accountable owner by selecting the presented option 'Approve all six (Recommended)', given after the stacked packet pull requests #404, #405 and #406 and their summary were presented: wave 3 of the code health assessment of 2026-09-07 (issue #378) and the revisit triggers of DEC-ECP-001 and DEC-ECP-002, the engine as an import surface, one validation per governance command, the three largest modules split along their seams, every recorded output byte-identical. Approval of a definition authorizes no work."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-08T18:17:07Z"
decided_by = "engineering-owner"
reason = "Started on 2026-09-08 by the accountable engineering owner, by selecting the presented option 'Complete, prepare the record, start group C' after WO-ECP-035 was marked implemented and VREC-ECP-039 prepared at ebd60b10: wave 3, group C, the validator, the generator and the compliance module split along their seams (SPEC-ECP-024 ECP-ENG-016 to ECP-ENG-026). Start preflight PASS. Stacked on the group B branch because the groups edit the same modules."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-08T19:41:11Z"
decided_by = "engineering-owner"
reason = "Completed on 2026-09-08 by the accountable engineering owner, by selecting the presented option 'Complete and prepare the record' after the handoff evidence packet (7edf17b3: 43 changed paths, every gate predicate passing, complete) and the green lanes of PR #414 were presented: the validator, the generator and the compliance module split along their seams, the workflow graph and edge names given public homes, the workflow cycle gone, no private cross-module import, no function above complexity 60, every recorded output byte-identical to the group B code at the same revision (SPEC-ECP-024 ECP-ENG-016 to ECP-ENG-026)."
+++

# Work Order: Wave 3, group C: the validator, the generator and the compliance module split along their seams

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. Commit-bound verification is `required`.

## Objective

Execute rules `ECP-ENG-016` to `ECP-ENG-026` of `SPEC-ECP-024`: the
validator split along its eight seams, the generator at its two builders,
`workflow_compliance.py` into three modules with the `workflow` cycle gone;
no private name imported across modules; no function above complexity 60;
every recorded output byte-identical.

## In scope

- `se_harness/engine/`: the validator's passes in modules named by seam
  (lifecycle, authoring, evidence, revision, architecture, decisions,
  layout, report), the orchestrator and `main()` staying in
  `validate_engineering_artifacts.py`; the generator's snapshot and bundle
  builders in their own modules, `main()` staying.
- `workflow_compliance.py` split into change-set, evidence-packet and
  predicate modules; `_classify`, `_diagnostic`, `project_scope`,
  `_catalog`, `_validation` and `_family` given one public home; the lazy
  imports between `workflow` and `workflow_compliance` gone.
- The eleven functions above complexity 60 reduced below it, each by
  extraction along a seam it already has.
- Tests: the import inventory (no private cross-module name), the complexity
  reading, the module-size readings; test modules following moved names.
- The index attributing codes in the new modules; the page regenerated.
- Amendment records on any approved specification `ECP-ENG-025` reaches.
- The domain index, this work order's evidence packet and its record.

## Out of scope

- The import surface and the twins (group A, `WO-ECP-034`); the number of
  validations per command (group B, `WO-ECP-035`).
- Any change to an engine argument, output format, exit code or diagnostic
  code, message or order; any contract JSON or template byte.
- Any behaviour change: this group moves code and changes none.

## Expected change surface

About ten new modules under `se_harness/engine/` and `se_harness/`; the
three largest modules reduced to their entry points; about thirty lazy
imports removed; tests following the moved names; this packet.

## Evidence to record

`docs/engineering/execution-control-plane/evidence/WO-ECP-036/`: the
`radon cc` readings before and after, the private-import inventory before
and after, the lazy-import count, the module-size readings, the
byte-identity readings at the base and at the candidate, the duplication
scan readings, the suite reading, `validate` and `doctor` readings.

## Authorized decision envelope

The names of the new modules; the order of the extractions; which of two
homes a shared helper takes when the specification names none; whether the
group lands as one commit or several.

## Constraints

- No managed path moves; `doctor` reads the managed set unchanged.
- No contract JSON byte and no candidate template byte changes
  (`ECP-ENG-024`); every recorded digest equals `main`'s (`ECP-ENG-023`).
- Every recorded output byte-identical at completion (`ECP-ENG-016`).
- `repository_tools` imports nothing from `se_harness` (`ARCH-REB-013`).
- The suite, `validate`, `doctor` and the handoff check over the Git-derived
  change set pass before completion.

## Required verification

Execute `VER-ECP-026` in full for this group; repository-required checks;
the pull request's lanes; the handoff check; a verification record bound to
the candidate commit.

## Stop and escalate conditions

A recorded output or digest that differs from `main`'s; a function that
cannot be brought below 60 without changing behaviour: stop and report; a
need to change an engine argument, output, exit code or diagnostic; a rule
that cannot be met as written, which is a deviation decision in this
domain's `decisions/`.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
