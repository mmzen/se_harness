+++
id = "SPEC-ECP-022"
type = "specification"
title = "Wave 1 deletions: dead code, the adopt alias, two dormant commands, the unwired journal, unreachable contract entries"
status = "draft"
owners = ["technical-owner"]
created = "2026-09-07"
updated = "2026-09-07"
contract = "Everything the code health assessment found unreferenced, dormant or unreachable leaves the package, the templates, the tests and the workflows, with a dated amendment record wherever a definition named it."

[relations]
specifies = ["REQ-ECP-033"]
+++

# Specification: Wave 1 deletions: dead code, the adopt alias, two dormant commands, the unwired journal, unreachable contract entries

## In plain words

Three groups of removals, each its own work order. Dead code and hygiene;
the one-release `adopt` alias; the dormant surface the owner retired on
2026-09-07.

## Scope

Group A (`WO-ECP-028`) is the unreferenced symbols of section 1 of the
assessment, eight orphan fixtures and a handful of dead configuration lines,
workflow outputs and test pins. Group B (`WO-ECP-029`) is
the `adopt` alias. Group C (`WO-ECP-030`) is the two dormant commands, the
unwired journal and two unreachable contract entries. The declared-digest chain of `hash_bound.py` stays for #377.

## Terms

- **Dead symbol.** A function, constant, class or parameter whose only
  reference in the product tree is its definition.
- **Dormant command.** A registered subcommand with no workflow caller and no
  retained operational output in this repository.
- **Amendment record.** A dated `## Amendment record` entry on an approved
  or implemented definition, naming this specification and the rule.

## Rules

**ECP-DEL-001.** The dead symbols listed in `WO-ECP-028` MUST be removed
with their comments, and `pyflakes` MUST report nothing on production code.

**ECP-DEL-002.** `render_operating_card` and its constants MUST leave
`workflow_contract.py` with their test; the managed card stays a template
file.

**ECP-DEL-003.** `InterpreterSafetyError` and the unreachable `except` in
`runtime_identity.py:178` MUST go; `RuntimeIdentity`'s fields MUST NOT
change.

**ECP-DEL-004.** `integrity.compare_lock_entry` MUST lose its unused `lock`
parameter at every call site, and its always-true conditional MUST be
dedented.

**ECP-DEL-005.** `candidate_acceptance.write_acceptance_manifest` MUST go;
`AcceptanceManifest` and `CONTRACT_SHA256` MUST stay unchanged.

**ECP-DEL-006.** The engine MUST lose `compute_impact`, `ALLOWED_STATUSES`,
the `risk_acceptance` type, both `--artifact-root` flags and the inspector's
unreachable plane fallback.

**ECP-DEL-007.** `pyflakes` MUST report nothing on `tests/`, and the invalid
escape at `tests/test_artifact_authoring.py:365` MUST be a raw string.

**ECP-DEL-008.** The eight orphan fixtures under `tests/fixtures/
publication_rehearsal/` and `tests/fixtures/agentic_execution/` MUST be
deleted.

**ECP-DEL-009.** `MANIFEST.in` MUST lose its `*.yaml` line with the test
that pins it, and `pyproject.toml` MUST lose `[tool.unittest]`.

**ECP-DEL-010.** The `SE_HARNESS_AGENT_HOST` test and the `agent_hosts`
fixture key MUST go; no code reads the variable.

**ECP-DEL-011.** The three self-referential `len()` pins and the `41` file
count in `tests/test_fixture_support.py` MUST go; `unittest.main()` MUST end
`tests/test_public_onboarding.py`.

**ECP-DEL-012.** The `workflow_call` outputs `candidate_commit` and
`version` of `release-qualification.yml` and `snapshot_sha256` and
`dashboard_sha256` of `pages-publication.yml` MUST go.

**ECP-DEL-013.** `publish-pypi.yml` MUST lose the `resolve` outputs
`source_date_epoch`, `distribution_schema`, `build_recipe`,
`build_recipe_sha256` and the `github_release` output `state`.

**ECP-DEL-014.** `candidate-evidence.yml`'s `candidate-package` job MUST read
`needs.candidate-source.outputs.candidate_version` instead of re-deriving
the version.

**ECP-DEL-015.** The parser MUST NOT register `adopt`; argparse refuses the
name as any unknown command, exit 2, no guard.

**ECP-DEL-016.** `tests/test_cli_shape.py` MUST drop `adopt` from the
repository-command set, and the alias test in `tests/test_harnessctl.py`
MUST go.

**ECP-DEL-017.** `harnessctl-reference.md` MUST lose the `adopt` inventory
row and synopsis line.

**ECP-DEL-018.** `SPEC-ECP-020`, `REQ-ECP-031`, `VER-ECP-022` and
`SPEC-ECP-016` MUST close their alias-window records by dated amendment
record naming this specification.

**ECP-DEL-019.** `candidate_acceptance.SCENARIO_IDS` MUST keep the scenario
id `adopt` unchanged, so `CONTRACT_SHA256` does not move.

