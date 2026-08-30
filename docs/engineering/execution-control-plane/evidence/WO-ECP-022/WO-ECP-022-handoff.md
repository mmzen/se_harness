```toml
artifact = "WO-ECP-022"
checkpoint = "handoff"
formal_snapshot_sha256 = "7c5e78ae4110643d4123d18bbd4625aa2c8930c0ee96c433e8234b093d3ab208"
rebound_at = "2026-08-30T19:20:34Z"
```

# WO-ECP-022 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

Every `harnessctl` subcommand follows one shape: the repository is the
positional `target` on the twenty-one repository commands and absent on
the three that read something else, pinned by a test; `prepare-release`
names its actor `--owner` and refuses `--authorized-by` by name; every
subcommand accepts `--json`; a completed operation exits `0`, a failed or
blocked result exits `1` and prints to standard output, a command that
could not run exits `2`; a diagnostic code appears once per line;
`capture-verification` and `prepare-release` refuse with one cause class
per code; the five commands never driven through `main()` have CLI-level
tests; the reference states the four rules once (`REQ-ECP-027`;
`ECP-CLI-001` to `ECP-CLI-009`).

## Evaluators

- Governing: released `se-harness 0.11.0` outside the checkout, `-I`, on
  this Windows checkout for every reading, the packet and the handoff check
  included. It keeps the old command shape until the next root adoption.
