```toml
artifact = "WO-ECP-020"
checkpoint = "handoff"
formal_snapshot_sha256 = "5e293e81cd67b889ed2cdd0654790351a84d734be0485d472b48c9dd89a27f55"
rebound_at = "2026-08-29T20:58:10Z"
```

# WO-ECP-020 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

`harnessctl` has no `next` subcommand: the parser does not register it,
`--help` does not list it, and a pre-parse guard makes `harnessctl next`
exit with status 2, empty standard output and one line on standard error
naming `harnessctl check` (with the `--artifact` the caller gave, when it
gave one). The reference has no `next` row and the check note says the
command was removed after 0.11.0. `REQ-ECP-025`, `SPEC-ECP-014` and
`VER-ECP-016` carry the amendment records the owner's decision required
(`ECP-CTX-004` and `ECP-CTX-007` as amended).

## Evaluators

- Governing: released `se-harness 0.11.0` outside the checkout, `-I`, on
  this Windows checkout for every reading, the packet and the handoff check
  included.
- Candidate: this checkout, branch `wo/ecp-020-remove-next` stacked on
  `wo/ecp-019-context-and-aliases` at `WO-ECP-019`'s completion commit
  `ee1e6af`; the suite and the demonstration run candidate source.

## Change

- `se_harness/cli.py`: the `next` parser, `_next` and its notice deleted;
  the guard beside the `focus` and `accept-candidate` guards.
- `tests/test_workflow_execution.py`: the alias test becomes
  `test_next_is_no_subcommand_and_names_check` (refusal with and without
  `--artifact`, `--help` census); the word-census test asserts no `next`
  row; the human-block test no longer drives `next`.
- `docs/notes/harnessctl-reference.md` (row and paragraph),
  `docs/notes/harnessctl-check.md` (one bullet).
- Amendment records on `REQ-ECP-025`, `SPEC-ECP-014` (`ECP-CTX-004`
  restated in place as the guard; `ECP-CTX-007`, the "alias window" term,
  the failure and compatibility paragraphs) and `VER-ECP-016` (the alias
  row is the refusal row; scenario 2; census; residual uncertainty); the
  domain index.

## Tests

- `next` with and without `--artifact WO-001`: exit 2, empty stdout, one
  stderr line naming `harnessctl check --artifact WO-001` or `harnessctl
  check [--artifact ID]`; `--help` without `next`.
- Every other row of `VER-ECP-016` as `WO-ECP-019` left it: context,
  default artifact, checkpoint without artifact, manifest by phase,
  selection counts, records and refusal, writes nothing, corrective,
  `accept-candidate` guard, word census (now also no `next` row), the
  reference's table equal to the parser's subcommand set.

## Suite readings

Windows workstation, candidate source, `scripts/run_tests.py`: 1152 tests, 1 error, 26 skipped, the error being the baseline `test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref` that precedes this work order; the nine suites `WO-ECP-019` pinned: 475 tests, OK, 8 skipped. Linux: the pull request's lanes at the completion commit.

## Demonstration on this repository

Candidate CLI on this checkout:

- `harnessctl next .`: exit 2, `harnessctl: next was removed after 0.11.0;
  run harnessctl check [--artifact ID] (add --json for the structured
  result)`;
- `harnessctl next . --artifact WO-ECP-020 --json`: exit 2, `… run
  harnessctl check --artifact WO-ECP-020 …`;
- `harnessctl --help`: no `next`.

## Readings under the 0.11.0 root

- `validate .`: 1166 artifacts, 0 errors, 485 warnings.
- `doctor .`: 0 FAIL.
- `validate_release_distributions.py`: PASS (8 records).
- Start preflight for `WO-ECP-020`: PASS with no diagnostics over
  `d936295`, after the unrelated architecture relations were removed
  (`W021` for `ARCH-ECP-001`, `W017` for `ADR-ECP-007`); like `WO-ECP-010`,
  the work order declares no architecture relation.

## Deviations, recorded for the completion decision

None.

## Complete changed-path set

Every path this work order changed since its base, `WO-ECP-019`'s
completion commit `ee1e6af`, packet included, as Git derived it; the
handoff check completed at its fixed point with every predicate of
`QG-G4-IMPLEMENTATION-EVIDENCE` passing, run by the released 0.11.0
evaluator on this Windows checkout: see `handoff.json` beside this file.