**ECP-DEL-020.** `se_harness/renumber.py`, `se_harness/recovery_rehearsal.py`
and `se_harness/journaled_apply.py` MUST be deleted with their three test
modules.

**ECP-DEL-021.** The parser MUST NOT register `renumber-artifacts` or
`rehearse-recovery`; argparse refuses both, exit 2, no guard.

**ECP-DEL-022.** `mutation_guard.py` MUST lose the `renumber-artifacts-apply`
operation, and `diagnostic_code_index.py` MUST lose the `REN`, `RR` and
`JNL` prefixes.

**ECP-DEL-023.** `docs/notes/diagnostic-codes.md` MUST be regenerated, and
`tests/test_release_build.py` MUST stop asserting `journaled_apply.py` in
the wheel.

**ECP-DEL-024.** `quality_gates_contract.json` MUST lose gate `QG-G0-INTENT`
with `QGP-G0-GRAPH` and `QGP-G0-INTEGRITY`; the template `QUALITY_GATES.json`
and `.md` MUST match.

**ECP-DEL-025.** `workflow_contract.json` MUST lose `PROC-CANDIDATE-COMMIT`
and `STEP-CANDIDATE-COMMIT-AUTHORIZE`; the template `WORKFLOW.json` and
`.md` MUST match.

**ECP-DEL-026.** The template `WORKFLOW.md` MUST lose "renumber apply" from
its authority sentence, and `harnessctl-check.md` MUST lose the `QG-G0`
row.

**ECP-DEL-027.** `harnessctl-reference.md` MUST lose the two commands' rows,
synopses and sections, and `evaluator-recovery-runbook.md` MUST state the
command's retirement.

**ECP-DEL-028.** Tests that compare the package contracts with the installed
copies MUST compare against the candidate template while the root lags.

**ECP-DEL-029.** `SPEC-DST-019` and `REQ-DST-061` MUST record the retirement
of renumbering by dated amendment record naming this specification.

**ECP-DEL-030.** `REQ-ECP-017`, `SPEC-ECP-006` rules `ECP-JNL-001` to `-005`
and `VER-ECP-014` MUST record the journal's retirement by dated amendment
record.

**ECP-DEL-031.** `SPEC-REB-001` rules 6 and 8, `SPEC-REB-002` rule 14,
`SPEC-ECP-016` `ECP-CLI-001`, `-003`, `-008`, `SPEC-TCM-002` and
`SPEC-DCM-001` MUST record the removals by dated amendment record.

**ECP-DEL-032.** Neither retired command MAY keep a pre-parse guard or a
product message naming a replacement (the `ECP-TMB` policy).

**ECP-DEL-033.** Every deletion MUST leave `validate` at 0 errors and the
suite at its baseline names, with nothing else changed.

**ECP-DEL-034.** No other registered command, no option, no result schema
and no managed path beyond the two template contracts and `WORKFLOW.md`
MAY change.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| `harnessctl adopt`, `renumber-artifacts` or `rehearse-recovery` | argparse usage error, exit 2 | none |
| a dead symbol reintroduced | the `vulture` reading in the evidence names it | none |
| a contract entry named by a rule but absent | `load_validated_contracts` refuses | `WEX-ECP-030` family |

## Examples

**Given** the candidate after group C, **when** `harnessctl --help` runs,
**then** neither `renumber-artifacts` nor `rehearse-recovery` is listed
(ECP-DEL-021).

**Given** the candidate after group A, **when** `vulture --min-confidence
60` runs over `se_harness scripts repository_tools`, **then** it reports
nothing but the kept test-only chains (ECP-DEL-001).

**Given** the candidate after group C, **when** the package contract and the
candidate template are compared, **then** they are byte-equal and name no
`QG-G0-INTENT` (ECP-DEL-024).

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-ECP-033` | ECP-DEL-001, ECP-DEL-002, ECP-DEL-003, ECP-DEL-004, ECP-DEL-005, ECP-DEL-006, ECP-DEL-007, ECP-DEL-008, ECP-DEL-009, ECP-DEL-010, ECP-DEL-011, ECP-DEL-012, ECP-DEL-013, ECP-DEL-014, ECP-DEL-015, ECP-DEL-016, ECP-DEL-017, ECP-DEL-018, ECP-DEL-019, ECP-DEL-020, ECP-DEL-021, ECP-DEL-022, ECP-DEL-023, ECP-DEL-024, ECP-DEL-025, ECP-DEL-026, ECP-DEL-027, ECP-DEL-028, ECP-DEL-029, ECP-DEL-030, ECP-DEL-031, ECP-DEL-032, ECP-DEL-033, ECP-DEL-034 |

## Not decided here

- The wording of the amendment records and the note sentences.
- Whether the three deleted test modules leave one absence test in
  `tests/test_cli_shape.py` or none.
- The order of the three work orders' pull requests; each is independent.
