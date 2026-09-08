+++
id = "SPEC-ECP-021"
type = "specification"
title = "Failure paths of harnessctl: one code splitter, one guard error, bounded launches"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-07"
updated = "2026-09-07"
contract = "Every failing command path reports one code per line, exits 1 for a result and 2 for a refusal, and no subprocess launch waits without a timeout."

[relations]
specifies = ["REQ-ECP-032"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-07T19:33:14Z"
decided_by = "technical-owner"
reason = "Approved on 2026-09-07 by the accountable owner with the words 'i approve', given after the packet PR #382 and its summary were presented: rules ECP-COR-001 to ECP-COR-022, one code splitter, the typed mutation-guard error, the shared exception tuple, dashboard and pr-body on the rule, bounded launches, the four latent defects, the tests and the records. Approval of a definition authorizes no work."
+++

# Specification: Failure paths of harnessctl: one code splitter, one guard error, bounded launches

## In plain words

The command reference already states how a failure looks. This
specification lists the places where the code departs from it and says what
each must do instead.

## Scope

The failure paths of the `harnessctl` handlers in `se_harness/cli.py`, the
mutation guard's exception type, three subprocess launchers, and four latent
defects from issue #375. The diagnostic-code registry and the single Git
launcher belong to #377; the `renumber-artifacts` output belongs to #376.
No registered command, option, result schema or managed template changes.

## Terms

- **Result.** A rendered outcome on standard output with exit 1, either a
  schema-2 workflow result or a `se-harness-command-result-v1` object.
- **Refusal.** A `harnessctl: …` line on standard error with exit 2, printed
  by `main()` for an exception no handler converted.
- **Shared tuple.** The exception classes `_check` converts into a result:
  `HarnessError`, `ContractError`, `ProcedureError`, `ValueError`.

## Rules

**ECP-COR-001.** `_check` and `_evidence` MUST obtain the result code and
message through `_split_code`, never through a hand-written prefix test.

**ECP-COR-002.** `_transition` and `_decide` MUST obtain the result code
through `_split_code(str(exc), _refusal_code(exc))`.

**ECP-COR-003.** `CODE_PREFIX` MUST keep recognizing `WEX` codes only; any
widening belongs to the code registry of #377.

**ECP-COR-004.** `mutation_guard._failure` MUST raise
`MutationGuardError`, a `HarnessError` subclass, with the message text
unchanged.

**ECP-COR-005.** `_transition`, `_decide`, `_capture_verification` and
`_prepare_release` MUST re-raise `MutationGuardError` by `isinstance`, never
by a message prefix.

**ECP-COR-006.** `_transition` MUST parse `--set`, `--decision` and
`--reason` before its `try`, so a syntax error is a refusal.

**ECP-COR-007.** Every handler that builds a schema-2 result MUST catch the
shared tuple and render a blocked result, as `_check` does.

**ECP-COR-008.** `main()` MUST catch `HarnessError`, `ContractError` and
`ProcedureError` and print the refusal with exit 2.

**ECP-COR-009.** `dashboard --json` MUST raise `HarnessError` carrying the
engine's last standard-error line when the engine exits 2.

**ECP-COR-010.** `dashboard --json` MUST add an `error` member, the engine's
standard error bounded to 2,000 characters, when the engine exits 1.

**ECP-COR-011.** `pr-body` with an unknown artifact MUST print a failed
command result with code `WEX-ECP-014` and exit 1.

**ECP-COR-012.** The human rendering of that failure MUST be the single
line `WEX-ECP-014: unknown artifact ID: <id>` on standard output.

**ECP-COR-013.** `gate_source._git` MUST pass `timeout=60` and convert
`OSError` and `SubprocessError` into `DelegationError("WEX-ECP-040", …)`.

**ECP-COR-014.** The four engine launches in `cli.py` MUST pass
`timeout=1800` and convert `TimeoutExpired` into `HarnessError`.

**ECP-COR-015.** `upgrade_rehearsal.run` MUST pass `timeout=600` and
convert `TimeoutExpired` into a `Completed` with return code 124.

**ECP-COR-016.** `artifact_layout.REF_ARTIFACT_PATTERN` MUST be built from
the values of `_REF_PREFIX`, so `OPS-*` and `DEC-*` files match.

**ECP-COR-017.** `evaluator_facts._front_matter` MUST read with `utf-8-sig`
and normalize `\r\n` and `\r` to `\n` before locating the closing `+++`.

**ECP-COR-018.** `normalize_artifacts` MUST project a list
`verification_method` as its members joined by `", "`, a string unchanged,
anything else as `None`.

**ECP-COR-019.** `pages-publication.yml` MUST read
`steps.package.outputs.bundle_manifest_sha256` where it read the
never-emitted `snapshot_sha256`.

**ECP-COR-020.** `publish-pypi.yml` MUST run the pinned `setup-python` step
in the `github_release` and `observe` jobs before any `python` command.

**ECP-COR-021.** Each rule from ECP-COR-001 to ECP-COR-020 MUST have a test
that fails on the code before the change and passes after it.

**ECP-COR-022.** `harnessctl-reference.md` MUST state the `pr-body` and
`dashboard --json` behaviour, and `SPEC-ECP-016` MUST close `ECP-CLI-004`
and `ECP-CLI-006` gaps by dated amendment record.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| a handler receives a coded message | one code, the remainder as message, exit 1 | the carried code |
| the mutation guard refuses a writing command | refusal on standard error, exit 2 | `MG00x` |
| `--set` value without `=` | usage refusal, exit 2 | none |
| an engine or Git subprocess exceeds its timeout | the caller's refusal, exit 2 | `WEX-ECP-040` for the gate |
| `pr-body` names an unknown artifact | failed result on standard output, exit 1 | `WEX-ECP-014` |

## Examples

**Given** this repository, **when** `check . --artifact WO-ZZZ-999
--checkpoint scope --json` runs, **then** `blocked_by` reads `WEX210:
unknown artifact ID: WO-ZZZ-999` once (ECP-COR-001).

**Given** a checkout whose evaluator is not the released one, **when**
`transition --apply` runs, **then** the guard's refusal is on standard
error and the exit status is 2 (ECP-COR-004, ECP-COR-005).

**Given** a requirement with `verification_method = ["test", "inspection"]`,
**when** the Explorer snapshot is built, **then** the item reads
`"test, inspection"` (ECP-COR-018).

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-ECP-032` | ECP-COR-001, ECP-COR-002, ECP-COR-003, ECP-COR-004, ECP-COR-005, ECP-COR-006, ECP-COR-007, ECP-COR-008, ECP-COR-009, ECP-COR-010, ECP-COR-011, ECP-COR-012, ECP-COR-013, ECP-COR-014, ECP-COR-015, ECP-COR-016, ECP-COR-017, ECP-COR-018, ECP-COR-019, ECP-COR-020, ECP-COR-021, ECP-COR-022 |

## Not decided here

- Test names and placement.
- The wording of the reference rows and the amendment records.
- Whether the engine timeout is a module constant or a parameter.
- Whether the `error` member is trimmed at the head or the tail.

## Amendment record

**The engine timeout row of the failure table is withdrawn under `WO-ECP-034` (`SPEC-ECP-024` `ECP-ENG-003` and `ECP-ENG-025`), recorded 2026-09-08.** The evaluator imports the validator, the generator and the inspector and runs them in-process, so no engine subprocess exists to exceed a timeout; the row's Git clause stands, and `WEX-ECP-040` stays the gate's code. The unspecified decision on the engine timeout constant is moot. Nothing else in this specification changes.
