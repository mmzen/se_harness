```toml
artifact = "WO-ECP-019"
checkpoint = "handoff"
formal_snapshot_sha256 = "25cf6b2d8f1b36d6cf860b4c9998a8a3ca127dea90dc9850ed88d701ffc6b802"
rebound_at = "2026-08-29T18:53:09Z"
```

# WO-ECP-019 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

`check` without a checkpoint is the execution context: it carries the
`context` object `next` introduced and selects the single `in_progress`
work order when none is named; `next` is a byte-identical alias for one
release with a removal notice on standard error; every corrective names
`check`; `accept-candidate` is gone behind a guard naming `qualify
candidate-package`; the template `WORKFLOW.md`, the notes and an amendment
record on `SPEC-ECP-001` say so (`REQ-ECP-025`; `ECP-CTX-001` to
`ECP-CTX-008`).

## Evaluators

- Governing: released `se-harness 0.11.0` outside the checkout, `-I`, on
  this Windows checkout for every reading, the packet and the handoff check
  included.
- Candidate: this checkout, branch `wo/ecp-019-context-and-aliases` off
  `main` at `970a0ae`; the suite and the demonstration run candidate source.

## Change

- `se_harness/workflow.py`: `project_selected` takes an optional artifact
  (the `WEX-ECP-001` selection moved from `next_step`), and appends the
  `context` object and the recomputed `result_sha256` to every projection;
  `next_step` is deleted.
- `se_harness/cli.py`: one `_project` helper behind `check` without a
  checkpoint and behind `next`, which prints the notice first; `check`'s
  `--artifact` is optional and `WEX210` refuses a checkpoint without it;
  the `accept-candidate` parser and handler are deleted and a pre-parse
  guard names `qualify candidate-package`.
- `se_harness/workflow_compliance.py`: the `WEX210` corrective and response
  name `check`.
- `se_harness/workflow_result.py`: unchanged; the `Context` section was
  already keyed on the object's presence, not the operation kind.
- `templates/repository/standard/docs/engineering/WORKFLOW.md`: step 5 and
  the corrective-form paragraph name `harnessctl check . --artifact WO-...`.
- Notes: the reference's command table (the `check` row carries the
  context, the `next` row says alias, the `accept-candidate` row and
  section are gone), the check note, the qualification-roles note.
- `SPEC-ECP-001`: one amendment record (`ECP-CTX-008`).
- Tests: `NextCommandTests` becomes `ExecutionContextTests` (nine tests:
  context and default artifact, alias byte identity and notice, checkpoint
  without artifact, manifest by phase, selection counts, records and
  refusal, writes nothing, corrective, word census and `--help`); the
  `WEX210` corrective in `tests/test_workflow_compliance.py`; the alias
  test in `tests/test_release_qualification.py` becomes the guard test; the
  projection golden digest moves from `b8ccd288…` to `c307910a…` because
  the block gains the `Context` section (`ECP-CTX-003`), recorded in the
  test's docstring.

## Tests

- `check .` with one `in_progress` work order: `operation.kind == "check"`,
  the six context members, `context.next` equal to the handoff checkpoint's
  step, the same result as `check --artifact WO-001`, a `Context` section
  after `Command or response` in the human block, `restitution_digest`
  reproducing `result_sha256`.
- `next` against `check` with and without `--artifact`: identical stdout,
  identical human block, `check` silent on standard error, `next` one line
  naming `harnessctl check`.
- `check --checkpoint start` without `--artifact`: exit 2, empty stdout,
  `WEX210: --artifact is required with --checkpoint`.
- `check .` with zero and two `in_progress` work orders: `blocked`,
  `WEX-ECP-001` with the count and the ids.
- A ready record and a requirement through `check`: the record's context;
  `check accepts only WO, VREC, or RLS`.
- Tree digest before and after `check .`: equal.
- A blocked `check --checkpoint start`: the corrective is `harnessctl check
  . --artifact WO-404`; no `"next", "."` anywhere in the result.
- `accept-candidate`: exit 2, empty stdout, one stderr line naming `qualify
  candidate-package`, the qualification handler not called, no output file,
  and `--help` without the word.
- Word census: the template `WORKFLOW.md` has no `harnessctl next`; the
  reference has one `next` row saying alias, no `harnessctl next [`
  synopsis, no `accept-candidate` row or invocation; the check note has no
  `harnessctl next`; the roles note says `removed after 0.11.0`.
- The reference's command table still equals the parser's subcommand set
  (`test_command_reference_exactly_covers_current_cli`).

## Suite readings

Windows workstation, candidate source, `scripts/run_tests.py`: 1146 tests, 1 error, 26 skipped, the error being the baseline `test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref` that precedes this work order; the nine suites this work order touches or pins (workflow execution, compliance, release qualification, progressive documentation, harnessctl, standard lifecycle, documentation contract, agentic execution, validation taxonomy): 469 tests, OK, 8 skipped. Linux: the pull request's lanes at the completion commit.

## Demonstration on this repository

Candidate CLI on this checkout, where `WO-ECP-019` is the single
`in_progress` work order:

- `harnessctl check .` (no artifact): selects `WO-ECP-019`, renders the
  `Context` section with the twelve-file reading manifest and `Next argv:
  harnessctl check . --artifact WO-ECP-019 --checkpoint handoff
  (PROC-WO-IMPLEMENT/STEP-WO-IMPLEMENT-CHECK)`; standard error empty;
- `harnessctl next . --json` and `harnessctl check . --json`: identical
  bytes (`operation.kind = check`, `result_sha256 = 82de1741…`), `next`
  printing `harnessctl: next is an alias of check and is removed after the
  release carrying this notice; run harnessctl check [--artifact ID]`;
- `harnessctl accept-candidate --wheel x.whl`: exit 2, `harnessctl:
  accept-candidate was removed after 0.11.0; run harnessctl qualify
  candidate-package --candidate-wheel PATH …`;
- `harnessctl check . --checkpoint start`: exit 2, `WEX210: --artifact is
  required with --checkpoint`.

## Readings under the 0.11.0 root

- `validate .`: 1160 artifacts, 0 errors, 485 warnings.
- `doctor .`: 0 FAIL.
- `validate_release_distributions.py`: PASS (8 records).
- Start preflight for `WO-ECP-019`: PASS over `7148b57`.

## Deviations, recorded for the completion decision

1. **The reference keeps a `next` row.** `ECP-CTX-007` says the reference
   "folds the `next` synopsis into `check`"; the synopsis line is gone and
   the paragraph is `check`'s, but the command table keeps one row for
   `next`, marked as the deprecated alias, because
   `test_command_reference_exactly_covers_current_cli` pins the table to
   the parser's subcommand set and the alias is a subcommand for the
   window. The row goes with the alias.
2. **`workflow_result.py` is unchanged.** The scope admitted it in case the
   `Context` section depended on the operation kind; it does not.

## Complete changed-path set

Every path this work order changed since `main` at `970a0ae`, packet
included, as Git derived it; the handoff check completed at its fixed point
with every predicate of `QG-G4-IMPLEMENTATION-EVIDENCE` passing, run by
the released 0.11.0 evaluator on this Windows checkout: see `handoff.json`
beside this file.
