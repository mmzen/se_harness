+++
id = "SPEC-DST-025"
type = "specification"
title = "Evaluator scripts ship inside the package, not in the repository template"
status = "draft"
owners = ["technical-owner"]
created = "2026-09-06"
updated = "2026-09-06"
contract = "The evaluator ships its validator, Explorer generator and inspector inside the package, installs none of them into a repository, and upgrades remove earlier copies."

[relations]
specifies = ["REQ-DST-070"]
+++

# Specification: Evaluator scripts ship inside the package, not in the repository template

## In plain words

The five evaluator files that every repository received under its scripts
directory now live only inside the installed package. The two shell wrappers
beside them are retired, and an upgrade removes the old copies.

## Scope

This contract covers where the five evaluator files live in the wheel and
how the evaluator finds them. It covers what the installer writes and what an
upgrade does to earlier installations. The scripts keep their form as
standard-library programs run in a subprocess. Making them importable
modules is a later packet, complexity audit item #225.

## Terms

Evaluator script: `validate_engineering_artifacts.py`,
`generate_harness_dashboard.py`, `inspect_engineering_artifacts.py`,
`artifact_layout_registry.py` or `harness_explorer/index.template.html`.
Engine directory: the directory inside the package that holds them. Retired
copy: one of the eight `scripts/` paths a prior lock records and the current
template no longer contains.

## Rules

**DST-ENG-001.** The directory `templates/repository/standard/scripts/` MUST
be removed, and the `data-files` table MUST carry no `scripts` entry.

**DST-ENG-002.** The standard template manifest MUST list no target under
`scripts/`.

**DST-ENG-003.** The five evaluator scripts MUST ship once, as package data
under one engine directory inside `se_harness`, and nowhere under `share/`.

**DST-ENG-004.** The evaluator MUST resolve an evaluator script from its own
package directory, never from the target, the working directory or a
`share/` prefix.

**DST-ENG-005.** A missing evaluator script MUST be reported as an
installation defect before the target is read.

**DST-ENG-006.** Each script MUST still run as a subprocess of
`sys.executable` with its own directory first on `sys.path`, so the sibling
imports keep working.

**DST-ENG-007.** Script arguments, output formats, exit codes and diagnostic
codes MUST NOT change.

**DST-ENG-008.** `select_harness_work_order.py` MUST be deleted without
replacement; the `select-work-order` command is the interface.

**DST-ENG-009.** `check_engineering_harness.sh` and
`check_engineering_harness.ps1` MUST be deleted; `harnessctl validate` and
`harnessctl dashboard` are the documented equivalents.

**DST-ENG-010.** Any hard-coded managed or required path list in the
evaluator MUST name no `scripts/` path.

**DST-ENG-011.** An upgrade MUST plan a byte-identical retired copy as
`remove` and a differing copy as `customized`, under the existing
leaving-set rule.

**DST-ENG-012.** A `customized` retired copy MUST block the upgrade
transaction with nothing written.

**DST-ENG-013.** After an upgrade the written lock MUST carry no retired
`scripts/` entry, and a fresh installation MUST produce the same file set.

**DST-ENG-014.** This work MUST NOT change this repository's hash-locked root
`scripts/` files or its lock.

**DST-ENG-015.** The root-adoption work order for the carrying release MUST
update AGENTS.md lines 9, 32 and 34 and the managed-path count in
`SPEC-IAR-012`.

**DST-ENG-016.** That adoption work order MUST switch
`release-qualification.yml`, `release-candidate-replay.yml` and
`pages-publication.yml` from root scripts to evaluator commands.

**DST-ENG-017.** The installation note and the developing note MUST describe
the package as the only home of the evaluator scripts.

## Failure behaviour

A `customized` entry is reported with its path, and the transaction refuses
without writing. The owner restores the recorded bytes or removes the file
under their own authority, then re-runs. A missing evaluator script raises the
existing missing-distribution-script error and exits non-zero before the
target is opened. A `scripts/` target in the manifest, or a
`share/.../scripts/` member in the wheel, is a defect that fails the
packaging tests.

## Examples

A wheel listing with `se_harness/<engine dir>/validate_engineering_artifacts.py`
and no `share/se-harness/templates/repository/standard/scripts/` member
conforms. An upgrade plan from a 0.15.0 installation showing eight `remove`
actions conforms. A plan that deletes a differing copy does not. A `doctor`
run on a fresh installation that lists a `scripts/` check does not.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-DST-070` | DST-ENG-001, DST-ENG-002, DST-ENG-003, DST-ENG-004, DST-ENG-005, DST-ENG-006, DST-ENG-007, DST-ENG-008, DST-ENG-009, DST-ENG-010, DST-ENG-011, DST-ENG-012, DST-ENG-013, DST-ENG-014, DST-ENG-017 |

## Not decided here

The name of the engine directory. Whether each script gains a docstring
naming its new home. The wording of the notes and the release notes. The
order in which the tests are rewritten.
