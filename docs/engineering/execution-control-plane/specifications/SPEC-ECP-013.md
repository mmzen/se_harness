+++
id = "SPEC-ECP-013"
type = "specification"
title = "Removal of the focus alias and the orientation skill's move to check"
status = "approved"
owners = ["technical-owner", "quality-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[relations]
specifies = ["REQ-ECP-024"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T12:27:21Z"
decided_by = "technical-owner"
reason = "Approved by the technical owner on 2026-08-29 with the words 'Approve and start WO-ECP-017': ECP-RMV-001 to ECP-RMV-007; the focus-json operation identifier stays as contract vocabulary and history is kept by a phase-5 vector row, never by editing a retained fixture."
+++

# Specification: Removal of the focus alias and the orientation skill's move to check

## Scope

Closes the alias window `SPEC-ECP-011` opened: the `focus` subcommand, its
deprecation notice and its alias tests go; `harness-orient` orients through
`check` (`ECP-ONE-007`, deferred at `WO-ECP-015`); the skill-identity
vectors gain a later row. No contract file, procedure step, gate, result
schema or hash-locked root file changes.

## Terms

- **Projection:** `check` without a checkpoint, as `ECP-ONE-001` defines it.
- **Retained vector row:** a JSON fixture under
  `tests/fixtures/agentic_execution/` whose digests describe a skill core
  at an earlier phase; retained rows are never edited.

## Behavioral rules

**ECP-RMV-001:** `harnessctl` has no `focus` subcommand: the parser does
not register it, `--help` does not list it, and `_focus` and the
deprecation notice are deleted from `cli.py`.

**ECP-RMV-002:** `harnessctl focus …` exits with status 2, writes nothing
to standard output and one line to standard error that names `harnessctl
check --artifact ID` as the replacement; the pre-parse guard is the only
place the word survives in the CLI.

**ECP-RMV-003:** The projection function in `workflow.py` loses its
`operation` parameter and names the operation `check` unconditionally;
`workflow_compliance.focus_selected` is removed with its callers moved to
the projection; the refusal for a non-primary artifact names `check`.

**ECP-RMV-004:** `harness-orient`'s `orient.py` probes and invokes `check`
where it probed and invoked `focus`, with the same `--artifact ID --json`
arguments and the same sections read; the deviation code `AEXORI030` and
the operation identifier `focus-json` are unchanged. `SKILL.md` names
`check`; `skill-contract.json` is unchanged in content.

**ECP-RMV-005:** A phase-5 vector fixture records the new `harness-orient`
identity (`manifest_sha256`, `contract_sha256`, `schema`) with the phase-4
orientation identity as its `previous`; the phase-1, phase-3 and phase-4
fixtures are byte-unchanged; the tests that asserted the live core against
the phase-1 `portable_core` and the phase-4 `orientation` assert those rows
against the phase-5 `previous` instead, and the live core against the
phase-5 `current`.

**ECP-RMV-006:** The alias tests and the captured fixture
(`tests/fixtures/focus_alias/`) are removed; the projection tests keep
their coverage under names that say `check`; the fake evaluator fixture
advertises `check`, and its `no-focus` mode becomes `no-check` with the
same degraded outcome.

**ECP-RMV-007:** `docs/notes/harnessctl-reference.md` drops the `focus`
row; `harnessctl-check.md` states that `focus` was removed in the release
after 0.10.0; `harness-orient.md`, the template `README.md.seed` and this
repository's `AGENTS.md` owner region name `check`.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-ECP-024 | ECP-RMV-001 to ECP-RMV-007 |

## Failure behaviour

Nothing new fails; `check` refuses as it does today. A consumer's script on
`focus` fails loudly at the guard rather than silently changing behaviour.

## Compatibility and migration

Consumer-visible: the command is gone after the alias window
`ECP-ONE-004` announced. The skill contracts and their operation
identifiers do not change, so a consumer's installed skills keep
validating; the shipped `harness-orient` core changes digest, which the
upgrade delivers as any managed-file change.

## Amendment record

**`ECP-RMV-002` is closed, proposed 2026-09-02 under `WO-ECP-025` (`SPEC-ECP-019` `ECP-TMB-001`, `ECP-TMB-002`).** The pre-parse guard for `focus` left `main()` three releases after the removal shipped; argparse refuses the name with its usage error and exit status 2, and the word no longer survives in the CLI. Nothing else in this specification changes.