- Candidate: this checkout, branch `wo/ecp-021-cli-shape` off `main` at
  `7cac025`, with `main` at `4b29d8a` (the live-PR-body chain, #293/#294)
  merged in at `cffcb61`; the suite and the demonstration run candidate
  source.

## Change

- `se_harness/provenance.py`: `RecordRefusal` and its four classes
  (`StateRefusal`, `ProvenanceRefusal`, `EvidenceRefusal`,
  `InputRefusal`), `CAUSE_SUFFIX`; every refusal in the module raised with
  its class; `_run` takes the class to raise; a domain-name refusal from
  `validate_domain` re-raised as an input refusal.
- `se_harness/cli.py`: `COMMAND_RESULT_SCHEMA`, `CODE_PREFIX`,
  `_split_code`, `_record_code`, `_command_result`, `_print_json`; `--json`
  on `init`, `adopt`, `dashboard` (new `_dashboard` handler reading the
  manifest digest), `doctor`, `pr-body`, `select-work-order`, `upgrade`,
  `rehearse-recovery` (which now exits by the rehearsal's result),
  `scaffold-domain`, `create-artifact`, `identity`; the install and
  upgrade refusals on standard output; `_project` splitting a leading
  code; the two record handlers mapping the cause class, printing to
  standard output and exiting `1`; `prepare-release --owner`; the
  `--authorized-by` guard in `main()`.
- `se_harness/workflow.py`, `se_harness/workflow_compliance.py`: unchanged;
  `failed_result` needed no leading-code strip once the callers split.
- Tests: `tests/test_cli_shape.py` (new, twelve tests);
  `tests/test_revision_provenance.py` (ten refusal sites read standard
  output, exit `1`, and assert their cause code once; a new `WEX303` test
  with the dashboard generator mocked; `--owner`);
  `tests/test_harnessctl.py` (six refusal sites read standard output);
  `tests/test_workflow_execution.py` (`--owner`);
  `tests/test_instruction_architecture.py` (three sites read standard
  output, under the scope amendment). `tests/test_release_qualification.py`,
  `test_artifact_authoring.py`, `test_artifact_renumbering.py`,
  `test_recovery_rehearsal.py`, `test_evaluator_identity.py` and
  `test_progressive_documentation.py` needed no change and pass.
- `docs/notes/harnessctl-reference.md`: the "Command shape" section,
  `[--json]` on every synopsis, `--owner`, the cause classes on both record
  commands. `docs/notes/harnessctl-check.md`: unchanged; it names none of
  the split codes.

## Tests

- Parser: the three target sets equal the parser's; no repository command
  carries `--root`, `--repository` or `--checkout-root`; every subcommand
  and every `qualify` role has `--json`; `prepare-release` has `--owner`
  and not `--authorized-by`, and `--authorized-by` exits `2` with one
  stderr line naming `--owner` and empty stdout.
- JSON: `doctor` (every check with `name`, `passed`, `detail`),
  `create-artifact` and `scaffold-domain` (`changes`, `dry_run`,
  `allocated_id` only when allocated), `renumber-artifacts` (its own
  schema), `pr-body` (`body`), `select-work-order` (`field`, `value`),
  `init --dry-run` (`written` false), `rehearse-recovery` (the report,
  exit by result), `identity` (the runtime-identity object), `qualify` (its
  own schema, exit `1` on a failed result).
- One code per line: `check --artifact REQ-…` blocks with `WEX210: ` once.
- One cause per code: `WEX301` state (work order not implemented),
  `WEX302` provenance (dirty tree, no `HEAD`), `WEX303` evidence (dashboard
  generator failing), `WEX304` inputs (duplicate, missing contract, output
  exists, reserved domain); `WEX401` state (record not verified),
  `WEX404` inputs (different candidate commits); each asserted to appear
  exactly once in the result.
- Exit and stream: every refused record preparation exits `1` with the
  result on standard output and nothing on standard error.

## Suite readings

Windows workstation, candidate source, `scripts/run_tests.py`: 1167 tests, 1 error, 26 skipped, the error being the baseline `test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref` that precedes this work order; the fifteen suites this work order touches or pins: 471 tests, OK, 8 skipped, plus `tests/test_instruction_architecture.py` (30, OK) under the amendment. Linux: the pull request's lanes at the completion commit.

## Demonstration on this repository

Candidate CLI on this checkout:

- `harnessctl doctor . --json`: one object with 113 checks; from the candidate
  copy on this checkout it reads `outcome failed`, 105 passed, because the
  eight distribution checks compare the root's 0.11.0 managed copies with the
  candidate templates (the expected candidate-versus-root skew; the root
  evaluator reads 0 FAIL).
- `harnessctl check . --artifact REQ-ECP-027 --json`: blocker
  `WEX210: check accepts only WO, VREC, or RLS artifacts` (once; the 0.11.0
  root prints `WEX210: WEX210: …`).
- `harnessctl capture-verification …` from the candidate copy on this
  checkout: refused by the mutation guard before any state is read
  (`harnessctl: mutation guard MG005 (capture-verification): RID002 …`),
  exit `2` — an environment refusal, not a result; the state, provenance,
  evidence and input classes are demonstrated by the fixture tests.
- `harnessctl prepare-release . --id RLS-X --authorized-by x`: exit `2`,
  one line naming `--owner`.
- `harnessctl identity --role candidate-source … --json`: the
  `se-harness-runtime-identity-v3` object.
- `harnessctl validate . --json`: the same keys as before this change.

## Readings under the 0.11.0 root

- `validate .`: 1177 artifacts, 0 errors, 485 warnings.
- `doctor .`: 0 FAIL.
- `validate_release_distributions.py`: PASS (8 records).
- Start preflight for `WO-ECP-022`: PASS with no diagnostics over `4e3a584`.

## Deviations, recorded for the completion decision

1. **`preflight` keeps `--work-order`** and **`rehearse-recovery` keeps its
   shape**, as `REQ-ECP-027` states; not deviations from the definitions,
   recorded here because they are the two places the command list still
   departs from the shape.
2. **The scope amendment** of 2026-08-30 (`tests/test_instruction_architecture.py`):
   three assertions moved from standard error to standard output; no
   product path.

## Identifier renumbering

A parallel session took the same four identifiers for the #280c chain and
merged first with a verified record; on the owner's decision of 2026-08-30
this chain was renumbered to `REQ-ECP-027`, `SPEC-ECP-016`, `VER-ECP-018`
and `WO-ECP-022` (see the work order's renumbering note). `renumber-artifacts`
refused the whole plan at inventory (`REN043` on the unrelated
`VREC-WEX-001`) in its first operational use, so the renumbering was by
hand; both facts stand as findings beside this packet.

## Complete changed-path set

Every path this work order changed since `main` at `4b29d8a`, packet
included, as Git derived it; the handoff check completed at its fixed point
with every predicate of `QG-G4-IMPLEMENTATION-EVIDENCE` passing, run by
the released 0.11.0 evaluator on this Windows checkout: see `handoff.json`
beside this file.
