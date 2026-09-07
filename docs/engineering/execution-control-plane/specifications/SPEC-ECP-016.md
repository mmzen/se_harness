+++
id = "SPEC-ECP-016"
type = "specification"
title = "The harnessctl command shape"
status = "approved"
owners = ["technical-owner", "quality-owner"]
created = "2026-08-30"
updated = "2026-08-30"

[relations]
specifies = ["REQ-ECP-027"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-30T16:56:30Z"
decided_by = "technical-owner"
reason = "Approved by the technical owner on 2026-08-30 with the words 'Approve and start WO-ECP-021': ECP-CLI-001 to ECP-CLI-009; the command-result object for the eleven commands without JSON, the 0/1/2 exit rule with failed results on standard output, one code per line, WEX301-304 and WEX401-404 by cause class raised in the provenance module, CLI-level tests for the five uncovered commands."
+++

# Specification: The harnessctl command shape

## Scope

The rules every `harnessctl` subcommand follows for the repository target,
artifact naming, `--json`, exit codes and diagnostic codes. No change to
the schema-2 workflow result (`se-harness-workflow-result-v2`), which the
workflow commands keep printing under `--json`.

## Terms

- **Repository command:** a subcommand that reads or writes the repository
  at `target`.
- **Command result:** the JSON object a non-workflow command prints under
  `--json`, schema `se-harness-command-result-v1`.
- **Failed result:** a schema-2 result whose `operation.outcome` is not
  `completed`, or a command result whose `outcome` is `failed`.

## Behavioral rules

**ECP-CLI-001:** The repository commands are `init`, `adopt`, `validate`,
`inspect`, `dashboard`, `doctor`, `preflight`, `check`, `evidence`,
`pr-body`, `transition`, `upgrade`, `scaffold-domain`, `create-artifact`,
`renumber-artifacts`, `release-unit`, `qualify released-root`, `qualify
complete-candidate`, `qualify public-install`, `capture-verification` and
`prepare-release`; each takes the optional positional `target` (default
`.`) and no other option that names the repository. `select-work-order`,
`identity` and `qualify candidate-package` take no `target`.
`rehearse-recovery` keeps `output` and `--repository` until issue #221
decides its fate. A test pins these three sets against the parser.

**ECP-CLI-002:** `prepare-release` takes `--owner` (the preparation actor,
recorded as the record owner; it does not authorize). `--authorized-by` is
refused before parsing with one line naming `--owner`, exit `2`.
`preflight` keeps `--work-order` (see `REQ-ECP-027`).

**ECP-CLI-003:** Every subcommand accepts `--json`. The workflow commands
(`check`, `evidence`, `transition`, `capture-verification`,
`prepare-release`) and the scripts `validate` and `inspect` keep their
existing JSON. The others print one command result:
`{"schema": "se-harness-command-result-v1", "command": NAME, "outcome":
"completed" | "failed", ...}` with these members:
`init`/`adopt`/`upgrade`: `changes` (list of `{action, path}`), `written`
(bool), `conflicts` or `customized` (list of paths) when any;
`doctor`: `checks` (list of `{name, passed, detail}`), `warnings`
(list of `{code, path, message}`); `dashboard`: `output`,
`manifest_sha256`; `pr-body`: `body`; `select-work-order`: `field`,
`value`; `rehearse-recovery`: the retained report object;
`scaffold-domain`/`create-artifact`: `changes` (list of `{action, path}`),
`allocated_id` when one was allocated, `dry_run`; `renumber-artifacts`:
its existing `se-harness-renumber-v1` object; `release-unit`: its existing
object; `identity`: the `se-harness-runtime-identity-v3` object;
`qualify`: its existing object.

**ECP-CLI-004:** Exit codes: `0` when the operation completed; `1` when it
ran and its result is failed, blocked or not passing (`doctor`,
`preflight`, `check`, `evidence`, `transition`, `capture-verification`,
`prepare-release`, `identity`, `qualify`, `release-unit`,
`renumber-artifacts`, `rehearse-recovery`, `init`/`adopt`/`upgrade` on a
conflict or a customized file); `2` when the command could not run (a
parser error, a pre-parse refusal, a `HarnessError` or `ContractError`
raised before any result exists). `capture-verification` and
`prepare-release` therefore exit `1`, not `2`, on a failed result.

**ECP-CLI-005:** A failed result is printed to standard output in both
renderings; standard error carries only the pre-parse refusals and the
`harnessctl: …` line of an exit-2 failure.

**ECP-CLI-006:** A diagnostic code is printed once per line. A message
passed to `failed_result` never begins with a code; when a raised message
begins with a code (`WEXnnn` or `WEX-XXX-nnn`), that code is the result's
code and the message is the remainder.

**ECP-CLI-007:** `capture-verification` refuses with `WEX301` when the
work order is not `implemented` or the graph is not valid; `WEX302` when
revision provenance cannot be established (Git missing, `HEAD` unresolved,
worktree not clean, evidence untracked); `WEX303` when the evaluator
evidence cannot be captured (a managed script missing, failing, timing out
or returning no contract); `WEX304` when a record input is invalid (id,
owner, evidence path, output path). `prepare-release` uses `WEX401` to
`WEX404` for the same four classes. The provenance module raises each
refusal with its class, so the CLI maps without inspecting text.

**ECP-CLI-008:** The five subcommands never driven through `main()` by a
test (`rehearse-recovery`, `create-artifact`, `renumber-artifacts`,
`identity`, `qualify`) gain one CLI-level test each, with their
collaborators mocked where they need an environment, asserting the exit
code rule, the `--json` object and the argv the handler passes on.

**ECP-CLI-009:** `docs/notes/harnessctl-reference.md` states the four
rules (target, naming, `--json`, exit codes) once in a short section and
carries `--json` in every synopsis; `harnessctl-check.md` names the new
codes where it names `WEX301`.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-ECP-027 | ECP-CLI-001 to ECP-CLI-009 |

## Failure behaviour

A script on `--authorized-by` fails loudly at the guard. A script that
read a failed `capture-verification` result from standard error sees it on
standard output and an exit code of `1`.

## Compatibility and migration

Consumer-visible: `--authorized-by` gone; exit code `1` instead of `2` for
a failed record preparation; failed results on stdout; new codes
`WEX302`-`WEX304` and `WEX402`-`WEX404`. Every existing `--json` output is
unchanged in shape. The evidence-checkpoint set (`start`, `pre-action`,
`transition`, `handoff`) and `check`'s (`+scope`) differ on purpose: the
scope checkpoint writes no packet.

## Amendment record

**The `--authorized-by` guard of `ECP-CLI-002` is closed, proposed 2026-09-02 under `WO-ECP-025` (`SPEC-ECP-019` `ECP-TMB-006`).** `prepare-release` still takes `--owner` only; the pre-parse guard that named it left `main()`, and argparse refuses `--authorized-by` as an unrecognized argument with exit status 2. Nothing else in this specification changes.

## Amendment record

**`ECP-CLI-001` is amended, proposed 2026-09-06 under `WO-ECP-026` (`SPEC-ECP-020` `ECP-INS-001`).** The repository-command list loses `adopt`: `init` is the one installation command and its behaviour follows the target's content. The pinned set in `tests/test_cli_shape.py` reads accordingly. Nothing else in this specification changes.

## Amendment record

**The `ECP-CLI-001` amendment of 2026-09-06 is qualified, decided by the accountable owner on 2026-09-06 by selecting the presented option "One-release alias window" under `WO-ECP-026`.** The repository-command list keeps `adopt` for the 0.16.0 release as a plain alias of `init` taking the positional `target`; the pinned set in `tests/test_cli_shape.py` keeps it for that release and drops it with the follow-up work order that removes the alias.

## Amendment record

**`ECP-CLI-004` is made to hold on every writing command, proposed 2026-09-07 under `WO-ECP-027` (`SPEC-ECP-021` `ECP-COR-004` to `ECP-COR-008`).** The mutation guard raises `MutationGuardError`, a `HarnessError` subclass, and `transition`, `decide`, `capture-verification` and `prepare-release` re-raise it by type, so every guard refusal exits 2; a `--set`, `--decision` or `--reason` syntax error on `transition` is a usage refusal, exit 2; every handler that builds a schema-2 result converts the same exception classes `check` converts, and `main()` also catches `ProcedureError`, so no traceback remains reachable for those classes. `pr-body` with an unknown artifact and `dashboard --json` follow the rule as `ECP-COR-009` to `ECP-COR-012` state. Nothing else in this specification changes.

## Amendment record

**`ECP-CLI-006` is made to hold on every result path, proposed 2026-09-07 under `WO-ECP-027` (`SPEC-ECP-021` `ECP-COR-001` to `ECP-COR-003`).** The checkpoint path of `check`, `evidence`, `transition` and `decide` obtain the result's code through the one splitter the projection already used, so a raised `WEX210` or `WEX200` message no longer renders its code twice; the code families the splitter recognizes are unchanged. Nothing else in this specification changes.

## Amendment record

**The `ECP-CLI-001` qualification of 2026-09-06 is closed, under `WO-ECP-029` (`SPEC-ECP-022` `ECP-DEL-015` to `ECP-DEL-018`), proposed 2026-09-07.** The repository-command list no longer names `adopt`; the pinned set in `tests/test_cli_shape.py` drops it. Nothing else changes.

## Amendment record

**`ECP-CLI-001`, `ECP-CLI-003` and `ECP-CLI-008` are amended, under `WO-ECP-030` (`SPEC-ECP-022`), proposed 2026-09-07 on the owner decisions recorded on issue #381 (`ECP-DEL-021`, `ECP-DEL-031`).** `renumber-artifacts` and `rehearse-recovery` leave the command list, the own-object list of `--json` and the list of subcommands tested through `main()`; `rehearse-recovery`'s reserved `output` and `--repository` shape (issue #221) is moot. Nothing else changes.
