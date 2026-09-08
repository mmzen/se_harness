+++
id = "WO-ECP-034"
type = "work_order"
title = "Wave 3, group A: the engine as an import surface and its twins folded into the package"
status = "draft"
owners = ["engineering-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[assurance]
commit_bound_verification = "required"
rationale = "This group changes how every governance command loads the validator, the generator and the inspector, and removes five twin definitions the engine and the package both carried; that every recorded output is byte-identical on the unchanged graph is a fact every later gate reading relies on, so verification binds the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/engine/",
  "se_harness/artifact_layout.py",
  "se_harness/cli.py",
  "se_harness/codes.py",
  "se_harness/evaluator_evidence.py",
  "se_harness/front_matter.py",
  "se_harness/installer.py",
  "se_harness/preflight.py",
  "se_harness/provenance.py",
  "se_harness/release_qualification.py",
  "se_harness/risks.py",
  "se_harness/workflow.py",
  "se_harness/workflow_compliance.py",
  "se_harness/workflow_contract.py",
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
  "docs/engineering/execution-control-plane/work-orders/WO-ECP-034.md",
  "docs/engineering/harness-distribution/specifications/",
  "docs/engineering/instruction-architecture/specifications/",
]

[relations]
implements = ["REQ-ECP-035"]
specifications = ["SPEC-ECP-024"]
verification = ["VER-ECP-026"]
+++

# Work Order: Wave 3, group A: the engine as an import surface and its twins folded into the package

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. Commit-bound verification is `required`.

## Objective

Execute rules `ECP-ENG-001` to `ECP-ENG-009`, `ECP-ENG-016` and
`ECP-ENG-023` to `ECP-ENG-026` of `SPEC-ECP-024`: `se_harness/engine/`
becomes an importable package the CLI, `preflight`, `workflow`,
`provenance` and `release_qualification` import; the five twins have one
definition; the engine's codes join the registry; every recorded output is
byte-identical.

## In scope

- `se_harness/engine/`: sibling imports by `se_harness.engine.<name>`, the
  validator's path load of the layout registry replaced by an import of
  `se_harness.artifact_layout`, each entry module runnable as
  `python -m se_harness.engine.<name>`; the `__init__` docstring states the
  import surface.
- `preflight._load_validator_module` retired; `workflow._validation`, the
  CLI's `validate`, `dashboard`, `inspect` and `doctor` handlers,
  `provenance._validation_catalog` and `_generate_snapshot`, and
  `release_qualification._validator_report` call the engine in-process.
- The twins: `engine/artifact_layout_registry.py` gone; the validator's
  `LifecycleStatePolicy` loader replaced by
  `workflow_contract.validate_lifecycle_registry`; one evaluator-evidence
  validator; the implemented-or-later status set in `workflow_contract.py`;
  one body parser and one artifact-id pattern.
- The engine's diagnostic codes in `codes.py`; the index attributing them
  by name; the page regenerated and compared.
- Amendment records on `SPEC-DST-025` (`DST-ENG-003`, `DST-ENG-006`) and on
  any other approved specification `ECP-ENG-025` reaches.
- Tests: the fourteen modules that load the engine by path import it; the
  hand-written lifecycle copy in `tests/test_lifecycle_state_contract.py`
  retired; the byte-identity comparison; the import-surface inventory.
- The domain index, this work order's evidence packet and its record.

## Out of scope

- Any change to the number of validations a command performs (group B,
  `WO-ECP-035`); any split of a module (group C, `WO-ECP-036`).
- Any change to an engine argument, output format, exit code or diagnostic
  code, message or order; any contract JSON or template byte.
- The lane scripts under `scripts/` and `.github/scripts/`.

## Expected change surface

The four engine modules and the package modules that load them, about
fourteen; one module removed; fourteen test modules touched at their loader;
two or three amendment records; the code page regenerated; this packet.

## Evidence to record

`docs/engineering/execution-control-plane/evidence/WO-ECP-034/`: the loader
grep before and after, the twin inventory before and after, the
byte-identity readings (formal snapshot digests, the dashboard manifest,
`result_sha256` on three artifacts, `validate --json` and the human
rendering) at the base and at the candidate, the duplication scan readings,
the regenerated page comparison, the suite reading, `validate` and `doctor`
readings.

## Authorized decision envelope

The order of edits inside the group; whether the layout registry module is
deleted or left as a re-export for one release; which lifecycle property
checks the status set; helper names beyond those the specification fixes;
whether the group lands as one commit or several.

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

A recorded output or digest that differs from `main`'s; a suite failure
beyond the baseline that a fold explains: two twins disagreed and a caller
depended on the difference, stop and report; a need to change an engine
argument, output, exit code or diagnostic; a rule that cannot be met as
written, which is a deviation decision in this domain's `decisions/`.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
