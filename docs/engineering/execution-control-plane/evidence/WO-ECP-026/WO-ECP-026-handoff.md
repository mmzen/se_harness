```toml
artifact = "WO-ECP-026"
checkpoint = "handoff"
formal_snapshot_sha256 = "9dae3fed87f1800188ed0d6ddaa38d833b83a2e1571d36c33f3d51c1ab781316"
rebound_at = "2026-09-06T11:34:31Z"
```

# WO-ECP-026 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

`init` is the one installation command. Its behaviour follows the target's
content: an absent or empty target receives the complete standard harness,
as before; a target with content keeps its ordinary files, receives the
bounded fragments in `AGENTS.md`, `CLAUDE.md` and `.gitignore`, and gets
`docs/engineering/ADOPTION_REPORT.md`, as `adopt` did before. For the 0.16.0
release only, `adopt` stays registered as a plain alias of `init` (same
options, same handler, `"command": "init"` in the result), because the
released 0.15.0 verifier's candidate acceptance invokes it; the owner opened
this one-release window on 2026-09-06 (second scope amendment, amendment
records on `REQ-ECP-031`, `SPEC-ECP-020`, `VER-ECP-022`, `SPEC-ECP-016`).
The candidate's own acceptance keeps the scenario id `adopt` and runs `init`
on a folder with content, so the successor verifier no longer invokes the
alias and a follow-up work order removes it under `REQ-ECP-030`. The
installer's planner lost the empty-directory
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
| `harnessctl --help`, `harnessctl init --help` | candidate | `init` is "install the standard harness into an absent, empty or existing repository"; `adopt` is "alias of init, kept for the 0.16.0 release only"; `--dry-run` shows "report the complete plan without writing" (`ECP-INS-001` as amended, `ECP-INS-008`) |
| `harnessctl adopt FOLDER` (a folder holding `README.md`) | candidate | exit 0, the harness and `docs/engineering/ADOPTION_REPORT.md` written; `test_adopt_is_a_plain_alias_of_init_for_one_release` pins `"command": "init"` and the same `changes` as `init` (`ECP-INS-006` as amended) |
| `harnessctl adopt .` before the alias window (implementation commit `ab2b8e3`) | candidate | exit 2, 0 bytes on standard output, argparse "invalid choice: 'adopt'" on standard error; superseded by the owner's decision of 2026-09-06 |
| `init EMPTY --dry-run --json` | candidate | `command: init`, `completed`, `written: false`, 48 changes, no `docs/engineering/ADOPTION_REPORT.md` (`ECP-INS-002`, `ECP-INS-005`) |
| `init RUST --dry-run --json` (a folder with `Cargo.toml` and an owner `AGENTS.md`) | candidate | `command: init`, `completed`, `written: false`, 49 changes, `AGENTS.md` `integrate`, `docs/engineering/ADOPTION_REPORT.md` `add` (`ECP-INS-003`, `ECP-INS-005`) |
| `python -m unittest tests.test_harnessctl tests.test_cli_shape tests.test_glossary tests.test_repository_context_retirement tests.test_mutation_guard` | candidate, Windows 11 | OK, 72 tests, 1 skipped (the Windows-only guard) |
| `python -m unittest tests.test_harnessctl tests.test_cli_shape tests.test_public_onboarding tests.test_release_qualification` after the alias window | candidate, Windows 11 | OK, 67 tests, 1 skipped |
| hosted `Candidate package evidence` lane (released 0.15.0 verifier, `qualify candidate-package`) | released verifier | at `144ac9c`: "candidate acceptance failed: adopt", the finding behind the alias window; re-read at the alias commit in the completion event |
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
- After the alias window (second scope amendment): a third reading found
  1,251 tests, 26 skipped, 1 error (the same baseline name) and 1 failure,
  `test_progressive_documentation.ProgressiveDocumentationTests.test_command_reference_exactly_covers_current_cli`,
  because the reference's inventory must cover every registered command
  and the alias had no row; the row was added (in scope). The fourth
  reading: 1,251 tests, 26 skipped, 1 error (the same baseline name),
  0 failures. No other name differs.

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
acceptance contract digest is unchanged: the scenario ids are the same ten. The
`candidate-evidence` workflow's bare `init` is unaffected: an absent target
follows the same path as before.

## Hosted lanes

Read on the pull request at the completion decision; recorded in the
completion event's reason.
