```toml
artifact = "WO-ECP-026"
checkpoint = "handoff"
formal_snapshot_sha256 = "eb32aee74cfeb7873ba632ae5c14b93367325a969f7ab677e2ed6f1f22f4eab8"
rebound_at = "2026-09-06T11:17:34Z"
```

# WO-ECP-026 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

`init` is the one installation command. Its behaviour follows the target's
content: an absent or empty target receives the complete standard harness,
as before; a target with content keeps its ordinary files, receives the
bounded fragments in `AGENTS.md`, `CLAUDE.md` and `.gitignore`, and gets
`docs/engineering/ADOPTION_REPORT.md`, as `adopt` did before. `adopt` is no
longer registered: argparse refuses it as any unknown command, exit status
2, empty standard output, the usage error on standard error, no guard and
no product message. The installer's planner lost the empty-directory
refusal and the init/adopt distinction and refuses any mode other than
`init` and `upgrade`. The lock-floor diagnostic names `harnessctl init`.
`--dry-run` carries a help sentence on `init`, `scaffold-domain` and
`create-artifact`. The README, the command reference and the installation
note read accordingly, and the reference states the plan-and-write
convention once. Seven definitions close their `adopt` wording by dated
amendment record. Nine `adopt` invocations in `tests/test_harnessctl.py`
and one each in `tests/test_glossary.py` and
`tests/test_repository_context_retirement.py` became `init` with their
assertions byte for byte; one new test pins the report's presence per
target state and the `"command": "init"` result in both. No managed
template, contract file, result schema, skill, workflow, lock format or
`upgrade` behaviour changed.

## Evaluators

- Governing: released `se-harness 0.15.0` outside the checkout
  (`C:/Users/mathi/se-harness-eval-0150`), `-I`, wheel-installed, for
  every governing reading, this packet and the handoff check.
- Candidate: this checkout, branch `wo/ecp-026-merge-init-adopt` off
  `main` at `9598859` (the merge of the approved packet, PR #359); `main`
  merged in at `7642132` (PR #358, a technical-communication packet that
  touches no path of this work order) before the handoff check below.

## Readings (VER-ECP-022)

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| `validate --advisories` | exact 0.15.0 | Errors: 0, Warnings: 71 (the `main` baseline), Advisories: 0 |
| `doctor` | exact 0.15.0 | 116 PASS, 0 FAIL |
| review preflight `--work-order WO-ECP-026` | exact 0.15.0 | PASS |
| `scripts/validate_release_distributions.py` | candidate | PASS, 12 distribution-bearing records |
| `harnessctl --help`, `harnessctl init --help` | candidate | the command list reads `init` and no `adopt`; `--dry-run` shows "report the complete plan without writing" (`ECP-INS-001`, `ECP-INS-008`) |
| `harnessctl adopt .` | candidate | exit 2, 0 bytes on standard output, argparse "invalid choice: 'adopt'" on standard error (`ECP-INS-006`) |
| `init EMPTY --dry-run --json` | candidate | `command: init`, `completed`, `written: false`, 48 changes, no `docs/engineering/ADOPTION_REPORT.md` (`ECP-INS-002`, `ECP-INS-005`) |
| `init RUST --dry-run --json` (a folder with `Cargo.toml` and an owner `AGENTS.md`) | candidate | `command: init`, `completed`, `written: false`, 49 changes, `AGENTS.md` `integrate`, `docs/engineering/ADOPTION_REPORT.md` `add` (`ECP-INS-003`, `ECP-INS-005`) |
| `python -m unittest tests.test_harnessctl tests.test_cli_shape tests.test_glossary tests.test_repository_context_retirement tests.test_mutation_guard` | candidate, Windows 11 | OK, 72 tests, 1 skipped (the Windows-only guard) |
| `python scripts/run_tests.py` | candidate, Windows 11 | section below |
| `check --checkpoint handoff --from-git 7642132` | exact 0.15.0 | section below |

### The Windows suite

`python scripts/run_tests.py` on this Windows 11 workstation (CPython 3.14,
CRLF checkout), two readings:

- At the implementation commit `ab2b8e3`: 1,250 tests, 26 skipped, 1 error
  and 1 failure. The error is the known Windows baseline name present on
  `main` and outside this work order
  (`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`,
  a `PermissionError` on a temporary `.git` object). The failure was
  `test_public_onboarding.PublicOnboardingTests.test_quick_start_commands_parse_against_the_current_cli`,
  which pinned the README quick-start set to `init`, `adopt`, `doctor`; the
  path was outside the declared scope and is the subject of the scope
  amendment of 2026-09-06 recorded on the work order.
- After the amendment and the one-assertion edit: 1,250 tests, 26 skipped,
  1 error (the same baseline name), 0 failures. No other name differs.

### Handoff check

`check . --artifact WO-ECP-026 --checkpoint handoff --from-git 7642132`,
exact 0.15.0, after the merge of `main`: Completed; every `QGP-G4I-*` predicate passes; every changed
path inside the declared scope as amended; `complete: true`; the
self-binding result retained as `handoff.json` beside this packet.

## Material non-effects

`upgrade`, `doctor`, the managed templates, the lock format, the adoption
report's content and path, the result schema, the skills and the workflows
are unchanged. The mutation-guard inventory is unchanged: `init` was not in
it and does not enter it. The plan/apply and dry-run flags of the eight
writing commands did not move; the reference states the convention. The
`candidate-evidence` workflow's bare `init` is unaffected: an absent target
follows the same path as before.

## Hosted lanes

Read on the pull request at the completion decision; recorded in the
completion event's reason.
