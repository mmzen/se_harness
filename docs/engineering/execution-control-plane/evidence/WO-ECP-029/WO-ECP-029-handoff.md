```toml
artifact = "WO-ECP-029"
checkpoint = "handoff"
formal_snapshot_sha256 = "0ef2097560dbd268da82547bbeac60e9ae73d0324d8ddbf19129b6dcf7f3f56d"
rebound_at = "2026-09-07T20:52:54Z"
```

# WO-ECP-029 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The `adopt` alias window `WO-ECP-026` opened on 2026-09-06 is closed. The
parser registers `init` only; `harnessctl adopt` is refused by argparse as
any unknown command, exit 2, with no guard and no product message naming a
replacement. The pinned repository-command set in `tests/test_cli_shape.py`
has no `adopt`, the alias test in `tests/test_harnessctl.py` is gone, and
the command reference lost the `adopt` inventory row and synopsis line.
Four dated amendment records close the alias-window records on
`SPEC-ECP-020`, `REQ-ECP-031`, `VER-ECP-022` and `SPEC-ECP-016`.
`candidate_acceptance.SCENARIO_IDS` keeps the scenario id `adopt`, so the
acceptance contract digest is unchanged. No managed path, result schema or
other command changed.

## Evaluators

- Governing: released `se-harness 0.16.0` outside the checkout
  (`C:/Users/mathi/se-harness-eval-0160`), `-I`, wheel-installed, for every
  governing reading, this packet and the handoff check. Its candidate
  acceptance runs `init` in the `adopt` scenario, which is why the alias can
  go now (`REQ-ECP-030`).
- Candidate: this checkout, branch `wo/ecp-029-adopt-alias` off `main` at
  `429e64c` (the merge of PR #388, the last of the wave 1 packet).

## Readings (VER-ECP-024, group B)

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| `validate --advisories` | exact 0.16.0 | Errors: 0, Warnings: 73 (the `main` baseline), Advisories: 0 |
| `doctor` | exact 0.16.0 | 0 FAIL |
| review preflight `--work-order WO-ECP-029` | exact 0.16.0 | PASS |
| `harnessctl --help` before | candidate | one `adopt` line |
| `harnessctl adopt . --dry-run --json` before | candidate | ran, exit 1 (a conflict result on this root) |
| `harnessctl --help` after | candidate | no `adopt` line (`ECP-DEL-015`) |
| `harnessctl adopt .` after | candidate | exit 2, empty stdout, argparse "invalid choice" usage error (`ECP-DEL-015`) |
| `python -m unittest tests.test_cli_shape tests.test_harnessctl tests.test_progressive_documentation tests.test_public_onboarding` | candidate, Windows 11 | OK, 84 tests, 1 skipped: the parser-shape set, the reference-covers-parser test and the README quick-start test all hold (`ECP-DEL-016`, `-017`) |
| `python scripts/run_tests.py` | candidate, Windows 11 | section below |
| `check --checkpoint handoff --from-git 429e64c` | exact 0.16.0 | section below |

### The Windows suite

`python scripts/run_tests.py` at `fe029cf` on this Windows 11 workstation
(CPython 3.14, CRLF checkout): 1,286 tests, 26 skipped, 1 error and 1
failure, both the names of this machine's baseline on `main`
(`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`,
a `PermissionError` on a temporary `.git` object;
`test_instruction_architecture.OwnerInstructionRegionTests.test_owner_region_stays_within_the_size_bound`,
the `AGENTS.md` owner region measured on a CRLF checkout, recorded on a
fresh worktree of `main` under `WO-ECP-027`). One test fewer than before:
the alias test. No other name differs.

### Handoff check

`check . --artifact WO-ECP-029 --checkpoint handoff --from-git 429e64c`,
exact 0.16.0: Completed; every `QGP-G4I-*` predicate passes; every changed
path inside the declared scope; `complete: true`; the self-binding result
retained as `handoff.json` beside this packet.

## Material non-effects

`init` is unchanged; `installer.plan_install` is unchanged; the acceptance
scenario list and its digest are unchanged; no managed path moved; groups A
and C of the wave are untouched.

## Hosted lanes

Read on the pull request at the completion decision; recorded in the
completion event's reason.
