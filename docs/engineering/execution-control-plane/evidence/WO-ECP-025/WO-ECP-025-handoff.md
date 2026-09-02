```toml
artifact = "WO-ECP-025"
checkpoint = "handoff"
formal_snapshot_sha256 = "03f54c932e0c830ea79ce26259448e8a5959c2ad1b52055c8f03502d8f0d17ec"
rebound_at = "2026-09-02T14:58:09Z"
```

# WO-ECP-025 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The four tombstone guards are gone from `main()` in `se_harness/cli.py`:
`focus`, `next`, `accept-candidate` and `prepare-release --authorized-by`,
thirty-nine lines. Each name is now refused by argparse as any unknown
command or option is: exit status 2, empty standard output, the usage error
on standard error, no product message naming a replacement. Three refusal
tests became one absence test that reads `--help` and `main()`'s source;
the `--authorized-by` assertion became argparse's usage error. Three notes
state the plain refusal. `REQ-ECP-024`, `SPEC-ECP-013`, `SPEC-ECP-014`,
`SPEC-ECP-016`, `VER-ECP-013` and `VER-ECP-016` close their guard rules by
dated amendment record. No registered command, option, result schema,
contract file or managed path changed.

## Evaluators

- Governing: released `se-harness 0.14.0` outside the checkout
  (`C:/Users/hok/se-harness-eval-0140`), `-I`, wheel-installed, for every
  reading, this packet and the handoff check.
- Candidate: this checkout, branch `wo/ecp-025-execution` off `main` at
  `2689b5e`; implementation commit `4212f0e`.

## The delegated route (ECP-TMB-007)

The gate is `.engineering-harness.delegation.toml` (`github-checks`,
`check_name = "validate"`, `base_ref = "origin/main"`), the check the
default branch's ruleset requires. Each mechanical decision is taken on the
evaluator's own restitution naming `delegated-executor` with a bound
command, and each lifecycle event records the class, the check-run id and
the exact head:

- `DR-WO-START`: taken at head `68af51f`, check-run `100294830645`,
  conclusion success.
- `DR-WO-COMPLETE` and `DR-VREC-PREPARE`: recorded below as they are
  taken, each on a fresh green reading of its own head.

The approval that granted the class, the verification of the prepared
record, and both merges are human decisions.

## Readings (VER-ECP-021)

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| `validate --advisories` | exact 0.14.0 | Artifacts: 1259 | Errors: 0 | Warnings: 69 | Advisories: 0 |
| `doctor` | exact 0.14.0 | 0 FAIL |
| review preflight `--work-order WO-ECP-025` | exact 0.14.0 | PASS |
| `main()` source and `--help` | candidate | `test_retired_names_are_unknown_to_the_parser`: none of the four names in `main()`'s source; `--help` lists none of the three commands; each invocation exits 2 with argparse's "invalid choice" and no "was removed" text |
| `prepare-release --authorized-by` | candidate | argparse usage error naming the required `--owner`, exit 2, no "was renamed" text (`test_prepare_release_names_its_actor_owner_and_knows_no_authorized_by`) |
| `python -m unittest tests.test_workflow_execution tests.test_release_qualification tests.test_cli_shape` | candidate, Windows 11, `PYTHONUTF8=1` | OK after the edits (244 tests across the three modules at the first run, 22 in the two smaller modules at the re-run) |
| `PYTHONUTF8=1 python scripts/run_tests.py --scale full` | candidate, Windows 11 | section below |
| `check --checkpoint handoff --from-git 2689b5e` | exact 0.14.0 | section below |

### The Windows suite

Recorded when the run completes.

### Handoff check

Recorded with its self-binding result beside this packet.

## Material non-effects

No registered command, option, result schema, contract JSON, managed
template, release or publication changed; the other one-release
acceptances the specifications name (`SPEC-ECP-001`, `SPEC-ECP-002`,
`SPEC-ECP-004`) are untouched observations for their own work orders.

## Hosted lanes

Recorded when the lanes complete at the pull request's head.
