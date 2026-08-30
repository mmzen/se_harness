+++
id = "REQ-ECP-026"
type = "requirement"
title = "One command shape: repository target, artifact naming, JSON, exit codes and one code per message"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-30"
updated = "2026-08-30"
statement = "WHEN an operator or a script invokes any harnessctl subcommand, THE SYSTEM SHALL address the repository, name artifacts, offer --json, map outcomes to exit codes and print diagnostic codes in one consistent way across the whole command list, so that a rule learnt on one command holds on every other."
verification_method = ["test"]
priority = "must"
source = "functional assessment of 2026-08-30, issue #282 (FA-3)"

[relations]
derives_from = ["CAP-ECP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-30T16:56:30Z"
decided_by = "requirements-steward"
reason = "Approved by the requirements steward on 2026-08-30 with the words 'Approve and start WO-ECP-021': one command shape across harnessctl for the repository target, artifact naming, --json, exit codes and diagnostic codes; preflight's --work-order and rehearse-recovery's shape are stated exclusions; issue #282 of the functional assessment."
+++

# Requirement: One command shape: repository target, artifact naming, JSON, exit codes and one code per message

## Rationale

The 22 subcommands grew one at a time, and each spells the same ideas its
own way. The repository root is a positional `target` in eighteen commands
and something else in the rest; the artifact is `--artifact`, `--id`,
`--work-order` or `ID=STATUS` depending on the command; eleven commands have
no `--json`; a failed result exits 1 in some commands and 2 in others, and
goes to stdout or stderr depending on a flag; one message prints its code
twice (`WEX210: WEX210: …`); one code (`WEX301`) stands for four unrelated
causes, from "work order not implemented" to a subprocess timeout. Every
one of these costs a user a re-read of the help text, and a script author a
special case. The assessment scored ease of use 3/10 with these as the
first evidence.

## Preconditions and trigger

Any invocation of `harnessctl`.

## Required response

- **Repository target.** Every subcommand that reads or writes a
  repository takes the optional positional `target`, default `.`. A
  subcommand that operates on something else (an event file, a runtime
  environment, a wheel) takes no `target`; a test pins which subcommand is
  which, so the classification cannot drift.
- **Artifact naming.** The selected existing artifact is `--artifact`; a
  record being created is `--id`; an option that names a relation of the
  new record keeps the relation's name (`--work-order`, `--verification`,
  `--verification-record`, `--release-contract`). `prepare-release` names
  its preparation actor `--owner`, as `capture-verification` does; the
  former `--authorized-by` is refused with a message naming `--owner`.
- **JSON.** Every subcommand accepts `--json` and prints one JSON object
  carrying the same facts as its human output.
- **Exit codes.** `0`: the operation completed. `1`: the operation ran and
  its result is blocked, failed or not ready. `2`: the command could not
  run (usage error, environment refusal). A failed result is printed to
  standard output in both renderings.
- **One code per message.** A diagnostic code appears once in a line; the
  message text never repeats its own code.
- **One cause per code.** `capture-verification` and `prepare-release`
  refuse with a code that names the cause class: the artifact's state, the
  revision provenance, the evaluator evidence, or the record's inputs.

## Failure and boundary behavior

`preflight` keeps `--work-order`: the shipped orientation skill and the
managed lane call it by that name, and the assessment's separate
recommendation is to fold `preflight` into `check`; the rename would be
churn on a surface about to go. `rehearse-recovery` keeps its shape because
its retirement is a separate decision (issue #221). Both are stated, not
silent.

## Constraints

No change to the schema-2 workflow result, to any gate, procedure or
contract file, or to any hash-locked root file.

## Acceptance examples

### Example: normal behavior

**Given** a repository with a verified record.

**When** `harnessctl doctor . --json` runs.

**Then** standard output is one JSON object listing every check with its
outcome, and the exit code is `0` when all pass.

### Example: failure behavior

**Given** `harnessctl capture-verification` on a work order that is not
`implemented`.

**When** it runs.

**Then** the result is printed to standard output, its blocker starts with
the state code (`WEX301`) exactly once, and the exit code is `1`.

## Open decisions

None.
