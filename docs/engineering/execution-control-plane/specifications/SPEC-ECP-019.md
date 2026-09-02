+++
id = "SPEC-ECP-019"
type = "specification"
title = "Retirement of the CLI tombstone guards"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-02"
updated = "2026-09-02"

[relations]
specifies = ["REQ-ECP-030"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-02T14:38:23Z"
decided_by = "technical-owner"
reason = "Approved on 2026-09-02 by the accountable owner by selecting the presented options 'Include the --authorized-by guard too' and 'Delegated route (the delegation class)' for WO-ECP-025: the four CLI tombstone guards (focus, next, accept-candidate, prepare-release --authorized-by) leave main() three releases after their removals shipped (issue #310, assessment item #285c). Rules ECP-TMB-001 to ECP-TMB-007: the guards out, argparse's refusal, one absence test, the notes, the dated amendment records, the fourth guard, the delegation gate of WO-ECP-024."
+++

# Specification: Retirement of the CLI tombstone guards

## Scope

One edit at the head of `main()` in `se_harness/cli.py`, the tests that
pinned the guards, the notes that recorded the removals, and dated
amendment records on the artifacts whose rules described the guards. No
registered command, option, result schema, contract file or managed
template changes.

## Behavioral rules

**ECP-TMB-001:** `main()` in `se_harness/cli.py` carries no pre-parse guard
for `focus`, `next` or `accept-candidate`; the three `if arguments[:1] ==
[...]` blocks and their comments are deleted, and `main()` proceeds to the
parser. `--help` lists none of the three names (unchanged).

**ECP-TMB-002:** Each of the three names is refused by argparse as an
invalid subcommand choice: exit status 2, empty standard output, the usage
error on standard error. No product message names a replacement; the
replacement is documented, not printed.

**ECP-TMB-003:** The three refusal tests are deleted
(`test_focus_is_refused_with_its_replacement_named`,
`test_next_is_no_subcommand_and_names_check`,
`test_accept_candidate_is_no_subcommand_and_names_the_typed_operation`);
their `--help` absence assertions are kept or folded into one test that
also reads `main()`'s source and asserts none of the three names appears
in it.

**ECP-TMB-004:** The notes that recorded the guards state the plain
refusal: `docs/notes/harnessctl-check.md`, `docs/notes/harnessctl-reference.md`
and `docs/notes/release-qualification-roles.md` no longer say that the
removed command "exits with status 2 naming" its replacement.

**ECP-TMB-005:** The rules that described the guards close by dated
amendment record, each naming this specification: `REQ-ECP-024` (the
clause "refuse focus with a message naming check"), `SPEC-ECP-013`
`ECP-RMV-002`, `SPEC-ECP-014` `ECP-CTX-004` and `ECP-CTX-006`,
`VER-ECP-013`'s "no second name" row and `VER-ECP-016`'s "no `next`" and
"no `accept-candidate`" rows. The records keep their bytes otherwise.

**ECP-TMB-006:** The `--authorized-by` guard of `prepare-release` retires
the same way, on the owner's decision of 2026-09-02: the guard block goes,
argparse refuses the unknown option (exit 2, usage error),
`tests/test_cli_shape.py`'s refusal assertion becomes an
unrecognized-argument assertion, and `SPEC-ECP-016` `ECP-CLI-002` closes by
amendment record.

**ECP-TMB-007:** The work order carries `[delegation] class = "execution"`
and uses the gate `WO-ECP-024` configured (`github-checks`, `check_name =
"validate"`, `base_ref = "origin/main"`). The delegated route takes
`DR-WO-START`, `DR-WO-COMPLETE` and `DR-VREC-PREPARE` only; approval,
verification and the merges stay human.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-ECP-030 | ECP-TMB-001 to ECP-TMB-007 |

## Failure behaviour

A guard reintroduced for any retired name fails the source-reading test.
The suite otherwise passes unchanged; the retirement changes no registered
behaviour.

## Compatibility and migration

Consumer-visible: a script still invoking `focus`, `next`,
`accept-candidate` or `prepare-release --authorized-by` after three releases
of loud refusals now receives argparse's generic usage error instead of the
named replacement. The
replacements stay documented in the command reference.
