+++
id = "SPEC-ECP-020"
type = "specification"
title = "The merged installation command: init keyed by the target's content"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-06"
updated = "2026-09-06"

[relations]
specifies = ["REQ-ECP-031"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-06T10:51:57Z"
decided_by = "technical-owner"
reason = "Approved on 2026-09-06 by the accountable owner with the words 'i approve', given after the packet PR #359 and its summary were presented: rules ECP-INS-001 to ECP-INS-011, the merged init keyed by the target's content, adopt refused by argparse without a guard, the diagnostic, the --dry-run help text, the three notes, the seven amendment records and the tests. Approval of a definition authorizes no work."
+++

# Specification: The merged installation command: init keyed by the target's content

## Scope

The `init` and `adopt` subcommands of `harnessctl`, their shared handler and
the installer's planner; one diagnostic that names `adopt`; the three notes
with a live reader; the tests that pin the command list and invoke `adopt`;
dated amendment records on the definitions that name `adopt` normatively.
No managed template, contract file, result schema, skill or workflow
changes. `upgrade` is untouched.

## Actors and external systems

The repository owner or an authorized agent installing the harness; the
`candidate-evidence` workflow, which runs a bare `init` and must keep
working; argparse, which refuses the removed name.

## Inputs

The positional `target` (default `.`), `--project-name`, `--dry-run`,
`--json`; the target directory's content.

## Outputs

The plan on standard output, the written files, the lock, the
`se-harness-command-result-v1` object under `--json`.

## State model

Two target states drive the plan: `empty` (the target is absent or has no
entries) and `existing` (at least one entry). Nothing else about the
installer's state model changes.

## Behavioral rules

**ECP-INS-001:** The parser registers `init` and does not register `adopt`.
`--help` lists `init` and no `adopt`. The synopsis is unchanged:
`harnessctl init [TARGET] [--project-name NAME] [--dry-run] [--json]`.

**ECP-INS-002:** When the target is `empty`, `init` plans and writes the
complete standard harness and no adoption report. The plan and the written
bytes are those the previous `init` produced for the same target.

**ECP-INS-003:** When the target is `existing`, `init` behaves as the
previous `adopt`: ordinary existing files are preserved, the bounded managed
fragments are integrated into `AGENTS.md`, `CLAUDE.md` and `.gitignore`, a
differing ordinary destination is a `conflict` that refuses every write with
exit status 1 and the line "no files were written", and
`docs/engineering/ADOPTION_REPORT.md` is planned (`add`, `unchanged` or
`conflict`) and written in the `generated` mode, outside the lock.

**ECP-INS-004:** `plan_install` in `se_harness/installer.py` loses the
refusal "init requires an empty or absent directory" and the `must_exist`
distinction; the two branches that read `mode in {"init", "adopt"}` read one
installation mode. `adopt` is no longer an accepted mode value. The
`upgrade` mode and its leaving-set planning are unchanged.

**ECP-INS-005:** The JSON result carries `"command": "init"` in both target
states and gains no member. A caller distinguishes the states by the
presence of the `docs/engineering/ADOPTION_REPORT.md` entry in `changes`.

**ECP-INS-006:** `harnessctl adopt ...` is refused by argparse as an invalid
subcommand choice: exit status 2, empty standard output, the usage error on
standard error. No pre-parse guard and no product message name a
replacement (the policy of `SPEC-ECP-019` `ECP-TMB-002`).

**ECP-INS-007:** The lock-floor diagnostic in `se_harness/integrity.py`
reads "remove the stale .engineering-harness.lock and re-adopt the
repository with harnessctl init". The verb "re-adopt" stays.

**ECP-INS-008:** The `--dry-run` option of `init`, `scaffold-domain` and
`create-artifact` carries the help text "report the complete plan without
writing", mirroring the help the `--apply` options already carry.

**ECP-INS-009:** Three notes change: `README.md` replaces the sentence
"For an existing project, use `harnessctl adopt ...` instead of `init`" with
one sentence saying `init` also installs into an existing project and keeps
its files; `docs/notes/harnessctl-reference.md` drops the `adopt` inventory
row and synopsis, describes the two target states in the `init` row, and
adds one sentence to its rules section stating the convention: commands
that change existing governed state plan by default and take `--apply`,
commands that add content write by default and take `--dry-run`;
`docs/notes/harness-installation-and-upgrades.md` replaces the
"choose one operation" block with the one command and its two behaviours.
Historical notes and dated packets keep their wording.

**ECP-INS-010:** The definitions that name `adopt` normatively close by
dated amendment record naming this specification, bytes otherwise kept:
`SPEC-ECP-016` `ECP-CLI-001` (the command list loses `adopt`),
`SPEC-DST-003` (the README's `adopt` line becomes the `init` sentence),
`SPEC-HUP-012` (the diagnostic wording of `ECP-INS-007`), and the
statements or lists of `REQ-DST-002`, `REQ-DST-025`, `REQ-DST-034` and
`REQ-DST-056` (each reads `init` where it read `init or adopt`).

**ECP-INS-011:** Tests: `tests/test_cli_shape.py` removes `adopt` from the
pinned repository-command set; every `adopt` invocation in
`tests/test_harnessctl.py`, `tests/test_glossary.py` and
`tests/test_repository_context_retirement.py` becomes `init` with its
assertions unchanged; the `plan_install(..., mode="adopt")` call becomes
the one installation mode; one new test asserts that `init` on a directory
with content writes the adoption report and `init` on an empty directory
does not. No refusal test for `adopt` is added (`ECP-TMB-003`).

## Error and recovery behavior

Nothing new fails. A conflict refuses every write as it does today. A
consumer's shell history with `adopt` fails loudly at the parser.

## Data and interface contracts

The `se-harness-command-result-v1` object is unchanged in shape. The lock
is unchanged: the adoption report stays a `generated` file outside it.

## Security and privacy properties

None new. The mutation-guard inventory of `SPEC-REB-001` rule 6 is
unchanged; `init` was never in it and does not enter it.

## Performance and capacity

The `existing` state adds the ecosystem scan the previous `adopt` ran; the
`empty` state adds nothing.

## Observability

The plan on standard output lists the adoption report as `add` when it is
planned; under `--json` the same entry appears in `changes`.

## Compatibility and migration

Consumer-visible in two ways. `harnessctl adopt` receives argparse's usage
error; the replacement is `harnessctl init` with the same options. `init`
on a directory with content is now permitted where it was refused; the
protections are those `adopt` had: conflicts refuse every write, fragments
only append, `--dry-run` shows the plan. No alias window: `adopt` is a
one-shot human command that no workflow, template or skill invokes, so the
one-release alias `SPEC-ECP-011` used for `focus` would serve no caller.
The candidate-evidence workflow's bare `init` is unaffected. The change
ships in 0.16.0 and reaches this repository's root at the next adoption.

## Examples and counterexamples

Conforming: `init` on a folder holding only `Cargo.toml` writes the
harness, the fragments and the report, exit 0. Conforming: `init` on an
absent path creates it and writes the harness and no report. Counterexample:
an `init` that writes the report into an empty folder, or refuses a folder
with content, does not conform.

## Explicitly unspecified decisions

The exact wording of the note sentences and the amendment records; the
name of the new test; whether the human rendering adds one line naming the
report path after "installed se-harness ... in ...".

## Amendment record

**`ECP-INS-001`, `ECP-INS-006` and `ECP-INS-011` open a one-release alias window, decided by the accountable owner on 2026-09-06 by selecting the presented option "One-release alias window" under `WO-ECP-026`.** For the 0.16.0 release only, the parser also registers `adopt` as a plain alias of `init`: the same options, the same handler, the same result (`"command": "init"`), listed in `--help` as an alias kept for 0.16.0. The refusal of `ECP-INS-006` and the command-set pin of `ECP-INS-011` apply from the candidate after 0.16.0 is adopted, by a follow-up work order under `REQ-ECP-030`. The candidate's own acceptance (`se_harness/candidate_acceptance.py`) keeps the scenario id `adopt` and runs `init` on a folder with content, so the contract digest is unchanged and the successor verifier no longer invokes the alias. The compatibility section's "No alias window" is withdrawn: the released verifier is the caller it did not count. Nothing else changes.

## Amendment record

**The alias window of 2026-09-06 is closed, under `WO-ECP-029` (`SPEC-ECP-022` `ECP-DEL-015` to `ECP-DEL-018`), proposed 2026-09-07.** `ECP-INS-001`, `ECP-INS-006` and `ECP-INS-011` now hold as written: the parser registers `init` only, `adopt` is refused by argparse as any unknown command, and the pinned command set has no `adopt`. The 0.16.0 verifier that governs this repository runs `init` in its `adopt` scenario, so the one-release rule of `REQ-ECP-030` is met. Nothing else changes.
