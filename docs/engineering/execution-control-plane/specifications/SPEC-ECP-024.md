+++
id = "SPEC-ECP-024"
type = "specification"
title = "Wave 3 engine: one import surface, one validation per command, and the three largest modules split"
status = "draft"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-08"
contract = "The engine is imported, its twins have one definition, each command validates once with outputs byte-identical, and no function exceeds complexity 60."

[relations]
specifies = ["REQ-ECP-035"]
+++

# Specification: Wave 3 engine: one import surface, one validation per command, and the three largest modules split

## In plain words

Three groups, each its own work order. The import surface and the twins;
one validation per command; the splits of the validator, the dashboard and
the compliance module.

## Scope

The package `se_harness/`, including `se_harness/engine/`, and the tests
that load the engine. The tools under `repository_tools/` stay behind the
import barrier of `ARCH-REB-013` and change only where the code index reads
the engine's codes. The lane scripts and the templates are out of scope.
Every rule carries a keyword and an identifier a test can cite.

## Terms

- **Engine.** The validator, the Explorer generator, the inspector and the
  layout registry under `se_harness/engine/`.
- **Twin.** A definition the engine and the package both carry today.
- **Governance command.** A `harnessctl` command that reads the artifact
  graph: `validate`, `preflight`, `check`, `transition`, `evidence`,
  `capture-verification`, `prepare-release`, `doctor`, `inspect`,
  `dashboard`, `decide`, `create-artifact` and the risk commands.
- **Recorded output.** A formal snapshot digest, the dashboard manifest
  digest, a `result_sha256`, or the validator's JSON and human renderings.
- **Seam.** A boundary between validator passes that share only the loaded
  artifacts and the report.

## Rules

**ECP-ENG-001.** `se_harness/engine/` MUST be an importable package whose
modules import their siblings and the package by name, never by path.

**ECP-ENG-002.** Each engine entry module MUST stay runnable as
`python -m se_harness.engine.<name>` with arguments, output formats, exit
codes and diagnostic codes unchanged.

**ECP-ENG-003.** The package MUST import the engine; `preflight`'s path
loader and the four command-line assemblies of `cli.py` MUST go.

**ECP-ENG-004.** `se_harness/artifact_layout.py` MUST be the one definition
of the layout tables, and `engine/artifact_layout_registry.py` MUST go.

**ECP-ENG-005.** The validator MUST read the lifecycle registry through
`workflow_contract.validate_lifecycle_registry`; its copy and the copy in
`tests/test_lifecycle_state_contract.py` MUST go.

**ECP-ENG-006.** One evaluator-evidence validator MUST serve the engine and
`evaluator_evidence.py`, each caller keeping its diagnostics and messages.

**ECP-ENG-007.** The implemented-or-later status set MUST have one
definition in `workflow_contract.py`, checked against the lifecycle registry
at load.

**ECP-ENG-008.** One body parser and one compiled artifact-id pattern MUST
serve the validator, the generator and the package.

**ECP-ENG-009.** `se_harness/codes.py` MUST name the engine's codes, no
engine module MAY spell one, and the index MUST attribute them by name.

**ECP-ENG-010.** Each governance command MUST call `validate_repository` at
most once per invocation, and a command that validates MUST do so exactly
once.

**ECP-ENG-011.** `run_preflight`, the snapshot builder, `provenance` and
`release_qualification` MUST accept the in-process `ValidationReport` and
MUST NOT re-parse artifact TOML.

**ECP-ENG-012.** `doctor` MUST obtain its `W013` layout warnings without
running the graph validation passes.

**ECP-ENG-013.** `inspect` MUST derive its queues and findings from one
validation and the in-process snapshot, writing no Explorer bundle.

**ECP-ENG-014.** One skew classifier MUST serve `preflight` and
`check --checkpoint start`, so an artifact the check admits is not refused
by preflight.

**ECP-ENG-015.** `capture-verification` and `prepare-release` MUST build the
snapshot from the validation they already hold.

**ECP-ENG-016.** Every recorded output MUST be byte-identical before and
after each group on this repository, measured at each group's completion.

**ECP-ENG-017.** The validator MUST be split along its eight seams into
engine modules, the orchestrator staying in the entry module.

**ECP-ENG-018.** The generator MUST be split at `build_snapshot` and
`build_dashboard_bundle` into snapshot, bundle and entry modules.

**ECP-ENG-019.** `workflow_compliance.py` MUST be split into change-set,
evidence-packet and predicate modules, and the `workflow` cycle MUST go.

**ECP-ENG-020.** `_classify`, `_diagnostic`, `project_scope`, `_catalog`,
`_validation` and `_family` MUST each have one public home.

**ECP-ENG-021.** No module in `se_harness/` MAY import an underscore-private
name from another module of the package.

**ECP-ENG-022.** No function in the package MAY exceed cyclomatic complexity
60 as `radon cc` measures it.

**ECP-ENG-023.** No recorded digest MAY change: recipes, locks, evidence
bindings, `CONTRACT_SHA256` and every digest pin MUST equal `main`'s.

**ECP-ENG-024.** The contract JSON files and the candidate templates MUST
NOT change bytes under this specification.

**ECP-ENG-025.** Where an approved specification names the subprocess launch,
the path load or an engine twin as operative, it MUST receive a dated
amendment record naming this specification.

**ECP-ENG-026.** The suite's failure set MUST equal the baseline, and
`validate`, `doctor` and the hosted lanes MUST pass at every head.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| an engine module is missing from the installation | the import fails as an installation defect before the target is read (ECP-ENG-001, DST-ENG-005) | the caller's code |
| a command validates twice | the counting test names the command (ECP-ENG-010) | none |
| a recorded output differs from `main`'s | the comparison names the output and the group stops (ECP-ENG-016) | none |
| a function exceeds complexity 60 | the complexity test names it (ECP-ENG-022) | none |
| a module imports a private name across modules | the import test names both modules (ECP-ENG-021) | none |
| an engine module spells a code | the registry test names the module (ECP-ENG-009) | none |

## Examples

**Given** the candidate after group A, **when** `harnessctl validate` runs,
**then** the validator is imported and its human rendering equals `main`'s
byte for byte (ECP-ENG-003, ECP-ENG-016).

**Given** the candidate after group B, **when** `check --checkpoint start`
runs under a patch counting `validate_repository`, **then** the count is one
(ECP-ENG-010).

**Given** the candidate after group C, **when** `radon cc` runs over the
package, **then** no function reads above 60 (ECP-ENG-022).

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-ECP-035` | ECP-ENG-001, ECP-ENG-002, ECP-ENG-003, ECP-ENG-004, ECP-ENG-005, ECP-ENG-006, ECP-ENG-007, ECP-ENG-008, ECP-ENG-009, ECP-ENG-010, ECP-ENG-011, ECP-ENG-012, ECP-ENG-013, ECP-ENG-014, ECP-ENG-015, ECP-ENG-016, ECP-ENG-017, ECP-ENG-018, ECP-ENG-019, ECP-ENG-020, ECP-ENG-021, ECP-ENG-022, ECP-ENG-023, ECP-ENG-024, ECP-ENG-025, ECP-ENG-026 |

## Not decided here

- The names of the new engine and compliance modules, provided the entry
  modules keep their names and their `main()`.
- Whether the layout registry module is deleted or left as a re-export for
  one release, provided the tables have one definition.
- Which property of the lifecycle registry checks the status set, provided
  the three states are checked at load.
- Whether the three groups land as one stacked series or three independent
  pull requests; group A unblocks the other two.
